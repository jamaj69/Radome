import unittest
from select_topodata_route_tiles import tile_name
class TopodataTileTest(unittest.TestCase):
 def test_official_upper_left_naming(self):
  self.assertEqual(tile_name(-22.3,-47.2),"22S48_ZN.zip")
  self.assertEqual(tile_name(-22.3,-46.2),"22S465ZN.zip")
  self.assertEqual(tile_name(.5,-51.2),"01N525ZN.zip")
if __name__=="__main__":unittest.main()
