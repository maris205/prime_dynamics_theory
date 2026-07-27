"""Counting diagnostics for fixed and repeatedly powered finite divisors."""

from __future__ import annotations

import numpy as np


def canonical_shape_roots(u: float, eta: float) -> np.ndarray:
    axial = float(u)
    asymmetry = float(eta)
    if not (0.0 <= axial <= 1.0 and -1.0 <= asymmetry <= 1.0):
        raise ValueError("coordinates lie outside the shape rectangle")
    a = np.sqrt(axial)
    b = np.sqrt((1.0 - axial) * (1.0 + asymmetry))
    d = np.sqrt((1.0 - axial) * (1.0 - asymmetry))
    return np.asarray([a + 1j * b, a - 1j * b, -a + 1j * d, -a - 1j * d])


def height_count(roots: np.ndarray, height: float, multiplicity: int = 1) -> int:
    values = np.asarray(roots, dtype=complex).reshape(-1)
    copies = int(multiplicity)
    if copies < 1 or height < 0.0:
        raise ValueError("positive multiplicity and nonnegative height are required")
    return copies * int(np.sum(np.abs(values.imag) <= float(height)))


def distinct_support_count(roots: np.ndarray, tolerance: float = 1.0e-10) -> int:
    values = list(np.asarray(roots, dtype=complex).reshape(-1))
    representatives: list[complex] = []
    for value in values:
        if not any(abs(value - existing) <= tolerance for existing in representatives):
            representatives.append(complex(value))
    return len(representatives)


def normalized_power_values(
    roots: np.ndarray,
    exponent: int,
    evaluation_points: np.ndarray,
    basepoint: complex,
) -> np.ndarray:
    values = np.asarray(roots, dtype=complex).reshape(-1)
    points = np.asarray(evaluation_points, dtype=complex)
    power = int(exponent)
    if power < 1:
        raise ValueError("a positive exponent is required")
    q_base = np.prod(complex(basepoint) - values)
    if abs(q_base) <= np.finfo(float).tiny:
        raise ValueError("the basepoint must avoid the divisor")
    q_points = np.prod(points[..., None] - values, axis=-1)
    return (q_points / q_base) ** power


def finite_degree_count_bound(degree: int) -> int:
    size = int(degree)
    if size < 0:
        raise ValueError("degree must be nonnegative")
    return size


def repeated_profile(roots: np.ndarray, exponents: tuple[int, ...], heights: np.ndarray) -> list[dict[str, object]]:
    values = np.asarray(roots, dtype=complex).reshape(-1)
    levels = np.asarray(heights, dtype=float)
    rows = []
    for exponent in exponents:
        rows.append({
            "exponent": int(exponent),
            "degree_counting_multiplicity": int(exponent) * values.size,
            "distinct_support_count": distinct_support_count(values),
            "height_counts": [height_count(values, height, int(exponent)) for height in levels],
        })
    return rows
