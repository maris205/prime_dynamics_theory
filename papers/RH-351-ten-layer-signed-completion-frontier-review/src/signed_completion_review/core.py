"""Deterministic RH-351 ten-layer signed-completion review ledger."""

from __future__ import annotations

from fractions import Fraction
from typing import Iterable


ROUTE_COORDINATE = "actual_growing_lower_even_signed_remainder_open"

DIRECTORY_NAMES: tuple[str, ...] = (
    "RH-342-common-hardy-head-counterloop-rank-lock-obstruction",
    "RH-343-equal-rank-equal-mass-first-alias-underdetermination",
    "RH-344-complete-critical-boundary-orbit-atom-decomposition",
    "RH-345-double-alias-parity-phase-compensation-obstruction",
    "RH-346-complete-lower-sideband-boundary-orbit-decomposition",
    "RH-347-lower-sideband-scalar-balance-underdetermination",
    "RH-348-punctured-lower-even-boundary-orbit-ladder",
    "RH-349-two-lower-sideband-phase-incompatibility",
    "RH-350-growing-depth-lower-sideband-phase-incompatibility",
    "RH-351-ten-layer-signed-completion-frontier-review",
)

LAYER_LEDGER: tuple[dict[str, object], ...] = (
    {
        "paper": 342,
        "layer": "common_hardy_head_counterloop_rank_lock",
        "result_class": "exact_rank_and_shifted_moment_theorems_with_hidden_shell_information_class_obstruction",
        "scoped_conclusion_proved": True,
        "actual_signed_remainder_discharged": False,
    },
    {
        "paper": 343,
        "layer": "equal_rank_equal_mass_first_alias",
        "result_class": "finite_normal_spectral_information_class_underdetermination",
        "scoped_conclusion_proved": True,
        "actual_signed_remainder_discharged": False,
    },
    {
        "paper": 344,
        "layer": "complete_critical_boundary_orbit",
        "result_class": "exact_physical_raw_partition_decomposition_and_double_demand",
        "scoped_conclusion_proved": True,
        "actual_signed_remainder_discharged": False,
    },
    {
        "paper": 345,
        "layer": "critical_parity_phase_compensation",
        "result_class": "conditional_physical_off_balance_obstruction_and_scalar_underdetermination",
        "scoped_conclusion_proved": True,
        "actual_signed_remainder_discharged": False,
    },
    {
        "paper": 346,
        "layer": "complete_lower_sideband_boundary_orbit",
        "result_class": "exact_physical_lower_sideband_decomposition_and_radial_scale",
        "scoped_conclusion_proved": True,
        "actual_signed_remainder_discharged": False,
    },
    {
        "paper": 347,
        "layer": "lower_sideband_scalar_balance",
        "result_class": "conditional_physical_off_balance_obstruction_and_scalar_underdetermination",
        "scoped_conclusion_proved": True,
        "actual_signed_remainder_discharged": False,
    },
    {
        "paper": 348,
        "layer": "punctured_lower_even_orbit_ladder",
        "result_class": "exact_physical_ladder_asymptotic_and_necessary_signed_supply",
        "scoped_conclusion_proved": True,
        "actual_signed_remainder_discharged": False,
    },
    {
        "paper": 349,
        "layer": "two_lower_sideband_phase_incompatibility",
        "result_class": "fixed_two_coordinate_conditional_physical_phase_obstruction",
        "scoped_conclusion_proved": True,
        "actual_signed_remainder_discharged": False,
    },
    {
        "paper": 350,
        "layer": "growing_depth_lower_sideband_phase_incompatibility",
        "result_class": "uniform_deterministic_laws_exact_minimax_and_conditional_physical_obstruction",
        "scoped_conclusion_proved": True,
        "actual_signed_remainder_discharged": False,
    },
    {
        "paper": 351,
        "layer": "ten_layer_signed_completion_frontier_review",
        "result_class": "growing_depth_affine_completion_surjectivity_and_information_class_underdetermination",
        "scoped_conclusion_proved": True,
        "actual_signed_remainder_discharged": False,
    },
)


def _fractions(values: Iterable[int | Fraction], name: str) -> tuple[Fraction, ...]:
    converted = []
    for value in values:
        if isinstance(value, bool) or not isinstance(value, (int, Fraction)):
            raise TypeError(f"{name} entries must be integers or Fractions")
        converted.append(Fraction(value))
    if not converted:
        raise ValueError(f"{name} must be nonempty")
    return tuple(converted)


