"""Check the full-context and retrieval comparison without model credentials."""
import contextlib
import io
import json
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]


class RAGLessonTests(unittest.TestCase):
    def test_same_questions_compare_full_library_with_retrieved_context(self):
        lesson = json.loads((ROOT / 'lessons/02_rag_systems.json').read_text())
        code = [c['source'] for c in lesson['cells'] if c['type'] == 'code']
        prompts = []

        class Model:
            def __init__(self):
                self.trace = []
            def ask(self, prompt):
                prompts.append(prompt)
                self.trace.append({'input_tokens': len(prompt.split()) + 3})
                if 'lunch?' in prompt.splitlines()[0]:
                    return 'The supplied policies do not answer this question.'
                return 'Use the retrieved policy [P1].' if 'Reporting' in prompt else 'Use CQRS [P3].'

        namespace = {'client': Model()}
        output = io.StringIO()
        with contextlib.redirect_stdout(output):
            exec(code[0], namespace)
            exec(code[1], namespace)
        records = {pid: (category, text) for pid, category, text in namespace['records']}
        self.assertEqual(len(namespace['policies']), 3)
        self.assertEqual(len(records), 9)
        self.assertEqual(len(prompts), 3)
        for prompt in prompts:
            for policy_id in records:
                self.assertIn(f'[{policy_id}]', prompt)

        class Search:
            def __init__(self):
                self.questions = []
            def query(self, *, query_texts, n_results):
                self.questions.append(query_texts[0])
                self.assert_two(n_results)
                ids = ['P1', 'P2'] if 'Reporting' in query_texts[0] else ['P3', 'P2']
                return {'ids': [ids], 'documents': [[records[i][1] for i in ids]],
                        'metadatas': [[{'category': records[i][0]} for i in ids]],
                        'distances': [[0.1, 0.3]]}
            @staticmethod
            def assert_two(n_results):
                if n_results != 2:
                    raise AssertionError('Expected two retrieved policies')

        search = Search()
        namespace['collection'] = search
        with contextlib.redirect_stdout(output):
            exec(code[3], namespace)
            exec(code[4], namespace)
        self.assertEqual(len(search.questions), 8)  # five demonstrations, three model calls
        self.assertEqual(len(prompts), 6)
        for baseline, rag in zip(prompts[:3], prompts[3:]):
            self.assertEqual(baseline.splitlines()[0], rag.splitlines()[0])
            self.assertEqual(baseline.splitlines()[-1], rag.splitlines()[-1])
            self.assertLess(len(rag.split()), len(baseline.split()))
            self.assertEqual(sum(f'[{policy_id}]' in rag for policy_id in records), 2)
        self.assertEqual(output.getvalue().count('Citation IDs valid: True'), 2)
        self.assertIn('What should we eat for lunch?', prompts[-1])
        self.assertIn('Reported insufficient evidence: True', output.getvalue())
        self.assertIn('Citation IDs valid: not needed', output.getvalue())
        self.assertIn('words (not tokens)', output.getvalue())
        self.assertEqual(output.getvalue().count('Provider input tokens:'), 6)

        class ModelWithoutUsage(Model):
            def ask(self, prompt):
                answer = super().ask(prompt)
                self.trace[-1]['input_tokens'] = None
                return answer.replace('[P1]', 'P1')

        namespace['client'] = ModelWithoutUsage()
        missing_usage = io.StringIO()
        with contextlib.redirect_stdout(missing_usage):
            exec(code[1], namespace)
            exec(code[4], namespace)
        self.assertIn('Provider input tokens: not reported', missing_usage.getvalue())
        self.assertIn('all policies = None | retrieved = None', missing_usage.getvalue())
        self.assertIn('Citation IDs valid: False', missing_usage.getvalue())


if __name__ == '__main__':
    unittest.main()
