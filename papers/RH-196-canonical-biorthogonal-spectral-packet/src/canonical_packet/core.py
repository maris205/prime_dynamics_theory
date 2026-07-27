"""Balanced exact packets on source-observation spectral channel spaces."""

from __future__ import annotations

import numpy as np


def orthonormal_basis(synthesis: np.ndarray) -> np.ndarray:
    matrix = np.asarray(synthesis, dtype=complex)
    basis, triangular = np.linalg.qr(matrix, mode="reduced")
    singular = np.linalg.svd(triangular, compute_uv=False)
    tolerance = np.finfo(float).eps * max(matrix.shape) * float(singular[0])
    if float(singular[-1]) <= tolerance:
        raise ValueError("synthesis is rank deficient")
    return basis


def balanced_packet(right_synthesis: np.ndarray, left_synthesis: np.ndarray) -> dict[str, np.ndarray | float]:
    right_basis = orthonormal_basis(right_synthesis)
    left_basis = orthonormal_basis(left_synthesis)
    if right_basis.shape != left_basis.shape:
        raise ValueError("right and left spaces must have equal rank and ambient dimension")
    cross = left_basis.conj().T @ right_basis
    left_singular, singular, right_adjoint = np.linalg.svd(cross)
    if float(singular[-1]) <= np.finfo(float).eps * max(cross.shape) * float(singular[0]):
        raise ValueError("spectral channel spaces are not transverse")
    inverse_half = np.diag(1.0 / np.sqrt(singular))
    right_frame = right_basis @ right_adjoint.conj().T @ inverse_half
    left_frame = left_basis @ left_singular @ inverse_half
    return {
        "right_basis": right_basis,
        "left_basis": left_basis,
        "cross_gram": cross,
        "cross_singular_values": singular,
        "right_frame": right_frame,
        "left_frame": left_frame,
        "minimum_cross_singular_value": float(singular[-1]),
        "optimal_frame_norm": float(1.0 / np.sqrt(singular[-1])),
        "optimal_norm_product": float(1.0 / singular[-1]),
    }


def apply_left(operator: np.ndarray, frame: np.ndarray, state_shape: tuple[int, int], *, adjoint: bool = False) -> np.ndarray:
    dynamics = np.asarray(operator, dtype=complex)
    if adjoint:
        dynamics = dynamics.conj().T
    values = np.asarray(frame, dtype=complex)
    return np.column_stack([
        (dynamics @ values[:, index].reshape(state_shape)).reshape(-1)
        for index in range(values.shape[1])
    ])


def exact_packet_metrics(
    operator: np.ndarray,
    right_frame: np.ndarray,
    left_frame: np.ndarray,
    state_shape: tuple[int, int],
) -> dict[str, np.ndarray | float]:
    right = np.asarray(right_frame, dtype=complex)
    left = np.asarray(left_frame, dtype=complex)
    forward = apply_left(operator, right, state_shape)
    backward = apply_left(operator, left, state_shape, adjoint=True)
    compressed = left.conj().T @ forward
    right_residual = forward - right @ compressed
    left_residual = backward - left @ compressed.conj().T
    return {
        "compressed": compressed,
        "biorthogonality_defect": float(np.linalg.norm(left.conj().T @ right - np.eye(right.shape[1]), 2)),
        "right_residual_norm": float(np.linalg.norm(right_residual, 2)),
        "left_residual_norm": float(np.linalg.norm(left_residual, 2)),
    }


def determinant_trace_ledger(matrix: np.ndarray, maximum_power: int = 8) -> dict[str, object]:
    values = np.linalg.eigvals(np.asarray(matrix, dtype=complex))
    return {
        "eigenvalues": values,
        "determinant": complex(np.linalg.det(matrix)),
        "traces": np.asarray([np.trace(np.linalg.matrix_power(matrix, power)) for power in range(1, int(maximum_power) + 1)]),
        "modal_traces": np.asarray([np.sum(values**power) for power in range(1, int(maximum_power) + 1)]),
    }
