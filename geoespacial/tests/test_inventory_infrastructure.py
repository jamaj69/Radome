import tempfile
import unittest
from pathlib import Path
from zipfile import ZipFile

from inventory_infrastructure import read_anac_csv, read_anatel_zip, read_decea_capabilities


class InfrastructureInventoryTest(unittest.TestCase):
    def test_reads_anac_preamble_and_records(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "airports.csv"
            path.write_bytes("Atualizado em: 2026-08-01\r\nNome;UF\r\nA;SP\r\n".encode("latin-1"))
            result = read_anac_csv(path)
        self.assertEqual(result["record_count"], 1)
        self.assertEqual(result["columns"], ["Nome", "UF"])
        self.assertEqual(result["source_timestamp"], "Atualizado em: 2026-08-01")

    def test_anatel_zip_does_not_infer_smp_from_columns(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "stations.zip"
            with ZipFile(path, "w") as archive:
                archive.writestr("Estacoes_Gerais.csv", "Serviço;Latitude;Longitude\nSMP;-1;-2\n")
            result = read_anatel_zip(path)
        self.assertFalse(result["contains_dedicated_smp_resource"])
        self.assertEqual(result["members"][0]["columns"], ["Serviço", "Latitude", "Longitude"])

    def test_selects_relevant_decea_layers(self):
        xml = """<WFS_Capabilities xmlns:wfs="http://www.opengis.net/wfs/2.0">
        <wfs:FeatureTypeList><wfs:FeatureType><wfs:Name>ICA:airport</wfs:Name>
        <wfs:Title>Aeródromos</wfs:Title></wfs:FeatureType></wfs:FeatureTypeList>
        </WFS_Capabilities>"""
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "capabilities.xml"
            path.write_text(xml, encoding="utf-8")
            result = read_decea_capabilities(path)
        self.assertEqual(result["feature_type_count"], 1)
        self.assertEqual(result["selected_layers"][0]["name"], "ICA:airport")
        self.assertIn("ICA:heliport", result["missing_expected_layers"])


if __name__ == "__main__":
    unittest.main()
