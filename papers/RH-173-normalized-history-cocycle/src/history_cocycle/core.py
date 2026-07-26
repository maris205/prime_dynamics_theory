"""Rectangular cocycle maps induced by normalized source histories."""

from __future__ import annotations

import math

import numpy as np


DEFAULT_ETA = 1.0 / 512.0


def _adjoint(matrix: np.ndarray) -> np.ndarray:
    return np.asarray(matrix).conj().T


def normalization_ratio(previous_state: np.ndarray, next_state: np.ndarray) -> float:
    previous = float(np.linalg.norm(previous_state, "fro"))
    following = float(np.linalg.norm(next_state, "fro"))
    if previous == 0.0 or following == 0.0:
        raise ValueError("normalization ratio requires nonzero states")
    return previous / following


def apply_history_cocycle(
    values: np.ndarray,
    operator: np.ndarray,
    ratio: float,
    *,
    eta: float = DEFAULT_ETA,
) -> np.ndarray:
    """Apply T_t(y_0,...,y_t)=(rAy_0,sqrt(eta)y_0,...)."""
    matrix = np.asarray(values)
    dynamics = np.asarray(operator)
    if dynamics.ndim != 2 or dynamics.shape[0] != dynamics.shape[1]:
        raise ValueError("operator must be square")
    dimension = dynamics.shape[0]
    if matrix.ndim != 2 or matrix.shape[0] % dimension:
        raise ValueError("values must be a vertical stack of history blocks")
    decay = math.sqrt(float(eta))
    blocks = [matrix[index * dimension:(index + 1) * dimension] for index in range(matrix.shape[0] // dimension)]
    return np.vstack([float(ratio) * dynamics @ blocks[0], *(decay * block for block in blocks)])


def apply_history_cocycle_adjoint(
    values: np.ndarray,
    operator: np.ndarray,
    ratio: float,
    *,
    eta: float = DEFAULT_ETA,
) -> np.ndarray:
    """Apply the adjoint T_t^* to a stack with t+2 blocks."""
    matrix = np.asarray(values)
    dynamics = np.asarray(operator)
    dimension = dynamics.shape[0]
    if matrix.ndim != 2 or matrix.shape[0] % dimension or matrix.shape[0] < 2 * dimension:
        raise ValueError("adjoint input must contain at least two history blocks")
    decay = math.sqrt(float(eta))
    blocks = [matrix[index * dimension:(index + 1) * dimension] for index in range(matrix.shape[0] // dimension)]
    first = float(ratio) * _adjoint(dynamics) @ blocks[0] + decay * blocks[1]
    return np.vstack([first, *(decay * block for block in blocks[2:])])


def history_cocycle_matrix(
    operator: np.ndarray,
    input_blocks: int,
    ratio: float,
    *,
    eta: float = DEFAULT_ETA,
) -> np.ndarray:
    dynamics = np.asarray(operator)
    dimension = dynamics.shape[0]
    blocks = int(input_blocks)
    if dynamics.ndim != 2 or dynamics.shape[1] != dimension or blocks < 1:
        raise ValueError("invalid operator or block count")
    result = np.zeros(((blocks + 1) * dimension, blocks * dimension), dtype=np.result_type(dynamics, float))
    result[:dimension, :dimension] = float(ratio) * dynamics
    decay = math.sqrt(float(eta))
    for index in range(blocks):
        result[(index + 1) * dimension:(index + 2) * dimension, index * dimension:(index + 1) * dimension] = decay * np.eye(dimension)
    return result


def cocycle_extreme_singular_values(
    operator: np.ndarray,
    input_blocks: int,
    ratio: float,
    *,
    eta: float = DEFAULT_ETA,
) -> tuple[float, float]:
    """Return the exact largest and smallest singular values of T_t."""
    dynamics = np.asarray(operator)
    singular = np.linalg.svd(dynamics, compute_uv=False)
    decay = float(eta)
    largest = math.sqrt(float(ratio) ** 2 * float(singular[0]) ** 2 + decay)
    first_minimum = math.sqrt(float(ratio) ** 2 * float(singular[-1]) ** 2 + decay)
    smallest = first_minimum if int(input_blocks) == 1 else math.sqrt(decay)
    return largest, smallest


def packet_residuals(
    old_frame: np.ndarray,
    new_frame: np.ndarray,
    operator: np.ndarray,
    ratio: float,
    *,
    eta: float = DEFAULT_ETA,
) -> dict[str, float | np.ndarray]:
    """Return primal and adjoint residuals for consecutive history packets."""
    old = np.asarray(old_frame)
    new = np.asarray(new_frame)
    transported = apply_history_cocycle(old, operator, ratio, eta=eta)
    reduced = _adjoint(new) @ transported
    primal = transported - new @ reduced
    pulled = apply_history_cocycle_adjoint(new, operator, ratio, eta=eta)
    adjoint = pulled - old @ (_adjoint(old) @ pulled)
    transported_norm = float(np.linalg.norm(transported, 2))
    pulled_norm = float(np.linalg.norm(pulled, 2))
    return {
        "transported": transported,
        "reduced": reduced,
        "primal": primal,
        "adjoint": adjoint,
        "primal_relative": float(np.linalg.norm(primal, 2)) / max(transported_norm, np.finfo(float).tiny),
        "adjoint_relative": float(np.linalg.norm(adjoint, 2)) / max(pulled_norm, np.finfo(float).tiny),
    }
