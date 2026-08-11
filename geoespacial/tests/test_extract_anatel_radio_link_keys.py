import csv, gzip, io, tempfile, unittest
from pathlib import Path
from zipfile import ZipFile
from build_canonical_smp import deterministic_gzip_csv
from extract_anatel_radio_link_keys import MEMBER, extract
from extract_anatel_radio_links import FIELDS

class RawLinkKeysTest(unittest.TestCase):
    def test_recovers_keys_and_confirms_row_equivalence(self):
        with tempfile.TemporaryDirectory() as directory:
            root=Path(directory); archive=root/"source.zip"; normalized=root/"normalized.gz"
            raw_fields=["Número da Estação","Serviço","Código e Nome do Serviço","Origem","Status da Validade da Estação","Tipo Classe Estação","Direção de Comunicação","Frequência (MHz)","Latitude (graus)","Longitude (graus)","Código IBGE do Município","Fistel do Serviço da Estação","Número do Ato de RF"]
            buffer=io.StringIO(newline=""); writer=csv.DictWriter(buffer,fieldnames=raw_fields,delimiter=";",lineterminator="\n"); writer.writeheader(); writer.writerow({"Número da Estação":"1","Serviço":"Telefonia Móvel - Radioenlace","Direção de Comunicação":"Transmissão","Frequência (MHz)":"100,5","Latitude (graus)":"-10","Longitude (graus)":"-40","Fistel do Serviço da Estação":"9","Número do Ato de RF":"8"})
            with ZipFile(archive,"w") as z: z.writestr(MEMBER,buffer.getvalue().encode("utf-8-sig"))
            with deterministic_gzip_csv(normalized,FIELDS) as out: out.writerow({"link_family":"smp","source_row_number":1,"station_number":"1","service":"Telefonia Móvel - Radioenlace","direction":"Transmissão","frequency_mhz":"100.5","latitude":"-10","longitude":"-40"})
            result=extract(archive,normalized,root/"out.gz",root/"report.json")
            self.assertTrue(result["row_equivalence_confirmed"]); self.assertEqual(result["key_availability"]["service_fistel"],1); self.assertEqual(result["pairing_status"],"not_performed")

if __name__ == "__main__": unittest.main()
