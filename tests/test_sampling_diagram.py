"""Guard the numerical claims and publication of the sampling illustration."""
import importlib.util
import json
from pathlib import Path
import re
import unittest

ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location('sampling_diagram', ROOT / 'scripts/build_sampling_diagram.py')
diagram = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(diagram)


class SamplingDiagramTests(unittest.TestCase):
    def test_filters_produce_the_displayed_probabilities(self):
        data = diagram.example()
        self.assertEqual([diagram.percent(x) for x in data['after_temperature']],
                         ['45.51%', '27.60%', '16.74%', '10.15%'])
        self.assertEqual([diagram.percent(x) for x in data['after_k']],
                         ['50.65%', '30.72%', '18.63%', '0.00%'])
        self.assertEqual(data['kept_p'], [0, 1])
        self.assertLess(data['after_k'][0], 0.80)
        self.assertGreaterEqual(data['accumulated'], 0.80)
        self.assertEqual([diagram.percent(x) for x in data['after_p']],
                         ['62.25%', '37.75%', '0.00%', '0.00%'])
        self.assertAlmostEqual(sum(data['after_p']), 1.0)

    def test_generated_artifact_is_current_and_linked_from_lab_and_site(self):
        self.assertEqual(diagram.OUTPUT.read_text(), diagram.render())
        lesson = json.loads((ROOT / 'lessons/01_prompting_evaluation.json').read_text())
        lesson_text = '\n'.join(cell['source'] for cell in lesson['cells'])
        self.assertIn('assets/images/sampling-settings.svg', lesson_text)
        js = (ROOT / 'assets/course.js').read_text()
        match = re.search(r'const labs = (\[.*?\n\]);', js, re.S)
        lab = next(lab for lab in json.loads(match[1]) if lab['id'] == '01')
        self.assertEqual(lab['picture']['src'], 'assets/images/sampling-settings.svg')
        self.assertTrue(lab['picture']['alt'])


if __name__ == '__main__':
    unittest.main()
