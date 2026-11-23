"""Check the lesson's message flow and validation with offline replies."""
import contextlib
import io
import json
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]
LESSON = json.loads((ROOT / 'lessons/01_prompting_evaluation.json').read_text())
CELLS = [cell['source'] for cell in LESSON['cells'] if cell['type'] == 'code']


class ScriptedClient:
    def __init__(self, responses):
        self.responses = iter(responses)
        self.calls = []

    def ask(self, prompt, **kwargs):
        self.calls.append((prompt, kwargs))
        return next(self.responses)


def run(cell, namespace):
    with contextlib.redirect_stdout(io.StringIO()) as output:
        exec(CELLS[cell], namespace)
    return output.getvalue()


class PromptingLessonTests(unittest.TestCase):
    def test_split_preserves_mixed_content_and_reuses_system_instructions(self):
        client = ScriptedClient(['mixed answer', 'split answer', 'next answer'])
        run(0, {'plain': client})
        mixed, split, next_question = client.calls
        self.assertEqual(mixed[1]['system'], '')
        self.assertEqual(mixed[0], split[1]['system'] + "\n" + split[0])
        self.assertEqual(split[1]['system'], next_question[1]['system'])
        self.assertNotEqual(split[0], next_question[0])

    def test_follow_up_carries_the_actual_previous_response(self):
        client = ScriptedClient(['actual model recommendation', 'trade-off'])
        run(1, {'plain': client})
        self.assertIn('actual model recommendation', client.calls[1][0])
        self.assertNotIn('actual model recommendation', client.calls[0][0])

    def test_validation_rejects_wrong_decision_and_malformed_json(self):
        for reply, expected in [
            ('{"decision":"BFF","reason":"Tailored to mobile."}', 'Valid format: True | Expected decision: True'),
            ('{"decision":"API gateway","reason":"Shared edge."}', 'Valid format: True | Expected decision: False'),
            ('not JSON', 'Valid format: False'),
            ('[]', 'Valid format: False'),
            ('{"decision":"BFF","reason": "  "}', 'Valid format: False'),
        ]:
            with self.subTest(reply=reply):
                self.assertIn(expected, run(2, {'plain': ScriptedClient([reply])}))


if __name__ == '__main__':
    unittest.main()
