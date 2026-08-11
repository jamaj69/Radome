import unittest

import networkx as nx

from build_unified_geospatial_graph import add_candidate_layer, add_membership_layer


class UnifiedGeospatialGraphTest(unittest.TestCase):
    def test_membership_is_oriented_toward_municipality(self):
        source = nx.Graph()
        source.add_node("municipio:1", kind="municipio")
        source.add_node("tower:1", kind="torre_smp")
        source.add_edge("municipio:1", "tower:1", relation="located_in")
        target = nx.MultiDiGraph()
        add_membership_layer(target, source, "smp_municipal", [])
        self.assertTrue(target.has_edge("tower:1", "municipio:1"))
        self.assertTrue(all(not data["operational_edge"] for _, _, data in target.edges(data=True)))

    def test_undirected_candidate_edge_becomes_two_nonoperational_arcs(self):
        source = nx.Graph()
        source.add_node("a", kind="capital")
        source.add_node("b", kind="airport")
        source.add_edge("a", "b")
        target = nx.MultiDiGraph()
        logical = add_candidate_layer(target, source, [])
        self.assertEqual(logical, 1)
        self.assertTrue(target.has_edge("a", "b"))
        self.assertTrue(target.has_edge("b", "a"))
        self.assertTrue(all(not data["terrain_confirmation"] for _, _, data in target.edges(data=True)))


if __name__ == "__main__":
    unittest.main()
