import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def test_archived_quotient_audit():
    payload = json.loads((ROOT / "results/orthogonal_quotient_audit.json").read_text())
    assert payload["eligible_endpoint_count"] == 17
    assert payload["rank_mismatch_count"] == 0
    assert payload["maximum_schur_partition_error_orders_2_to_12"] < 1e-12
    assert payload["maximum_archived_residual_error_orders_2_to_12"] < 1e-10
    assert payload["one_step_contractive_count"] == 0
    assert payload["minimum_first_contractive_power_depth"] >= 3
    boundary = payload["theorem_boundary"]
    assert boundary["orthogonal_quotient_trace_identity_fixed_noise"] is True
    assert boundary["uniform_selected_subspace_stability"] is False
    assert boundary["gate_A"] is False
