"""Check the readable, reusable checks for scenarios and reviewer proposals."""
import contextlib
import io
import json
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]


class FramingValidatorTests(unittest.TestCase):
    def setUp(self):
        lesson = json.loads((ROOT / 'lessons/15_framing_contract.json').read_text())
        cells = [cell['source'] for cell in lesson['cells'] if cell['type'] == 'code']
        self.ns = {}
        with contextlib.redirect_stdout(io.StringIO()):
            exec(cells[0], self.ns)
            exec(cells[2], self.ns)

    def test_scenario_needs_a_known_quality_and_a_number(self):
        check = self.ns['scenario_problems']
        valid = {'quality': 'reliability', 'stimulus': 'timeout',
                 'response': 'use fallback', 'measure': 'within 1 second'}
        self.assertEqual(check(valid), [])
        self.assertIn('measure needs a number', check({**valid, 'measure': 'fast'}))
        self.assertIn('unknown quality', check({**valid, 'quality': 'speed'}))

    def test_proposal_rejects_bad_marks_and_boolean_confidence(self):
        check = self.ns['contract_problems']
        valid = {'option': 'guarded checkout', 'confidence': 0.8,
                 'marks': {'0': '+', '1': '-', '2': '+'}, 'claim': 'Bound the wait.'}
        self.assertEqual(check(valid), [])
        self.assertIn('mark every scenario', check({**valid, 'marks': {'0': '+'}}))
        self.assertIn('confidence must be a number from 0 to 1', check({**valid, 'confidence': True}))
        self.assertIn('unknown option', check({**valid, 'option': 'unknown'}))


if __name__ == '__main__':
    unittest.main()
