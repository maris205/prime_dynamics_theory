"""Unitary Schur packet identities and time-ordered Stein recursions."""

from __future__ import annotations

from dataclasses import dataclass
import math
from typing import Sequence

import numpy as np
from scipy.linalg import schur


def _square_matrix(value: np.ndarray, name: str) -> np.ndarray:
    result = np.asarray(value, dtype=np.complex128)
    if result.ndim != 2 or result.shape[0] != result.shape[1]:
        raise ValueError(f"{name} must be square")
    return result


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


def _cuts(value: Sequence[float]) -> tuple[float, ...]:
    result = tuple(float(item) for item in value)
    if any(not math.isfinite(item) or item <= 0.0 for item in result):
        raise ValueError("cuts must be finite and positive")
    if any(right <= left for left, right in zip(result, result[1:])):
        raise ValueError("cuts must be strictly increasing")
    return result


def _block_slices(sizes: Sequence[int]) -> tuple[slice, ...]:
    result = []
    position = 0
    for size in sizes:
        width = int(size)
        if width <= 0:
            raise ValueError("active block sizes must be positive")
        result.append(slice(position, position + width))
        position += width
    return tuple(result)


@dataclass(frozen=True)
class OrderedSchurPartition:
    """Complex unitary Schur form ordered into fixed radial bands."""

    triangular: np.ndarray
    unitary: np.ndarray
    names: tuple[str, ...]
    sizes: tuple[int, ...]
    cuts: tuple[float, ...]
    physical_scale: float
    physical_moduli: np.ndarray
    reconstruction_defect: float
    unitary_defect: float
    strict_lower_defect: float
    minimum_boundary_gap: float

    @property
    def slices(self) -> tuple[slice, ...]:
        return _block_slices(self.sizes)


def ordered_radial_schur(
    operator: np.ndarray,
    cuts: Sequence[float],
    *,
    physical_scale: float = 1.0,
    names: Sequence[str] | None = None,
) -> OrderedSchurPartition:
    r"""Return a unitary Schur form with contiguous radial bands.

    The first sort places the central disk first.  Each subsequent sort acts
    only on the trailing Schur block, preserving upper triangularity and all
    previously selected bands.
    """

    a = _square_matrix(operator, "operator")
    boundaries = _cuts(cuts)
    scale = float(physical_scale)
    if not math.isfinite(scale) or scale <= 0.0:
        raise ValueError("physical_scale must be finite and positive")
    group_count = len(boundaries) + 1
    if names is None:
        labels = ("central",) + tuple(
            f"annulus_{index}" for index in range(1, group_count - 1)
        ) + (("edge",) if group_count > 1 else ())
    else:
        labels = tuple(str(item) for item in names)
        if len(labels) != group_count:
            raise ValueError("names must have len(cuts)+1 entries")

    if boundaries:
        triangular, unitary, selected = schur(
            a,
            output="complex",
            sort=lambda value: abs(value) * scale <= boundaries[0],
            check_finite=False,
        )
        raw_sizes = [int(selected)]
        position = int(selected)
        for boundary in boundaries[1:]:
            if position == a.shape[0]:
                raw_sizes.append(0)
                continue
            trailing, rotation, selected = schur(
                triangular[position:, position:],
                output="complex",
                sort=lambda value, cut=boundary: abs(value) * scale <= cut,
                check_finite=False,
            )
            triangular[:position, position:] = (
                triangular[:position, position:] @ rotation
            )
            triangular[position:, position:] = trailing
            unitary[:, position:] = unitary[:, position:] @ rotation
            raw_sizes.append(int(selected))
            position += int(selected)
        raw_sizes.append(a.shape[0] - position)
    else:
        triangular, unitary = schur(a, output="complex", check_finite=False)
        raw_sizes = [a.shape[0]]

    active_names = tuple(
        label for label, size in zip(labels, raw_sizes) if int(size) > 0
    )
    active_sizes = tuple(int(size) for size in raw_sizes if int(size) > 0)
    moduli = np.abs(np.diag(triangular)) * scale
    identity = np.eye(a.shape[0], dtype=np.complex128)
    scale_a = max(1.0, float(np.linalg.norm(a, 2)))
    boundary_gap = min(
        (float(np.min(np.abs(moduli - boundary))) for boundary in boundaries),
        default=math.inf,
    )
    return OrderedSchurPartition(
        triangular=triangular,
        unitary=unitary,
        names=active_names,
        sizes=active_sizes,
        cuts=boundaries,
        physical_scale=scale,
        physical_moduli=moduli,
        reconstruction_defect=float(
            np.linalg.norm(a - unitary @ triangular @ unitary.conjugate().T, 2)
            / scale_a
        ),
        unitary_defect=float(
            np.linalg.norm(unitary.conjugate().T @ unitary - identity, 2)
        ),
        strict_lower_defect=float(
            np.linalg.norm(np.tril(triangular, -1), "fro") / scale_a
        ),
        minimum_boundary_gap=boundary_gap,
    )


