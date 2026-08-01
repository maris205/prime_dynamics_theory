"""Build the deterministic RH-338 far-atom result ledger."""

from __future__ import annotations

from decimal import Decimal
import json
from pathlib import Path
import sys


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from far_atom import (  # noqa: E402
    R_H,
    R_TRACE,
    certified_far_count,
    decimal_text,
    diagnostic_row,
    fixed_gap_diagnostics,
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
    gaps = fixed_gap_diagnostics()
    rows = [_encode(diagnostic_row(k)) for k in (2, 4, 8, 16, 32)]
    false_claims = {
        "aggregate_far_nonvanishing_proved": False,
        "aggregate_far_o_H_k_proved": False,
        "actual_model_Delta_R_typed": False,
        "determinant_gluing_activated": False,
        "full_trace_divergence_proved": False,
        "full_trace_replacement_proved": False,
        "head_counterloop_transport_proved": False,
        "hilbert_polya_constructed": False,
        "off_alias_background_closed": False,
        "Omega_canonical_physical_window_proved": False,
        "physical_parity_alias_replacement_closed": False,
        "rest_compensation_estimated": False,
        "rh330_transfer_activated": False,
        "riemann_hypothesis_proved": False,
        "riemann_zeros_identified": False,
        "separate_absolute_far_majorant_closes": False,
        "von_mangoldt_trace_proved": False,
        "zeta_divisor_equality": False,
    }
    return {
        "status": "rh338_boundary_orbit_far_atom_and_signed_diffuse_compensation_obstruction",
        "scope": "actual_physical_far_orbit_atom_subledger_not_aggregate_far_verdict",
        "constants": {
            "r_H": f"{R_H.numerator}/{R_H.denominator}",
            "R": f"{R_TRACE.numerator}/{R_TRACE.denominator}",
            **_encode(constants),
            "status": "high_precision_diagnostics_except_exact_rational_radii",
        },
        "analytic_containment": {
            "windows": "J_minus=[0,1] intersect [b-A*sqrt(sigma),b), J_plus=[0,1] intersect [b,b+A*sqrt(sigma)]",
            "far_set": "F=[0,1]\\(J_minus union J_plus)",
            "excluded_marked_index": "2k-2",
            "Omega_cardinality": "2k-1",
            "Omega_subset_F_eventually": True,
            "odd_folded_points_bound": "abs(f^(2j+1)(p_2k))<=r<b",
            "interior_even_bound": "h^m(p_2k)<=h(b)<b for m>=2",
            "endpoint_bound": "p_2k>=p_2>b by a fixed gap",
            "fixed_gap_diagnostics": _encode(gaps),
        },
        "far_atom_theorem": {
            "noisy_localized_trace_on_Omega": "0_exactly_because_M_Omega=0_on_L2",
            "deterministic_mass": "D_orb=r_H^(-2k)*(2k-1)/(1+abs(M_k))",
            "signed_atom": "R_orb=-D_orb",
            "D_orb_asymptotic": "(2k/C_M)*beta^(2k)*(1+o(1))",
            "D_orb_over_alias_limit": "1",
            "D_orb_over_H_limit": "+infinity",
            "certified_far_counts": {str(k): certified_far_count(k) for k in (2, 4, 8, 16, 32)},
        },
        "signed_compensation_barrier": {
            "decomposition": "R_k=R_orb_k+R_rest_k",
            "necessary_condition_for_R_o_H": "R_rest_k=D_orb_k+o(H_k)",
            "required_relative_precision": "o(H_k/D_orb_k)=o((beta*R)^(-2k))",
            "separate_absolute_atom_rest_bound_sufficient": False,
            "aggregate_verdict": "NOT_TESTABLE_without_moving_order_R_rest_estimate",
        },
        "finite_rows": rows,
        "finite_rows_are_reproduction_checks_only": True,
        "false_claims": false_claims,
        "gates": {key: False for key in "ABCDE"},
        "source_anchors": [
            "RH-10_primitive_boundary_orbit",
            "RH-17_ordered_boundary_chain_fixed_gaps_and_multiplier_law",
            "RH-19_missing_bulk_resolvent_control",
            "RH-326_first_alias_packet_and_multiplier_asymptotic",
            "RH-330_aggregated_signed_far_firewall",
            "RH-334_frozen_physical_far_slot_and_multiplier_preserving_fold",
            "RH-336_exact_beta_R_greater_than_one_certificate",
            "RH-337_wrong_clock_comparator_excluded",
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
