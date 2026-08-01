"""Build the deterministic RH-335 exact-algebra and claim ledger."""

from __future__ import annotations

from fractions import Fraction
import json
from pathlib import Path
import sys


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from projector_ledger import (  # noqa: E402
    E_MINUS_FIXTURE,
    K_FIXTURE,
    commutator_fixture,
    exact_fixture_audit,
    extension_nonuniqueness_fixture,
    fraction_text,
    localized_ledger_fixture,
    perron_projector,
    remaining_projector,
)


def _exact(value):
    if isinstance(value, Fraction):
        return fraction_text(value)
    if isinstance(value, tuple):
        return [_exact(item) for item in value]
    if isinstance(value, list):
        return [_exact(item) for item in value]
    if isinstance(value, dict):
        return {key: _exact(item) for key, item in value.items()}
    return value


def result_payload() -> dict[str, object]:
    """Return the complete deterministic RH-335 result payload."""

    audit = exact_fixture_audit()
    ledger = localized_ledger_fixture()
    bracket = commutator_fixture()
    extension = extension_nonuniqueness_fixture()

    false_claims = {
        "actual_model_replacement_proved": False,
        "adapted_norm_physical_upper_exponent_proved": False,
        "all_physical_leg_operator_errors_uniform_order_sigma": False,
        "determinant_gluing_activated": False,
        "deterministic_noisy_projector_transport_proved": False,
        "duhamel_full_cycle_closure_proved": False,
        "far_remainder_o_H_k_proved": False,
        "forward_probability_identified_with_cyclic_trace": False,
        "full_trace_replacement_proved": False,
        "head_counterloop_transport_proved": False,
        "hilbert_polya_constructed": False,
        "moving_order_localized_ledger_proved": False,
        "off_alias_background_closed": False,
        "physical_local_parity_density_identified": False,
        "physical_prefix_suffix_norm_bounds_proved": False,
        "riemann_hypothesis_proved": False,
        "riemann_zeros_identified": False,
        "signed_duhamel_cancellation_proved": False,
        "von_mangoldt_trace_proved": False,
        "zeta_divisor_equality": False,
    }

    return {
        "status": "rh335_projector_localized_parity_ledger_and_cellwise_extension_nonuniqueness",
        "scope": "finite_order_exact_projector_gauge_ledger_and_scoped_nonuniqueness",
        "operator_typing": {
            "localized_noisy_trace": "L_sigma_n(J)=Tr(M_J K_sigma^n)",
            "localized_deterministic_trace": "P_n_abs(J)",
            "parity_projector": "rank_one_Riesz_projector_E_minus_sigma",
            "projector_mass": "pi_sigma(J)=Tr(M_J E_minus_sigma)",
            "projector_not_eigenvalue_weighted": True,
            "projector_measure_type": "real_finite_signed_measure",
            "deterministic_parity_allocation": "frozen_noisy_projector_density_gauge",
            "canonical_physical_localization": False,
            "deterministic_projector_transport": False,
        },
        "exact_fixture": {
            "K": _exact(K_FIXTURE),
            "spectrum": _exact(audit["spectrum"]),
            "E_zero": _exact(perron_projector()),
            "E_minus": _exact(E_MINUS_FIXTURE),
            "E_plus": _exact(remaining_projector()),
            "row_sums": _exact(audit["row_sums"]),
            "positive_entries": audit["positive_entries"],
            "spectral_projector_sum_is_identity": audit[
                "spectral_projector_sum_is_identity"
            ],
            "left_right_pairing": _exact(audit["left_right_pairing"]),
            "scaled_factorization_is_invariant": (
                audit["scaled_factorization"] == E_MINUS_FIXTURE
            ),
            "E_minus_idempotent": audit["E_minus_squared"] == E_MINUS_FIXTURE,
            "K_E_minus_equals_minus_two_fifths_E_minus": (
                audit["K_E_minus"]
                == tuple(
                    tuple(Fraction(-2, 5) * value for value in row)
                    for row in E_MINUS_FIXTURE
                )
            ),
            "E_minus_K_equals_minus_two_fifths_E_minus": (
                audit["E_minus_K"]
                == tuple(
                    tuple(Fraction(-2, 5) * value for value in row)
                    for row in E_MINUS_FIXTURE
                )
            ),
            "trace_E_minus": _exact(audit["trace_E_minus"]),
            "projector_masses": _exact(audit["projector_masses"]),
            "projector_masses_are_probabilities": audit[
                "projector_masses_are_probabilities"
            ],
        },
        "localized_ledger_fixture": {
            "n": ledger["n"],
            "r_H": _exact(ledger["r_H"]),
            "lambda_minus": _exact(ledger["lambda_minus"]),
            "P_i": _exact(ledger["localized_deterministic"]),
            "L_i": _exact(ledger["localized_noisy"]),
            "pi_i": _exact(ledger["projector_masses"]),
            "parity_scalar": _exact(ledger["parity_scalar"]),
            "C_i": _exact(ledger["corrected_cells"]),
            "sum_C_i": _exact(ledger["corrected_total"]),
            "c_H_sigma_minus_c_H": _exact(ledger["global_difference"]),
            "partition_sum_error": _exact(
                ledger["corrected_total"] - ledger["global_difference"]
            ),
            "first_alias_counterloop_fixture": False,
            "reason": "n=2_is_only_a_fixed_order_algebra_fixture;_archived_counterloop_requires_k>=2",
        },
        "first_alias_relation": {
            "domain": "k>=2_and_n=2k",
            "q_FT": "sum_J_C_sigma_2k(J)-A_k_2k",
            "alias_packet_sign": "subtracted",
            "omitting_minus_A_is_valid": False,
            "coefficient_type": "hardy_full_trace_constituent",
        },
        "local_deflation_commutator": {
            "n": 2,
            "M_2": _exact(bracket["M_2"]),
            "E_zero_plus_lambda_squared_E_minus": _exact(
                bracket["deflation_E_zero_plus_lambda_squared_E_minus"]
            ),
            "commutator": _exact(bracket["commutator"]),
            "commutator_trace": _exact(bracket["commutator_trace"]),
            "commutator_is_nonzero": bracket["commutator_is_nonzero"],
            "zero_trace_implies_commutation": False,
        },
        "cellwise_extension_nonuniqueness": {
            "global_scalar": _exact(extension["global_scalar"]),
            "projector_gauge_allocation": _exact(
                extension["projector_gauge_allocation"]
            ),
            "zero_total_perturbation": _exact(
                extension["zero_total_perturbation"]
            ),
            "alternative_allocation": _exact(extension["alternative_allocation"]),
            "base_total": _exact(extension["base_total"]),
            "perturbation_total": _exact(extension["perturbation_total"]),
            "alternative_total": _exact(extension["alternative_total"]),
            "allocations_are_distinct": extension["allocations_are_distinct"],
            "every_finite_partition_aggregate_preserved_by_zero_total_measure": True,
            "specific_RH334_interval_projector_mass_nonzero_claimed": False,
        },
        "adapted_norm_route": {
            "verdict": "STOP_SCOPED_NOT_TESTABLE",
            "gamma_threshold": "0.3503698834605293...",
            "missing_inputs": {
                "uniform_physical_delta_j_order_sigma_for_all_legs": False,
                "physical_trace_observation_T_and_prefix_suffix_norm_upper_bounds": False,
                "max_W_j_order_sigma_minus_gamma_with_gamma_below_threshold": False,
            },
            "RH18_conditioning_statement": "lower_bound_sigma^(-1/4+o(1))_only",
            "RH18_lower_bound_substitutes_for_required_upper_bound": False,
            "failure_of_sufficient_majorant_proves_divergence": False,
        },
        "finite_calculations_are_reproduction_checks_only": True,
        "false_claims": false_claims,
        "gates": {key: False for key in "ABCDE"},
        "source_anchors": [
            "RH-18_packet_conditioning_lower_bound_only",
            "RH-325_trace_observation_duhamel_criterion_and_gamma_threshold",
            "RH-326_hardy_parity_alias_sign_ledger",
            "RH-334_corrected_P_abs_and_frozen_basepoint_observation",
        ],
    }


def main() -> None:
    output = ROOT / "results" / "result.json"
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(
        json.dumps(result_payload(), indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    print(output.relative_to(ROOT))


if __name__ == "__main__":
    main()
