"""Physical-covariance optimization of block residual Gram envelopes."""

from __future__ import annotations

from dataclasses import dataclass
import math

import numpy as np
from scipy.linalg import null_space, solve_discrete_lyapunov


@dataclass(frozen=True)
class BlockComponents:
    horizon: int
    depth: int
    krylov_rank: int
    source_columns: int
    metric_contraction: float
    frame: np.ndarray
    exact_gram: np.ndarray
    center_gram: np.ndarray
    residual_pieces: tuple[np.ndarray, ...]


@dataclass(frozen=True)
class CovarianceCertificate:
    epsilon: float
    residual_weights: tuple[float, ...]
    young_parameter: float
    residual_gram_upper: np.ndarray
    gram_envelope: np.ndarray
    physical_gain: float
    weighted_trace_gain: float
    global_spectral_gain: float
    directional_optimal_gain: float
    minimum_slack_eigenvalue: float


@dataclass(frozen=True)
class CancellationLedger:
    epsilon: float
    physical_gain: float
    global_spectral_gain: float
    weighted_trace_gain: float
    young_parameter: float
    target_exact_energy: float
    complement_exact_energy: float
    complement_center_energy: float
    complement_residual_upper: float


def _square(value: np.ndarray, name: str) -> np.ndarray:
    result = np.asarray(value, dtype=np.complex128)
    if result.ndim != 2 or result.shape[0] != result.shape[1]:
        raise ValueError(f"{name} must be square")
    return result


def _hermitian(value: np.ndarray) -> np.ndarray:
    return 0.5 * (value + value.conjugate().T)


def lyapunov_metric(operator: np.ndarray) -> np.ndarray:
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


def metric_contraction(operator: np.ndarray, metric: np.ndarray) -> float:
    a = _square(operator, "operator")
    m = _square(metric, "metric")
    eigenvalues, vectors = np.linalg.eigh(_hermitian(m))
    if np.min(eigenvalues) <= 0.0:
        raise ValueError("metric must be positive")
    root = (vectors * np.sqrt(eigenvalues)) @ vectors.conjugate().T
    inverse = (
        vectors * (1.0 / np.sqrt(eigenvalues))
    ) @ vectors.conjugate().T
    return float(np.linalg.norm(root @ a @ inverse, 2))


def coefficient_frame(coefficients: np.ndarray) -> np.ndarray:
    """Unitary frame whose first axis is the physical coefficient ray."""

    vector = np.asarray(coefficients, dtype=np.complex128).reshape(-1)
    size = float(np.linalg.norm(vector))
    if vector.size == 0 or size == 0.0:
        raise ValueError("coefficients must be nonzero")
    first = (vector / size).reshape(-1, 1)
    if vector.size == 1:
        return first
    complement = null_space(first.conjugate().T)
    return np.column_stack([first, complement])


def _block_basis(
    operator: np.ndarray,
    sources: np.ndarray,
    depth: int,
    tolerance: float,
) -> np.ndarray:
    blocks = []
    current = sources.copy()
    for _ in range(depth):
        blocks.append(current)
        current = operator @ current
    matrix = np.column_stack(blocks)
    left, singular_values, _ = np.linalg.svd(matrix, full_matrices=False)
    if singular_values.size == 0 or singular_values[0] == 0.0:
        raise ValueError("block source has zero Krylov rank")
    rank = int(
        np.count_nonzero(singular_values > tolerance * singular_values[0])
    )
    return left[:, :rank]