@dataclass(frozen=True)
class BlockGramBudget:
    """Exact packet reconstruction and coherence-weighted upper."""

    exact_energy: float
    square_sum_energy: float
    signed_fusion_ratio: float
    coherence_constant: float
    coherence_upper: float
    absolute_packet_upper: float
    block_energies: np.ndarray
    normalized_gram: np.ndarray
    minimum_gram_eigenvalue: float


def gram_budget(gram: np.ndarray, *, tolerance: float = 1.0e-12) -> BlockGramBudget:
    value = _hermitian(_square_matrix(gram, "gram"))
    diagonal = np.real(np.diag(value))
    scale = max(1.0, float(np.max(np.abs(diagonal), initial=0.0)))
    tol = float(tolerance)
    if np.min(diagonal, initial=0.0) < -tol * scale:
        raise ValueError("gram has a negative diagonal beyond tolerance")
    energies = np.sqrt(np.maximum(diagonal, 0.0))
    active = energies > math.sqrt(tol * scale)
    normalized = np.zeros_like(value)
    if np.any(active):
        indices = np.flatnonzero(active)
        block = value[np.ix_(indices, indices)] / np.outer(
            energies[active], energies[active]
        )
        block = _hermitian(block)
        normalized[np.ix_(indices, indices)] = block
        coherence = float(np.max(np.linalg.eigvalsh(block)).real)
    else:
        coherence = 0.0
    square_squared = float(np.sum(np.maximum(diagonal, 0.0)))
    exact_squared = float(np.real(np.sum(value)))
    if exact_squared < -tol * max(1.0, square_squared):
        raise ValueError("reconstructed energy square is negative beyond tolerance")
    exact_squared = max(exact_squared, 0.0)
    return BlockGramBudget(
        exact_energy=math.sqrt(exact_squared),
        square_sum_energy=math.sqrt(square_squared),
        signed_fusion_ratio=(exact_squared / square_squared if square_squared else 0.0),
        coherence_constant=coherence,
        coherence_upper=math.sqrt(max(0.0, coherence * square_squared)),
        absolute_packet_upper=float(np.sum(energies)),
        block_energies=energies,
        normalized_gram=normalized,
        minimum_gram_eigenvalue=float(np.min(np.linalg.eigvalsh(value)).real),
    )


def schur_state_gram(
    gramian: np.ndarray,
    observation: np.ndarray,
    partition: OrderedSchurPartition,
) -> np.ndarray:
    r"""Gram of observed state blocks in Schur coordinates."""

    g = _square_matrix(gramian, "gramian")
    y = _observation_matrix(observation, g.shape[0])
    q = partition.unitary
    if q.shape != g.shape:
        raise ValueError("partition has incompatible dimension")
    transformed_gramian = q.conjugate().T @ g @ q
    transformed_observation = y @ q
    slices = partition.slices
    result = np.empty((len(slices), len(slices)), dtype=np.complex128)
    for row, left in enumerate(slices):
        for column, right in enumerate(slices):
            result[row, column] = np.trace(
                transformed_observation[:, left]
                @ transformed_gramian[left, right]
                @ transformed_observation[:, right].conjugate().T
            )
    return _hermitian(result)


