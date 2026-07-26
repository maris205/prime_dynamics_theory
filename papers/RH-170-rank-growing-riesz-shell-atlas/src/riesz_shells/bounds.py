"""Scalar ledger for shellwise cloud convergence."""

from __future__ import annotations

import math
from collections.abc import Iterable


def rank_change_norm_floor(source_rank: int, target_rank: int) -> float:
    source = int(source_rank)
    target = int(target_rank)
    if source < 0 or target < 0:
        raise ValueError("ranks must be nonnegative")
    return 0.0 if source == target else 1.0


def shell_tail_bound(step_bounds: Iterable[float], start: int = 0) -> dict[str, float | bool | int]:
    values = tuple(float(value) for value in step_bounds)
    index = int(start)
    if index < 0 or index > len(values):
        raise ValueError("invalid tail start")
    if not all(math.isfinite(value) and value >= 0.0 for value in values):
        raise ValueError("step bounds must be finite and nonnegative")
    return {
        "start": index,
        "tail_upper": sum(values[index:]),
        "all_step_transports_stable": all(value < 1.0 for value in values[index:]),
    }


def finite_partial_cloud(shell_ranks: Iterable[int]) -> dict[str, int]:
    ranks = tuple(int(value) for value in shell_ranks)
    if any(value < 0 for value in ranks):
        raise ValueError("shell ranks must be nonnegative")
    return {"shell_count": len(ranks), "partial_cloud_rank": sum(ranks)}
