import unittest

from select_augmented_mesh_topodata_tiles import edge_tile_names


class SelectAugmentedMeshTopodataTilesTests(unittest.TestCase):
    def test_short_edge_includes_both_endpoints(self):
        names = edge_tile_names((-10.0, -50.99), (-10.0, -51.01), 2.2, 1.0)
        self.assertEqual(len(names), 4)
        self.assertIn("10S51_ZN.zip", names)
        self.assertIn("10S525ZN.zip", names)

    def test_spacing_must_be_positive(self):
        with self.assertRaises(ValueError):
            edge_tile_names((0, 0), (1, 1), 1, 0)


if __name__ == "__main__":
    unittest.main()
