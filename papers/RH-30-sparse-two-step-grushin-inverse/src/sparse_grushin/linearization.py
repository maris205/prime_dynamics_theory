"""Sparse two-step Grushin linearization of the lifted complement shift."""

from __future__ import annotations

from dataclasses import dataclass

import numpy as np
from scipy.sparse import bmat, csc_matrix, eye


@dataclass(frozen=True)
class LowRankUpdate:
    """A factorization ``X @ Y`` of the correction to the sparse base."""

    columns: np.ndarray
    rows: np.ndarray
    channel_labels: tuple[str, ...]
    channel_scales: np.ndarray

    def __post_init__(self) -> None:
        columns = np.asarray(self.columns)
        rows = np.asarray(self.rows)
        if columns.ndim != 2 or rows.ndim != 2:
            raise ValueError("low-rank factors must be matrices")
        if columns.shape[1] != rows.shape[0]:
            raise ValueError("low-rank factors do not align")
        if len(self.channel_labels) != columns.shape[1]:
            raise ValueError("one label is required per channel")
        if np.asarray(self.channel_scales).shape != (columns.shape[1],):
            raise ValueError("one scale is required per channel")

    @property
    def rank(self) -> int:
        return int(np.asarray(self.columns).shape[1])


@dataclass(frozen=True)
class SparseGrushinSystem:
    """Sparse bordered matrix whose leading inverse block is the lifted inverse."""

    matrix: csc_matrix
    base: csc_matrix
    update: LowRankUpdate
    physical_dimension: int
    auxiliary_scale: float

    @property
    def linearized_dimension(self) -> int:
        return 2 * int(self.physical_dimension)

    @property
    def bordered_dimension(self) -> int:
        return int(self.matrix.shape[0])


def one_step_bulk_dense(
    matrix,
    right_modes: np.ndarray,
    left_modes: np.ndarray,
    peripheral_values: np.ndarray,
    values: np.ndarray,
) -> np.ndarray:
    """Apply ``U=M-R Lambda L^T`` to a thin dense block."""

    source = np.asarray(values)
    weighted_right = np.asarray(right_modes) * np.asarray(peripheral_values)[None, :]
    return np.asarray(matrix @ source) - weighted_right @ (
        np.asarray(left_modes).T @ source
    )


def build_low_rank_update(
    matrix,
    right_modes: np.ndarray,
    left_modes: np.ndarray,
    peripheral_values: np.ndarray,
    synthesis: np.ndarray,
    analysis: np.ndarray,
    dangerous_left: np.ndarray,
    dangerous_right: np.ndarray,
    singular_value: float,
    *,
    lift: float = 1.0,
    auxiliary_scale: float = 1.0,
    balance_channels: bool = True,
) -> LowRankUpdate:
    r"""Factor the low-rank correction to the sparse two-step base.

    The target two-by-two block matrix is

    ``[[zI + c u v*, -t Q U], [-t^{-1} U Q, I]]``.

    Relative to ``[[zI,-tM],[-t^{-1}M,I]]``, the two off-diagonal
    corrections are

    ``M-QU = R Lambda L^T + V(WU)`` and
    ``M-UQ = R Lambda L^T + (UV)W``.
    """

    dimension = int(matrix.shape[0])
    right = np.asarray(right_modes)
    left = np.asarray(left_modes)
    values = np.asarray(peripheral_values)
    synthesis_values = np.asarray(synthesis)
    analysis_values = np.asarray(analysis)
    u = np.asarray(dangerous_left).reshape(-1)
    v = np.asarray(dangerous_right).reshape(-1)
    if u.shape != (dimension,) or v.shape != (dimension,):
        raise ValueError("dangerous directions have incompatible dimensions")
    tau = float(lift)
    singular = float(singular_value)
    scale = float(auxiliary_scale)
    if tau <= 0.0 or singular <= 0.0 or scale <= 0.0:
        raise ValueError("lift, singular value, and auxiliary scale must be positive")

    u_norm = float(np.linalg.norm(u))
    v_norm = float(np.linalg.norm(v))
    lift_coefficient = (tau - singular) / (u_norm * v_norm)
    peripheral_columns = right * values[None, :]
    peripheral_rows = left.T
    u_synthesis = one_step_bulk_dense(
        matrix, right, left, values, synthesis_values
    )
    w_u = np.asarray(analysis_values @ matrix) - (
        analysis_values @ peripheral_columns
    ) @ peripheral_rows

    zero_top = np.zeros((dimension, 0), dtype=np.complex128)
    del zero_top  # documents the block placement used below
    columns: list[np.ndarray] = []
    rows: list[np.ndarray] = []
    labels: list[str] = []

    def append_channel(column: np.ndarray, row: np.ndarray, label: str) -> None:
        columns.append(np.asarray(column, dtype=np.complex128).reshape(-1))
        rows.append(np.asarray(row, dtype=np.complex128).reshape(-1))
        labels.append(label)

    lift_column = np.zeros(2 * dimension, dtype=np.complex128)
    lift_column[:dimension] = lift_coefficient * u
    lift_row = np.zeros(2 * dimension, dtype=np.complex128)
    lift_row[:dimension] = v.conj()
    append_channel(lift_column, lift_row, "lift")

    for index in range(peripheral_columns.shape[1]):
        column = np.zeros(2 * dimension, dtype=np.complex128)
        column[:dimension] = scale * peripheral_columns[:, index]
        row = np.zeros(2 * dimension, dtype=np.complex128)
        row[dimension:] = peripheral_rows[index, :]
        append_channel(column, row, f"top_peripheral_{index}")
    for index in range(synthesis_values.shape[1]):
        column = np.zeros(2 * dimension, dtype=np.complex128)
        column[:dimension] = scale * synthesis_values[:, index]
        row = np.zeros(2 * dimension, dtype=np.complex128)
        row[dimension:] = w_u[index, :]
        append_channel(column, row, f"top_packet_{index}")

    for index in range(peripheral_columns.shape[1]):
        column = np.zeros(2 * dimension, dtype=np.complex128)
        column[dimension:] = peripheral_columns[:, index] / scale
        row = np.zeros(2 * dimension, dtype=np.complex128)
        row[:dimension] = peripheral_rows[index, :]
        append_channel(column, row, f"bottom_peripheral_{index}")
    for index in range(synthesis_values.shape[1]):
        column = np.zeros(2 * dimension, dtype=np.complex128)
        column[dimension:] = u_synthesis[:, index] / scale
        row = np.zeros(2 * dimension, dtype=np.complex128)
        row[:dimension] = analysis_values[index, :]
        append_channel(column, row, f"bottom_packet_{index}")

    x = np.column_stack(columns)
    y = np.vstack(rows)
    channel_scales = np.ones(x.shape[1], dtype=np.float64)
    if balance_channels:
        for index in range(x.shape[1]):
            column_norm = float(np.linalg.norm(x[:, index]))
            row_norm = float(np.linalg.norm(y[index, :]))
            if column_norm > 0.0 and row_norm > 0.0:
                factor = float(np.sqrt(row_norm / column_norm))
                x[:, index] *= factor
                y[index, :] /= factor
                channel_scales[index] = factor
    return LowRankUpdate(
        columns=x,
        rows=y,
        channel_labels=tuple(labels),
        channel_scales=channel_scales,
    )


