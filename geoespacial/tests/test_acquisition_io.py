import tempfile
import unittest
from pathlib import Path

from acquire_http import acquire, file_sha256
from extract_zip import safe_destination


class AcquisitionIoTest(unittest.TestCase):
    def test_local_url_acquisition_is_atomic_and_hash_checked(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            source = root / "source.bin"
            source.write_bytes(b"radome")
            target = root / "raw" / "target.bin"
            result = acquire(source.as_uri(), target, file_sha256(source))
            self.assertEqual(target.read_bytes(), b"radome")
            self.assertEqual(result["sha256"], file_sha256(source))

    def test_zip_member_cannot_escape_destination(self):
        with tempfile.TemporaryDirectory() as directory:
            with self.assertRaises(ValueError):
                safe_destination(Path(directory), "../escape.txt")


if __name__ == "__main__":
    unittest.main()
