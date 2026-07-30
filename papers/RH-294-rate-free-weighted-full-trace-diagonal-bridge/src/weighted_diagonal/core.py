from __future__ import annotations


def weighted_sum(level: int, radius: float = 1.4) -> float:
    if level < 2 or radius <= 1.0:
        raise ValueError("invalid diagonal level")
    return sum(radius**order / order for order in range(2, level + 1))


def level_tolerance(level: int, radius: float = 1.4) -> float:
    return 1.0 / (2.0 * level * weighted_sum(level, radius))


def certified_budget(level: int, radius: float = 1.4) -> float:
    return 2.0 * level_tolerance(level, radius) * weighted_sum(level, radius)
