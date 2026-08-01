"""Build the deterministic RH-340 synchronization ledger."""

from __future__ import annotations

from decimal import Decimal
import json
from pathlib import Path
import sys


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from prefix_sync import (  # noqa: E402
    R_H,
    R_TRACE,
    U_RADIUS,
    decimal_text,
    physical_constants,
    synchronization_diagnostic,
    tail_exponents,
)


def _encode(value):
    if isinstance(value, Decimal):
        return decimal_text(value)
    if isinstance(value, (list, tuple)):
        return [_encode(item) for item in value]
    if isinstance(value, dict):
        return {key: _encode(item) for key, item in value.items()}
    return value


def result_payload() -> dict[str, object]:
    false_claims = {
        "aggregate_prefix_nonvanishing_proved": False,
        "aggregate_prefix_vanishing_proved": False,
        "determinant_gluing_activated": False,
        "diffuse_critical_compensation_estimated": False,
        "diffuse_lower_sideband_compensation_estimated": False,
        "full_trace_divergence_proved": False,
        "full_trace_replacement_proved": False,
        "head_counterloop_budget_closed": False,
        "hilbert_polya_constructed": False,
        "off_alias_background_closed": False,
        "physical_parity_alias_replacement_closed": False,
        "rh288_activated": False,
        "riemann_hypothesis_proved": False,
        "riemann_zeros_identified": False,
        "separate_absolute_two_atom_route_closes": False,
        "von_mangoldt_trace_proved": False,
        "zeta_divisor_equality": False,
    }
    exponents = tail_exponents()
    return {
        "status": "rh340_synchronized_determinant_prefix_and_two_order_orbit_head_compensation_obstruction",
        "scope": "same_clock_prefix_equivalence_and_two_order_compensation_necessity_not_gluing_verdict",
        "constants": {
            "r_H": f"{R_H.numerator}/{R_H.denominator}",
            "R": f"{R_TRACE.numerator}/{R_TRACE.denominator}",
            "U=R/r_H": f"{U_RADIUS.numerator}/{U_RADIUS.denominator}",
            **_encode(physical_constants()),
            "tail_exponents": _encode(exponents),
            "printed_C_M_is_diagnostic_only": True,
        },
        "common_cut": {
            "cut": "u=4k",
            "one_alias_window": "2k<u<=4k",
            "tail_clock_is_rederived_from_mass_bound": True,
            "noisy_tail_vanishes": True,
            "target_tail_vanishes": True,
        },
        "prefix_identity": {
            "p_n": "tau_(sigma,n)-a_n=q_(sigma,k,n)-d_(sigma,k,n)",
            "P_u": "sum_(2<=n<u)|p_n|R^n/n",
            "E_u": "sum_(2<=n<u)|q_n|R^n/n",
            "D_u": "sum_(2<=n<u)|d_n|R^n/n",
            "sharp_bound": "abs(P_u-E_u)<=D_u",
            "conditional_equivalence": "D_u->0 implies (P_u->0 iff E_u->0)",
        },
        "three_budget_equivalence": {
            "critical_order": "2k",
            "off_alias": "E_off excludes n=2k",
            "same_clock_condition": "D_u->0, E_off->0, q_(sigma,k,2k)=o(H_k)",
            "rh288_status": "OPEN_not_activated",
        },
        "two_order_atoms": {
            "critical_order": "2k",
            "lower_order": "2k-2",
            "critical_atom": "D_k^orb",
            "lower_atom": "D_(k-1)^orb",
            "critical_compensation": "C_k^0-d_(sigma,k,2k)=D_k^orb+o(H_k)",
            "lower_compensation": "C_k^--d_(sigma,k,2k-2)=D_(k-1)^orb+o(H_(k-1))",
            "critical_relative_precision": "o((beta*R)^(-2k))",
            "lower_relative_precision": "o((beta*R)^(-2(k-1)))",
            "separate_absolute_majorant": "(D_k^orb/(2H_k))+(D_(k-1)^orb/(2H_(k-1))) -> +infinity",
        },
        "finite_rows": [_encode(synchronization_diagnostic(k)) for k in (3, 5, 9, 17, 33)],
        "finite_rows_are_reproduction_checks_only": True,
        "false_claims": false_claims,
        "gates": {key: False for key in "ABCDE"},
        "source_anchors": [
            "RH-262_exact_target_radius_ratio_28_over_17_less_than_lambda",
            "RH-267_all_order_deterministic_envelope",
            "RH-282_mass_and_cap_tail_bound",
            "RH-288_prefix_tail_gluing_criterion",
            "RH-330_one_alias_critical_extraction",
            "RH-334_full_trace_to_modulus_complement_head_identity",
            "RH-336_lambda_less_than_17_over_10_and_beta_R_greater_than_one",
            "RH-338_critical_boundary_orbit_atom",
            "RH-339_lower_sideband_orbit_atom",
        ],
    }


def main() -> None:
    output = ROOT / "results" / "result.json"
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(result_payload(), indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(output.relative_to(ROOT))


if __name__ == "__main__":
    main()
