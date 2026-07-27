"""Linear-algebra primitives for adjacent-level packet transport."""

from __future__ import annotations

import math

import numpy as np
from scipy.optimize import linear_sum_assignment


def haar_embedding(fine_dimension: int) -> np.ndarray:
    """Embed coarse cell values isometrically into a dyadic fine grid."""

    fine = int(fine_dimension)
    if fine < 2 or fine % 2:
        raise ValueError("fine_dimension must be positive and even")
    coarse = fine // 2
    result = np.zeros((fine, coarse), dtype=float)
    columns = np.arange(coarse)
    result[2 * columns, columns] = 1.0 / math.sqrt(2.0)
    result[2 * columns + 1, columns] = 1.0 / math.sqrt(2.0)
    return result


def _basis(matrix: np.ndarray) -> np.ndarray:
    values = np.asarray(matrix, dtype=complex)
    if values.ndim != 2 or values.shape[1] < 1:
        raise ValueError("a nonempty matrix is required")
    return np.linalg.qr(values, mode="reduced")[0]


def principal_data(first: np.ndarray, second: np.ndarray) -> dict[str, object]:
    """Return all principal cosines and the largest principal sine."""

    left = _basis(first)
    right = _basis(second)
    if left.shape != right.shape:
        raise ValueError("subspaces must have equal ambient dimension and rank")
    singular = np.clip(
        np.linalg.svd(left.conj().T @ right, compute_uv=False), 0.0, 1.0
    )
    minimum = float(singular[-1])
    return {
        "principal_cosines": [float(value) for value in singular],
        "minimum_principal_cosine": minimum,
        "maximum_principal_sine": float(math.sqrt(max(0.0, 1.0 - minimum**2))),
    }


def matched_assignment(
    coarse_values: np.ndarray, fine_values: np.ndarray
) -> list[int]:
    """Find the minimum-total-distance one-to-one spectral assignment."""

    coarse = np.asarray(coarse_values, dtype=complex).reshape(-1)
    fine = np.asarray(fine_values, dtype=complex).reshape(-1)
    if coarse.size != fine.size or coarse.size < 1:
        raise ValueError("equal nonempty packets are required")
    rows, columns = linear_sum_assignment(np.abs(coarse[:, None] - fine[None, :]))
    assignment = np.empty(coarse.size, dtype=int)
    assignment[rows] = columns
    return assignment.tolist()


def biorthogonal_eigenpacket(
    right: np.ndarray, left: np.ndarray
) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    """Biorthogonalize matching right/left eigenvector columns."""

    vectors = np.asarray(right, dtype=complex)
    duals = np.asarray(left, dtype=complex)
    if vectors.shape != duals.shape or vectors.ndim != 2:
        raise ValueError("matching two-dimensional frames are required")
    gram = duals.conj().T @ vectors
    normalized_duals = duals @ np.linalg.inv(gram).conj().T
    projector = vectors @ normalized_duals.conj().T
    return vectors, normalized_duals, projector


def channel_state(
    right: np.ndarray,
    left: np.ndarray,
    source: np.ndarray,
    observation: np.ndarray,
) -> tuple[np.ndarray, np.ndarray, complex]:
    """Return P S, P^* O^*, and the source-observation residue."""

    vector = np.asarray(right, dtype=complex).reshape(-1)
    dual = np.asarray(left, dtype=complex).reshape(-1)
    seed = np.asarray(source, dtype=complex)
    output = np.asarray(observation, dtype=complex)
    source_coefficient = dual.conj() @ seed
    observation_coefficient = output @ vector
    x_state = np.outer(vector, source_coefficient)
    y_state = np.outer(dual, np.conj(observation_coefficient))
    return x_state, y_state, complex(source_coefficient @ observation_coefficient)


def relative_frobenius_defect(reference: np.ndarray, candidate: np.ndarray) -> float:
    """Measure a Frobenius defect relative to the reference norm."""

    target = np.asarray(reference, dtype=complex)
    value = np.asarray(candidate, dtype=complex)
    if target.shape != value.shape:
        raise ValueError("matrix shapes must agree")
    return float(
        np.linalg.norm(target - value, "fro")
        / max(np.linalg.norm(target, "fro"), np.finfo(float).tiny)
    )


def coefficient_error(coarse_values: np.ndarray, fine_values: np.ndarray) -> dict[str, object]:
    """Compare coefficients of two monic packet characteristic polynomials."""

    coarse = np.poly(np.asarray(coarse_values, dtype=complex))
    fine = np.poly(np.asarray(fine_values, dtype=complex))
    difference = fine - coarse
    return {
        "coarse_coefficients_real": [float(value.real) for value in coarse],
        "coarse_coefficients_imag": [float(value.imag) for value in coarse],
        "fine_coefficients_real": [float(value.real) for value in fine],
        "fine_coefficients_imag": [float(value.imag) for value in fine],
        "maximum_absolute_coefficient_error": float(np.max(np.abs(difference))),
        "relative_l2_coefficient_error": float(
            np.linalg.norm(difference) / max(np.linalg.norm(fine), np.finfo(float).tiny)
        ),
    }
