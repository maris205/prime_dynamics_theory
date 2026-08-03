"""Build the deterministic RH-348 punctured ladder ledger."""

from __future__ import annotations

from decimal import Decimal
from fractions import Fraction
import json
from pathlib import Path
import sys


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from lower_even_ladder import (  # noqa: E402
    C_M_DIAGNOSTIC,
    R_H,
    R_TRACE,
    decimal_text,
    ladder_row,
    physical_constants,
    typed_compensation_fixture,
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
    rows = [_encode(ladder_row(k)) for k in (8, 12, 16, 20)]
    fixture = typed_compensation_fixture(
        demands=(Fraction(3, 2), Fraction(5, 3), Fraction(7, 4)),
        supplies=(Fraction(3, 2), Fraction(5, 3), Fraction(9, 4)),
    )
    false_claims = {
        "actual_punctured_prefix_closed": False,
        "actual_punctured_prefix_nonclosure_proved": False,
        "actual_signed_supply_estimated": False,
        "actual_lower_remainders_negligible_proved": False,
        "all_off_alias_orders_controlled": False,
        "odd_orders_controlled": False,
        "orders_above_first_alias_controlled": False,
        "absolute_demand_is_residual_lower_bound": False,
        "radial_sign_source_locked": False,
        "finite_rows_are_asymptotic_evidence": False,
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
        "status": "rh348_punctured_lower_even_boundary_orbit_ladder",
        "verdict": "GO_SCOPED_exact_punctured_lower_even_orbit_ladder_and_aggregate_compensation_demand",
        "scope": "lower_even_punctured_subprefix_not_full_E_off_closure_or_nonclosure",
        "constants": {
            "r_H": f"{R_H.numerator}/{R_H.denominator}",
            "R": f"{R_TRACE.numerator}/{R_TRACE.denominator}",
            "C_M_source_decimal_diagnostic": decimal_text(C_M_DIAGNOSTIC),
            **_encode(constants),
            "decimal_status": "finite_diagnostics_not_interval_certificates",
        },
        "index_set": {
            "physical_noise_clock": "k=log(1/sigma)/(2log(lambda))+O(1)",
            "punctured_lower_even_orders": "n=2m_with_m_star<=m<=k-2",
            "excluded_selected_orders": "2k_and_2k-2",
            "orders_are_in_strict_one_alias_prefix": True,
        },
        "coefficient_ladder": {
            "full_orbit": "F_m^orb=2m*G_m",
            "point_weight": "G_m=r_H^(-2m)/(1+abs(M_m))",
            "full_trace": "q_(sigma,k,2m)=T_(k,m)^rest+P_(sigma,2m)-A_(k,2m)-F_m^orb",
            "direct": "p_(sigma,k,2m)=Y_(k,m)+P_(sigma,2m)-S_(k,m)",
            "Y": "Y_(k,m)=T_(k,m)^rest-d_(sigma,k,2m)",
            "S": "S_(k,m)=F_m^orb+A_(k,2m)",
        },
        "aggregate_theorem": {
            "x": "x=(beta*R)^2>1",
            "orbit_ladder": "L_k^orb=sum_(m_star<=m<=k-2) G_m*R^(2m)",
            "orbit_asymptotic": "x^(k-1)/(C_M*(x-1))*(1+o(1))",
            "absolute_radial_over_orbit": "O(1/k)->0",
            "absolute_combined_demand_over_orbit": "1+o(1)",
            "combined_demand_diverges": True,
        },
        "necessary_compensation": {
            "residual_subprefix": "sum abs(p_(sigma,k,2m))*R^(2m)/(2m)",
            "supply": "Z_(k,m)=Y_(k,m)+P_(sigma,2m)",
            "demand": "S_(k,m)",
            "reverse_triangle": "sum_abs_Z>=sum_abs_S-residual_subprefix",
            "closure_requires_supply_mass_asymptotic_at_least_orbit_ladder": True,
            "actual_supply_bound_available": False,
        },
        "rational_compensation_fixture": _encode(fixture),
        "finite_rows": rows,
        "finite_rows_are_reproduction_checks_only": True,
        "route_boundary": {
            "lower_even_punctured_demand": "PROVED_exact_and_asymptotic",
            "actual_signed_compensation": "NOT_TESTABLE_open",
            "remaining_E_off": "NOT_TESTABLE_open",
            "next_route": "RH-349_two_lower_sideband_phase_incompatibility",
        },
        "false_claims": false_claims,
        "gates": {key: False for key in "ABCDE"},
        "source_anchors": [
            "RH-17_boundary_orbit_multiplier_and_fixed_gap_chain",
            "RH-326_all_order_radial_counterloop_identity",
            "RH-334_all_order_physical_five_slot_coefficient",
            "RH-336_beta_R_superunit_certificate",
            "RH-340_punctured_prefix_data_type",
            "RH-346_complete_single_lower_orbit_extraction",
            "RH-347_roadmap_to_punctured_aggregate",
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
