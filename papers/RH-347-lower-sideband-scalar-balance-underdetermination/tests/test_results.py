import json
from pathlib import Path

from experiments.build_result import result_payload


ROOT = Path(__file__).resolve().parents[1]


def _result():
    return json.loads((ROOT / "results/result.json").read_text(encoding="utf-8"))


def test_result_file_is_deterministic():
    assert _result() == result_payload()


def test_clock_keeps_m_as_period_parameter_only():
    clock = _result()["clock"]
    assert clock["lower_orbit_parameter"] == "m=k-1"
    assert clock["retained_relation"] == "k=m+1"
    assert clock["inverse_root_exponent"] == "1/(2m)"
    assert clock["new_noise_clock_at_m"] is False


def test_lower_identity_keeps_head_and_radial_terms_typed():
    identity = _result()["lower_identity"]
    assert "-d_" in identity["orbit_free_remainder"]
    assert "+A_" in identity["combined_demand"]
    assert identity["direct"].endswith("-S_m^-")


def test_conditional_obstruction_records_exact_coefficient():
    obstruction = _result()["conditional_physical_obstruction"]
    assert obstruction["hypothesis"].startswith("Y_m^-=o(H_m)")
    assert obstruction["exact_asymptotic_coefficient"].startswith(
        "abs(C_star*C_M"
    )
    assert obstruction["aggregate_nonclosure_claimed"] is False


def test_balance_phase_is_not_promoted_to_target_closure_or_window_exclusion():
    data = _result()
    assert data["phase_law"]["balance_interface_novel_here"] is False
    assert data["phase_law"]["decimal_excludes_canonical_window"] is False
    assert data["balance_phase_precision"]["target_closure_decided"] is False


def test_scalar_information_class_is_not_an_actual_operator_claim():
    scalar = _result()["scalar_information_class"]
    assert scalar["close_direct_residual"] == "0"
    assert scalar["far_direct_residual"] == "F_m^orb/m=2G_m"
    assert scalar["far_weighted_lower"] == "G_m/H_m->infinity"
    assert scalar["actual_noisy_realization_claimed"] is False


def test_finite_rows_are_diagnostics_only():
    data = _result()
    assert len(data["finite_rows"]) == 4
    assert data["finite_rows_are_reproduction_checks_only"] is True


def test_claim_firewall_and_gates_remain_false():
    data = _result()
    assert len(data["false_claims"]) == 19
    assert not any(data["false_claims"].values())
    assert set(data["gates"]) == set("ABCDE")
    assert not any(data["gates"].values())


def test_route_moves_to_punctured_aggregate_without_closing_E_off():
    route = _result()["route_boundary"]
    assert route["lower_scalar_parity_mechanism"].startswith("STOP_SCOPED")
    assert route["actual_lower_signed_compensation"].startswith(
        "NOT_TESTABLE"
    )
    assert route["remaining_E_off"].startswith("NOT_TESTABLE")
    assert route["next_route"].startswith("RH-348")
