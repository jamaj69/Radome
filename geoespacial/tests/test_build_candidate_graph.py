import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from build_candidate_graph import horizon_km, node_id, tile_pixel


class CandidateGraphTest(unittest.TestCase):
    def test_horizon_increases_with_height(self):
        self.assertGreater(horizon_km(1000, 4 / 3), horizon_km(100, 4 / 3))

    def test_tile_pixel_stays_inside_tile(self):
        _, _, pixel_x, pixel_y = tile_pixel(-47.88, -15.78, 8)
        self.assertTrue(0 <= pixel_x < 256)
        self.assertTrue(0 <= pixel_y < 256)

    def test_airport_id_does_not_use_repeated_placeholder_code(self):
        first = {"properties": {"siglaicao": "NI"}, "geometry": {"coordinates": [-40, -20]}}
        second = {"properties": {"siglaicao": "NI"}, "geometry": {"coordinates": [-41, -20]}}
        self.assertNotEqual(node_id("airport", first), node_id("airport", second))


if __name__ == "__main__":
    unittest.main()
