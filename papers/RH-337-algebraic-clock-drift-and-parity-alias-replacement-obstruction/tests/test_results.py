import json
from pathlib import Path

from experiments.build_result import result_payload


ROOT = Path(__file__).resolve().parents[1]


def _result():
    return json.loads((ROOT / "results" / "result.json").read_text(encoding="utf-8"))


def test_result_file_is_deterministic():
    assert _result() == result_payload()


def test_exact_clock_certificate_and_model_type_are_locked():
    data = _result()
    certificate = data["exact_clock_certificate"]
    assert certificate["Lambda_hat_greater_than_lambda"] is True
    assert certificate["R_over_r_H_squared"] == "784/289"
    assert certificate["beta_R_greater_than_one_from_lambda_less_than_two"] is True
    assert certificate["polynomial_at_Lambda_hat"] == (
        "5765081705833725291502719395827/"
        "1953125000000000000000000000000000000000000000"
    )
    assert data["hatted_model_constants"]["status"] == (
        "RH329_model_definitions_not_physical_intervals"
    )
    assert "RH-327_target_relative_precision_barrier" in data["source_anchors"]
    assert "RH-334_physical_lambda_algebraic_identity" in data["source_anchors"]


def test_off_phase_trichotomy_does_not_reuse_bounded_phase_theorem():
    theorem = _result()["off_phase_trichotomy"]
    assert theorem["ratio_law"] == (
        "P_route/A_route=C_star*C_M*(lambda/Lambda_c)^k*(1+o(1))"
    )
    assert theorem["bounded_phase_theorem_reused_outside_scope"] is False
    assert theorem["derivation_uses_uniform_binomial_remainder"] is True


def test_rh329_obstruction_keeps_the_sign_and_scope_firewall():
    obstruction = _result()["rh329_comparator_obstruction"]
    assert obstruction["D_over_A_route_limit"] == "-1"
    assert obstruction["D_over_H_limit"] == "-infinity"
    assert obstruction["rh330_fixed_phase_transfer_invoked"] is False
    assert obstruction["verdict"] == (
        "STOP_SCOPED_for_RH329_as_physical_fixed_phase_comparator"
    )


def test_correct_clock_route_remains_not_testable():
    barrier = _result()["target_resolution_barrier"]
    assert barrier["ordinary_relative_o_1_is_sufficient"] is False
    assert barrier["correct_clock_physical_remainder_certificate_present"] is False
    assert barrier["verdict"] == (
        "NOT_TESTABLE_after_replacing_Lambda_hat_by_exact_lambda"
    )


def test_finite_rows_and_claim_firewall_are_explicit():
    data = _result()
    assert len(data["finite_hatted_rows"]) == 4
    assert data["finite_rows_are_reproduction_checks_only"] is True
    assert len(data["false_claims"]) == 18
    assert not any(data["false_claims"].values())
    assert set(data["gates"]) == set("ABCDE")
    assert not any(data["gates"].values())
