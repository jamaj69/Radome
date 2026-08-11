import json
import sys
import tempfile
import unittest
import zipfile
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from acquire_topodata_route_tiles import acquire_selection


class AcquireTopodataRouteTilesTest(unittest.TestCase):
    def setUp(self):
        self.temporary = tempfile.TemporaryDirectory()
        self.root = Path(self.temporary.name)

    def tearDown(self):
        self.temporary.cleanup()

    def make_selection(self, source: Path) -> Path:
        selection = self.root / "selection.json"
        selection.write_text(json.dumps({
            "archives": [{"name": "22S465ZN.zip", "url": source.as_uri(), "listed_size_bytes": 123}],
            "missing_archive_names": ["26S48_ZN.zip"],
        }), encoding="utf-8")
        return selection

    def test_downloads_valid_zip_and_then_reuses_it(self):
        source = self.root / "source.zip"
        with zipfile.ZipFile(source, "w") as archive:
            archive.writestr("22S465ZN.tif", b"fake-geotiff")
        selection = self.make_selection(source)
        output = self.root / "raw"
        report = self.root / "report.json"

        first = acquire_selection(selection, output, report)
        second = acquire_selection(selection, output, report)

        self.assertTrue(first["complete"])
        self.assertEqual(first["archives"][0]["status"], "downloaded")
        self.assertEqual(second["archives"][0]["status"], "reused")
        self.assertEqual(second["missing_archive_names_from_selection"], ["26S48_ZN.zip"])

    def test_records_invalid_zip_without_publishing_target(self):
        source = self.root / "invalid.zip"
        source.write_bytes(b"not a zip")
        selection = self.make_selection(source)
        output = self.root / "raw"

        result = acquire_selection(selection, output, self.root / "report.json")

        self.assertFalse(result["complete"])
        self.assertEqual(result["failed_archive_count"], 1)
        self.assertFalse((output / "22S465ZN.zip").exists())


if __name__ == "__main__":
    unittest.main()
