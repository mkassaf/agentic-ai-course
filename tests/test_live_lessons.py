"""Exercise the failure paths hidden by the default scripted notebook runs."""
import ast
import contextlib
import io
import json
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]


def code_cells(slug):
    lesson = json.loads((ROOT / "lessons" / f"{slug}.json").read_text())
    return [cell["source"] for cell in lesson["cells"] if cell["type"] == "code"]


def quiet_exec(source, namespace):
    with contextlib.redirect_stdout(io.StringIO()):
        exec(source, namespace)


def load_function(source, name, namespace):
    node = next(node for node in ast.parse(source).body
                if isinstance(node, ast.FunctionDef) and node.name == name)
    exec(compile(ast.Module(body=[node], type_ignores=[]), "<lesson>", "exec"), namespace)


class LiveRetryTests(unittest.TestCase):
    def test_a2a_adapter_keeps_provider_fields_out_of_the_internal_model(self):
        ns = {}
        quiet_exec(code_cells("13_a2a_protocol")[0], ns)
        reply = json.loads(ns["payment_adapter"](json.dumps(
            {"id": "pi-17", "status": "succeeded", "amount_received": 4200,
             "currency": "eur", "metadata": {"order_id": "order-17"}})))
        self.assertNotIn("amount_received", reply)
        self.assertNotIn("metadata", reply)
        self.assertNotIn("error", reply)
        for bad in [True, False, "4200", -1]:
            request = {"id": "pi-17", "status": "succeeded", "amount_received": bad,
                       "currency": "eur", "metadata": {"order_id": "order-17"}}
            self.assertIn("error", json.loads(ns["payment_adapter"](json.dumps(request))))

    def test_langgraph_retries_every_project_and_stops_after_two_failures(self):
        cells = code_cells("14_frameworks_langgraph")
        prompts = []

        def ask(prompt, *, example):
            self.assertEqual(example, "")
            prompts.append(prompt)
            return json.dumps({"orderId": "string", "amount": "number"})  # breaks the old total field

        ns = {"MODE": "live", "ask": ask}
        for cell in cells[:3]:
            quiet_exec(cell, ns)
        ns["scripted"].clear()
        for project in ns["projects"]:
            result = ns["app"].invoke({"project": project})
            self.assertEqual(result["attempts"], 2)
            self.assertFalse(result["passed"])
        self.assertEqual(len(prompts), 2 * len(ns["projects"]))
        self.assertTrue(all("Do not rename total" in prompt for prompt in prompts[1::2]))


class SkillContractTests(unittest.TestCase):
    def run_skill(self, ask):
        cells = code_cells("12_agent_skills")
        ns = {"ask": ask, "choice": "saga-adr",
              "skills": {"saga-adr": {"body": "Review the checkout saga."}}}
        quiet_exec(cells[3], ns)
        quiet_exec(cells[4], ns)

    def test_explanation_in_decision_is_repaired_without_weakening_the_checker(self):
        prompts = []

        def ask(prompt, *, example):
            prompts.append(prompt)
            if len(prompts) == 1:
                return example.replace("Decision: compensate", "Decision: compensate, because payment failed")
            return example

        self.run_skill(ask)
        self.assertEqual(len(prompts), 3)
        self.assertIn("Decision contains only", prompts[0])
        self.assertIn("Your last reply:", prompts[1])
        self.assertIn("Fix these problems:", prompts[1])

    def test_invalid_skill_output_still_fails_after_the_repair_budget(self):
        prompts = []

        def ask(prompt, *, example):
            prompts.append(prompt)
            return "Decision: ignore the payment failure"

        with self.assertRaises(AssertionError):
            self.run_skill(ask)
        self.assertEqual(len(prompts), 2)


class MemoryScopeTests(unittest.TestCase):
    def test_similar_but_out_of_scope_memory_never_enters_the_search_prompt(self):
        cells = code_cells("08_human_feedback_memory")
        prompts, queries = [], []
        stored_lesson = "Past case: Pricing quote; idempotent read and transient failure; bounded retry with jitter."

        class Memory:
            def query(self, **kwargs):
                queries.append(kwargs)
                # A semantic false positive: Search would be the closer match without a scope filter.
                scope = kwargs.get("where")
                approved = {"$and": [{"idempotent": True}, {"transient": True}]}
                records = [{"lesson": stored_lesson}] if scope is None or scope == approved else []
                return {"distances": [[0.22] if records else []], "metadatas": [records]}

        def ask(prompt, *, example):
            prompts.append(prompt)
            return example

        ns = {"ask": ask, "memory": Memory()}
        quiet_exec(cells[0], ns)
        load_function(cells[2], "recall", ns)
        quiet_exec(cells[3], ns)
        prompts.clear()
        quiet_exec(cells[4], ns)
        self.assertEqual(ns["scores"], {"before": 1, "after": 2})
        self.assertIn(stored_lesson, prompts[2])
        self.assertNotIn(stored_lesson, prompts[3])
        self.assertEqual(queries[-1]["where"], {"$and": [{"idempotent": False}, {"transient": True}]})
        self.assertEqual(queries[-2]["where"], {"$and": [{"idempotent": True}, {"transient": True}]})

    def test_a_flat_learning_result_is_reported_instead_of_asserted_away(self):
        cells = code_cells("08_human_feedback_memory")
        ns = {"case": "feedback case", "held_out": [("new case", False, True, "do not retry")],
              "recall": lambda *args, **kwargs: [],
              "council": lambda *args, **kwargs: "do not retry"}
        quiet_exec(cells[4], ns)
        self.assertEqual(ns["scores"], {"before": 1, "after": 1})


if __name__ == "__main__":
    unittest.main()
