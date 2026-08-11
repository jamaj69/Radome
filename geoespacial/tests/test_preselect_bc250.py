import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from preselect_bc250 import Point, azimuth_sector, deduplicate, distance_km


class PreselectBc250Test(unittest.TestCase):
    def test_distance_is_symmetric(self):
        a = Point("a", -46.63, -23.55)
        b = Point("b", -43.17, -22.91)
        self.assertAlmostEqual(distance_km(a, b), distance_km(b, a))
        self.assertGreater(distance_km(a, b), 300)

    def test_deduplication_keeps_highest_point(self):
        high = Point("high", -44.0, -22.0, 2000)
        low = Point("low", -44.001, -22.001, 1500)
        self.assertEqual(deduplicate([low, high], 10), [high])

    def test_cardinal_azimuth_sectors_differ(self):
        origin = Point("origin", 0, 0)
        north = Point("north", 0, 1)
        east = Point("east", 1, 0)
        self.assertNotEqual(azimuth_sector(origin, north), azimuth_sector(origin, east))


if __name__ == "__main__":
    unittest.main()