def _locked_arrays(
    demand: Iterable[int | Fraction],
    parity: Iterable[int | Fraction],
    residual: Iterable[int | Fraction],
    weights: Iterable[int | Fraction],
) -> tuple[tuple[Fraction, ...], ...]:
    arrays = (
        _fractions(demand, "demand"),
        _fractions(parity, "parity"),
        _fractions(residual, "residual"),
        _fractions(weights, "weights"),
    )
    lengths = {len(array) for array in arrays}
    if len(lengths) != 1:
        raise ValueError("demand, parity, residual, and weights must have equal lengths")
    if any(weight <= 0 for weight in arrays[3]):
        raise ValueError("weights must be strictly positive")
    return arrays


def _weighted_size(values: tuple[Fraction, ...], weights: tuple[Fraction, ...]) -> Fraction:
    return sum((weight * abs(value) for value, weight in zip(values, weights)), Fraction(0))


def affine_completion(
    demand: Iterable[int | Fraction],
    parity: Iterable[int | Fraction],
    residual: Iterable[int | Fraction],
    weights: Iterable[int | Fraction],
) -> dict[str, object]:
    """Return the exact formal completion Y=S-P+r and its direct residual.

    The arrays are coefficient ledgers only.  No operator realization is
    constructed or inferred.
    """

    demand_values, parity_values, residual_values, weight_values = _locked_arrays(
        demand, parity, residual, weights
    )
    remainder = tuple(
        source - packet + target
        for source, packet, target in zip(
            demand_values, parity_values, residual_values
        )
    )
    direct = tuple(
        y_value + packet - source
        for y_value, packet, source in zip(
            remainder, parity_values, demand_values
        )
    )
    return {
        "demand": demand_values,
        "parity": parity_values,
        "prescribed_residual": residual_values,
        "weights": weight_values,
        "completion_Y": remainder,
        "direct_residual": direct,
        "weighted_Y_budget": _weighted_size(remainder, weight_values),
        "weighted_direct_budget": _weighted_size(direct, weight_values),
        "physical_operator_constructed": False,
    }


