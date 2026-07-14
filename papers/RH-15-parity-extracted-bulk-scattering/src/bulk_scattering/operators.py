"""Sparse folded Gaussian operators and their parity-extracted spectra."""

from __future__ import annotations

from dataclasses import dataclass

import numpy as np
from scipy.sparse import csr_matrix
from scipy.sparse.linalg import eigs

from .deterministic import U_CRITICAL


def positive_midpoints(dimension: int) -> np.ndarray:
    if int(dimension) < 4:
        raise ValueError("dimension must be at least four")
    return (np.arange(int(dimension), dtype=np.float64) + 0.5) / int(dimension)


def sparse_folded_gaussian_matrix(
    dimension: int,
    sigma: float,
    *,
    u: float = U_CRITICAL,
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
        x = (np.arange(lower, upper, dtype=np.float64) + 0.5) / dimension
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


@dataclass(frozen=True)
class BulkSpectrum:
    eigenvalues: np.ndarray
    perron: complex
    parity: complex
    bulk: np.ndarray
    exact_bulk_trace_two: float


def _deterministic_start(dimension: int) -> np.ndarray:
    index = np.arange(int(dimension), dtype=np.float64)
    vector = np.sin((index + 0.5) * np.sqrt(2.0))
    vector += 0.37 * np.cos((index + 0.5) * np.sqrt(3.0))
    return vector / np.linalg.norm(vector)


def resolve_bulk_spectrum(
    matrix: csr_matrix,
    *,
    eigenvalue_count: int = 80,
    tolerance: float = 3.0e-10,
) -> BulkSpectrum:
    """Resolve the leading spectrum and remove the Perron/parity modes."""

    count = min(int(eigenvalue_count), matrix.shape[0] - 2)
    values = eigs(
        matrix,
        k=count,
        which="LM",
        tol=float(tolerance),
        maxiter=18000,
        v0=_deterministic_start(matrix.shape[0]),
        return_eigenvectors=False,
    )
    values = values[np.argsort(-np.abs(values))]
    perron_index = int(np.argmin(np.abs(values - 1.0)))
    remaining = np.delete(np.arange(values.size), perron_index)
    real_candidates = remaining[np.abs(values[remaining].imag) < 2.0e-8]
    if not real_candidates.size:
        raise RuntimeError("no real parity resonance was resolved")
    parity_index = int(real_candidates[np.argmin(values[real_candidates].real)])
    bulk = np.delete(values, (perron_index, parity_index))
    trace_two = float(matrix.multiply(matrix.T).sum())
    exact_bulk_trace_two = trace_two - 1.0 - float(values[parity_index].real) ** 2
    return BulkSpectrum(
        eigenvalues=values,
        perron=complex(values[perron_index]),
        parity=complex(values[parity_index]),
        bulk=np.asarray(bulk),
        exact_bulk_trace_two=float(exact_bulk_trace_two),
    )
