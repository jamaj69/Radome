import unittest

from build_augmented_candidate_graph import candidate_attributes


class AugmentedCandidateGraphTests(unittest.TestCase):
    def test_gap_candidate_remains_nonoperational_and_has_positive_radius(self):
        row = {"candidate_id": "gap:1", "longitude": "-50", "latitude": "-10", "elevation_m": "500",
               "multiscale_status": "summit_like_all_scales", "terrain_score": "0.5", "uf": "MT",
               "represented_cell_count": "2", "represented_cell_ids": "a|b", "seed_id": "seed:1"}
        attributes = candidate_attributes(row, 15.0, 3000.0, 4.0 / 3.0)
        self.assertEqual(attributes["node_type"], "candidate_radome_gap")
        self.assertFalse(attributes["operational_site"])
        self.assertGreater(attributes["coverage_radius_km"], 0)
        self.assertIn("pending", attributes["radius_status"])


if __name__ == "__main__":
    unittest.main()
