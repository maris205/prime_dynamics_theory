"""Independent exact sanity check for the four-packet polarization identity."""

from __future__ import annotations

import argparse
from fractions import Fraction


Gaussian = tuple[Fraction, Fraction]


def add(left: Gaussian, right: Gaussian) -> Gaussian:
    return left[0] + right[0], left[1] + right[1]


def mul(left: Gaussian, right: Gaussian) -> Gaussian:
    return left[0] * right[0] - left[1] * right[1], left[0] * right[1] + left[1] * right[0]


def conjugate(value: Gaussian) -> Gaussian:
    return value[0], -value[1]


def scale(value: Gaussian, scalar: Fraction) -> Gaussian:
    return scalar * value[0], scalar * value[1]


def norm_squared(value: Gaussian) -> Fraction:
    return value[0] * value[0] + value[1] * value[1]


def check() -> bool:
    beta = (Fraction(2), Fraction(1))
    weight = (Fraction(1), Fraction(-2))
    powers = ((Fraction(1), Fraction(0)), (Fraction(0), Fraction(1)), (Fraction(-1), Fraction(0)), (Fraction(0), Fraction(-1)))
    total = (Fraction(0), Fraction(0))
    for power in powers:
        packet = add(beta, mul(power, weight))
        total = add(total, scale(mul(power, (norm_squared(packet), Fraction(0))), Fraction(1, 4)))
    return total == mul(beta, conjugate(weight))


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--check", action="store_true")
    parser.parse_args()
    if not check():
        print("TPC214_PACKET_CHECK=FAIL")
        return 1
    print("TPC214_PACKET_CHECK=PASS")
    print("identity=1/4 sum_j i^j |beta+i^j w|^2 = beta conjugate(w)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
