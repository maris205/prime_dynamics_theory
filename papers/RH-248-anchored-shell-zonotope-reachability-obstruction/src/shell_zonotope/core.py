"""Linear and mixed-integer programs for real conjugate-shell jets."""

from __future__ import annotations

import numpy as np
from scipy.optimize import Bounds, LinearConstraint, linprog, milp


def weighted_distance(residual: np.ndarray, orders: np.ndarray) -> float:
    values = np.asarray(residual, dtype=float).reshape(-1)
    powers = np.asarray(orders, dtype=float).reshape(-1)
    if values.size != powers.size or np.any(powers <= 0.0):
        raise ValueError("residual and positive orders must have equal length")
    return float(np.sum(np.abs(values) / powers))


def _l1_problem(
    target_difference: np.ndarray,
    shell_vectors: np.ndarray,
    orders: np.ndarray,
) -> tuple[np.ndarray, np.ndarray, np.ndarray, int, int]:
    difference = np.asarray(target_difference, dtype=float).reshape(-1)
    matrix = np.asarray(shell_vectors, dtype=float)
    powers = np.asarray(orders, dtype=float).reshape(-1)
    if matrix.ndim != 2 or matrix.shape[0] != difference.size or powers.size != difference.size:
        raise ValueError("shell matrix rows must match the target jet")
    order_count, shell_count = matrix.shape
    objective = np.concatenate((np.zeros(shell_count), 1.0 / powers))
    constraints = np.vstack((
        np.hstack((matrix, -np.eye(order_count))),
        np.hstack((-matrix, -np.eye(order_count))),
    ))
    upper = np.concatenate((difference, -difference))
    return objective, constraints, upper, shell_count, order_count


def solve_box_zonotope(
    target_difference: np.ndarray,
    shell_vectors: np.ndarray,
    orders: np.ndarray,
) -> dict[str, object]:
    """Solve 0<=w<=1 and its explicit zonotope dual."""

    objective, constraints, upper, shell_count, order_count = _l1_problem(
        target_difference,
        shell_vectors,
        orders,
    )
    primal = linprog(
        objective,
        A_ub=constraints,
        b_ub=upper,
        bounds=[(0.0, 1.0)] * shell_count + [(0.0, None)] * order_count,
        method="highs",
    )
    if not primal.success:
        raise RuntimeError(f"box primal failed: {primal.message}")

    difference = np.asarray(target_difference, dtype=float).reshape(-1)
    matrix = np.asarray(shell_vectors, dtype=float)
    powers = np.asarray(orders, dtype=float).reshape(-1)
    dual_objective = np.concatenate((-difference, np.ones(shell_count)))
    dual_constraints = np.hstack((matrix.T, -np.eye(shell_count)))
    dual = linprog(
        dual_objective,
        A_ub=dual_constraints,
        b_ub=np.zeros(shell_count),
        bounds=[(-1.0 / power, 1.0 / power) for power in powers]
        + [(0.0, None)] * shell_count,
        method="highs",
    )
    if not dual.success:
        raise RuntimeError(f"box dual failed: {dual.message}")
    primal_value = float(primal.fun)
    dual_value = float(-dual.fun)
    return {
        "distance": primal_value,
        "weights": np.asarray(primal.x[:shell_count]),
        "dual_vector": np.asarray(dual.x[:order_count]),
        "dual_value": dual_value,
        "primal_dual_gap": float(primal_value - dual_value),
    }


def solve_binary_selection(
    target_difference: np.ndarray,
    shell_vectors: np.ndarray,
    orders: np.ndarray,
) -> dict[str, object]:
    """Solve the arbitrary shell-subset problem by exact-integrality MILP."""

    objective, constraints, upper, shell_count, order_count = _l1_problem(
        target_difference,
        shell_vectors,
        orders,
    )
    lower_bounds = np.zeros(shell_count + order_count)
    upper_bounds = np.concatenate((np.ones(shell_count), np.full(order_count, np.inf)))
    result = milp(
        c=objective,
        integrality=np.concatenate((np.ones(shell_count), np.zeros(order_count))),
        bounds=Bounds(lower_bounds, upper_bounds),
        constraints=LinearConstraint(constraints, -np.inf, upper),
        options={"mip_rel_gap": 0.0},
    )
    if not result.success:
        raise RuntimeError(f"binary MILP failed: {result.message}")
    return {
        "distance": float(result.fun),
        "weights": np.asarray(result.x[:shell_count]),
        "mip_gap": float(getattr(result, "mip_gap", 0.0) or 0.0),
    }


def binary_subset_count(shell_sizes: np.ndarray, minimum_rank: int = 0) -> int:
    """Count all shell subsets whose total algebraic rank meets a floor."""

    sizes = np.asarray(shell_sizes, dtype=int).reshape(-1)
    floor = int(minimum_rank)
    if np.any(sizes <= 0) or floor < 0:
        raise ValueError("shell sizes must be positive and rank floor nonnegative")
    counts = {0: 1}
    for size in sizes:
        updated = dict(counts)
        for rank, count in counts.items():
            updated[rank + int(size)] = updated.get(rank + int(size), 0) + count
        counts = updated
    return int(sum(count for rank, count in counts.items() if rank >= floor))
