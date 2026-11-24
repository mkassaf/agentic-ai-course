"""Check arithmetic and routing with deterministic test-only model doubles."""
import contextlib
import io
import json
from pathlib import Path
import sys
from types import SimpleNamespace
import unittest
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]


def run_lesson(slug, *, cells=None, responses=()):
    lesson = json.loads((ROOT / 'lessons' / f'{slug}.json').read_text())
    code = [cell['source'] for cell in lesson['cells'] if cell['type'] == 'code' and not cell.get('optional')]
    answers = iter(responses)
    namespace = {'ask': lambda prompt: next(answers)}
    with contextlib.redirect_stdout(io.StringIO()):
        for source in code if cells is None else code[:cells]:
            exec(source, namespace)
    return namespace


class NumericOutcomeTests(unittest.TestCase):
    def test_quiz_compares_each_case_to_the_rule(self):
        ns = run_lesson('00_rules_and_llms', responses=['A'] * 8)
        self.assertEqual(len(ns['cases']), 7)
        self.assertEqual(ns['agreement'], 3)

    def test_evaluation_dataset_and_judge_calibration(self):
        replies = [json.dumps({'names_cost': value}) for value in (False, False, True, True, False, True, True, True)]
        ns = run_lesson('09_multi_agent_evaluation', responses=replies)
        self.assertEqual((ns['agree'], len(ns['human'])), (3, 4))
        self.assertTrue(ns['trusted'])
        self.assertEqual((ns['scores']['Council']['calls'], ns['scores']['DeepSeek']['calls']), (10, 2))
        self.assertEqual(ns['ratio'], 5.0)

    def test_invalid_judgments_leave_the_affected_system_metric_missing(self):
        invalid_replies = ['not JSON', '[]', 'null', '{}', '{"names_cost": null}',
                           '{"names_cost": "true"}', '{"names_cost": 1}']
        for invalid in invalid_replies:
            with self.subTest(reply=invalid):
                replies = [json.dumps({'names_cost': value})
                           for value in (False, False, True, False, False, True, True, True)]
                replies[6] = invalid
                ns = run_lesson('09_multi_agent_evaluation', responses=replies)
                self.assertTrue(ns['trusted'])
                self.assertIsNone(ns['judged'][('Council', 'Support search')])
                self.assertIsNone(ns['scores']['Council']['names_cost'])
                self.assertEqual(ns['scores']['DeepSeek']['names_cost'], 1)
                self.assertNotIn('names_cost', ns['wins'])

    def test_missing_calibration_verdict_does_not_count_as_a_negative_rating(self):
        replies = [json.dumps({'names_cost': value})
                   for value in (False, False, True, False, False, True, True, True)]
        replies[0] = '{}'
        ns = run_lesson('09_multi_agent_evaluation', responses=replies)
        self.assertEqual(ns['agree'], 3)
        self.assertFalse(ns['trusted'])
        self.assertTrue(all(score['names_cost'] is None for score in ns['scores'].values()))

    def test_mlflow_omits_missing_judge_metrics_and_keeps_valid_zero_scores(self):
        replies = [json.dumps({'names_cost': value})
                   for value in (False, False, True, False, False, True, False, False)]
        replies[6] = '{}'
        ns = run_lesson('09_multi_agent_evaluation', responses=replies)
        recorded = []
        fake_mlflow = SimpleNamespace(
            set_tracking_uri=lambda uri: None, set_experiment=lambda name: None,
            start_run=lambda **kwargs: contextlib.nullcontext(),
            log_params=lambda params: None, log_metrics=lambda metrics: recorded.append(metrics),
        )
        lesson = json.loads((ROOT / 'lessons/09_multi_agent_evaluation.json').read_text())
        logging_cell = next(cell['source'] for cell in lesson['cells']
                            if cell['type'] == 'code' and 'import mlflow' in cell['source'])
        with patch.dict(sys.modules, {'mlflow': fake_mlflow}), contextlib.redirect_stdout(io.StringIO()):
            exec(logging_cell, ns)
        self.assertEqual(recorded[0]['names_cost'], 0)
        self.assertNotIn('names_cost', recorded[3])
        self.assertEqual(recorded[3]['correct'], 2)

    def test_routing_estimate_includes_router_and_queued_reviews(self):
        replies = [json.dumps({'route': r, 'reason': 'test'}) for r in ('rule','review','review','review','review')]
        ns = run_lesson('10_routing', responses=replies)
        self.assertEqual(ns['wasted'], ['Catalog'])
        self.assertEqual(ns['skipped'], [])
        self.assertEqual(ns['calls'], 25)

    def test_graph_retries_only_bad_contract(self):
        bad = {'orderId': 'string', 'amount': 'number', 'couponCode': 'optional string'}
        good = {'orderId': 'string', 'total': 'number', 'couponCode': 'optional string'}
        campaign = {'orderId': 'string', 'total': 'number', 'campaignId': 'optional string'}
        ns = run_lesson('14_frameworks_langgraph', responses=map(json.dumps, (bad, good, campaign)))
        self.assertEqual([r['attempts'] for r in ns['results']], [2, 1])
        self.assertTrue(all(r['passed'] for r in ns['results']))

    def test_learning_curve_values_match_held_out_cases(self):
        ns = run_lesson('16_learning_curve_trust')
        self.assertEqual((len(ns['feedback']), len(ns['test'])), (6, 4))
        self.assertFalse(set(ns['feedback']) & set(ns['test']))
        self.assertEqual(ns['curve'], [2, 2, 2, 2, 2, 4, 4])

    def test_weighted_scores_and_consumer_limit(self):
        ns = run_lesson('17_weighted_decision_jev', cells=3)
        self.assertEqual((ns['averages']['Task queue'], ns['averages']['Event log']), (2.25, 2.75))
        self.assertEqual([round(value, 2) for _, value in ns['table']], [2.83, 2.17])
        self.assertEqual([round(value, 2) for _, value in ns['table2']], [1.00, 3.67])
        self.assertEqual(min(ns['partitions'], ns['consumers']), 4)


if __name__ == '__main__':
    unittest.main()
