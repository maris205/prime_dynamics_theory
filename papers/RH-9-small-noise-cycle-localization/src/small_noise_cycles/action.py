"""Closed-path action, its Jacobian, and numerical boundary-gap audits."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable

import numpy as np
from scipy.optimize import minimize


def _arrays(points: Iterable[float], parameters: Iterable[float]) -> tuple[np.ndarray, np.ndarray]:
    point_array = np.asarray(tuple(points), dtype=np.float64)
    parameter_array = np.asarray(tuple(parameters), dtype=np.float64)
    if point_array.ndim != 1 or point_array.size == 0:
        raise ValueError("points must be a nonempty vector")
    if point_array.shape != parameter_array.shape:
        raise ValueError("points and parameters must have the same length")
    return point_array, parameter_array


def cycle_residual(points: Iterable[float], parameters: Iterable[float]) -> np.ndarray:
    """Return ``x_(j+1)-f_uj(x_j)`` with cyclic indexing."""

    point_array, parameter_array = _arrays(points, parameters)
    return np.roll(point_array, -1) - (1.0 - parameter_array * point_array * point_array)


def cycle_action(points: Iterable[float], parameters: Iterable[float]) -> float:
    """Return one half of the squared closed-path residual."""

    residual = cycle_residual(points, parameters)
    return float(0.5 * np.dot(residual, residual))


def cycle_action_gradient(points: Iterable[float], parameters: Iterable[float]) -> np.ndarray:
    point_array, parameter_array = _arrays(points, parameters)
    residual = cycle_residual(point_array, parameter_array)
    return 2.0 * parameter_array * point_array * residual + np.roll(residual, 1)


def residual_jacobian(points: Iterable[float], parameters: Iterable[float]) -> np.ndarray:
    """Jacobian of the cyclic residual map."""

    point_array, parameter_array = _arrays(points, parameters)
    size = point_array.size
    jacobian = np.zeros((size, size), dtype=np.float64)
    indices = np.arange(size)
    jacobian[indices, indices] += 2.0 * parameter_array * point_array
    jacobian[indices, (indices + 1) % size] += 1.0
    return jacobian


@dataclass(frozen=True)
class BoundaryMinimum:
    action: float
    points: tuple[float, ...]
    active_coordinates: int
    success: bool


def estimate_boundary_minima(
    parameters: Iterable[float],
    *,
    starts: int = 500,
    seed: int = 1729,
    zero_tolerance: float = 1.0e-10,
    distinct_tolerance: float = 1.0e-8,
) -> list[BoundaryMinimum]:
    """Numerically catalogue positive-action constrained minima on ``[-1,1]^m``.

    This is an audit, not a certification routine.  Zero-action deterministic
    cycles are discarded.  Positive minima often lie on the boundary and set
    the visible preasymptotic exponential scale.
    """

    values = tuple(float(value) for value in parameters)
    if not values:
        raise ValueError("at least one parameter is required")
    if starts < 1:
        raise ValueError("starts must be positive")
    rng = np.random.default_rng(seed)
    initial = rng.uniform(-1.0, 1.0, size=(int(starts), len(values)))
    candidates: list[BoundaryMinimum] = []
    for point in initial:
        result = minimize(
            cycle_action,
            point,
            args=(values,),
            jac=cycle_action_gradient,
            bounds=[(-1.0, 1.0)] * len(values),
            method="L-BFGS-B",
            options={"ftol": 1.0e-15, "gtol": 1.0e-10, "maxiter": 1000},
        )
        action = float(result.fun)
        if not result.success or action <= zero_tolerance:
            continue
        active = int(np.count_nonzero(np.abs(np.abs(result.x) - 1.0) < 2.0e-7))
        candidates.append(
            BoundaryMinimum(
                action=action,
                points=tuple(float(value) for value in result.x),
                active_coordinates=active,
                success=bool(result.success),
            )
        )
    candidates.sort(key=lambda record: record.action)
    distinct: list[BoundaryMinimum] = []
    for record in candidates:
        if not distinct or abs(record.action - distinct[-1].action) > distinct_tolerance:
            distinct.append(record)
    return distinct