def opposite_completion_witness(
    demand: Iterable[int | Fraction],
    parity: Iterable[int | Fraction],
    weights: Iterable[int | Fraction],
) -> dict[str, object]:
    """Return exact close/far ledgers and the budget-exchange identity."""

    demand_values = _fractions(demand, "demand")
    parity_values = _fractions(parity, "parity")
    weight_values = _fractions(weights, "weights")
    if len({len(demand_values), len(parity_values), len(weight_values)}) != 1:
        raise ValueError("demand, parity, and weights must have equal lengths")
    if any(weight <= 0 for weight in weight_values):
        raise ValueError("weights must be strictly positive")

    zero = tuple(Fraction(0) for _ in demand_values)
    close = affine_completion(demand_values, parity_values, zero, weight_values)
    far_residual = tuple(
        packet - source for source, packet in zip(demand_values, parity_values)
    )
    far = affine_completion(demand_values, parity_values, far_residual, weight_values)
    if any(far["completion_Y"]):
        raise AssertionError("far completion must have Y=0 exactly")

    return {
        "coordinate_count": len(demand_values),
        "close": close,
        "far": far,
        "budget_exchange": {
            "close_Y_equals_far_direct": close["weighted_Y_budget"]
            == far["weighted_direct_budget"],
            "far_Y_equals_close_direct_zero": far["weighted_Y_budget"]
            == close["weighted_direct_budget"]
            == 0,
            "common_nonzero_budget": close["weighted_Y_budget"],
        },
        "physical_operator_constructed": False,
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


def _finite_witness(coordinate_count: int) -> dict[str, object]:
    if coordinate_count < 2:
        raise ValueError("coordinate_count must be at least two")
    demand = tuple(Fraction(2 ** (coordinate_count - index)) for index in range(coordinate_count))
    parity = tuple(
        source * Fraction(2, 3) ** index
        for index, source in enumerate(demand)
    )
    weights = tuple(Fraction(1, 2**index) for index in range(coordinate_count))
    return _fraction_text(opposite_completion_witness(demand, parity, weights))


def review_status() -> dict[str, object]:
    gates = {
        "A_canonical_intrinsic_dynamical_spectral_determinant": False,
        "B_time_oriented_scattering_or_unitary_completion": False,
        "C_self_adjoint_generator_and_intrinsic_T_log_T": False,
        "D_von_mangoldt_weighted_prime_power_traces": False,
        "E_completed_zeta_divisor_equality": False,
    }
    false_claims = {
        "abstract_close_ledger_is_actual_noisy_operator": False,
        "abstract_far_ledger_is_actual_noisy_operator": False,
        "actual_Y_is_zero_proved": False,
        "actual_Y_equals_S_minus_P_proved": False,
        "actual_aggregate_small_Y_proved": False,
        "unconditional_selected_lower_even_closure_proved": False,
        "unconditional_selected_lower_even_nonclosure_proved": False,
        "unconditional_full_prefix_closure_proved": False,
        "unconditional_full_prefix_nonclosure_proved": False,
        "full_E_off_decided": False,
        "head_counterloop_transport_closed": False,
        "critical_signed_remainder_decided": False,
        "first_lower_signed_remainder_decided": False,
        "odd_orders_controlled": False,
        "upper_alias_orders_controlled": False,
        "rh241_moving_noisy_envelope_closed": False,
        "rh288_activated": False,
        "hilbert_polya_constructed": False,
        "riemann_zeros_identified": False,
        "riemann_hypothesis_proved": False,
        "von_mangoldt_trace_proved": False,
        "zeta_divisor_equality": False,
    }
    obligations = {
        "actual_growing_lower_even_Y_theorem": False,
        "actual_critical_signed_remainder": False,
        "actual_first_lower_signed_remainder": False,
        "actual_head_counterloop_transport": False,
        "odd_order_control": False,
        "upper_alias_control": False,
        "full_signed_E_off": False,
        "direct_physical_annular_theorem": False,
    }
    return {
        "status": "rh351_ten_layer_signed_completion_frontier_review",
        "verdict": "GO_SCOPED_growing_depth_coefficient_ledger_information_class_underdetermination",
        "scope": "selected_growing_lower_even_direct_coefficients_not_physical_operator_realizability_or_full_prefix",
        "paper_numbers": list(range(342, 352)),
        "route_coordinate": ROUTE_COORDINATE,
        "layers": [dict(layer) for layer in LAYER_LEDGER],
        "layer_count": len(LAYER_LEDGER),
        "proved_scoped_conclusion_count": sum(
            bool(layer["scoped_conclusion_proved"]) for layer in LAYER_LEDGER
        ),
        "discharged_actual_signed_remainder_count": sum(
            bool(layer["actual_signed_remainder_discharged"])
            for layer in LAYER_LEDGER
        ),
        "rh241_ancestry": {
            "moving_noisy_all_order_trace_envelope_still_open": True,
            "no_over_extraction_coefficient_bridge_still_open": True,
            "deterministic_numerator_anchor_later_proved_by_RH263": True,
            "deterministic_all_order_envelope_later_proved_by_RH267": True,
            "deterministic_sharp_radius_later_proved_by_RH268": True,
            "RH350_selected_lower_even_uniformity_is_not_RH241_noisy_envelope": True,
            "gate_A_still_open": True,
        },
        "growing_window": {
            "clock": "k=log(1/sigma)/(2log(lambda))+O(1)",
            "indices": "m_(k,j)=k-j_for_2<=j<=J_k",
            "depth": "J_k->infinity_and_J_k=o(k)",
            "target": "H_m=m*R^(-2m)",
            "x": "x=(beta*R)^2>1",
            "direct_identity": "p_(k,j)=Y_(k,j)+P_(k,j)-S_(k,j)",
            "actual_Y_type": "Y_(k,j)=T_(k,m)^rest-d_(sigma,k,2m)",
        },
        "information_class_theorem": {
            "affine_surjectivity": "Y=S-P+r_gives_p=r_exactly",
            "close_completion": "Y=S-P_gives_p=0",
            "far_completion": "Y=0_gives_p=P-S",
            "budget_exchange": "Yagg(close)=L(far)_and_Yagg(far)=L(close)=0",
            "far_weighted_law": "L(far)=F_(J_k-2)(a_k)/C_M+o(1)",
            "far_positive_liminf": "[1/(x-1)-1/(x*lambda-1)]/C_M>0",
            "far_unnormalized_selected_subprefix": "diverges_at_least_on_x^(k-2)_scale",
            "physical_realizability_claimed": False,
            "actual_physical_verdict_determined": False,
        },
        "open_obligations": obligations,
        "open_obligation_count": sum(not value for value in obligations.values()),
        "finite_witness_rows": [_finite_witness(count) for count in (2, 4, 7)],
        "finite_rows_are_abstract_algebra_checks_only": True,
        "upstream_gate_values_expected_false": 45,
        "batch_gate_values_expected_false": 50,
        "expected_upstream_publication_files": 135,
        "expected_review_publication_files": 19,
        "expected_batch_publication_files": 154,
        "expected_batch_tree_files": 176,
        "source_anchors": [
            "RH-241_open_moving_noisy_uniform_trace_envelope_and_coefficient_bridge",
            "RH-263_all_order_deterministic_numerator_anchor",
            "RH-267_certified_deterministic_all_order_envelope",
            "RH-268_sharp_deterministic_coefficient_radius_law",
            *[f"RH-{number}_batch_layer" for number in range(342, 351)],
        ],
        "false_claims": false_claims,
        "gates": gates,
    }
