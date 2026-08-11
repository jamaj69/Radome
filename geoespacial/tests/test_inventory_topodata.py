import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from inventory_topodata import parse_index


class InventoryTopodataTest(unittest.TestCase):
    def test_selects_only_numeric_altitude_archives(self):
        html = """
        <a href="22S465ZN.zip">22S465ZN.zip</a><td align="right"> 61M</td>
        <a href="22S465SN.zip">22S465SN.zip</a><td align="right"> 66M</td>
        <a href="23S48_ZN.zip">23S48_ZN.zip</a><td align="right"> 512K</td>
        """
        result = parse_index(html)
        self.assertEqual([item["name"] for item in result], ["22S465ZN.zip", "23S48_ZN.zip"])
        self.assertEqual(result[0]["listed_size_bytes"], 61 * 1024**2)
        self.assertEqual(result[1]["listed_size_bytes"], 512 * 1024)


if __name__ == "__main__":
    unittest.main()
