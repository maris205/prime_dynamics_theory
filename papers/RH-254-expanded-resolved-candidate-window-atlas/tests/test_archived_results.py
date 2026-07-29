import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def test_archived_expanded_window():
    payload = json.loads((ROOT / "results/expanded_window_atlas.json").read_text())
    assert payload["endpoint_count"] == 32
    assert payload["expanded_candidate_margin"] == 32
    assert payload["minimum_expanded_candidate_rank"] > payload["minimum_reference_candidate_rank"]
    assert payload["maximum_matching_error"] < 1e-7
    assert payload["expanded_shell_complete_endpoint_count"] == 21
    assert payload["expanded_shell_incomplete_endpoint_count"] == 11
    assert payload["maximum_discarded_incomplete_expanded_root_count"] == 1
    assert payload["theorem_boundary"]["expanded_window_finite"] is True
    assert payload["theorem_boundary"]["anchored_reachability_completed"] is False
    assert payload["theorem_boundary"]["gate_A"] is False
