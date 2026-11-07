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
    def test_a2a_live_retry_never_reads_the_practice_answers(self):
        prompts = []

        def ask(prompt, *, example):
            self.assertEqual(example, "")
            prompts.append(prompt)
            return "modular monolith"

        ns = {"MODE": "live", "ask": ask}
        quiet_exec(code_cells("13_a2a_protocol")[2], ns)
        for project in ns["projects"]:
            ns["scripted"].clear()  # live behavior must be independent of these fixtures
            self.assertEqual(ns["propose"](project, "Policy check failed; revise."), "modular monolith")
        self.assertEqual(len(prompts), 4)
        self.assertTrue(all("Policy check failed" in prompt for prompt in prompts))

    def test_langgraph_retries_every_project_and_stops_after_two_failures(self):
        cells = code_cells("14_frameworks_langgraph")
        prompts = []

        def ask(prompt, *, example):
            self.assertEqual(example, "")
            prompts.append(prompt)
            return "serverless"  # deliberately fails both attempts

        ns = {"MODE": "live", "ask": ask}
        for cell in cells[:3]:
            quiet_exec(cell, ns)
        ns["scripted"].clear()
        for project in ns["projects"]:
            result = ns["app"].invoke({"project": project})
            self.assertEqual(result["attempts"], 2)
            self.assertFalse(result["passed"])
        self.assertEqual(len(prompts), 8)
        self.assertTrue(all("failed a check" in prompt for prompt in prompts[1::2]))


class SkillContractTests(unittest.TestCase):
    def run_skill(self, ask):
        cells = code_cells("12_agent_skills")
        ns = {"ask": ask, "choice": "architecture-decision",
              "skills": {"architecture-decision": {"body": "Apply the course policy."}}}
        quiet_exec(cells[3], ns)
        quiet_exec(cells[4], ns)

    def test_explanation_in_decision_is_repaired_without_weakening_the_checker(self):
        prompts = []

        def ask(prompt, *, example):
            prompts.append(prompt)
            if len(prompts) == 1:
                return example.replace("Decision: modular monolith", "Decision: modular monolith, because the team is small")
            return example

        self.run_skill(ask)
        self.assertEqual(len(prompts), 3)
        self.assertIn("Decision must contain only", prompts[0])
        self.assertIn("Your last reply:", prompts[1])
        self.assertIn("Fix these problems:", prompts[1])

    def test_invalid_skill_output_still_fails_after_the_repair_budget(self):
        prompts = []

        def ask(prompt, *, example):
            prompts.append(prompt)
            return "Decision: serverless"

        with self.assertRaises(AssertionError):
            self.run_skill(ask)
        self.assertEqual(len(prompts), 2)


class MemoryScopeTests(unittest.TestCase):
    def test_similar_but_out_of_scope_memory_never_enters_the_search_prompt(self):
        cells = code_cells("08_human_feedback_memory")
        prompts, queries = [], []
        stored_lesson = "Past case: Payments platform; one operations engineer; use modular monolith."

        class Memory:
            def query(self, **kwargs):
                queries.append(kwargs)
                # A semantic false positive: Search would be the closer match without a scope filter.
                records = [] if kwargs.get("where") == {"ops_engineers": 4} else [{"lesson": stored_lesson}]
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
        self.assertEqual(queries[-1]["where"], {"ops_engineers": 4})
        self.assertEqual(queries[-2]["where"], {"ops_engineers": 1})

    def test_a_flat_learning_result_is_reported_instead_of_asserted_away(self):
        cells = code_cells("08_human_feedback_memory")
        ns = {"case": "feedback case", "held_out": [("new case", 4, "microservices")],
              "recall": lambda *args, **kwargs: [],
              "council": lambda *args, **kwargs: "microservices"}
        quiet_exec(cells[4], ns)
        self.assertEqual(ns["scores"], {"before": 1, "after": 1})


if __name__ == "__main__":
    unittest.main()
