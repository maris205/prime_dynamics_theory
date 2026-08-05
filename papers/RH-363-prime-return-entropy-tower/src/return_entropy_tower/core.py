"""Exact finite checks for the RH-363 return-power entropy tower.

The all-prime entropy, moment-recovery, and local-uniform convergence
statements are proved in the manuscript.  This module reproduces finite
return ranks, gcd-stratified fixed-point counts, first zeta defects, and
high-precision truncations of the multiples-Mobius identity.
"""

from __future__ import annotations

from collections import defaultdict
from decimal import Decimal, localcontext
from fractions import Fraction
from math import comb, gcd, prod
from typing import Iterable


Point = tuple[int, int]
A0: Point = (0, 0)


def henon_mod(point: Point, modulus: int) -> Point:
    if modulus < 1:
        raise ValueError("modulus must be positive")
    x, y = point
    return ((1 - 6 * x * x - y) % modulus, x % modulus)


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
    raise AssertionError("the reduced Henon map is a permutation")


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


def return_rank_table(point: Point, primes: Iterable[int]) -> dict[int, int]:
    return {prime: modular_return_rank(point, prime) for prime in primes}


def return_power_moduli(ranks: dict[int, int], m: int) -> tuple[int, ...]:
    if m < 1:
        raise ValueError("tower level must be positive")
    if any(not is_prime(prime) or rank < 1 for prime, rank in ranks.items()):
        raise ValueError("invalid prime/rank table")
    return tuple(prime ** (m * ranks[prime]) for prime in sorted(ranks))


def pairwise_coprime(values: Iterable[int]) -> bool:
    rows = tuple(values)
    return all(
        gcd(left, right) == 1
        for index, left in enumerate(rows)
        for right in rows[index + 1 :]
    )


def coprime_moduli_polynomial(moduli: tuple[int, ...]) -> dict[int, int]:
    """Return coefficients of the source inclusion--exclusion polynomial."""
    if not moduli or any(modulus < 2 for modulus in moduli):
        raise ValueError("moduli must be a nonempty tuple with entries >= 2")
    if not pairwise_coprime(moduli):
        raise ValueError("moduli must be pairwise coprime")

    terms: dict[int, int] = {1: 1}
    for modulus in moduli:
        updated: defaultdict[int, int] = defaultdict(int)
        for old_degree, old_coefficient in terms.items():
            for missing_count in range(1, modulus + 1):
                degree = old_degree * (modulus - missing_count)
                coefficient = (
                    old_coefficient
                    * (-1) ** (missing_count + 1)
                    * comb(modulus, missing_count)
                )
                updated[degree] += coefficient
        terms = dict(updated)
    return dict(sorted(terms.items()))


def evaluate_polynomial(coefficients: dict[int, int], value: int) -> int:
    return sum(coefficient * value**degree for degree, coefficient in coefficients.items())


