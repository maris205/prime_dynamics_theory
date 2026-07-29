"""Mixed-integer optimization for bounded signed shell selectors."""

from __future__ import annotations

import numpy as np
from scipy.optimize import Bounds, LinearConstraint, milp


def solve_bounded_signed_integer(
    difference: np.ndarray,
    matrix: np.ndarray,
    orders: np.ndarray,
    cap: int = 1,
) -> dict[str, object]:
    target = np.asarray(difference, dtype=float).reshape(-1)
    shell_matrix = np.asarray(matrix, dtype=float)
    powers = np.asarray(orders, dtype=float).reshape(-1)
    bound = int(cap)
    if shell_matrix.ndim != 2 or shell_matrix.shape[0] != target.size or powers.size != target.size:
        raise ValueError("matrix rows, target, and orders must match")
    if np.any(powers <= 0.0) or bound < 1:
        raise ValueError("positive orders and a positive integer cap are required")
    order_count, shell_count = shell_matrix.shape
    objective = np.concatenate((np.zeros(shell_count), 1.0 / powers))
    constraints = np.vstack((
        np.hstack((shell_matrix, -np.eye(order_count))),
        np.hstack((-shell_matrix, -np.eye(order_count))),
    ))
    upper = np.concatenate((target, -target))
    lower_bounds = np.concatenate((-bound * np.ones(shell_count), np.zeros(order_count)))
    upper_bounds = np.concatenate((bound * np.ones(shell_count), np.full(order_count, np.inf)))
    result = milp(
        c=objective,
        integrality=np.concatenate((np.ones(shell_count), np.zeros(order_count))),
        bounds=Bounds(lower_bounds, upper_bounds),
        constraints=LinearConstraint(constraints, -np.inf, upper),
        options={"mip_rel_gap": 0.0},
    )
    if not result.success:
        raise RuntimeError(f"signed-integer MILP failed: {result.message}")
    return {
        "distance": float(result.fun),
        "weights": np.rint(result.x[:shell_count]).astype(int),
        "mip_gap": float(getattr(result, "mip_gap", 0.0) or 0.0),
        "mip_node_count": int(getattr(result, "mip_node_count", 0) or 0),
    }


def signed_lattice_size(shell_count: int, cap: int = 1) -> int:
    count = int(shell_count)
    bound = int(cap)
    if count < 0 or bound < 1:
        raise ValueError("nonnegative shell count and positive cap required")
    return int((2 * bound + 1) ** count)
