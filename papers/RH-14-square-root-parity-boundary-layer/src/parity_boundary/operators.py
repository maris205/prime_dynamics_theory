"""Sparse folded Gaussian operators and peripheral eigendata.

The rows of the matrix act on observables.  The positive-state folding is
exact for the nonzero spectrum because ``f_u(x)=1-u*x**2`` is even.
"""

from __future__ import annotations

from dataclasses import dataclass

import numpy as np
from scipy.sparse import csr_matrix
from scipy.sparse.linalg import eigs


U_CRITICAL = 1.5436890126920763615708559718017479865
R_FIXED = U_CRITICAL - 1.0
LAMBDA_FIXED = 2.0 * U_CRITICAL * R_FIXED


def positive_midpoints(dimension: int) -> np.ndarray:
    """Return midpoint nodes on ``[0,1]``."""

    if dimension < 4:
        raise ValueError("dimension must be at least four")
    return (np.arange(int(dimension), dtype=np.float64) + 0.5) / dimension


def sparse_folded_gaussian_matrix(
    dimension: int,
    sigma: float,
    *,
    u: float = U_CRITICAL,
    support_standard_deviations: float = 8.0,
    chunk_rows: int = 2048,
) -> csr_matrix:
    """Build a sparse midpoint approximation of the folded Markov operator.

    Only destinations within ``support_standard_deviations`` standard
    deviations of ``abs(f_u(x))`` are retained.  At the default cutoff the
    omitted row mass is below double-precision roundoff.  Every retained row
    is renormalized exactly, so the returned matrix is row stochastic.
    """

    dimension = int(dimension)
    sigma = float(sigma)
    if sigma <= 0.0:
        raise ValueError("sigma must be positive")
    if support_standard_deviations < 5.0:
        raise ValueError("the Gaussian cutoff must be at least five standard deviations")
    if chunk_rows < 1:
        raise ValueError("chunk_rows must be positive")

    half_width = int(np.ceil(support_standard_deviations * sigma * dimension)) + 2
    offsets = np.arange(-half_width, half_width + 1, dtype=np.int32)
    data_parts: list[np.ndarray] = []
    index_parts: list[np.ndarray] = []
    indptr = [0]

    for lower in range(0, dimension, chunk_rows):
        upper = min(dimension, lower + chunk_rows)
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
        row_maxima = np.max(log_weights, axis=1, keepdims=True)
        weights = np.exp(log_weights - row_maxima)
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
class PeripheralSpectrum:
    """Leading spectral data of a folded row-stochastic matrix."""

    eigenvalues: np.ndarray
    perron: complex
    parity: complex
    bulk_radius_observed: float

    @property
    def parity_gap(self) -> float:
        return float(1.0 + self.parity.real)


def peripheral_spectrum(
    matrix: csr_matrix,
    *,
    eigenvalue_count: int = 6,
    tolerance: float = 5.0e-12,
) -> PeripheralSpectrum:
    """Resolve the Perron root, negative parity root, and observed bulk."""

    count = min(int(eigenvalue_count), matrix.shape[0] - 2)
    values = eigs(
        matrix,
        k=count,
        which="LM",
        tol=tolerance,
        maxiter=6000,
        return_eigenvectors=False,
    )
    values = values[np.argsort(-np.abs(values))]
    perron_index = int(np.argmin(np.abs(values - 1.0)))
    candidates = np.delete(np.arange(values.size), perron_index)
    near_real = candidates[np.abs(values[candidates].imag) < 2.0e-8]
    if near_real.size == 0:
        raise RuntimeError("no real parity resonance was resolved")
    parity_index = int(near_real[np.argmin(values[near_real].real)])
    bulk = np.delete(values, (perron_index, parity_index))
    return PeripheralSpectrum(
        eigenvalues=values,
        perron=complex(values[perron_index]),
        parity=complex(values[parity_index]),
        bulk_radius_observed=float(np.max(np.abs(bulk), initial=0.0)),
    )


@dataclass(frozen=True)
class ParityEigenvectors:
    """Normalized right parity observable and left signed cell masses."""

    eigenvalue: float
    right_observable: np.ndarray
    left_cell_masses: np.ndarray


def parity_eigenvectors(
    matrix: csr_matrix,
    sigma: float,
    *,
    r: float = R_FIXED,
    tolerance: float = 5.0e-12,
) -> ParityEigenvectors:
    """Return consistently normalized left and right parity eigenvectors.

    The right vector is scaled so that its two outer component averages differ
    by two.  The left vector is then normalized to pair to one with it and is
    oriented positively on the lower component.
    """

    values, right = eigs(matrix, k=4, which="LM", tol=tolerance, maxiter=6000)
    real_candidates = np.flatnonzero(np.abs(values.imag) < 2.0e-8)
    parity_index = int(real_candidates[np.argmin(values[real_candidates].real)])
    parity = float(values[parity_index].real)
    observable = np.asarray(right[:, parity_index].real)

    grid = positive_midpoints(matrix.shape[0])
    margin = max(12.0 * float(sigma), 0.02)
    lower = grid < r - margin
    upper = grid > r + margin
    lower_mean = float(np.mean(observable[lower]))
    upper_mean = float(np.mean(observable[upper]))
    observable *= 2.0 / (lower_mean - upper_mean)
    if np.mean(observable[lower]) < 0.0:
        observable *= -1.0

    left_values, left = eigs(
        matrix.T,
        k=4,
        which="LM",
        tol=tolerance,
        maxiter=6000,
    )
    left_index = int(np.argmin(np.abs(left_values - parity)))
    masses = np.asarray(left[:, left_index].real)
    pairing = float(np.dot(masses, observable))
    masses /= pairing
    if np.sum(masses[grid < r]) < 0.0:
        masses *= -1.0
        observable *= -1.0

    return ParityEigenvectors(
        eigenvalue=parity,
        right_observable=observable,
        left_cell_masses=masses,
    )
