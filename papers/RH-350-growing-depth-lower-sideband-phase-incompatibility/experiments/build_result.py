"""Build the deterministic RH-350 growing-depth ledger."""

from __future__ import annotations

from decimal import Decimal
import json
from pathlib import Path
import sys


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from growing_sideband_phase import (  # noqa: E402
    C_M_DIAGNOSTIC,
    C_STAR_DIAGNOSTIC,
    R_H,
    R_TRACE,
    balance_phase,
    decimal_text,
    growing_row,
    physical_constants,
    relative_minimax,
    weighted_minimax,
)


def _encode(value):
    if isinstance(value, Decimal):
        return decimal_text(value)
    if isinstance(value, list):
        return [_encode(item) for item in value]
    if isinstance(value, tuple):
        return [_encode(item) for item in value]
    if isinstance(value, dict):
        return {key: _encode(item) for key, item in value.items()}
    return value


def result_payload() -> dict[str, object]:
    constants = physical_constants()
    fixed_depths = [_encode(relative_minimax(depth)) for depth in (3, 5, 8, 12)]
    weighted = [_encode(weighted_minimax(n)) for n in (1, 3, 6, 10)]
    rows = [
        _encode(growing_row(k, depth))
        for k, depth in ((18, 4), (28, 5), (40, 6), (56, 7))
    ]
    false_claims = {
        "actual_aggregate_Y_negligible_proved": False,
        "actual_uniform_Y_negligible_proved": False,
        "actual_Y_hypothesis_verified_numerically": False,
        "unconditional_selected_subprefix_nonclosure_proved": False,
        "unconditional_full_prefix_nonclosure_proved": False,
        "actual_E_off_closed": False,
        "actual_E_off_nonclosure_proved": False,
        "odd_orders_controlled": False,
        "upper_alias_orders_controlled": False,
        "finite_rows_are_asymptotic_evidence": False,
        "finite_rows_are_operator_observations": False,
        "growing_depth_inferred_from_fixed_depth_only": False,
        "determinant_gluing_activated": False,
        "rh288_activated": False,
        "hilbert_polya_constructed": False,
        "riemann_hypothesis_proved": False,
        "riemann_zeros_identified": False,
        "von_mangoldt_trace_proved": False,
        "zeta_divisor_equality": False,
        "gate_A_closed": False,
    }
    return {
        "status": "rh350_growing_depth_lower_sideband_phase_incompatibility",
        "verdict": "GO_SCOPED_uniform_deterministic_and_conditional_actual_subprefix",
        "scope": "J_k_to_infinity_J_k_o_k_selected_lower_even_direct_coefficients",
        "constants": {
            "r_H": f"{R_H.numerator}/{R_H.denominator}",
            "R": f"{R_TRACE.numerator}/{R_TRACE.denominator}",
            "C_star_source_decimal_diagnostic": decimal_text(C_STAR_DIAGNOSTIC),
            "C_M_source_decimal_diagnostic": decimal_text(C_M_DIAGNOSTIC),
            "eta_balance_diagnostic": decimal_text(balance_phase()),
            **_encode(constants),
            "x_lambda_exact": "(28/17)^2",
            "decimal_status": "finite_diagnostics_not_interval_certificates",
        },
        "index_family": {
            "physical_noise_clock": "k=log(1/sigma)/(2log(lambda))+O(1)",
            "phase": "eta_k_bounded",
            "sidebands": "m_(k,j)=k-j_for_2<=j<=J_k",
            "depth": "J_k->infinity_and_J_k=o(k)",
            "eventual_RH348_membership": True,
        },
        "coefficient_identity": {
            "direct": "p_(k,j)=Y_(k,j)+P_(k,j)-S_(k,j)",
            "actual_remainder": "Y_(k,j)=T_(k,m)^rest-d_(sigma,k,2m)",
            "demand": "S_(k,j)=F_m^orb+A_(k,2m)",
            "target": "H_m=m*R^(-2m)",
        },
        "uniform_theorems": {
            "demand": "sup_j_abs(C_M*S/(2H_m*x^m)-1)->0",
            "parity": "sup_j_abs(C_M*P/(2H_m*x^m)-a_k*lambda^(2-j))->0",
            "actual_remainder_estimated": False,
        },
        "minimax_theorems": {
            "relative_formula": "(lambda^(J-2)-1)/(lambda^(J-2)+1)",
            "relative_rows": fixed_depths,
            "weighted_formula": "A_N=(1-x^(-N))/(x-1)-(1-(x*lambda)^(-N))/(x*lambda-1)",
            "weighted_optimizer": "a=1",
            "weighted_limit": "1/(x-1)-1/(x*lambda-1)>0",
            "weighted_rows": weighted,
        },
        "conditional_conclusion": {
            "actual_aggregate_hypothesis": "x^(-(k-2))*sum_j_abs(Y_(k,j))/(2H_m)->0",
            "hypothesis_proved": False,
            "normalized_law": "x^(-(k-2))*sum_j_W_(k,j)=F_(J_k-2)(a_k)/C_M+o(1)",
            "positive_liminf": "A_infinity/C_M",
            "stronger_sufficient_hypothesis": "max_j_abs(Y_(k,j))/H_m->0",
            "unconditional_conclusion": False,
        },
        "finite_rows": rows,
        "finite_fixture": {
            "phase": "weighted_optimum_a_k=1",
            "remainder": "Y_(k,j)=0",
            "depths": "finite_sqrt_k_style_diagnostics",
            "status": "formula_reproduction_only_not_actual_remainder_evidence",
        },
        "finite_rows_are_reproduction_checks_only": True,
        "route_boundary": {
            "growing_deterministic_uniformity": "PROVED",
            "conditional_selected_subprefix": "PROVED_under_named_actual_aggregate_hypothesis",
            "actual_remainder_control": "NOT_TESTABLE_open",
            "full_E_off": "NOT_TESTABLE_open",
            "next_route": "RH-351_ten_layer_signed_completion_frontier_review",
        },
        "false_claims": false_claims,
        "gates": {key: False for key in "ABCDE"},
        "source_anchors": [
            "RH-14_actual_square_root_parity_eigenvalue_law",
            "RH-17_boundary_multiplier_asymptotic",
            "RH-326_all_order_parity_quadratic_remainder",
            "RH-334_direct_coefficient_full_trace_distinction",
            "RH-336_exact_x_lambda_weight_dominance",
            "RH-348_simultaneous_lower_even_coefficient_ladder",
            "RH-349_fixed_two_sideband_phase_incompatibility",
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
