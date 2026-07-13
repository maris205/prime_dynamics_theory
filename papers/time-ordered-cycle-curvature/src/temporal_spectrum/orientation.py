"""Commutator responses and minimal directed cycle traces."""

from __future__ import annotations

import numpy as np


def commutator(left: np.ndarray, right: np.ndarray) -> np.ndarray:
    return np.asarray(left) @ np.asarray(right) - np.asarray(right) @ np.asarray(left)


def orientation_trace(
    first: np.ndarray,
    second: np.ndarray,
    third: np.ndarray,
) -> complex:
    """Return ``tr(ABC)-tr(ACB) = tr(A[B,C])``."""
    first = np.asarray(first)
    second = np.asarray(second)
    third = np.asarray(third)
    return complex(np.trace(first @ (second @ third - third @ second)))


def vandermonde(a: float, b: float, c: float) -> float:
    """Alternating parameter factor used throughout the paper."""
    return float((a - b) * (b - c) * (c - a))


def orientation_curvature(
    matrix: np.ndarray,
    first: np.ndarray,
    second: np.ndarray,
) -> complex:
    """Diagonal quotient ``1/2 tr(K [K',K''])``."""
    return 0.5 * orientation_trace(matrix, first, second)


def parity_block_family(
    matrix: np.ndarray,
    first: np.ndarray,
    second: np.ndarray,
) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    """Return ``Q=K^2`` and its first two parameter derivatives."""
    matrix = np.asarray(matrix)
    first = np.asarray(first)
    second = np.asarray(second)
    block = matrix @ matrix
    block_first = first @ matrix + matrix @ first
    block_second = second @ matrix + 2.0 * first @ first + matrix @ second
    return block, block_first, block_second


def parity_orientation_curvature(
    matrix: np.ndarray,
    first: np.ndarray,
    second: np.ndarray,
) -> complex:
    block, block_first, block_second = parity_block_family(matrix, first, second)
    return orientation_curvature(block, block_first, block_second)


def matrix_infinity_norm(matrix: np.ndarray) -> float:
    return float(np.max(np.sum(np.abs(np.asarray(matrix)), axis=1)))


def matched_spectrum_error(
    first: np.ndarray,
    second: np.ndarray,
    *,
    threshold: float = 1.0e-7,
) -> dict[str, float | int]:
    """Match significant eigenvalues of two finite matrices by proximity."""
    import scipy.linalg as la

    values_first = la.eigvals(np.asarray(first))
    values_second = la.eigvals(np.asarray(second))
    significant = values_first[np.abs(values_first) > threshold]
    errors = [float(np.min(np.abs(values_second - value))) for value in significant]
    return {
        "significant_count": len(significant),
        "maximum_match_error": max(errors, default=0.0),
    }
