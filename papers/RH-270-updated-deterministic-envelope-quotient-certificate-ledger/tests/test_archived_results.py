import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def test_archived_updated_certificate_ledger():
    payload = json.loads(
        (ROOT / "results/updated_certificate_ledger.json").read_text(
            encoding="utf-8"
        )
    )
    target = payload["deterministic_target"]
    assert target["unified_envelope"]["constant"] == 48
    assert target["parity_anchor"]["all_order_exact"] is True
    assert target["direct_order_29_tail"]["logarithmic_lt"] == "0.000026624745"
    assert target["sharp_law"]["smaller_geometric_base_possible"] is False
    assert target["cross_source_comparison"]["upper_endpoint_improvement_factor"] > 6.93

    quotient = payload["quotient_and_cloud"]
    assert quotient["finite_sample_count"] == 23
    assert quotient["missing_archived_endpoint_count"] == 9
    assert quotient["criterion"]["satisfied_hypothesis_count"] == 0
    assert quotient["criterion"]["required_hypothesis_count"] == 4
    assert quotient["uniform_quotient_tail"] is False

    status = payload["certificate_status"]
    assert status["obligation_vector"] == [False, False, False, True, True]
    assert status["satisfied_component_count"] == 2
    assert status["complete"] is False
    assert payload["complete_certificate_count"] == 0
    assert payload["source_consistency_audit"]["check_count"] >= 90
    assert payload["source_consistency_audit"]["failure_count"] == 0
    assert all(
        payload["theorem_boundary"][f"gate_{letter}"] is False
        for letter in "ABCDE"
    )
