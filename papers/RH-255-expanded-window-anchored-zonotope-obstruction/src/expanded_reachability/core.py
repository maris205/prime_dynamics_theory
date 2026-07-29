"""Shell-jet helpers for expanded anchored reachability."""

from __future__ import annotations

import numpy as np


def shell_power_matrix(shells: list[np.ndarray], orders: np.ndarray) -> np.ndarray:
    powers = np.asarray(orders, dtype=int).reshape(-1)
    if powers.size == 0 or np.any(powers < 1):
        raise ValueError("positive orders are required")
    return np.column_stack([
        [np.sum(np.asarray(shell, dtype=complex) ** order) for order in powers]
        for shell in shells
    ])


def best_prefix_distance(
    difference: np.ndarray,
    matrix: np.ndarray,
    orders: np.ndarray,
    shell_sizes: np.ndarray,
    minimum_rank: int = 4,
) -> dict[str, float | int]:
    target = np.asarray(difference, dtype=float).reshape(-1)
    shell_matrix = np.asarray(matrix, dtype=float)
    powers = np.asarray(orders, dtype=float).reshape(-1)
    sizes = np.asarray(shell_sizes, dtype=int).reshape(-1)
    best: tuple[float, int, int] | None = None
    for stop in range(1, sizes.size + 1):
        rank = int(np.sum(sizes[:stop]))
        if rank < int(minimum_rank):
            continue
        residual = target - np.sum(shell_matrix[:, :stop], axis=1)
        distance = float(np.sum(np.abs(residual) / powers))
        candidate = (distance, rank, stop)
        if best is None or candidate < best:
            best = candidate
    if best is None:
        raise ValueError("no eligible prefix")
    return {"distance": best[0], "rank": best[1], "stop_shell": best[2]}


def single_coefficient_box_gap(difference: np.ndarray, matrix: np.ndarray, orders: np.ndarray) -> dict[str, float | int]:
    target = np.asarray(difference, dtype=float).reshape(-1)
    shell_matrix = np.asarray(matrix, dtype=float)
    powers = np.asarray(orders, dtype=float).reshape(-1)
    lower = np.sum(np.minimum(shell_matrix, 0.0), axis=1)
    upper = np.sum(np.maximum(shell_matrix, 0.0), axis=1)
    gaps = np.maximum(lower - target, 0.0) + np.maximum(target - upper, 0.0)
    weighted = gaps / powers
    index = int(np.argmax(weighted))
    return {"weighted_gap": float(weighted[index]), "order": int(powers[index])}