def build_sparse_grushin_system(
    matrix,
    right_modes: np.ndarray,
    left_modes: np.ndarray,
    peripheral_values: np.ndarray,
    synthesis: np.ndarray,
    analysis: np.ndarray,
    dangerous_left: np.ndarray,
    dangerous_right: np.ndarray,
    singular_value: float,
    spectral_parameter: complex,
    *,
    lift: float = 1.0,
    auxiliary_scale: float = 1.0,
    balance_channels: bool = True,
) -> SparseGrushinSystem:
    """Build the sparse bordered linearization."""

    sparse = csc_matrix(matrix, dtype=np.complex128)
    dimension = int(sparse.shape[0])
    identity = eye(dimension, format="csc", dtype=np.complex128)
    scale = float(auxiliary_scale)
    base = bmat(
        [
            [complex(spectral_parameter) * identity, -scale * sparse],
            [-sparse / scale, identity],
        ],
        format="csc",
    )
    update = build_low_rank_update(
        sparse,
        right_modes,
        left_modes,
        peripheral_values,
        synthesis,
        analysis,
        dangerous_left,
        dangerous_right,
        singular_value,
        lift=lift,
        auxiliary_scale=scale,
        balance_channels=balance_channels,
    )
    x_sparse = csc_matrix(update.columns)
    y_sparse = csc_matrix(update.rows)
    border_identity = eye(update.rank, format="csc", dtype=np.complex128)
    bordered = bmat(
        [[base, x_sparse], [y_sparse, -border_identity]],
        format="csc",
    )
    return SparseGrushinSystem(
        matrix=bordered,
        base=base,
        update=update,
        physical_dimension=dimension,
        auxiliary_scale=scale,
    )


def dense_lifted_complement(
    matrix: np.ndarray,
    right_modes: np.ndarray,
    left_modes: np.ndarray,
    peripheral_values: np.ndarray,
    synthesis: np.ndarray,
    analysis: np.ndarray,
    dangerous_left: np.ndarray,
    dangerous_right: np.ndarray,
    singular_value: float,
    spectral_parameter: complex,
    *,
    lift: float = 1.0,
) -> np.ndarray:
    """Dense reference construction used only by small tests."""

    stored = np.asarray(matrix, dtype=np.complex128)
    right = np.asarray(right_modes)
    left = np.asarray(left_modes)
    values = np.asarray(peripheral_values)
    synthesis_values = np.asarray(synthesis)
    analysis_values = np.asarray(analysis)
    u = np.asarray(dangerous_left).reshape(-1)
    v = np.asarray(dangerous_right).reshape(-1)
    bulk = stored - (right * values[None, :]) @ left.T
    external = np.eye(stored.shape[0], dtype=np.complex128) - (
        synthesis_values @ analysis_values
    )
    shifted = complex(spectral_parameter) * np.eye(stored.shape[0]) - (
        external @ bulk @ bulk @ external
    )
    coefficient = (float(lift) - float(singular_value)) / (
        np.linalg.norm(u) * np.linalg.norm(v)
    )
    return shifted + coefficient * np.outer(u, v.conj())
