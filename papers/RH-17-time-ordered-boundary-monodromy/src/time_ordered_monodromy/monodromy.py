"""Weighted cyclic shifts, bipartite lifts, and geometric determinants."""

from __future__ import annotations

import numpy as np

from .dynamics import BoundaryCycle


def inverse_jacobian_weights(cycle: BoundaryCycle) -> np.ndarray:
    """Return ``1/|S'(x_j)|`` in forward cycle order."""

    return np.asarray(
        [float(1 / abs(value)) for value in cycle.two_step_derivatives],
        dtype=np.float64,
    )


def weighted_cycle_matrix(cycle: BoundaryCycle) -> np.ndarray:
    """Return the inverse-Jacobian weighted cyclic shift."""

    weights = inverse_jacobian_weights(cycle)
    dimension = weights.size
    matrix = np.zeros((dimension, dimension), dtype=np.float64)
    columns = np.arange(dimension)
    matrix[(columns + 1) % dimension, columns] = weights
    return matrix


def balancing_diagonal(cycle: BoundaryCycle) -> np.ndarray:
    """Return ``d`` such that ``D^-1 W D = rho C``.

    A scalar normalization centers the logarithmic range and leaves the
    condition number unchanged.
    """

    weights = inverse_jacobian_weights(cycle)
    rho = float(cycle.inverse_jacobian_radius)
    logarithms = np.zeros(weights.size, dtype=np.float64)
    for index in range(weights.size - 1):
        logarithms[index + 1] = (
            logarithms[index] + np.log(weights[index]) - np.log(rho)
        )
    logarithms -= 0.5 * (np.max(logarithms) + np.min(logarithms))
    return np.exp(logarithms)


def balancing_condition_number(cycle: BoundaryCycle) -> float:
    """Two-norm condition number of the canonical diagonal balance."""

    diagonal = balancing_diagonal(cycle)
    return float(np.max(diagonal) / np.min(diagonal))


def eigenvalue_condition_number(cycle: BoundaryCycle) -> float:
    """Common Euclidean condition number of every simple cycle eigenvalue."""

    diagonal = balancing_diagonal(cycle)
    return float(
        np.linalg.norm(diagonal)
        * np.linalg.norm(1.0 / diagonal)
        / diagonal.size
    )


def bipartite_lift(cycle: BoundaryCycle) -> np.ndarray:
    r"""Return ``[[0,I],[W,0]]``, whose square is ``diag(W,W)``."""

    weighted = weighted_cycle_matrix(cycle)
    dimension = weighted.shape[0]
    zero = np.zeros_like(weighted)
    identity = np.eye(dimension)
    return np.block([[zero, identity], [weighted, zero]])


def geometric_section(degree: int, value: complex | np.ndarray) -> np.ndarray:
    """Evaluate ``1+q+...+q^degree`` without dividing near ``q=1``."""

    degree = int(degree)
    if degree < 0:
        raise ValueError("degree must be nonnegative")
    values = np.asarray(value, dtype=np.complex128)
    result = np.zeros_like(values)
    term = np.ones_like(values)
    for _ in range(degree + 1):
        result += term
        term *= values
    return result


def edge_deflated_determinant(
    cycle: BoundaryCycle, z: complex | np.ndarray
) -> np.ndarray:
    r"""Return the exact edge-deflated bipartite cycle determinant."""

    rho = float(cycle.inverse_jacobian_radius)
    return geometric_section(cycle.component_period - 1, rho * np.asarray(z) ** 2)


def ideal_reciprocal_cloud(cycle: BoundaryCycle) -> np.ndarray:
    """Return the edge-deflated one-step reciprocal resonance cloud."""

    period = cycle.component_period
    if period == 1:
        return np.asarray([], dtype=np.complex128)
    radius = float(cycle.one_step_radius)
    angles = np.arange(1, period, dtype=np.float64) * np.pi / period
    positive = radius * np.exp(1j * angles)
    return np.concatenate((positive, np.conjugate(positive)))
