import tempfile
import unittest
from pathlib import Path

import numpy as np
from PIL import Image

from generate_topodata_gap_seeds import pixel_window, seed_cell


class TopodataGapSeedTests(unittest.TestCase):
    def test_pixel_window_selects_centres_inside_cell(self):
        window = pixel_window(-2, 1, 0.25, 0.25, 8, 8, -1.5, -0.5, -1.0, 0.0)
        self.assertEqual(window, (2, 4, 4, 6))

    def test_pixel_window_clips_to_raster(self):
        window = pixel_window(-2, 1, 0.25, 0.25, 8, 8, -3, -2, 0, 2)
        self.assertEqual(window, (0, 0, 8, 8))

    def test_seed_cell_uses_highest_pixel_and_reports_relative_relief(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            values = np.array([[10, 20], [30, 40]], dtype=np.float32)
            Image.fromarray(values).save(root / "tile.tif")
            tiles = [{
                "west": -1.0, "south": -1.0, "east": 0.0, "north": 0.0,
                "geotiff": "tile.tif", "pixel_x": 0.5, "pixel_y": 0.5,
            }]
            row = {"cell_id": "cell:test", "uf": "ZZ", "latitude": -0.5, "longitude": -0.5}
            seed = seed_cell(row, tiles, root, 1.0)
            self.assertEqual(seed["elevation_m"], 40.0)
            self.assertEqual(seed["relative_relief_m"], 30.0)
            self.assertEqual(seed["longitude"], -0.25)
            self.assertEqual(seed["latitude"], -0.75)
            self.assertEqual(seed["valid_pixel_count"], 4)


if __name__ == "__main__":
    unittest.main()
