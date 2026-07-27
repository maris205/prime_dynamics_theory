import json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
def test_archived_procrustes_audit():
 p=json.loads((ROOT/"results/procrustes_shell_audit.json").read_text())
 assert p["identity_case_count"]==80 and p["identity_failure_count"]==0
 assert p["maximum_identity_error"]<1e-12
 assert p["maximum_right_rank_normalized_procrustes_residual"]>0.69
 assert p["maximum_left_rank_normalized_procrustes_residual"]>0.70
 assert p["theorem_boundary"]["exact_endpoint_packet_map"]
 assert not p["theorem_boundary"]["predictive_interlevel_transport"]
