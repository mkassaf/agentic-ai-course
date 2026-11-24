"""Exercise the introductory examples without sending any model requests."""
import contextlib
import io
import json
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]


class WarmupTests(unittest.TestCase):
    def test_examples_run_and_pass_the_context_forward(self):
        # MCP and A2A warm-ups run with the real SDKs in execute_notebooks.py.
        for number in ['00', '01', '02', '04', '05', '06', '07', '08', '09',
                       '10', '12', '14', '15', '16', '17']:
            with self.subTest(lab=number):
                path = next((ROOT / 'lessons').glob(number + '_*.json'))
                warmup = json.loads(path.read_text())['warmup']
                prompts = []
                responses = {
                    '04': iter(['get_weather', 'A raincoat.']),
                    '05': iter(['LOOKUP', 'FINISH', 'Visit a museum.']),
                    '06': iter(['Go for a walk.', 'It is raining.']),
                }

                def ask(prompt, **kwargs):
                    prompts.append((prompt, kwargs))
                    return next(responses[number]) if number in responses else 'A sample answer.'

                class Client:
                    def ask(self, prompt, **kwargs):
                        return ask(prompt, **kwargs)

                namespace = {'ask': ask, 'plain': Client(), 'client': Client(),
                             'make_ask': lambda **kwargs: ask}
                with contextlib.redirect_stdout(io.StringIO()):
                    exec(warmup['code'], namespace)
                if number == '01':
                    self.assertIn('system', prompts[1][1])
                if number == '02':
                    self.assertIn('museum opens at 10:00', prompts[0][0])
                if number == '04':
                    self.assertIn('rainy', prompts[1][0])
                if number == '05':
                    self.assertIn('rainy', prompts[1][0])
                if number == '06':
                    self.assertIn('Go for a walk.', prompts[1][0])
                if number == '08':
                    self.assertIn('It is raining', prompts[0][0])
                if number == '12':
                    self.assertIn('Explain a term', prompts[0][0])
                if number == '14':
                    self.assertEqual(namespace['warm_graph'].compile().invoke({'message': 'Sam'})['message'],
                                     'Hello, Sam')

    def test_every_lab_starts_with_its_simple_example(self):
        for path in sorted((ROOT / 'notebooks').glob('*.ipynb')):
            with self.subTest(lab=path.stem):
                notebook = json.loads(path.read_text())
                cells = notebook['cells']
                code = [cell for cell in cells if cell['cell_type'] == 'code'
                        and 'setup' not in cell['metadata'].get('tags', [])]
                if path.name.startswith('03_'):
                    self.assertIn('vegetarian lunch', ''.join(code[0]['source']))
                else:
                    self.assertIn('warmup', code[0]['metadata'].get('tags', []))
                warmup_index = cells.index(code[0])
                review_index = next(i for i, cell in enumerate(cells)
                                    if ''.join(cell['source']).startswith('## Think about the example'))
                self.assertLess(warmup_index, review_index)


if __name__ == '__main__':
    unittest.main()
