import unittest
import urllib.parse

from acquire_decea_wfs import request_url


class DeceaAcquisitionTest(unittest.TestCase):
    def test_encodes_layer_and_output_format(self):
        url = request_url("GetFeature", typeNames="ICA:vor", outputFormat="application/json")
        query = urllib.parse.parse_qs(urllib.parse.urlparse(url).query)
        self.assertEqual(query["request"], ["GetFeature"])
        self.assertEqual(query["typeNames"], ["ICA:vor"])
        self.assertEqual(query["outputFormat"], ["application/json"])


if __name__ == "__main__":
    unittest.main()
