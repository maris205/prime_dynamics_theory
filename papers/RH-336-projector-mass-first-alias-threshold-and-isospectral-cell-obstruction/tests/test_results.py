import json
from fractions import Fraction
from pathlib import Path

from experiments.build_result import result_payload


ROOT = Path(__file__).resolve().parents[1]


def _result():
    return json.loads((ROOT / "results" / "result.json").read_text(encoding="utf-8"))


def test_result_file_is_deterministic():
    assert _result() == result_payload()


def test_moving_threshold_symbolic_types_and_exponent_distinction_are_locked():
    theorem = _result()["moving_theorem"]
    assert theorem["ratio_asymptotic"] == (
        "G/H=2*C_star*lambda^eta_sigma*(beta*R)^(2k)*pi_sigma(J)*(1+o(1))"
    )
    assert theorem["kappa_proj_symbolic"] == (
        "log(beta*R)/log(lambda)=log(28/17)/log(lambda)-1/2"
    )
    assert theorem["kappa_proj_equals_gamma_star_RH325"] is False
    assert theorem["exact_exponent_order"] == "kappa_proj>gamma_star_RH325"
    assert theorem["exponent_separation_certificate"] == {
        "R_squared_over_r_H": "196/85",
        "conclusion": "kappa_proj>gamma_star_RH325",
        "kappa_minus_gamma_formula": (
            "log((R^2/r_H)/lambda^(3/2))/log(lambda)"
        ),
        "lambda_polynomial": "lambda^3+4*lambda^2-16=0",
        "lambda_upper_bound": "17/10",
        "polynomial_at_upper": "473/1000",
        "positive_axis_derivative": "3*lambda^2+8*lambda>0",
        "squared_comparison_gap": "116783/289000",
    }
    assert theorem["beta_R_greater_than_one"] is True
    assert theorem["negligibility_equivalence"] == (
        "G=o(H)_iff_pi=o((beta*R)^(-2k))"
    )


def test_fixed_partition_conclusion_keeps_the_maximizer_and_cancellation_scope():
    data = _result()["fixed_partition_consequence"]
    assert data["max_pi_i_lower_bound"] == "1/N"
    assert data["maximum_normalized_parity_cell_diverges"] is True
    assert data["maximizing_cell_may_depend_on_sigma"] is True
    assert data["pigeonhole_fixed_cell_only_on_subsequence"] is True
    assert data["identified_with_physical_B_plus_S"] is False
    assert data["raw_local_alias_signed_cancellation_may_remove_contribution"] is True


def test_exact_family_locks_sufficient_not_maximal_interval_and_power_traces():
    family = _result()["exact_family"]
    assert family["sufficient_positivity_interval"] == "(-5/174,1/2)"
    assert family["sufficient_interval_is_maximal"] is False
    assert family["maximal_connected_positivity_interval_containing_zero"] == (
        "(-5/174,(-19+sqrt(781))/12)"
    )
    assert family["spectrum"] == ["1/1", "-2/5", "1/5"]
    assert family["all_power_trace_formula"] == (
        "Tr(K_t^m)=1+(-2/5)^m+(1/5)^m_for_m>=1"
    )
    assert len(family["t_fixture"]["power_rows"]) == 12
    assert all(
        row["direct_trace"] == row["spectral_trace"]
        for row in family["t_fixture"]["power_rows"]
    )


def test_projector_and_corrected_cell_drifts_are_exact():
    data = _result()
    mass = data["projector_mass_family"]
    cells = data["corrected_cell_family"]
    assert mass["pi_t"] == ["(10-8t)/17", "(-4+24t)/51", "25/51"]
    assert mass["drift"] == ["-8t/17", "8t/17", "0"]
    assert cells["C_t"] == [
        "(6800-5760t)/4913",
        "(400+5760t)/4913",
        "6672/4913",
    ]
    assert cells["sum_C_t"] == "48/17"
    assert cells["t_1_over_100_drift"] == [
        "-288/24565",
        "288/24565",
        "0/1",
    ]
    assert cells["first_alias_k1_interpretation"] is False


def test_phase_conversion_rows_are_numeric_reproduction_only_and_close():
    diagnostics = _result()["moving_scale_diagnostics"]
    assert diagnostics["certification_status"] == (
        "ordinary_floating_point_reproduction_only"
    )
    assert 0.4634 < diagnostics["kappa_proj"] < 0.4635
    assert 0.1130 < diagnostics["diagnostic_decimal_gap"] < 0.1131
    assert len(diagnostics["phase_conversion_rows"]) == 3
    for row in diagnostics["phase_conversion_rows"]:
        assert row["absolute_error"] < 1e-15


def test_physical_route_novelty_and_claim_firewall_are_explicit():
    data = _result()
    assert data["physical_duhamel_route"]["verdict"] == "NOT_TESTABLE"
    assert data["physical_duhamel_route"]["physical_nonzero_normalized_obstruction"] == (
        "absent"
    )
    assert data["novelty_boundary"] == {
        "RH210_fixed_divisor_projector_motion_example_preexists": True,
        "RH336_adds_all_power_trace_lock": True,
        "RH336_adds_corrected_singleton_cell_drift": True,
        "RH336_adds_strict_positive_row_stochastic_family": True,
    }
    assert data["finite_calculations_are_reproduction_checks_only"] is True
    assert len(data["false_claims"]) == 19
    assert not any(data["false_claims"].values())
    assert set(data["gates"]) == set("ABCDE")
    assert not any(data["gates"].values())


def test_all_fraction_strings_in_exact_fixture_parse():
    family = _result()["exact_family"]["t_fixture"]
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

    collect(family)
    assert len(strings) >= 100
    assert all(Fraction(value).denominator > 0 for value in strings)
