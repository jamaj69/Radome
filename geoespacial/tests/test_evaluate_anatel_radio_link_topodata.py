import json
import sys
import tempfile
import unittest
from pathlib import Path

from PIL import Image, TiffImagePlugin

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from evaluate_anatel_radio_link_topodata import Topodata


class TopodataSamplerTest(unittest.TestCase):
    def test_samples_indexed_tile_and_fails_closed_outside(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            tags = TiffImagePlugin.ImageFileDirectory_v2()
            tags[33550] = (0.5, 0.5, 0.0)
            tags[33922] = (0.0, 0.0, 0.0, -46.5, -22.0, 0.0)
            Image.new("F", (3, 2), 123.0).save(root / "tile.tif", tiffinfo=tags)
            index = root / "index.geojson"
            index.write_text(json.dumps({"features": [{"geometry": {"coordinates": [[[-46.5, -23], [-45, -23], [-45, -22], [-46.5, -22], [-46.5, -23]]]}, "properties": {"geotiff": "tile.tif", "pixel_size_x_degrees": 0.5, "pixel_size_y_degrees": 0.5}}]}), encoding="utf-8")
            sampler = Topodata(root, index, cache_size=1)
            try:
                self.assertEqual(sampler(-22.25, -46.25), 123.0)
                self.assertIsNone(sampler(-24.0, -46.25))
            finally:
                sampler.close()


if __name__ == "__main__":
    unittest.main()
