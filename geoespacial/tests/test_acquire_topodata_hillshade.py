import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "blender_topografia_radomes"))
from acquire_topodata_hillshade import hillshade_archive_name


class AcquireTopodataHillshadeTests(unittest.TestCase):
    def test_converts_altitude_tile_name_to_matching_rs_archive(self):
        self.assertEqual(hillshade_archive_name("21S48_ZN.tif"), "21S48_RS.zip")
        self.assertEqual(hillshade_archive_name("16S495ZN.tif"), "16S495RS.zip")
