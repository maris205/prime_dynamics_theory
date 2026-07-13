"""Folded midpoint matrices for normalized Gaussian quadratic kernels."""

from __future__ import annotations

import numpy as np


def positive_midpoints(dimension: int) -> np.ndarray:
    """Midpoints of ``[0,1]`` for the exact even-state folding."""

    if dimension < 2:
        raise ValueError("dimension must be at least two")
    return (np.arange(dimension, dtype=np.float64) + 0.5) / dimension


def folded_gaussian_matrix(dimension: int, u: float, sigma: float) -> np.ndarray:
    """Return the folded row-stochastic midpoint matrix.

    ``dimension`` is the positive-half dimension; the corresponding full
    midpoint discretization has size ``2*dimension``.
    """

    if sigma <= 0.0:
        raise ValueError("sigma must be positive")
    grid = positive_midpoints(int(dimension))
    means = 1.0 - float(u) * grid * grid
    destination = grid[None, :]
    mean = means[:, None]
    log_positive = -0.5 * ((destination - mean) / float(sigma)) ** 2
    log_negative = -0.5 * ((-destination - mean) / float(sigma)) ** 2
    log_weights = np.logaddexp(log_positive, log_negative)
    log_weights -= np.max(log_weights, axis=1, keepdims=True)
    weights = np.exp(log_weights)
    return weights / np.sum(weights, axis=1, keepdims=True)


def trace_three(first: np.ndarray, second: np.ndarray, third: np.ndarray) -> float:
    """Compute ``tr(first second third)`` with one dense product."""

    product = np.asarray(first) @ np.asarray(second)
    return float(np.sum(product * np.asarray(third).T))


def directed_matrix_trace(
    first: np.ndarray,
    second: np.ndarray,
    third: np.ndarray,
    *,
    block_length: int = 1,
) -> float:
    """Return the finite-matrix forward-minus-reversed directed trace."""

    if block_length not in (1, 2):
        raise ValueError("the audited block lengths are one and two")
    first = np.asarray(first)
    second = np.asarray(second)
    third = np.asarray(third)
    if block_length == 2:
        first = first @ first
        second = second @ second
        third = third @ third
    return trace_three(first, second, third) - trace_three(first, third, second)


def autonomous_cycle_traces(matrix: np.ndarray) -> tuple[float, float]:
    """Return the third- and sixth-power traces using three products."""

    matrix = np.asarray(matrix)
    square = matrix @ matrix
    cube = square @ matrix
    sixth = cube @ cube
    return float(np.trace(cube)), float(np.trace(sixth))
