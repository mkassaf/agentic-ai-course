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

    def run_replies(self, replies):
        replies = iter(replies)
        calls = []

        class Client:
            def ask(self, prompt, *, system):
                calls.append((prompt, system))
                return next(replies)

        self.ns["client"] = Client()
        output = io.StringIO()
        with contextlib.redirect_stdout(output):
            exec(self.cells[4], self.ns)
        return calls, output.getvalue()

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
        calls, output = self.run_replies([
            '{"tool":"extract_service","name":"orders"}',
            '{"tool":"validate_service"}',
            '{"tool":"format_html"}',
            '{"tool":"finish","answer":"Done"}',
        ])
        self.assertIn("extract_service", calls[0][1])
        self.assertIn("Sales team", calls[1][0])
        self.assertIn("Valid", calls[2][0])
        self.assertIn("<h2>Orders</h2>", calls[3][0])
        self.assertIn("Final answer: <h2>Orders</h2><p>Owner: Sales team</p>", output)
        self.assertNotIn("Final answer: Done", output)

    def test_invalid_requests_cannot_format(self):
        early_finish = '{"tool":"finish","answer":"<h2>Orders</h2><p>Invented owner</p>"}'
        _, output = self.run_replies(['{"tool":"format_html"}'] + [early_finish] * 5)
        self.assertIn("extract and validate", self.ns["history"])
        self.assertNotIn("Final answer:", output)
        self.assertIn("Stopped after six turns", output)

    def test_model_recovers_from_wrong_service_and_finishes_with_requested_html(self):
        calls, output = self.run_replies([
            '{"tool":"extract_service","name":"inventory"}',
            '{"tool":"finish","answer":"I used Inventory."}',
            '{"tool":"extract_service","name":"orders"}',
            '{"tool":"validate_service"}',
            '{"tool":"format_html"}',
            '{"tool":"finish"}',
        ])
        self.assertIn("Wrong service. Look up Orders.", calls[1][0])
        self.assertNotIn("Stock team", output)
        self.assertIn("Final answer: <h2>Orders</h2>", output)

    def test_missing_service_returns_the_lookup_error_even_if_model_invents_html(self):
        self.ns.update(html_target="Shipping", question="Show the Shipping service as HTML.")
        _, output = self.run_replies([
            '{"tool":"extract_service","name":"shipping"}',
            '{"tool":"finish","answer":"<h2>Shipping</h2>"}',
        ])
        self.assertIn("Final answer: Service not found.", output)

    def test_conceptual_question_can_finish_without_tools(self):
        self.ns.update(html_target=None, question="What does a microservice own?")
        calls, output = self.run_replies(['{"tool":"finish","answer":"Its own private data."}'])
        self.assertEqual(len(calls), 1)
        self.assertIn("Final answer: Its own private data.", output)

    def test_native_tool_formats_only_matching_catalog_record(self):
        formatter_source = '\n'.join(self.cells[5].splitlines()[1:])  # omit notebook install magic
        exec(formatter_source, self.ns)
        formatter = self.ns["format_catalog_html"]
        record = self.ns["extract_service"]("Orders")
        self.assertIn("Sales team", formatter(record))
        for other in (self.ns["extract_service"]("Inventory"), dict(record, owner="Invented team")):
            self.assertIn("Extract the Orders record", formatter(other))

    def test_non_json_reply_returns_a_result_and_the_loop_retries(self):
        self.run_replies([
            "I will extract it now.",
            '{"tool":"extract_service","name":"orders"}',
            '{"tool":"validate_service"}',
            '{"tool":"format_html"}',
            '{"tool":"finish","answer":"Done"}',
        ])
        self.assertIn("JSON object", self.ns["history"])
        self.assertTrue(self.ns["validated"])


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
            premature = {"action": "finish", "input": "circuit breaker"}
            actions = [{"action": "read_metrics", "input": service}] + [premature] * 4
            with self.subTest(service=service), self.assertRaisesRegex(AssertionError, "budget"):
                self.run_actions(actions)

    def test_agent_can_recover_by_observing_the_target_after_a_failed_lookup(self):
        ns = self.run_actions([
            {"action": "read_metrics", "input": "stock"},
            {"action": "read_metrics", "input": "Inventory"},
            {"action": "finish", "input": "circuit breaker"},
        ])
        self.assertEqual(ns["decision"], "circuit breaker")
        self.assertEqual(len(ns["history"]), 2)
        self.assertTrue(ns["observed"])

    def test_premature_finish_returns_an_observation_and_the_agent_recovers(self):
        ns = self.run_actions([
            {"action": "finish", "input": "circuit breaker"},
            {"action": "read_metrics", "input": "Inventory"},
            {"action": "finish", "input": "circuit breaker"},
        ])
        self.assertEqual(ns["decision"], "circuit breaker")
        self.assertTrue(ns["observed"])
        self.assertEqual(len(ns["history"]), 2)

    def test_malformed_reply_becomes_an_error_observation(self):
        cells = code_cells("05_react_agent")
        ns = {}
        quiet_exec(cells[0], ns)
        quiet_exec(cells[1], ns)
        replies = iter([
            "I will read the metrics first.",
            '{"thought":"Now I can act.","action":"READ_METRICS","input":"Inventory"}',
            '{"action":"finish","input":"Circuit breaker."}',
        ])
        ns["ask"] = lambda prompt: next(replies)
        quiet_exec(cells[2], ns)
        self.assertEqual(ns["decision"], "circuit breaker")
        self.assertEqual(len(ns["history"]), 2)


if __name__ == "__main__":
    unittest.main()
