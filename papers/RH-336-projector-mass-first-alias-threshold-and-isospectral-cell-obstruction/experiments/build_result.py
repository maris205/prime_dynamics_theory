"""Build the deterministic RH-336 theorem and exact-fixture ledger."""

from __future__ import annotations

from fractions import Fraction
import json
import math
from pathlib import Path
import sys


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from projector_mass import (  # noqa: E402
    E_MINUS_BASE,
    K_BASE,
    SUFFICIENT_LOWER,
    SUFFICIENT_UPPER,
    corrected_cell_drift,
    corrected_cell_formula,
    family_audit,
    fraction_text,
    positivity_factor_ledger,
    projector_mass_drift,
)


LAMBDA_DIAGNOSTIC = 1.678573510428322265103705129306573
R_H = Fraction(17, 20)
R_TRACE = Fraction(7, 5)
C_STAR_DIAGNOSTIC = 0.105258535936908
GAMMA_STAR_DIAGNOSTIC = 0.3503698834605293


def _exact(value):
    if isinstance(value, Fraction):
        return fraction_text(value)
    if isinstance(value, tuple):
        return [_exact(item) for item in value]
    if isinstance(value, list):
        return [_exact(item) for item in value]
    if isinstance(value, dict):
        return {key: _exact(item) for key, item in value.items()}
    return value


def moving_scale_diagnostics() -> dict[str, object]:
    """Return ordinary floating-point reproductions of symbolic scale laws."""

    beta_r = float(R_TRACE / R_H) / math.sqrt(LAMBDA_DIAGNOSTIC)
    kappa = math.log(beta_r) / math.log(LAMBDA_DIAGNOSTIC)
    rows = []
    for k, eta in ((8, -1.0), (16, 0.0), (24, 0.5)):
        sigma = LAMBDA_DIAGNOSTIC ** (-2.0 * (k - eta))
        direct = beta_r ** (-2 * k)
        converted = sigma**kappa * beta_r ** (-2 * eta)
        rows.append(
            {
                "k": k,
                "eta": eta,
                "sigma": sigma,
                "direct_scale": direct,
                "converted_scale": converted,
                "absolute_error": abs(direct - converted),
            }
        )
    p = 3.0 / 7.0
    eta = 0.25
    critical_limit = 2 * C_STAR_DIAGNOSTIC * LAMBDA_DIAGNOSTIC**eta * p
    return {
        "lambda": LAMBDA_DIAGNOSTIC,
        "r_H": float(R_H),
        "R": float(R_TRACE),
        "beta_R": beta_r,
        "kappa_proj": kappa,
        "gamma_star_RH325": GAMMA_STAR_DIAGNOSTIC,
        "exponents_are_distinct": abs(kappa - GAMMA_STAR_DIAGNOSTIC) > 0.1,
        "phase_conversion_rows": rows,
        "critical_limit_fixture": {
            "p": p,
            "eta": eta,
            "limit": critical_limit,
        },
        "certification_status": "ordinary_floating_point_reproduction_only",
    }


