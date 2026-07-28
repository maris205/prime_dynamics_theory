import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def test_archived_zonotope_obstruction():
    payload = json.loads((ROOT / "results/zonotope_audit.json").read_text())
    assert payload["endpoint_count"] == 32
    assert payload["total_eligible_prefix_count"] == 543
    assert payload["total_eligible_contiguous_interval_count"] == 5012
    assert payload["total_eligible_binary_subset_count"] == 139572890
    assert payload["prefix_pass_count"] == 0
    assert payload["binary_subset_pass_count"] == 0
    assert payload["box_zonotope_pass_count"] == 0
    assert payload["maximum_box_primal_dual_gap"] < 1e-10
    boundary = payload["theorem_boundary"]
    assert boundary["expanded_candidate_windows_excluded"] is False
    assert boundary["gate_A"] is False
