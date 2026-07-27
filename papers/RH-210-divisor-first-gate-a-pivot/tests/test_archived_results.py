import json
from pathlib import Path
R=Path(__file__).resolve().parents[1]
def test_archived_divisor_first_pivot():
 p=json.loads((R/"results/divisor_first_route_audit.json").read_text())
 assert p["route_coordinate"]=="finite_dual_channel_divisor_flow_open_renormalization"
 assert p["maximum_counterexample_projector_distance"]>0.999
 assert p["maximum_counterexample_coefficient_error"]<1e-12
 assert all(p["statuses"][k] for k in ("finite_branch_correspondence","finite_dual_channel_divisor","naive_state_transport_rejected","scalar_residue_renormalization_rejected"))
 assert not p["theorem_boundary"]["gate_A"]
