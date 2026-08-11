import unittest

from audit_anatel_spectrum import emission_bandwidth_hz, positive_frequency


class EmissionBandwidthTest(unittest.TestCase):
    def test_decodes_itu_necessary_bandwidth_prefix(self):
        self.assertEqual(emission_bandwidth_hz("200KG7W"), 200_000)
        self.assertEqual(emission_bandwidth_hz("5M00G7W"), 5_000_000)
        self.assertEqual(emission_bandwidth_hz("10M0D7W"), 10_000_000)
        self.assertEqual(emission_bandwidth_hz("100MG7W"), 100_000_000)

    def test_rejects_missing_or_invalid_designation(self):
        self.assertIsNone(emission_bandwidth_hz(""))
        self.assertIsNone(emission_bandwidth_hz("INVALID"))

    def test_rejects_nonpositive_frequency_as_physical_spectrum(self):
        self.assertIsNone(positive_frequency(0.0))
        self.assertIsNone(positive_frequency(-1.0))
        self.assertEqual(positive_frequency(778.0), 778.0)


if __name__ == "__main__":
    unittest.main()
