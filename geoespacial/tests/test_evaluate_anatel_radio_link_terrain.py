import unittest
from evaluate_anatel_radio_link_terrain import profile
class TerrainTest(unittest.TestCase):
 def test_flat_short_route_is_clear(self):
  x=profile((0,0),(0,.01),1.112,30,30,1000,lambda lat,lon:0,k=1)
  self.assertEqual(x["missing"],0);self.assertGreater(x["los"],0);self.assertGreater(x["fresnel"],0)
 def test_missing_terrain_fails_closed(self):
  self.assertGreater(profile((0,0),(0,.01),1.112,30,30,1000,lambda lat,lon:None)["missing"],0)
if __name__=="__main__":unittest.main()
