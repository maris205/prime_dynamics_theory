"""Cross-column block Krylov Gram certificates."""

from __future__ import annotations

from dataclasses import dataclass
import math

import numpy as np
from scipy.linalg import solve_discrete_lyapunov


@dataclass(frozen=True)
class BlockGramCertificate:
    """A coherent center, residual Gram radius, and PSD envelope."""

    horizon: int
    depth: int
    source_columns: int
    krylov_rank: int
    metric_contraction: float
    exact_gram: np.ndarray
    center_gram: np.ndarray
    residual_gram_upper: np.ndarray
    gram_envelope: np.ndarray
    trace_eta: float
    residual_relation_norm: float
    source_reconstruction_norm: float


@dataclass(frozen=True)
class DirectionalCertificate:
    exact_energy: float
    center_energy: float
    residual_radius: float
    upper_energy: float
    coefficient_norm: float


def _square(value: np.ndarray, name: str) -> np.ndarray:
    result = np.asarray(value, dtype=np.complex128)
    if result.ndim != 2 or result.shape[0] != result.shape[1]:
        raise ValueError(f"{name} must be square")
    return result


def _sources(value: np.ndarray, rows: int) -> np.ndarray:
    result = np.asarray(value, dtype=np.complex128)
    if result.ndim == 1:
        result = result.reshape(-1, 1)
    if result.ndim != 2 or result.shape[0] != rows or result.shape[1] == 0:
        raise ValueError("sources must be a nonempty matching matrix")
    if np.linalg.norm(result) == 0.0:
        raise ValueError("sources must be nonzero")
    return result


def _hermitian(value: np.ndarray) -> np.ndarray:
    return 0.5 * (value + value.conjugate().T)


def lyapunov_metric(operator: np.ndarray) -> np.ndarray:
    """Canonical positive metric M-A^*MA=I."""

    a = _square(operator, "operator")
    if np.max(np.abs(np.linalg.eigvals(a))) >= 1.0:
        raise ValueError("operator must be stable")
    metric = solve_discrete_lyapunov(
        a.conjugate().T,
        np.eye(a.shape[0], dtype=np.complex128),
    )
    metric = _hermitian(metric)
    if np.min(np.linalg.eigvalsh(metric)) <= 0.0:
        raise ArithmeticError("Lyapunov metric is not positive")
    return metric


def _metric_root(metric: np.ndarray) -> tuple[np.ndarray, np.ndarray]:
    eigenvalues, vectors = np.linalg.eigh(_hermitian(metric))
    if np.min(eigenvalues) <= 0.0:
        raise ValueError("metric must be positive definite")
    root = (vectors * np.sqrt(eigenvalues)) @ vectors.conjugate().T
    inverse = (
        vectors * (1.0 / np.sqrt(eigenvalues))
    ) @ vectors.conjugate().T
    return root, inverse


def metric_contraction(operator: np.ndarray, metric: np.ndarray) -> float:
    a = _square(operator, "operator")
    m = _square(metric, "metric")
    if a.shape != m.shape:
        raise ValueError("operator and metric dimensions must agree")
    root, inverse = _metric_root(m)
    return float(np.linalg.norm(root @ a @ inverse, 2))


def block_krylov_basis(
    operator: np.ndarray,
    sources: np.ndarray,
    depth: int,
    *,
    tolerance: float = 1.0e-12,
) -> np.ndarray:
    """Orthonormal basis of span{Z,AZ,...,A^(depth-1)Z}."""

    a = _square(operator, "operator")
    z = _sources(sources, a.shape[0])
    levels = int(depth)
    if levels <= 0:
        raise ValueError("depth must be positive")
    threshold = float(tolerance)
    if not math.isfinite(threshold) or threshold <= 0.0:
        raise ValueError("tolerance must be finite and positive")
    blocks = []
    current = z.copy()
    for _ in range(levels):
        blocks.append(current)
        current = a @ current
    concatenated = np.column_stack(blocks)
    left, singular_values, _ = np.linalg.svd(
        concatenated,
        full_matrices=False,
    )
    if singular_values.size == 0 or singular_values[0] == 0.0:
        raise ArithmeticError("block Krylov matrix has zero rank")
    rank = int(np.count_nonzero(singular_values > threshold * singular_values[0]))
    if rank == 0:
        raise ArithmeticError("block Krylov rank was truncated to zero")
    return left[:, :rank]


def _trace_real(value: np.ndarray) -> float:
    return max(0.0, float(np.real(np.trace(value))))


def _residual_terms(
    hessenberg: np.ndarray,
    source_coordinates: np.ndarray,
    horizon: int,
) -> list[tuple[int, np.ndarray]]:
    terms = []
    power = np.eye(hessenberg.shape[0], dtype=np.complex128)
    for index in range(horizon):
        terms.append((horizon - 1 - index, power @ source_coordinates))
        power = hessenberg @ power
    return terms


