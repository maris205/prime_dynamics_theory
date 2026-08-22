#!/usr/bin/env python3
"""Adversarial finite check: a short window does not orthogonalize two rows."""

from __future__ import annotations

import argparse
import sys
from fractions import Fraction
from math import gcd


Q_VALUES = (101, 131, 151, 181)
HEIGHT = 500
MODULUS = 5


class CheckFailure(RuntimeError):
    pass


def require(condition: bool, message: str) -> None:
    if type(condition) is not bool or not condition:
        raise CheckFailure(message)


def psi(argument: Fraction) -> Fraction:
    return Fraction(1, 1) / (1 + argument * argument) ** 2


def row() -> tuple[Fraction, ...]:
    result = [Fraction(0, 1) for _ in range(MODULUS)]
    for q in Q_VALUES:
        require(q % MODULUS == 1 and gcd(q, MODULUS) == 1, "aligned congruence")
        cutoff = MODULUS * q // HEIGHT
        for m in range(-cutoff, cutoff + 1):
            if m:
                result[(m * pow(q, -1, MODULUS)) % MODULUS] += psi(
                    Fraction(HEIGHT * m, MODULUS * q)
                )
    return tuple(result)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--check", action="store_true")
    parser.parse_args()
    try:
        values = row()
        support = [index for index, value in enumerate(values) if value]
        require(support == [1, 4], "support")
        diagonal = sum((values[index] * values[index] for index in support), Fraction(0, 1))
        one_point = sum(values[index] for index in support) ** 2
        require(one_point == 2 * diagonal, "short-window coherent ratio")
    except (CheckFailure, ValueError, ZeroDivisionError) as error:
        print(f"TPC217_FREQUENCY_CROWDING=FAIL {error}", file=sys.stderr)
        return 1
    print("TPC217_FREQUENCY_CROWDING=PASS")
    print("support=", support)
    print("window_length=1")
    print("window_to_diagonal_ratio=2")
    print("classification=FINITE_STRUCTURAL_ADVERSARY")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
