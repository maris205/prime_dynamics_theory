"""Dense midpoint operators and the exact even-state folding reduction."""

from __future__ import annotations

import numpy as np
import scipy.linalg as la


def grid_centers(d: int) -> np.ndarray:
    """Return the midpoint grid on ``[-1, 1]``."""
    if d < 2:
        raise ValueError("d must be at least two")
    return -1.0 + 2.0 * (np.arange(d, dtype=np.float64) + 0.5) / d


def gaussian_markov_family(
    d: int,
    u: float,
    sigma: float,
) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    """Build the full row-stochastic midpoint matrix and its ``u`` derivative.

    The derivative uses the exactly centered Gaussian score, so every row of
    the derivative sums to zero up to floating-point roundoff.
    """
    if sigma <= 0.0:
        raise ValueError("sigma must be positive")
    centers = grid_centers(d)
    source_squares = centers * centers
    means = 1.0 - float(u) * source_squares
    residual = centers[None, :] - means[:, None]
    log_weights = -0.5 * (residual / float(sigma)) ** 2
    log_weights -= np.max(log_weights, axis=1, keepdims=True)
    weights = np.exp(log_weights)
    matrix = weights / np.sum(weights, axis=1, keepdims=True)

    score = -source_squares[:, None] * residual / (float(sigma) ** 2)
    score -= np.sum(matrix * score, axis=1, keepdims=True)
    derivative = matrix * score
    return centers, matrix, derivative


def gaussian_markov_matrix(d: int, u: float, sigma: float) -> np.ndarray:
    """Build only the full Gaussian quadratic Markov matrix."""
    return gaussian_markov_family(d, u, sigma)[1]


def fold_matrix(matrix: np.ndarray) -> np.ndarray:
    """Restrict an even-row matrix to observables on ``[0, 1]``.

    For a symmetric midpoint grid with ``d=2m``, positive destination cell
    ``j`` is paired with its reflected negative cell.  The resulting ``m`` by
    ``m`` matrix has exactly the nonzero spectrum of the full quadratic
    matrix in exact arithmetic.
    """
    matrix = np.asarray(matrix)
    if matrix.ndim != 2 or matrix.shape[0] != matrix.shape[1]:
        raise ValueError("matrix must be square")
    d = matrix.shape[0]
    if d % 2:
        raise ValueError("folding requires an even dimension")
    m = d // 2
    positive_source_rows = matrix[m:, :]
    return positive_source_rows[:, m:] + positive_source_rows[:, :m][:, ::-1]


def nonperron_spectrum(matrix: np.ndarray) -> np.ndarray:
    """Return all eigenvalues except the one closest to the Perron root one."""
    eigenvalues = la.eigvals(np.asarray(matrix))
    perron_index = int(np.argmin(np.abs(eigenvalues - 1.0)))
    return np.delete(eigenvalues, perron_index)


def conditioned_eigenvalues(matrix: np.ndarray) -> tuple[np.ndarray, np.ndarray]:
    """Return eigenvalues and left-right eigenvalue condition numbers."""
    eigenvalues, left, right = la.eig(np.asarray(matrix), left=True, right=True)
    left_norms = np.linalg.norm(left, axis=0)
    right_norms = np.linalg.norm(right, axis=0)
    overlaps = np.abs(np.sum(np.conjugate(left) * right, axis=0))
    conditions = left_norms * right_norms / np.maximum(overlaps, np.finfo(float).tiny)
    return eigenvalues, conditions
