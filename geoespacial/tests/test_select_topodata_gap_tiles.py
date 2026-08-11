import csv
import gzip
import json
import tempfile
import unittest
from pathlib import Path

from select_topodata_gap_tiles import cell_sample_points, select


class TopodataGapTileTests(unittest.TestCase):
    def test_cell_points_include_centre_and_four_interior_corners(self):
        points = cell_sample_points(-10.125, -50.125, 0.25)
        self.assertEqual(len(points), 5)
        self.assertEqual(points[0], (-10.125, -50.125))
        self.assertTrue(all(-10.25 < latitude < -10 for latitude, _ in points[1:]))
        self.assertTrue(all(-50.25 < longitude < -50 for _, longitude in points[1:]))

    def test_selects_only_tiles_of_uncovered_cells_and_preserves_missing_names(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            grid = root / "grid.csv.gz"
            fields = ["latitude", "longitude", "uf", "covering_candidate_count"]
            with gzip.open(grid, "wt", encoding="utf-8", newline="") as target:
                writer = csv.DictWriter(target, fieldnames=fields)
                writer.writeheader()
                writer.writerow({"latitude": -10.125, "longitude": -50.125, "uf": "PA", "covering_candidate_count": 0})
                writer.writerow({"latitude": -22.125, "longitude": -47.125, "uf": "SP", "covering_candidate_count": 1})
            names = ["10S51_ZN.zip"]
            manifest = root / "manifest.json"
            manifest.write_text(json.dumps({"archives": [
                {"name": name, "url": f"https://example/{name}", "listed_size_bytes": 10} for name in names
            ]}), encoding="utf-8")
            result = select(grid, manifest, root / "selection.json")
            self.assertEqual(result["uncovered_cell_count"], 1)
            self.assertEqual(result["uncovered_cells_by_uf"], {"PA": 1})
            self.assertEqual(result["selected_archive_count"], 1)
            self.assertNotIn("22S48_ZN.zip", result["missing_archive_names"])

    def test_rejects_resolution_larger_than_tile_height(self):
        with self.assertRaises(ValueError):
            cell_sample_points(0, 0, 1.1)


if __name__ == "__main__":
    unittest.main()
