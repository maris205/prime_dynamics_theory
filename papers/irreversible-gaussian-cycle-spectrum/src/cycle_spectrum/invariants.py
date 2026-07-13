"""Cycle affinities, contraction bounds, traces, and determinant utilities."""

from __future__ import annotations

from collections.abc import Iterable

import numpy as np
from scipy.spatial.distance import pdist
from scipy.special import log_ndtr, ndtr


def _normalizer(mean: float, sigma: float) -> float:
    upper = ndtr((1.0 - mean) / sigma)
    lower = ndtr((-1.0 - mean) / sigma)
    return float(sigma * np.sqrt(2.0 * np.pi) * (upper - lower))


def _truncated_cdf(y: float, mean: float, sigma: float) -> float:
    lower = ndtr((-1.0 - mean) / sigma)
    denominator = ndtr((1.0 - mean) / sigma) - lower
    return float((ndtr((y - mean) / sigma) - lower) / denominator)


def _log_interval_probability(
    lower: float,
    upper: float,
    mean: float,
    sigma: float,
) -> float:
    """Stable log probability of a normal variable lying in an interval."""
    a = (lower - mean) / sigma
    b = (upper - mean) / sigma
    if not a < b:
        raise ValueError("lower endpoint must be smaller than upper endpoint")
    if b <= 0.0:
        log_b = float(log_ndtr(b))
        log_a = float(log_ndtr(a))
        return float(log_b + np.log1p(-np.exp(log_a - log_b)))
    if a >= 0.0:
        log_a_survival = float(log_ndtr(-a))
        log_b_survival = float(log_ndtr(-b))
        return float(
            log_a_survival
            + np.log1p(-np.exp(log_b_survival - log_a_survival))
        )
    omitted = np.exp(float(log_ndtr(a))) + np.exp(float(log_ndtr(-b)))
    return float(np.log1p(-omitted))


def log_kernel(x: float, y: float, u: float, sigma: float) -> float:
    """Logarithm of the normalized continuum kernel ``q(x,y)``."""
    mean = 1.0 - u * x * x
    return float(-0.5 * ((y - mean) / sigma) ** 2 - np.log(_normalizer(mean, sigma)))


def cycle_affinity(x: float, y: float, z: float, u: float, sigma: float) -> float:
    """Closed form for the oriented three-cycle log-ratio."""
    return float(u * (x - y) * (y - z) * (z - x) / (sigma * sigma))


def cycle_affinity_from_kernel(
    x: float,
    y: float,
    z: float,
    u: float,
    sigma: float,
) -> float:
    """Evaluate the same affinity directly from six normalized kernels."""
    forward = (
        log_kernel(x, y, u, sigma)
        + log_kernel(y, z, u, sigma)
        + log_kernel(z, x, u, sigma)
    )
    reverse = (
        log_kernel(x, z, u, sigma)
        + log_kernel(z, y, u, sigma)
        + log_kernel(y, x, u, sigma)
    )
    return float(forward - reverse)


def exact_dobrushin_coefficient(u: float, sigma: float) -> dict[str, float]:
    """Exact one-step coefficient for the full signed-state kernel.

    The Gaussian row mean ranges between ``1`` and ``1-u``.  Equal-variance
    truncated normal rows form a monotone-likelihood-ratio family, so the
    largest total-variation distance occurs at these endpoint means.
    """
    if sigma <= 0.0:
        raise ValueError("sigma must be positive")
    a, b = sorted((1.0, 1.0 - float(u)))
    if a == b:
        return {
            "lower_mean": a,
            "upper_mean": b,
            "crossing": 0.0,
            "delta": 0.0,
            "overlap": 1.0,
            "log10_overlap": 0.0,
        }
    crossing = 0.5 * (a + b) + sigma * sigma * (
        np.log(_normalizer(b, sigma)) - np.log(_normalizer(a, sigma))
    ) / (b - a)
    log_denominator_a = _log_interval_probability(-1.0, 1.0, a, sigma)
    log_denominator_b = _log_interval_probability(-1.0, 1.0, b, sigma)
    log_right_a = (
        _log_interval_probability(crossing, 1.0, a, sigma) - log_denominator_a
    )
    log_left_b = (
        _log_interval_probability(-1.0, crossing, b, sigma) - log_denominator_b
    )
    log_overlap = float(np.logaddexp(log_right_a, log_left_b))
    overlap = float(np.exp(log_overlap))
    delta = float(-np.expm1(log_overlap))
    return {
        "lower_mean": float(a),
        "upper_mean": float(b),
        "crossing": float(crossing),
        "delta": float(np.clip(delta, 0.0, 1.0)),
        "overlap": overlap,
        "log10_overlap": float(log_overlap / np.log(10.0)),
    }


