"""Sparse Hermitian threshold dilations and exact pair congruences."""

from __future__ import annotations

from dataclasses import dataclass

import numpy as np
from scipy.sparse import bmat, csc_matrix, eye
from scipy.sparse.csgraph import reverse_cuthill_mckee


@dataclass(frozen=True)
class ThresholdInertiaSystem:
    """A paired Hermitian matrix whose inertia tests a singular threshold."""

    matrix: csc_matrix
    threshold: float
    source_dimension: int
    pair_permutation: np.ndarray
    scalar_permutation: np.ndarray

    @property
    def dimension(self) -> int:
        return int(self.matrix.shape[0])


def shifted_hermitian_dilation(matrix, threshold: float) -> csc_matrix:
    r"""Return ``[[ -a I, G ], [G*, -a I]]``.

    Its eigenvalues are ``s_j(G)-a`` and ``-s_j(G)-a``.  It therefore has
    exactly ``m`` positive eigenvalues if and only if ``s_min(G) > a``.
    """

    sparse = csc_matrix(matrix, dtype=np.complex128)
    rows, columns = sparse.shape
    if rows != columns:
        raise ValueError("the threshold dilation requires a square matrix")
    alpha = float(threshold)
    if alpha <= 0.0 or not np.isfinite(alpha):
        raise ValueError("the singular threshold must be positive and finite")
    identity = eye(rows, format="csc", dtype=np.complex128)
    return bmat(
        [[-alpha * identity, sparse], [sparse.conj().T, -alpha * identity]],
        format="csc",
    )


def paired_hadamard_congruence(matrix, threshold: float) -> csc_matrix:
    r"""Apply the exact integer congruence ``diag([[1,1],[1,-1]])``.

    The returned ordering first stores all plus coordinates and then all
    minus coordinates.  If ``C=G+G*`` and ``D=G*-G``, the matrix is

    ``[[C-2aI, D], [-D, -C-2aI]]``.

    This is congruent to the shifted Hermitian dilation and has the same
    inertia.  Unlike a normalized rotation, the congruence uses only integer
    coefficients and introduces no irrational normalization constant.
    """

    sparse = csc_matrix(matrix, dtype=np.complex128)
    rows, columns = sparse.shape
    if rows != columns:
        raise ValueError("the paired congruence requires a square matrix")
    alpha = float(threshold)
    if alpha <= 0.0 or not np.isfinite(alpha):
        raise ValueError("the singular threshold must be positive and finite")
    identity = eye(rows, format="csc", dtype=np.complex128)
    hermitian = sparse + sparse.conj().T
    skew = sparse.conj().T - sparse
    transformed = bmat(
        [
            [hermitian - 2.0 * alpha * identity, skew],
            [-skew, -hermitian - 2.0 * alpha * identity],
        ],
        format="csc",
    )
    transformed.sum_duplicates()
    transformed.eliminate_zeros()
    return transformed


def symmetric_pair_order(matrix) -> np.ndarray:
    """Return a reverse-Cuthill--McKee order on the pair-level graph."""

    sparse = csc_matrix(matrix)
    rows, columns = sparse.shape
    if rows != columns:
        raise ValueError("pair ordering requires a square matrix")
    graph = sparse.copy()
    graph.data = np.ones(graph.nnz, dtype=np.int8)
    graph = (graph + graph.T).astype(bool).astype(np.int8).tocsr()
    return np.asarray(
        reverse_cuthill_mckee(graph, symmetric_mode=True), dtype=np.int64
    )


def expand_pair_order(pair_order: np.ndarray, dimension: int) -> np.ndarray:
    """Interleave plus/minus coordinates according to one pair order."""

    order = np.asarray(pair_order, dtype=np.int64).reshape(-1)
    size = int(dimension)
    if order.shape != (size,) or not np.array_equal(np.sort(order), np.arange(size)):
        raise ValueError("pair order must be a permutation")
    return np.column_stack((order, size + order)).reshape(-1)


def build_threshold_inertia_system(
    matrix,
    threshold: float,
    *,
    pair_order: np.ndarray | None = None,
) -> ThresholdInertiaSystem:
    """Build and symmetrically permute the paired threshold matrix."""

    sparse = csc_matrix(matrix, dtype=np.complex128)
    dimension = int(sparse.shape[0])
    order = symmetric_pair_order(sparse) if pair_order is None else np.asarray(pair_order)
    scalar = expand_pair_order(order, dimension)
    transformed = paired_hadamard_congruence(sparse, threshold)
    permuted = transformed[scalar, :][:, scalar].tocsc()
    return ThresholdInertiaSystem(
        matrix=permuted,
        threshold=float(threshold),
        source_dimension=dimension,
        pair_permutation=np.asarray(order, dtype=np.int64),
        scalar_permutation=scalar,
    )


def dense_inertia(matrix: np.ndarray, *, tolerance: float = 1.0e-10) -> tuple[int, int, int]:
    """Reference inertia for small Hermitian tests."""

    values = np.linalg.eigvalsh(np.asarray(matrix, dtype=np.complex128))
    scale = max(float(np.max(np.abs(values))), 1.0)
    cutoff = float(tolerance) * scale
    positive = int(np.count_nonzero(values > cutoff))
    negative = int(np.count_nonzero(values < -cutoff))
    return positive, negative, int(values.size - positive - negative)
