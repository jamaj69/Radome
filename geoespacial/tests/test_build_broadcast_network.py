import unittest

from build_broadcast_network import normalize_name


class BroadcastNetworkTest(unittest.TestCase):
    def test_normalizes_accents_apostrophes_and_hyphens(self):
        self.assertEqual(normalize_name("Alta Floresta D'Oeste"), "alta floresta d oeste")
        self.assertEqual(normalize_name("São-João"), "sao joao")


if __name__ == "__main__":
    unittest.main()
