"""Check that generation-setting examples compare the same task fairly."""
import contextlib
import io
import json
from pathlib import Path
import sys
from types import SimpleNamespace
import unittest
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]
LESSON = json.loads((ROOT / 'lessons/01_prompting_evaluation.json').read_text())
OPTIONAL = [cell['source'] for cell in LESSON['cells'] if cell['type'] == 'code' and cell.get('optional') and 'IFrame' not in cell['source']]


class SamplingExamplesTests(unittest.TestCase):
    def test_temperature_changes_one_setting_without_dropping_provider_options(self):
        made = []

        class Client:
            def __init__(self, **options):
                self.options = options
                made.append(self)
            def ask(self, prompt, *, system):
                self.prompt, self.system = prompt, system
                return 'A BFF adds a component to maintain.'

        ns = {'Client': Client, 'settings': {'model': 'test-model', 'base_url': 'https://example.test/v1',
                                             'extra_body': {'thinking': {'type': 'disabled'}}},
              'key': 'TEST_ONLY', 'system_prompt': 'Explain architecture concisely.'}
        with contextlib.redirect_stdout(io.StringIO()):
            exec(OPTIONAL[0], ns)
        self.assertEqual(len(made), 2)
        self.assertEqual([c.options['extra_body']['temperature'] for c in made], [0.0, 1.3])
        self.assertTrue(all(c.options['extra_body']['thinking'] == {'type': 'disabled'} for c in made))
        self.assertEqual(made[0].prompt, made[1].prompt)
        self.assertEqual(made[0].system, made[1].system)
        self.assertEqual(ns['settings']['extra_body'], {'thinking': {'type': 'disabled'}})

    def test_top_k_changes_only_k_and_enables_local_sampling(self):
        calls = []

        def old(messages, **options):
            calls.append((messages, options))
            return [{'generated_text': [{'role': 'assistant', 'content': 'A circuit breaker.'}]}]

        seeds = []
        with patch.dict(sys.modules, {'transformers': SimpleNamespace(set_seed=seeds.append)}), \
                contextlib.redirect_stdout(io.StringIO()):
            exec(OPTIONAL[1], {'old': old})
        self.assertEqual(seeds, [42, 42])
        self.assertEqual(len(calls), 2)
        self.assertEqual([entry[1]['top_k'] for entry in calls], [1, 20])
        self.assertEqual(calls[0][0], calls[1][0])
        settings0, settings1 = dict(calls[0][1]), dict(calls[1][1])
        settings0.pop('top_k'); settings1.pop('top_k')
        self.assertEqual(settings0, settings1)
        self.assertTrue(settings0['do_sample'])
        self.assertEqual(settings0['top_p'], 1.0)


if __name__ == '__main__':
    unittest.main()
