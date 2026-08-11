import unittest
from consolidate_anatel_radio_link_prequalification import qualification


class RadioLinkPrequalificationTest(unittest.TestCase):
    def test_all_gates_prequalify_without_pairing(self):
        result, blockers = qualification("unambiguous_cadastral_height", "horizontal_consistent_15deg", "fresnel60_clear", "vertical_consistent_1deg")
        self.assertEqual(result, "cadastral_prequalified")
        self.assertEqual(blockers, [])

    def test_every_failed_gate_is_preserved(self):
        result, blockers = qualification("missing_height", "horizontal_inconsistent_15deg", "terrain_or_curvature_obstructed", "vertical_inconsistent_1deg")
        self.assertEqual(result, "blocked")
        self.assertEqual(len(blockers), 4)

    def test_missing_derived_products_fail_closed(self):
        result, blockers = qualification("unambiguous_cadastral_height", "horizontal_consistent_15deg", None, None)
        self.assertEqual(result, "blocked")
        self.assertIn("terrain_not_evaluated", blockers)


if __name__ == "__main__":
    unittest.main()
