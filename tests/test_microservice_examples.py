"""Behavior checks for the microservices quiz, tool, and agent examples."""
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


class MicroserviceQuizTests(unittest.TestCase):
    def setUp(self):
        cells = code_cells("00_rules_and_llms")
        self.ns = {}
        quiet_exec(cells[0], self.ns)
        quiet_exec(cells[1], self.ns)

    def test_retries_require_transient_failure_and_idempotency(self):
        for transient in (False, True):
            for idempotent in (False, True):
                with self.subTest(transient=transient, idempotent=idempotent):
                    case = {"name": "test", "kind": "retry", "transient": transient, "idempotent": idempotent}
                    expected = "A" if transient and idempotent else "B"
                    ns = {"cases": [case]}
                    quiet_exec(code_cells("00_rules_and_llms")[1], ns)
                    self.assertEqual(ns["rule_answers"]["test"], expected)

    def test_scenarios_have_the_expected_answers(self):
        actual = [self.ns["rule_answers"][case["name"]] for case in self.ns["cases"]]
        self.assertEqual(actual, ["A", "B", "A", "B", "A", "C", "B"])
        with self.assertRaises(ValueError):
            quiet_exec(code_cells("00_rules_and_llms")[1], {"cases": [{"kind": "unknown"}]})


class ToolAgentTests(unittest.TestCase):
    def setUp(self):
        self.ns = {}
        self.cells = code_cells("04_why_tools")
        for cell in self.cells[:4]:
            quiet_exec(cell, self.ns)

    def test_extract_validate_and_escape_html(self):
        data = self.ns["extract_service"]("Orders")
        self.assertEqual(self.ns["validate_service"](data), "Valid")
        self.assertIn("Sales team", self.ns["format_html"](data))
        self.assertEqual(self.ns["validate_service"]({}), "Invalid: missing name")
        self.assertEqual(self.ns["format_html"]({"name": "Orders"}), "Cannot format an invalid record.")
        data["name"] = "<script>"
        self.assertIn("&lt;script&gt;", self.ns["format_html"](data))
        self.assertEqual(self.ns["extract_service"]("missing"), {})

    def test_agent_receives_system_prompt_and_tool_results(self):
        replies = iter([
            '{"tool":"extract_service","name":"orders"}',
            '{"tool":"validate_service"}',
            '{"tool":"format_html"}',
            '{"tool":"finish","answer":"Done"}',
        ])
        calls = []
        class Client:
            def ask(self, prompt, *, system):
                calls.append((prompt, system))
                return next(replies)
        self.ns["client"] = Client()
        quiet_exec(self.cells[4], self.ns)
        self.assertIn("extract_service", calls[0][1])
        self.assertIn("Sales team", calls[1][0])
        self.assertIn("Valid", calls[2][0])
        self.assertIn("<h2>Orders</h2>", calls[3][0])

    def test_invalid_requests_cannot_format(self):
        replies = iter(['{"tool":"format_html"}', '{"tool":"finish","answer":"Stopped"}'])
        class Client:
            def ask(self, prompt, *, system):
                return next(replies)
        self.ns["client"] = Client()
        quiet_exec(self.cells[4], self.ns)
        self.assertIn("extract and validate", self.ns["history"])


class ReActObservationTests(unittest.TestCase):
    def run_actions(self, actions):
        cells = code_cells("05_react_agent")
        ns = {}
        quiet_exec(cells[0], ns)
        quiet_exec(cells[1], ns)
        steps = iter(actions)
        ns["ask"] = lambda prompt: json.dumps(next(steps))
        quiet_exec(cells[2], ns)
        return ns

    def test_failed_or_wrong_target_lookup_cannot_unlock_finish(self):
        for service in ("stock", "Payments"):
            with self.subTest(service=service), self.assertRaisesRegex(ValueError, "successfully"):
                self.run_actions([
                    {"action": "read_metrics", "input": service},
                    {"action": "finish", "input": "circuit breaker"},
                ])

    def test_agent_can_recover_by_observing_the_target_after_a_failed_lookup(self):
        ns = self.run_actions([
            {"action": "read_metrics", "input": "stock"},
            {"action": "read_metrics", "input": "Inventory"},
            {"action": "finish", "input": "circuit breaker"},
        ])
        self.assertEqual(ns["decision"], "circuit breaker")
        self.assertEqual(len(ns["history"]), 2)
        self.assertTrue(ns["observed"])


if __name__ == "__main__":
    unittest.main()
