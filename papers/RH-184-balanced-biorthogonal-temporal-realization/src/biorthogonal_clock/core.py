"""Canonical balanced biorthogonal frames for two finite subspaces."""

from __future__ import annotations

import math

import numpy as np


def adjoint(matrix: np.ndarray) -> np.ndarray:
    return np.asarray(matrix).conj().T


def operator_norm(matrix: np.ndarray) -> float:
    return float(np.linalg.norm(np.asarray(matrix), 2))


def orthonormal_basis(synthesis: np.ndarray) -> np.ndarray:
    matrix = np.asarray(synthesis)
    if matrix.ndim != 2 or matrix.shape[0] < matrix.shape[1]:
        raise ValueError("synthesis must be tall")
    basis, triangular = np.linalg.qr(matrix, mode="reduced")
    singular = np.linalg.svd(triangular, compute_uv=False)
    tolerance = np.finfo(float).eps * max(matrix.shape) * float(singular[0])
    if float(singular[-1]) <= tolerance:
        raise ValueError("synthesis is rank deficient")
    return basis


def balanced_biorthogonal_frames(
    right_synthesis: np.ndarray,
    left_synthesis: np.ndarray,
) -> dict[str, np.ndarray | float]:
    right_basis = orthonormal_basis(right_synthesis)
    left_basis = orthonormal_basis(left_synthesis)
    if right_basis.shape != left_basis.shape:
        raise ValueError("right and left subspaces must have equal ambient dimension and rank")
    cross = adjoint(left_basis) @ right_basis
    left_singular, singular, right_adjoint = np.linalg.svd(cross)
    tolerance = np.finfo(float).eps * max(cross.shape) * float(singular[0])
    if float(singular[-1]) <= tolerance:
        raise ValueError("right and left subspaces are not transverse")
    inverse_half = np.diag(1.0 / np.sqrt(singular))
    right_frame = right_basis @ adjoint(right_adjoint) @ inverse_half
    left_frame = left_basis @ left_singular @ inverse_half
    minimum = float(singular[-1])
    return {
        "right_basis": right_basis,
        "left_basis": left_basis,
        "cross_gram": cross,
        "cross_singular_values": singular,
        "right_frame": right_frame,
        "left_frame": left_frame,
        "minimum_cross_singular_value": minimum,
        "optimal_frame_norm": 1.0 / math.sqrt(minimum),
        "optimal_norm_product": 1.0 / minimum,
    }


def oblique_projector(right_frame: np.ndarray, left_frame: np.ndarray) -> np.ndarray:
    right = np.asarray(right_frame)
    left = np.asarray(left_frame)
    if right.shape != left.shape:
        raise ValueError("biorthogonal frames must have one shape")
    return right @ adjoint(left)


def biorthogonal_residuals(
    operator: np.ndarray,
    right_frame: np.ndarray,
    left_frame: np.ndarray,
) -> dict[str, np.ndarray | float]:
    dynamics = np.asarray(operator)
    right = np.asarray(right_frame)
    left = np.asarray(left_frame)
    if dynamics.ndim != 2 or dynamics.shape[0] != dynamics.shape[1] or right.shape != left.shape:
        raise ValueError("invalid operator or frames")
    if right.shape[0] != dynamics.shape[0]:
        raise ValueError("operator and frames do not share an ambient space")
    projector = oblique_projector(right, left)
    compressed = adjoint(left) @ dynamics @ right
    right_residual = (np.eye(dynamics.shape[0]) - projector) @ dynamics @ right
    left_residual = (np.eye(dynamics.shape[0]) - adjoint(projector)) @ adjoint(dynamics) @ left
    return {
        "compressed": compressed,
        "projector": projector,
        "right_residual": right_residual,
        "left_residual": left_residual,
        "right_residual_norm": operator_norm(right_residual),
        "left_residual_norm": operator_norm(left_residual),
    }


def gauge_transform(
    right_frame: np.ndarray,
    left_frame: np.ndarray,
    gauge: np.ndarray,
) -> tuple[np.ndarray, np.ndarray]:
    matrix = np.asarray(gauge)
    if matrix.ndim != 2 or matrix.shape[0] != matrix.shape[1]:
        raise ValueError("gauge must be square")
    inverse = np.linalg.inv(matrix)
    return np.asarray(right_frame) @ matrix, np.asarray(left_frame) @ adjoint(inverse)
