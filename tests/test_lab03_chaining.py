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

    def test_bad_context_shape_clears_previous_handoff_and_stops_chain(self):
        prompts = []
        replies = iter(['["Order", "Inventory", "Shipping"]', '[123, null, {}]'])
        def ask(prompt):
            prompts.append(prompt)
            return next(replies)

        namespace = {'ask': ask}
        with contextlib.redirect_stdout(io.StringIO()):
            exec(STEPS[1], namespace)
            exec(STEPS[2], namespace)
            self.assertIsNotNone(namespace['contexts'])
            with self.assertRaisesRegex(ValueError, 'Quality gate'):
                exec(STEPS[2], namespace)
            self.assertIsNone(namespace['contexts'])
            with self.assertRaisesRegex(ValueError, 'complete Step 3'):
                exec(STEPS[3], namespace)
        self.assertEqual(len(prompts), 2)

    def test_gate_explains_malformed_json(self):
        namespace = {'ask': lambda prompt: '```json\n["Order", "Inventory", "Shipping"]\n```'}
        with contextlib.redirect_stdout(io.StringIO()):
            exec(STEPS[1], namespace)
            with self.assertRaisesRegex(ValueError, 'expected JSON without extra text'):
                exec(STEPS[2], namespace)

    def test_decision_gate_requires_exactly_three_nonempty_lines(self):
        for reply in (
            'Context: Shared data\nDecision: business capability split\nConsequence: ',
            'Context: Shared data\nDecision: business capability split\nConsequence: More calls\nExtra line',
        ):
            with self.subTest(reply=reply), contextlib.redirect_stdout(io.StringIO()):
                namespace = {'ask': lambda prompt: reply}
                exec(STEPS[1], namespace)
                namespace.update(contexts=['Order', 'Inventory', 'Shipping'], tradeoffs={})
                with self.assertRaisesRegex(ValueError, 'Quality gate'):
                    exec(STEPS[4], namespace)
                self.assertIsNone(namespace['record'])

    def test_notebook_starts_with_the_everyday_example(self):
        notebook = json.loads((ROOT / 'notebooks/03_prompt_chaining.ipynb').read_text())
        text = [''.join(cell['source']) for cell in notebook['cells']]
        simple = next(i for i, source in enumerate(text) if source.startswith('## Step 1 ·'))
        architecture = next(i for i, source in enumerate(text) if source.startswith('## Think about the example'))
        self.assertLess(simple, architecture)


if __name__ == '__main__':
    unittest.main()
