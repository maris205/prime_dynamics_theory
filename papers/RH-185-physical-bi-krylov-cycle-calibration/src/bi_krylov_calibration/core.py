"""Bi-Krylov temporal windows and their two directed Ritz residuals."""

from __future__ import annotations

import cmath
import itertools
import math

import numpy as np


def adjoint(matrix: np.ndarray) -> np.ndarray:
    return np.asarray(matrix).conj().T


def column_operator_norm(matrix: np.ndarray) -> float:
    gram = adjoint(matrix) @ np.asarray(matrix)
    return math.sqrt(max(0.0, float(np.linalg.eigvalsh((gram + adjoint(gram)) / 2.0)[-1])))


def apply_left(operator: np.ndarray, columns: np.ndarray, shape: tuple[int, int], *, dual: bool = False) -> np.ndarray:
    dynamics = adjoint(operator) if dual else np.asarray(operator)
    values = np.asarray(columns)
    return np.column_stack(
        [(dynamics @ values[:, index].reshape(shape)).reshape(-1) for index in range(values.shape[1])]
    )


def phase_grid_error(eigenvalues: np.ndarray, wrap_phase: complex) -> float:
    values = np.asarray(eigenvalues)
    size = values.size
    offset = cmath.phase(complex(wrap_phase)) / size
    expected = [offset + 2.0 * math.pi * index / size for index in range(size)]
    observed = [cmath.phase(complex(value)) for value in values]

    def distance(left: float, right: float) -> float:
        difference = abs(left - right) % (2.0 * math.pi)
        return min(difference, 2.0 * math.pi - difference)

    return min(
        math.sqrt(sum(distance(left, right) ** 2 for left, right in zip(permutation, expected)) / size)
        for permutation in itertools.permutations(observed)
    )


def bi_krylov_window_metrics(
    operator: np.ndarray,
    right_synthesis: np.ndarray,
    left_synthesis: np.ndarray,
    state_shape: tuple[int, int],
    *,
    target_radius: float,
    wrap_phase: complex,
    balanced_builder,
) -> dict[str, float | list[float]]:
    data = balanced_builder(right_synthesis, left_synthesis)
    right = np.asarray(data["right_frame"])
    left = np.asarray(data["left_frame"])
    forward = apply_left(operator, right, state_shape)
    backward = apply_left(operator, left, state_shape, dual=True)
    compressed = adjoint(left) @ forward
    right_residual = forward - right @ compressed
    left_residual = backward - left @ adjoint(compressed)
    right_norm = column_operator_norm(right_residual)
    left_norm = column_operator_norm(left_residual)
    forward_norm = column_operator_norm(forward)
    backward_norm = column_operator_norm(backward)
    eigenvalues = np.linalg.eigvals(compressed)
    radius = float(target_radius)
    radial_error = math.sqrt(sum((abs(value) - radius) ** 2 for value in eigenvalues) / eigenvalues.size)
    minimum_cross = float(data["minimum_cross_singular_value"])
    return {
        "minimum_cross_singular_value": minimum_cross,
        "oblique_condition_number": 1.0 / minimum_cross,
        "right_frame_norm": column_operator_norm(right),
        "left_frame_norm": column_operator_norm(left),
        "biorthogonality_defect": column_operator_norm(adjoint(left) @ right - np.eye(right.shape[1])),
        "right_residual_norm": right_norm,
        "left_residual_norm": left_norm,
        "right_relative_residual": right_norm / max(forward_norm, np.finfo(float).tiny),
        "left_relative_residual": left_norm / max(backward_norm, np.finfo(float).tiny),
        "forward_norm": forward_norm,
        "backward_norm": backward_norm,
        "compressed_spectral_radius": float(max(abs(eigenvalues))),
        "compressed_cycle_radial_rms_error": float(radial_error),
        "compressed_cycle_phase_rms_error": float(phase_grid_error(eigenvalues, wrap_phase)),
        "compressed_eigenvalues_real": [float(value.real) for value in eigenvalues],
        "compressed_eigenvalues_imag": [float(value.imag) for value in eigenvalues],
    }
