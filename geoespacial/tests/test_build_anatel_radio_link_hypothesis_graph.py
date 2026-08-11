import unittest
from build_anatel_radio_link_hypothesis_graph import build_graph, component_summary, node_id


class RadioLinkHypothesisGraphTest(unittest.TestCase):
    def test_preserves_parallel_frequency_hypotheses_and_nonoperational_state(self):
        base = {
            "candidate_id": "candidate:1", "link_family": "scm", "service_fistel": "1",
            "rf_act_number": "2", "source_coordinate": "-10,-40",
            "destination_coordinate": "-11,-41", "prequalification_status_k1": "cadastral_prequalified",
            "prequalification_status_k4_3": "cadastral_prequalified", "maximum_two_end_azimuth_error_deg": "0.2",
        }
        rows = [dict(base, path_id=f"path:{index}", frequency_mhz=str(frequency)) for index, frequency in enumerate((6000, 7000), 1)]
        terrain = {row["path_id"]: {"distance_km": "10", "source_height_m": "20", "destination_height_m": "30", "minimum_fresnel60_clearance_k1_m": "1", "minimum_fresnel60_clearance_k4_3_m": "2"} for row in rows}
        vertical = {row["path_id"]: {"maximum_two_end_error_k1_deg": "0.1", "maximum_two_end_error_k4_3_deg": "0.1"} for row in rows}

        graph = build_graph(rows, terrain, vertical)

        self.assertEqual(graph.number_of_nodes(), 2)
        self.assertEqual(graph.number_of_edges(), 2)
        self.assertTrue(all(not data["operational_edge"] for _, _, data in graph.edges(data=True)))
        self.assertEqual(component_summary(graph, "prequalified_k1")["component_count"], 1)

    def test_node_identity_is_coordinate_stable(self):
        self.assertEqual(node_id("-10,-40"), node_id("-10.000000,-40.000000"))


if __name__ == "__main__":
    unittest.main()
