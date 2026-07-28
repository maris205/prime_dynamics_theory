"""Stability diagnostics for shell-complete spectral prefixes."""

from __future__ import annotations

import numpy as np
from scipy.optimize import linear_sum_assignment


def multiset_matching_error(first: np.ndarray, second: np.ndarray) -> float:
    left = np.asarray(first, dtype=complex).reshape(-1)
    right = np.asarray(second, dtype=complex).reshape(-1)
    if left.size != right.size:
        return float("inf")
    rows, columns = linear_sum_assignment(np.abs(left[:, None] - right[None, :]))
    return float(np.max(np.abs(left[rows] - right[columns]), initial=0.0))


def minimal_shell_completion_rank(shell_sizes: list[int], target_rank: int) -> int:
    target = int(target_rank)
    if target < 1:
        raise ValueError("target rank must be positive")
    total = 0
    for size in shell_sizes:
        if int(size) not in (1, 2):
            raise ValueError("real-operator shells have size one or two")
        total += int(size)
        if total >= target:
            return total
    raise ValueError("insufficient shells")


def shell_completion_is_minimal(shell_sizes: list[int], target_rank: int) -> bool:
    rank = minimal_shell_completion_rank(shell_sizes, target_rank)
    preceding = rank - int(shell_sizes[next(
        index
        for index in range(len(shell_sizes))
        if sum(shell_sizes[: index + 1]) == rank
    )])
    return preceding < int(target_rank) <= rank
