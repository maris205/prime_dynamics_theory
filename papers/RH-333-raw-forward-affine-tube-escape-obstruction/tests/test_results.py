import json
from pathlib import Path

from experiments.build_result import result_payload


ROOT = Path(__file__).resolve().parents[1]


def _result():
    return json.loads((ROOT / "results/result.json").read_text(encoding="utf-8"))


def test_result_is_deterministic_and_has_exact_row_counts():
    data = _result()
    assert data == result_payload()
    assert len(data["finite_orbit_rows"]) == 6
    assert len(data["limiting_phase_rows"]) == 3
    assert [row["component_period"] for row in data["finite_orbit_rows"]] == [
        4,
        8,
        12,
        16,
        20,
        24,
    ]


def test_positive_claims_record_the_scoped_obstruction():
    data = _result()
    positive_fields = (
        "exact_forward_affine_expansion_proved",
        "sigma_scaled_coordinate_about_cycle_point_used",
        "canonical_two_step_tangent_coarsening_derived",
        "exact_first_innovation_sd_product_identity_proved",
        "signed_forward_mean_slopes_used",
        "forward_variance_recurrence_with_plus_noise_proved",
        "rh18_widths_identified_as_peak_normalized_backward_observables",
        "gaussian_maximum_interval_mass_lemma_proved",
        "physical_preclosing_support_interval_length_is_one_over_sigma",
        "factor_four_unhalved_l1_lower_bound_proved",
        "marginal_contraction_lifts_bound_to_retained_paths",
        "full_retained_extensions_including_preclosing_coordinate_covered",
        "fixed_phase_positive_path_l1_liminf_proved",
        "compact_phase_uniform_positive_path_l1_liminf_proved",
        "fixed_or_compact_phase_raw_forward_retained_path_O_k_sigma_disproved",
        "fixed_or_compact_phase_raw_forward_retained_path_o_H_k_disproved",
        "raw_full_line_mass_one_affine_reference_refuted_at_preclosing_path_scope",
        "symbolic_constants_used_in_theorem",
        "unhalved_l1_convention",
    )
    assert all(data[field] is True for field in positive_fields)
    assert "k_minus_1_component_row" in data["data_type"]
    assert "retained_preclosing_coordinate" in data["data_type"]
    assert data["phase_scope"] == {
        "eta_sigma": "k-log(1/sigma)/(2*log(lambda))",
        "fixed_phase": "eta_sigma_converges_to_a_finite_eta",
        "compact_phase": "eta_sigma_stays_in_one_fixed_compact_interval",
        "rate_refutation_scope": "fixed_or_compact_first_alias_phase",
    }


def test_signed_slope_period_and_preclosing_scope_are_explicit():
    data = _result()
    scope = data["period_scope"]
    assert scope["component_period"] == "k"
    assert scope["minimum_component_period"] == 2
    assert scope["sigma_domain"] == "sigma>0"
    assert scope["physical_one_step_period"] == "2k"
    assert scope["raw_prefix_component_rows"] == "k-1"
    assert scope["retained_coordinate"] == "q_k_minus_1_preclosing"
    for row in data["finite_orbit_rows"]:
        assert row["physical_one_step_period"] == 2 * row["component_period"]
        assert row["signed_first_slope"] < 0
        assert row["signed_last_slope"] > 0
        assert row["product_identity_relative_error"] < 1e-85


def test_symbolic_theorem_is_separated_from_noncertified_decimals():
    data = _result()
    constants = data["theorem_constants"]
    assert "C_b" in constants["symbolic"]["C_s"]
    assert "C_M" in constants["symbolic"]["C_s"]
    assert constants["decimal_values_are_interval_certificates"] is False
    assert data["finite_rows_promoted_to_asymptotic_evidence"] is False
    assert all(
        row["certification_status"] == "noncertified_reproduction"
        for row in data["finite_orbit_rows"] + data["limiting_phase_rows"]
    )


def test_all_out_of_scope_claims_and_gates_remain_false():
    data = _result()
    assert len(data["false_claims"]) == 19
    assert not any(data["false_claims"].values())
    assert set(data["gates"]) == set("ABCDE")
    assert not any(data["gates"].values())
    assert data["false_claims"]["final_endpoint_marginal_lower_bound_proved"] is False
    assert data["false_claims"]["closing_row_endpoint_failure_proved"] is False
    assert data["false_claims"]["cyclic_bridge_refuted"] is False
    assert data["false_claims"]["doob_transform_refuted"] is False
    assert data["false_claims"]["physical_truncated_folded_affine_kernel_refuted"] is False
    assert data["false_claims"]["adapted_reference_refuted"] is False
    assert data["false_claims"]["branch_complete_nonlinear_closing_profile_refuted"] is False
