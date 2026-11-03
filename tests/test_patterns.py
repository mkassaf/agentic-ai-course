"""Contract and stopping-condition tests for the introductory protocols."""
import json
import unittest

from coursekit.patterns import bounded_tool_loop, retrieve, run_council, validate_proposal
from coursekit.runtime import Client


DOCUMENTS = [{"id": "S1", "text": "Option A has low operational effort; option B has stronger audit support."}]


def proposal(option="A", rationale="An independently constructed reason"):
    return {"option": option, "rationale": rationale, "tradeoffs": ["Audit versus operational effort"],
            "evidence": ["S1"], "confidence": 0.6}


class RecordingClient(Client):
    def __init__(self):
        super().__init__()
        self.prompts = []

    def ask(self, prompt, **kwargs):
        self.prompts.append(prompt)
        return super().ask(prompt, **kwargs)


class PatternTests(unittest.TestCase):
    def test_retrieval_has_no_random_evidence_when_nothing_matches(self):
        self.assertEqual(retrieve("astronomy", DOCUMENTS), [])
        self.assertEqual(retrieve("audit", DOCUMENTS)[0]["id"], "S1")

    def test_shape_and_known_citation_are_necessary_but_not_truth_proof(self):
        valid = proposal()
        self.assertEqual(validate_proposal(valid, {"S1"})["option"], "A")
        for change in ({"evidence": ["fabricated"]}, {"confidence": True}, {"evidence": []},
                       {"tradeoffs": []}, {"confidence": 1.1}, {"option": "C"}):
            with self.subTest(change=change), self.assertRaises(ValueError):
                validate_proposal(dict(valid, **change), {"S1"})
        # A source ID alone does not establish entailment: that needs a separate evidence review.

    def test_tool_allowlist_blocks_unknown_action_before_execution(self):
        executed = []
        with self.assertRaisesRegex(ValueError, "Denied tool"):
            bounded_tool_loop(Client(), "question", {"search": lambda query: executed.append(query)},
                              [json.dumps({"action": "tool", "name": "shell", "arguments": {"query": "x"}})])
        self.assertEqual(executed, [])

    def test_tool_loop_terminates_even_when_model_never_finishes(self):
        action = json.dumps({"action": "tool", "name": "search", "arguments": {"query": "audit"}})
        model = Client()
        result = bounded_tool_loop(model, "question", {"search": lambda query: "S1"}, [action], max_steps=2)
        self.assertEqual(result["status"], "budget_exhausted")
        self.assertEqual(len(result["trace"]), 2)
        self.assertEqual(len(model.trace), 2)

    def test_independent_proposals_do_not_see_peer_answers_and_dissent_survives(self):
        models = [RecordingClient() for _ in range(3)]
        fixtures = [proposal("A", "UNIQUE-PEER-ONE"), proposal("A", "UNIQUE-PEER-TWO"),
                    proposal("B", "UNIQUE-PEER-THREE")]
        result = run_council(models, "Choose a system", DOCUMENTS, fixtures, rounds=1)
        for model in models:
            self.assertNotIn("UNIQUE-PEER", model.prompts[0])
            self.assertIn("UNIQUE-PEER", model.prompts[1])
            self.assertEqual(len(model.trace), 3)
        self.assertEqual(result["decision"], "A")
        self.assertEqual(result["status"], "majority_proposal")
        self.assertEqual(result["dissent"][0]["proposal"]["option"], "B")
        self.assertTrue(result["human_approval_required"])

    def test_deadlock_escalates_and_distinct_role_names_cannot_replace_families(self):
        fixtures = [proposal("A"), proposal("B"), proposal("abstain")]
        result = run_council([Client() for _ in range(3)], "question", DOCUMENTS, fixtures, rounds=0)
        self.assertIsNone(result["decision"])
        self.assertEqual(result["status"], "escalate_to_human")
        models = [Client(mode="live", model=f"alias-{i}", family="same-family",
                         base_url="https://gateway.university.example/v1", api_key="TEST_ONLY") for i in range(3)]
        with self.assertRaisesRegex(ValueError, "families"):
            run_council(models, "question", DOCUMENTS, fixtures)
        self.assertTrue(all(not model.trace for model in models))


if __name__ == "__main__":
    unittest.main()
