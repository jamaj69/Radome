import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from audit_anatel_radio_link_heights import classify_heights


class AuditRadioLinkHeightsTest(unittest.TestCase):
    def test_unambiguous_requires_one_value_at_each_endpoint(self):
        self.assertEqual(classify_heights(["20.0"], ["30.0"]), "unambiguous_cadastral_height")

    def test_missing_endpoint_fails_closed(self):
        self.assertEqual(classify_heights([], ["30.0"]), "missing_height")

    def test_multiple_values_remain_ambiguous(self):
        self.assertEqual(classify_heights(["20.0", "25.0"], ["30.0"]), "ambiguous_cadastral_height")


if __name__ == "__main__":
    unittest.main()
