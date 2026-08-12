import unittest

from topodata_tile_plan import starts, windows
from regional_terrain_geometry import grid_shape, regional_bounds


class TopodataTilePlanTest(unittest.TestCase):
    def test_blocks_share_their_border_and_cover_the_full_leaf(self):
        plan = windows(10, 8, 3)
        self.assertEqual(plan[0], (0, 0, 4, 4))
        self.assertEqual(plan[-1], (6, 6, 4, 2))
        self.assertEqual(starts(10, 3), [0, 3, 6])
        self.assertEqual(starts(8, 3), [0, 3, 6])

    def test_invalid_block_size_fails(self):
        with self.assertRaises(ValueError):
            windows(10, 8, 1)

    def test_regional_grid_has_margin_and_exact_edges(self):
        sites = [{"longitude": -48, "latitude": -16}, {"longitude": -46, "latitude": -22}]
        bounds = regional_bounds(sites, .25)
        self.assertEqual(bounds, (-48.25, -22.25, -45.75, -15.75))
        longitudes, latitudes = grid_shape(bounds, .2)
        self.assertEqual((longitudes[0], longitudes[-1]), (-48.25, -45.75))
        self.assertEqual((latitudes[0], latitudes[-1]), (-22.25, -15.75))


if __name__ == "__main__":
    unittest.main()
