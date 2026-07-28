"""Biorthogonal finite-dimensional spectral projectors."""

from __future__ import annotations

import numpy as np


def match_eigenvalues(
    computed: np.ndarray,
    targets: np.ndarray,
    *,
    conjugate_targets: bool = False,
) -> tuple[np.ndarray, float]:
    """Greedily match distinct computed eigenvalues to a target multiset."""

    values = np.asarray(computed, dtype=complex).reshape(-1)
    wanted = np.asarray(targets, dtype=complex).reshape(-1)
    if wanted.size > values.size:
        raise ValueError("there are fewer computed values than targets")
    unused = set(range(values.size))
    indices: list[int] = []
    maximum_error = 0.0
    for target in wanted:
        reference = np.conj(target) if conjugate_targets else target
        index = min(unused, key=lambda candidate: abs(values[candidate] - reference))
        unused.remove(index)
        indices.append(index)
        maximum_error = max(maximum_error, float(abs(values[index] - reference)))
    return np.asarray(indices, dtype=int), maximum_error


def overlap_matrix(right: np.ndarray, left: np.ndarray) -> np.ndarray:
    right_basis = np.asarray(right, dtype=complex)
    left_basis = np.asarray(left, dtype=complex)
    if right_basis.ndim != 2 or left_basis.ndim != 2:
        raise ValueError("two basis matrices are required")
    if right_basis.shape != left_basis.shape:
        raise ValueError("left and right bases must have the same shape")
    return left_basis.conj().T @ right_basis


def low_rank_singular_values(first: np.ndarray, second: np.ndarray) -> np.ndarray:
    """Return the nonzero singular values of ``first @ second^*``."""

    left = np.asarray(first, dtype=complex)
    right = np.asarray(second, dtype=complex)
    if left.ndim != 2 or right.ndim != 2 or left.shape[1] != right.shape[1]:
        raise ValueError("compatible low-rank factors are required")
    q_left, r_left = np.linalg.qr(left, mode="reduced")
    q_right, r_right = np.linalg.qr(right, mode="reduced")
    del q_left, q_right
    return np.linalg.svd(r_left @ r_right.conj().T, compute_uv=False)


def biorthogonal_projector_metrics(
    right: np.ndarray,
    left: np.ndarray,
) -> dict[str, float | np.ndarray]:
    """Return the small-matrix data for ``P=R(L^*R)^{-1}L^*``."""

    right_basis = np.asarray(right, dtype=complex)
    left_basis = np.asarray(left, dtype=complex)
    gram = overlap_matrix(right_basis, left_basis)
    singular = np.linalg.svd(gram, compute_uv=False)
    if singular[-1] <= np.finfo(float).tiny:
        raise np.linalg.LinAlgError("the left/right overlap is singular")
    inverse = np.linalg.inv(gram)
    primal = right_basis @ inverse
    projector_singular = low_rank_singular_values(primal, left_basis)
    return {
        "overlap": gram,
        "inverse_overlap": inverse,
        "minimum_overlap_singular_value": float(singular[-1]),
        "maximum_overlap_singular_value": float(singular[0]),
        "overlap_condition_number": float(singular[0] / singular[-1]),
        "projector_operator_norm": float(projector_singular[0]),
        "projector_frobenius_norm": float(np.linalg.norm(projector_singular)),
    }


def low_rank_frobenius_norm(first: np.ndarray, second: np.ndarray) -> float:
    singular = low_rank_singular_values(first, second)
    return float(np.linalg.norm(singular))


def commutator_frobenius_norm(
    matrix,
    right: np.ndarray,
    left: np.ndarray,
    inverse_overlap: np.ndarray,
) -> float:
    """Compute ``||AP-PA||_F`` without forming the dense projector."""

    operator = matrix
    right_basis = np.asarray(right, dtype=complex)
    left_basis = np.asarray(left, dtype=complex)
    inverse = np.asarray(inverse_overlap, dtype=complex)
    ar = operator @ right_basis
    atl = operator.T.conj() @ left_basis
    first = np.hstack((ar @ inverse, -right_basis @ inverse))
    second = np.hstack((left_basis, atl))
    return low_rank_frobenius_norm(first, second)


def eigenpair_residuals(
    matrix,
    vectors: np.ndarray,
    eigenvalues: np.ndarray,
) -> np.ndarray:
    basis = np.asarray(vectors, dtype=complex)
    values = np.asarray(eigenvalues, dtype=complex).reshape(-1)
    if basis.shape[1] != values.size:
        raise ValueError("one eigenvalue is required per vector")
    residual = matrix @ basis - basis * values[None, :]
    return np.linalg.norm(residual, axis=0)
