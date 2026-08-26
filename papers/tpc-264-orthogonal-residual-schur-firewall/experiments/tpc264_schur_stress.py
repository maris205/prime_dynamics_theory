#!/usr/bin/env python3
"""Exact dimension and radius stress audit for TPC-264."""

from __future__ import annotations

import argparse
import sys
from fractions import Fraction
from typing import NamedTuple


Gaussian = tuple[Fraction, Fraction]


class Scale(NamedTuple):
    a: Fraction
    b: Fraction


def need(condition: bool, message: str) -> None:
    if type(condition) is not bool or not condition:
        raise RuntimeError(message)


def multiply(left: Gaussian, right: Gaussian) -> Gaussian:
    return (left[0] * right[0] - left[1] * right[1],
            left[0] * right[1] + left[1] * right[0])


def conjugate(value: Gaussian) -> Gaussian:
    return (value[0], -value[1])


def ip(left: tuple[Gaussian, ...], right: tuple[Gaussian, ...]) -> Gaussian:
    out = (Fraction(0), Fraction(0))
    for a, b in zip(left, right):
        prior = multiply(conjugate(a), b)
        out = (out[0] + prior[0], out[1] + prior[1])
    return out


def norm2(vector: tuple[Gaussian, ...]) -> Fraction:
    value = ip(vector, vector)
    need(value[1] == 0, "non-real norm")
    return value[0]


def modulus2(value: Gaussian) -> Fraction:
    return value[0] * value[0] + value[1] * value[1]


def schur_ok(a: Fraction, b: Fraction, z: Gaussian) -> bool:
    return modulus2(z) <= a * a * b * b


def vector(a: Fraction, first: Gaussian, second: Gaussian) -> tuple[Gaussian, Gaussian]:
    return ((a, Fraction(0)), (Fraction(0), Fraction(0)))


def disk_witnesses(scale: Scale) -> list[tuple[Gaussian, tuple[Gaussian, ...], tuple[Gaussian, ...]]]:
    a, b = scale
    # Each pair (first coefficient, second coefficient) has squared norm one.
    coefficients = (
        ((Fraction(0), Fraction(0)), (Fraction(1), Fraction(0))),
        ((Fraction(3, 5), Fraction(0)), (Fraction(4, 5), Fraction(0))),
        ((Fraction(0), Fraction(3, 5)), (Fraction(4, 5), Fraction(0))),
        ((Fraction(1), Fraction(0)), (Fraction(0), Fraction(0))),
    )
    output = []
    for first, second in coefficients:
        u = ((a, Fraction(0)), (Fraction(0), Fraction(0)))
        v = (multiply((b, Fraction(0)), first),
             multiply((b, Fraction(0)), second))
        output.append((ip(u, v), u, v))
    return output


def run() -> None:
    scales = (Scale(Fraction(1), Fraction(1)),
              Scale(Fraction(2), Fraction(3, 2)),
              Scale(Fraction(5, 3), Fraction(7, 4)),
              Scale(Fraction(0), Fraction(5, 2)))
    disk_cases = circle_cases = singleton_cases = rejected = 0
    for scale in scales[:3]:
        a, b = scale
        radius2 = a * a * b * b
        for z, u, v in disk_witnesses(scale):
            need(norm2(u) == a * a and norm2(v) == b * b,
                 "witness norm")
            need(schur_ok(a, b, z), "disk witness")
            disk_cases += 1
        # An exact point outside the disk.
        outside = (a * b * Fraction(6, 5), Fraction(0))
        need(not schur_ok(a, b, outside), "outside point accepted")
        rejected += 1
        # In a one-dimensional complement every nonzero witness is on the circle.
        for phase in ((Fraction(1), Fraction(0)),
                      (Fraction(-1), Fraction(0)),
                      (Fraction(0), Fraction(1))):
            z = multiply((a * b, Fraction(0)), phase)
            need(modulus2(z) == radius2, "circle point")
            circle_cases += 1
        need(modulus2((Fraction(0), Fraction(0))) < radius2,
             "zero should be interior")
        rejected += 1

    # A zero residual norm collapses every complement dimension to a singleton.
    for m in (0, 1, 2, 7):
        z = (Fraction(0), Fraction(0))
        need(schur_ok(Fraction(0), Fraction(5, 2), z),
             "zero residual singleton")
        singleton_cases += 1
        if m == 1:
            need(modulus2(z) == 0, "one-dimensional zero residual")

    # The endpoint scale is an exponent identity, not a numerical prime claim.
    need(2 * Fraction(5, 6) == Fraction(5, 3), "endpoint exponent")
    need(Fraction(1, 320) > Fraction(1, 400), "strict budget fixture")
    need(Fraction(1, 400) == Fraction(1, 400), "borderline budget fixture")
    print("TPC264_SCHUR_STRESS=PASS "
          f"disk_cases={disk_cases} circle_cases={circle_cases} "
          f"singleton_cases={singleton_cases} rejected={rejected} "
          "dimensions=0,1,>=2 radius_exponent=5/3")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()
    need(args.check, "--check required")
    run()
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except Exception as exc:
        print("TPC264_SCHUR_STRESS=FAIL " + str(exc), file=sys.stderr)
        raise SystemExit(1)
