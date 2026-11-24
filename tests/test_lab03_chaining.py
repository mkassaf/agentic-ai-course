"""Check the handoffs and failure behavior of the Lab 03 exercise."""
import contextlib
import io
import json
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]
LESSON = json.loads((ROOT / 'lessons/03_prompt_chaining.json').read_text())
STEPS = [cell['source'] for cell in LESSON['cells'] if cell['type'] == 'code']


class PromptChainTests(unittest.TestCase):
    def test_each_answer_reaches_the_next_call(self):
        tradeoffs = {
            option: {criterion: mark for criterion in (
                'cohesive business rules', 'independent change', 'private data ownership')}
            for option, mark in [('business capability split', '+'), ('technical layer split', '-')]
        }
        replies = iter([
            'vegetable pasta', 'pasta\ntomatoes\nspinach',
            '["Order", "Inventory", "Shipping"]', json.dumps(tradeoffs),
            'Context: Shared tables and releases\nDecision: business capability split\nConsequence: More service contracts',
        ])
        prompts = []

        def ask(prompt):
            prompts.append(prompt)
            return next(replies)

        namespace = {'ask': ask}
        with contextlib.redirect_stdout(io.StringIO()):
            for step in STEPS:
                exec(step, namespace)

        self.assertEqual(len(prompts), 5)
        self.assertIn('vegetable pasta', prompts[1])
        self.assertIn('OrderPlaced', prompts[2])
        self.assertIn('Inventory', prompts[3])
        self.assertIn('Inventory', prompts[4])
        self.assertIn('private data ownership', prompts[4])
        self.assertIn('Consequence:', namespace['record'])

    def test_bad_context_shape_stops_before_the_comparison(self):
        prompts = []

        def ask(prompt):
            prompts.append(prompt)
            return '["Order"]'

        namespace = {'ask': ask}
        with contextlib.redirect_stdout(io.StringIO()):
            exec(STEPS[1], namespace)
            with self.assertRaisesRegex(ValueError, 'Quality gate'):
                exec(STEPS[2], namespace)
        self.assertEqual(len(prompts), 1)

    def test_notebook_starts_with_the_everyday_example(self):
        notebook = json.loads((ROOT / 'notebooks/03_prompt_chaining.ipynb').read_text())
        text = [''.join(cell['source']) for cell in notebook['cells']]
        simple = next(i for i, source in enumerate(text) if source.startswith('## Step 1 ·'))
        architecture = next(i for i, source in enumerate(text) if source.startswith('## Think about the example'))
        self.assertLess(simple, architecture)


if __name__ == '__main__':
    unittest.main()