def result_payload() -> dict[str, object]:
    audit = family_audit(Fraction(1, 100), max_power=12)
    factors_at_lower_test = positivity_factor_ledger(Fraction(-1, 100))
    diagnostics = moving_scale_diagnostics()

    false_claims = {
        "actual_model_replacement_proved": False,
        "determinant_gluing_activated": False,
        "duhamel_full_cycle_closure_proved": False,
        "far_remainder_o_H_k_proved": False,
        "fixed_maximizing_physical_cell_for_all_sigma_identified": False,
        "full_trace_replacement_proved": False,
        "head_counterloop_transport_proved": False,
        "hilbert_polya_constructed": False,
        "isospectral_family_is_physical_noisy_operator": False,
        "local_parity_cell_equals_physical_B_plus_S": False,
        "moving_projector_mass_cancellation_excluded": False,
        "off_alias_background_closed": False,
        "physical_Delta_B_plus_Delta_S_cancellation_proved": False,
        "physical_nonzero_normalized_duhamel_obstruction_proved": False,
        "riemann_hypothesis_proved": False,
        "riemann_zeros_identified": False,
        "signed_raw_local_alias_cancellation_excluded": False,
        "von_mangoldt_trace_proved": False,
        "zeta_divisor_equality": False,
    }

    return {
        "status": "rh336_projector_mass_first_alias_threshold_and_isospectral_cell_obstruction",
        "scope": "moving_projector_mass_scale_and_nonphysical_positive_markov_isospectral_cell_obstruction",
        "moving_theorem": {
            "G_definition": "G_sigma_k(J)=r_H^(-2k)*(1-lambda_minus(sigma)^(2k))*pi_sigma(J)",
            "H_definition": "H_k=k*R^(-2k)",
            "phase": "eta_sigma=k-log(1/sigma)/(2log(lambda))_bounded",
            "ratio_asymptotic": "G/H=2*C_star*lambda^eta_sigma*(beta*R)^(2k)*pi_sigma(J)*(1+o(1))",
            "beta": "1/(r_H*sqrt(lambda))",
            "kappa_proj_symbolic": "log(beta*R)/log(lambda)=log(28/17)/log(lambda)-1/2",
            "kappa_proj_diagnostic": diagnostics["kappa_proj"],
            "gamma_star_RH325_diagnostic": diagnostics["gamma_star_RH325"],
            "kappa_proj_equals_gamma_star_RH325": False,
            "negligibility_equivalence": "G=o(H)_iff_pi=o((beta*R)^(-2k))",
            "exact_phase_conversion": "(beta*R)^(-2k)=sigma^kappa_proj*(beta*R)^(-2eta_sigma)",
            "critical_limit": "if_(beta*R)^(2k)*pi->p_and_eta_sigma->eta_then_G/H->2*C_star*lambda^eta*p",
            "beta_R_greater_than_one": True,
        },
        "fixed_partition_consequence": {
            "partition_size": "fixed_N",
            "sum_pi_i": "1",
            "max_pi_i_lower_bound": "1/N",
            "maximum_normalized_parity_cell_diverges": True,
            "maximizing_cell_may_depend_on_sigma": True,
            "pigeonhole_fixed_cell_only_on_subsequence": True,
            "identified_with_physical_B_plus_S": False,
            "raw_local_alias_signed_cancellation_may_remove_contribution": True,
        },
        "exact_family": {
            "K": _exact(K_BASE),
            "E_minus": _exact(E_MINUS_BASE),
            "S_t": "[[1-t,t,0],[0,1,0],[0,0,1]]",
            "definition": "K_t=S_t^(-1)*K*S_t",
            "sufficient_positivity_interval": "(-5/174,1/2)",
            "sufficient_interval_is_maximal": False,
            "maximal_connected_positivity_interval_containing_zero": "(-5/174,(-19+sqrt(781))/12)",
            "spectrum": ["1/1", "-2/5", "1/5"],
            "all_power_trace_formula": "Tr(K_t^m)=1+(-2/5)^m+(1/5)^m_for_m>=1",
            "t_fixture": _exact(audit),
            "positivity_factor_reproduction_at_t_minus_1_over_100": _exact(
                factors_at_lower_test
            ),
        },
        "projector_mass_family": {
            "pi_t": ["(10-8t)/17", "(-4+24t)/51", "25/51"],
            "drift": ["-8t/17", "8t/17", "0"],
            "drift_formula_at_t_1_over_100": _exact(projector_mass_drift(Fraction(1, 100))),
            "sum_pi_t": "1",
        },
        "corrected_cell_family": {
            "n": 2,
            "r_H": "17/20",
            "deterministic_singleton_slots": ["0/1", "0/1", "0/1"],
            "C_t": [
                "(6800-5760t)/4913",
                "(400+5760t)/4913",
                "6672/4913",
            ],
            "sum_C_t": "48/17",
            "drift": ["-5760t/4913", "5760t/4913", "0"],
            "t_1_over_100_cells": _exact(corrected_cell_formula(Fraction(1, 100))),
            "t_1_over_100_drift": _exact(corrected_cell_drift(Fraction(1, 100))),
            "first_alias_k1_interpretation": False,
            "family_is_nonphysical_finite_algebra": True,
        },
        "moving_scale_diagnostics": diagnostics,
        "novelty_boundary": {
            "RH210_general_similarity_projector_motion_preexists": True,
            "RH336_adds_strict_positive_row_stochastic_family": True,
            "RH336_adds_all_power_trace_lock": True,
            "RH336_adds_corrected_singleton_cell_drift": True,
        },
        "physical_duhamel_route": {
            "verdict": "NOT_TESTABLE",
            "physical_Delta_B_plus_Delta_S_signed_cancellation": "not_proved",
            "physical_nonzero_normalized_obstruction": "absent",
        },
        "finite_calculations_are_reproduction_checks_only": True,
        "false_claims": false_claims,
        "gates": {key: False for key in "ABCDE"},
        "source_anchors": [
            "RH-210_general_projector_motion_under_similarity",
            "RH-326_uniform_parity_packet_and_common_weighted_exponent",
            "RH-334_rational_bracket_and_physical_basepoint_observation",
            "RH-335_signed_projector_measure_and_corrected_cell_ledger",
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
