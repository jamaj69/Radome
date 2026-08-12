import unittest

from select_regional_topodata_tiles import required_names, tile_name


class RegionalTopodataTilesTest(unittest.TestCase):
    def test_official_name_at_the_18s_48w_boundary(self):
        self.assertEqual(tile_name(-17.99, -47.98), "17S48_ZN.zip")
        self.assertEqual(tile_name(-18.01, -47.98), "18S48_ZN.zip")

    def test_regional_requirements_include_the_northern_missing_leaf(self):
        names = required_names((-49.18, -22.09, -46.31, -15.53), .02)
        self.assertIn("17S48_ZN.zip", names)
        self.assertIn("18S48_ZN.zip", names)


if __name__ == "__main__":
    unittest.main()
