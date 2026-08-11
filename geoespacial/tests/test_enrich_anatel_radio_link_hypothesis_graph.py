import unittest
from collections import defaultdict

import networkx as nx

from enrich_anatel_radio_link_hypothesis_graph import apply_context


class EnrichRadioLinkHypothesisGraphTest(unittest.TestCase):
    def test_preserves_multiple_municipalities_and_adds_context_edges(self):
        graph = nx.MultiDiGraph()
        graph.add_node("endpoint:1", node_type="anatel_cadastral_endpoint")
        context = {"endpoint:1": defaultdict(set, {
            "ibge_codes": {"1", "2"}, "station_numbers": {"10"}, "entities": {"Entity"},
        })}
        municipalities = nx.Graph()
        municipalities.add_node("municipio:1", kind="municipio")
        municipalities.add_node("municipio:2", kind="municipio")

        result = apply_context(graph, context, municipalities)

        self.assertEqual(result["endpoint_municipality_conflict_count"], 1)
        self.assertEqual(result["municipality_membership_edge_count"], 2)
        self.assertEqual(graph.nodes["endpoint:1"]["ibge_codes"], "1|2")
        self.assertTrue(all(not data["operational_edge"] for _, _, data in graph.edges(data=True)))

    def test_missing_municipality_is_reported(self):
        graph = nx.MultiDiGraph()
        graph.add_node("endpoint:1", node_type="anatel_cadastral_endpoint")
        context = {"endpoint:1": defaultdict(set, {"ibge_codes": {"9"}})}
        result = apply_context(graph, context, nx.Graph())
        self.assertEqual(result["missing_municipality_codes"], ["9"])


if __name__ == "__main__":
    unittest.main()
