"""Check sequential reviewers and their persisted evidence links."""
import contextlib
import io
import json
import os
from pathlib import Path
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]


class Lab07LoggingTests(unittest.TestCase):
    def test_logs_decision_and_adds_rule_reviewer(self):
        lesson = json.loads((ROOT / 'lessons/07_observe_trace_swap.json').read_text())
        cells = [cell['source'] for cell in lesson['cells'] if cell['type'] == 'code']
        replies = iter([
            '{"option":"CQRS","claim":"Search.","cites":["R3"]}',
            'Plain text rather than a proposal object.',
            '{"option":"CQRS","claim":"Search.","cites":["R3"]}',
            '{"option":"CQRS","claim":"Search.","cites":["C1"]}',
        ])
        ns = {'ask': lambda prompt: next(replies)}
        original_cwd = os.getcwd()
        with tempfile.TemporaryDirectory() as directory:
            try:
                os.chdir(directory)
                with contextlib.redirect_stdout(io.StringIO()):
                    for source in cells:
                        exec(source, ns)
                    self.assertEqual(ns['decision']['kind'], 'escalation')
                    exec(cells[3], ns)
                    exec(cells[4], ns)
                    exec(cells[5], ns)
                self.assertEqual(ns['decision']['option'], 'CQRS')
                self.assertEqual(len(ns['decision']['cites']), 3)
                ns['CASE']['cross_service_search'] = False
                ns['ask'] = lambda prompt: '{"option":"API composition","claim":"Bad citation.","cites":[{}]}'
                with contextlib.redirect_stdout(io.StringIO()):
                    exec(cells[3], ns)
                rulebook = next(message for message in ns['accepted'] if message['sender'] == 'Rulebook')
                self.assertEqual(rulebook['option'], 'API composition')
                with open('council.log') as log:
                    messages = [json.loads(line) for line in log]
                by_id = {message['id']: message for message in messages}
                self.assertEqual(len(by_id), len(messages))
                invalid_json = next(message for message in messages if message.get('reason') == 'Invalid JSON')
                self.assertEqual(invalid_json['kind'], 'rejected')
                self.assertEqual(invalid_json['sender'], 'Modernizer')
                self.assertTrue(all('time' in message for message in messages))
                chair_messages = [message for message in messages if message['sender'] == 'Chair']
                self.assertEqual(len(chair_messages), 2)
                self.assertEqual(chair_messages[0]['trace_id'], invalid_json['trace_id'])
                self.assertNotEqual(chair_messages[0]['trace_id'], chair_messages[1]['trace_id'])
                for decision in chair_messages:
                    self.assertTrue(decision['cites'])
                    for proposal_id in decision['cites']:
                        self.assertEqual(by_id[proposal_id]['trace_id'], decision['trace_id'])
            finally:
                os.chdir(original_cwd)


if __name__ == '__main__':
    unittest.main()
