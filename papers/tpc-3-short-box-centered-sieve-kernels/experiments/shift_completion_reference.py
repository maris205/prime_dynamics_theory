#!/usr/bin/env python3
"""Exact rational brute-force certificate for short-shift completion.

This module implements the finite inequality called Theorem 4.3 in the Paper
12 draft.  It is a regression oracle for the H/Q normalization and the stated
completion cost; it is not a proof of the theorem.
"""

from __future__ import annotations

import math
from dataclasses import dataclass
from fractions import Fraction
from typing import Any, Iterable, Sequence


Rational = int | Fraction
WeightedPoint = tuple[int, Rational]


def product(values: Iterable[int]) -> int:
    result = 1
    for value in values:
        result *= value
    return result


def is_prime(value: int) -> bool:
    if value < 2:
        return False
    for divisor in range(2, math.isqrt(value) + 1):
        if value % divisor == 0:
            return False
    return True


def fraction_text(value: Fraction) -> str:
    if value.denominator == 1:
        return str(value.numerator)
    return f"{value.numerator}/{value.denominator}"


def _as_fraction(value: Rational) -> Fraction:
    if isinstance(value, Fraction):
        return value
    if isinstance(value, int):
        return Fraction(value, 1)
    raise TypeError("the exact certificate accepts only int or Fraction weights")


def _validate_primes(primes: Sequence[int]) -> tuple[int, ...]:
    normalized = tuple(primes)
    if not normalized:
        raise ValueError("at least one prime is required")
    if len(set(normalized)) != len(normalized):
        raise ValueError("Q must be squarefree")
    if any(p <= 2 or not is_prime(p) for p in normalized):
        raise ValueError("Q must be a product of distinct odd primes")
    return normalized


def _validate_points(points: Sequence[WeightedPoint], name: str) -> tuple[tuple[int, Fraction], ...]:
    normalized = tuple((int(value), _as_fraction(weight)) for value, weight in points)
    if not normalized:
        raise ValueError(f"{name} must be nonempty")
    values = [value for value, _ in normalized]
    if len(set(values)) != len(values):
        raise ValueError(f"{name} must represent a finite set without duplicates")
    return normalized


def global_kappa(primes: Sequence[int]) -> Fraction:
    value = Fraction(1, 1)
    for p in primes:
        value *= Fraction(p - 2, p - 1)
    return value


def exact_shifted_bilinear_form(
    primes: Sequence[int],
    alpha: Sequence[WeightedPoint],
    beta: Sequence[WeightedPoint],
    ell: int,
) -> Fraction:
    """Compute B_{2 ell}(alpha,beta) exactly for one fully active shift."""

    primes = _validate_primes(primes)
    alpha = _validate_points(alpha, "alpha")
    beta = _validate_points(beta, "beta")
    modulus = product(primes)
    if math.gcd(ell, modulus) != 1:
        raise ValueError("ell must be a unit modulo Q")
    kappa = global_kappa(primes)

    total = Fraction(0, 1)
    for m, alpha_m in alpha:
        if math.gcd(m, modulus) != 1:
            continue
        for n, beta_n in beta:
            if math.gcd(n, modulus) != 1:
                continue
            allowed = all((m * n + 2 * ell) % p != 0 for p in primes)
            centered_kernel = Fraction(int(allowed), 1) / kappa - 1
            total += alpha_m * beta_n * centered_kernel
    return total


@dataclass(frozen=True)
class ShiftCompletionCertificate:
    primes: tuple[int, ...]
    alpha: tuple[tuple[int, Fraction], ...]
    beta: tuple[tuple[int, Fraction], ...]
    modulus: int
    kappa: Fraction
    ell_start: int
    shift_length: int
    normalization: Fraction
    alpha_l1: Fraction
    beta_l1: Fraction
    short_energy: Fraction
    complete_energy: Fraction
    scaled_complete_energy: Fraction
    discrepancy: Fraction
    completion_cost: Fraction
    theorem_bound: Fraction
    slack: Fraction

    @property
    def holds(self) -> bool:
        return self.discrepancy <= self.theorem_bound

    def as_dict(self) -> dict[str, Any]:
        return {
            "statement": (
                "Exact finite brute-force check of Theorem 4.3; this is a "
                "regression certificate, not a proof."
            ),
            "primes": list(self.primes),
            "alpha": [
                {"point": point, "weight_exact": fraction_text(weight)}
                for point, weight in self.alpha
            ],
            "beta": [
                {"point": point, "weight_exact": fraction_text(weight)}
                for point, weight in self.beta
            ],
            "Q": self.modulus,
            "kappa_exact": fraction_text(self.kappa),
            "ell_interval": [self.ell_start, self.ell_start + self.shift_length],
            "H": self.shift_length,
            "short_fully_active_shift_count": sum(
                1
                for ell in range(
                    self.ell_start, self.ell_start + self.shift_length
                )
                if math.gcd(ell, self.modulus) == 1
            ),
            "complete_fully_active_shift_count": sum(
                1 for ell in range(self.modulus) if math.gcd(ell, self.modulus) == 1
            ),
            "normalization_name": "H/Q",
            "normalization_exact": fraction_text(self.normalization),
            "L_alpha_exact": fraction_text(self.alpha_l1),
            "L_beta_exact": fraction_text(self.beta_l1),
            "short_energy_exact": fraction_text(self.short_energy),
            "complete_energy_exact": fraction_text(self.complete_energy),
            "H_over_Q_times_complete_energy_exact": fraction_text(
                self.scaled_complete_energy
            ),
            "absolute_discrepancy_exact": fraction_text(self.discrepancy),
            "E_Q_exact": fraction_text(self.completion_cost),
            "theorem_bound_exact": fraction_text(self.theorem_bound),
            "slack_exact": fraction_text(self.slack),
            "inequality_holds": self.holds,
        }


