"""Gaussian quadratic midpoint operators and exact parameter derivatives."""

from __future__ import annotations

import numpy as np
import scipy.linalg as la


def grid_centers(d: int) -> np.ndarray:
    if d < 2:
        raise ValueError("d must be at least two")
    return -1.0 + 2.0 * (np.arange(d, dtype=np.float64) + 0.5) / d


def fold_matrix(matrix: np.ndarray) -> np.ndarray:
    """Fold a symmetric full-state matrix to positive absolute states."""
    matrix = np.asarray(matrix)
    if matrix.ndim != 2 or matrix.shape[0] != matrix.shape[1]:
        raise ValueError("matrix must be square")
    d = matrix.shape[0]
    if d % 2:
        raise ValueError("folding requires an even dimension")
    m = d // 2
    return matrix[m:, m:] + matrix[m:, :m][:, ::-1]


def gaussian_markov_family(
    d: int,
    u: float,
    sigma: float,
    *,
    folded: bool = True,
) -> tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray]:
    """Return grid, ``K``, ``K'``, and ``K''`` for the normalized kernel."""
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
    variance = np.sum(matrix * score * score, axis=1, keepdims=True)
    first = matrix * score
    second = matrix * (score * score - variance)

    if not folded:
        return centers, matrix, first, second
    m = d // 2
    return centers[m:], fold_matrix(matrix), fold_matrix(first), fold_matrix(second)


def gaussian_markov_matrix(
    d: int,
    u: float,
    sigma: float,
    *,
    folded: bool = True,
) -> np.ndarray:
    return gaussian_markov_family(d, u, sigma, folded=folded)[1]


def stationary_distribution(matrix: np.ndarray) -> np.ndarray:
    """Compute the normalized positive left Perron vector of a dense matrix."""
    eigenvalues, eigenvectors = la.eig(np.asarray(matrix).T)
    index = int(np.argmin(np.abs(eigenvalues - 1.0)))
    vector = np.real_if_close(eigenvectors[:, index], tol=1000).real
    if np.sum(vector) < 0.0:
        vector = -vector
    vector /= np.sum(vector)
    return vector


def nonperron_spectrum(matrix: np.ndarray) -> np.ndarray:
    values = la.eigvals(np.asarray(matrix))
    return np.delete(values, int(np.argmin(np.abs(values - 1.0))))
