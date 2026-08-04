"""RH-361 typed review of signed completion and upper counterloops."""

from __future__ import annotations

from fractions import Fraction
from typing import Iterable


DIRECTORY_NAMES: tuple[str, ...] = (
    "RH-352-modulus-cap-forced-growing-ladder-signed-cancellation",
    "RH-353-critical-first-lower-actual-signed-completion-gap",
    "RH-354-parity-free-near-alias-direct-tail-envelope",
    "RH-355-upper-alias-counterloop-burden-and-head-transfer-precision",
    "RH-356-sharp-post-first-alias-mesoscopic-crossover",
    "RH-357-uniform-linear-depth-upper-counterloop-profile",
    "RH-358-terminal-lag-geometric-localization",
    "RH-359-logarithmic-terminal-window-accuracy-thresholds",
    "RH-360-terminal-lag-exponential-tilt-phase-transition",
    "RH-361-ten-layer-signed-completion-and-upper-counterloop-review",
)

UPSTREAM_FALSE_CLAIM_COUNTS: tuple[int, ...] = (15, 14, 13, 14, 14, 14, 14, 15, 16)

LAYER_LEDGER: tuple[dict[str, object], ...] = (
    {
        "paper": 352,
        "layer": "actual_growing_lower_even_signed_cancellation",
        "object_type": "actual_direct_p_and_actual_signed_Y",
        "result_class": "normalized_selected_natural_scale_theorem",
        "unconditional_scoped_conclusion": True,
        "actual_head_transfer": "not_the_claim",
    },
    {
        "paper": 353,
        "layer": "actual_critical_first_lower_signed_completion_gap",
        "object_type": "actual_direct_p_and_actual_signed_Y",
        "result_class": "two_coordinate_normalized_gap_and_selected_Y_supply",
        "unconditional_scoped_conclusion": True,
        "actual_head_transfer": "not_the_claim",
    },
    {
        "paper": 354,
        "layer": "actual_parity_free_near_alias_direct_tail",
        "object_type": "actual_direct_p_equals_tau_minus_a",
        "result_class": "normalized_all_order_tail_above_a_moving_cut",
        "unconditional_scoped_conclusion": True,
        "actual_head_transfer": "not_the_claim",
    },
    {
        "paper": 355,
        "layer": "deterministic_upper_counterloop_burden",
        "object_type": "deterministic_graded_counterloop_s",
        "result_class": "complete_strict_upper_band_and_transport_precision_obligation",
        "unconditional_scoped_conclusion": True,
        "actual_head_transfer": "conditional_on_same_clock_unnormalized_D_4k",
    },
    {
        "paper": 356,
        "layer": "deterministic_mesoscopic_crossover",
        "object_type": "deterministic_graded_counterloop_s",
        "result_class": "uniform_post_alias_mesoscopic_profile_and_integer_phase",
        "unconditional_scoped_conclusion": True,
        "actual_head_transfer": "conditional_on_same_clock_unnormalized_D_4k",
    },
    {
        "paper": 357,
        "layer": "deterministic_linear_depth_profile",
        "object_type": "deterministic_graded_counterloop_s",
        "result_class": "uniform_complete_band_endpoint_profile",
        "unconditional_scoped_conclusion": True,
        "actual_head_transfer": "conditional_on_same_clock_unnormalized_D_4k",
    },
    {
        "paper": 358,
        "layer": "deterministic_terminal_lag_localization",
        "object_type": "normalized_deterministic_counterloop_budget_probability",
        "result_class": "uniform_tail_geometric_TV_and_moment_limits",
        "unconditional_scoped_conclusion": True,
        "actual_head_transfer": "conditional_on_same_clock_unnormalized_D_4k",
    },
    {
        "paper": 359,
        "layer": "deterministic_logarithmic_accuracy_thresholds",
        "object_type": "deterministic_terminal_lag_tail_budget",
        "result_class": "polynomial_accuracy_phase_and_inverse_window_laws",
        "unconditional_scoped_conclusion": True,
        "actual_head_transfer": "conditional_on_same_clock_unnormalized_D_4k",
    },
    {
        "paper": 360,
        "layer": "deterministic_exponential_tilt_transition",
        "object_type": "deterministic_terminal_lag_budget_transform",
        "result_class": "subcritical_critical_supercritical_transform_phase_diagram",
        "unconditional_scoped_conclusion": True,
        "actual_head_transfer": "conditional_on_same_clock_unnormalized_D_4k",
    },
    {
        "paper": 361,
        "layer": "ten_layer_typed_separation_review",
        "object_type": "repository_result_and_dependency_audit",
        "result_class": "exact_actual_direct_vs_deterministic_counterloop_separation",
        "unconditional_scoped_conclusion": True,
        "actual_head_transfer": "not_proved",
    },
)


