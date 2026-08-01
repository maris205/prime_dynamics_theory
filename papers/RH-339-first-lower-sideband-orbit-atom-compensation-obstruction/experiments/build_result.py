"""Build the deterministic RH-339 sideband compensation ledger."""

from __future__ import annotations

from decimal import Decimal
import json
from pathlib import Path
import sys


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from sideband_atom import (  # noqa: E402
    R_H,
    R_TRACE,
    decimal_text,
    physical_constants,
    sideband_diagnostic,
    sideband_in_one_alias_cut,
    sideband_order,
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
    rows = [_encode(sideband_diagnostic(k)) for k in (3, 5, 9, 17, 33)]
    false_claims = {
        "E_off_nonvanishing_proved": False,
        "E_off_to_zero_proved": False,
        "aggregate_sideband_coefficient_lower_bound_proved": False,
        "determinant_gluing_activated": False,
        "diffuse_sideband_compensation_estimated": False,
        "full_trace_divergence_proved": False,
        "full_trace_replacement_proved": False,
        "head_counterloop_transport_proved": False,
        "hilbert_polya_constructed": False,
        "off_alias_background_closed": False,
        "physical_parity_alias_replacement_closed": False,
        "rh330_transfer_activated": False,
        "riemann_hypothesis_proved": False,
        "riemann_zeros_identified": False,
        "separate_absolute_sideband_route_closes": False,
        "von_mangoldt_trace_proved": False,
        "zeta_divisor_equality": False,
    }
    return {
        "status": "rh339_first_lower_sideband_orbit_atom_compensation_obstruction",
        "scope": "necessary_signed_compensation_at_n_equals_2k_minus_2_not_E_off_verdict",
        "constants": {
            "r_H": f"{R_H.numerator}/{R_H.denominator}",
            "R": f"{R_TRACE.numerator}/{R_TRACE.denominator}",
            **_encode(physical_constants()),
            "status": "high_precision_diagnostics_except_exact_rational_radii",
        },
        "cut_lemma": {
            "one_alias_cut": "2k<h<=4k",
            "mandatory_sideband": "n_minus=2k-2",
            "included_for_every_admissible_cut": all(
                sideband_in_one_alias_cut(k, 2 * k + 1) for k in (3, 5, 9, 17, 33)
            ),
            "weighted_term": "abs(q_minus)*R^(2k-2)/(2k-2)=abs(q_minus)/(2H_(k-1))",
        },
        "physical_orbit_atom": {
            "orbit": "primitive boundary orbit p_(2(k-1))",
            "far_subset_cardinality": "2k-3",
            "signed_atom": "R_orb_minus=-D_(k-1)_orb",
            "atom_mass": "D_(k-1)_orb=r_H^(-2(k-1))*(2k-3)/(1+abs(M_(k-1)))",
            "atom_over_H_(k-1)_limit": "+infinity",
            "absolute_weighted_atom_limit": "+infinity",
        },
        "necessary_compensation": {
            "typed_coefficient": "q_minus=q_(sigma,k,2k-2)=-D_(k-1)_orb+C_minus",
            "E_off_to_zero_implies": "C_minus=D_(k-1)_orb+o(H_(k-1))",
            "required_relative_precision": "o((beta*R)^(-2(k-1)))",
            "aggregate_verdict": "NOT_TESTABLE_without_signed_C_minus_estimate",
            "separate_absolute_atom_complement_bound_sufficient": False,
        },
        "counterloop_sideband_identity": {
            "A_(k,2k-2)": "2*(beta^(2k-2)-beta_k^(2k-2))",
            "sign_claimed_from_current_sources": False,
            "reason": "source_proves_only_C_M_positive_and_rounded_decimal_is_not_interval_certificate",
        },
        "finite_rows": rows,
        "finite_rows_are_reproduction_checks_only": True,
        "false_claims": false_claims,
        "gates": {key: False for key in "ABCDE"},
        "source_anchors": [
            "RH-17_boundary_orbit_ordering_fixed_gaps_and_multiplier",
            "RH-19_missing_bulk_resolvent_control",
            "RH-326_general_counterloop_defect_and_first_alias_normalization",
            "RH-330_off_alias_prefix_definition_and_nonnegative_extraction",
            "RH-334_general_full_trace_constituent_and_corrected_far_partition",
            "RH-336_exact_beta_R_greater_than_one",
            "RH-338_physical_far_orbit_atom_method",
        ],
    }


def main() -> None:
    output = ROOT / "results" / "result.json"
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(result_payload(), indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(output.relative_to(ROOT))


if __name__ == "__main__":
    main()
