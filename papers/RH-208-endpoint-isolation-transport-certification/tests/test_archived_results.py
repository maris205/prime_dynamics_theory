import json
from pathlib import Path
R=Path(__file__).resolve().parents[1]
def test_archived_feasibility_split():
 p=json.loads((R/"results/transport_certification_feasibility.json").read_text())
 assert p["endpoint_case_below_one_count"]==p["endpoint_case_count"]==6
 assert p["transport_case_below_one_count"]==0
 assert p["maximum_endpoint_isolation_ratio"]<1e-12
 assert p["minimum_transport_ratio"]>3.3 and p["maximum_transport_ratio"]>29
 assert not p["theorem_boundary"]["validated_riesz_projector"]
