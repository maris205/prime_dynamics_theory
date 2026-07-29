import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def test_archived_expanded_reachability_obstruction():
    payload = json.loads((ROOT / "results/expanded_reachability_audit.json").read_text())
    assert payload["endpoint_count"] == 32
    assert payload["box_zonotope_pass_count"] == 0
    assert payload["prefix_pass_count"] == 0
    assert payload["minimum_box_distance"] > 0.14
    assert payload["maximum_box_primal_dual_gap"] < 1e-10
    assert payload["total_eligible_binary_subset_count"] > 100_000_000
    assert payload["theorem_boundary"]["all_expanded_single_use_shell_subsets_excluded"] is True
    assert payload["theorem_boundary"]["signed_or_complex_selector_excluded"] is False
    assert payload["theorem_boundary"]["gate_A"] is False
