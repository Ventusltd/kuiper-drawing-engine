import importlib.util
from pathlib import Path
import tempfile
import unittest

spec = importlib.util.spec_from_file_location('gate', Path(__file__).resolve().parents[1] / 'tools/check_public_bundle.py')
gate = importlib.util.module_from_spec(spec)
spec.loader.exec_module(gate)


class BundleTest(unittest.TestCase):
    def test_extra_data_file_is_rejected(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            for name in gate.ALLOWED:
                (root / name).write_text('synthetic fixture')
            self.assertEqual(len(gate.check(root)['files']), 5)
            (root / 'local-review.json').write_text('{}')
            with self.assertRaises(ValueError):
                gate.check(root)

    def test_missing_file_is_rejected(self):
        with tempfile.TemporaryDirectory() as temp:
            with self.assertRaises(ValueError):
                gate.check(Path(temp))


if __name__ == '__main__':
    unittest.main()
