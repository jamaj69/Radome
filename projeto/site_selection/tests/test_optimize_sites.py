import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from optimize_sites import Candidate, solve


def candidate(candidate_id, covers, peers=(), exempt=False, score=0.0):
    return Candidate(candidate_id, frozenset(covers), frozenset(peers), exempt, score)


class OptimizeSitesTest(unittest.TestCase):
    def test_minimum_pair_and_independent_island(self):
        candidates = [
            candidate("ridge-a", {"west", "centre"}, {"ridge-b"}, score=2),
            candidate("ridge-b", {"centre", "east"}, {"ridge-a"}, score=2),
            candidate("ridge-c", {"east"}, set(), score=10),
            candidate("island", {"oceanic"}, exempt=True, score=1),
        ]
        result = solve(candidates, {"west", "centre", "east", "oceanic"})
        self.assertEqual(result["site_count"], 3)
        self.assertEqual(set(result["selected_ids"]), {"ridge-a", "ridge-b", "island"})
        self.assertEqual(result["coverage_fraction"], 1.0)

    def test_non_exempt_isolated_candidate_cannot_be_selected(self):
        candidates = [
            candidate("isolated", {"north"}),
            candidate("paired-a", {"north"}, {"paired-b"}),
            candidate("paired-b", {"south"}, {"paired-a"}),
        ]
        result = solve(candidates, {"north", "south"})
        self.assertEqual(set(result["selected_ids"]), {"paired-a", "paired-b"})

    def test_uncoverable_cell_is_reported(self):
        with self.assertRaisesRegex(ValueError, "no candidate coverage"):
            solve([candidate("island", {"known"}, exempt=True)], {"known", "missing"})


if __name__ == "__main__":
    unittest.main()
