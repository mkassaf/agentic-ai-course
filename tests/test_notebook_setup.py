"""Prevent stale notebook helpers from silently returning obsolete responses."""
import json
from pathlib import Path
import re
import sys
import types
import unittest
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]


class NotebookSetupTests(unittest.TestCase):
    def provisioning(self, installed_version):
        notebook = json.loads((ROOT / 'notebooks/01_prompting_evaluation.ipynb').read_text())
        setup = next(''.join(c['source']) for c in notebook['cells']
                     if c['cell_type'] == 'code' and 'setup' in c.get('metadata', {}).get('tags', []))
        source = setup.split('PROVIDER =', 1)[0]
        source, count = re.subn(r'(?m)^    %pip install .+$', '    upgrades.append(True)', source)
        self.assertEqual(count, 1)
        old_modules = {key: value for key, value in sys.modules.items()
                       if key == 'coursekit' or key.startswith('coursekit.')}
        sys.modules['coursekit.runtime'] = types.ModuleType('coursekit.runtime')
        ns = {'upgrades': []}
        try:
            with patch('importlib.metadata.version', return_value=installed_version), \
                 patch('importlib.util.find_spec', return_value=object()):
                exec(source, ns)
            removed = 'coursekit.runtime' not in sys.modules
        finally:
            for key in list(sys.modules):
                if key == 'coursekit' or key.startswith('coursekit.'):
                    del sys.modules[key]
            sys.modules.update(old_modules)
        return ns['upgrades'], removed

    def test_old_installed_helper_is_upgraded_and_unloaded(self):
        upgrades, removed = self.provisioning('0.5.0')
        self.assertEqual(upgrades, [True])
        self.assertTrue(removed)

    def test_current_installed_helper_is_reused(self):
        upgrades, removed = self.provisioning('0.5.1')
        self.assertEqual(upgrades, [])
        self.assertFalse(removed)


if __name__ == '__main__':
    unittest.main()
