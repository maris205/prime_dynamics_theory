"""Build the deterministic RH-330 signed transfer ledger."""

from __future__ import annotations

import json
import sys
from fractions import Fraction
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
RH329 = ROOT.parent / "RH-329-validated-isolated-exchange-model-audit"
sys.path.insert(0, str(ROOT / "src"))
sys.path.insert(0, str(RH329 / "src"))

from full_trace_transfer import (  # noqa: E402
    collapse_shell,
    critical_weighted_contribution,
    fraction_string,
    gauge_shift,
    grouped_signed_interval,
    observable_residual,
    outward_decimal_interval,
    rh331_interface,
    split_residual,
    transfer_audit_row,
    transfer_identity,
    weighted_prefix_decomposition,
)
from isolated_audit import (  # noqa: E402
    MULTIPLIER_CONSTANT,
    PARITY_CONSTANT,
    alias_packet,
    frozen_certificates,
    isolated_interface,
    residual,
    target,
)


ORDERS = (2, 4, 8, 16, 24, 32)


def encoded_interval_row(row: dict[str, Fraction]) -> dict[str, object]:
    return {
        key: {
            "exact": fraction_string(value),
            "interval": outward_decimal_interval(value),
        }
        for key, value in row.items()
    }


def main() -> None:
    rows = [
        transfer_audit_row(
            k,
            model_residual=residual(k),
            alias_scale=alias_packet(k),
            target=target(k),
        )
        for k in ORDERS
    ]
    phase_margin = 1 - PARITY_CONSTANT * MULTIPLIER_CONSTANT
    growth_base = Fraction(frozen_certificates()["growth_base"])

    split = {
        "boundary": Fraction(2),
        "exchange": Fraction(7, 3),
        "observation": Fraction(-5, 6),
        "remainder": Fraction(1, 7),
        "parity": Fraction(3, 5),
        "alias": Fraction(11, 4),
    }
    shifted = gauge_shift(split, Fraction(13, 9))
    gauge_check = {
        "original_split_residual": split_residual(split),
        "shifted_split_residual": split_residual(shifted),
        "original_observable_residual": observable_residual(collapse_shell(split)),
        "shifted_observable_residual": observable_residual(collapse_shell(shifted)),
    }

    model = {
        "boundary": Fraction(1, 2),
        "shell": Fraction(-1, 3),
        "remainder": Fraction(1, 7),
        "parity": Fraction(2, 5),
        "alias": Fraction(3, 4),
    }
    actual = {
        "boundary": Fraction(2, 3),
        "shell": Fraction(-1, 4),
        "remainder": Fraction(1, 8),
        "parity": Fraction(3, 7),
        "alias": Fraction(4, 5),
    }
    identity_check = transfer_identity(actual, model)
    grouped_check = grouped_signed_interval(
        Fraction(3, 2),
        [Fraction(-1), Fraction(-1, 2)],
        [Fraction(1, 10), Fraction(1, 20)],
    )
    prefix_check = weighted_prefix_decomposition(
        Fraction(1, 10), Fraction(1, 2), Fraction(1)
    )

    data = {
        "status": "rh330_joint_cancellation_full_trace_transfer_criterion",
        "scope": "conditional_first_alias_full_trace_constituent_transfer_only",
        "clock": "fixed_phase_moving_order_n=2k",
        "target": "H_k=k*R^(-2k)",
        "finite_rows_status": "exact_reproduction_checks_not_physical_data",
        "observable_five_slot_ledger_proved": True,
        "exact_actual_model_transfer_identity_proved": True,
        "exchange_observation_gauge_invariance_proved": True,
        "critical_weighted_prefix_extraction_identity_proved": True,
        "model_closure_transfer_iff_joint_defect_little_o_proved": True,
        "normalized_limit_transfer_under_joint_little_o_proved": True,
        "modular_critical_plus_far_sufficient_criterion_proved": True,
        "grouped_signed_enclosure_proved_sharp": True,
        "grouped_best_worst_residual_formulas_proved": True,
        "all_abstract_duhamel_terms_retained_before_grouping": True,
        "separate_absolute_majorant_sufficient_but_not_necessary": True,
        "same_unsigned_bounds_opposite_verdict_counterexample_proved": True,
        "order_H_replacement_insufficient_counterexample_proved": True,
        "little_o_alias_replacement_insufficient_for_closure_proved": True,
        "rh329_exact_repair_law_proved": True,
        "rh329_synthetic_closing_repair_counterexample_proved": True,
        "rh329_failure_transfer_under_subalias_joint_defect_proved": True,
        "full_trace_constituent_criterion_is_inactive": True,
        "actual_to_rh329_identification_map_proved": False,
        "actual_critical_packet_identified_with_weighted_prefix_coefficient": False,
        "actual_exchange_observation_split_identified": False,
        "actual_two_channel_duhamel_signed_enclosures_proved": False,
        "actual_all_duhamel_weights_controlled": False,
        "actual_parity_alias_replacement_little_o_proved": False,
        "actual_far_remainder_signed_little_o_proved": False,
        "actual_off_alias_weighted_background_vanishing_proved": False,
        "actual_joint_replacement_little_o_H_proved": False,
        "actual_joint_replacement_little_o_alias_proved": False,
        "actual_critical_coefficient_little_o_proved": False,
        "actual_weighted_full_trace_prefix_vanishing_proved": False,
        "actual_full_trace_replacement_proved": False,
        "actual_full_trace_divergence_proved": False,
        "determinant_gluing_activated": False,
        "head_counterloop_budget_closed": False,
        "single_all_order_operator_constructed": False,
        "finite_rows_promoted_to_physical_asymptotics": False,
        "hilbert_polya_constructed": False,
        "riemann_zeros_identified": False,
        "von_mangoldt_trace_proved": False,
        "zeta_divisor_equality": False,
        "riemann_hypothesis_proved": False,
        "gates": {
            "A_canonical_intrinsic_dynamical_spectral_determinant": False,
            "B_time_oriented_scattering_or_unitary_completion": False,
            "C_self_adjoint_generator_and_intrinsic_T_log_T": False,
            "D_von_mangoldt_weighted_prime_power_traces": False,
            "E_completed_zeta_divisor_equality": False,
        },
        "transfer_theorem": {
            "observable_model_residual": "e_hat=B_hat+S_hat+R_hat+P_hat-A_hat",
            "joint_defect": "Theta=Delta_B+Delta_S+Delta_R+Delta_P-Delta_A",
            "identity": "e_actual=e_hat+Theta",
            "minimal_closure_condition": "Theta=-e_hat+o(H_k)",
            "closing_model_specialization": "e_hat=o(H_k) iff require Theta=o(H_k)",
            "modular_sufficient_condition": (
                "Theta_critical=o(H_k) and Delta_R=o(H_k) separately"
            ),
            "critical_prefix_identity": "E_prefix=E_off+abs(e_actual)/(2H_k)",
        },
        "rh329_application": {
            "negative_alias_limit_exact": fraction_string(-phase_margin),
            "repair_alias_limit_exact": fraction_string(phase_margin),
            "alias_target_growth_base_exact": fraction_string(growth_base),
            "repair_law": "Theta=-e_hat+o(H_k)",
            "synthetic_repair": "Theta_k=-e_hat_k+H_k/k gives e_actual=H_k/k",
            "failure_transfer_sufficient_condition": "Theta_k=o(A_k)",
            "status": "conditional_algebra_not_actual_operator_transfer",
        },
        "sharp_counterexamples": {
            "order_H_not_little_o": {
                "model_residual": "0/1",
                "joint_defect": "H_k",
                "actual_to_target": "1/1",
            },
            "balanced_large_defects": (
                "Delta_B=A_k, Delta_S=-A_k: Theta=0 but l1/H=2A_k/H"
            ),
            "same_unsigned_bounds_breaking": (
                "Delta_B=A_k, Delta_S=A_k: Theta=2A_k"
            ),
            "subalias_not_target_scale": (
                "Theta=A_k/k=o(A_k) but Theta/H_k->infinity"
            ),
        },
        "identity_check": encoded_interval_row(identity_check),
        "gauge_check": encoded_interval_row(gauge_check),
        "grouped_interval_check": encoded_interval_row(grouped_check),
        "critical_prefix_check": encoded_interval_row(prefix_check),
        "row_orders": list(ORDERS),
        "row_count": len(rows),
        "total_retained_synthetic_duhamel_terms": sum(4 * k for k in ORDERS),
        "rows": rows,
        "rh329_interface_consumed": isolated_interface(),
        "rh331_interface": rh331_interface(),
    }

    output = ROOT / "results" / "result.json"
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(
        json.dumps(data, indent=2, sort_keys=True, allow_nan=False) + "\n"
    )
    print(
        json.dumps(
            {
                "all_balanced_cancellations_exact": all(
                    row["balanced_cancellation_exact"] for row in rows
                ),
                "all_repairs_exact": all(
                    row["repaired_residual_is_H_over_k_exact"] for row in rows
                ),
                "rows": len(rows),
                "synthetic_duhamel_terms": data[
                    "total_retained_synthetic_duhamel_terms"
                ],
            },
            sort_keys=True,
        )
    )


if __name__ == "__main__":
    main()
