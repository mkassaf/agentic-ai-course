"""Behavior checks for the slide-based readiness, aggregate, and agent examples."""
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


class ReadinessScreenTests(unittest.TestCase):
    def test_independent_releases_and_operational_readiness_are_both_needed(self):
        source = code_cells("00_rules_and_llms")[0]
        node = next(node for node in ast.parse(source).body
                    if isinstance(node, ast.FunctionDef) and node.name == "decide")
        ns = {}
        exec(compile(ast.Module(body=[node], type_ignores=[]), "<readiness>", "exec"), ns)
        cases = [
            (False, False, "modular monolith"),
            (True, False, "modular monolith"),
            (False, True, "modular monolith"),
            (True, True, "microservices"),
        ]
        for ready, independent, expected in cases:
            with self.subTest(ops_ready=ready, independent_deploys=independent):
                decision, reason = ns["decide"]({"ops_ready": ready, "independent_deploys": independent})
                self.assertEqual(decision, expected)
                self.assertTrue(reason.strip())


class OrderAggregateTests(unittest.TestCase):
    def setUp(self):
        self.ns = {}
        cells = code_cells("04_why_tools")
        quiet_exec(cells[0], self.ns)
        self.ns["order"] = self.ns["Order"]("regression-order")
        quiet_exec(cells[1], self.ns)
        quiet_exec(cells[2], self.ns)

    def test_root_recomputes_total_when_items_change(self):
        order = self.ns["order"]
        order.add_item("Jacket", 1, 4200)
        snapshot = order.add_item("Scarf", 2, 1500)
        self.assertEqual(snapshot["total_cents"], 7200)
        self.assertEqual(snapshot["total_cents"],
                         sum(line["quantity"] * line["price_cents"] for line in snapshot["lines"]))

    def test_invalid_quantity_cannot_partially_change_order(self):
        order = self.ns["order"]
        order.add_item("Jacket", 1, 4200)
        before = order.read()
        for quantity in (0, -1):
            with self.subTest(quantity=quantity):
                self.assertIn("error", order.add_item("Scarf", quantity, 1500))
                self.assertEqual(order.read(), before)

    def test_snapshot_edit_does_not_mutate_aggregate(self):
        order = self.ns["order"]
        order.add_item("Jacket", 1, 4200)
        before = order.read()
        snapshot = order.read()
        snapshot["lines"][0]["quantity"] = 999
        snapshot["lines"].append({"product": "Injected", "quantity": 1, "price_cents": 0})
        snapshot["total_cents"] = 0
        self.assertEqual(order.read(), before)

    def test_dispatcher_rejects_malformed_requests_without_state_change(self):
        dispatch = self.ns["call_tool"]
        before = self.ns["order"].read()
        bad_requests = [
            "not JSON", "null", "[]",
            '{"tool":"read_order","args":null}',
            '{"tool":"add_item","args":{}}',
            '{"tool":"add_item","args":{"product":"Scarf","quantity":"2","price_cents":1500}}',
            '{"tool":"add_item","args":{"product":"Scarf","quantity":true,"price_cents":1500}}',
            '{"tool":"set_total","args":{"total_cents":0}}',
        ]
        for request in bad_requests:
            with self.subTest(request=request):
                self.assertIn("error", dispatch(request, confirmed=True))
                self.assertEqual(self.ns["order"].read(), before)

    def test_valid_write_still_requires_confirmation(self):
        request = json.dumps({"tool": "add_item", "args": {"product": "Scarf", "quantity": 2, "price_cents": 1500}})
        self.assertIn("error", self.ns["call_tool"](request))
        self.assertEqual(self.ns["order"].read()["lines"], [])
        self.assertEqual(self.ns["call_tool"](request, confirmed=True)["total_cents"], 3000)


class ReActObservationTests(unittest.TestCase):
    def run_actions(self, actions):
        cells = code_cells("05_react_agent")
        ns = {}
        quiet_exec(cells[0], ns)
        quiet_exec(cells[1], ns)
        steps = iter(actions)
        ns["next_action"] = lambda history: next(steps)
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
