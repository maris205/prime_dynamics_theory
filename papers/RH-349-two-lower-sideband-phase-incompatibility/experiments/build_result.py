"""Build the deterministic RH-349 two-sideband ledger."""

from __future__ import annotations

from decimal import Decimal
import json
from pathlib import Path
import sys


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from two_sideband_phase import (  # noqa: E402
    C_M_DIAGNOSTIC,
    C_STAR_DIAGNOSTIC,
    R_H,
    R_TRACE,
    balance_phase_j2,
    decimal_text,
    minimax_ledger,
    physical_constants,
    two_sideband_row,
)


def _encode(value):
    if isinstance(value, Decimal):
        return decimal_text(value)
    if isinstance(value, tuple):
        return [_encode(item) for item in value]
    if isinstance(value, list):
        return [_encode(item) for item in value]
    if isinstance(value, dict):
        return {key: _encode(item) for key, item in value.items()}
    return value


def result_payload() -> dict[str, object]:
    constants = physical_constants()
    minimax = minimax_ledger()
    rows = [_encode(two_sideband_row(k)) for k in (10, 18, 30, 46)]
    false_claims = {
        "actual_Y_2_negligible_proved": False,
        "actual_Y_3_negligible_proved": False,
        "actual_two_sideband_hypotheses_verified_numerically": False,
        "unconditional_two_sideband_nonclosure_proved": False,
        "unconditional_physical_prefix_nonclosure_proved": False,
        "actual_E_off_closed": False,
        "actual_E_off_nonclosure_proved": False,
        "growing_depth_uniformity_proved": False,
        "odd_orders_controlled": False,
        "upper_alias_orders_controlled": False,
        "finite_rows_are_asymptotic_evidence": False,
        "finite_rows_are_operator_observations": False,
        "determinant_gluing_activated": False,
        "full_direct_prefix_closed": False,
        "hilbert_polya_constructed": False,
        "rh288_activated": False,
        "riemann_hypothesis_proved": False,
        "riemann_zeros_identified": False,
        "von_mangoldt_trace_proved": False,
        "zeta_divisor_equality": False,
    }
    return {
        "status": "rh349_two_lower_sideband_phase_incompatibility",
        "verdict": "GO_SCOPED_fixed_two_sideband_conditional_phase_obstruction",
        "scope": "fixed_j_2_3_direct_coefficients_under_two_unproved_actual_remainder_hypotheses",
        "constants": {
            "r_H": f"{R_H.numerator}/{R_H.denominator}",
            "R": f"{R_TRACE.numerator}/{R_TRACE.denominator}",
            "C_star_source_decimal_diagnostic": decimal_text(
                C_STAR_DIAGNOSTIC
            ),
            "C_M_source_decimal_diagnostic": decimal_text(C_M_DIAGNOSTIC),
            "eta_j2_balance_diagnostic": decimal_text(balance_phase_j2()),
            **_encode(constants),
            "decimal_status": "finite_diagnostics_not_interval_certificates",
        },
        "index_family": {
            "physical_noise_clock": "k=log(1/sigma)/(2log(lambda))+O(1)",
            "phase": "eta_sigma=k-log(1/sigma)/(2log(lambda))->eta",
            "sidebands": "m_j=k-j_for_j_in_{2,3}",
            "orders": "n_j=2m_j",
            "both_orders_are_punctured_lower_even": True,
        },
        "coefficient_identity": {
            "direct": "p_j=Y_j+P_j-S_j",
            "actual_remainder": "Y_j=T_(k,m_j)^rest-d_(sigma,k,2m_j)",
            "demand": "S_j=F_(m_j)^orb+A_(k,2m_j)",
            "demand_scale": "S_j=(2m_j/C_M)*beta^(2m_j)*(1+o(1))",
            "target": "H_(m_j)=m_j*R^(-2m_j)",
        },
        "fixed_phase_law": {
            "gamma_j": "C_star*C_M*lambda^(eta-j)",
            "gamma_3_over_gamma_2": "1/lambda",
            "a": "gamma_2>0",
            "actual_hypotheses": [
                "Y_2=o(H_(m_2))",
                "Y_3=o(H_(m_3))",
            ],
            "hypotheses_proved": False,
            "coordinate_limit": "W_j/x^(m_j)->abs(gamma_j-1)/C_M",
        },
        "minimax_theorems": {
            "relative": "inf_(a>0)max(abs(a-1),abs(a/lambda-1))=(lambda-1)/(lambda+1)",
            "relative_optimizer": "2lambda/(lambda+1)",
            "weighted": "inf_(a>0)(x*abs(a-1)+abs(a/lambda-1))=1-1/lambda",
            "weighted_optimizer": "1",
            "diagnostic_values": _encode(minimax),
        },
        "conditional_conclusion": {
            "two_order_subprefix": "W_2+W_3",
            "normalized_limit": "(x*abs(a-1)+abs(a/lambda-1))/C_M>0",
            "normalization": "x^(k-3)",
            "diverges_exponentially_under_both_actual_hypotheses": True,
            "bounded_phase_liminf": ">=(1-1/lambda)/C_M_under_the_same_two_hypotheses",
            "unconditional_conclusion": False,
        },
        "finite_rows": rows,
        "finite_fixture": {
            "phase": "weighted_optimum_a=1",
            "remainder": "Y_2=Y_3=0",
            "scaled_limit": "C_M*(W_2+W_3)/x^(k-3)->1-1/lambda",
            "status": "formula_reproduction_only_not_actual_remainder_evidence",
        },
        "finite_rows_are_reproduction_checks_only": True,
        "route_boundary": {
            "fixed_two_sideband_law": "PROVED_conditional_on_two_named_actual_remainders",
            "actual_remainder_control": "NOT_TESTABLE_open",
            "full_E_off": "NOT_TESTABLE_open",
            "next_route": "RH-350_fixed_or_slowly_growing_depth_minimax_audit",
        },
        "false_claims": false_claims,
        "gates": {key: False for key in "ABCDE"},
        "source_anchors": [
            "RH-14_actual_square_root_parity_eigenvalue_law",
            "RH-17_boundary_multiplier_asymptotic",
            "RH-326_exact_even_parity_packet_and_uniform_quadratic_remainder",
            "RH-334_direct_coefficient_and_deterministic_numerator_anchor",
            "RH-336_beta_R_superunit_certificate",
            "RH-346_fixed_lower_sideband_phase_interface",
            "RH-347_actual_remainder_hypothesis_firewall",
            "RH-348_simultaneous_punctured_lower_even_coefficient_ladder",
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
