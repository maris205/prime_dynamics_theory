"""Exact arithmetic used by the RH-362 reproduction artifact.

The functions in this module check finite identities only.  The normal
convergence, zero-free half-plane, Schatten bounds, and nonpromotion theorem
are analytic statements proved in the manuscript.
"""

from __future__ import annotations

from math import gcd
from typing import Iterable


Point = tuple[int, int]
A0: Point = (0, 0)


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


def integer_orbit(point: Point, steps: int) -> list[Point]:
    if steps < 0:
        raise ValueError("steps must be nonnegative")
    orbit = [point]
    for _ in range(steps):
        orbit.append(henon(orbit[-1]))
    return orbit


def first_coordinates(point: Point, steps: int) -> list[int]:
    return [row[0] for row in integer_orbit(point, steps)]


def gcd_sequence(point: Point, maximum_index: int) -> list[int]:
    if maximum_index < 1:
        return []
    x0, y0 = point
    orbit = integer_orbit(point, maximum_index)
    return [
        gcd(abs(orbit[n][0] - x0), abs(orbit[n][1] - y0))
        for n in range(1, maximum_index + 1)
    ]


def modular_return_rank(point: Point, modulus: int) -> int:
    if modulus < 1:
        raise ValueError("modulus must be positive")
    if modulus == 1:
        return 1
    start = (point[0] % modulus, point[1] % modulus)
    current = start
    for rank in range(1, modulus * modulus + 1):
        current = henon_mod(current, modulus)
        if current == start:
            return rank
    raise AssertionError("the reduced polynomial automorphism must be a permutation")


def is_prime(value: int) -> bool:
    if value < 2:
        return False
    if value % 2 == 0:
        return value == 2
    divisor = 3
    while divisor * divisor <= value:
        if value % divisor == 0:
            return False
        divisor += 2
    return True


def primes_up_to(limit: int) -> list[int]:
    return [value for value in range(2, limit + 1) if is_prime(value)]


def distinct_prime_factors(value: int) -> list[int]:
    value = abs(value)
    if value == 0:
        raise ValueError("zero has every prime divisor")
    factors: list[int] = []
    divisor = 2
    while divisor * divisor <= value:
        if value % divisor == 0:
            factors.append(divisor)
            while value % divisor == 0:
                value //= divisor
        divisor = 3 if divisor == 2 else divisor + 2
    if value > 1:
        factors.append(value)
    return factors


def low_rank_prime_set(point: Point, threshold: int) -> list[int]:
    if threshold < 2:
        return []
    product = 1
    for term in gcd_sequence(point, threshold - 1):
        if term == 0:
            raise ValueError("the low-rank identity requires a nonperiodic prefix")
        product *= term
    return distinct_prime_factors(product)


def local_cycle_trace(rank: int, power: int) -> int:
    if rank < 1 or power < 1:
        raise ValueError("rank and power must be positive")
    return rank if power % rank == 0 else 0


def local_cycle_determinant(rank: int, z: complex) -> complex:
    if rank < 1:
        raise ValueError("rank must be positive")
    return 1 - z**rank


def factor_integer(value: int) -> dict[int, int]:
    if value < 1:
        raise ValueError("value must be positive")
    factors: dict[int, int] = {}
    divisor = 2
    while divisor * divisor <= value:
        while value % divisor == 0:
            factors[divisor] = factors.get(divisor, 0) + 1
            value //= divisor
        divisor = 3 if divisor == 2 else divisor + 2
    if value > 1:
        factors[value] = factors.get(value, 0) + 1
    return factors


def dirichlet_coefficient(value: int, ranks: dict[int, int]) -> int:
    """Return the finite local-product coefficient for a fully ranked integer."""
    factors = factor_integer(value)
    for prime, exponent in factors.items():
        if prime not in ranks:
            raise KeyError(f"missing return rank for prime {prime}")
        if exponent % ranks[prime] != 0:
            return 0
    return 1


def return_divisibility_holds(
    point: Point,
    primes: Iterable[int],
    maximum_index: int,
) -> bool:
    terms = gcd_sequence(point, maximum_index)
    for prime in primes:
        rank = modular_return_rank(point, prime)
        for index, term in enumerate(terms, start=1):
            if (term % prime == 0) != (index % rank == 0):
                return False
    return True
