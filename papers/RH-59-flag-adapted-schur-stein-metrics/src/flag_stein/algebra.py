"""Flag-adapted block metrics and packetwise Stein supersolutions."""

from __future__ import annotations

from dataclasses import dataclass
import math
from typing import Sequence

import numpy as np
from scipy.linalg import cho_factor, cho_solve, solve_discrete_lyapunov


def _square_matrix(value: np.ndarray, name: str) -> np.ndarray:
    result = np.asarray(value, dtype=np.complex128)
    if result.ndim != 2 or result.shape[0] != result.shape[1]:
        raise ValueError(f"{name} must be square")
    return result


def _sizes(value: Sequence[int], dimension: int) -> tuple[int, ...]:
    result = tuple(int(item) for item in value)
    if not result or any(item <= 0 for item in result):
        raise ValueError("block sizes must be positive")
    if sum(result) != dimension:
        raise ValueError("block sizes do not match the matrix dimension")
    return result


def block_slices(sizes: Sequence[int]) -> tuple[slice, ...]:
    result = []
    position = 0
    for width in sizes:
        size = int(width)
        if size <= 0:
            raise ValueError("block sizes must be positive")
        result.append(slice(position, position + size))
        position += size
    return tuple(result)


def _source_matrix(value: np.ndarray, dimension: int) -> np.ndarray:
    result = np.asarray(value, dtype=np.complex128)
    if result.ndim == 1:
        result = result[:, None]
    if result.ndim != 2 or result.shape[0] != dimension:
        raise ValueError("source has incompatible shape")
    return result


def _observation_matrix(value: np.ndarray, dimension: int) -> np.ndarray:
    result = np.asarray(value, dtype=np.complex128)
    if result.ndim == 1:
        result = result[None, :]
    if result.ndim != 2 or result.shape[1] != dimension:
        raise ValueError("observation has incompatible shape")
    return result


def _hermitian(value: np.ndarray) -> np.ndarray:
    return 0.5 * (value + value.conjugate().T)


@dataclass(frozen=True)
class LocalLyapunovBlock:
    """The canonical identity-forced Lyapunov metric of one Schur block."""

    metric: np.ndarray
    square_root: np.ndarray
    inverse_square_root: np.ndarray
    normalized_diagonal: np.ndarray
    contraction: float
    residual_relative: float
    minimum_eigenvalue: float
    maximum_eigenvalue: float
    condition_number: float


@dataclass(frozen=True)
class FlagMetricFamily:
    """Local block metrics and their normalized upper-triangular coupling."""

    triangular: np.ndarray
    sizes: tuple[int, ...]
    blocks: tuple[LocalLyapunovBlock, ...]
    normalized_triangular: np.ndarray
    comparison_matrix: np.ndarray
    strict_lower_relative_defect: float

    @property
    def slices(self) -> tuple[slice, ...]:
        return block_slices(self.sizes)


def build_flag_metric(
    triangular: np.ndarray,
    sizes: Sequence[int],
    *,
    stability_tolerance: float = 1.0e-10,
) -> FlagMetricFamily:
    r"""Build canonical local metrics for an upper-triangular Schur flag.

    Each diagonal metric is the unique positive solution of

    ``H_i - D_i^* H_i D_i = I``.
    """

    value = _square_matrix(triangular, "triangular")
    widths = _sizes(sizes, value.shape[0])
    slices = block_slices(widths)
    scale = max(1.0, float(np.linalg.norm(value, 2)))
    lower_defect = float(np.linalg.norm(np.tril(value, -1), "fro") / scale)
    if lower_defect > stability_tolerance:
        raise ValueError("matrix is not upper triangular within tolerance")

    local = []
    for block_slice in slices:
        diagonal = value[block_slice, block_slice]
        if np.max(np.abs(np.diag(diagonal)), initial=0.0) >= 1.0:
            raise ValueError("every diagonal Schur block must be stable")
        metric = solve_discrete_lyapunov(
            diagonal.conjugate().T,
            np.eye(diagonal.shape[0], dtype=np.complex128),
        )
        metric = _hermitian(metric)
        eigenvalues, eigenvectors = np.linalg.eigh(metric)
        minimum = float(eigenvalues[0])
        maximum = float(eigenvalues[-1])
        if minimum <= 0.0:
            raise ValueError("local Lyapunov metric is not positive definite")
        root = (eigenvectors * np.sqrt(eigenvalues)) @ eigenvectors.conjugate().T
        inverse_root = (
            eigenvectors * (1.0 / np.sqrt(eigenvalues))
        ) @ eigenvectors.conjugate().T
        normalized = root @ diagonal @ inverse_root
        residual = (
            metric
            - diagonal.conjugate().T @ metric @ diagonal
            - np.eye(diagonal.shape[0])
        )
        local.append(
            LocalLyapunovBlock(
                metric=metric,
                square_root=root,
                inverse_square_root=inverse_root,
                normalized_diagonal=normalized,
                contraction=float(np.linalg.norm(normalized, 2)),
                residual_relative=float(
                    np.linalg.norm(residual, 2)
                    / max(1.0, np.linalg.norm(metric, 2))
                ),
                minimum_eigenvalue=minimum,
                maximum_eigenvalue=maximum,
                condition_number=maximum / minimum,
            )
        )

    normalized_triangular = np.zeros_like(value)
    comparison = np.zeros((len(slices), len(slices)), dtype=np.float64)
    for row, left in enumerate(slices):
        for column, right in enumerate(slices):
            if row > column:
                continue
            normalized_block = (
                local[row].square_root
                @ value[left, right]
                @ local[column].inverse_square_root
            )
            normalized_triangular[left, right] = normalized_block
            comparison[row, column] = float(
                np.linalg.norm(normalized_block, 2)
            )

    return FlagMetricFamily(
        triangular=value,
        sizes=widths,
        blocks=tuple(local),
        normalized_triangular=normalized_triangular,
        comparison_matrix=comparison,
        strict_lower_relative_defect=lower_defect,
    )


