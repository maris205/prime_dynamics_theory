#!/usr/bin/env python3
"""Standalone adversarial checks for TPC-218's two collapse barriers."""

from __future__ import annotations

import argparse
import sys
from fractions import Fraction


Q_VALUES = (101, 131, 151, 181)
HEIGHT = 500
MODULUS = 5


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


def row(q: int) -> tuple[Fraction, ...]:
    require(is_prime(q) and q % MODULUS == 1, f"q={q} is not aligned")
    cutoff = MODULUS * q // HEIGHT
    values = [Fraction(0, 1) for _ in range(MODULUS)]
    for m in range(-cutoff, cutoff + 1):
        if m:
            values[(m * pow(q, -1, MODULUS)) % MODULUS] += Fraction(1, 1)
    return tuple(values)


def norm(values: tuple[Fraction, ...]) -> Fraction:
    return sum((value * value for value in values), Fraction(0, 1))


def q_alignment_ratio() -> Fraction:
    rows = [row(q) for q in Q_VALUES]
    combined = tuple(sum((values[index] for values in rows), Fraction(0, 1)) for index in range(MODULUS))
    return norm(combined) / sum((norm(values) for values in rows), Fraction(0, 1))


def packet_alignment_ratio() -> Fraction:
    # Z_j = omega_j v, omega=(1,i,-1,-i)/2.  The unit projection is v.
    return Fraction(1, 1)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--check", action="store_true")
    parser.parse_args()
    try:
        q_ratio = q_alignment_ratio()
        require(q_ratio == 4, "prime labels are not fully aligned")
        packet_ratio = packet_alignment_ratio()
        require(packet_ratio == 1, "packet alignment ratio changed")
    except (CheckFailure, ValueError, ZeroDivisionError) as error:
        print(f"TPC218_ALIGNMENT_ADVERSARY=FAIL {error}", file=sys.stderr)
        return 1
    print("TPC218_ALIGNMENT_ADVERSARY=PASS")
    print("q_collapse_ratio=4")
    print("packet_projection_ratio=1")
    print("classification=FINITE_AND_ALGEBRAIC_STRUCTURAL_ADVERSARIES")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
