"""Exercise the introductory examples without sending any model requests."""
import contextlib
import io
import json
from pathlib import Path
import unittest
from unittest.mock import patch

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
                    '04': iter(['I cannot check live data.', 'get_weather', 'It is 18°C.']),
                    '05': iter(['I do not know the weather yet.\nLOOKUP',
                                'Now I know it is rainy.\nFINISH', 'Visit a museum.']),
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
                weather_response = io.BytesIO(b'{"current":{"temperature_2m":18,"weather_code":3}}')
                with contextlib.redirect_stdout(io.StringIO()), patch('urllib.request.urlopen', return_value=weather_response):
                    exec(warmup['code'], namespace)
                    for step in warmup.get('extra_steps', []):
                        exec(step['code'], namespace)
                if number == '01':
                    self.assertEqual(len(prompts), 4)
                    mixed, *views = prompts
                    question, architect = views[0]
                    self.assertEqual(mixed[1]['system'], '')
                    self.assertEqual(mixed[0].split(), f"{architect['system']} {question}".split())
                    self.assertEqual([prompt for prompt, _ in views], [question] * 3)
                    system_prompts = {kwargs['system'].strip() for _, kwargs in views}
                    self.assertEqual(len(system_prompts), 3)
                    self.assertNotIn('', system_prompts)
                if number == '02':
                    self.assertIn('museum opens at 10:00', prompts[0][0])
                if number == '04':
                    self.assertIn('without', warmup['explanation'])
                    self.assertIn("'temperature_2m': 18", prompts[2][0])
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

    def test_crewai_install_cell_includes_pinned_coursekit(self):
        notebook = json.loads((ROOT / 'notebooks/05_react_agent.ipynb').read_text())
        install = next(''.join(cell['source']) for cell in notebook['cells']
                       if cell['cell_type'] == 'code' and 'crewai==1.15.45' in ''.join(cell['source']))
        revision = (ROOT / 'coursekit-ref.txt').read_text().strip()
        self.assertIn('agentic-ai-coursekit @ https://github.com/', install)
        self.assertIn(revision + '.zip', install)

    def test_react_warmup_returns_each_rejected_action_to_the_model(self):
        lesson = json.loads((ROOT / 'lessons/05_react_agent.json').read_text())
        replies = iter(['I can guess.\nFINISH', 'I need weather.\nCHECK_WEATHER', 'I can look it up.\nLOOKUP'])
        prompts = []

        def ask(prompt):
            prompts.append(prompt)
            return next(replies)

        with contextlib.redirect_stdout(io.StringIO()):
            exec(lesson['warmup']['code'], {'ask': ask})

        self.assertEqual(len(prompts), 3)
        self.assertIn('LOOKUP is required before FINISH.', prompts[1])
        self.assertIn('Unknown action.', prompts[2])

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
