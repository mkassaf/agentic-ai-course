"""Test the optional provider adapters without credentials or network requests."""
import contextlib
import io
import json
from pathlib import Path
import re
import sys
from types import SimpleNamespace
import unittest
from unittest.mock import patch

import coursekit

ROOT = Path(__file__).resolve().parents[1]
LESSON = json.loads((ROOT / 'lessons/00_rules_and_llms.json').read_text())
OPTIONAL = [cell['source'] for cell in LESSON['cells'] if cell.get('optional') and 'DeepSeekHarness' not in cell['source']]
HARNESS = next(cell['source'] for cell in LESSON['cells'] if cell.get('optional') and 'DeepSeekHarness' in cell['source'])


class SDKExamplesTests(unittest.TestCase):
    def test_both_examples_use_selected_provider_and_same_prompt(self):
        self.assertEqual(len(OPTIONAL), 2)
        for provider in ('deepseek', 'gemini', 'freeinference'):
            with self.subTest(provider=provider):
                config = coursekit.PROVIDERS[provider]
                expected_extra = config.get('extra_body') or {}
                if provider == 'freeinference':
                    expected_extra = {'thinking': {'type': 'disabled'}}
                calls = []

                class FakeSDK:
                    def __init__(self, **kwargs):
                        calls.append(('sdk_config', kwargs))
                        self.chat = SimpleNamespace(completions=self)
                    def create(self, **kwargs):
                        calls.append(('sdk_request', kwargs))
                        return SimpleNamespace(choices=[SimpleNamespace(message=SimpleNamespace(content='A'))])

                class FakeFramework:
                    def __init__(self, **kwargs):
                        calls.append(('framework_config', kwargs))
                    def invoke(self, messages):
                        calls.append(('framework_prompt', messages))
                        return SimpleNamespace(content='A')

                modules = {'openai': SimpleNamespace(OpenAI=FakeSDK),
                           'langchain_openai': SimpleNamespace(ChatOpenAI=FakeFramework)}
                namespace = {'MODE': 'live', 'PROVIDER': provider, 'prompt': 'same question',
                             'find_spec': lambda name: True}
                with patch.dict(sys.modules, modules), patch.object(coursekit, 'secret', return_value='TEST_ONLY'), \
                        contextlib.redirect_stdout(io.StringIO()):
                    for source in OPTIONAL:
                        # IPython handles this line in Colab; packages are faked here.
                        python = re.sub(r'(?m)^(\s*)%pip.*$', r'\1pass', source)
                        exec(python, namespace)
                records = dict(calls)
                self.assertEqual(records['sdk_config']['base_url'], config['base_url'])
                self.assertEqual(records['sdk_config']['max_retries'], 0)
                self.assertEqual(records['sdk_request']['model'], config['model'])
                self.assertEqual(records['sdk_request']['messages'], [
                    {'role': 'system', 'content': 'You are a concise teaching assistant.'},
                    {'role': 'user', 'content': 'same question'}])
                self.assertEqual(records['sdk_request']['extra_body'], expected_extra)
                self.assertEqual(records['framework_config']['base_url'], config['base_url'])
                self.assertEqual(records['framework_config']['model'], config['model'])
                self.assertEqual(records['framework_config']['extra_body'], expected_extra)
                self.assertEqual(records['framework_prompt'], [
                    ('system', 'You are a concise teaching assistant.'), ('user', 'same question')])

    def test_practice_requires_no_imports_or_key(self):
        with patch.object(coursekit, 'secret', side_effect=AssertionError('unexpected secret')), \
                contextlib.redirect_stdout(io.StringIO()) as output:
            for source in OPTIONAL:
                python = re.sub(r'(?m)^(\s*)%pip.*$', r'\1pass', source)
                exec(python, {'MODE': 'practice'})
        self.assertEqual(output.getvalue().count('scripted; no model request'), 2)


class HarnessExampleTests(unittest.TestCase):
    def python_source(self):
        return re.sub(r'(?m)^(\s*)%pip.*$', r'\1pass', HARNESS)

    def test_practice_and_other_providers_do_not_launch_the_runtime(self):
        with contextlib.redirect_stdout(io.StringIO()) as output:
            exec(self.python_source(), {'MODE': 'practice'})
            exec(self.python_source(), {'MODE': 'live', 'PROVIDER': 'deepseek'})
            exec(self.python_source().replace('RUN_HARNESS = False', 'RUN_HARNESS = True'),
                 {'MODE': 'live', 'PROVIDER': 'gemini'})
        self.assertIn('scripted; no model request', output.getvalue())
        self.assertIn('Set RUN_HARNESS', output.getvalue())

    def test_live_branch_rejects_unverified_sdk_versions(self):
        namespace = {'MODE': 'live', 'PROVIDER': 'deepseek', 'find_spec': lambda name: True}
        source = self.python_source().replace('RUN_HARNESS = False', 'RUN_HARNESS = True')
        with patch('importlib.metadata.version', return_value='0.0.0'):
            with self.assertRaisesRegex(AssertionError, 'pinned SDK'):
                exec(source, namespace)

    def test_live_branch_disables_tools_and_uses_temporary_home(self):
        captured = {}

        class FakeHarness:
            def __init__(self, **kwargs):
                captured['options'] = kwargs
                captured['patch'] = Path(kwargs['patches'][0]).read_text()
                captured['workspace_exists'] = Path(kwargs['cwd']).is_dir()
            def __enter__(self):
                return self
            def __exit__(self, *args):
                return False
            def run(self, prompt, **kwargs):
                captured['prompt'] = prompt
                return SimpleNamespace(finish_reason='completed', final_response='A')

        modules = {'deepseek_harness': SimpleNamespace(DeepSeekHarness=FakeHarness)}
        namespace = {'MODE': 'live', 'PROVIDER': 'deepseek', 'prompt': 'same question',
                     'find_spec': lambda name: True}
        with patch.dict(sys.modules, modules), patch.object(coursekit, 'secret', return_value='TEST_ONLY'), \
                patch('importlib.metadata.version', return_value='0.2.2rc2'), \
                contextlib.redirect_stdout(io.StringIO()):
            exec(self.python_source().replace('RUN_HARNESS = False', 'RUN_HARNESS = True'), namespace)
        for name in ('persistent-bash', 'persistent-pwsh', 'tool-fs', 'tool-working-directory',
                     'session-log-deepseek', 'plugin-package-inventory-deepseek'):
            self.assertIn(f'- id: {name}\n  disabled: true\n', captured['patch'])
        self.assertTrue(captured['workspace_exists'])
        self.assertFalse(Path(captured['options']['cwd']).exists())
        self.assertEqual(captured['options']['profile'], 'sdk-minimal')
        self.assertEqual(captured['prompt'], 'same question')


if __name__ == '__main__':
    unittest.main()
