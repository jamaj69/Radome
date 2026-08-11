import unittest

from profile_augmented_mesh_edges_topodata import los_profile, status


class ProfileAugmentedMeshEdgesTopodataTests(unittest.TestCase):
    def test_flat_short_profile_is_clear(self):
        result = los_profile((0, 0), (0, 0.01), 1.1, 15, 15, lambda *_: 100.0, 1.0, 1.0)
        self.assertEqual(status(result), "los_clear")
        self.assertGreater(result["clearance"], 0)

    def test_missing_terrain_fails_closed(self):
        result = los_profile((0, 0), (0, 0.01), 1.1, 15, 15, lambda *_: None, 1.0, 1.0)
        self.assertEqual(status(result), "terrain_missing")


if __name__ == "__main__": unittest.main()
