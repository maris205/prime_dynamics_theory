#!/usr/bin/env python3
"""Exact stress tests for TPC-249 contraction and triangle sharpness."""

from __future__ import annotations

import argparse
from fractions import Fraction
from itertools import product


class Failure(RuntimeError):
    pass


def need(condition: bool, message: str) -> None:
    if type(condition) is not bool or not condition:
        raise Failure(message)


def dot(a, b):
    return sum((x * y for x, y in zip(a, b)), Fraction(0))


def norm2(a):
    return dot(a, a)


def common_ray(vectors):
    active = [vector for vector in vectors if norm2(vector) != 0]
    if not active:
        return True
    anchor = active[0]
    for vector in active[1:]:
        need(len(vector) == 2, "two-dimensional stress")
        if anchor[0] * vector[1] - anchor[1] * vector[0] != 0:
            return False
        if dot(anchor, vector) < 0:
            return False
    return True


def check():
    families = [
        ([[1, 0], [0, 1]], [1, 1]),
        ([[1, 0], [1, 0]], [1, 1]),
        ([[3, 4], [0, 5]], [5, 5]),
        ([[3, 4], [-3, -4]], [5, 5]),
    ]
    cases = 0
    equalities = 0
    cancellations = 0
    for raw_probes, norms in families:
        probes = [[Fraction(value) for value in row] for row in raw_probes]
        for raw_weights in product(range(-2, 3), repeat=2):
            weights = [Fraction(value) for value in raw_weights]
            weighted = [[weight * value for value in probe]
                        for weight, probe in zip(weights, probes)]
            g = [sum((vector[j] for vector in weighted), Fraction(0)) for j in range(2)]
            tagged = sum((abs(weight) * norm
                          for weight, norm in zip(weights, norms)), Fraction(0))
            need(norm2(g) <= tagged * tagged, "triangle dominance")
            equality = norm2(g) == tagged * tagged
            need(equality == common_ray(weighted), "equality criterion")
            equalities += int(equality)
            cancellations += int(tagged > 0 and norm2(g) == 0)
            cases += 1
    need(cancellations > 0 and equalities > 0, "adversarial coverage")
    print("TPC249_WEIGHTED_CONTRACTION_STRESS=PASS")
    print("weighted_cases=" + str(cases))
    print("triangle_equalities=" + str(equalities))
    print("exact_cancellations=" + str(cancellations))


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()
    if not args.check:
        raise SystemExit("TPC249_WEIGHTED_CONTRACTION_STRESS=FAIL: use --check")
    try:
        check()
    except (Failure, TypeError, ValueError, ZeroDivisionError) as error:
        raise SystemExit("TPC249_WEIGHTED_CONTRACTION_STRESS=FAIL: " + str(error))


if __name__ == "__main__":
    main()
