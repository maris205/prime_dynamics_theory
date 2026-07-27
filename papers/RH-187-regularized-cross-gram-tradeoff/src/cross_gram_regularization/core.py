"""Singular-value clipping for nearly nontransverse biorthogonal frames."""

from __future__ import annotations

import math


def clipped_cross_gram_budget(
    minimum_cross_singular_value: float,
    residual_level: float,
    clipping_threshold: float,
) -> dict[str, float | bool]:
    sigma = float(minimum_cross_singular_value)
    epsilon = float(residual_level)
    tau = float(clipping_threshold)
    if sigma <= 0.0 or epsilon < 0.0 or tau <= 0.0:
        raise ValueError("sigma and tau must be positive and residual nonnegative")
    effective = max(sigma, tau)
    duality_ratio = sigma / effective
    duality_defect = 1.0 - duality_ratio
    conditioning = 1.0 / effective
    combined = duality_defect + epsilon * conditioning
    return {
        "minimum_cross_singular_value": sigma,
        "residual_level": epsilon,
        "clipping_threshold": tau,
        "effective_singular_value": effective,
        "duality_ratio": duality_ratio,
        "duality_defect": duality_defect,
        "regularized_norm_product": conditioning,
        "combined_regularized_gate": combined,
        "strict_contraction": combined < 1.0,
    }


def clipped_gate_infimum(
    minimum_cross_singular_value: float,
    residual_level: float,
) -> dict[str, float | bool]:
    sigma = float(minimum_cross_singular_value)
    epsilon = float(residual_level)
    if sigma <= 0.0 or epsilon < 0.0:
        raise ValueError("invalid clipping data")
    exact_gate = epsilon / sigma
    strict_exists = epsilon < sigma
    infimum = exact_gate if strict_exists else 1.0
    return {
        "unregularized_gate": exact_gate,
        "gate_infimum": infimum,
        "strict_contraction_exists": strict_exists,
        "residual_to_cross_angle_ratio": exact_gate,
    }


def directionwise_clipped_budget(
    singular_values,
    residual_levels,
    clipping_threshold: float,
) -> dict[str, object]:
    singular = [float(value) for value in singular_values]
    residual = [float(value) for value in residual_levels]
    if not singular or len(singular) != len(residual):
        raise ValueError("singular values and residual levels must have one nonempty shape")
    records = [
        clipped_cross_gram_budget(sigma, epsilon, clipping_threshold)
        for sigma, epsilon in zip(singular, residual)
    ]
    return {
        "direction_count": len(records),
        "direction_budgets": records,
        "maximum_combined_gate": max(float(item["combined_regularized_gate"]) for item in records),
        "strict_contraction_in_every_direction": all(bool(item["strict_contraction"]) for item in records),
        "exact_directionwise_criterion": all(epsilon < sigma for sigma, epsilon in zip(singular, residual)),
    }


def threshold_for_condition_cap(condition_cap: float) -> float:
    cap = float(condition_cap)
    if cap < 1.0:
        raise ValueError("condition cap must be at least one")
    return 1.0 / cap
