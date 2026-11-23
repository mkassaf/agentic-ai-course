"""Verify that the course's published example numbers match its practice runs."""
import contextlib
import io
import json
from pathlib import Path
import unittest

from coursekit import make_ask

ROOT = Path(__file__).resolve().parents[1]


def run_lesson(slug, *, cells=None):
    lesson = json.loads((ROOT / 'lessons' / f'{slug}.json').read_text())
    code = [cell['source'] for cell in lesson['cells'] if cell['type'] == 'code' and not cell.get('optional')]
    namespace = {'ask': make_ask(mode='practice'), 'MODE': 'practice'}
    with contextlib.redirect_stdout(io.StringIO()):
        for source in code if cells is None else code[:cells]:
            exec(source, namespace)
    return namespace


class NumericOutcomeTests(unittest.TestCase):
    def test_quiz_rejects_missing_practice_answers_for_new_cases(self):
        lesson = json.loads((ROOT / 'lessons/00_rules_and_llms.json').read_text())
        code = [c['source'] for c in lesson['cells'] if c['type'] == 'code' and not c.get('optional')]
        ns = {'ask': make_ask(mode='practice')}
        with contextlib.redirect_stdout(io.StringIO()):
            exec(code[0], ns)
            exec(code[1], ns)
            ns['cases'].append(dict(ns['cases'][0]))
            with self.assertRaisesRegex(AssertionError, 'practice answer'):
                exec(code[3], ns)

    def test_evaluation_fixtures_and_judge_agreement(self):
        ns = run_lesson('09_multi_agent_evaluation')
        self.assertEqual((ns['agree'], len(ns['human'])), (3, 4))
        self.assertTrue(ns['trusted'])
        self.assertEqual(ns['scores']['Council']['correct'], 2)
        self.assertEqual(ns['scores']['DeepSeek']['correct'], 2)
        self.assertEqual((ns['scores']['Council']['calls'], ns['scores']['DeepSeek']['calls']), (10, 2))
        self.assertEqual(ns['ratio'], 5.0)

    def test_routing_estimate_includes_router_and_queued_reviews(self):
        ns = run_lesson('10_routing')
        self.assertEqual(len(ns['cases']), 5)
        self.assertEqual(ns['wasted'], ['Catalog'])
        self.assertEqual(ns['skipped'], [])
        self.assertEqual(ns['calls'], 25)
        self.assertEqual(ns['COST']['review'] * len(ns['cases']), 25)

    def test_graph_uses_three_scripted_generation_attempts(self):
        ns = run_lesson('14_frameworks_langgraph')
        self.assertEqual([r['attempts'] for r in ns['results']], [2, 1])
        self.assertTrue(all(r['passed'] for r in ns['results']))

    def test_learning_curve_values_match_held_out_cases(self):
        ns = run_lesson('16_learning_curve_trust')
        self.assertEqual((len(ns['feedback']), len(ns['test'])), (6, 4))
        self.assertFalse(set(ns['feedback']) & set(ns['test']))
        self.assertEqual(ns['curve'], [2, 2, 2, 2, 2, 4, 4])

    def test_weighted_scores_and_consumer_limit(self):
        ns = run_lesson('17_weighted_decision_jev', cells=3)
        self.assertEqual((ns['average'](ns['queue']), ns['average'](ns['log'])), (2.25, 2.75))
        self.assertEqual([round(value, 2) for _, value in ns['table']], [2.83, 2.17])
        self.assertEqual([round(value, 2) for _, value in ns['table2']], [1.00, 3.67])
        self.assertEqual(min(ns['partitions'], ns['consumers']), 4)


if __name__ == '__main__':
    unittest.main()
