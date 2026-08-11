import unittest

from prioritize_augmented_mesh_edges import face_edges


class PrioritizeAugmentedMeshEdgesTests(unittest.TestCase):
    def test_face_edges_are_unique_and_stable(self):
        self.assertEqual(face_edges("c|a|b"), [("a", "b"), ("a", "c"), ("b", "c")])

    def test_rejects_invalid_face(self):
        with self.assertRaises(ValueError):
            face_edges("a|a|b")


if __name__ == "__main__":
    unittest.main()
