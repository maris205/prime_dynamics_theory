"""Tail-energy bounds for the concentration of the fourth exterior power."""

from __future__ import annotations

from itertools import combinations
import math

import numpy as np


def _spectrum(values: list[float] | tuple[float, ...] | np.ndarray) -> np.ndarray:
    singular = np.asarray(values, dtype=float)
    if singular.ndim != 1 or singular.size < 4 or np.any(~np.isfinite(singular)) or np.any(singular < 0.0):
        raise ValueError("at least four finite nonnegative singular values are required")
    return np.sort(singular)[::-1]


def exterior_dimension(rank: int) -> int:
    width = int(rank)
    if width < 4:
        raise ValueError("rank must be at least four")
    return math.comb(width, 4)


def elementary_symmetric_four(values: list[float] | tuple[float, ...] | np.ndarray) -> float:
    numbers = np.asarray(values, dtype=float)
    if numbers.ndim != 1 or numbers.size < 4 or np.any(~np.isfinite(numbers)) or np.any(numbers < 0.0):
        raise ValueError("values must be a finite nonnegative vector of length at least four")
    return float(math.fsum(float(np.prod(numbers[list(index)])) for index in combinations(range(numbers.size), 4)))


def spectral_concentration(values: list[float] | tuple[float, ...] | np.ndarray) -> float:
    """Return kappa_4=e4(s^2)/(s1^2 s2^2 s3^2 s4^2)."""
    singular = _spectrum(values)
    denominator = float(np.prod(singular[:4] ** 2))
    if denominator == 0.0:
        return math.inf
    return elementary_symmetric_four(singular**2) / denominator


def concentration_upper_bound(
    recent_singular_values: list[float] | tuple[float, ...] | np.ndarray,
    tail_operator_bound: float,
) -> dict[str, float | int]:
    """Bound kappa using Frobenius tail energy and Weyl endpoints."""
    singular = _spectrum(recent_singular_values)
    delta = float(tail_operator_bound)
    if not math.isfinite(delta) or delta < 0.0:
        raise ValueError("tail radius must be finite and nonnegative")
    rank = singular.size
    lower = np.maximum(singular - delta, 0.0)
    upper = singular + delta
    denominator = float(np.prod(lower[:4] ** 2))
    dimension = exterior_dimension(rank)
    if denominator == 0.0:
        return {"upper": math.inf, "tail_energy_upper": math.inf, "exterior_dimension": dimension}
    frobenius_upper = float(np.linalg.norm(singular) + math.sqrt(rank) * delta)
    tail_energy = max(0.0, frobenius_upper**2 - float(np.sum(lower[:4] ** 2)))
    bound = 0.0
    top_squared = upper[:4] ** 2
    for k in range(0, 5):
        degree = 4 - k
        elementary = 1.0 if degree == 0 else float(
            math.fsum(float(np.prod(top_squared[list(index)])) for index in combinations(range(4), degree))
        )
        bound += elementary * tail_energy**k / math.factorial(k)
    return {
        "upper": min(float(dimension), float(bound / denominator)),
        "tail_energy_upper": tail_energy,
        "exterior_dimension": dimension,
    }


def normalized_trace_lower_bound(
    recent_singular_values: list[float] | tuple[float, ...] | np.ndarray,
    tail_operator_bound: float,
) -> dict[str, float | int]:
    """Use the concentration upper bound to lower-bound normalized spectral volume."""
    singular = _spectrum(recent_singular_values)
    delta = float(tail_operator_bound)
    lower = np.maximum(singular - delta, 0.0)
    upper_leading = float(singular[0] + delta)
    concentration = concentration_upper_bound(singular, delta)
    e4_lower = elementary_symmetric_four(lower**2)
    if upper_leading == 0.0 or not math.isfinite(concentration["upper"]):
        lower_bound = 0.0
    else:
        lower_bound = math.sqrt(e4_lower / concentration["upper"]) / upper_leading**4
    generic = math.sqrt(e4_lower / concentration["exterior_dimension"]) / upper_leading**4 if upper_leading else 0.0
    return {
        "refined_lower": float(lower_bound),
        "generic_lower": float(generic),
        "concentration_upper": float(concentration["upper"]),
        "tail_energy_upper": float(concentration["tail_energy_upper"]),
        "exterior_dimension": int(concentration["exterior_dimension"]),
    }
