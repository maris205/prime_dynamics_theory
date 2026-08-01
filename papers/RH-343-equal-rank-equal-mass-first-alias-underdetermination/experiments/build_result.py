"""Build the deterministic RH-343 information-class ledger."""

from __future__ import annotations

from decimal import Decimal
from fractions import Fraction
import json
from pathlib import Path
import sys


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from first_alias_underdetermination import (  # noqa: E402
    A_RADIUS,
    BETA_LIMIT,
    B_RADIUS,
    C_RADIUS_SQUARED,
    Q_HEAD,
    R_H,
    R_TRACE,
    decimal_text,
    finite_diagnostic,
    genus_one_quotient_factor,
    radius_order_certificate,
)


def _encode(value):
    if isinstance(value, Decimal):
        return decimal_text(value)
    if isinstance(value, Fraction):
        return f"{value.numerator}/{value.denominator}"
    if isinstance(value, (list, tuple)):
        return [_encode(item) for item in value]
    if isinstance(value, dict):
        return {key: _encode(item) for key, item in value.items()}
    return value


def result_payload() -> dict[str, object]:
    radii = radius_order_certificate()
    false_claims = {
        "actual_D_4k_divergence_proved": False,
        "actual_D_4k_vanishing_proved": False,
        "actual_head_rank_mismatch_proved": False,
        "actual_head_transport_proved": False,
        "actual_noisy_operator_realized": False,
        "determinant_gluing_activated": False,
        "direct_annular_route_closed": False,
        "future_transport_theorems_refuted": False,
        "hilbert_polya_constructed": False,
        "model_spectra_identified_with_K_sigma": False,
        "physical_rank_cap_6k_minus_2_proved": False,
        "physical_rank_or_mass_saturated": False,
        "physical_rank_mismatch_proved": False,
        "p_prefix_equivalent_to_q_prefix": False,
        "rh288_activated": False,
        "riemann_hypothesis_proved": False,
        "riemann_zeros_identified": False,
        "von_mangoldt_trace_proved": False,
        "zeta_divisor_equality": False,
    }
    return {
        "status": "rh343_equal_rank_equal_mass_first_alias_underdetermination",
        "verdict": "GO_SCOPED_finite_normal_spectral_information_class",
        "scope": "exact_equal_invariant_first_alias_underdetermination_not_actual_noisy_operator_transport",
        "constants": {
            "q": _encode(Q_HEAD),
            "r_H": _encode(R_H),
            "R": _encode(R_TRACE),
            "a": _encode(A_RADIUS),
            "b": _encode(B_RADIUS),
            "c_squared": _encode(C_RADIUS_SQUARED),
            "beta_limit_source_decimal": decimal_text(BETA_LIMIT),
            "radius_order_certificate": _encode(radii),
        },
        "construction": {
            "full_shell": "U_L(r)={r exp(2pi i j/L):0<=j<L}",
            "shell_moment": "p_n(U_L(r))=L r^n 1_(L|n)",
            "base": "Y_k_RH342_counterloop_rank_2k_minus_2",
            "invisible": "X_k^inv=Y_k_disjoint_union_U_(4k)(c)",
            "visible": "X_k^vis=Y_k_disjoint_union_U_(2k)(a)_disjoint_union_U_(2k)(b)",
            "model_spectra_only": True,
        },
        "rank_and_mass": {
            "common_rank": "6k-2",
            "common_squared_spectral_mass": "(2k-2)beta_k^2+481k/200",
            "shell_mass_identity": "4k c^2=2k(a^2+b^2)=481k/200",
            "conjugation_closed": True,
            "eventually_simple": True,
            "eventual_radius_order": "q<a<c<b<beta_k<1/r_H",
            "common_maximum_modulus": "beta_k",
            "finite_normal_diagonal_realization": True,
            "diagonal_Hilbert_Schmidt_mass_equals_squared_spectral_mass": True,
        },
        "clock_and_coarse_compatibility": {
            "clock": "k=log(1/sigma)/(2log(lambda))+O(1)",
            "rank_scale": "O(k)=O(log(1/sigma))=o(1/sigma)",
            "squared_mass_scale": "O(k)=O(log(1/sigma))=o(1/sigma)",
            "RH282_coarse_rank_ceiling": "4/sigma",
            "RH282_coarse_squared_mass_ceiling": "1/sigma",
            "compatible_only_not_realized": True,
        },
        "moment_ledger": {
            "both_equal_Y": "2<=n<2k",
            "all_fixed_orders_eventually_equal_Y": True,
            "not_equal_on_entire_strict_prefix": True,
            "first_split_order": "n=2k",
            "invisible_difference_at_2k": "0",
            "visible_difference_at_2k": "2k(a^(2k)+b^(2k))",
            "strict_endpoint": "2<=n<4k",
        },
        "weighted_budget": {
            "definition": "D_m(X,Y)=sum_(2<=n<m)|p_n(X)-p_n(Y)|R^n/n",
            "invisible_D_4k": "0_exactly",
            "visible_D_4k": "(21/20)^(2k)+(28/25)^(2k)",
            "visible_D_4k_diverges": True,
            "one_over_n_cancellation_retained": True,
        },
        "genus_one_quotients": {
            "invisible": genus_one_quotient_factor("invisible"),
            "visible": genus_one_quotient_factor("visible"),
        },
        "underdetermination_corollary": {
            "equal_data": [
                "rank",
                "squared_spectral_mass",
                "common_cap_and_maximum_modulus",
                "simple_conjugation_closed_normal_realizability",
                "all_pre_alias_moments",
                "every_fixed_order_eventually",
            ],
            "data_do_not_determine": "moving_strict_prefix_D_4k",
            "future_actual_rank_cap_2k_minus_2_excludes_both_examples": True,
        },
        "route_boundary": {
            "actual_alias_inclusive_head_transport": "NOT_TESTABLE_open",
            "equal_rank_mass_fixed_order_inference": "STOP_SCOPED_without_sharper_actual_rank_or_moving_order_physical_input",
            "determinant_gluing": "OPEN_not_activated",
        },
        "finite_rows": [_encode(finite_diagnostic(k)) for k in (3, 5, 9, 17)],
        "finite_rows_are_exact_reproduction_checks_only": True,
        "false_claims": false_claims,
        "gates": {key: False for key in "ABCDE"},
        "source_anchors": [
            "RH_HANDOFF_sections_3_5_6",
            "RH-272_counterloop_radius_limit",
            "RH-282_coarse_rank_and_squared_mass_ceilings",
            "RH-289_complete_shell_moment_and_genus_one_identity",
            "RH-299_weighted_D_m_normalization",
            "RH-303_fixed_order_head_transport_necessity",
            "RH-342_common_Hardy_counterloop_and_rank_lock",
        ],
    }


def main() -> None:
    output = ROOT / "results" / "result.json"
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(
        json.dumps(result_payload(), indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )
    print(output.relative_to(ROOT))


if __name__ == "__main__":
    main()
