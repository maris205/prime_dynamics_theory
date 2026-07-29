import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def test_frontier_review_archive_boundaries():
    payload = json.loads((ROOT / "results/frontier_review.json").read_text())
    assert payload["paper_numbers"] == list(range(252, 262))
    assert payload["audit_failure_count"] == 0
    assert payload["finite_review_records"] == 842
    assert payload["headline_metrics"]["rh254_complete_incomplete"] == [21, 11]
    assert payload["headline_metrics"]["rh255_box_passes"] == 0
    assert payload["headline_metrics"]["rh257_signed_fit_passes"] == 32
    assert payload["headline_metrics"]["rh257_integer_fit_passes"] == 0
    assert payload["headline_metrics"]["rh258_unit_cap_passes"] == 0
    assert payload["headline_metrics"]["rh259_endpoint_count"] == 23
    assert payload["headline_metrics"]["rh260_complete_certificates"] == 0
    assert payload["macro_gates"] == {letter: False for letter in "ABCDE"}
    assert payload["theorem_boundary"]["hilbert_polya_operator"] is False
    assert payload["theorem_boundary"]["zeta_divisor_identification"] is False
    assert payload["theorem_boundary"]["riemann_hypothesis_implication"] is False