def schur_source_gram(
    observability_gramian: np.ndarray,
    source: np.ndarray,
    partition: OrderedSchurPartition,
) -> np.ndarray:
    r"""Gram of orthogonal initial Schur packets propagated for all time."""

    o = _square_matrix(observability_gramian, "observability_gramian")
    x = _source_matrix(source, o.shape[0])
    q = partition.unitary
    if q.shape != o.shape:
        raise ValueError("partition has incompatible dimension")
    transformed_observability = q.conjugate().T @ o @ q
    transformed_source = q.conjugate().T @ x
    slices = partition.slices
    result = np.empty((len(slices), len(slices)), dtype=np.complex128)
    for row, left in enumerate(slices):
        for column, right in enumerate(slices):
            result[row, column] = np.trace(
                transformed_source[right, :].conjugate().T
                @ transformed_observability[right, left]
                @ transformed_source[left, :]
            )
    return _hermitian(result)


@dataclass(frozen=True)
class RecursionRow:
    left_block: int
    right_block: int
    gramian_norm: float
    right_hand_side_norm: float
    source_norm: float
    feed_forward_norm: float
    empirical_gain: float
    residual_norm: float


@dataclass(frozen=True)
class CrossSteinRecursionAudit:
    rows: tuple[RecursionRow, ...]
    maximum_residual_norm: float
    maximum_empirical_gain: float


def cross_stein_recursion_audit(
    gramian: np.ndarray,
    source: np.ndarray,
    partition: OrderedSchurPartition,
) -> CrossSteinRecursionAudit:
    """Audit the reverse-order block Stein recursion using one exact Gramian."""

    g = _square_matrix(gramian, "gramian")
    x = _source_matrix(source, g.shape[0])
    q = partition.unitary
    t = partition.triangular
    transformed_gramian = q.conjugate().T @ g @ q
    transformed_source = q.conjugate().T @ x
    slices = partition.slices
    rows = []
    for row, left in enumerate(slices):
        for column, right in enumerate(slices):
            block = transformed_gramian[left, right]
            source_term = (
                transformed_source[left, :]
                @ transformed_source[right, :].conjugate().T
            )
            feed = np.zeros_like(block)
            for outer_row in range(row, len(slices)):
                row_slice = slices[outer_row]
                for outer_column in range(column, len(slices)):
                    column_slice = slices[outer_column]
                    if outer_row == row and outer_column == column:
                        continue
                    feed += (
                        t[left, row_slice]
                        @ transformed_gramian[row_slice, column_slice]
                        @ t[right, column_slice].conjugate().T
                    )
            lhs = block - t[left, left] @ block @ t[right, right].conjugate().T
            residual = lhs - source_term - feed
            rhs_norm = float(np.linalg.norm(lhs, "fro"))
            block_norm = float(np.linalg.norm(block, "fro"))
            rows.append(
                RecursionRow(
                    left_block=row,
                    right_block=column,
                    gramian_norm=block_norm,
                    right_hand_side_norm=rhs_norm,
                    source_norm=float(np.linalg.norm(source_term, "fro")),
                    feed_forward_norm=float(np.linalg.norm(feed, "fro")),
                    empirical_gain=(block_norm / rhs_norm if rhs_norm else 0.0),
                    residual_norm=float(np.linalg.norm(residual, "fro")),
                )
            )
    return CrossSteinRecursionAudit(
        rows=tuple(rows),
        maximum_residual_norm=max((item.residual_norm for item in rows), default=0.0),
        maximum_empirical_gain=max((item.empirical_gain for item in rows), default=0.0),
    )


@dataclass(frozen=True)
class BlockSteinGains:
    horizon: int
    power_norms: tuple[tuple[float, ...], ...]
    gains: np.ndarray
    maximum_terminal_power_norm: float
    maximum_gain: float


