"""Build the deterministic RH-345 scalar-phase ledger."""

from __future__ import annotations

from decimal import Decimal
import json
from pathlib import Path
import sys


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from double_alias_phase import (  # noqa: E402
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
    rows = [_encode(completion_row(k)) for k in (8, 16, 24, 32)]
    false_claims = {
        "actual_orbit_free_rest_negligible_proved": False,
        "actual_parity_eigenvalue_replaced": False,
        "actual_critical_closure_proved": False,
        "actual_critical_nonclosure_proved": False,
        "actual_D_4k_closed": False,
        "actual_head_transport_proved": False,
        "balance_phase_target_closure_proved": False,
        "determinant_gluing_activated": False,
        "finite_rows_are_asymptotic_evidence": False,
        "full_strict_prefix_closed": False,
        "hilbert_polya_constructed": False,
        "lower_sideband_closed": False,
        "off_alias_background_closed": False,
        "parity_scalar_sequences_are_noisy_operators": False,
        "physical_prefix_divergence_proved": False,
        "physical_prefix_vanishing_proved": False,
        "rh288_activated": False,
        "riemann_hypothesis_proved": False,
        "riemann_zeros_identified": False,
        "von_mangoldt_trace_proved": False,
        "zeta_divisor_equality": False,
    }
    return {
        "status": "rh345_double_alias_parity_phase_compensation_obstruction",
        "verdict": "GO_SCOPED_scalar_only_physical_conditional_obstruction_and_information_class_underdetermination",
        "scope": "critical_parity_scalar_mechanism_not_aggregate_physical_compensation_verdict",
        "constants": {
            "r_H": f"{R_H.numerator}/{R_H.denominator}",
            "R": f"{R_TRACE.numerator}/{R_TRACE.denominator}",
            "C_star_source_decimal_diagnostic": decimal_text(C_STAR_DIAGNOSTIC),
            "C_M_source_decimal_diagnostic": decimal_text(C_M_DIAGNOSTIC),
            "eta_two_diagnostic": decimal_text(balance_phase()),
            **_encode(constants),
            "decimal_status": "finite_diagnostics_not_interval_certificates",
        },
        "critical_identity": {
            "orbit_free_remainder": "Y_k=T_rest_k-d_(sigma,k,2k)",
            "positive_demand": "S_k=A_(k,2k)+F_orb_k",
            "direct": "p_(sigma,k,2k)=Y_k+P_(sigma,2k)-S_k",
            "S_over_A_limit": "2",
            "A_over_H_limit": "+infinity",
        },
        "phase_law": {
            "P_over_A": "C_star*C_M*lambda^(eta_sigma)*(1+o(1))",
            "P_over_S_limit_at_fixed_eta": "C_star*C_M*lambda^eta/2",
            "unique_double_alias_balance_phase": "eta_2=log(2/(C_star*C_M))/log(lambda)",
        },
        "conditional_physical_obstruction": {
            "hypothesis": "Y_k=o(H_k)_on_the_actual_physical_coefficient",
            "off_balance_condition": "liminf_abs(C_star*C_M*lambda^(eta_sigma)-2)>0",
            "conclusion": "abs(p_(sigma,k,2k))/(2H_k)->infinity",
            "aggregate_nonclosure_claimed": False,
        },
        "balance_phase_precision": {
            "necessary_scalar_match": "P_(sigma,2k)=S_k+o(H_k)",
            "relative_precision": "o(H_k/S_k)=o((beta*R)^(-2k))",
            "source_phase_law_precision": "relative_o(1)_only",
            "target_closure_decided": False,
        },
        "scalar_information_class": {
            "phase": "eta_2",
            "exact_parity_form": "P=r_H^(-2k)*(1-(1-delta_k)^(2k))",
            "close_choice": "P_close=S_k",
            "far_choice": "P_far=S_k+A_k/k",
            "both_square_root_law": "delta_k=C_star*sqrt(sigma_k)*(1+o(1))",
            "close_direct_residual": "0",
            "far_direct_residual": "A_k/k",
            "far_weighted_critical": "A_k/(2kH_k)->infinity",
            "actual_noisy_realization_claimed": False,
        },
        "finite_rows": rows,
        "finite_rows_are_reproduction_checks_only": True,
        "route_boundary": {
            "scalar_only_parity_mechanism": "STOP_SCOPED_off_balance_and_underdetermined_at_balance",
            "actual_critical_signed_compensation": "NOT_TESTABLE_open",
            "next_route": "RH-346_lower_sideband_complete_physical_decomposition",
        },
        "false_claims": false_claims,
        "gates": {key: False for key in "ABCDE"},
        "source_anchors": [
            "RH-14_actual_square_root_parity_eigenvalue_law",
            "RH-326_actual_first_alias_parity_phase_law",
            "RH-340_nonnegative_critical_prefix_extraction",
            "RH-344_complete_orbit_atom_and_double_alias_demand",
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
