import unittest

from inventory_decea_navaids import present


class DeceaNavaidInventoryTest(unittest.TestCase):
    def test_zero_is_a_present_numeric_value(self):
        self.assertTrue(present(0))

    def test_null_and_empty_are_absent(self):
        self.assertFalse(present(None))
        self.assertFalse(present(""))


if __name__ == "__main__":
    unittest.main()