def matrix_dobrushin_coefficient(rows: np.ndarray) -> float:
    """Maximum pairwise row total variation of a stochastic array."""
    rows = np.asarray(rows, dtype=np.float64)
    if rows.ndim != 2:
        raise ValueError("rows must be a two-dimensional array")
    if rows.shape[0] < 2:
        return 0.0
    return float(0.5 * np.max(pdist(rows, metric="cityblock")))


def multistep_dobrushin_roots(
    matrix: np.ndarray,
    steps: int,
    unique_rows: slice | np.ndarray | None = None,
) -> list[dict[str, float | int]]:
    """Compute ``delta(K^n)`` and its ``n``th root for finite matrices."""
    if steps < 1:
        raise ValueError("steps must be positive")
    matrix = np.asarray(matrix, dtype=np.float64)
    active = matrix if unique_rows is None else matrix[unique_rows, :]
    records: list[dict[str, float | int]] = []
    for n in range(1, steps + 1):
        delta = matrix_dobrushin_coefficient(active)
        records.append(
            {
                "step": n,
                "delta": delta,
                "root": float(delta ** (1.0 / n)),
            }
        )
        active = active @ matrix
    return records


def _orders(orders: Iterable[int]) -> tuple[int, ...]:
    result = tuple(sorted(set(int(order) for order in orders)))
    if not result or result[0] < 2:
        raise ValueError("trace orders must be integers at least two")
    return result


def centered_trace_moments(
    matrix: np.ndarray,
    orders: Iterable[int],
) -> dict[int, complex]:
    """Return ``tr(K^n)-1``, the power sums of non-Perron eigenvalues."""
    requested = _orders(orders)
    matrix = np.asarray(matrix)
    power = matrix.copy()
    result: dict[int, complex] = {}
    for n in range(2, requested[-1] + 1):
        power = power @ matrix
        if n in requested:
            result[n] = complex(np.trace(power) - 1.0)
    return result


def centered_trace_derivatives(
    matrix: np.ndarray,
    derivative: np.ndarray,
    orders: Iterable[int],
) -> dict[int, complex]:
    """Return ``n tr(K' K^(n-1))`` for the centered cycle moments."""
    requested = _orders(orders)
    matrix = np.asarray(matrix)
    derivative = np.asarray(derivative)
    power = matrix.copy()
    result: dict[int, complex] = {}
    for n in range(2, requested[-1] + 1):
        if n in requested:
            result[n] = complex(n * np.trace(derivative @ power))
        power = power @ matrix
    return result


def regularized_logabs(
    z: np.ndarray,
    nonperron_eigenvalues: np.ndarray,
) -> np.ndarray:
    """Evaluate ``log|det_2(I-zN)|`` from a finite non-Perron spectrum."""
    values = np.zeros_like(np.asarray(z), dtype=np.float64)
    for eigenvalue in np.asarray(nonperron_eigenvalues):
        values += np.log(np.maximum(np.abs(1.0 - z * eigenvalue), 1.0e-300))
        values += np.real(z * eigenvalue)
    return values
