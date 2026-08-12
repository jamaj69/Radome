import unittest
from pathlib import Path
from tempfile import TemporaryDirectory
import json

from select_regional_topodata_tiles import build, required_names, tile_name


class RegionalTopodataTilesTest(unittest.TestCase):
    def test_official_name_at_the_18s_48w_boundary(self):
        self.assertEqual(tile_name(-17.99, -47.98), "17S48_ZN.zip")
        self.assertEqual(tile_name(-18.01, -47.98), "18S48_ZN.zip")

    def test_regional_requirements_include_the_northern_missing_leaf(self):
        names = required_names((-49.18, -22.09, -46.31, -15.53), .02)
        self.assertIn("17S48_ZN.zip", names)
        self.assertIn("18S48_ZN.zip", names)

    def test_explicit_bbox_overrides_automatic_margin(self):
        with TemporaryDirectory() as directory:
            root = Path(directory)
            selection = root / "sites.json"; manifest = root / "manifest.json"; output = root / "selection.json"
            selection.write_text(json.dumps({"selected_sites": [{"longitude": -48, "latitude": -17}]}))
            manifest.write_text(json.dumps({"archives": [
                {"name": "17S48_ZN.zip", "url": "test", "listed_size_bytes": 1},
                {"name": "18S48_ZN.zip", "url": "test", "listed_size_bytes": 1},
            ]}))
            result = build(selection, manifest, root, output, bbox=(-48, -18, -47, -17))
            self.assertEqual(result["bbox_wgs84"], [-48.0, -18.0, -47.0, -17.0])


if __name__ == "__main__":
    unittest.main()
