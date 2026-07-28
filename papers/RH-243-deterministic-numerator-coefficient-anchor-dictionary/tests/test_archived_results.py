import json
from pathlib import Path


def test_archived_coefficient_anchor_dictionary():
    payload = json.loads(
        (Path(__file__).parents[1] / "results/coefficient_anchor_audit.json").read_text()
    )
    assert payload["maximum_one_step_order"] == 12
    assert payload["symmetric_jet_identity_error"] < 1.0e-14
    assert 0.49 < payload["one_step_target_unit_disk_log_jet_norm_orders_2_to_12"] < 0.50
    assert payload["minimum_archived_anchored_jet_distance"] > 0.4
    boundary = payload["theorem_boundary"]
    assert boundary["deterministic_one_step_trace_style_anchor_target_defined"]
    assert not boundary["two_step_anchor_identifies_odd_one_step_coefficients"]
    assert not boundary["current_cloud_coefficient_bridge"]
    assert not boundary["gate_A"]