def _fractions(values: Iterable[int | Fraction], name: str) -> tuple[Fraction, ...]:
    converted: list[Fraction] = []
    for value in values:
        if isinstance(value, bool) or not isinstance(value, (int, Fraction)):
            raise TypeError(f"{name} entries must be integers or Fractions")
        converted.append(Fraction(value))
    if not converted:
        raise ValueError(f"{name} must be nonempty")
    return tuple(converted)


def _weighted_size(values: tuple[Fraction, ...], weights: tuple[Fraction, ...]) -> Fraction:
    return sum((weight * abs(value) for value, weight in zip(values, weights)), Fraction(0))


def typed_defect_fiber(
    direct: Iterable[int | Fraction],
    counterloop: Iterable[int | Fraction],
    defect: Iterable[int | Fraction],
    weights: Iterable[int | Fraction],
) -> dict[str, object]:
    """Build one exact coefficient fiber with p=q-d and d=h-s.

    This is an algebraic coefficient ledger.  It constructs neither a noisy
    operator nor a spectral inclusion.
    """

    p_values = _fractions(direct, "direct")
    s_values = _fractions(counterloop, "counterloop")
    d_values = _fractions(defect, "defect")
    weight_values = _fractions(weights, "weights")
    if len({len(p_values), len(s_values), len(d_values), len(weight_values)}) != 1:
        raise ValueError("direct, counterloop, defect, and weights must have equal lengths")
    if any(weight <= 0 for weight in weight_values):
        raise ValueError("weights must be strictly positive")

    full_trace = tuple(p + d for p, d in zip(p_values, d_values))
    head = tuple(s + d for s, d in zip(s_values, d_values))
    recovered_defect = tuple(h - s for h, s in zip(head, s_values))
    recovered_direct = tuple(q - d for q, d in zip(full_trace, recovered_defect))
    return {
        "direct_p": p_values,
        "counterloop_s": s_values,
        "defect_d": d_values,
        "full_trace_q": full_trace,
        "actual_head_h": head,
        "weights": weight_values,
        "p_equals_q_minus_d_exact": recovered_direct == p_values,
        "d_equals_h_minus_s_exact": recovered_defect == d_values,
        "weighted_direct_budget": _weighted_size(p_values, weight_values),
        "weighted_counterloop_budget": _weighted_size(s_values, weight_values),
        "weighted_defect_budget": _weighted_size(d_values, weight_values),
        "weighted_full_trace_budget": _weighted_size(full_trace, weight_values),
        "weighted_head_budget": _weighted_size(head, weight_values),
        "physical_operator_constructed": False,
        "spectral_submultiset_claimed": False,
    }


