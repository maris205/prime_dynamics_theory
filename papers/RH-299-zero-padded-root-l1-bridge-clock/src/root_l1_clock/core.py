from __future__ import annotations

import itertools
import math


def _padded(values: list[complex], size: int) -> list[complex]:
    return list(values) + [0j] * (size - len(values))


def padded_l1_cost(left: list[complex], right: list[complex]) -> float:
    size = max(len(left), len(right))
    if size > 8:
        raise ValueError("exact permutation helper is limited to size eight")
    x = _padded(left, size)
    y = _padded(right, size)
    return min(
        sum(abs(a - y[index]) for a, index in zip(x, permutation))
        for permutation in itertools.permutations(range(size))
    )


def moment_error(left: list[complex], right: list[complex], order: int) -> float:
    if order < 1:
        raise ValueError("order must be positive")
    return abs(sum(value**order for value in left) - sum(value**order for value in right))


def transport_bound(
    cost: float,
    cap: float,
    radius: float,
    order_cut: int,
) -> float:
    if cost < 0.0 or cap <= 0.0 or radius <= 0.0 or order_cut < 3:
        raise ValueError("invalid transport parameters")
    return cost * radius * sum(
        (cap * radius) ** index for index in range(1, order_cut - 1)
    )


def critical_exponent(slope: float, cap: float, radius: float = 1.4) -> float:
    if slope <= 0.0 or cap * radius <= 1.0:
        raise ValueError("require a superunit weighted cap")
    return slope * math.log(cap * radius)


def radial_pair_budget(
    sigma: float,
    gamma: float,
    slope: float,
    cap: float,
    radius: float = 1.4,
) -> float:
    if not 0.0 < sigma < 1.0 or gamma <= 0.0:
        raise ValueError("invalid radial-pair parameters")
    cut = max(3, math.ceil(slope * math.log(1.0 / sigma)))
    shifted = cap - sigma**gamma
    if shifted < 0.0:
        raise ValueError("radial perturbation exceeds cap")
    return sum(
        abs(cap**order - shifted**order) * radius**order / order
        for order in range(2, cut)
    )
