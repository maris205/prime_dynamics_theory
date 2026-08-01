import json
from fractions import Fraction
from pathlib import Path

from experiments.build_result import result_payload


ROOT = Path(__file__).resolve().parents[1]


def _result():
    return json.loads((ROOT / "results" / "result.json").read_text(encoding="utf-8"))


def test_result_file_is_deterministic():
    assert _result() == result_payload()


def test_exact_fixture_and_projector_mass_type_are_locked():
    data = _result()
    fixture = data["exact_fixture"]
    assert fixture["spectrum"] == ["1/1", "-2/5", "1/5"]
    assert fixture["E_minus_idempotent"] is True
    assert fixture["K_E_minus_equals_minus_two_fifths_E_minus"] is True
    assert fixture["E_minus_K_equals_minus_two_fifths_E_minus"] is True
    assert fixture["trace_E_minus"] == "1/1"
    assert fixture["projector_masses"] == ["10/17", "-4/51", "25/51"]
    assert fixture["projector_masses_are_probabilities"] is False


def test_localized_ledger_keeps_the_alias_subtraction_and_fixture_boundary():
    data = _result()
    ledger = data["localized_ledger_fixture"]
    relation = data["first_alias_relation"]
    assert ledger["C_i"] == ["400/289", "400/4913", "6672/4913"]
    assert ledger["sum_C_i"] == ledger["c_H_sigma_minus_c_H"] == "48/17"
    assert ledger["partition_sum_error"] == "0/1"
    assert ledger["first_alias_counterloop_fixture"] is False
    assert relation["domain"] == "k>=2_and_n=2k"
    assert relation["q_FT"] == "sum_J_C_sigma_2k(J)-A_k_2k"
    assert relation["omitting_minus_A_is_valid"] is False


def test_commutator_and_extension_nonuniqueness_are_both_strict():
    data = _result()
    bracket = data["local_deflation_commutator"]
    extension = data["cellwise_extension_nonuniqueness"]
    assert bracket["commutator_is_nonzero"] is True
    assert bracket["commutator_trace"] == "0/1"
    assert bracket["zero_trace_implies_commutation"] is False
    assert extension["perturbation_total"] == "0/1"
    assert extension["base_total"] == extension["alternative_total"] == "21/25"
    assert extension["allocations_are_distinct"] is True
    assert extension["specific_RH334_interval_projector_mass_nonzero_claimed"] is False


def test_adapted_norm_stop_names_all_three_missing_upper_inputs():
    route = _result()["adapted_norm_route"]
    assert route["verdict"] == "STOP_SCOPED_NOT_TESTABLE"
    assert route["gamma_threshold"] == "0.3503698834605293..."
    assert set(route["missing_inputs"]) == {
        "uniform_physical_delta_j_order_sigma_for_all_legs",
        "physical_trace_observation_T_and_prefix_suffix_norm_upper_bounds",
        "max_W_j_order_sigma_minus_gamma_with_gamma_below_threshold",
    }
    assert not any(route["missing_inputs"].values())
    assert route["RH18_lower_bound_substitutes_for_required_upper_bound"] is False
    assert route["failure_of_sufficient_majorant_proves_divergence"] is False


def test_every_fraction_string_in_exact_sections_parses():
    data = _result()
    strings = []

    def collect(value):
        if isinstance(value, str) and "/" in value:
            numerator, denominator = value.split("/", 1)
            if numerator.lstrip("-").isdigit() and denominator.isdigit():
                strings.append(value)
        elif isinstance(value, list):
            for item in value:
                collect(item)
        elif isinstance(value, dict):
            for item in value.values():
                collect(item)

    for key in (
        "exact_fixture",
        "localized_ledger_fixture",
        "local_deflation_commutator",
        "cellwise_extension_nonuniqueness",
    ):
        collect(data[key])
    assert len(strings) >= 80
    assert all(Fraction(value).denominator > 0 for value in strings)


def test_claim_firewall_and_all_gates_remain_false():
    data = _result()
    assert data["finite_calculations_are_reproduction_checks_only"] is True
    assert len(data["false_claims"]) == 20
    assert not any(data["false_claims"].values())
    assert set(data["gates"]) == set("ABCDE")
    assert not any(data["gates"].values())
    for key in (
        "adapted_norm_physical_upper_exponent_proved",
        "moving_order_localized_ledger_proved",
        "physical_local_parity_density_identified",
        "deterministic_noisy_projector_transport_proved",
        "signed_duhamel_cancellation_proved",
        "riemann_hypothesis_proved",
    ):
        assert data["false_claims"][key] is False
