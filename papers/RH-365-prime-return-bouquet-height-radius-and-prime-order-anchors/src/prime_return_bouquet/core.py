"""Exact integer and finite bouquet ledgers used by the RH-365 artifact.

The all-order midpoint, height, trace-envelope, normal-convergence, and
operator statements are proved in the manuscript.  This module reproduces
finite exact rows and exposes the formulas used by the tests.
"""

from __future__ import annotations

from functools import lru_cache
from math import ceil, gcd, log2, sqrt
from typing import Iterable


Point = tuple[int, int]
P0: Point = (0, 0)


def henon(point: Point) -> Point:
    x, y = point
    return 1 - 6 * x * x - y, x


def henon_inverse(point: Point) -> Point:
    u, v = point
    return v, 1 - 6 * v * v - u


def henon_mod(point: Point, modulus: int) -> Point:
    if modulus < 1:
        raise ValueError("modulus must be positive")
    x, y = point
    return ((1 - 6 * x * x - y) % modulus, x % modulus)


def orbit(point: Point, steps: int) -> list[Point]:
    if steps < 0:
        raise ValueError("steps must be nonnegative")
    rows = [point]
    for _ in range(steps):
        rows.append(henon(rows[-1]))
    return rows


def first_coordinates(maximum_index: int) -> list[int]:
    if maximum_index < 0:
        raise ValueError("maximum index must be nonnegative")
    return [row[0] for row in orbit(P0, maximum_index)]


def gcd_terms(maximum_order: int) -> list[int]:
    if maximum_order < 0:
        raise ValueError("maximum order must be nonnegative")
    rows = orbit(P0, maximum_order)
    return [gcd(abs(rows[n][0]), abs(rows[n][1])) for n in range(1, maximum_order + 1)]


def midpoint_value(order: int) -> int:
    if order < 1:
        raise ValueError("order must be positive")
    maximum = (order + 1) // 2
    values = {-1: 0}
    values.update(enumerate(first_coordinates(maximum)))
    if order % 2 == 0:
        k = order // 2
        return abs(values[k] - values[k - 1])
    k = (order - 1) // 2
    return abs(values[k + 1] - values[k - 1])


def height_value(index: int) -> int:
    if index < 2:
        raise ValueError("height index must be at least two")
    return -first_coordinates(index)[index]


def height_bounds(index: int) -> tuple[int, int]:
    if index < 2:
        raise ValueError("height index must be at least two")
    lower = 5 ** (2 ** (index - 1) - 1)
    upper = 30 ** (2 ** (index - 2)) // 6
    return lower, upper


def gcd_height_bounds(order: int) -> tuple[int, int]:
    if order < 3:
        raise ValueError("gcd height bound starts at order three")
    middle = ceil(order / 2)
    lower = 4 * 5 ** (2 ** (middle - 1) - 2)
    upper = 30 ** (2 ** (middle - 2)) // 5
    return lower, upper


@lru_cache(maxsize=None)
def distinct_prime_factors(value: int) -> tuple[int, ...]:
    if value < 1:
        raise ValueError("factor input must be positive")
    factors: list[int] = []
    divisor = 2
    remaining = value
    while divisor * divisor <= remaining:
        if remaining % divisor == 0:
            factors.append(divisor)
            while remaining % divisor == 0:
                remaining //= divisor
        divisor = 3 if divisor == 2 else divisor + 2
    if remaining > 1:
        factors.append(remaining)
    return tuple(factors)


def bounded_return_rank(prime: int, maximum_order: int) -> int:
    if prime < 2 or maximum_order < 1:
        raise ValueError("invalid prime or maximum order")
    current = P0
    for order in range(1, maximum_order + 1):
        current = henon_mod(current, prime)
        if current == P0:
            return order
    raise ValueError(f"no return through order {maximum_order} for modulus {prime}")


def finite_rank_table(maximum_order: int) -> dict[int, int]:
    terms = gcd_terms(maximum_order)
    primes = sorted(
        {
            prime
            for term in terms
            for prime in distinct_prime_factors(term)
        }
    )
    return {prime: bounded_return_rank(prime, maximum_order) for prime in primes}


def primitive_rank_counts(maximum_order: int) -> list[int]:
    ranks = finite_rank_table(maximum_order)
    return [sum(rank == order for rank in ranks.values()) for order in range(1, maximum_order + 1)]


def bouquet_traces(maximum_order: int) -> list[int]:
    ranks = finite_rank_table(maximum_order)
    return [
        sum(rank for rank in ranks.values() if order % rank == 0)
        for order in range(1, maximum_order + 1)
    ]


def trace_envelope(order: int) -> float:
    if order < 1:
        raise ValueError("order must be positive")
    return log2(30.0) * order * 2.0 ** (ceil(order / 2) - 2)


def logarithmic_majorant(radius: float) -> float:
    if not (0.0 <= radius < 1.0 / sqrt(2.0)):
        raise ValueError("radius lies outside the strict certified disk")
    return log2(30.0) * (radius**3 + radius**4) / (1.0 - 2.0 * radius**2)


def zeta_coefficients(maximum_order: int) -> list[int]:
    traces = [0] + bouquet_traces(maximum_order)
    coefficients = [1]
    for order in range(1, maximum_order + 1):
        numerator = sum(traces[k] * coefficients[order - k] for k in range(1, order + 1))
        if numerator % order:
            raise AssertionError("Artin--Mazur coefficient recurrence lost integrality")
        coefficients.append(numerator // order)
    return coefficients


def local_cycle_determinant(rank: int, z: complex) -> complex:
    if rank < 1:
        raise ValueError("rank must be positive")
    return 1 - z**rank


def naive_schatten_partial_sum(
    block_dimensions: Iterable[int], z_absolute: float, q: float
) -> float:
    if z_absolute < 0 or q <= 0:
        raise ValueError("invalid scalar or Schatten exponent")
    return sum(block_dimensions) * z_absolute**q


def certified_radius_bracket() -> dict[str, float]:
    return {
        "lower": 1.0 / sqrt(2.0),
        "upper": 1.0,
    }
