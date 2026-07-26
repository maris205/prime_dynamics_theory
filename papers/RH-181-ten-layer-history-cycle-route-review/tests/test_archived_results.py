import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def test_review_archive():
    payload = json.loads((ROOT / "results/history_cycle_review.json").read_text())
    assert payload["aggregate_finite_case_count"] == 2600
    assert payload["formula_or_rank_failure_count"] == 0
    assert payload["history_snapshot_count"] == 130
    assert payload["history_two_sided_threshold_success_count"] == 0
    assert payload["cycle_shell_case_count"] == 1248
    assert payload["current_route_status"] == "open"
    assert not payload["macro_boundary"]["gate_A"]