def _prefix_scales(
    family: FlagMetricFamily,
    packet_index: int,
    log_scales: Sequence[float],
) -> tuple[int, np.ndarray]:
    index = int(packet_index)
    if index < 0 or index >= len(family.sizes):
        raise ValueError("packet index is out of range")
    values = np.asarray(tuple(float(item) for item in log_scales))
    if values.shape != (index + 1,) or not np.all(np.isfinite(values)):
        raise ValueError("log scales must contain one finite value per prefix block")
    return index, values


def scaled_normalized_prefix(
    family: FlagMetricFamily,
    packet_index: int,
    log_scales: Sequence[float],
) -> np.ndarray:
    r"""Return ``P^(1/2) T P^(-1/2)`` on one Schur prefix."""

    index, values = _prefix_scales(family, packet_index, log_scales)
    slices = family.slices[: index + 1]
    dimension = slices[-1].stop
    result = np.zeros((dimension, dimension), dtype=np.complex128)
    for row, left in enumerate(slices):
        for column, right in enumerate(slices):
            if row <= column:
                result[left, right] = (
                    math.exp(values[row] - values[column])
                    * family.normalized_triangular[left, right]
                )
    return result


def scaled_comparison_prefix(
    family: FlagMetricFamily,
    packet_index: int,
    log_scales: Sequence[float],
) -> np.ndarray:
    """Return the scalar block-norm comparison under the same scaling."""

    index, values = _prefix_scales(family, packet_index, log_scales)
    comparison = family.comparison_matrix[: index + 1, : index + 1]
    return np.exp(values[:, None] - values[None, :]) * comparison


def _scaled_observation_prefix(
    observation: np.ndarray,
    family: FlagMetricFamily,
    packet_index: int,
    log_scales: np.ndarray,
) -> np.ndarray:
    y = _observation_matrix(observation, family.triangular.shape[0])
    pieces = []
    for block, block_slice, log_scale in zip(
        family.blocks[: packet_index + 1],
        family.slices[: packet_index + 1],
        log_scales,
    ):
        pieces.append(
            y[:, block_slice]
            @ block.inverse_square_root
            / math.exp(float(log_scale))
        )
    return np.hstack(pieces)


def _packet_source_metric_squared(
    source: np.ndarray,
    family: FlagMetricFamily,
    packet_index: int,
    log_scale: float,
) -> float:
    x = _source_matrix(source, family.triangular.shape[0])
    block_slice = family.slices[packet_index]
    weighted = (
        math.exp(float(log_scale))
        * family.blocks[packet_index].square_root
        @ x[block_slice, :]
    )
    return float(np.linalg.norm(weighted, "fro") ** 2)


def packet_log_upper_objective(
    source: np.ndarray,
    observation: np.ndarray,
    family: FlagMetricFamily,
    packet_index: int,
    log_scales: Sequence[float],
) -> float:
    r"""Return the log of the exact-dissipation packet upper.

    A ``ValueError`` is raised when the proposed metric has nonpositive
    dissipation.
    """

    index, values = _prefix_scales(family, packet_index, log_scales)
    normalized = scaled_normalized_prefix(family, index, values)
    dissipation = _hermitian(
        np.eye(normalized.shape[0]) - normalized.conjugate().T @ normalized
    )
    try:
        factor = cho_factor(dissipation, lower=True, check_finite=False)
    except np.linalg.LinAlgError as error:
        raise ValueError("scaled block metric is not strictly dissipative") from error
    scaled_observation = _scaled_observation_prefix(
        observation, family, index, values
    )
    kernel = scaled_observation @ cho_solve(
        factor, scaled_observation.conjugate().T, check_finite=False
    )
    kappa = max(0.0, float(np.linalg.eigvalsh(_hermitian(kernel))[-1]))
    source_squared = _packet_source_metric_squared(
        source, family, index, values[-1]
    )
    if kappa <= 0.0 or source_squared <= 0.0:
        return -math.inf
    return 0.5 * (math.log(kappa) + math.log(source_squared))


