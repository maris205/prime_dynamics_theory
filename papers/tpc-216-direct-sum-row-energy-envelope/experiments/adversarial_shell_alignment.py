#!/usr/bin/env python3
"""Exact finite adversary for the false shell-orthogonality shortcut."""

from __future__ import annotations

import argparse
import sys
from fractions import Fraction


H = 500
D = 5


class CheckFailure(RuntimeError):
    pass


def require(condition: bool, message: str) -> None:
    if type(condition) is not bool or not condition:
        raise CheckFailure(message)


def is_prime(value: int) -> bool:
    if value < 2:
        return False
    divisor = 2
    while divisor * divisor <= value:
        if value % divisor == 0:
            return value == divisor
        divisor += 1
    return True


def psi(value: Fraction) -> Fraction:
    return Fraction(1, 1) / (1 + value * value) ** 2


def row(q: int) -> tuple[Fraction, ...]:
    require(is_prime(q) and q % D == 1, f"invalid q={q}")
    cutoff = D * q // H
    result = [Fraction(0, 1) for _ in range(D)]
    for m in range(-cutoff, cutoff + 1):
        if m:
            result[(m * pow(q, -1, D)) % D] += psi(Fraction(H * m, D * q))
    return tuple(result)


def norm(values: tuple[Fraction, ...]) -> Fraction:
    return sum((value * value for value in values), Fraction(0, 1))


def ratio(q_values: tuple[int, ...]) -> Fraction:
    rows = [row(q) for q in q_values]
    combined = tuple(sum((values[index] for values in rows), Fraction(0, 1)) for index in range(D))
    return norm(combined) / sum((norm(values) for values in rows), Fraction(0, 1))


def check_case(q_values: tuple[int, ...]) -> Fraction:
    rows = [row(q) for q in q_values]
    supports = [{index for index, value in enumerate(values) if value} for values in rows]
    require(all(item == {1, 4} for item in supports), "support is not aligned")
    value = ratio(q_values)
    require(value > 1, "cross energy is not positive")
    require(value < len(q_values), "Cauchy upper bound failed")
    return value


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--check", action="store_true")
    parser.parse_args()
    try:
        three = check_case((101, 131, 151))
        four = check_case((101, 131, 151, 181))
    except (CheckFailure, ValueError, ZeroDivisionError) as error:
        print(f"TPC216_ALIGNMENT_ADVERSARY=FAIL {error}", file=sys.stderr)
        return 1
    print("TPC216_ALIGNMENT_ADVERSARY=PASS")
    print("three_q_ratio=", three)
    print("four_q_ratio=", four)
    print("classification=FINITE_STRUCTURAL_ADVERSARY")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