def opposite_typed_fibers(
    direct: Iterable[int | Fraction],
    counterloop: Iterable[int | Fraction],
    nonzero_defect: Iterable[int | Fraction],
    weights: Iterable[int | Fraction],
) -> dict[str, object]:
    """Return zero- and nonzero-defect fibers with the same p and s."""

    p_values = _fractions(direct, "direct")
    s_values = _fractions(counterloop, "counterloop")
    d_values = _fractions(nonzero_defect, "nonzero_defect")
    weight_values = _fractions(weights, "weights")
    if len({len(p_values), len(s_values), len(d_values), len(weight_values)}) != 1:
        raise ValueError("all arrays must have equal lengths")
    if not any(d_values):
        raise ValueError("nonzero_defect must contain a nonzero entry")
    zero = tuple(Fraction(0) for _ in p_values)
    zero_fiber = typed_defect_fiber(p_values, s_values, zero, weight_values)
    shifted_fiber = typed_defect_fiber(p_values, s_values, d_values, weight_values)
    return {
        "zero_defect_fiber": zero_fiber,
        "shifted_defect_fiber": shifted_fiber,
        "same_direct_p": zero_fiber["direct_p"] == shifted_fiber["direct_p"],
        "same_counterloop_s": zero_fiber["counterloop_s"] == shifted_fiber["counterloop_s"],
        "full_trace_budget_changed": zero_fiber["weighted_full_trace_budget"]
        != shifted_fiber["weighted_full_trace_budget"],
        "head_budget_changed": zero_fiber["weighted_head_budget"]
        != shifted_fiber["weighted_head_budget"],
        "physical_operator_constructed": False,
        "spectral_submultiset_claimed": False,
    }


def _fraction_text(value: object) -> object:
    if isinstance(value, Fraction):
        return f"{value.numerator}/{value.denominator}"
    if isinstance(value, tuple):
        return [_fraction_text(item) for item in value]
    if isinstance(value, list):
        return [_fraction_text(item) for item in value]
    if isinstance(value, dict):
        return {key: _fraction_text(item) for key, item in value.items()}
    return value


def _finite_witness(scale: int) -> dict[str, object]:
    if scale <= 0:
        raise ValueError("scale must be positive")
    direct = (Fraction(1, scale + 1), Fraction(-1, scale + 2), Fraction(1, scale + 3))
    counterloop = (Fraction(8 * scale), Fraction(4 * scale), Fraction(2 * scale))
    defect = (Fraction(16 * scale), Fraction(-8 * scale), Fraction(4 * scale))
    weights = (Fraction(1), Fraction(1, 2), Fraction(1, 4))
    return _fraction_text(opposite_typed_fibers(direct, counterloop, defect, weights))


