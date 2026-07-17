"""Sparse two-step Grushin realization of the unlifted complement shift."""

from __future__ import annotations

from dataclasses import dataclass

import numpy as np
from scipy.sparse import bmat, csc_matrix, eye


@dataclass(frozen=True)
class DirectGrushinSystem:
    """Bordered sparse matrix whose leading inverse block targets A(z)^-1."""

    matrix: csc_matrix
    physical_dimension: int
    border_rank: int
    channel_labels: tuple[str, ...]

    @property
    def bordered_dimension(self) -> int:
        return int(self.matrix.shape[0])


def _one_step_bulk_dense(
    matrix,
    right_modes: np.ndarray,
    left_modes: np.ndarray,
    peripheral_values: np.ndarray,
    values: np.ndarray,
) -> np.ndarray:
    source = np.asarray(values)
    weighted_right = np.asarray(right_modes) * np.asarray(peripheral_values)[
        None, :
    ]
    return np.asarray(matrix @ source) - weighted_right @ (
        np.asarray(left_modes).T @ source
    )


def build_direct_grushin_system(
    matrix,
    right_modes: np.ndarray,
    left_modes: np.ndarray,
    peripheral_values: np.ndarray,
    synthesis: np.ndarray,
    analysis: np.ndarray,
    spectral_parameter: complex,
    *,
    auxiliary_scale: float = 1.0,
    balance_channels: bool = True,
) -> DirectGrushinSystem:
    r"""Build a sparse realization of ``zI-Q U^2 Q``.

    The physical Schur complement of

    ``[[zI,-t Q U],[-t^-1 U Q,I]]``

    is the stored complement shift.  Both off-diagonal blocks are represented
    as a sparse base plus peripheral and packet low-rank channels.  Unlike
    RH-30, no dangerous-direction lift channel is inserted.
    """

    sparse = csc_matrix(matrix, dtype=np.complex128)
    dimension = int(sparse.shape[0])
    identity = eye(dimension, format="csc", dtype=np.complex128)
    scale = float(auxiliary_scale)
    if scale <= 0.0:
        raise ValueError("auxiliary scale must be positive")
    base = bmat(
        [
            [complex(spectral_parameter) * identity, -scale * sparse],
            [-sparse / scale, identity],
        ],
        format="csc",
    )

    right = np.asarray(right_modes)
    left = np.asarray(left_modes)
    peripheral = np.asarray(peripheral_values)
    synthesis_values = np.asarray(synthesis)
    analysis_values = np.asarray(analysis)
    peripheral_columns = right * peripheral[None, :]
    peripheral_rows = left.T
    u_synthesis = _one_step_bulk_dense(
        sparse, right, left, peripheral, synthesis_values
    )
    w_u = np.asarray(analysis_values @ sparse) - (
        analysis_values @ peripheral_columns
    ) @ peripheral_rows

    columns: list[np.ndarray] = []
    rows: list[np.ndarray] = []
    labels: list[str] = []

    def append(column: np.ndarray, row: np.ndarray, label: str) -> None:
        columns.append(np.asarray(column, dtype=np.complex128).reshape(-1))
        rows.append(np.asarray(row, dtype=np.complex128).reshape(-1))
        labels.append(label)

    for index in range(peripheral_columns.shape[1]):
        column = np.zeros(2 * dimension, dtype=np.complex128)
        row = np.zeros(2 * dimension, dtype=np.complex128)
        column[:dimension] = scale * peripheral_columns[:, index]
        row[dimension:] = peripheral_rows[index, :]
        append(column, row, f"top_peripheral_{index}")
    for index in range(synthesis_values.shape[1]):
        column = np.zeros(2 * dimension, dtype=np.complex128)
        row = np.zeros(2 * dimension, dtype=np.complex128)
        column[:dimension] = scale * synthesis_values[:, index]
        row[dimension:] = w_u[index, :]
        append(column, row, f"top_packet_{index}")
    for index in range(peripheral_columns.shape[1]):
        column = np.zeros(2 * dimension, dtype=np.complex128)
        row = np.zeros(2 * dimension, dtype=np.complex128)
        column[dimension:] = peripheral_columns[:, index] / scale
        row[:dimension] = peripheral_rows[index, :]
        append(column, row, f"bottom_peripheral_{index}")
    for index in range(synthesis_values.shape[1]):
        column = np.zeros(2 * dimension, dtype=np.complex128)
        row = np.zeros(2 * dimension, dtype=np.complex128)
        column[dimension:] = u_synthesis[:, index] / scale
        row[:dimension] = analysis_values[index, :]
        append(column, row, f"bottom_packet_{index}")

    x = np.column_stack(columns)
    y = np.vstack(rows)
    if balance_channels:
        for index in range(x.shape[1]):
            column_norm = float(np.linalg.norm(x[:, index]))
            row_norm = float(np.linalg.norm(y[index, :]))
            if column_norm > 0.0 and row_norm > 0.0:
                factor = float(np.sqrt(row_norm / column_norm))
                x[:, index] *= factor
                y[index, :] /= factor
    border = eye(x.shape[1], format="csc", dtype=np.complex128)
    bordered = bmat(
        [[base, csc_matrix(x)], [csc_matrix(y), -border]],
        format="csc",
    )
    return DirectGrushinSystem(
        matrix=bordered,
        physical_dimension=dimension,
        border_rank=int(x.shape[1]),
        channel_labels=tuple(labels),
    )
