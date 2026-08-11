import tempfile
import unittest
from pathlib import Path

from verify_reproducibility import sha256


class ReproducibilityTest(unittest.TestCase):
    def test_hash_is_stable_for_same_bytes(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "product.bin"
            path.write_bytes(b"same input, same output")
            first = sha256(path)
            second = sha256(path)
            self.assertEqual(first, second)


if __name__ == "__main__":
    unittest.main()
