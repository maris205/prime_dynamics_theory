"""Build the deterministic RH-346 lower-sideband ledger."""

from __future__ import annotations

from decimal import Decimal
from fractions import Fraction
import json
from pathlib import Path
import sys


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from lower_sideband_orbit import (  # noqa: E402
    C_STAR_DIAGNOSTIC,
    R_H,
    R_TRACE,
    decimal_text,
    physical_constants,
    sideband_row,
    typed_ledger_fixture,
)


def _encode(value):
    if isinstance(value, Decimal):
        return decimal_text(value)
    if isinstance(value, Fraction):
        return f"{value.numerator}/{value.denominator}"
    if isinstance(value, tuple):
        return [_encode(item) for item in value]
    if isinstance(value, list):
        return [_encode(item) for item in value]
    if isinstance(value, dict):
        return {key: _encode(item) for key, item in value.items()}
    return value


def result_payload() -> dict[str, object]:
    constants = physical_constants()
    rows = [_encode(sideband_row(k)) for k in (3, 5, 9, 17, 33)]
    fixture = typed_ledger_fixture(
        raw_rest=Fraction(29, 7),
        parity=Fraction(11, 5),
        radial_sideband=Fraction(13, 9),
        full_atom=Fraction(17, 8),
        head_defect=Fraction(19, 12),
    )
    false_claims = {
        "actual_lower_compensation_proved": False,
        "actual_lower_nonclosure_proved": False,
        "actual_E_off_closed": False,
        "actual_head_transport_proved": False,
        "complete_lower_orbit_always_far": False,
        "determinant_gluing_activated": False,
        "finite_radial_sign_is_asymptotic_theorem": False,
        "finite_rows_are_asymptotic_evidence": False,
        "full_direct_prefix_closed": False,
        "hilbert_polya_constructed": False,
        "lower_orbit_free_rest_estimated": False,
        "radial_sideband_target_negligible_proved": False,
        "remaining_off_alias_background_closed": False,
        "rh288_activated": False,
        "riemann_hypothesis_proved": False,
        "riemann_zeros_identified": False,
        "same_m_clock_substituted_for_sigma_k_clock": False,
        "von_mangoldt_trace_proved": False,
        "zeta_divisor_equality": False,
    }
    return {
        "status": "rh346_complete_lower_sideband_boundary_orbit_decomposition",
        "verdict": "GO_SCOPED_exact_physical_lower_sideband_decomposition",
        "scope": "complete_period_2m_raw_atom_radial_sideband_and_necessary_compensation_not_E_off_verdict",
        "constants": {
            "r_H": f"{R_H.numerator}/{R_H.denominator}",
            "R": f"{R_TRACE.numerator}/{R_TRACE.denominator}",
            "C_star_source_decimal_diagnostic": decimal_text(C_STAR_DIAGNOSTIC),
            **_encode(constants),
            "decimal_status": "finite_diagnostics_not_interval_certificates",
        },
        "clock": {
            "physical_noise_clock": "k=log(1/sigma)/(2log(lambda))+O(1)",
            "lower_orbit_parameter": "m=k-1",
            "sideband_order": "n_minus=2m=2k-2",
            "new_noise_clock_at_m": False,
        },
        "complete_orbit": {
            "Gamma_m": "{abs(f^j(p_2m)):0<=j<2m}",
            "cardinality": "2m_distinct",
            "point_weight": "G_m=r_H^(-2m)/(1+abs(M_m))",
            "full_atom": "F_m^orb=2m*G_m",
            "signed_raw_atom": "-F_m^orb",
        },
        "cellwise_refinement": {
            "critical_point": "xi_m=h(p_2m)<b",
            "epsilon": "1_(xi_m in J_minus)=1_(q_b,m<=A)",
            "eventual_counts_Jminus_Jplus_F": "(epsilon_m,0,2m-epsilon_m)",
            "fixed_phase_limit_q_b": "sqrt(C_b)*lambda^(1-eta)/(2*u_c)",
            "threshold_equality_stabilization": "NOT_DETERMINED_by_available_o(1)",
        },
        "typed_identity": {
            "raw": "T_(sigma,2m)=T_(k,m)^rest-F_m^orb",
            "full_trace": "q_(sigma,k,2m)=T_rest+P_(sigma,2m)-A_(k,2m)-F_m^orb",
            "direct": "p_(sigma,k,2m)=T_rest+P_(sigma,2m)-d_(sigma,k,2m)-A_(k,2m)-F_m^orb",
            "direct_compensation": "T_rest+P-d=A_(k,2m)+F_m^orb+o(H_m)",
        },
        "scale_theorem": {
            "RH339_partial_atom": "D_m^orb=(2m-1)*G_m",
            "exact_full_over_partial": "2m/(2m-1)",
            "missing_point": "F_m^orb-D_m^orb=G_m",
            "missing_point_over_H": "(beta*R)^(2m)/(C_M*m)*(1+o(1))->infinity",
            "full_atom_asymptotic": "(2m/C_M)*beta^(2m)*(1+o(1))",
            "full_atom_over_H": "(2/C_M)*(beta*R)^(2m)*(1+o(1))->infinity",
        },
        "radial_sideband": {
            "exact": "A_(k,2m)=2*(beta^(2m)-beta_k^(2m))",
            "relative_to_full": "(C_M-1)/m+o(1/m)->0",
            "eventual_sign_source_locked": False,
            "target_negligibility_source_locked": False,
            "combined_demand_over_full_limit": "1",
            "combined_demand_eventually_positive": True,
        },
        "lower_parity_phase": {
            "P_(sigma,2m)_over_F_m_limit": "C_star*C_M*lambda^(eta-1)",
            "next_scalar_balance_phase": "eta_-=1-log(C_star*C_M)/log(lambda)",
            "compensation_decided": False,
        },
        "rational_ledger_fixture": _encode(fixture),
        "finite_rows": rows,
        "finite_rows_are_reproduction_checks_only": True,
        "route_boundary": {
            "lower_signed_compensation": "NOT_TESTABLE_open",
            "remaining_E_off": "NOT_TESTABLE_open",
            "next_route": "RH-347_lower_sideband_scalar_phase_obstruction_or_actual_compensation",
        },
        "false_claims": false_claims,
        "gates": {key: False for key in "ABCDE"},
        "source_anchors": [
            "RH-17_boundary_orbit_and_multiplier",
            "RH-326_all_order_radial_counterloop_sideband",
            "RH-327_same_sigma_phase_resolved_source_location",
            "RH-334_all_order_physical_raw_partition_and_direct_head_defect",
            "RH-339_mandatory_2m_minus_1_lower_far_atom",
            "RH-340_direct_lower_compensation_necessity",
            "RH-345_roadmap_to_complete_lower_decomposition",
        ],
    }


def main() -> None:
    output = ROOT / "results/result.json"
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(
        json.dumps(result_payload(), indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    print(output.relative_to(ROOT))


if __name__ == "__main__":
    main()
