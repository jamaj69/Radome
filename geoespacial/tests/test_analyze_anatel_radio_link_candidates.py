import tempfile,unittest
from pathlib import Path
from analyze_anatel_radio_link_candidates import analyze
from build_canonical_smp import deterministic_gzip_csv
from extract_anatel_radio_link_keys import FIELDS
class CandidateTest(unittest.TestCase):
 def test_reciprocal_two_coordinate_group(self):
  with tempfile.TemporaryDirectory() as d:
   r=Path(d); src=r/"s.gz"
   with deterministic_gzip_csv(src,FIELDS) as w:
    w.writerow({"link_family":"scm","service_fistel":"1","rf_act_number":"2","station_number":"A","latitude":"-10","longitude":"-40","direction":"Transmissão","frequency_mhz":"100"})
    w.writerow({"link_family":"scm","service_fistel":"1","rf_act_number":"2","station_number":"B","latitude":"-11","longitude":"-41","direction":"Recepção","frequency_mhz":"100"})
   x=analyze(src,r/"o.gz",r/"r.json");self.assertEqual(x["partition"],[*x["partition"]] and {"two_coordinate_reciprocal":1});self.assertEqual(x["pairing_status"],"not_performed")
if __name__=="__main__":unittest.main()
