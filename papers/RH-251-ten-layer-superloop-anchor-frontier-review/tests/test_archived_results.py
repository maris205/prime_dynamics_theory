import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def test_archived_ten_layer_review():
    payload = json.loads((ROOT / "results/frontier_review.json").read_text())
    assert payload["paper_numbers"] == list(range(242, 252))
    assert payload["audit_failure_count"] == 0
    assert payload["headline_metrics"]["rh244_prefix_passes"] == 0
    assert payload["headline_metrics"]["rh250_complete_gluing_certificates"] == 0
    assert payload["theorem_boundary"]["gate_A"] is False
    assert payload["macro_gates"] == {gate: False for gate in "ABCDE"}
