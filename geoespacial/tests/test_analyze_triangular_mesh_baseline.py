import unittest

import numpy as np

from analyze_triangular_mesh_baseline import CANDIDATE_TYPES, face_status, lambert_azimuthal_equal_area, triangle_quality


class TriangularMeshBaselineTests(unittest.TestCase):
    def test_gap_candidate_is_an_explicit_mesh_vertex_type(self):
        self.assertIn("candidate_radome_gap", CANDIDATE_TYPES)

    def test_projection_centre_maps_to_origin(self):
        x, y = lambert_azimuthal_equal_area(-54, -15)
        self.assertAlmostEqual(x, 0.0)
        self.assertAlmostEqual(y, 0.0)

    def test_equilateral_triangle_quality(self):
        quality = triangle_quality(np.array([[0.0, 0.0], [1.0, 0.0], [0.5, np.sqrt(3) / 2]]))
        self.assertAlmostEqual(quality["minimum_angle_deg"], 60.0)
        self.assertAlmostEqual(quality["edge_aspect_ratio"], 1.0)

    def test_status_does_not_claim_confirmed_visibility(self):
        self.assertEqual(face_status(3), "triangle_k3_curvature_pending")
        self.assertEqual(face_status(2), "triangle_two_edge_curvature_pending")
        self.assertEqual(face_status(1), "triangle_sparse_curvature_pending")


if __name__ == "__main__":
    unittest.main()
