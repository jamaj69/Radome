import unittest
from collections import Counter

from build_municipal_emitter_network import dominant_code


class MunicipalEmitterNetworkTest(unittest.TestCase):
    def test_dominant_code_marks_conflict(self):
        code, conflict = dominant_code(Counter({"3550308": 10, "3548708": 1}))
        self.assertEqual(code, "3550308")
        self.assertTrue(conflict)

    def test_empty_code_is_reported(self):
        self.assertEqual(dominant_code(Counter()), (None, False))


if __name__ == "__main__":
    unittest.main()