def fixed_point_count(moduli: tuple[int, ...], period: int) -> int:
    """Exact count for a finite pairwise-coprime B-admissible shift."""
    if period < 1:
        raise ValueError("period must be positive")
    if not moduli or not pairwise_coprime(moduli):
        raise ValueError("moduli must be nonempty and pairwise coprime")
    reduced = tuple(gcd(period, modulus) for modulus in moduli)
    if any(value == 1 for value in reduced):
        return 1
    combined = prod(reduced)
    if period % combined:
        raise AssertionError("pairwise-coprime reduced moduli must divide the period")
    return evaluate_polynomial(
        coprime_moduli_polynomial(reduced),
        2 ** (period // combined),
    )


def primorial(primes: Iterable[int]) -> int:
    rows = tuple(primes)
    if not rows:
        raise ValueError("at least one prime is required")
    return prod(rows)


def normalized_entropy_fraction(moduli: Iterable[int]) -> Fraction:
    density = Fraction(1, 1)
    for modulus in moduli:
        if modulus < 2:
            raise ValueError("moduli must be at least two")
        density *= Fraction(modulus - 1, modulus)
    return density


def zeta_coefficients(moduli: tuple[int, ...], order: int) -> list[int]:
    """Expand exp(sum N_n z^n/n) through the requested order exactly."""
    if order < 0:
        raise ValueError("order must be nonnegative")
    coefficients = [1]
    for n in range(1, order + 1):
        numerator = sum(
            fixed_point_count(moduli, k) * coefficients[n - k]
            for k in range(1, n + 1)
        )
        if numerator % n:
            raise AssertionError("Artin--Mazur recurrence lost integrality")
        coefficients.append(numerator // n)
    return coefficients


def universal_first_defect(ranks: dict[int, int], m: int) -> dict[str, int]:
    primes = tuple(sorted(ranks))
    moduli = return_power_moduli(ranks, m)
    wheel = primorial(primes)
    if any(fixed_point_count(moduli, n) != 1 for n in range(1, wheel)):
        raise AssertionError("a defect occurred before the primorial")
    count = fixed_point_count(moduli, wheel)
    universal_count = evaluate_polynomial(
        coprime_moduli_polynomial(primes), 2
    )
    if count != universal_count or count <= 1:
        raise AssertionError("the first defect is not the reduced prime wheel")
    if (count - 1) % wheel:
        raise AssertionError("nonzero first-defect points must form full cycles")
    coefficients = zeta_coefficients(moduli, wheel)
    if coefficients[:wheel] != [1] * wheel:
        raise AssertionError("zeta coefficients changed before the primorial")
    coefficient_defect = (count - 1) // wheel
    if coefficients[wheel] != 1 + coefficient_defect:
        raise AssertionError("first zeta coefficient defect is inconsistent")
    return {
        "prime_count": len(primes),
        "primorial_period": wheel,
        "fixed_point_count_at_first_defect": count,
        "primitive_orbit_defect": coefficient_defect,
        "zeta_coefficient_at_first_defect": coefficients[wheel],
    }


def mobius(value: int) -> int:
    if value < 1:
        raise ValueError("Mobius input must be positive")
    remaining = value
    prime_count = 0
    divisor = 2
    while divisor * divisor <= remaining:
        if remaining % divisor == 0:
            remaining //= divisor
            prime_count += 1
            if remaining % divisor == 0:
                return 0
            while remaining % divisor == 0:
                remaining //= divisor
        divisor += 1
    if remaining > 1:
        prime_count += 1
    return -1 if prime_count % 2 else 1


def finite_entropy_density_decimal(
    ranks: dict[int, int], m: int, precision: int = 80
) -> Decimal:
    if m < 1:
        raise ValueError("tower level must be positive")
    with localcontext() as context:
        context.prec = precision
        density = Decimal(1)
        for prime, rank in sorted(ranks.items()):
            q_power = Decimal(1) / Decimal(prime ** (m * rank))
            density *= Decimal(1) - q_power
        return +density


def finite_moment_decimal(
    ranks: dict[int, int], m: int, precision: int = 80
) -> Decimal:
    if m < 1:
        raise ValueError("moment order must be positive")
    with localcontext() as context:
        context.prec = precision
        return +sum(
            (
                (Decimal(1) / Decimal(prime**rank)) ** m
                for prime, rank in sorted(ranks.items())
            ),
            Decimal(0),
        )


def truncated_multiples_mobius_recovery(
    ranks: dict[int, int],
    m: int,
    maximum_multiplier: int,
    precision: int = 80,
) -> dict[str, Decimal]:
    """Numerically truncate M_m=sum_j mu(j) Lambda_{mj}/j.

    Here Lambda_n=-log(prod_p(1-p^{-n r_p})) for the finite prime table.
    The manuscript proves the absolutely convergent infinite-prime identity.
    """
    if maximum_multiplier < 1:
        raise ValueError("maximum multiplier must be positive")
    with localcontext() as context:
        context.prec = precision
        recovered = Decimal(0)
        for multiplier in range(1, maximum_multiplier + 1):
            mu = mobius(multiplier)
            if not mu:
                continue
            density = finite_entropy_density_decimal(
                ranks, m * multiplier, precision=precision
            )
            lambert_value = -density.ln()
            recovered += Decimal(mu) * lambert_value / Decimal(multiplier)
        target = finite_moment_decimal(ranks, m, precision=precision)
        return {
            "target_moment": +target,
            "recovered_truncation": +recovered,
            "absolute_error": +abs(target - recovered),
        }
