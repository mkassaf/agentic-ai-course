import unittest

from coursekit.protocol_examples import review_over_a2a


class ArchitectureReviewTests(unittest.IsolatedAsyncioTestCase):
    async def test_agent_card_and_message_round_trip(self):
        agent, report = await review_over_a2a(
            {"team_size": 3, "independent_deploys": False}, "modular monolith",
        )
        self.assertEqual(agent, "Architecture reviewer")
        self.assertEqual(report, "PASS: course policy expects modular monolith.")

    async def test_conflicting_proposal_fails_policy_check(self):
        _, report = await review_over_a2a(
            {"team_size": 3, "independent_deploys": False}, "microservices",
        )
        self.assertEqual(report, "FAIL: course policy expects modular monolith.")

    async def test_independent_deploys_and_team_threshold_are_both_required(self):
        for size, independent, expected in [
            (7, True, "modular monolith"),
            (8, False, "modular monolith"),
            (8, True, "microservices"),
        ]:
            with self.subTest(size=size, independent=independent):
                _, report = await review_over_a2a(
                    {"team_size": size, "independent_deploys": independent}, expected,
                )
                self.assertEqual(report, f"PASS: course policy expects {expected}.")

    async def test_bad_project_facts_are_rejected(self):
        for case in [
            {"team_size": True, "independent_deploys": False},
            {"team_size": 0, "independent_deploys": False},
            {"team_size": 3, "independent_deploys": "false"},
        ]:
            with self.subTest(case=case), self.assertRaises(ValueError):
                await review_over_a2a(case, "modular monolith")


if __name__ == "__main__":
    unittest.main()
