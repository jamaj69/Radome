import unittest

from rank_candidate_sites import SCENARIOS, normalize, ranks


class RankCandidateSitesTests(unittest.TestCase):
    def test_normalize_range_and_constant(self):
        self.assertEqual(normalize([2.0, 4.0, 6.0]), [0.0, 0.5, 1.0])
        self.assertEqual(normalize([3.0, 3.0]), [0.0, 0.0])

    def test_rank_tie_break_is_stable(self):
        rows = [{"node_id": "b", "score_test": 1.0}, {"node_id": "a", "score_test": 1.0}]
        ranks(rows, "score_test")
        self.assertEqual({row["node_id"]: row["rank_test"] for row in rows}, {"a": 1, "b": 2})

    def test_scenario_weights_sum_to_one(self):
        for weights in SCENARIOS.values():
            self.assertAlmostEqual(sum(weights.values()), 1.0)


if __name__ == "__main__":
    unittest.main()
