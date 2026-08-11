import unittest
from validate_anatel_radio_link_vertical_geometry import angular_error, elevation_angle, status


class VerticalGeometryTest(unittest.TestCase):
    def test_equal_heights_include_earth_curvature_depression(self):
        self.assertLess(elevation_angle(100_000, 1000, 1000, 1.0), 0)

    def test_reverse_angles_have_expected_height_symmetry(self):
        forward = elevation_angle(10_000, 100, 200, 1.0)
        reverse = elevation_angle(10_000, 200, 100, 1.0)
        self.assertGreater(forward, reverse)

    def test_angular_error_wraps(self):
        self.assertAlmostEqual(angular_error(179, -179), 2)

    def test_missing_fails_closed(self):
        self.assertEqual(status(None), "vertical_geometry_missing")


if __name__ == "__main__":
    unittest.main()
