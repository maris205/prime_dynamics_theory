"""Nested Arnoldi certificates with a positive weighted residual norm."""

from __future__ import annotations

from dataclasses import dataclass
from functools import lru_cache
import math
from typing import Sequence

import numpy as np
from scipy.linalg import solve_discrete_lyapunov


@dataclass(frozen=True)
class WeightedKrylovCertificate:
    horizon: int
    dimensions: tuple[int, ...]
    exact_metric_norm: float
    approximation_metric_norm: float
    terminal_remainder_bound: float
    upper_bound: float
    metric_contraction: float
    euclidean_operator_norm: float
    terminal_breakdown: bool


@dataclass(frozen=True)
class _Level:
    source: np.ndarray
    basis: np.ndarray
    hessenberg: np.ndarray
    residual: np.ndarray
    breakdown: bool


def _square(value: np.ndarray) -> np.ndarray:
    result = np.asarray(value, dtype=np.complex128)
    if result.ndim != 2 or result.shape[0] != result.shape[1]:
        raise ValueError("operator must be square")
    return result


def _nonzero_vector(value: np.ndarray, dimension: int) -> np.ndarray:
    result = np.asarray(value, dtype=np.complex128).reshape(-1)
    if result.shape != (dimension,) or np.linalg.norm(result) == 0.0:
        raise ValueError("source must be a nonzero matching vector")
    return result


def _arnoldi(
    operator: np.ndarray,
    source: np.ndarray,
    dimension: int,
    tolerance: float,
) -> _Level:
    if dimension <= 0 or dimension > operator.shape[0]:
        raise ValueError("Krylov dimension is out of range")
    vectors = [source / np.linalg.norm(source)]
    hessenberg = np.zeros((dimension, dimension), dtype=np.complex128)
    residual = np.zeros(operator.shape[0], dtype=np.complex128)
    breakdown = False
    for column in range(dimension):
        work = operator @ vectors[column]
        for row, vector in enumerate(vectors):
            coefficient = np.vdot(vector, work)
            hessenberg[row, column] = coefficient
            work -= coefficient * vector
        size = float(np.linalg.norm(work))
        if column == dimension - 1:
            if size > tolerance:
                residual = work
            else:
                breakdown = True
            break
        if size <= tolerance:
            breakdown = True
            break
        hessenberg[column + 1, column] = size
        vectors.append(work / size)
    basis = np.column_stack(vectors)
    return _Level(
        source=source,
        basis=basis,
        hessenberg=hessenberg[: basis.shape[1], : basis.shape[1]],
        residual=residual,
        breakdown=breakdown,
    )


def lyapunov_metric(operator: np.ndarray) -> np.ndarray:
    """Return the positive solution of M-A^*MA=I for a stable matrix."""

    a = _square(operator)
    metric = solve_discrete_lyapunov(
        a.conjugate().T,
        np.eye(a.shape[0], dtype=np.complex128),
    )
    metric = 0.5 * (metric + metric.conjugate().T)
    if np.min(np.linalg.eigvalsh(metric)) <= 0.0:
        raise ValueError("Lyapunov metric is not positive")
    return metric


def _metric_root(metric: np.ndarray) -> tuple[np.ndarray, np.ndarray]:
    eigenvalues, vectors = np.linalg.eigh(metric)
    if np.min(eigenvalues) <= 0.0:
        raise ValueError("metric must be positive definite")
    root = (vectors * np.sqrt(eigenvalues)) @ vectors.conjugate().T
    inverse = (
        vectors * (1.0 / np.sqrt(eigenvalues))
    ) @ vectors.conjugate().T
    return root, inverse


def metric_contraction(operator: np.ndarray, metric: np.ndarray) -> float:
    """Return the operator norm in the positive metric."""

    a = _square(operator)
    root, inverse = _metric_root(metric)
    return float(np.linalg.norm(root @ a @ inverse, 2))


def weighted_nested_certificate(
    operator: np.ndarray,
    source: np.ndarray,
    metric: np.ndarray,
    horizon: int,
    dimensions: Sequence[int],
    *,
    tolerance: float = 1.0e-13,
) -> WeightedKrylovCertificate:
    """Build a coherent nested certificate in the metric norm."""

    a = _square(operator)
    z = _nonzero_vector(source, a.shape[0])
    m = _square(metric)
    if m.shape != a.shape:
        raise ValueError("metric has incompatible shape")
    length = int(horizon)
    if length < 0:
        raise ValueError("horizon must be nonnegative")
    schedule = tuple(int(value) for value in dimensions)
    if not schedule:
        raise ValueError("at least one Krylov dimension is required")
    threshold = float(tolerance)
    if not math.isfinite(threshold) or threshold <= 0.0:
        raise ValueError("tolerance must be finite and positive")
    root, _ = _metric_root(m)
    q = metric_contraction(a, m)

    levels = []
    current = z
    for dimension in schedule:
        level = _arnoldi(a, current, dimension, threshold)
        levels.append(level)
        if level.breakdown:
            break
        current = level.residual
    terminal_source = current

    def metric_norm(value: np.ndarray) -> float:
        return float(np.linalg.norm(root @ value))

    @lru_cache(maxsize=None)
    def expand(level_index: int, power: int) -> tuple[np.ndarray, float]:
        if level_index >= len(levels):
            return (
                np.zeros(a.shape[0], dtype=np.complex128),
                q**power * metric_norm(terminal_source),
            )
        level = levels[level_index]
        beta = np.zeros(level.basis.shape[1], dtype=np.complex128)
        beta[0] = np.linalg.norm(level.source)
        projected = level.basis @ (
            np.linalg.matrix_power(level.hessenberg, power) @ beta
        )
        if level.breakdown or power == 0:
            return projected, 0.0
        approximation = projected.copy()
        remainder = 0.0
        power_h = np.eye(level.hessenberg.shape[0], dtype=np.complex128)
        selector = np.zeros(level.hessenberg.shape[0], dtype=np.complex128)
        selector[-1] = 1.0
        for index in range(power):
            coefficient = np.vdot(selector, power_h @ beta)
            child_vector, child_remainder = expand(
                level_index + 1, power - 1 - index
            )
            approximation += coefficient * child_vector
            remainder += abs(coefficient) * child_remainder
            power_h = level.hessenberg @ power_h
        return approximation, float(remainder)

    approximation, remainder = expand(0, length)
    exact = metric_norm(np.linalg.matrix_power(a, length) @ z)
    approximation_norm = metric_norm(approximation)
    return WeightedKrylovCertificate(
        horizon=length,
        dimensions=schedule[: len(levels)],
        exact_metric_norm=exact,
        approximation_metric_norm=approximation_norm,
        terminal_remainder_bound=remainder,
        upper_bound=approximation_norm + remainder,
        metric_contraction=q,
        euclidean_operator_norm=float(np.linalg.norm(a, 2)),
        terminal_breakdown=levels[-1].breakdown,
    )
