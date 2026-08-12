import unittest

from blender_topografia_radomes.export_local_boundaries import bounds


class ExportLocalBoundariesTests(unittest.TestCase):
    def test_derives_window_bounds_from_terrain_vertices(self):
        site = {"vertices": [[-48.2, -16.1, 1000], [-47.8, -15.8, 1200], [-48.0, -16.3, 900]]}
        self.assertEqual(bounds(site), (-48.2, -16.3, -47.8, -15.8))