def block_gram_certificate(
    operator: np.ndarray,
    sources: np.ndarray,
    metric: np.ndarray,
    horizon: int,
    depth: int,
    *,
    tolerance: float = 1.0e-12,
) -> BlockGramCertificate:
    """Build a phase-preserving PSD Gram envelope."""

    a = _square(operator, "operator")
    z = _sources(sources, a.shape[0])
    m = _square(metric, "metric")
    if m.shape != a.shape:
        raise ValueError("metric has incompatible shape")
    length = int(horizon)
    if length < 0:
        raise ValueError("horizon must be nonnegative")
    basis = block_krylov_basis(
        a,
        z,
        depth,
        tolerance=tolerance,
    )
    source_coordinates = basis.conjugate().T @ z
    projected = basis.conjugate().T @ a @ basis
    residual = a @ basis - basis @ projected
    source_reconstruction = z - basis @ source_coordinates
    center = basis @ (
        np.linalg.matrix_power(projected, length) @ source_coordinates
    )
    exact = np.linalg.matrix_power(a, length) @ z
    exact_gram = _hermitian(exact.conjugate().T @ m @ exact)
    center_gram = _hermitian(center.conjugate().T @ m @ center)
    residual_metric_gram = _hermitian(
        residual.conjugate().T @ m @ residual
    )
    contraction = metric_contraction(a, m)
    terms = _residual_terms(projected, source_coordinates, length)
    scales = []
    pieces = []
    for power, coordinates in terms:
        piece = _hermitian(
            coordinates.conjugate().T
            @ residual_metric_gram
            @ coordinates
        )
        scale = contraction**power * math.sqrt(_trace_real(piece))
        scales.append(scale)
        pieces.append((power, piece))
    source_piece = _hermitian(
        source_reconstruction.conjugate().T @ m @ source_reconstruction
    )
    source_scale = contraction**length * math.sqrt(
        _trace_real(source_piece)
    )
    scales.append(source_scale)
    pieces.append((length, source_piece))
    scale_sum = sum(scales)
    residual_upper = np.zeros_like(exact_gram)
    if scale_sum > 0.0:
        for scale, (power, piece) in zip(scales, pieces, strict=True):
            if scale == 0.0:
                continue
            theta = scale / scale_sum
            residual_upper += contraction ** (2 * power) * piece / theta
    residual_upper = _hermitian(residual_upper)
    center_trace = _trace_real(center_gram)
    residual_trace = _trace_real(residual_upper)
    if residual_trace == 0.0:
        eta = 0.0
        envelope = center_gram.copy()
    elif center_trace == 0.0:
        eta = math.inf
        envelope = residual_upper.copy()
    else:
        eta = math.sqrt(residual_trace / center_trace)
        envelope = (
            (1.0 + eta) * center_gram
            + (1.0 + 1.0 / eta) * residual_upper
        )
    return BlockGramCertificate(
        horizon=length,
        depth=int(depth),
        source_columns=z.shape[1],
        krylov_rank=basis.shape[1],
        metric_contraction=contraction,
        exact_gram=exact_gram,
        center_gram=center_gram,
        residual_gram_upper=residual_upper,
        gram_envelope=_hermitian(envelope),
        trace_eta=eta,
        residual_relation_norm=float(np.linalg.norm(residual)),
        source_reconstruction_norm=float(np.linalg.norm(source_reconstruction)),
    )


def directional_certificate(
    operator: np.ndarray,
    sources: np.ndarray,
    metric: np.ndarray,
    horizon: int,
    depth: int,
    coefficients: np.ndarray,
    *,
    tolerance: float = 1.0e-12,
) -> DirectionalCertificate:
    """Return the tighter center-radius certificate for one packet vector."""

    a = _square(operator, "operator")
    z = _sources(sources, a.shape[0])
    m = _square(metric, "metric")
    coeff = np.asarray(coefficients, dtype=np.complex128).reshape(-1)
    if coeff.shape != (z.shape[1],) or np.linalg.norm(coeff) == 0.0:
        raise ValueError("coefficients must be a nonzero matching vector")
    length = int(horizon)
    if length < 0:
        raise ValueError("horizon must be nonnegative")
    basis = block_krylov_basis(
        a,
        z,
        depth,
        tolerance=tolerance,
    )
    source_coordinates = basis.conjugate().T @ z
    projected = basis.conjugate().T @ a @ basis
    residual = a @ basis - basis @ projected
    source_reconstruction = z - basis @ source_coordinates
    center = basis @ (
        np.linalg.matrix_power(projected, length)
        @ source_coordinates
        @ coeff
    )
    exact = np.linalg.matrix_power(a, length) @ z @ coeff
    residual_metric_gram = _hermitian(
        residual.conjugate().T @ m @ residual
    )
    contraction = metric_contraction(a, m)
    radius = 0.0
    for power, coordinates in _residual_terms(
        projected,
        source_coordinates,
        length,
    ):
        vector = coordinates @ coeff
        size_squared = max(
            0.0,
            float(np.real(np.vdot(vector, residual_metric_gram @ vector))),
        )
        radius += contraction**power * math.sqrt(size_squared)
    source_vector = source_reconstruction @ coeff
    source_size_squared = max(
        0.0,
        float(np.real(np.vdot(source_vector, m @ source_vector))),
    )
    radius += contraction**length * math.sqrt(source_size_squared)

    def energy(vector: np.ndarray) -> float:
        return max(0.0, float(np.real(np.vdot(vector, m @ vector))))

    center_energy = energy(center)
    exact_energy = energy(exact)
    return DirectionalCertificate(
        exact_energy=exact_energy,
        center_energy=center_energy,
        residual_radius=radius,
        upper_energy=(math.sqrt(center_energy) + radius) ** 2,
        coefficient_norm=float(np.linalg.norm(coeff)),
    )
