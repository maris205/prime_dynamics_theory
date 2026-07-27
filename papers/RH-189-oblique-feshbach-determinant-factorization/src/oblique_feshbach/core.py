"""Exact finite-dimensional Feshbach factorization in oblique coordinates."""

from __future__ import annotations

import numpy as np


def adjoint(matrix: np.ndarray) -> np.ndarray:
    return np.asarray(matrix).conj().T


def oblique_coordinates(right_frame: np.ndarray, left_frame: np.ndarray) -> dict[str, np.ndarray]:
    right = np.asarray(right_frame)
    left = np.asarray(left_frame)
    if right.ndim != 2 or left.shape != right.shape:
        raise ValueError("frames must have one shape")
    rank = right.shape[1]
    if np.linalg.norm(adjoint(left) @ right - np.eye(rank), 2) > 1e-8:
        raise ValueError("frames must be biorthogonal")
    _, singular, right_adjoint = np.linalg.svd(adjoint(left), full_matrices=True)
    if singular[-1] <= np.finfo(float).eps * max(left.shape) * singular[0]:
        raise ValueError("left frame is rank deficient")
    complement = adjoint(right_adjoint)[..., rank:]
    coordinate_matrix = np.column_stack([right, complement])
    if abs(np.linalg.det(coordinate_matrix)) <= np.finfo(float).eps:
        raise ValueError("oblique coordinate matrix is singular")
    inverse = np.linalg.inv(coordinate_matrix)
    dual_complement = adjoint(inverse[rank:, :])
    if np.linalg.norm(inverse[:rank, :] - adjoint(left), 2) > 1e-7:
        raise ValueError("coordinate dual does not match the left frame")
    return {
        "right_frame": right,
        "left_frame": left,
        "complement_frame": complement,
        "dual_complement_frame": dual_complement,
        "coordinate_matrix": coordinate_matrix,
        "coordinate_inverse": inverse,
    }


def block_coordinates(
    operator: np.ndarray,
    right_frame: np.ndarray,
    left_frame: np.ndarray,
) -> dict[str, np.ndarray]:
    data = oblique_coordinates(right_frame, left_frame)
    dynamics = np.asarray(operator)
    right = data["right_frame"]
    complement = data["complement_frame"]
    left = data["left_frame"]
    dual_complement = data["dual_complement_frame"]
    return {
        **data,
        "K": adjoint(left) @ dynamics @ right,
        "B": adjoint(left) @ dynamics @ complement,
        "C": adjoint(dual_complement) @ dynamics @ right,
        "D": adjoint(dual_complement) @ dynamics @ complement,
    }


def feshbach_reduced_matrix(
    spectral_parameter: complex,
    blocks: dict[str, np.ndarray],
) -> np.ndarray:
    z = complex(spectral_parameter)
    D = np.asarray(blocks["D"])
    K = np.asarray(blocks["K"])
    B = np.asarray(blocks["B"])
    C = np.asarray(blocks["C"])
    complement_resolvent = np.linalg.inv(z * np.eye(D.shape[0]) - D)
    return z * np.eye(K.shape[0]) - K - B @ complement_resolvent @ C


def feshbach_determinant_identity(
    spectral_parameter: complex,
    operator: np.ndarray,
    blocks: dict[str, np.ndarray],
) -> dict[str, complex | float]:
    z = complex(spectral_parameter)
    dynamics = np.asarray(operator)
    D = np.asarray(blocks["D"])
    reduced = feshbach_reduced_matrix(z, blocks)
    left = np.linalg.det(z * np.eye(dynamics.shape[0]) - dynamics)
    right = np.linalg.det(z * np.eye(D.shape[0]) - D) * np.linalg.det(reduced)
    relative = abs(left - right) / max(abs(left), abs(right), np.finfo(float).tiny)
    return {
        "full_determinant": complex(left),
        "factorized_determinant": complex(right),
        "relative_error": float(relative),
    }
