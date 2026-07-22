"""Phase-coherence lower bounds for block Krylov depth."""

from __future__ import annotations

from dataclasses import dataclass
import math

import numpy as np


@dataclass(frozen=True)
class ProjectionAudit:
    horizon: int
    depth: int
    numerical_rank: int
    projection_error: float
    minimum_gram_eigenvalue: float
    target_correlation_norm: float
    spectral_lower_bound: float
    mutual_coherence: float
    coherence_lower_bound: float


def uniform_ring_phases(dimension: int) -> np.ndarray:
    size = int(dimension)
    if size <= 0:
        raise ValueError("dimension must be positive")
    return 2.0 * np.pi * np.arange(size, dtype=float) / size


def phase_krylov_vectors(
    phases: np.ndarray,
    maximum_power: int,
    weights: np.ndarray | None = None,
) -> np.ndarray:
    """Return normalized vectors sqrt(w_j) exp(i m theta_j)."""

    theta = np.asarray(phases, dtype=float).reshape(-1)
    if theta.size == 0 or not np.all(np.isfinite(theta)):
        raise ValueError("phases must be finite and nonempty")
    power = int(maximum_power)
    if power < 0:
        raise ValueError("maximum power must be nonnegative")
    if weights is None:
        mass = np.full(theta.size, 1.0 / theta.size, dtype=float)
    else:
        mass = np.asarray(weights, dtype=float).reshape(-1)
        if mass.shape != theta.shape or np.any(mass <= 0.0):
            raise ValueError("weights must be positive and match phases")
        mass = mass / np.sum(mass)
    powers = np.arange(power + 1, dtype=float)
    return np.sqrt(mass)[:, None] * np.exp(
        1.0j * np.outer(theta, powers)
    )


def _coherence(gram: np.ndarray) -> float:
    difference = gram - np.eye(gram.shape[0], dtype=np.complex128)
    return float(np.max(np.abs(difference)))


def projection_audit(
    phases: np.ndarray,
    horizon: int,
    depth: int,
    weights: np.ndarray | None = None,
    *,
    tolerance: float = 1.0e-12,
) -> ProjectionAudit:
    """Audit the distance of v_L from span(v_0,...,v_(k-1))."""

    length = int(horizon)
    levels = int(depth)
    if length < 0 or levels <= 0:
        raise ValueError("invalid horizon or depth")
    if levels > length + 1:
        raise ValueError("depth cannot exceed horizon plus one")
    vectors = phase_krylov_vectors(phases, length, weights)
    basis_matrix = vectors[:, :levels]
    left, singular_values, _ = np.linalg.svd(
        basis_matrix,
        full_matrices=False,
    )
    rank = int(
        np.count_nonzero(singular_values > tolerance * singular_values[0])
    )
    basis = left[:, :rank]
    target = vectors[:, length]
    residual = target - basis @ (basis.conjugate().T @ target)
    error = float(np.linalg.norm(residual))
    gram = _hermitian(basis_matrix.conjugate().T @ basis_matrix)
    eigenvalues = np.linalg.eigvalsh(gram)
    lambda_min = max(0.0, float(eigenvalues[0]))
    correlations = basis_matrix.conjugate().T @ target
    correlation_norm = float(np.linalg.norm(correlations))
    if lambda_min > 0.0:
        spectral_lower = math.sqrt(
            max(0.0, 1.0 - correlation_norm**2 / lambda_min)
        )
    else:
        spectral_lower = 0.0
    full_gram = _hermitian(vectors.conjugate().T @ vectors)
    coherence = _coherence(full_gram)
    denominator = 1.0 - (levels - 1) * coherence
    if denominator > 0.0:
        coherence_lower = math.sqrt(
            max(
                0.0,
                1.0 - levels * coherence**2 / denominator,
            )
        )
    else:
        coherence_lower = 0.0
    return ProjectionAudit(
        horizon=length,
        depth=levels,
        numerical_rank=rank,
        projection_error=error,
        minimum_gram_eigenvalue=lambda_min,
        target_correlation_norm=correlation_norm,
        spectral_lower_bound=spectral_lower,
        mutual_coherence=coherence,
        coherence_lower_bound=coherence_lower,
    )


def _hermitian(value: np.ndarray) -> np.ndarray:
    return 0.5 * (value + value.conjugate().T)


def required_depth(
    phases: np.ndarray,
    horizon: int,
    tolerance: float,
    weights: np.ndarray | None = None,
) -> int:
    """First depth whose normalized projection error is at most tolerance."""

    target = float(tolerance)
    if not math.isfinite(target) or not (0.0 <= target < 1.0):
        raise ValueError("tolerance must lie in [0,1)")
    for depth in range(1, int(horizon) + 2):
        if projection_audit(
            phases,
            horizon,
            depth,
            weights,
        ).projection_error <= target:
            return depth
    raise ArithmeticError("target depth was not found")


def arc_phases(dimension: int, width: float) -> np.ndarray:
    size = int(dimension)
    arc = float(width)
    if size <= 0 or not math.isfinite(arc) or arc < 0.0:
        raise ValueError("invalid dimension or arc width")
    if arc == 0.0:
        return np.zeros(size, dtype=float)
    return np.linspace(-arc / 2.0, arc / 2.0, size, endpoint=False)


def jittered_ring_phases(dimension: int, jitter: float) -> np.ndarray:
    size = int(dimension)
    amount = float(jitter)
    if size <= 0 or not math.isfinite(amount) or amount < 0.0:
        raise ValueError("invalid dimension or jitter")
    index = np.arange(size, dtype=float)
    return (
        2.0 * np.pi * index / size
        + 2.0
        * np.pi
        * amount
        * np.sin(2.0 * np.pi * 7.0 * index / size)
        / size
    )
