"""Sharp normalized coefficient laws for the deterministic numerator."""

from __future__ import annotations


def odd_normalized_ratio(order: int, lam: float) -> float:
    n = int(order)
    if n < 3 or n % 2 == 0 or lam <= 1.0:
        raise ValueError("require odd order at least three and lambda > 1")
    return float(1.0 / (1.0 + lam ** (-n)))


def even_endpoint_normalized_ratio(iterate: int, lam: float) -> float:
    m = int(iterate)
    if m < 1 or lam <= 1.0:
        raise ValueError("require positive iterate and lambda > 1")
    x = lam ** (-m)
    return float((1.0 - 2.0 * x) / (1.0 - x * x))


def critical_harmonic_lower_bound(first_order: int, last_order: int, ratio_floor: float) -> float:
    start = int(first_order); stop = int(last_order); floor = float(ratio_floor)
    if start < 1 or stop < start or not 0.0 < floor <= 1.0:
        raise ValueError("invalid harmonic lower-bound inputs")
    return float(floor * sum(1.0 / order for order in range(start, stop + 1)))
