"""LPs for bounded and unbounded nonnegative shell weights."""

from __future__ import annotations

import numpy as np
from scipy.optimize import linprog


def _arrays(
    target_difference: np.ndarray,
    shell_vectors: np.ndarray,
    orders: np.ndarray,
) -> tuple[np.ndarray, np.ndarray, np.ndarray, int, int]:
    difference = np.asarray(target_difference, dtype=float).reshape(-1)
    matrix = np.asarray(shell_vectors, dtype=float)
    powers = np.asarray(orders, dtype=float).reshape(-1)
    if matrix.ndim != 2 or matrix.shape[0] != difference.size or powers.size != difference.size:
        raise ValueError("shell matrix rows must match the target jet")
    if np.any(powers <= 0.0):
        raise ValueError("orders must be positive")
    return difference, matrix, powers, matrix.shape[1], matrix.shape[0]


def _primal(
    target_difference: np.ndarray,
    shell_vectors: np.ndarray,
    orders: np.ndarray,
    upper_weight: float | None,
) -> dict[str, object]:
    difference, matrix, powers, shell_count, order_count = _arrays(
        target_difference,
        shell_vectors,
        orders,
    )
    objective = np.concatenate((np.zeros(shell_count), 1.0 / powers))
    constraints = np.vstack((
        np.hstack((matrix, -np.eye(order_count))),
        np.hstack((-matrix, -np.eye(order_count))),
    ))
    upper = np.concatenate((difference, -difference))
    weight_bound = (0.0, None) if upper_weight is None else (0.0, float(upper_weight))
    result = linprog(
        objective,
        A_ub=constraints,
        b_ub=upper,
        bounds=[weight_bound] * shell_count + [(0.0, None)] * order_count,
        method="highs",
    )
    if not result.success:
        raise RuntimeError(f"nonnegative primal failed: {result.message}")
    return {
        "distance": float(result.fun),
        "weights": np.asarray(result.x[:shell_count]),
    }


def solve_nonnegative_cone(
    target_difference: np.ndarray,
    shell_vectors: np.ndarray,
    orders: np.ndarray,
) -> dict[str, object]:
    """Solve w>=0 and the dual constrained by V^T y<=0."""

    primal = _primal(target_difference, shell_vectors, orders, None)
    difference, matrix, powers, _, _ = _arrays(
        target_difference,
        shell_vectors,
        orders,
    )
    dual = linprog(
        -difference,
        A_ub=matrix.T,
        b_ub=np.zeros(matrix.shape[1]),
        bounds=[(-1.0 / power, 1.0 / power) for power in powers],
        method="highs",
    )
    if not dual.success:
        raise RuntimeError(f"nonnegative dual failed: {dual.message}")
    dual_value = float(-dual.fun)
    primal["dual_value"] = dual_value
    primal["primal_dual_gap"] = float(primal["distance"] - dual_value)
    primal["dual_vector"] = np.asarray(dual.x)
    return primal


def solve_bounded_nonnegative(
    target_difference: np.ndarray,
    shell_vectors: np.ndarray,
    orders: np.ndarray,
    upper_weight: float,
) -> dict[str, object]:
    cap = float(upper_weight)
    if cap < 0.0:
        raise ValueError("upper_weight must be nonnegative")
    return _primal(target_difference, shell_vectors, orders, cap)


def minimum_weight_cap_for_tolerance(
    target_difference: np.ndarray,
    shell_vectors: np.ndarray,
    orders: np.ndarray,
    tolerance: float,
) -> dict[str, object]:
    """Minimize max_j w_j subject to weighted jet distance at most tolerance."""

    difference, matrix, powers, shell_count, order_count = _arrays(
        target_difference,
        shell_vectors,
        orders,
    )
    threshold = float(tolerance)
    if threshold < 0.0:
        raise ValueError("tolerance must be nonnegative")
    variable_count = shell_count + order_count + 1
    objective = np.zeros(variable_count)
    objective[-1] = 1.0
    residual_constraints = np.vstack((
        np.hstack((matrix, -np.eye(order_count), np.zeros((order_count, 1)))),
        np.hstack((-matrix, -np.eye(order_count), np.zeros((order_count, 1)))),
    ))
    residual_upper = np.concatenate((difference, -difference))
    distance_row = np.concatenate((np.zeros(shell_count), 1.0 / powers, [0.0]))
    cap_rows = np.hstack((np.eye(shell_count), np.zeros((shell_count, order_count)), -np.ones((shell_count, 1))))
    constraints = np.vstack((residual_constraints, distance_row, cap_rows))
    upper = np.concatenate((residual_upper, [threshold], np.zeros(shell_count)))
    result = linprog(
        objective,
        A_ub=constraints,
        b_ub=upper,
        bounds=[(0.0, None)] * variable_count,
        method="highs",
    )
    return {
        "feasible": bool(result.success),
        "minimum_cap": float(result.fun) if result.success else None,
        "weights": np.asarray(result.x[:shell_count]) if result.success else None,
        "message": str(result.message),
    }