def short_shift_completion_certificate(
    primes: Sequence[int],
    alpha: Sequence[WeightedPoint],
    beta: Sequence[WeightedPoint],
    ell_start: int,
    shift_length: int,
) -> ShiftCompletionCertificate:
    """Brute-force both sides of the exact short-shift completion bound."""

    primes = _validate_primes(primes)
    alpha = _validate_points(alpha, "alpha")
    beta = _validate_points(beta, "beta")
    if shift_length < 1:
        raise ValueError("shift_length must be positive")

    modulus = product(primes)
    kappa = global_kappa(primes)
    short_energy = sum(
        (
            exact_shifted_bilinear_form(primes, alpha, beta, ell) ** 2
            for ell in range(ell_start, ell_start + shift_length)
            if math.gcd(ell, modulus) == 1
        ),
        Fraction(0, 1),
    )
    complete_energy = sum(
        (
            exact_shifted_bilinear_form(primes, alpha, beta, ell) ** 2
            for ell in range(modulus)
            if math.gcd(ell, modulus) == 1
        ),
        Fraction(0, 1),
    )
    normalization = Fraction(shift_length, modulus)
    scaled_complete = normalization * complete_energy
    discrepancy = abs(short_energy - scaled_complete)

    alpha_l1 = sum(
        (abs(weight) for value, weight in alpha if math.gcd(value, modulus) == 1),
        Fraction(0, 1),
    )
    beta_l1 = sum(
        (abs(weight) for value, weight in beta if math.gcd(value, modulus) == 1),
        Fraction(0, 1),
    )
    rank = len(primes)
    completion_cost = (
        Fraction(4**rank, 1) / (kappa**2)
        + Fraction(2 * 3**rank, 1) / kappa
        + Fraction(2**rank, 1)
    )
    theorem_bound = completion_cost * (alpha_l1 * beta_l1) ** 2
    slack = theorem_bound - discrepancy

    return ShiftCompletionCertificate(
        primes=primes,
        alpha=alpha,
        beta=beta,
        modulus=modulus,
        kappa=kappa,
        ell_start=ell_start,
        shift_length=shift_length,
        normalization=normalization,
        alpha_l1=alpha_l1,
        beta_l1=beta_l1,
        short_energy=short_energy,
        complete_energy=complete_energy,
        scaled_complete_energy=scaled_complete,
        discrepancy=discrepancy,
        completion_cost=completion_cost,
        theorem_bound=theorem_bound,
        slack=slack,
    )


DEFAULT_ALPHA: tuple[WeightedPoint, ...] = (
    (2, Fraction(1, 1)),
    (3, Fraction(7, 5)),  # excluded by (m,Q)=1
    (4, Fraction(-1, 2)),
    (7, Fraction(2, 3)),
    (10, Fraction(-9, 7)),  # excluded by (m,Q)=1
    (11, Fraction(-3, 4)),
)

DEFAULT_BETA: tuple[WeightedPoint, ...] = (
    (1, Fraction(1, 3)),
    (5, Fraction(11, 6)),  # excluded by (n,Q)=1
    (8, Fraction(-2, 1)),
    (9, Fraction(5, 4)),
    (14, Fraction(1, 2)),
    (15, Fraction(-13, 8)),  # excluded by (n,Q)=1
)


def default_theorem_4_3_certificate() -> ShiftCompletionCertificate:
    return short_shift_completion_certificate(
        primes=(3, 5),
        alpha=DEFAULT_ALPHA,
        beta=DEFAULT_BETA,
        ell_start=7,
        shift_length=23,
    )
