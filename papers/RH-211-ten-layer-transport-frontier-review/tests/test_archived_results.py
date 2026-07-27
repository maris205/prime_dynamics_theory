import json
from pathlib import Path
R=Path(__file__).resolve().parents[1]
def test_archived_review_coordinate_and_gates():
 p=json.loads((R/"results/transport_frontier_review.json").read_text())
 assert p["route_coordinate"]=="finite_dual_channel_divisor_flow_open_renormalization"
 assert p["aggregate_finite_item_count"]==649
 assert p["aggregate_identity_failure_count"]==0
 assert all(p["statuses"][k] for k in ("naive_haar_transport_rejected","branch_correspondence_supported","dual_channel_divisor_supported","expanded_cloud_rejected"))
 assert not any(p["macro_gates"].values())
 assert p["next_target"]["paper"]=="RH-212"
