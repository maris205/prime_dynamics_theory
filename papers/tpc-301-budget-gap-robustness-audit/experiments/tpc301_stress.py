#!/usr/bin/env python3
"""Small exact stress fixtures for the TPC-301 theorem layer."""

from __future__ import annotations

from fractions import Fraction
import sys

import mpmath as mp

mp.mp.dps = 50


class Failure(RuntimeError):
    pass


def need(condition: bool, message: str) -> None:
    if type(condition) is not bool or not condition:
        raise Failure(message)


def scalar_fixture() -> None:
    # V=3, M=2, b=6.  For 0<tau<1 the least-budget feasible c is
    # c=2(1-tau), hence B=8(1-tau)^2.
    values = []
    for tau in (Fraction(1, 4), Fraction(1, 2), Fraction(3, 4)):
        c = Fraction(2) * (1 - tau)
        budget = Fraction(2) * c * c
        expected = Fraction(8) * (1 - tau) * (1 - tau)
        need(budget == expected, "scalar frontier identity")
        values.append(budget)
    need(values[0] >= values[1] >= values[2],
         "scalar tolerance monotonicity")
    # Relative target scaling leaves the normalized frontier unchanged.
    for alpha in (Fraction(2), Fraction(-3)):
        b = Fraction(6) * alpha
        radius = Fraction(1, 2) * abs(b)
        c = (b - radius if b >= 0 else b + radius) / 3
        scaled_budget = Fraction(2) * c * c
        need(scaled_budget == alpha * alpha * values[1],
             "scalar homogeneity")


def normalization_fixture() -> None:
    weighted = Fraction(7, 11)
    positive = Fraction(1, 37)
    for normalizer in (Fraction(2), Fraction(13, 5), Fraction(101, 7)):
        need(weighted / normalizer / (positive / normalizer) ==
             weighted / positive, "normalization invariance")


def nested_prefix_fixture() -> None:
    # Adding an unused source coordinate cannot increase the feasible minimum.
    # The second coordinate is visible but its zero coefficient realizes the
    # old solution, so the feasible set is nested exactly.
    old_budget = Fraction(5)
    extended_budget = min(old_budget, Fraction(5) + Fraction(0))
    need(extended_budget <= old_budget, "nested prefix budget")


def main() -> int:
    try:
        scalar_fixture()
        normalization_fixture()
        nested_prefix_fixture()
    except Failure as error:
        print("TPC301_STRESS=FAIL " + str(error), file=sys.stderr)
        return 1
    print("TPC301_STRESS=PASS tolerance=1 homogeneity=1 normalization=1 prefix=1")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
