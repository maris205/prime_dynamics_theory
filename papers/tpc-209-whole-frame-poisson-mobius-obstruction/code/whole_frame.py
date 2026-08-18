"""Exact finite objects for the TPC-209 whole-frame Poisson obstruction.

The module deliberately contains only finite linear algebra and finite
reindexing.  It does not claim an asymptotic estimate for the TPC packets.
"""

from __future__ import annotations

from fractions import Fraction
from math import gcd
from typing import Iterable


def units(q: int) -> tuple[int, ...]:
    return tuple(range(1, q))


def edges(q: int) -> tuple[tuple[int, int], ...]:
    vertex_count = q - 1
    return tuple(
        (left, right)
        for left in range(vertex_count)
        for right in range(left + 1, vertex_count)
    )


def projection(q: int) -> tuple[tuple[Fraction, ...], ...]:
    n = q - 1
    return tuple(
        tuple(Fraction(int(left == right), 1) - Fraction(1, n) for right in range(n))
        for left in range(n)
    )


def laplacian(q: int) -> tuple[tuple[int, ...], ...]:
    n = q - 1
    matrix = [[0 for _ in range(n)] for _ in range(n)]
    for left, right in edges(q):
        matrix[left][left] += 1
        matrix[right][right] += 1
        matrix[left][right] -= 1
        matrix[right][left] -= 1
    return tuple(tuple(row) for row in matrix)


def dilation_image(q: int, divisor: int) -> tuple[int, ...]:
    """Permutation image indices for (U_D b)(k)=b(kD)."""

    require(gcd(divisor, q) == 1, "dilation must be a unit")
    return tuple((k * divisor) % q - 1 for k in units(q))


def apply_dilation(vector: tuple[complex, ...], q: int, divisor: int) -> tuple[complex, ...]:
    image = dilation_image(q, divisor)
    return tuple(vector[index] for index in image)


def dual_index(q: int, divisor: int, frequency: int, poisson_index: int) -> int:
    require(1 <= frequency < q, "frequency must be nonzero")
    require(gcd(divisor, q) == 1, "dilation must be a unit")
    return q * poisson_index + frequency * divisor


def dual_inverse(q: int, divisor: int, dual: int) -> tuple[int, int]:
    require(dual % q != 0, "dual index must be nonzero modulo q")
    frequency = (dual * pow(divisor, -1, q)) % q
    require(frequency != 0, "inverse frequency must be nonzero")
    poisson_index = (dual - frequency * divisor) // q
    return frequency, poisson_index


def mobius(n: int) -> int:
    if n < 1:
        raise ValueError("mobius domain")
    value = n
    prime = 2
    parity = 0
    while prime * prime <= value:
        if value % prime == 0:
            value //= prime
            parity ^= 1
            if value % prime == 0:
                return 0
            while value % prime == 0:
                value //= prime
        prime += 1
    if value > 1:
        parity ^= 1
    return -1 if parity else 1


def nonzero_mobius_divisors(q: int) -> tuple[int, ...]:
    return tuple(divisor for divisor in range(2, q) if mobius(divisor) != 0)


def alignment_ratio(weights: Iterable[int]) -> Fraction:
    values = tuple(abs(value) for value in weights)
    denominator = sum(value * value for value in values)
    if denominator == 0:
        raise ValueError("zero weights")
    return Fraction(sum(values) ** 2, denominator)


def coherent_alignment(
    q: int, divisors: tuple[int, ...], weights: tuple[int, ...]
) -> tuple[tuple[Fraction, ...], tuple[Fraction, ...]]:
    """Return individual and aggregate squared coordinates for z=e1-e2.

    The vectors are normalized so that the direct-sum input energy is one.
    All values are exact rationals.
    """

    require(len(divisors) == len(weights) and len(divisors) > 0, "alignment shape")
    n = q - 1
    z = [Fraction(0) for _ in range(n)]
    z[0] = Fraction(1, 2)
    z[1] = Fraction(-1, 2)
    individual = [Fraction(0) for _ in range(n)]
    aggregate = [Fraction(0) for _ in range(n)]
    # Choose B_D=sign(weight) U_D^{-1}z.  The signs align all weighted
    # outputs, so this records the sharp coherent energy ratio.
    l1 = sum(abs(value) for value in weights)
    for weight in weights:
        for index, value in enumerate(z):
            individual[index] += value * value
    for index, value in enumerate(z):
        aggregate[index] = Fraction(l1) * value * Fraction(l1) * value
    return tuple(individual), tuple(aggregate)


def quadratic_character(q: int, value: int) -> int:
    require(value % q != 0, "quadratic character at zero")
    result = pow(value % q, (q - 1) // 2, q)
    return 1 if result == 1 else -1


def quadratic_multiplier(q: int, divisors: tuple[int, ...], weights: tuple[int, ...]) -> int:
    require(q % 2 == 1, "odd prime required")
    require(len(divisors) == len(weights), "multiplier shape")
    return sum(weight * quadratic_character(q, divisor) for divisor, weight in zip(divisors, weights))


def require(condition: bool, message: str) -> None:
    if type(condition) is not bool or not condition:
        raise ValueError(message)