def block_components(
    operator: np.ndarray,
    sources: np.ndarray,
    metric: np.ndarray,
    horizon: int,
    depth: int,
    coefficients: np.ndarray,
    *,
    tolerance: float = 1.0e-12,
) -> BlockComponents:
    """Build stable coefficient-frame factors for the RH-66 envelope."""

    a = _square(operator, "operator")
    z = np.asarray(sources, dtype=np.complex128)
    if z.ndim == 1:
        z = z.reshape(-1, 1)
    if z.ndim != 2 or z.shape[0] != a.shape[0] or z.shape[1] == 0:
        raise ValueError("sources must be a nonempty matching matrix")
    m = _square(metric, "metric")
    if m.shape != a.shape:
        raise ValueError("metric has incompatible shape")
    length = int(horizon)
    levels = int(depth)
    if length < 0 or levels <= 0:
        raise ValueError("invalid horizon or depth")
    frame = coefficient_frame(coefficients)
    if frame.shape[0] != z.shape[1]:
        raise ValueError("coefficient dimension does not match sources")
    basis = _block_basis(a, z, levels, tolerance)
    coordinates = basis.conjugate().T @ z
    projected = basis.conjugate().T @ a @ basis
    residual = a @ basis - basis @ projected
    source_residual = z - basis @ coordinates
    transformed_coordinates = coordinates @ frame
    center_vectors = basis @ (
        np.linalg.matrix_power(projected, length)
        @ transformed_coordinates
    )
    exact_vectors = np.linalg.matrix_power(a, length) @ z @ frame
    center_gram = _hermitian(
        center_vectors.conjugate().T @ m @ center_vectors
    )
    exact_gram = _hermitian(
        exact_vectors.conjugate().T @ m @ exact_vectors
    )
    contraction = metric_contraction(a, m)
    pieces = []
    power = np.eye(projected.shape[0], dtype=np.complex128)
    for index in range(length):
        propagated_power = length - 1 - index
        residual_vectors = residual @ power @ transformed_coordinates
        piece = residual_vectors.conjugate().T @ m @ residual_vectors
        pieces.append(
            _hermitian(contraction ** (2 * propagated_power) * piece)
        )
        power = projected @ power
    source_vectors = source_residual @ frame
    pieces.append(
        _hermitian(
            contraction ** (2 * length)
            * source_vectors.conjugate().T
            @ m
            @ source_vectors
        )
    )
    return BlockComponents(
        horizon=length,
        depth=levels,
        krylov_rank=basis.shape[1],
        source_columns=z.shape[1],
        metric_contraction=contraction,
        frame=frame,
        exact_gram=exact_gram,
        center_gram=center_gram,
        residual_pieces=tuple(pieces),
    )


def physical_covariance(dimension: int, epsilon: float) -> np.ndarray:
    size = int(dimension)
    value = float(epsilon)
    if size <= 0 or not math.isfinite(value) or not (0.0 < value <= 1.0):
        raise ValueError("invalid covariance dimension or epsilon")
    diagonal = np.full(size, value, dtype=float)
    diagonal[0] = 1.0
    return np.diag(diagonal).astype(np.complex128)


def _positive_quadratic(matrix: np.ndarray, index: int = 0) -> float:
    return max(0.0, float(np.real(matrix[index, index])))


def covariance_certificate(
    components: BlockComponents,
    epsilon: float,
) -> CovarianceCertificate:
    """Optimize the positive envelope for a regularized physical ray."""

    covariance = physical_covariance(
        components.source_columns,
        epsilon,
    )
    active_pieces = []
    roots = []
    for piece in components.residual_pieces:
        piece_trace = max(0.0, float(np.real(np.trace(piece))))
        if piece_trace == 0.0:
            continue
        score = max(0.0, float(np.real(np.trace(covariance @ piece))))
        if score == 0.0:
            raise ArithmeticError("positive covariance produced a zero score")
        active_pieces.append(piece)
        roots.append(math.sqrt(score))
    if active_pieces:
        root_sum = sum(roots)
        weights = tuple(root / root_sum for root in roots)
        residual_upper = sum(
            piece / weight
            for piece, weight in zip(active_pieces, weights, strict=True)
        )
        residual_upper = _hermitian(residual_upper)
    else:
        weights = ()
        residual_upper = np.zeros_like(components.exact_gram)
    center_score = max(
        0.0,
        float(np.real(np.trace(covariance @ components.center_gram))),
    )
    residual_score = max(
        0.0,
        float(np.real(np.trace(covariance @ residual_upper))),
    )
    if residual_score == 0.0:
        eta = 0.0
        envelope = components.center_gram.copy()
    elif center_score == 0.0:
        eta = math.inf
        envelope = residual_upper.copy()
    else:
        eta = math.sqrt(residual_score / center_score)
        envelope = (
            (1.0 + eta) * components.center_gram
            + (1.0 + 1.0 / eta) * residual_upper
        )
    envelope = _hermitian(envelope)
    exact_physical = _positive_quadratic(components.exact_gram)
    envelope_physical = _positive_quadratic(envelope)
    exact_weighted = max(
        1.0e-300,
        float(np.real(np.trace(covariance @ components.exact_gram))),
    )
    envelope_weighted = max(
        0.0,
        float(np.real(np.trace(covariance @ envelope))),
    )
    exact_global = max(
        1.0e-300,
        float(np.max(np.linalg.eigvalsh(components.exact_gram))),
    )
    envelope_global = max(
        0.0,
        float(np.max(np.linalg.eigvalsh(envelope))),
    )
    directional_radius = sum(
        math.sqrt(_positive_quadratic(piece))
        for piece in components.residual_pieces
    )
    directional_upper = (
        math.sqrt(_positive_quadratic(components.center_gram))
        + directional_radius
    ) ** 2
    slack = _hermitian(envelope - components.exact_gram)
    return CovarianceCertificate(
        epsilon=float(epsilon),
        residual_weights=weights,
        young_parameter=eta,
        residual_gram_upper=residual_upper,
        gram_envelope=envelope,
        physical_gain=envelope_physical / max(exact_physical, 1.0e-300),
        weighted_trace_gain=envelope_weighted / exact_weighted,
        global_spectral_gain=envelope_global / exact_global,
        directional_optimal_gain=directional_upper
        / max(exact_physical, 1.0e-300),
        minimum_slack_eigenvalue=float(np.min(np.linalg.eigvalsh(slack))),
    )


