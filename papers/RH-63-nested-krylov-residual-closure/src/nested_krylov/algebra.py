"""Recursive coherent Arnoldi expansions with a terminal positive remainder."""

from __future__ import annotations

from dataclasses import dataclass
from functools import lru_cache
import math
from typing import Sequence

import numpy as np


def _matrix(value: np.ndarray) -> np.ndarray:
    result = np.asarray(value, dtype=np.complex128)
    if result.ndim != 2 or result.shape[0] != result.shape[1]:
        raise ValueError("operator must be square")
    return result


def _vector(value: np.ndarray, dimension: int) -> np.ndarray:
    result = np.asarray(value, dtype=np.complex128).reshape(-1)
    if result.shape != (dimension,):
        raise ValueError("source has incompatible dimension")
    if np.linalg.norm(result) == 0.0:
        raise ValueError("source must be nonzero")
    return result


@dataclass(frozen=True)
class _ArnoldiLevel:
    source: np.ndarray
    basis: np.ndarray
    hessenberg: np.ndarray
    residual: np.ndarray
    breakdown: bool


@dataclass(frozen=True)
class NestedKrylovCertificate:
    horizon: int
    dimensions: tuple[int, ...]
    exact_norm: float
    approximation_norm: float
    remainder_bound: float
    upper_bound: float
    operator_norm: float
    level_residual_norms: tuple[float, ...]
    terminal_breakdown: bool


def _arnoldi(
    operator: np.ndarray,
    source: np.ndarray,
    dimension: int,
    tolerance: float,
) -> _ArnoldiLevel:
    count = int(dimension)
    if count <= 0 or count > operator.shape[0]:
        raise ValueError("every Krylov dimension must lie in [1,n]")
    source_norm = float(np.linalg.norm(source))
    vectors = [source / source_norm]
    hessenberg = np.zeros((count, count), dtype=np.complex128)
    residual_vector = np.zeros(operator.shape[0], dtype=np.complex128)
    breakdown = False
    for column in range(count):
        work = operator @ vectors[column]
        for row, vector in enumerate(vectors):
            coefficient = np.vdot(vector, work)
            hessenberg[row, column] = coefficient
            work -= coefficient * vector
        residual_norm = float(np.linalg.norm(work))
        if column == count - 1:
            if residual_norm > tolerance:
                residual_vector = work
            else:
                breakdown = True
            break
        if residual_norm <= tolerance:
            breakdown = True
            break
        hessenberg[column + 1, column] = residual_norm
        vectors.append(work / residual_norm)
    basis = np.column_stack(vectors)
    return _ArnoldiLevel(
        source=source,
        basis=basis,
        hessenberg=hessenberg[: basis.shape[1], : basis.shape[1]],
        residual=residual_vector,
        breakdown=breakdown,
    )


def nested_krylov_certificate(
    operator: np.ndarray,
    source: np.ndarray,
    horizon: int,
    dimensions: Sequence[int],
    *,
    operator_norm: float | None = None,
    tolerance: float = 1.0e-13,
) -> NestedKrylovCertificate:
    r"""Coherently expand Arnoldi residuals through several levels.

    Every level contributes its projected vector to one common approximation.
    Only the final unexpanded residual is bounded by an ordinary norm power.
    """

    a = _matrix(operator)
    z = _vector(source, a.shape[0])
    length = int(horizon)
    if length < 0:
        raise ValueError("horizon must be nonnegative")
    schedule = tuple(int(value) for value in dimensions)
    if not schedule:
        raise ValueError("at least one Krylov dimension is required")
    threshold = float(tolerance)
    if not math.isfinite(threshold) or threshold <= 0.0:
        raise ValueError("tolerance must be finite and positive")
    rho = float(np.linalg.norm(a, 2) if operator_norm is None else operator_norm)
    if not math.isfinite(rho) or rho < 0.0:
        raise ValueError("operator_norm must be finite and nonnegative")

    levels: list[_ArnoldiLevel] = []
    current = z
    for dimension in schedule:
        level = _arnoldi(a, current, dimension, threshold)
        levels.append(level)
        if level.breakdown:
            break
        current = level.residual
    terminal_source = current

    @lru_cache(maxsize=None)
    def expand(level_index: int, power: int) -> tuple[np.ndarray, float]:
        if level_index >= len(levels):
            return (
                np.zeros(a.shape[0], dtype=np.complex128),
                float(rho**power * np.linalg.norm(terminal_source)),
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
    exact = float(np.linalg.norm(np.linalg.matrix_power(a, length) @ z))
    approximation_norm = float(np.linalg.norm(approximation))
    return NestedKrylovCertificate(
        horizon=length,
        dimensions=schedule[: len(levels)],
        exact_norm=exact,
        approximation_norm=approximation_norm,
        remainder_bound=remainder,
        upper_bound=approximation_norm + remainder,
        operator_norm=rho,
        level_residual_norms=tuple(
            float(np.linalg.norm(level.residual)) for level in levels
        ),
        terminal_breakdown=levels[-1].breakdown,
    )
