"""Matrix models for the weighted unilateral history completion."""

from __future__ import annotations

import math

import numpy as np


def unilateral_shift_truncation(length: int, *, multiplicity: int = 1) -> np.ndarray:
    size = int(length)
    block = int(multiplicity)
    if size < 1 or block < 1:
        raise ValueError("length and multiplicity must be positive")
    shift = np.zeros((size * block, size * block))
    identity = np.eye(block)
    for index in range(size - 1):
        shift[(index + 1) * block:(index + 2) * block, index * block:(index + 1) * block] = identity
    return shift


def finite_history_completion(
    operator: np.ndarray,
    history_blocks: int,
    ratio: float,
    *,
    eta: float = 1.0 / 512.0,
) -> np.ndarray:
    """Return the square L-block truncation of the autonomous history map."""
    dynamics = np.asarray(operator)
    if dynamics.ndim != 2 or dynamics.shape[0] != dynamics.shape[1]:
        raise ValueError("operator must be square")
    blocks = int(history_blocks)
    if blocks < 1:
        raise ValueError("at least one history block is required")
    dimension = dynamics.shape[0]
    result = math.sqrt(float(eta)) * unilateral_shift_truncation(blocks, multiplicity=dimension)
    result[:dimension, :dimension] = float(ratio) * dynamics
    return result


def shift_resolvent_vector_lower_bound(length: int, weight: float, spectral_point: complex) -> float:
    """Exact norm of (zI-qS_L)^(-1)e_0 for a scalar shift truncation."""
    size = int(length)
    q = abs(float(weight))
    radius = abs(complex(spectral_point))
    if size < 1 or radius == 0.0:
        raise ValueError("length must be positive and spectral point nonzero")
    ratio = q / radius
    if ratio == 1.0:
        square_sum = float(size)
    else:
        square_sum = (ratio ** (2 * size) - 1.0) / (ratio * ratio - 1.0)
    return math.sqrt(square_sum) / radius
