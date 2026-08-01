import json
from pathlib import Path

from experiments.build_result import result_payload


ROOT = Path(__file__).resolve().parents[1]


def _result():
    return json.loads((ROOT / "results/result.json").read_text(encoding="utf-8"))


def test_result_file_is_deterministic():
    assert _result() == result_payload()


def test_phase_law_has_unique_double_alias_balance():
    law = _result()["phase_law"]
    assert law["P_over_S_limit_at_fixed_eta"].endswith("/2")
    assert law["unique_double_alias_balance_phase"].startswith("eta_2=")


def test_conditional_obstruction_keeps_actual_hypothesis_explicit():
    obstruction = _result()["conditional_physical_obstruction"]
    assert obstruction["hypothesis"].startswith("Y_k=o(H_k)")
    assert obstruction["conclusion"].endswith("->infinity")
    assert obstruction["aggregate_nonclosure_claimed"] is False


def test_balance_phase_is_not_promoted_to_target_closure():
    precision = _result()["balance_phase_precision"]
    assert precision["source_phase_law_precision"] == "relative_o(1)_only"
    assert precision["target_closure_decided"] is False


def test_scalar_information_class_is_not_an_actual_operator_claim():
    scalar = _result()["scalar_information_class"]
    assert scalar["close_direct_residual"] == "0"
    assert scalar["far_direct_residual"] == "A_k/k"
    assert scalar["actual_noisy_realization_claimed"] is False


def test_finite_rows_are_diagnostics_only():
    data = _result()
    assert len(data["finite_rows"]) == 4
    assert data["finite_rows_are_reproduction_checks_only"] is True


def test_claim_firewall_and_gates_remain_false():
    data = _result()
    assert len(data["false_claims"]) == 21
    assert not any(data["false_claims"].values())
    assert set(data["gates"]) == set("ABCDE")
    assert not any(data["gates"].values())


def test_route_moves_to_lower_sideband_decomposition():
    boundary = _result()["route_boundary"]
    assert boundary["scalar_only_parity_mechanism"].startswith("STOP_SCOPED")
    assert boundary["actual_critical_signed_compensation"].startswith("NOT_TESTABLE")
    assert boundary["next_route"].startswith("RH-346")
