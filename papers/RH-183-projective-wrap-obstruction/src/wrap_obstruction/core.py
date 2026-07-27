"""Exact phase-optimized wrap identities for normalized temporal clocks."""

from __future__ import annotations

import math

import numpy as np


def unit_inner(seed: np.ndarray, endpoint: np.ndarray) -> complex:
    left = np.asarray(seed).reshape(-1)
    right = np.asarray(endpoint).reshape(-1)
    if not math.isclose(float(np.linalg.norm(left)), 1.0, rel_tol=1e-10, abs_tol=1e-10):
        raise ValueError("seed must be normalized")
    if not math.isclose(float(np.linalg.norm(right)), 1.0, rel_tol=1e-10, abs_tol=1e-10):
        raise ValueError("endpoint must be normalized")
    return complex(np.vdot(left, right))


def optimal_wrap_phase(seed: np.ndarray, endpoint: np.ndarray) -> complex:
    inner = unit_inner(seed, endpoint)
    return 1.0 + 0.0j if abs(inner) <= np.finfo(float).tiny else inner / abs(inner)


def phase_optimized_chord(seed: np.ndarray, endpoint: np.ndarray) -> float:
    inner = unit_inner(seed, endpoint)
    return math.sqrt(max(0.0, 2.0 - 2.0 * min(1.0, abs(inner))))


def projective_return_distance(seed: np.ndarray, endpoint: np.ndarray) -> float:
    inner = unit_inner(seed, endpoint)
    return math.sqrt(max(0.0, 1.0 - min(1.0, abs(inner)) ** 2))


def best_scalar_wrap_residual(
    seed: np.ndarray,
    endpoint: np.ndarray,
    amplitude: float,
) -> dict[str, float | complex]:
    scale = float(amplitude)
    if scale < 0.0:
        raise ValueError("amplitude must be nonnegative")
    inner = unit_inner(seed, endpoint)
    coefficient = scale * inner
    residual = scale * math.sqrt(max(0.0, 1.0 - min(1.0, abs(inner)) ** 2))
    return {
        "optimal_scalar": coefficient,
        "minimum_residual": residual,
        "projective_distance": projective_return_distance(seed, endpoint),
    }


def polar_wrap_bounds(
    amplitude: float,
    chord: float,
    smallest_gram_eigenvalue: float,
    largest_gram_eigenvalue: float,
) -> dict[str, float]:
    weight = float(amplitude)
    distance = float(chord)
    lower_eigenvalue = float(smallest_gram_eigenvalue)
    upper_eigenvalue = float(largest_gram_eigenvalue)
    if min(weight, distance, lower_eigenvalue, upper_eigenvalue) < 0.0 or lower_eigenvalue == 0.0:
        raise ValueError("invalid wrap-bound data")
    if upper_eigenvalue < lower_eigenvalue:
        raise ValueError("Gram eigenvalues are reversed")
    return {
        "lower_bound": weight * distance / math.sqrt(upper_eigenvalue),
        "upper_bound": weight * distance / math.sqrt(lower_eigenvalue),
    }
