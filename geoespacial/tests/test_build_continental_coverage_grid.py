import unittest

from build_continental_coverage_grid import approximate_cell_area_km2, covering_candidates


class ContinentalCoverageGridTests(unittest.TestCase):
    def test_cell_area_decreases_away_from_equator(self):
        self.assertGreater(approximate_cell_area_km2(0, 0.25), approximate_cell_area_km2(-30, 0.25))

    def test_candidate_radius_is_inclusive(self):
        candidates = [{"node_id": "same", "latitude": 0, "longitude": 0, "coverage_radius_km": 0}]
        self.assertEqual(covering_candidates(0, 0, candidates), ["same"])
        self.assertEqual(covering_candidates(0, 0.01, candidates), [])


if __name__ == "__main__":
    unittest.main()
