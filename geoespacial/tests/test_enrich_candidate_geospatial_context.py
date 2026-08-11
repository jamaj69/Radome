import unittest

from enrich_candidate_geospatial_context import coordinates, distance_km


class CandidateContextTests(unittest.TestCase):
    def test_coordinates_accept_both_graph_schemas(self):
        self.assertEqual(coordinates({"latitude": -10, "longitude": -40}), (-10.0, -40.0))
        self.assertEqual(coordinates({"y_latitude": -11, "x_longitude": -41}), (-11.0, -41.0))

    def test_great_circle_distance(self):
        self.assertAlmostEqual(distance_km(0, 0, 0, 1), 111.195, places=3)
        self.assertEqual(distance_km(-10, -40, -10, -40), 0.0)


if __name__ == "__main__":
    unittest.main()
