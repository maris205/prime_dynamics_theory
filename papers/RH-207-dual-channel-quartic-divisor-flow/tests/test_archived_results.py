import json
from pathlib import Path
R=Path(__file__).resolve().parents[1]
def test_archived_quartic_flow():
 p=json.loads((R/"results/quartic_divisor_flow.json").read_text())
 assert p["newton_identity_case_count"]==120 and p["newton_identity_failure_count"]==0
 assert p["maximum_left_right_coefficient_relative_error"]<0.009
 assert p["maximum_adjacent_scale_coefficient_relative_error"]>0.31
 assert p["finest_left_right_constant_term_relative_error"]<0.008
 assert not p["theorem_boundary"]["coefficient_limit_exists"]
