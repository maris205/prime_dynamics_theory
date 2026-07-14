"""Sparse folded Gaussian matrices and branch-isolated return operators."""

from __future__ import annotations

from dataclasses import dataclass

import numpy as np
from scipy.sparse import csr_matrix


def positive_midpoints(dimension: int) -> np.ndarray:
    """Return midpoint nodes on ``[0,1]``."""

    dimension = int(dimension)
    if dimension < 4:
        raise ValueError("dimension must be at least four")
    return (np.arange(dimension, dtype=np.float64) + 0.5) / dimension


def sparse_folded_gaussian_matrix(
    dimension: int,
    sigma: float,
    *,
    u: float,
    support_standard_deviations: float = 8.0,
    chunk_rows: int = 2048,
) -> csr_matrix:
    """Build the row-normalized folded Gaussian midpoint operator."""

    dimension = int(dimension)
    sigma = float(sigma)
    if sigma <= 0.0:
        raise ValueError("sigma must be positive")
    if support_standard_deviations < 5.0:
        raise ValueError("Gaussian support cutoff must be at least five")

    half_width = int(np.ceil(support_standard_deviations * sigma * dimension)) + 2
    offsets = np.arange(-half_width, half_width + 1, dtype=np.int32)
    data_parts: list[np.ndarray] = []
    index_parts: list[np.ndarray] = []
    indptr = [0]

    for lower in range(0, dimension, int(chunk_rows)):
        upper = min(dimension, lower + int(chunk_rows))
        x = positive_midpoints(dimension)[lower:upper]
        means = 1.0 - float(u) * x * x
        centers = np.floor(np.abs(means) * dimension - 0.5).astype(np.int64)
        indices = centers[:, None] + offsets[None, :]
        valid = (indices >= 0) & (indices < dimension)
        clipped = np.clip(indices, 0, dimension - 1)
        destinations = (clipped + 0.5) / dimension
        positive_log = -0.5 * ((destinations - means[:, None]) / sigma) ** 2
        negative_log = -0.5 * ((-destinations - means[:, None]) / sigma) ** 2
        log_weights = np.logaddexp(positive_log, negative_log)
        log_weights[~valid] = -np.inf
        maxima = np.max(log_weights, axis=1, keepdims=True)
        weights = np.exp(log_weights - maxima)
        weights[~valid] = 0.0
        weights /= np.sum(weights, axis=1, keepdims=True)

        for local_row in range(upper - lower):
            mask = valid[local_row]
            row_indices = indices[local_row, mask].astype(np.int32, copy=False)
            row_data = weights[local_row, mask]
            index_parts.append(row_indices)
            data_parts.append(row_data)
            indptr.append(indptr[-1] + row_indices.size)

    return csr_matrix(
        (
            np.concatenate(data_parts),
            np.concatenate(index_parts),
            np.asarray(indptr, dtype=np.int64),
        ),
        shape=(dimension, dimension),
    )


def packet_masks(
    grid: np.ndarray,
    points: np.ndarray,
    physical_widths: np.ndarray,
    *,
    window_multiple: float,
    critical_partition: float,
) -> list[np.ndarray]:
    """Return time-labeled packet windows with the final critical branch cut."""

    nodes = np.asarray(grid, dtype=np.float64)
    centers = np.asarray(points, dtype=np.float64)
    widths = np.asarray(physical_widths, dtype=np.float64)
    if centers.shape != widths.shape or centers.ndim != 1:
        raise ValueError("points and widths must be equal-length vectors")
    if window_multiple <= 0.0 or np.any(widths <= 0.0):
        raise ValueError("all window widths must be positive")
    masks = [
        np.abs(nodes - center) <= float(window_multiple) * width
        for center, width in zip(centers, widths)
    ]
    masks[-1] &= nodes < float(critical_partition)
    return masks


def apply_local_return(
    matrix: csr_matrix,
    masks: list[np.ndarray],
    vector: np.ndarray,
) -> np.ndarray:
    """Apply ``A_0 A_1 ... A_(k-1)`` to an endpoint-supported observable."""

    result = np.asarray(vector, dtype=np.float64)
    for index in range(len(masks) - 1, -1, -1):
        result = matrix @ (matrix @ result)
        result[~masks[index]] = 0.0
    return result


@dataclass(frozen=True)
class ReturnEigenpair:
    eigenvalue: float
    vector: np.ndarray
    residual: float
    iterations: int


def principal_return_eigenpair(
    matrix: csr_matrix,
    masks: list[np.ndarray],
    initial: np.ndarray,
    *,
    iterations: int = 12,
) -> ReturnEigenpair:
    """Resolve the positive principal return mode by normalized power iteration."""

    vector = np.asarray(initial, dtype=np.float64).copy()
    vector[~masks[0]] = 0.0
    norm = np.linalg.norm(vector)
    if norm == 0.0:
        raise ValueError("initial vector has no endpoint-window mass")
    vector /= norm
    for _ in range(int(iterations)):
        updated = apply_local_return(matrix, masks, vector)
        norm = np.linalg.norm(updated)
        if norm == 0.0:
            raise RuntimeError("local return annihilated the iterate")
        vector = updated / norm
    updated = apply_local_return(matrix, masks, vector)
    eigenvalue = float(np.vdot(vector, updated).real)
    residual = float(
        np.linalg.norm(updated - eigenvalue * vector) / np.linalg.norm(updated)
    )
    return ReturnEigenpair(
        eigenvalue=eigenvalue,
        vector=vector,
        residual=residual,
        iterations=int(iterations),
    )