def diagonal_cancellation_ledger(
    epsilon: float,
    *,
    slow: float = 0.995,
    fused: float = 0.55,
    fast: float = 0.2,
    mixing: float = 0.2,
    horizon: int = 32,
) -> CancellationLedger:
    """Exact scalar reduction of the RH-66 cancellation model."""

    eps = float(epsilon)
    if not (0.0 < eps <= 1.0):
        raise ValueError("epsilon must lie in (0,1]")
    values = (slow, fused, fast)
    if any(not (0.0 < value < 1.0) for value in values):
        raise ValueError("diagonal contractions must lie in (0,1)")
    if mixing < 0.0 or horizon < 0:
        raise ValueError("invalid mixing or horizon")
    m_slow = 1.0 / (1.0 - slow * slow)
    m_fused = 1.0 / (1.0 - fused * fused)
    m_fast = 1.0 / (1.0 - fast * fast)
    normalizer = 1.0 + mixing * mixing
    projected = (slow + mixing * mixing * fast) / normalizer
    source_coordinate = math.sqrt(2.0 * normalizer)
    vector_metric = (
        m_slow + mixing * mixing * m_fast
    ) / normalizer
    residual_metric = (
        (slow - projected) ** 2 * m_slow
        + mixing * mixing * (fast - projected) ** 2 * m_fast
    ) / normalizer
    residual_radius = 0.0
    for index in range(horizon):
        residual_radius += (
            slow ** (horizon - 1 - index)
            * projected**index
            * source_coordinate
            * math.sqrt(residual_metric)
        )
    complement_residual = residual_radius**2
    complement_center = (
        source_coordinate**2
        * projected ** (2 * horizon)
        * vector_metric
    )
    target_exact = (
        2.0 * fused ** (2 * horizon) * m_fused
    )
    complement_exact = 2.0 * (
        slow ** (2 * horizon) * m_slow
        + mixing * mixing * fast ** (2 * horizon) * m_fast
    )
    eta = math.sqrt(
        eps * complement_residual
        / (target_exact + eps * complement_center)
    )
    target_envelope = (1.0 + eta) * target_exact
    complement_envelope = (
        (1.0 + eta) * complement_center
        + (1.0 + 1.0 / eta) * complement_residual
    )
    weighted_exact = target_exact + eps * complement_exact
    weighted_envelope = target_envelope + eps * complement_envelope
    return CancellationLedger(
        epsilon=eps,
        physical_gain=target_envelope / target_exact,
        global_spectral_gain=max(target_envelope, complement_envelope)
        / max(target_exact, complement_exact),
        weighted_trace_gain=weighted_envelope / weighted_exact,
        young_parameter=eta,
        target_exact_energy=target_exact,
        complement_exact_energy=complement_exact,
        complement_center_energy=complement_center,
        complement_residual_upper=complement_residual,
    )
