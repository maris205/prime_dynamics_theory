import json
from pathlib import Path
R=Path(__file__).resolve().parents[1]
def test_archived_cloud_obstruction():
 p=json.loads((R/"results/expanding_cloud_audit.json").read_text())
 assert p["rank_case_count"]==32
 assert p["two_sided_green_rank_case_count"]==0
 assert p["expanded_two_sided_green_count"]==0
 assert p["minimum_joint_maximum_principal_sine"]>0.69
 assert p["maximum_expanded_joint_maximum_principal_sine"]>0.999999
 assert not p["theorem_boundary"]["all_level_cloud_obstruction"]
