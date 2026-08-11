import csv
import gzip
import tempfile
import unittest
from pathlib import Path

from select_topodata_gap_ring_tiles import required_names, requirements


class SelectTopodataGapRingTilesTests(unittest.TestCase):
    def test_required_names_include_seed_and_ring_tiles(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "seeds.csv.gz"
            with gzip.open(path, "wt", encoding="utf-8", newline="") as target:
                writer = csv.DictWriter(target, fieldnames=["latitude", "longitude"])
                writer.writeheader()
                writer.writerow({"latitude": -10.0, "longitude": -50.99})
            count, names = required_names(path, 8)
            self.assertEqual(count, 1)
            self.assertIn("10S51_ZN.zip", names)
            self.assertGreaterEqual(len(names), 1)

    def test_requirements_count_points_and_affected_seed(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "seeds.csv.gz"
            with gzip.open(path, "wt", encoding="utf-8", newline="") as target:
                writer = csv.DictWriter(
                    target, fieldnames=["seed_id", "latitude", "longitude"]
                )
                writer.writeheader()
                writer.writerow(
                    {"seed_id": "seed:a", "latitude": -10.0, "longitude": -50.99}
                )
            count, point_counts, seed_ids = requirements(path, 8)
            self.assertEqual(count, 1)
            self.assertEqual(sum(point_counts.values()), 25)
            self.assertTrue(all(ids == {"seed:a"} for ids in seed_ids.values()))

    def test_rejects_too_few_azimuths(self):
        with self.assertRaises(ValueError):
            required_names(Path("unused"), 4)


if __name__ == "__main__":
    unittest.main()
