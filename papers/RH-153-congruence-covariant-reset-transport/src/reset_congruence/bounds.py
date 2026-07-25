"""Sharp and outward bounds for reset overlap congruences."""

from __future__ import annotations

import math


def normalized_base(eigenvalue_lower: float, eigenvalue_upper: float) -> float:
    lower = float(eigenvalue_lower)
    upper = float(eigenvalue_upper)
    if not math.isfinite(lower) or not math.isfinite(upper) or lower < 0.0 or upper < lower:
        raise ValueError("invalid eigenvalue endpoints")
    return math.sqrt(lower / upper) if upper > 0.0 else 0.0


def correlated_base_lower(
    eigenvalue_lower: float,
    eigenvalue_upper: float,
    overlap_lower: float,
    overlap_upper: float = 1.0,
) -> float:
    lower = float(overlap_lower)
    upper = float(overlap_upper)
    if not math.isfinite(lower) or not math.isfinite(upper) or lower < 0.0 or upper <= 0.0 or lower > upper:
        raise ValueError("invalid overlap endpoints")
    return lower / upper * normalized_base(eigenvalue_lower, eigenvalue_upper)


def inverse_congruence_radius(
    nominal_overlap_smin: float,
    overlap_radius: float,
    nominal_gram_norm: float,
    gram_radius: float,
) -> dict[str, float | bool]:
    """Independent-ball radius for C^{-*} H C^{-1}.

    The nominal overlap is C0, ||C-C0|| <= eta, and ||H-H0|| <= rho.
    """
    alpha = float(nominal_overlap_smin)
    eta = float(overlap_radius)
    hnorm = float(nominal_gram_norm)
    rho = float(gram_radius)
    if not all(math.isfinite(value) for value in (alpha, eta, hnorm, rho)):
        raise ValueError("non-finite congruence data")
    if alpha <= 0.0 or eta < 0.0 or hnorm < 0.0 or rho < 0.0:
        raise ValueError("invalid congruence data")
    lower = alpha - eta
    if lower <= 0.0:
        return {"stable": False, "overlap_lower": 0.0, "inverse_difference_upper": math.inf, "radius": math.inf}
    inverse_difference = eta / (alpha * lower)
    radius = rho / (lower * lower) + hnorm * inverse_difference * (1.0 / lower + 1.0 / alpha)
    return {
        "stable": True,
        "overlap_lower": lower,
        "inverse_difference_upper": inverse_difference,
        "radius": radius,
    }
