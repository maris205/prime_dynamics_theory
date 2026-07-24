from __future__ import annotations

import math

import numpy as np


def _spd_eigenvalues(matrix: np.ndarray) -> np.ndarray:
    array = np.asarray(matrix, dtype=float)
    if array.ndim != 2 or array.shape[0] != array.shape[1]:
        raise ValueError("matrix must be square")
    values = np.linalg.eigvalsh((array + array.T) / 2.0)
    if values[0] <= 0.0:
        raise ValueError("matrix must be positive definite")
    return values


def normalized_base(matrix: np.ndarray) -> float:
    """Return sqrt(lambda_min/lambda_max) for an SPD Gramian."""
    values = _spd_eigenvalues(matrix)
    return float(math.sqrt(values[0] / values[-1]))


def projective_distance(source: np.ndarray, target: np.ndarray) -> float:
    """Hilbert projective distance between two SPD matrices."""
    source_array = np.asarray(source, dtype=float)
    target_array = np.asarray(target, dtype=float)
    values, vectors = np.linalg.eigh((source_array + source_array.T) / 2.0)
    if values[0] <= 0.0:
        raise ValueError("source must be positive definite")
    _spd_eigenvalues(target_array)
    inverse = (vectors / np.sqrt(values)) @ vectors.T
    relative = inverse @ target_array @ inverse
    generalized = np.linalg.eigvalsh((relative + relative.T) / 2.0)
    return float(math.log(generalized[-1] / generalized[0]))


def cumulative_base_lower(initial_base: float, distances: list[float]) -> float:
    """Sharp universal lower obtained by iterating projective steps."""
    if initial_base < 0.0 or any(distance < 0.0 for distance in distances):
        raise ValueError("base and distances must be nonnegative")
    return float(initial_base * math.exp(-0.5 * math.fsum(distances)))

