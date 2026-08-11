import unittest

from consolidate_topodata_gap_candidates import consolidate, destination, ring_clearance


class ConsolidateTopodataGapCandidatesTests(unittest.TestCase):
    def test_destination_zero_distance_preserves_point(self):
        latitude, longitude = destination(-10, -50, 0, 123)
        self.assertAlmostEqual(latitude, -10)
        self.assertAlmostEqual(longitude, -50)

    def test_consolidation_keeps_higher_score_and_assigns_every_seed(self):
        rows = [
            {"seed_id": "a", "latitude": 0, "longitude": 0, "terrain_score": 0.9},
            {"seed_id": "b", "latitude": 0, "longitude": 0.01, "terrain_score": 0.8},
            {"seed_id": "c", "latitude": 0, "longitude": 1, "terrain_score": 0.7},
        ]
        selected, assignment = consolidate(rows, 10)
        self.assertEqual([row["seed_id"] for row in selected], ["a", "c"])
        self.assertEqual(assignment, {"a": "a", "b": "a", "c": "c"})

    def test_ring_clearance_reports_partial_sampling(self):
        class Terrain:
            def __call__(self, latitude, longitude):
                return 90.0 if longitude >= 0 else None

        clearance, count = ring_clearance(Terrain(), 0, 0, 100, 5, 8)
        self.assertEqual(clearance, 10.0)
        self.assertLess(count, 8)


if __name__ == "__main__":
    unittest.main()
