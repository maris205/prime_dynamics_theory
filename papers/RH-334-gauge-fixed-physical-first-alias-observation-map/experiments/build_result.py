"""Build the deterministic RH-334 reproduction and claim ledger."""

from __future__ import annotations

from fractions import Fraction
import json
from pathlib import Path
import sys

import mpmath as mp


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from physical_observation import (  # noqa: E402
    EXPECTED_COEFFICIENT_TYPE,
    exact_block_folding_fixture,
    exact_fraction_ledger,
    finite_nystrom_folding_check,
    fraction_text,
    frozen_windows,
    period_two_bijection_rows,
    period_two_slot_weights,
    period_two_total_weight,
    period_two_witness,
    positive_gauge_shift_check,
    validate_coefficient_type,
    validate_localized_weight_partition,
)


def _decimal(value: mp.mpf, digits: int = 34) -> str:
    return mp.nstr(value, digits, strip_zeros=False)


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


def _mutation_locks() -> dict[str, bool]:
    witness = period_two_witness()
    old_slots = period_two_slot_weights(corrected=False)
    old_binning_rejected = False
    try:
        validate_localized_weight_partition(old_slots, period_two_total_weight())
    except ValueError:
        old_binning_rejected = True
    wrong_type_rejected = False
    try:
        validate_coefficient_type("modulus_complement")
    except ValueError:
        wrong_type_rejected = True
    with mp.workdps(110):
        missing_weight_lock = mp.almosteq(
            period_two_total_weight() - mp.fsum(old_slots.values()),
            witness.cycle_weight,
        )
    return {
        "old_signed_x_binning_rejected": old_binning_rejected,
        "wrong_coefficient_type_rejected": wrong_type_rejected,
        "old_binning_misses_exactly_one_cycle_weight": missing_weight_lock,
    }


