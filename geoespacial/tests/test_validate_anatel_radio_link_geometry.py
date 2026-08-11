import tempfile,unittest
from pathlib import Path
from build_canonical_smp import deterministic_gzip_csv
from validate_anatel_radio_link_geometry import validate
class GeometryTest(unittest.TestCase):
 def test_aligned_reciprocal_candidate_remains_unpaired(self):
  with tempfile.TemporaryDirectory() as d:
   r=Path(d);c=r/"c.gz";k=r/"k.gz";e=r/"e.gz"
   with deterministic_gzip_csv(c,("candidate_id","link_family","service_fistel","rf_act_number","status","coordinate_a","coordinate_b","distance_km","reciprocal_frequency_count")) as w:w.writerow({"candidate_id":"x","link_family":"scm","service_fistel":"1","rf_act_number":"2","status":"two_coordinate_reciprocal","coordinate_a":"0,0","coordinate_b":"0,1","distance_km":"111","reciprocal_frequency_count":"1"})
   with deterministic_gzip_csv(k,("link_family","service_fistel","rf_act_number","source_row_number")) as w:w.writerow({"link_family":"scm","service_fistel":"1","rf_act_number":"2","source_row_number":"1"});w.writerow({"link_family":"scm","service_fistel":"1","rf_act_number":"2","source_row_number":"2"})
   with deterministic_gzip_csv(e,("source_row_number","latitude","longitude","frequency_mhz","direction","azimuth_deg")) as w:w.writerow({"source_row_number":"1","latitude":"0","longitude":"0","frequency_mhz":"100","direction":"Transmissão","azimuth_deg":"90"});w.writerow({"source_row_number":"2","latitude":"0","longitude":"1","frequency_mhz":"100","direction":"Recepção","azimuth_deg":"270"})
   x=validate(c,k,e,r/"o.gz",r/"r.json");self.assertEqual(x["status"],{"azimuth_consistent_15deg":1});self.assertEqual(x["pairing_status"],"not_performed")
if __name__=="__main__":unittest.main()
