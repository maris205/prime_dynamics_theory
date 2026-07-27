"""Intrinsic normalizations and sparse extraction for conjugate quartets.

The numerical layer deliberately keeps extraction separate from the exact
algebra.  All normalizations below act only on a four-root multiset and are
therefore easy to audit independently of the matrix model.
"""

from __future__ import annotations

from dataclasses import dataclass
import math

import numpy as np
from scipy import sparse
from scipy.sparse.linalg import eigs


@dataclass(frozen=True)
class NormalizedQuartet:
    roots: np.ndarray
    center: complex
    scale: float


def monic_coefficients(roots: np.ndarray) -> np.ndarray:
    values = np.asarray(roots, dtype=complex).reshape(-1)
    if values.size != 4:
        raise ValueError("a quartet is required")
    return np.poly(values)


def determinant_radius_normalize(roots: np.ndarray) -> NormalizedQuartet:
    """Divide by the geometric mean root modulus, without recentering."""

    values = np.asarray(roots, dtype=complex).reshape(-1)
    if values.size != 4:
        raise ValueError("a quartet is required")
    radius = float(abs(np.prod(values)) ** 0.25)
    if not math.isfinite(radius) or radius <= np.finfo(float).tiny:
        raise ValueError("the determinant radius must be positive")
    return NormalizedQuartet(values / radius, 0.0j, radius)


def centered_rms_normalize(roots: np.ndarray) -> NormalizedQuartet:
    """Remove the root barycenter and impose mean square modulus one."""

    values = np.asarray(roots, dtype=complex).reshape(-1)
    if values.size != 4:
        raise ValueError("a quartet is required")
    center = complex(np.mean(values))
    centered = values - center
    radius = float(np.sqrt(np.mean(np.abs(centered) ** 2)))
    if not math.isfinite(radius) or radius <= np.finfo(float).tiny:
        raise ValueError("the centered RMS radius must be positive")
    return NormalizedQuartet(centered / radius, center, radius)


def coefficient_distance(first: np.ndarray, second: np.ndarray) -> dict[str, float]:
    left = monic_coefficients(first)
    right = monic_coefficients(second)
    difference = left - right
    return {
        "maximum_absolute_error": float(np.max(np.abs(difference))),
        "relative_l2_error": float(
            np.linalg.norm(difference) / max(np.linalg.norm(left), np.finfo(float).tiny)
        ),
    }


def haar_coarse_embedding(dimension: int) -> sparse.csr_matrix:
    """Sparse pair-average embedding used by the inherited dyadic model."""

    size = int(dimension)
    if size < 4 or size % 2:
        raise ValueError("an even dimension at least four is required")
    columns = np.repeat(np.arange(size // 2), 2)
    rows = np.arange(size)
    data = np.full(size, 1.0 / math.sqrt(2.0))
    return sparse.coo_matrix((data, (rows, columns)), shape=(size, size // 2)).tocsr()


def outer_bulk_quartet(matrix: sparse.spmatrix, candidate_count: int = 16) -> np.ndarray:
    """Extract the four largest-modulus eigenvalues after two inherited modes.

    The folded Gaussian model has a Perron root near one and a distinguished
    negative real parity root.  The historical ``spectral_bulk`` routine
    replaces those two eigenvalues by zero.  Consequently its outer quartet
    can be obtained without forming the dense deflated matrix: resolve a
    sufficiently large modulus cloud, delete the same two roots, and retain
    the next four.  The runner records conjugacy and radial-gap diagnostics so
    that a failed cloud resolution cannot pass silently.
    """

    operator = sparse.csr_matrix(matrix, dtype=float)
    n = operator.shape[0]
    if operator.shape[1] != n or n < 10:
        raise ValueError("a square matrix of dimension at least ten is required")
    k = min(int(candidate_count), n - 2)
    values = eigs(
        operator,
        k=k,
        which="LM",
        return_eigenvectors=False,
        tol=2.0e-12,
        maxiter=max(20000, 40 * n),
        ncv=min(n, max(2 * k + 1, 40)),
    )
    values = np.asarray(values, dtype=complex)
    perron = int(np.argmin(np.abs(values - 1.0)))
    available = [index for index in range(values.size) if index != perron]
    nearly_real_negative = [
        index for index in available
        if abs(values[index].imag) <= 2.0e-8 and values[index].real < -1.0e-8
    ]
    if not nearly_real_negative:
        raise RuntimeError("the negative real parity root was not resolved")
    parity = min(nearly_real_negative, key=lambda index: values[index].real)
    remaining = np.delete(values, (perron, parity))
    order = np.argsort(-np.abs(remaining))
    return remaining[order[:4]] / 0.85


def conjugacy_error(roots: np.ndarray) -> float:
    values = np.asarray(roots, dtype=complex).reshape(-1)
    return float(max(np.min(np.abs(values - np.conj(value))) for value in values))


def radial_gap_in_candidate_cloud(matrix: sparse.spmatrix, candidate_count: int = 16) -> float:
    """Diagnostic helper retained for focused tests; not used for selection."""

    values = eigs(
        sparse.csr_matrix(matrix, dtype=float),
        k=min(int(candidate_count), matrix.shape[0] - 2),
        which="LM",
        return_eigenvectors=False,
        tol=2.0e-12,
        maxiter=max(20000, 40 * matrix.shape[0]),
    )
    moduli = np.sort(np.abs(values))[::-1]
    return float(moduli[5] - moduli[6])
