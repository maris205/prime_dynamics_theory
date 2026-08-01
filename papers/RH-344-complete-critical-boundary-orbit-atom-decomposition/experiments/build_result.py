"""Build the deterministic RH-344 complete-orbit ledger."""

from __future__ import annotations

from decimal import Decimal
from fractions import Fraction
import json
from pathlib import Path
import sys


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from critical_orbit_atom import (  # noqa: E402
    R_H,
    R_TRACE,
    complete_orbit_row,
    decimal_text,
    ledger_fixture,
    physical_constants,
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
    rows = [_encode(complete_orbit_row(k)) for k in (2, 4, 8, 16, 32)]
    fixture = ledger_fixture(
        raw_rest=Fraction(31, 7),
        parity=Fraction(13, 5),
        alias=Fraction(17, 6),
        full_atom=Fraction(19, 8),
        head_defect=Fraction(23, 11),
    )
    false_claims = {
        "actual_critical_compensation_proved": False,
        "actual_critical_nonclosure_proved": False,
        "actual_D_4k_closed": False,
        "actual_head_transport_proved": False,
        "aggregate_far_nonvanishing_proved": False,
        "complete_orbit_always_far": False,
        "determinant_gluing_activated": False,
        "finite_rows_are_asymptotic_evidence": False,
        "full_trace_prefix_closed": False,
        "hilbert_polya_constructed": False,
        "missing_point_target_negligible": False,
        "off_alias_background_closed": False,
        "orbit_free_rest_estimated": False,
        "parity_alone_proves_compensation": False,
        "physical_prefix_nonvanishing_proved": False,
        "physical_prefix_vanishing_proved": False,
        "rh288_activated": False,
        "riemann_hypothesis_proved": False,
        "riemann_zeros_identified": False,
        "von_mangoldt_trace_proved": False,
        "zeta_divisor_equality": False,
    }
    return {
        "status": "rh344_complete_critical_boundary_orbit_atom_decomposition",
        "verdict": "GO_SCOPED_exact_physical_raw_partition_decomposition",
        "scope": "complete_boundary_orbit_raw_atom_and_necessary_compensation_not_aggregate_verdict",
        "constants": {
            "r_H": f"{R_H.numerator}/{R_H.denominator}",
            "R": f"{R_TRACE.numerator}/{R_TRACE.denominator}",
            **_encode(constants),
            "decimal_status": "high_precision_diagnostics_except_exact_rational_radii",
        },
        "complete_orbit_theorem": {
            "folded_orbit": "Gamma_k={abs(f^j(p_k)):0<=j<2k}",
            "cardinality": "2k_distinct",
            "common_multiplier": "M_k=-C_M*lambda^k*(1+o(1))",
            "point_weight": "G_k=r_H^(-2k)/(1+abs(M_k))",
            "full_atom": "F_orb_k=2k*G_k",
            "signed_raw_atom": "-F_orb_k",
            "noisy_trace_on_finite_orbit": "0_exactly",
        },
        "cellwise_refinement": {
            "critical_point": "xi_k=h(p_k)<b",
            "epsilon": "1_(xi_k in J_minus)=1_(q_b<=A)",
            "eventual_counts_Jminus_Jplus_F": "(epsilon_k,0,2k-epsilon_k)",
            "B_decomposition": "B=B_rest-epsilon_k*G_k",
            "S_decomposition": "S=S_rest",
            "R_decomposition": "R=R_rest-(2k-epsilon_k)*G_k",
            "fixed_phase_limit_q_b": "sqrt(C_b)*lambda^(-eta)/(2*u_c)",
            "threshold_equality_stabilization": "NOT_DETERMINED_by_available_o(1)",
        },
        "typed_identity": {
            "raw": "T_sigma_2k=T_rest_k-F_orb_k",
            "full_trace": "q=T_rest+P_parity-A_alias-F_orb",
            "direct": "p=T_rest+P_parity-d_head-A_alias-F_orb",
            "critical_closure_requirement": "T_rest+P_parity-d_head=A_alias+F_orb+o(H_k)",
        },
        "scale_theorem": {
            "RH338_far_atom": "D_orb_k=(2k-1)*G_k",
            "exact_full_over_far": "2k/(2k-1)",
            "missing_point": "F_orb_k-D_orb_k=G_k",
            "missing_point_over_H": "(beta*R)^(2k)/(C_M*k)*(1+o(1))->infinity",
            "full_atom_asymptotic": "(2k/C_M)*beta^(2k)*(1+o(1))",
            "full_over_alias_limit": "1",
            "full_over_H": "(2/C_M)*(beta*R)^(2k)*(1+o(1))->infinity",
            "alias_plus_full": "(4k/C_M)*beta^(2k)*(1+o(1))",
            "alias_plus_full_over_alias_limit": "2",
            "full_equals_far_plus_o_H": False,
        },
        "exact_finite_k_relation": {
            "beta_k_power": "beta_k^(2k)=r_H^(-2k)/abs(M_k)",
            "full_atom": "2k*beta_k^(2k)*abs(M_k)/(1+abs(M_k))",
            "alias_minus_full": "2*(beta^(2k)-beta_k^(2k))+2k*beta_k^(2k)/(1+abs(M_k))",
            "sign_source_locked": False,
        },
        "rational_ledger_fixture": _encode(fixture),
        "finite_rows": rows,
        "finite_rows_are_reproduction_checks_only": True,
        "route_boundary": {
            "orbit_free_rest_minus_head_estimate": "NOT_TESTABLE_open",
            "critical_signed_compensation": "NOT_TESTABLE_open",
            "direct_prefix": "OPEN",
            "determinant_gluing": "OPEN_not_activated",
        },
        "false_claims": false_claims,
        "gates": {key: False for key in "ABCDE"},
        "source_anchors": [
            "RH-17_complete_primitive_boundary_orbit_and_multiplier",
            "RH-327_phase_resolved_critical_source_location",
            "RH-334_multiplier_preserving_fold_and_raw_partition",
            "RH-334_first_alias_typed_identity_and_head_defect",
            "RH-338_far_2k_minus_1_orbit_atom_and_scales",
            "RH-340_same_clock_prefix_and_critical_compensation",
            "RH-343_roadmap_to_complete_critical_decomposition",
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
