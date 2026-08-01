"""Build the deterministic RH-337 clock-drift result ledger."""

from __future__ import annotations

from decimal import Decimal
from fractions import Fraction
import json
from pathlib import Path
import sys


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from clock_drift import (  # noqa: E402
    C_M_HAT,
    C_STAR_HAT,
    LAMBDA_HAT,
    R_H,
    R_TRACE,
    clock_diagnostics,
    exact_clock_certificate,
    fraction_text,
    model_packet_audit,
)


def _exact(value):
    if isinstance(value, Fraction):
        return fraction_text(value)
    if isinstance(value, Decimal):
        return format(value, "f")
    if isinstance(value, tuple):
        return [_exact(item) for item in value]
    if isinstance(value, list):
        return [_exact(item) for item in value]
    if isinstance(value, dict):
        return {key: _exact(item) for key, item in value.items()}
    return value


def result_payload() -> dict[str, object]:
    certificate = exact_clock_certificate()
    diagnostics = clock_diagnostics()
    finite_rows = [_exact(model_packet_audit(k)) for k in (2, 3, 4, 6)]

    false_claims = {
        "correct_physical_fixed_phase_replacement_proved": False,
        "determinant_gluing_activated": False,
        "far_remainder_o_H_k_proved": False,
        "full_trace_divergence_proved": False,
        "full_trace_replacement_proved": False,
        "head_counterloop_transport_proved": False,
        "hilbert_polya_constructed": False,
        "off_alias_background_closed": False,
        "physical_Delta_B_plus_Delta_S_closed": False,
        "physical_full_operator_counterexample_constructed": False,
        "physical_parity_alias_target_replacement_closed": False,
        "rh329_constants_are_physical_intervals": False,
        "rh329_fixed_eta_zero_is_physical_eta_zero": False,
        "rh330_fixed_phase_transfer_activated": False,
        "riemann_hypothesis_proved": False,
        "riemann_zeros_identified": False,
        "von_mangoldt_trace_proved": False,
        "zeta_divisor_equality": False,
    }

    return {
        "status": "rh337_algebraic_clock_drift_and_parity_alias_replacement_obstruction",
        "scope": "exact_RH329_wrong_clock_scalar_comparator_obstruction",
        "exact_clock_certificate": _exact(certificate),
        "hatted_model_constants": {
            "r_H": fraction_text(R_H),
            "R": fraction_text(R_TRACE),
            "Lambda_hat": fraction_text(LAMBDA_HAT),
            "C_M_hat": fraction_text(C_M_HAT),
            "C_star_hat": fraction_text(C_STAR_HAT),
            "status": "RH329_model_definitions_not_physical_intervals",
        },
        "clock_diagnostics": {
            **_exact(diagnostics),
            "certification_status": "high_precision_decimal_reproduction_only",
        },
        "off_phase_trichotomy": {
            "clock": "sigma_k=Lambda_c^(-2k), Lambda_c>1",
            "parity_law": "P_route=2k*C_star*r_H^(-2k)*Lambda_c^(-k)*(1+o(1))",
            "alias_law": "A_route=(2k/C_M)*r_H^(-2k)*lambda^(-k)*(1+o(1))",
            "ratio_law": "P_route/A_route=C_star*C_M*(lambda/Lambda_c)^k*(1+o(1))",
            "Lambda_c_greater_than_lambda": "alias_dominates_exponentially",
            "Lambda_c_equal_lambda": "finite_nonzero_balance_possible",
            "Lambda_c_less_than_lambda": "parity_dominates_exponentially",
            "bounded_phase_theorem_reused_outside_scope": False,
            "derivation_uses_uniform_binomial_remainder": True,
        },
        "rh329_comparator_obstruction": {
            "signed_scalar_defect": "D_k=(P_route-P_hat)-(A_route-A_hat)",
            "sign_convention": "RH330_actual_minus_model_parity_minus_alias_only",
            "D_over_A_route_limit": "-1",
            "A_route_over_H_limit": "+infinity",
            "D_over_H_limit": "-infinity",
            "rh330_fixed_phase_transfer_invoked": False,
            "verdict": "STOP_SCOPED_for_RH329_as_physical_fixed_phase_comparator",
        },
        "target_resolution_barrier": {
            "required_relative_precision": "o(H_k/A_route)=o((beta*R)^(-2k))",
            "ordinary_relative_o_1_is_sufficient": False,
            "correct_clock_physical_remainder_certificate_present": False,
            "verdict": "NOT_TESTABLE_after_replacing_Lambda_hat_by_exact_lambda",
        },
        "finite_hatted_rows": finite_rows,
        "finite_rows_are_reproduction_checks_only": True,
        "false_claims": false_claims,
        "gates": {key: False for key in "ABCDE"},
        "source_anchors": [
            "RH-326_uniform_parity_remainder_and_alias_asymptotic",
            "RH-327_target_relative_precision_barrier",
            "RH-328_physical_lambda_packet_types_and_fixed_phase_clock",
            "RH-329_exact_rational_model_clock_and_packets",
            "RH-330_actual_minus_model_sign_convention_and_inactive_bridge",
            "RH-334_physical_lambda_algebraic_identity",
            "RH-336_exact_beta_R_and_exponent_certificates",
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
