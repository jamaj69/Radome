import unittest

from blender_topografia_radomes.terrain_mesh_geometry import terrain_geometry


class RenderTopodataLocalTerrainTests(unittest.TestCase):
    def test_faces_and_z_follow_the_dem_elevations(self):
        site = {
            "longitude": -48.0, "latitude": -16.0, "width": 2, "height": 2,
            "vertices": [[-48, -16, 100], [-47.999, -16, 110], [-48, -16.001, 120], [-47.999, -16.001, 130]],
        }
        vertices, faces, reference = terrain_geometry(site, 2.0)
        self.assertEqual(reference, 100)
        self.assertEqual([vertex[2] for vertex in vertices], [0, 20, 40, 60])
        self.assertEqual(faces, [(0, 1, 3, 2)])
