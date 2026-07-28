import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def test_archived_cone_pathology():
    payload = json.loads((ROOT / "results/cone_reachability_audit.json").read_text())
    assert payload["endpoint_count"] == 32
    assert payload["cone_pass_count"] == 26
    assert payload["cone_failure_count"] == 6
    assert payload["cap_40_pass_count"] == 0
    assert payload["cap_41_pass_count"] == 1
    assert payload["minimum_required_weight_cap_among_passing_endpoints"] > 40.0
    assert payload["maximum_required_weight_cap_among_passing_endpoints"] > 1e9
    boundary = payload["theorem_boundary"]
    assert boundary["unbounded_real_weights_are_legal_spectral_multiplicities"] is False
    assert boundary["gate_A"] is False