def block_power_stein_gains(
    partition: OrderedSchurPartition, horizon: int
) -> BlockSteinGains:
    r"""Bound each diagonal-block Stein inverse by a block-power split."""

    count = int(horizon)
    if count < 1:
        raise ValueError("horizon must be positive")
    power_norms = []
    for block_slice in partition.slices:
        block = partition.triangular[block_slice, block_slice]
        power = np.eye(block.shape[0], dtype=np.complex128)
        norms = []
        for _ in range(count + 1):
            norms.append(float(np.linalg.norm(power, 2)))
            power = block @ power
        if norms[-1] >= 1.0:
            raise ValueError("selected horizon does not contract every Schur block")
        power_norms.append(tuple(norms))
    gains = np.empty((len(power_norms), len(power_norms)), dtype=np.float64)
    for row, left in enumerate(power_norms):
        for column, right in enumerate(power_norms):
            denominator = 1.0 - left[-1] * right[-1]
            gains[row, column] = sum(
                left[power] * right[power] for power in range(count)
            ) / denominator
    return BlockSteinGains(
        horizon=count,
        power_norms=tuple(power_norms),
        gains=gains,
        maximum_terminal_power_norm=max(item[-1] for item in power_norms),
        maximum_gain=float(np.max(gains, initial=0.0)),
    )


@dataclass(frozen=True)
class ScalarPathMajorant:
    horizon: int
    energy_squared_upper: float
    energy_upper: float
    gramian_norm_uppers: np.ndarray
    source_norms: np.ndarray
    feed_forward_uppers: np.ndarray
    observation_weights: np.ndarray
    block_coupling_norms: np.ndarray
    stein_gains: BlockSteinGains


def scalar_path_majorant(
    source: np.ndarray,
    observation: np.ndarray,
    partition: OrderedSchurPartition,
    *,
    horizon: int,
) -> ScalarPathMajorant:
    r"""Evaluate the reverse-order absolute Schur-path majorant."""

    dimension = partition.triangular.shape[0]
    x = _source_matrix(source, dimension)
    y = _observation_matrix(observation, dimension)
    transformed_source = partition.unitary.conjugate().T @ x
    transformed_observation = y @ partition.unitary
    slices = partition.slices
    block_count = len(slices)
    stein = block_power_stein_gains(partition, horizon)
    source_norms = np.zeros((block_count, block_count), dtype=np.float64)
    coupling = np.zeros_like(source_norms)
    observation_weights = np.zeros_like(source_norms)
    for row, left in enumerate(slices):
        for column, right in enumerate(slices):
            source_norms[row, column] = float(
                np.linalg.norm(
                    transformed_source[left, :]
                    @ transformed_source[right, :].conjugate().T,
                    "fro",
                )
            )
            if row <= column:
                coupling[row, column] = float(
                    np.linalg.norm(partition.triangular[left, right], 2)
                )
            observation_weights[row, column] = float(
                np.linalg.norm(
                    transformed_observation[:, right].conjugate().T
                    @ transformed_observation[:, left],
                    "fro",
                )
            )
    gamma = np.zeros_like(source_norms)
    feed = np.zeros_like(source_norms)
    for row in range(block_count - 1, -1, -1):
        for column in range(block_count - 1, -1, -1):
            value = 0.0
            for outer_row in range(row, block_count):
                for outer_column in range(column, block_count):
                    if outer_row == row and outer_column == column:
                        continue
                    value += (
                        coupling[row, outer_row]
                        * gamma[outer_row, outer_column]
                        * coupling[column, outer_column]
                    )
            feed[row, column] = value
            gamma[row, column] = stein.gains[row, column] * (
                source_norms[row, column] + value
            )
    energy_squared = float(np.sum(observation_weights * gamma))
    return ScalarPathMajorant(
        horizon=int(horizon),
        energy_squared_upper=energy_squared,
        energy_upper=math.sqrt(max(energy_squared, 0.0)),
        gramian_norm_uppers=gamma,
        source_norms=source_norms,
        feed_forward_uppers=feed,
        observation_weights=observation_weights,
        block_coupling_norms=coupling,
        stein_gains=stein,
    )
