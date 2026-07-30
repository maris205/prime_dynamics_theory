import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def test_frontier_review_archive_boundaries():
    payload = json.loads((ROOT / "results/frontier_review.json").read_text())
    assert payload["paper_numbers"] == list(range(262, 272))
    assert payload["audit_failure_count"] == 0
    assert payload["finite_review_records"] == 187
    assert payload["headline_metrics"]["parity_cross_check_orders"] == 27
    assert payload["headline_metrics"]["direct_order_29_log_tail_lt"] == "0.000026624745"
    assert payload["headline_metrics"]["finite_quotient_samples"] == 23
    assert payload["headline_metrics"]["missing_quotient_endpoints"] == 9
    assert payload["headline_metrics"]["envelope_constant"] == 48
    assert payload["headline_metrics"]["quotient_criterion_satisfied_required"] == [0, 4]
    assert payload["headline_metrics"]["ledger_satisfied_required"] == [2, 5]
    assert payload["finite_head_separation_witness"]["vanishing_moment_count"] == 28
    assert payload["finite_head_separation_witness"]["first_visible_order"] == 29
    assert payload["certificate_status"]["obligation_vector"] == [False, False, False, True, True]
    assert payload["complete_certificate_count"] == 0
    assert payload["macro_gates"] == {letter: False for letter in "ABCDE"}
    assert payload["theorem_boundary"]["hilbert_polya_operator"] is False
    assert payload["theorem_boundary"]["zeta_divisor_equality"] is False
    assert payload["theorem_boundary"]["riemann_hypothesis_implication"] is False