def result_payload() -> dict[str, object]:
    """Return the complete deterministic result and claim firewall."""

    witness = period_two_witness()
    rows = period_two_bijection_rows()
    windows = frozen_windows()
    corrected_slots = period_two_slot_weights(corrected=True)
    old_slots = period_two_slot_weights(corrected=False)
    validate_localized_weight_partition(corrected_slots, period_two_total_weight())
    block = exact_block_folding_fixture()
    nystrom = finite_nystrom_folding_check()
    gauge = positive_gauge_shift_check()
    if gauge["contains_period_two_point"]:
        raise RuntimeError("the frozen gauge set must avoid Fix(T^2)")
    ledger = exact_fraction_ledger()
    validate_coefficient_type(ledger["coefficient_type"])
    with mp.workdps(110):
        old_positive_total = +(witness.fixed_weight + witness.cycle_weight)
        corrected_total = +(witness.fixed_weight + 2 * witness.cycle_weight)

    false_claims = {
        "actual_model_replacement_proved": False,
        "all_cycle_trace_localization_proved": False,
        "determinant_gluing_activated": False,
        "duhamel_full_cycle_closure_proved": False,
        "far_remainder_o_H_k_proved": False,
        "forward_probability_identified_with_cyclic_trace": False,
        "full_trace_replacement_proved": False,
        "head_counterloop_transport_proved": False,
        "hilbert_polya_constructed": False,
        "moving_order_localization_proved": False,
        "off_alias_background_closed": False,
        "perron_or_parity_projectors_localized": False,
        "physical_exchange_parameter_identified": False,
        "riemann_hypothesis_proved": False,
        "riemann_zeros_identified": False,
        "slot_asymptotics_proved": False,
        "slot_signs_proved": False,
        "time_floquet_sectors_localized": False,
        "von_mangoldt_trace_proved": False,
        "zeta_divisor_equality": False,
    }

    return {
        "status": "rh334_gauge_fixed_physical_first_alias_observation_map",
        "data_type": (
            "folded_source_basepoint_localized_noisy_minus_physical_flat_trace_"
            "in_the_hardy_full_trace_constituent"
        ),
        "coefficient_type": EXPECTED_COEFFICIENT_TYPE,
        "operator_typing": {
            "signed_domain": "I=[-1,1]",
            "folded_domain": "I_plus=[0,1]",
            "deterministic_fold": "T=abs(f)",
            "operator_action": "backward_observable",
            "multiplication_role": "M_J_marks_source_basepoint",
            "kernel_orientation": "first_variable_source_second_variable_destination",
            "signed_folded_orientation": "signed_x_maps_to_folded_y=abs(x)",
            "noisy_operator_trace_orders": "n>=2",
            "deterministic_bijection_orders": "n>=1",
            "localized_peripheral_projectors": False,
            "localized_floquet_sectors": False,
        },
        "n2_witness": {
            "u_c": _decimal(witness.critical.u),
            "r": _decimal(witness.critical.r),
            "lambda": _decimal(witness.critical.lambda_fixed),
            "fold_cusp_b": _decimal(witness.critical.fold_cusp),
            "x_minus": _decimal(witness.x_minus),
            "x_plus": _decimal(witness.x_plus),
            "y_minus_abs_x_minus": _decimal(witness.y_minus),
            "cycle_multiplier": _decimal(witness.cycle_multiplier),
            "fixed_weight_w_r": _decimal(witness.fixed_weight),
            "cycle_weight_w_c": _decimal(witness.cycle_weight),
            "cycle_weight_exact_formula": "1/(4*u_c-3)",
            "old_positive_x_total": _decimal(old_positive_total),
            "corrected_total": _decimal(corrected_total),
            "exact_missing_weight": _decimal(witness.cycle_weight),
        },
        "period_two_bijection_rows": [
            {
                key: _decimal(value)
                for key, value in row.items()
            }
            for row in rows
        ],
        "frozen_partition": {
            "k": 2,
            "sigma": "1/4",
            "A": "1/4",
            "J_minus": f"[{_decimal(windows.minus_left)},{_decimal(windows.fold_cusp)})",
            "J_plus": f"[{_decimal(windows.fold_cusp)},{_decimal(windows.plus_right)}]",
            "F": "[0,1]\\(J_minus_union_J_plus)",
            "corrected_P_abs_slots": {
                key: _decimal(value) for key, value in corrected_slots.items()
            },
            "old_positive_x_slots": {
                key: _decimal(value) for key, value in old_slots.items()
            },
            "expected_corrected_symbolic_slots": ["0", "w_c", "w_r+w_c"],
            "expected_old_symbolic_slots": ["0", "w_c", "w_r"],
            "deterministic_membership_rule": "abs(x)_in_J",
            "endpoint_ownership": {
                "minus_left": "J_minus",
                "fold_cusp_b": "J_plus",
                "plus_right": "J_plus",
                "outside_union": "F",
            },
            "windows_frozen_before_evaluation": True,
        },
        "exact_rational_block_folding": {
            "signed_matrix": _exact(block["signed_matrix"]),
            "folded_matrix": _exact(block["folded_matrix"]),
            "signed_localized_traces": _exact(block["signed_localized_traces"]),
            "folded_localized_traces": _exact(block["folded_localized_traces"]),
            "identity_holds": block["identity_holds"],
        },
        "finite_nystrom_folding": {
            "order": nystrom["order"],
            "decimal_digits": nystrom["decimal_digits"],
            "sigma": _decimal(nystrom["sigma"]),
            "rows": [
                {
                    "slot": row["slot"],
                    "signed_trace": _decimal(row["signed_trace"]),
                    "folded_trace": _decimal(row["folded_trace"]),
                    "absolute_error": _decimal(row["absolute_error"]),
                }
                for row in nystrom["rows"]
            ],
            "maximum_absolute_error": _decimal(nystrom["maximum_absolute_error"]),
            "certification_status": nystrom["certification_status"],
        },
        "partition_dependence_reproduction": {
            "E": f"[{_decimal(gauge['left'])},{_decimal(gauge['right'])})",
            "symbolic_E": "[b-1/10,b-2/25)",
            "length": _decimal(gauge["length"]),
            "exact_length": "1/50",
            "source_cell": "J_minus",
            "target_cell": "F",
            "contained_in_J_minus": gauge["contained_in_J_minus"],
            "contains_period_two_point": gauge["contains_period_two_point"],
            "localized_trace": _decimal(gauge["localized_trace"]),
            "hardy_scaled_delta": _decimal(gauge["hardy_scaled_delta"]),
            "shift_vector": [_decimal(value) for value in gauge["shift_vector"]],
            "certification_status": gauge["certification_status"],
        },
        "exact_fraction_ledger": _exact(ledger),
        "coefficient_relations": {
            "q_FT": "c_H_sigma-s_k_n-a_n_num",
            "first_alias_identity": "q_FT=B+S+R+P-A",
            "slot_sign_pattern": "+B+S+R+P-A",
            "localized_slot_scale": "r_H^(-n)",
            "q_FT_equals": "e_sigma_k_2k",
            "modulus_complement_relation": "tau_sigma_n-a_n_num=q_FT-d_sigma_k_n",
            "d_definition": "d_sigma_k_n=h_sigma_n-s_k_n",
            "q_FT_is_modulus_complement_without_d_zero": False,
        },
        "mutation_locks": _mutation_locks(),
        "exact_localized_signed_folded_noisy_trace_identity_proved": True,
        "multiplier_preserving_fixed_point_bijection_proved": True,
        "corrected_P_abs_localization_proved": True,
        "rh327_old_localized_partition_disproved_at_n2": True,
        "frozen_partition_additivity_proved": True,
        "first_alias_five_slot_ledger_proved": True,
        "strict_window_partition_dependence_proved": True,
        "window_partition_dependence_distinguished_from_exchange_observation_gauge": True,
        "fraction_fixture_errors_are_zero": (
            ledger["q_path_error"] == 0 and ledger["tau_relation_error"] == 0
        ),
        "finite_rows_promoted_to_continuum_certificates": False,
        "false_claims": false_claims,
        "gates": {key: False for key in "ABCDE"},
        "source_anchors": [
            "RH-10_signed_map_physical_flat_trace_and_trace_class",
            "RH-14_deterministic_and_noisy_folding",
            "RH-15_full_signed_physical_flat_trace",
            "RH-17_inverse_jacobian_channel_only",
            "RH-18_folded_kernel_and_time_labeled_path_distinction",
            "RH-19_folded_Hilbert_Schmidt_square_trace_class",
            "RH-326_hardy_parity_alias_coefficient_ledger",
            "RH-327_localized_definition_repaired_here",
            "RH-330_exchange_observation_gauge_distinction",
        ],
    }


def main() -> None:
    payload = result_payload()
    (ROOT / "results/result.json").write_text(
        json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )
    print(
        json.dumps(
            {
                "bijection_rows": len(payload["period_two_bijection_rows"]),
                "false_claims": len(payload["false_claims"]),
                "nystrom_rows": len(payload["finite_nystrom_folding"]["rows"]),
                "q_path_error": payload["exact_fraction_ledger"]["q_path_error"],
            },
            sort_keys=True,
        )
    )


if __name__ == "__main__":
    main()
