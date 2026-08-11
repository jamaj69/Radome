import csv
import gzip
import json
import tempfile
import unittest
from pathlib import Path

from blender_topografia_radomes.select_visual_sites import build


class SelectBlenderVisualSitesTests(unittest.TestCase):
    def test_selects_three_high_elevation_candidates_by_rank(self):
        with tempfile.TemporaryDirectory() as directory:
            ranking, output = Path(directory) / "ranking.csv.gz", Path(directory) / "selection.json"
            fields = ["robust_rank", "node_id", "name", "longitude", "latitude", "terrain_elevation_m", "nearby_smp_site_count", "nearby_broadcast_site_count", "nearby_radio_link_endpoint_count"]
            rows = [{"robust_rank": str(index), "node_id": f"n{index}", "name": f"N{index}", "longitude": "-45", "latitude": "-15", "terrain_elevation_m": "1100", "nearby_smp_site_count": "500", "nearby_broadcast_site_count": "0", "nearby_radio_link_endpoint_count": "0"} for index in range(1, 5)]
            with gzip.open(ranking, "wt", encoding="utf-8", newline="") as stream:
                writer = csv.DictWriter(stream, fieldnames=fields); writer.writeheader(); writer.writerows(rows)
            result = build(ranking, output)
            self.assertEqual([site["node_id"] for site in result["selected_sites"]], ["n1", "n2", "n3"])
            self.assertEqual(json.loads(output.read_text(encoding="utf-8"))["selected_sites"][0]["robust_rank"], 1)
