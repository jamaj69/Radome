import json
import sys
import tempfile
import unittest
import zipfile
from pathlib import Path

from PIL import Image, TiffImagePlugin

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from extract_topodata_route_tiles import extract_receipt, sha256_file


class ExtractTopodataRouteTilesTest(unittest.TestCase):
    def setUp(self):
        self.temporary = tempfile.TemporaryDirectory()
        self.root = Path(self.temporary.name)

    def tearDown(self):
        self.temporary.cleanup()

    def make_archive(self) -> tuple[Path, Path]:
        tif = self.root / "22S465ZN.tif"
        tags = TiffImagePlugin.ImageFileDirectory_v2()
        tags[33550] = (0.5, 0.5, 0.0)
        tags[33922] = (0.0, 0.0, 0.0, -46.5, -22.0, 0.0)
        Image.new("F", (3, 2), 100.0).save(tif, tiffinfo=tags)
        archive_dir = self.root / "archives"
        archive_dir.mkdir()
        archive = archive_dir / "22S465ZN.zip"
        with zipfile.ZipFile(archive, "w") as output:
            output.write(tif, tif.name)
        receipt = self.root / "receipt.json"
        receipt.write_text(json.dumps({"archives": [{"name": archive.name, "sha256": sha256_file(archive)}], "missing_archive_names_from_selection": ["26S48_ZN.zip"]}), encoding="utf-8")
        return archive_dir, receipt

    def test_extracts_and_indexes_geotiff_then_reuses_it(self):
        archive_dir, receipt = self.make_archive()
        target = self.root / "target"
        report = self.root / "report.json"
        index = self.root / "index.geojson"

        first = extract_receipt(receipt, archive_dir, target, report, index)
        second = extract_receipt(receipt, archive_dir, target, report, index)

        self.assertTrue(first["complete"])
        self.assertEqual(first["tiles"][0]["status"], "extracted")
        self.assertEqual(second["tiles"][0]["status"], "reused")
        feature = json.loads(index.read_text(encoding="utf-8"))["features"][0]
        self.assertEqual(feature["geometry"]["coordinates"][0][0], [-46.5, -23.0])
        self.assertEqual(first["missing_archive_names_from_selection"], ["26S48_ZN.zip"])

    def test_rejects_archive_hash_mismatch(self):
        archive_dir, receipt = self.make_archive()
        value = json.loads(receipt.read_text(encoding="utf-8"))
        value["archives"][0]["sha256"] = "0" * 64
        receipt.write_text(json.dumps(value), encoding="utf-8")

        result = extract_receipt(receipt, archive_dir, self.root / "target", self.root / "report.json", self.root / "index.json")

        self.assertFalse(result["complete"])
        self.assertEqual(result["failed_archive_count"], 1)


if __name__ == "__main__":
    unittest.main()
