"""Conditioning budgets forced by a transverse pair of temporal subspaces."""

from __future__ import annotations

import math


def oblique_condition_number(minimum_cross_singular_value: float) -> float:
    value = float(minimum_cross_singular_value)
    if not 0.0 < value <= 1.0 + 1e-12:
        raise ValueError("cross singular value must lie in (0,1]")
    return 1.0 / value


def principal_angle_degrees(minimum_cross_singular_value: float) -> float:
    value = min(1.0, max(0.0, float(minimum_cross_singular_value)))
    return math.degrees(math.acos(value))


def conditioned_residual_budget(
    minimum_cross_singular_value: float,
    right_relative_residual: float,
    left_relative_residual: float,
) -> dict[str, float | bool]:
    sigma = float(minimum_cross_singular_value)
    right = float(right_relative_residual)
    left = float(left_relative_residual)
    if min(sigma, right, left) < 0.0 or sigma == 0.0:
        raise ValueError("invalid conditioning budget")
    chi = oblique_condition_number(sigma)
    maximum = max(right, left)
    amplified = chi * maximum
    return {
        "minimum_cross_singular_value": sigma,
        "oblique_condition_number": chi,
        "maximum_relative_residual": maximum,
        "amplified_maximum_residual": amplified,
        "relative_residual_product": right * left,
        "conditioned_contraction_gate": amplified < 1.0,
    }


def projector_perturbation_bound(oblique_condition: float, subspace_error: float) -> float:
    chi = float(oblique_condition)
    error = float(subspace_error)
    if chi < 1.0 or error < 0.0:
        raise ValueError("invalid projector perturbation data")
    denominator = 1.0 - chi * error
    return math.inf if denominator <= 0.0 else chi * chi * error / denominator
