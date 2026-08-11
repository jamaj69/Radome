import csv
import gzip
import json
import tempfile
import unittest
from pathlib import Path

import networkx as nx

from analyze_augmented_mesh_resilience import build, component_metrics


class AnalyzeAugmentedMeshResilienceTests(unittest.TestCase):
    def test_component_and_articulation_metrics(self):
        graph = nx.Graph([(1, 2), (2, 3)]); graph.add_node(4)
        metrics = component_metrics(graph)
        self.assertEqual(metrics["component_count"], 2)
        self.assertEqual(metrics["largest_component_node_count"], 3)
        self.assertEqual(metrics["isolated_node_count"], 1)
        self.assertEqual(metrics["articulation_vertex_count"], 1)

    def write_gzip_csv(self, path: Path, fields: list[str], rows: list[dict]) -> None:
        with gzip.open(path, "wt", encoding="utf-8", newline="") as output:
            writer = csv.DictWriter(output, fieldnames=fields)
            writer.writeheader(); writer.writerows(rows)

    def test_build_validates_mesh_and_disk_provenance(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            faces = root / "faces.csv.gz"; profiles = root / "profiles.csv.gz"
            disk = root / "disk.json"; output = root / "sensitivity.csv.gz"; report = root / "summary.json"
            self.write_gzip_csv(faces, ["face_id", "vertex_ids", "continental_grid_cell_count", "continental_grid_area_km2", "terrain_face_status_k1", "terrain_face_status_k4_3"], [{"face_id": "f1", "vertex_ids": "a|b|c", "continental_grid_cell_count": "2", "continental_grid_area_km2": "4.0", "terrain_face_status_k1": "triangle_k3_terrain_los", "terrain_face_status_k4_3": "triangle_k3_terrain_los"}])
            profile_rows = [{"edge_id": edge, "left_id": left, "right_id": right, "terrain_status_k1": "los_clear", "terrain_status_k4_3": "los_clear"} for edge, left, right in (("ab", "a", "b"), ("bc", "b", "c"), ("ca", "c", "a"))]
            self.write_gzip_csv(profiles, list(profile_rows[0]), profile_rows)
            disk.write_text(json.dumps({"candidate_count": 3, "cell_count": 3, "covered_cell_count": 3}), encoding="utf-8")
            result = build(faces, profiles, disk, output, report)
            self.assertEqual(result["models"]["k1"]["assigned_grid_cell_count"], 2)
            self.assertTrue(output.exists())
            disk.write_text(json.dumps({"candidate_count": 4, "cell_count": 3, "covered_cell_count": 3}), encoding="utf-8")
            with self.assertRaisesRegex(ValueError, "candidate_count"):
                build(faces, profiles, disk, output, report)


if __name__ == "__main__": unittest.main()
