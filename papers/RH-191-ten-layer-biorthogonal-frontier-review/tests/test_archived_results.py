import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def test_archived_frontier_review():
    payload = json.loads((ROOT / "results/biorthogonal_frontier_review.json").read_text())
    assert payload["paper_numbers"] == list(range(182, 191))
    assert payload["orthogonal_clock_three_gate_success_count"] == 0
    assert payload["local_biorthogonal_gate_count"] > 0
    assert payload["norm_only_resolvent_success_count"] == 0
    assert not payload["macro_boundary"]["gate_A"]
