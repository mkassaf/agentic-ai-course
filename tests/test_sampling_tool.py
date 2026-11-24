"""Verify the provided interactive sampling tool and its course links."""
import json
from pathlib import Path
import re
import subprocess
import unittest

ROOT = Path(__file__).resolve().parents[1]


class SamplingToolTests(unittest.TestCase):
    def test_browser_calculations_use_post_top_k_probabilities(self):
        result = subprocess.run(['node', 'tests/check_sampling_tool.js'], cwd=ROOT,
                                text=True, capture_output=True, timeout=15, check=True)
        self.assertIn('Interactive sampling math passed', result.stdout)

    def test_tool_is_self_contained_and_accessible_from_lab_and_site(self):
        tool = (ROOT / 'assets/tools/sampling.html').read_text()
        self.assertIn('../vendor/chartjs/chart.umd.js', tool)
        self.assertIn("connect-src 'none'", tool)
        self.assertNotIn('window.parent.postMessage', tool)
        self.assertNotIn('pageVault', tool)
        self.assertTrue((ROOT / 'assets/vendor/chartjs/chart.umd.js').is_file())
        self.assertTrue((ROOT / 'assets/vendor/chartjs/LICENSE.md').is_file())
        lesson = json.loads((ROOT / 'lessons/01_prompting_evaluation.json').read_text())
        embed = [c for c in lesson['cells'] if c['type'] == 'code' and c.get('optional') and 'IFrame' in c['source']]
        self.assertEqual(len(embed), 1)
        self.assertIn('assets/tools/sampling.html', embed[0]['source'])
        js = (ROOT / 'assets/course.js').read_text()
        match = re.search(r'const labs = (\[.*?\n\]);', js, re.S)
        lab = next(lab for lab in json.loads(match[1]) if lab['id'] == '01')
        self.assertEqual(lab['tool']['src'], 'assets/tools/sampling.html')
        self.assertEqual(lab['optional_examples'], 3)


if __name__ == '__main__':
    unittest.main()