@dataclass(frozen=True)
class PacketSteinCertificate:
    """One packetwise positive Stein supersolution certificate."""

    packet_index: int
    log_scales: tuple[float, ...]
    energy_upper: float
    energy_squared_upper: float
    kappa: float
    source_metric_squared: float
    normalized_contraction: float
    comparison_contraction: float
    minimum_dissipation_eigenvalue: float
    minimum_supersolution_eigenvalue: float
    endpoint_observation_squared: float
    contraction_energy_upper: float


def evaluate_packet_certificate(
    source: np.ndarray,
    observation: np.ndarray,
    family: FlagMetricFamily,
    packet_index: int,
    log_scales: Sequence[float],
    *,
    positivity_tolerance: float = 1.0e-12,
) -> PacketSteinCertificate:
    r"""Evaluate the exact flag-metric dissipation certificate.

    If ``R=P-T^*PT`` and ``kappa=||Y R^(-1/2)||_2^2``, then
    ``kappa P`` is an observability Stein supersolution on the packet prefix.
    """

    index, values = _prefix_scales(family, packet_index, log_scales)
    normalized = scaled_normalized_prefix(family, index, values)
    dissipation = _hermitian(
        np.eye(normalized.shape[0]) - normalized.conjugate().T @ normalized
    )
    minimum_dissipation = float(np.linalg.eigvalsh(dissipation)[0])
    if minimum_dissipation <= positivity_tolerance:
        raise ValueError("scaled block metric lacks a positive dissipation margin")
    factor = cho_factor(dissipation, lower=True, check_finite=False)
    scaled_observation = _scaled_observation_prefix(
        observation, family, index, values
    )
    kernel = scaled_observation @ cho_solve(
        factor, scaled_observation.conjugate().T, check_finite=False
    )
    kappa = max(0.0, float(np.linalg.eigvalsh(_hermitian(kernel))[-1]))
    source_squared = _packet_source_metric_squared(
        source, family, index, values[-1]
    )
    upper_squared = kappa * source_squared
    supersolution = _hermitian(
        kappa * dissipation
        - scaled_observation.conjugate().T @ scaled_observation
    )
    minimum_supersolution = float(np.linalg.eigvalsh(supersolution)[0])
    contraction = float(np.linalg.norm(normalized, 2))
    endpoint_squared = float(np.linalg.norm(scaled_observation, 2) ** 2)
    contraction_upper = math.sqrt(
        max(0.0, source_squared * endpoint_squared / (1.0 - contraction**2))
    )
    comparison = float(
        np.linalg.norm(
            scaled_comparison_prefix(family, index, values), 2
        )
    )
    return PacketSteinCertificate(
        packet_index=index,
        log_scales=tuple(float(item) for item in values),
        energy_upper=math.sqrt(max(0.0, upper_squared)),
        energy_squared_upper=upper_squared,
        kappa=kappa,
        source_metric_squared=source_squared,
        normalized_contraction=contraction,
        comparison_contraction=comparison,
        minimum_dissipation_eigenvalue=minimum_dissipation,
        minimum_supersolution_eigenvalue=minimum_supersolution,
        endpoint_observation_squared=endpoint_squared,
        contraction_energy_upper=contraction_upper,
    )


def comparison_contraction_log_upper(
    source: np.ndarray,
    observation: np.ndarray,
    family: FlagMetricFamily,
    packet_index: int,
    log_scales: Sequence[float],
) -> float:
    """Return the scalar comparison contraction upper in logarithmic form."""

    index, values = _prefix_scales(family, packet_index, log_scales)
    comparison_q = float(
        np.linalg.norm(scaled_comparison_prefix(family, index, values), 2)
    )
    if comparison_q >= 1.0:
        raise ValueError("scalar comparison is not contractive")
    y = _observation_matrix(observation, family.triangular.shape[0])
    observation_upper = 0.0
    for block, block_slice, log_scale in zip(
        family.blocks[: index + 1], family.slices[: index + 1], values
    ):
        local = y[:, block_slice] @ block.inverse_square_root
        observation_upper += (
            float(np.linalg.norm(local, 2) ** 2)
            / math.exp(2.0 * float(log_scale))
        )
    source_squared = _packet_source_metric_squared(
        source, family, index, values[-1]
    )
    return 0.5 * (
        math.log(source_squared)
        + math.log(observation_upper)
        - math.log1p(-(comparison_q**2))
    )
