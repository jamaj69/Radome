import tempfile
import unittest
from pathlib import Path
from zipfile import ZipFile

from inventory_smp import inventory


class SmpInventoryTest(unittest.TestCase):
    def test_collapses_repeated_records_at_same_coordinate(self):
        header = (
            "Número Estação;Latitude decimal;Longitude decimal;Situacao;Tecnologia;"
            "Geração;Empresa Estação;Entidade;UF\n"
        )
        rows = (
            "10;-23.100001;-46.200001;Licenciada;LTE;4G;A;;SP\n"
            "10;-23.100002;-46.200002;Licenciada;NR;5G;A;;SP\n"
            "20;-22;-45;Licenciada;GSM;2G;B;;MG\n"
        )
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "smp.zip"
            with ZipFile(path, "w") as archive:
                archive.writestr("Estacoes_SMP.csv", header + rows)
            result = inventory(path, coordinate_decimals=5)
        self.assertEqual(result["record_count"], 3)
        self.assertEqual(result["approximate_physical_site_count"], 2)
        self.assertEqual(result["unique_station_number_count"], 2)
        self.assertEqual(result["valid_coordinate_record_count"], 3)


if __name__ == "__main__":
    unittest.main()
