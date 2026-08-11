import sys
import unittest
from collections import Counter
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from evaluate_anatel_radio_link_paths_topodata import candidate_status


class CandidatePathTerrainStatusTest(unittest.TestCase):
    def test_any_fresnel_path_has_priority(self):
        self.assertEqual(candidate_status(Counter({"fresnel60_clear": 1, "terrain_or_curvature_obstructed": 2})), "at_least_one_fresnel60_clear_path")

    def test_los_only_precedes_obstructed(self):
        self.assertEqual(candidate_status(Counter({"los_clear_fresnel_obstructed": 1, "terrain_or_curvature_obstructed": 2})), "at_least_one_los_only_path")

    def test_all_missing_fails_closed(self):
        self.assertEqual(candidate_status(Counter({"terrain_missing": 2})), "terrain_missing_for_all_paths")


if __name__ == "__main__":
    unittest.main()
