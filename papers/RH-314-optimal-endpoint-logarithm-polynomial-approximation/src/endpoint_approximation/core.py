from __future__ import annotations

import math


def logarithmic_tail_energy(degree: int) -> float:
    n = int(degree)
    if n < 1:
        raise ValueError("degree must be positive")
    return math.pi * math.pi / 6.0 - math.fsum(1.0 / (order * order) for order in range(1, n + 1))


def best_log_error(degree: int) -> float:
    return math.sqrt(max(0.0, logarithmic_tail_energy(degree)))


def tail_energy_bounds(degree: int) -> tuple[float, float]:
    n = int(degree)
    if n < 1:
        raise ValueError("degree must be positive")
    return 1.0 / (n + 1.0), 1.0 / n
