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
            '{"option":"CQRS","claim":"Bad citation.","cites":[{}]}',
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
                    exec(cells[2], ns)
                    exec(cells[3], ns)
                    exec(cells[4], ns)
                self.assertEqual(ns['decision']['option'], 'CQRS')
                self.assertEqual(len(ns['decision']['cites']), 3)
                ns['CASE']['cross_service_search'] = False
                ns['ask'] = lambda prompt: '{"option":"API composition","claim":"Small lookup.","cites":["R2"]}'
                with contextlib.redirect_stdout(io.StringIO()):
                    exec(cells[2], ns)
                rulebook = next(message for message in ns['accepted'] if message['sender'] == 'Rulebook')
                self.assertEqual(rulebook['option'], 'API composition')
                with open('council.log') as log:
                    messages = [json.loads(line) for line in log]
                self.assertEqual(len({message['id'] for message in messages}), len(messages))
                self.assertTrue(any(message['kind'] == 'rejected' for message in messages))
                self.assertTrue(all('time' in message for message in messages))
            finally:
                os.chdir(original_cwd)


if __name__ == '__main__':
    unittest.main()
