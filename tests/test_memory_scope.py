"""Prevent a retrieved retry lesson from being applied outside its approved scope."""
import ast
import json
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]


class MemoryScopeTests(unittest.TestCase):
    def setUp(self):
        lesson = json.loads((ROOT / 'lessons/08_human_feedback_memory.json').read_text())
        source = next(c['source'] for c in lesson['cells'] if c['type'] == 'code' and 'def recall(' in c['source'])
        fn = next(n for n in ast.parse(source).body if isinstance(n, ast.FunctionDef) and n.name == 'recall')
        self.queries = []
        calls = self.queries

        class FakeMemory:
            def query(self, **kwargs):
                calls.append(kwargs)
                eligible = kwargs['where'] is None or kwargs['where'] == {
                    '$and': [{'idempotent': True}, {'transient': True}]}
                return {'distances': [[0.1] if eligible else []],
                        'metadatas': [[{'lesson': 'approved advice'}] if eligible else []]}

        ns = {'memory': FakeMemory()}
        exec(compile(ast.Module(body=[fn], type_ignores=[]), '<memory-scope>', 'exec'), ns)
        self.recall = ns['recall']

    def test_unknown_or_invalid_scope_returns_no_applicable_advice(self):
        for idem, transient in ((None, True), (True, None), ('true', True), (True, 1)):
            with self.subTest(idempotent=idem, transient=transient):
                self.assertEqual(self.recall('case', idempotent=idem, transient=transient), [])
        self.assertEqual(self.queries, [])

    def test_both_approved_conditions_are_required(self):
        self.assertTrue(self.recall('case', idempotent=True, transient=True))
        self.assertFalse(self.recall('case', idempotent=False, transient=True))
        self.assertFalse(self.recall('case', idempotent=True, transient=False))

    def test_candidates_only_is_an_explicit_unfiltered_diagnostic(self):
        self.assertTrue(self.recall('case', candidates_only=True))
        self.assertIsNone(self.queries[-1]['where'])


if __name__ == '__main__':
    unittest.main()
