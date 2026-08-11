import unittest

from reclassify_augmented_mesh_faces_topodata import face_status


class ReclassifyAugmentedMeshFacesTopodataTests(unittest.TestCase):
    def test_face_status_uses_only_los_edge_count(self):
        self.assertEqual(face_status(3), "triangle_k3_terrain_los")
        self.assertEqual(face_status(2), "triangle_two_edge_terrain_los")
        self.assertEqual(face_status(1), "triangle_sparse_terrain_los")
        self.assertEqual(face_status(0), "triangle_sparse_terrain_los")


if __name__ == "__main__": unittest.main()
