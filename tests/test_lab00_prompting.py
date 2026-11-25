"""Check the controlled prompting comparisons without making model requests."""
import contextlib
import importlib.util
import io
import json
from pathlib import Path
import re
import unittest

ROOT = Path(__file__).resolve().parents[1]


def run_prompting_step():
    lesson = json.loads((ROOT / 'lessons/00_rules_and_llms.json').read_text())
    cell = next(cell for cell in lesson['cells']
                if cell['type'] == 'code' and 'shot_prompts' in cell['source'])
    prompts = []
    options = {'preserved': True}

    def ask(prompt):
        prompts.append(prompt)
        return 'BFF'

    namespace = {'ask': ask, 'prompt': 'original', 'options': options}
    with contextlib.redirect_stdout(io.StringIO()):
        exec(cell['source'], namespace)
    return cell, prompts, namespace, options


class PromptingTechniqueTests(unittest.TestCase):
    def test_shot_comparison_changes_examples_and_keeps_the_task_constant(self):
        cell, prompts, namespace, _ = run_prompting_step()
        self.assertFalse(cell.get('optional', False))
        self.assertEqual(len(prompts), 5)
        demonstrations = namespace['demonstrations']
        self.assertEqual(len(demonstrations), 3)
        self.assertEqual(len(set(demonstrations)), 3)
        question = namespace['technique_question']
        instruction = namespace['label_request']

        for call, expected_examples in zip(prompts[:3], (0, 1, 3)):
            with self.subTest(examples=expected_examples):
                self.assertEqual(call.count(question), 1)
                self.assertEqual(call.count(instruction), 1)
                for index, example in enumerate(demonstrations):
                    if index < expected_examples:
                        self.assertEqual(call.count(example), 1)
                        self.assertLess(call.index(example), call.index(question))
                    else:
                        self.assertNotIn(example, call)

    def test_persona_comparison_changes_only_the_role(self):
        _, prompts, namespace, _ = run_prompting_step()
        self.assertEqual(len(prompts), 5)
        task = namespace['persona_task']
        self.assertIn(namespace['technique_question'], task)
        self.assertIn('two short sentences', task)
        role = 'You are a cautious software architect. Consider operational cost.'
        self.assertEqual(prompts[3].strip(), task)
        self.assertEqual(prompts[4].strip(), f'{role}\n{task}')

    def test_comparison_preserves_the_original_prompt_and_provider_options(self):
        _, _, namespace, options = run_prompting_step()
        self.assertEqual(namespace['prompt'], 'original')
        self.assertIs(namespace['options'], options)
        self.assertEqual(options, {'preserved': True})

    def test_generated_diagram_is_current_and_linked_from_lab_notebook_and_site(self):
        spec = importlib.util.spec_from_file_location(
            'prompting_diagram', ROOT / 'scripts/build_prompting_diagram.py')
        diagram = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(diagram)
        self.assertEqual(diagram.OUTPUT.read_text(), diagram.render())

        image_path = 'assets/images/prompt-techniques.svg'
        lesson = json.loads((ROOT / 'lessons/00_rules_and_llms.json').read_text())
        self.assertIn(image_path, '\n'.join(cell['source'] for cell in lesson['cells']))
        notebook = json.loads((ROOT / 'notebooks/00_rules_and_llms.ipynb').read_text())
        self.assertIn(image_path, '\n'.join(''.join(cell['source']) for cell in notebook['cells']))

        javascript = (ROOT / 'assets/course.js').read_text()
        labs = re.search(r'const labs = (\[.*?\n\]);', javascript, re.S)
        self.assertIsNotNone(labs)
        lab = next(lab for lab in json.loads(labs[1]) if lab['id'] == '00')
        self.assertEqual(lab['picture']['src'], image_path)
        self.assertTrue(lab['picture']['alt'])


if __name__ == '__main__':
    unittest.main()
