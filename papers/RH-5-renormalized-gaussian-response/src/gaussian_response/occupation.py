"""Occupation-weighted transition estimators and safe CSR normalization."""

from __future__ import annotations

import numpy as np
import scipy.sparse as sp


def row_normalize_csr(matrix: sp.spmatrix) -> sp.csr_matrix:
    """Return a correctly row-normalized CSR matrix.

    CSR ``indices`` are column indices.  They must not be used to look up row
    sums; the row number of each stored value is encoded by ``indptr``.
    """
    result = matrix.tocsr(copy=True).astype(np.float64, copy=False)
    row_sums = np.asarray(result.sum(axis=1)).ravel()
    nonzero = row_sums != 0.0
    inverse = np.zeros_like(row_sums)
    inverse[nonzero] = 1.0 / row_sums[nonzero]
    result.data *= np.repeat(inverse, np.diff(result.indptr))
    return result


def occupation_weighted_average(
    kernels: np.ndarray,
    occupations: np.ndarray,
) -> np.ndarray:
    """Compute the row-normalized expected flow matrix.

    ``kernels[t, i, j]`` is the time-t conditional kernel and
    ``occupations[t, i]`` is the source distribution.  Every source row must
    have positive total occupation.
    """
    kernels = np.asarray(kernels, dtype=np.float64)
    occupations = np.asarray(occupations, dtype=np.float64)
    if kernels.ndim != 3 or occupations.shape != kernels.shape[:2]:
        raise ValueError("incompatible kernel and occupation arrays")
    denominators = np.sum(occupations, axis=0)
    if np.any(denominators <= 0.0):
        raise ValueError("every source row needs positive total occupation")
    flows = np.einsum("ti,tij->ij", occupations, kernels, optimize=True)
    return flows / denominators[:, np.newaxis]
