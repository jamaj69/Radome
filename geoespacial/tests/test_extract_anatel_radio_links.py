import csv
import gzip
import tempfile
import unittest
from pathlib import Path

from build_canonical_smp import deterministic_gzip_csv
from extract_anatel_radio_links import FIELDS, extract


class RadioLinkExtractionTest(unittest.TestCase):
    def test_extracts_only_explicit_families_without_pairing(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            source = root / "source.csv.gz"
            source_fields = tuple(field for field in FIELDS if field != "link_family")
            with deterministic_gzip_csv(source, source_fields) as writer:
                for service, station, direction in (
                    ("Telefonia Fixa - Radioenlace", "1", "Transmissão"),
                    ("Telefonia Fixa - Radioenlace", "1", "Recepção"),
                    ("Banda Larga Fixa - Radioenlace", "2", "Transmissão"),
                    ("Limitado Privado", "3", "Transmissão"),
                ):
                    writer.writerow({"service": service, "station_number": station, "direction": direction, "latitude": "-10", "longitude": "-40"})
            first = extract(source, root / "first.csv.gz", root / "first.json")
            second = extract(source, root / "second.csv.gz", root / "second.json")
            self.assertEqual(first["records"], 3)
            self.assertEqual(first["families"]["stfc"]["station_numbers_with_tx_and_rx"], 1)
            self.assertEqual(first["pairing_status"], "not_performed")
            self.assertEqual((root / "first.csv.gz").read_bytes(), (root / "second.csv.gz").read_bytes())
            with gzip.open(root / "first.csv.gz", "rt", encoding="utf-8") as stream:
                self.assertEqual(sum(1 for _ in csv.DictReader(stream)), 3)


if __name__ == "__main__":
    unittest.main()
