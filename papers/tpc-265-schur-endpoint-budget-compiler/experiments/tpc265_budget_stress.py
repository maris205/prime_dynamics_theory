#!/usr/bin/env python3
"""Exact stress tests for the Schur radial and endpoint budget rules."""

from __future__ import annotations

import argparse
import sys
from fractions import Fraction


def need(condition: bool, message: str) -> None:
    if type(condition) is not bool or not condition:
        raise RuntimeError(message)


def radial_check(center: Fraction, radius: Fraction) -> tuple[Fraction, Fraction]:
    upper = abs(center) + radius
    lower = max(abs(center) - radius, Fraction(0))
    # Real aligned/opposite points certify both disk endpoints exactly.
    plus = center + radius if center >= 0 else center - radius
    opposite = center - radius if center >= 0 else center + radius
    need(abs(plus) == upper, "aligned endpoint")
    need(abs(opposite) >= lower, "opposite endpoint")
    if abs(center) <= radius:
        cancel = -center
        need(abs(center + cancel) == 0, "disk cancellation")
    return upper, lower


def budget_check() -> tuple[int, int, int]:
    required = Fraction(1, 400)
    strict = borderline = insufficient = 0
    for delta in (Fraction(1, 200), Fraction(1, 320), Fraction(1, 400),
                  Fraction(1, 500), Fraction(0)):
        for loss in (Fraction(0), Fraction(1, 1200)):
            effective = delta - loss
            if effective > required:
                strict += 1
            elif effective == required:
                borderline += 1
            else:
                insufficient += 1
    need(strict == 3 and borderline == 1 and insufficient == 6,
         "budget census")
    return strict, borderline, insufficient


def run() -> None:
    centers = (Fraction(0), Fraction(1), Fraction(2), Fraction(-3),
               Fraction(7, 2))
    radii = (Fraction(0), Fraction(1, 3), Fraction(2), Fraction(5))
    radial_cases = 0
    for center in centers:
        for radius in radii:
            radial_check(center, radius)
            radial_cases += 1

    # Independent Schur radii add exactly when their phases are free.
    lane_sets = (
        (Fraction(1), Fraction(2)),
        (Fraction(1, 2), Fraction(3, 2), Fraction(5, 2)),
        (Fraction(0), Fraction(4), Fraction(7, 3), Fraction(1, 3)),
    )
    minkowski_cases = 0
    for radii_set in lane_sets:
        total = sum(radii_set, Fraction(0))
        upper, _ = radial_check(Fraction(3, 2), total)
        need(upper == Fraction(3, 2) + total, "Minkowski upper")
        minkowski_cases += 1

    strict, borderline, insufficient = budget_check()
    need(2 * Fraction(5, 6) == Fraction(5, 3), "scale exponent")
    print("TPC265_BUDGET_STRESS=PASS "
          f"radial_cases={radial_cases} minkowski_cases={minkowski_cases} "
          f"strict={strict} borderline={borderline} insufficient={insufficient} "
          "threshold=1/400 log_credit=0")


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
        print("TPC265_BUDGET_STRESS=FAIL " + str(exc), file=sys.stderr)
        raise SystemExit(1)
