"""Exact algebra for phase-weighted critical branch returns."""

from __future__ import annotations

import numpy as np


def phase_weighted_return(
    left: np.ndarray,
    right: np.ndarray,
    phase: float | complex,
) -> np.ndarray:
    """Return ``R_- + exp(i*phase) R_+`` for a real phase angle."""

    first = np.asarray(left, dtype=np.complex128)
    second = np.asarray(right, dtype=np.complex128)
    if first.shape != second.shape:
        raise ValueError("left and right returns must have the same shape")
    weight = np.exp(1j * float(phase)) if np.isrealobj(phase) else complex(phase)
    return first + weight * second


def forced_relative_phase(
    left_amplitude: float,
    right_amplitude: float,
    target_modulus: float,
) -> float:
    r"""Return ``theta in [0,pi]`` with ``|a + exp(i theta)b| = target``."""

    left = float(left_amplitude)
    right = float(right_amplitude)
    target = float(target_modulus)
    if left <= 0.0 or right <= 0.0 or target < 0.0:
        raise ValueError("branch amplitudes must be positive and target nonnegative")
    cosine = (target * target - left * left - right * right) / (2.0 * left * right)
    if cosine < -1.0 - 1.0e-12 or cosine > 1.0 + 1.0e-12:
        raise ValueError("the target modulus violates the triangle inequalities")
    return float(np.arccos(np.clip(cosine, -1.0, 1.0)))


def rank_one_branch_matrix(
    entrance: np.ndarray,
    exit: np.ndarray,
    *,
    phase: float = 0.0,
) -> np.ndarray:
    r"""Return ``J_theta c e^*`` on the two-dimensional branch space."""

    column = np.asarray(entrance, dtype=np.complex128).reshape(-1)
    row = np.asarray(exit, dtype=np.complex128).reshape(-1)
    if column.shape != row.shape:
        raise ValueError("entrance and exit vectors must have the same length")
    if column.size != 2:
        raise ValueError("the critical branch space must have dimension two")
    weights = np.asarray((1.0, np.exp(1j * float(phase))))
    return np.diag(weights) @ np.outer(column, np.conjugate(row))


def bright_dark_transform(matrix: np.ndarray) -> np.ndarray:
    """Express a two-branch matrix in the symmetric/antisymmetric basis."""

    values = np.asarray(matrix, dtype=np.complex128)
    if values.shape != (2, 2):
        raise ValueError("bright/dark transform requires a 2x2 matrix")
    transform = np.asarray(((1.0, 1.0), (1.0, -1.0))) / np.sqrt(2.0)
    return transform.conj().T @ values @ transform
