import json
from pathlib import Path

from experiments.build_result import result_payload


ROOT = Path(__file__).resolve().parents[1]


def _result():
    return json.loads((ROOT / "results/result.json").read_text(encoding="utf-8"))


def test_result_file_is_deterministic():
    assert _result() == result_payload()


def test_clock_does_not_create_a_new_noise_sequence_at_m():
    clock = _result()["clock"]
    assert clock["lower_orbit_parameter"] == "m=k-1"
    assert clock["new_noise_clock_at_m"] is False


def test_complete_orbit_and_cellwise_refinement_are_typed():
    data = _result()
    assert data["complete_orbit"]["cardinality"] == "2m_distinct"
    assert data["cellwise_refinement"]["eventual_counts_Jminus_Jplus_F"] == "(epsilon_m,0,2m-epsilon_m)"
    assert data["cellwise_refinement"]["threshold_equality_stabilization"].startswith("NOT_DETERMINED")


def test_direct_identity_keeps_radial_and_head_signs():
    typed = _result()["typed_identity"]
    assert "-d_" in typed["direct"]
    assert "-A_" in typed["direct"]
    assert "-F_m" in typed["direct"]


def test_radial_sideband_is_relative_small_not_target_negligible():
    radial = _result()["radial_sideband"]
    assert radial["relative_to_full"].endswith("->0")
    assert radial["eventual_sign_source_locked"] is False
    assert radial["target_negligibility_source_locked"] is False
    assert radial["combined_demand_eventually_positive"] is True


def test_lower_phase_law_is_recorded_only_as_next_interface():
    phase = _result()["lower_parity_phase"]
    assert phase["P_(sigma,2m)_over_F_m_limit"].endswith("lambda^(eta-1)")
    assert phase["compensation_decided"] is False


def test_finite_rows_are_diagnostics_only():
    data = _result()
    assert len(data["finite_rows"]) == 5
    assert data["finite_rows_are_reproduction_checks_only"] is True


def test_claim_firewall_and_gates_remain_false():
    data = _result()
    assert len(data["false_claims"]) == 19
    assert not any(data["false_claims"].values())
    assert set(data["gates"]) == set("ABCDE")
    assert not any(data["gates"].values())


def test_route_moves_to_rh347_without_closing_E_off():
    route = _result()["route_boundary"]
    assert route["lower_signed_compensation"].startswith("NOT_TESTABLE")
    assert route["remaining_E_off"].startswith("NOT_TESTABLE")
    assert route["next_route"].startswith("RH-347")
