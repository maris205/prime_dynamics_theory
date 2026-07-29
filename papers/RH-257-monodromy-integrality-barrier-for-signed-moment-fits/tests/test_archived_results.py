import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def test_archived_signed_fit_barrier():
    payload = json.loads((ROOT / "results/signed_moment_audit.json").read_text())
    assert payload["endpoint_count"] == 32
    assert payload["signed_fit_pass_count"] == 32
    assert payload["integer_weight_fit_count"] == 0
    assert payload["maximum_signed_fit_distance"] < 0.004
    assert payload["minimum_fractional_weight_count"] > 0
    assert payload["theorem_boundary"]["integer_weights_are_necessary_for_single_valued_meromorphic_product"] is True
    assert payload["theorem_boundary"]["fractional_signed_fit_is_legal_determinant_quotient"] is False
    assert payload["theorem_boundary"]["gate_A"] is False
