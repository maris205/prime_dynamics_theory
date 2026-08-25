#!/usr/bin/env python3
"""Deterministic exact-rational finite illustrations for the TPC-250 bound."""

from __future__ import annotations

import argparse
from fractions import Fraction


LABEL = "NUMERICAL_FINITE_ILLUSTRATION_ONLY"
FAMILY_COUNT = 128


def _unit_vector(parameter: Fraction) -> tuple[Fraction, Fraction]:
    denominator = 1 + parameter * parameter
    return ((1 - parameter * parameter) / denominator, 2 * parameter / denominator)


def _dot(left: tuple[Fraction, Fraction], right: tuple[Fraction, Fraction]) -> Fraction:
    return left[0] * right[0] + left[1] * right[1]


def _family(seed: int) -> tuple[list[tuple[Fraction, Fraction]], list[Fraction]]:
    size = 2 + seed % 5
    vectors: list[tuple[Fraction, Fraction]] = []
    weights: list[Fraction] = []
    for index in range(size):
        numerator = ((seed + 3) * (index + 2) % 17) - 8
        denominator = 1 + ((seed + 5 * index) % 7)
        vectors.append(_unit_vector(Fraction(numerator, denominator)))
        magnitude = Fraction(1 + ((seed + 1) * (index + 2) % 9), 1 + ((2 * seed + index) % 5))
        sign = -1 if (seed + index) % 3 == 0 else 1
        weights.append(sign * magnitude)
    return vectors, weights


def _check_family(seed: int) -> tuple[bool, bool]:
    vectors, weights = _family(seed)
    for vector in vectors:
        if _dot(vector, vector) != 1:
            raise ValueError(f"family {seed}: rational parametrization lost unit norm")
    active = [index for index, weight in enumerate(weights) if weight != 0]
    mu = Fraction(0)
    if len(active) >= 2:
        mu = max(abs(_dot(vectors[i], vectors[j])) for i in active for j in active if i != j)
    diagonal = sum(weight * weight for weight in weights)
    ell_one = sum(abs(weight) for weight in weights)
    off_mass = ell_one * ell_one - diagonal
    resultant = (
        sum((weight * vector[0] for vector, weight in zip(vectors, weights)), Fraction(0)),
        sum((weight * vector[1] for vector, weight in zip(vectors, weights)), Fraction(0)),
    )
    quadratic = _dot(resultant, resultant)
    lower = max(diagonal - mu * off_mass, Fraction(0))
    upper = diagonal + mu * off_mass
    if abs(quadratic - diagonal) > mu * off_mass:
        raise ValueError(f"family {seed}: absolute deviation bound failed")
    if quadratic < lower or quadratic > upper:
        raise ValueError(f"family {seed}: two-sided bound failed")
    if diagonal <= 0:
        raise ValueError(f"family {seed}: generated family unexpectedly has D=0")
    kappa = ell_one * ell_one / diagonal
    if kappa < 1 or kappa > len(active):
        raise ValueError(f"family {seed}: kappa range failed")
    certifies = mu * (kappa - 1) < 1
    if certifies and quadratic <= 0:
        raise ValueError(f"family {seed}: noncancellation certificate failed")
    return certifies, quadratic == 0


def _check_edge_cases() -> None:
    vectors = [_unit_vector(Fraction(0)), _unit_vector(Fraction(1, 2))]
    zero_weights = [Fraction(0), Fraction(0)]
    active = [index for index, weight in enumerate(zero_weights) if weight != 0]
    mu = Fraction(0) if len(active) <= 1 else max(
        abs(_dot(vectors[i], vectors[j])) for i in active for j in active if i != j
    )
    diagonal = sum(weight * weight for weight in zero_weights)
    if active or mu != 0 or diagonal != 0:
        raise ValueError("D=0 empty-pair edge case failed")
    singleton_weights = [Fraction(3, 7), Fraction(0)]
    singleton_active = [index for index, weight in enumerate(singleton_weights) if weight != 0]
    singleton_mu = Fraction(0) if len(singleton_active) <= 1 else max(
        abs(_dot(vectors[i], vectors[j])) for i in singleton_active for j in singleton_active if i != j
    )
    singleton_d = sum(weight * weight for weight in singleton_weights)
    singleton_l = sum(abs(weight) for weight in singleton_weights)
    if len(singleton_active) != 1 or singleton_mu != 0 or singleton_l * singleton_l / singleton_d != 1:
        raise ValueError("singleton active edge case failed")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()
    if not args.check:
        print("FAIL use --check for the deterministic release run")
        return 2
    try:
        _check_edge_cases()
        certified = 0
        cancellations = 0
        for seed in range(FAMILY_COUNT):
            does_certify, cancels = _check_family(seed)
            certified += int(does_certify)
            cancellations += int(cancels)
    except ValueError as error:
        print(f"FAIL {error}")
        return 1
    print(
        f"PASS {LABEL} exact_rational_unit_vector_families={FAMILY_COUNT} "
        f"noncancellation_certificates={certified} exact_cancellations={cancellations} edge_cases=2"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