def review_status() -> dict[str, object]:
    gates = {
        "A_canonical_intrinsic_dynamical_spectral_determinant": False,
        "B_time_oriented_scattering_or_unitary_completion": False,
        "C_self_adjoint_generator_and_intrinsic_T_log_T": False,
        "D_von_mangoldt_weighted_prime_power_traces": False,
        "E_completed_zeta_divisor_equality": False,
    }
    false_claims = {
        "same_clock_unnormalized_D_4k_transport_proved": False,
        "actual_head_equals_counterloop_proved": False,
        "counterloop_is_actual_spectral_submultiset": False,
        "deterministic_counterloop_budget_is_actual_head_budget": False,
        "direct_p_budget_transferred_to_full_trace_q": False,
        "full_E_off_closed": False,
        "normalized_direct_tail_is_unnormalized_prefix": False,
        "actual_roots_identified": False,
        "actual_rank_identified": False,
        "actual_spectrum_identified": False,
        "tilted_budget_is_eigenvalue_distribution": False,
        "rh241_moving_noisy_all_order_envelope_closed": False,
        "rh241_coefficient_bridge_closed": False,
        "rh288_activated": False,
        "hilbert_polya_constructed": False,
        "riemann_zeros_identified": False,
        "von_mangoldt_trace_proved": False,
        "zeta_divisor_equality": False,
        "riemann_hypothesis_proved": False,
        "finite_rows_are_asymptotic_evidence": False,
    }
    obligations = {
        "same_clock_unnormalized_D_4k_transport": False,
        "typed_full_trace_q_or_E_off_theorem": False,
        "unnormalized_complete_direct_prefix": False,
        "low_order_direct_prefix_below_moving_cut": False,
        "rh241_moving_noisy_all_order_envelope": False,
        "rh241_no_over_extraction_coefficient_bridge": False,
        "rh288_one_type_prefix_tail_gluing": False,
        "actual_root_rank_or_spectral_identification": False,
    }
    upstream_audit = [
        {
            "paper": number,
            "gate_count": 5,
            "gate_true_count": 0,
            "false_claim_count": false_count,
            "false_claim_true_count": 0,
        }
        for number, false_count in zip(range(352, 361), UPSTREAM_FALSE_CLAIM_COUNTS)
    ]
    return {
        "status": "RH-361_ten_layer_signed_completion_and_upper_counterloop_review",
        "verdict": "GO_SCOPED_TYPED_BATCH_SEPARATION",
        "scope": "repository_typed_audit_not_actual_operator_root_rank_or_RH_identification",
        "paper_numbers": list(range(352, 362)),
        "directory_names": list(DIRECTORY_NAMES),
        "layer_count": len(LAYER_LEDGER),
        "layers": [dict(layer) for layer in LAYER_LEDGER],
        "actual_direct_layer_numbers": [352, 353, 354],
        "deterministic_counterloop_layer_numbers": list(range(355, 361)),
        "review_layer_number": 361,
        "unconditional_scoped_conclusion_count": sum(
            bool(layer["unconditional_scoped_conclusion"]) for layer in LAYER_LEDGER
        ),
        "conditional_actual_head_layer_count": sum(
            layer["actual_head_transfer"] == "conditional_on_same_clock_unnormalized_D_4k"
            for layer in LAYER_LEDGER
        ),
        "typed_identities": {
            "direct": "p=tau-a=q-d",
            "head_defect": "d=h-s",
            "fiber": "q=p+d_and_h=s+d",
            "p_to_q_promotion_requires_same_clock_defect_control": True,
        },
        "typed_separation_theorem": {
            "actual_branch": "RH352_354_actual_p_or_Y_at_selected_normalized_scales",
            "deterministic_branch": "RH355_360_unconditional_graded_counterloop_budget_laws",
            "only_named_actual_head_bridge": "same_clock_unnormalized_D_(4k)(R)->0",
            "bridge_proved_in_batch": False,
            "p_alone_determines_q": False,
            "s_alone_determines_h": False,
            "spectral_submultiset_inclusion_proved": False,
            "physical_counterexample_constructed": False,
        },
        "terminal_lag_route": {
            "status": "deterministic_route_closed_through_transform_phase_diagram",
            "geometric_localization": "RH-358",
            "logarithmic_inverse_accuracy": "RH-359",
            "exponential_tilt_phase_transition": "RH-360",
            "actual_transfer_requires_D_4k": True,
        },
        "rh241_frontier": {
            "moving_noisy_all_order_envelope_open": True,
            "coefficient_bridge_open": True,
            "deterministic_anchor_does_not_close_noisy_frontier": True,
        },
        "rh288_status": {
            "active": False,
            "reason": "complete_same_type_physical_prefix_leaf_absent",
        },
        "open_obligations": obligations,
        "open_obligation_count": sum(not value for value in obligations.values()),
        "upstream_audit": upstream_audit,
        "upstream_gate_values_expected_false": 45,
        "upstream_false_claim_values_expected_false": sum(UPSTREAM_FALSE_CLAIM_COUNTS),
        "review_gate_values_expected_false": 5,
        "batch_gate_values_expected_false": 50,
        "review_false_claim_values_expected_false": len(false_claims),
        "batch_false_claim_values_expected_false": sum(UPSTREAM_FALSE_CLAIM_COUNTS)
        + len(false_claims),
        "expected_upstream_publication_files": 156,
        "expected_review_publication_files": 20,
        "expected_batch_publication_files": 176,
        "expected_batch_tree_files": 198,
        "finite_typed_fiber_rows": [_finite_witness(scale) for scale in (1, 3, 7)],
        "finite_rows_are_coefficient_ledger_reproduction_only": True,
        "source_anchors": [
            "RH-241_open_moving_noisy_all_order_envelope_and_coefficient_bridge",
            "RH-288_inactive_weighted_prefix_tail_gluing_criterion",
            "RH-340_exact_same_clock_p_equals_q_minus_d_identity",
            "RH-351_signed_completion_frontier_review",
            *[f"RH-{number}_batch_layer" for number in range(352, 361)],
        ],
        "false_claims": false_claims,
        "gates": gates,
    }
