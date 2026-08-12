import unittest

from blender_topografia_radomes.terrain_mesh_geometry import vertices_from_window


class Array:
    shape = (3, 3)

    def __getitem__(self, key):
        row, column = key
        return ((100, 110, 120), (130, 140, 150), (160, 170, 180))[row][column]


class ExportTopodataTerrainMeshTests(unittest.TestCase):
    def test_one_vertex_is_created_for_each_dem_cell(self):
        vertices, width, height = vertices_from_window(
            Array(), (-50, .001, 0, -20, 0, -.001), 10, 20, 1
        )
        self.assertEqual((width, height), (3, 3))
        self.assertEqual(vertices[0], [-49.9895, -20.0205, 100.0])
        self.assertEqual(vertices[-1], [-49.9875, -20.0225, 180.0])
