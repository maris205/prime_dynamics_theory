"""Build the deterministic RH-342 rank-lock ledger."""

from __future__ import annotations

from decimal import Decimal
from fractions import Fraction
import json
from pathlib import Path
import sys


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from head_rank_lock import (  # noqa: E402
    HIDDEN_RADIUS,
    Q_HEAD,
    R_H,
    R_TRACE,
    common_clock_thresholds,
    decimal_text,
    finite_diagnostic,
    physical_constants,
)


def _encode(value):
    if isinstance(value, Decimal):
        return decimal_text(value)
    if isinstance(value, Fraction):
        return f"{value.numerator}/{value.denominator}"
    if isinstance(value, (list, tuple)):
        return [_encode(item) for item in value]
    if isinstance(value, dict):
        return {key: _encode(item) for key, item in value.items()}
    return value


def result_payload() -> dict[str, object]:
    constants = physical_constants()
    thresholds = common_clock_thresholds()
    false_claims = {
        "actual_head_rank_identified": False,
        "actual_head_rank_mismatch_proved": False,
        "actual_local_head_shell_cap_proved": False,
        "actual_root_matching_proved": False,
        "aggregate_hardy_route_closed": False,
        "aggregate_moment_route_closed": False,
        "annular_convergence_proved": False,
        "determinant_gluing_activated": False,
        "direct_prefix_closure_proved": False,
        "fourier_route_closed": False,
        "head_counterloop_budget_closed": False,
        "head_counterloop_factor_is_physical_decomposition": False,
        "head_defect_divergence_proved": False,
        "head_defect_vanishing_proved": False,
        "hidden_shell_is_actual_noisy_operator": False,
        "hilbert_polya_constructed": False,
        "physical_nonidentification_theorem_proved": False,
        "rh288_activated": False,
        "riemann_hypothesis_proved": False,
        "riemann_zeros_identified": False,
        "von_mangoldt_trace_proved": False,
        "zeta_divisor_equality": False,
    }
    return {
        "status": "rh342_common_hardy_head_counterloop_rank_lock_obstruction",
        "scope": "exact_rank_and_shifted_moment_theorems_plus_nonphysical_hidden_shell_counterexample",
        "constants": {
            "q": _encode(Q_HEAD),
            "r_H": _encode(R_H),
            "R": _encode(R_TRACE),
            "hidden_shell_radius": _encode(HIDDEN_RADIUS),
            **_encode(constants),
        },
        "source_lock": {
            "actual_head": "algebraic_nonperipheral_eigenvalues_of_K_sigma_over_r_H_with_modulus_gt_q",
            "actual_head_moment": "h_(sigma,n)=sum_(mu in H_sigma)mu^n",
            "actual_head_rank": "r_sigma=#H_sigma",
            "source_rank_bound": "r_sigma<=4/sigma",
            "endpoint_singular_rank_identified_with_head_rank": False,
            "counterloop_multiset": "Y_k={beta_k exp(+-i j pi/k):1<=j<=k-1}",
            "counterloop_rank": "m_k=2k-2",
            "counterloop_moment": "s_(k,n)=beta_k^n(2k 1_(2k|n)-1-(-1)^n)",
            "defect": "d_(sigma,k,n)=h_(sigma,n)-s_(k,n)",
            "clock": "k=log(1/sigma)/(2log(lambda))+O(1)",
            "strict_prefix": "2<=n<4k_contains_2k_excludes_4k",
        },
        "analytic_factor_interface": {
            "genus_one_factor": "Phi_X(z)=prod_(x in X)(1-xz)exp(xz)",
            "local_quotient": "Phi_(H_sigma)(z)/Phi_(Y_k)(z)",
            "logarithm": "-sum_(n>=2)d_(sigma,k,n)z^n/n",
            "common_physical_determinant_decomposition": False,
        },
        "rank_lock": {
            "bound": "d1^0(H_sigma,Y_k)>=q(r_sigma-m_k)_+ + beta_k(m_k-r_sigma)_+",
            "beta_limit_gt_q": constants["beta"] > Decimal(1) / 2,
            "o1_matching_forces_eventual_exact_rank": True,
            "positive_power_rate_forces_eventual_exact_rank": True,
            "actual_rank_law_available": False,
        },
        "shifted_moment_uniqueness": {
            "hypothesis": "nonzero_finite_multisets_ranks_at_most_N_equal_power_sums_2_through_2N_plus_1",
            "rational_function": "F_X(z)=sum_x x^2/(1-xz)",
            "numerator_degree_bound": "2N-1",
            "zero_order": "2N",
            "conclusion": "X=Y_as_multisets",
            "rank_capped_strict_prefix_corollary": "N=2k-2_and_equality_for_2<=n<4k_identifies_roots",
        },
        "hidden_shell_counterexample": {
            "base": "Y_k",
            "shell": "Z_k={(3/4)exp(2pi i j/(4k)):0<=j<4k}",
            "enlarged": "X_k=Y_k_disjoint_union_Z_k",
            "conjugation_closed": True,
            "finite_normal_spectral_information_class": True,
            "actual_noisy_operator": False,
            "strict_prefix_moments_equal": True,
            "D_4k": "0_exactly",
            "padded_distance_lower_bound": "4kq=2k",
            "added_genus_one_factor": "1-(3z/4)^(4k)",
            "rank_cap_is_essential": True,
        },
        "rh299_specialization": {
            "cut": "m=4k",
            "clock_slope": _encode(thresholds["clock_slope"]),
            "global_source_safe_cap": "B=1/r_H",
            "global_threshold_formula": "gamma>2log(R/r_H)/log(lambda)",
            "global_threshold": _encode(thresholds["global_threshold"]),
            "local_unproved_cap": "every_actual_head_root_has_modulus_at_most_beta_plus_o1",
            "local_threshold_formula": "gamma>2log(beta R)/log(lambda)",
            "local_threshold": _encode(thresholds["local_threshold"]),
            "threshold_gap": _encode(thresholds["threshold_gap"]),
            "eventual_rank_equality_also_required": True,
            "actual_matching_theorem_available": False,
        },
        "route_verdict": {
            "rh299_without_rank_law_cap_rate": "STOP_SCOPED",
            "aggregate_moment_fourier_hardy": "NOT_TESTABLE_open",
            "direct_annular": "NOT_TESTABLE_open",
            "rh288": "OPEN_not_activated",
        },
        "finite_rows": [_encode(finite_diagnostic(k)) for k in (3, 5, 9, 17)],
        "finite_rows_are_reproduction_checks_only": True,
        "false_claims": false_claims,
        "gates": {key: False for key in "ABCDE"},
        "source_anchors": [
            "RH-272_counterloop_root_shell_and_beta_k_limit",
            "RH-282_modulus_complete_actual_head_and_rank_bound",
            "RH-288_weighted_prefix_tail_gluing_criterion",
            "RH-290_typed_spectral_counterloop_ledger",
            "RH-297_natural_counterloop_alias_ledger",
            "RH-299_zero_padded_root_l1_transport",
            "RH-300_annular_analytic_prefix_criteria",
            "RH-301_weighted_prefix_frontier_review",
            "RH-334_common_hardy_full_trace_head_counterloop_identity",
            "RH-341_actual_first_alias_frontier_review",
        ],
    }


def main() -> None:
    output = ROOT / "results" / "result.json"
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(
        json.dumps(result_payload(), indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )
    print(output.relative_to(ROOT))


if __name__ == "__main__":
    main()
