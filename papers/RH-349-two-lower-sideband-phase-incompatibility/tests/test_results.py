import json
from pathlib import Path

from experiments.build_result import result_payload


ROOT = Path(__file__).resolve().parents[1]


def _result():
    return json.loads((ROOT / "results/result.json").read_text(encoding="utf-8"))


def test_result_file_is_deterministic_and_schema_is_strict():
    data = _result()
    assert data == result_payload()
    assert set(data) == {
        "coefficient_identity",
        "conditional_conclusion",
        "constants",
        "false_claims",
        "finite_fixture",
        "finite_rows",
        "finite_rows_are_reproduction_checks_only",
        "fixed_phase_law",
        "gates",
        "index_family",
        "minimax_theorems",
        "route_boundary",
        "scope",
        "source_anchors",
        "status",
        "verdict",
    }


def test_index_family_is_exactly_the_two_fixed_lower_sidebands():
    index = _result()["index_family"]
    assert index["sidebands"].endswith("{2,3}")
    assert index["both_orders_are_punctured_lower_even"] is True


def test_coefficient_identity_preserves_actual_remainder_and_direct_type():
    identity = _result()["coefficient_identity"]
    assert identity["direct"].startswith("p_j=")
    assert "-d_" in identity["actual_remainder"]
    assert identity["demand"].startswith("S_j=")


def test_both_actual_hypotheses_are_named_and_unproved():
    law = _result()["fixed_phase_law"]
    assert law["actual_hypotheses"] == [
        "Y_2=o(H_(m_2))",
        "Y_3=o(H_(m_3))",
    ]
    assert law["hypotheses_proved"] is False


def test_both_minimax_identities_are_recorded_with_distinct_optimizers():
    theorems = _result()["minimax_theorems"]
    assert theorems["relative_optimizer"] == "2lambda/(lambda+1)"
    assert theorems["weighted_optimizer"] == "1"
    assert theorems["weighted"].endswith("=1-1/lambda")


def test_conditional_conclusion_is_not_unconditional_prefix_nonclosure():
    conclusion = _result()["conditional_conclusion"]
    assert conclusion["diverges_exponentially_under_both_actual_hypotheses"] is True
    assert conclusion["bounded_phase_liminf"].startswith(">=")
    assert conclusion["unconditional_conclusion"] is False


def test_finite_rows_are_formula_reproduction_only():
    data = _result()
    assert len(data["finite_rows"]) == 4
    assert data["finite_rows_are_reproduction_checks_only"] is True
    assert data["finite_fixture"]["remainder"].startswith("Y_2=Y_3=0")


def test_claim_firewall_and_gates_remain_false():
    data = _result()
    assert len(data["false_claims"]) == 20
    assert not any(data["false_claims"].values())
    assert set(data["gates"]) == set("ABCDE")
    assert not any(data["gates"].values())


def test_route_moves_only_to_a_uniformity_audit():
    route = _result()["route_boundary"]
    assert route["fixed_two_sideband_law"].startswith("PROVED_conditional")
    assert route["actual_remainder_control"].startswith("NOT_TESTABLE")
    assert route["full_E_off"].startswith("NOT_TESTABLE")
    assert route["next_route"].startswith("RH-350")
