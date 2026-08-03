"""Build the deterministic RH-347 lower scalar-balance ledger."""

from __future__ import annotations

from decimal import Decimal
import json
from pathlib import Path
import sys


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from lower_sideband_balance import (  # noqa: E402
    C_M_DIAGNOSTIC,
    C_STAR_DIAGNOSTIC,
    R_H,
    R_TRACE,
    balance_phase,
    completion_row,
    decimal_text,
    physical_constants,
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
    rows = [_encode(completion_row(m)) for m in (8, 16, 24, 40)]
    false_claims = {
        "actual_lower_remainder_negligible_proved": False,
        "actual_lower_compensation_proved": False,
        "actual_lower_nonclosure_proved": False,
        "actual_parity_eigenvalue_replaced": False,
        "actual_noisy_operator_constructed_from_scalar_envelope": False,
        "actual_E_off_closed": False,
        "actual_head_transport_proved": False,
        "canonical_phase_excluded_by_decimal_diagnostic": False,
        "determinant_gluing_activated": False,
        "finite_rows_are_asymptotic_evidence": False,
        "full_direct_prefix_closed": False,
        "hilbert_polya_constructed": False,
        "punctured_off_alias_background_closed": False,
        "rh288_activated": False,
        "riemann_hypothesis_proved": False,
        "riemann_zeros_identified": False,
        "same_m_clock_substituted_for_sigma_k_clock": False,
        "von_mangoldt_trace_proved": False,
        "zeta_divisor_equality": False,
    }
    return {
        "status": "rh347_lower_sideband_scalar_balance_underdetermination",
        "verdict": "GO_SCOPED_conditional_physical_off_balance_obstruction_and_scalar_information_class_underdetermination",
        "scope": "lower_sideband_parity_scalar_mechanism_not_actual_signed_compensation_or_E_off_verdict",
        "constants": {
            "r_H": f"{R_H.numerator}/{R_H.denominator}",
            "R": f"{R_TRACE.numerator}/{R_TRACE.denominator}",
            "C_star_source_decimal_diagnostic": decimal_text(
                C_STAR_DIAGNOSTIC
            ),
            "C_M_source_decimal_diagnostic": decimal_text(C_M_DIAGNOSTIC),
            "eta_minus_diagnostic": decimal_text(balance_phase()),
            **_encode(constants),
            "decimal_status": "finite_diagnostics_not_interval_certificates",
        },
        "clock": {
            "physical_noise_clock": "k=log(1/sigma)/(2log(lambda))+O(1)",
            "lower_orbit_parameter": "m=k-1",
            "retained_relation": "k=m+1",
            "sideband_order": "n_minus=2m=2k-2",
            "inverse_root_exponent": "1/(2m)",
            "new_noise_clock_at_m": False,
        },
        "lower_identity": {
            "orbit_free_remainder": "Y_m^-=T_(k,m)^rest-d_(sigma,k,2m)",
            "combined_demand": "S_m^-=F_m^orb+A_(k,2m)",
            "direct": "p_(sigma,k,2m)=Y_m^-+P_(sigma,2m)-S_m^-",
            "F_m": "F_m^orb=2m*G_m",
            "G_m": "G_m=r_H^(-2m)/(1+abs(M_m))",
            "S_over_F_limit": "1",
        },
        "phase_law": {
            "P_over_S_at_fixed_eta": "C_star*C_M*lambda^(eta-1)",
            "unique_balance_phase": "eta_-=1-log(C_star*C_M)/log(lambda)",
            "balance_interface_novel_here": False,
            "decimal_excludes_canonical_window": False,
        },
        "conditional_physical_obstruction": {
            "hypothesis": "Y_m^-=o(H_m)_on_the_actual_physical_coefficient",
            "off_balance_condition": "eta!=eta_-",
            "weighted_conclusion": "abs(p)/(2H_m)->infinity",
            "exact_asymptotic_coefficient": "abs(C_star*C_M*lambda^(eta-1)-1)/C_M",
            "exponential_factor": "(beta*R)^(2m)",
            "aggregate_nonclosure_claimed": False,
        },
        "balance_phase_precision": {
            "necessary_scalar_match": "P_(sigma,2m)=S_m^-+o(H_m)",
            "relative_precision": "o(H_m/S_m^-)=o((beta*R)^(-2m))",
            "source_phase_law_precision": "relative_o(1)_only",
            "target_closure_decided": False,
        },
        "scalar_information_class": {
            "phase_clock": "sigma_m=lambda^(-2*(m+1-eta_-))",
            "exact_inverse_map": "delta_m(X)=1-(1-r_H^(2m)*X)^(1/(2m))",
            "legal_domain": "0<X<r_H^(-2m)",
            "close_choice": "P_close=S_m^-",
            "far_choice": "P_far=S_m^-+F_m^orb/m",
            "both_square_root_law": "delta_m=C_star*sqrt(sigma_m)*(1+o(1))",
            "close_direct_residual": "0",
            "far_direct_residual": "F_m^orb/m=2G_m",
            "far_weighted_lower": "G_m/H_m->infinity",
            "actual_noisy_realization_claimed": False,
        },
        "finite_rows": rows,
        "finite_rows_are_reproduction_checks_only": True,
        "route_boundary": {
            "lower_scalar_parity_mechanism": "STOP_SCOPED_off_balance_and_underdetermined_at_balance",
            "actual_lower_signed_compensation": "NOT_TESTABLE_open",
            "remaining_E_off": "NOT_TESTABLE_open",
            "next_route": "RH-348_punctured_one_alias_signed_aggregate",
        },
        "false_claims": false_claims,
        "gates": {key: False for key in "ABCDE"},
        "source_anchors": [
            "RH-14_actual_square_root_parity_eigenvalue_law",
            "RH-326_exact_even_parity_packet_and_phase_law",
            "RH-336_beta_R_superunit_certificate",
            "RH-340_nonnegative_lower_prefix_extraction",
            "RH-341_actual_first_alias_frontier_firewall",
            "RH-345_scalar_information_class_precedent_at_critical_order",
            "RH-346_exact_complete_lower_coefficient_and_shifted_phase_interface",
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
