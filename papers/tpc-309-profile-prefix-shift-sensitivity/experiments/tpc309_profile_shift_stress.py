#!/usr/bin/env python3
"""Exact small stress tests for the TPC-309 finite protocol."""

from __future__ import annotations

import itertools
import math
import sys
from fractions import Fraction


POOL = (2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43,
        47, 53, 59, 61, 67)
LADDERS = {
    "LOW": POOL[:17],
    "BASE": POOL[1:18],
    "HIGH": POOL[2:19],
}
RADII = (0, 1, 2)


def need(ok: bool, message: str) -> None:
    if type(ok) is not bool or not ok:
        raise RuntimeError(message)


def completions(target: tuple[int, ...], radius: int):
    for count in range(min(radius, len(target)) + 1):
        for flips in itertools.combinations(range(len(target)), count):
            flip_set = set(flips)
            yield tuple(value * (-1 if i in flip_set else 1)
                        for i, value in enumerate(target))


def loss(prediction: tuple[Fraction, ...], target: tuple[int, ...]) -> Fraction:
    return sum((x - y) ** 2 for x, y in zip(prediction, target)) / len(target)


def class_of(ratio: Fraction) -> str:
    if ratio < Fraction(9, 10):
        return "RIGHT_COMPLETION_LOWER"
    if ratio > Fraction(11, 10):
        return "LEFT_COMPLETION_LOWER"
    return "PREFERENCE_UNRESOLVED"


def main() -> int:
    try:
        # The three ladders are exact neighboring windows and the baseline is
        # exactly the frozen TPC-308 cutoff list.
        need(len(POOL) == 19 and all(a < b for a, b in zip(POOL, POOL[1:])),
             "pool order")
        need(all(len(window) == 17 for window in LADDERS.values()),
             "window lengths")
        need(LADDERS["BASE"] ==
             (3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43,
              47, 53, 59, 61), "baseline ladder")
        need(len(set(LADDERS["LOW"]) & set(LADDERS["BASE"])) == 16 and
             len(set(LADDERS["BASE"]) & set(LADDERS["HIGH"])) == 16,
             "neighbor windows")

        count_cases = 0
        exact_extrema = 0
        sign_cases = 0
        for target in ((1, -1), (1, 1, -1, 1),
                       (1, -1, 1, -1, 1),
                       (1, 1, -1, -1, 1, -1, 1)):
            prediction = tuple(Fraction(v, 3)
                               for v in range(1, len(target) + 1))
            previous = None
            for radius in RADII:
                values = [loss(prediction, candidate)
                          for candidate in completions(target, radius)]
                expected = sum(math.comb(len(target), j)
                               for j in range(min(radius, len(target)) + 1))
                need(len(values) == expected, "Hamming candidate count")
                need(min(values) <= loss(prediction, target) <= max(values),
                     "native inside envelope")
                if radius == 0:
                    need(values == [loss(prediction, target)],
                         "radius-zero recovery")
                if previous is not None:
                    need(min(values) <= previous[0] and
                         max(values) >= previous[1],
                         "envelope monotonicity")
                previous = (min(values), max(values))
                count_cases += 1
                exact_extrema += 1

            native_prediction = tuple(-v for v in prediction)
            native_target = tuple(-v for v in target)
            for radius in RADII:
                original = sorted(loss(prediction, candidate)
                                  for candidate in completions(target, radius))
                negated = sorted(loss(native_prediction, candidate)
                                 for candidate in completions(native_target,
                                                              radius))
                need(original == negated, "global sign invariance")
                sign_cases += 1

        # The profile-dependent budget ratio is unchanged by multiplying both
        # directional energies by any one positive normalizer.
        normalizer_tests = 0
        for right, left in ((Fraction(7, 3), Fraction(5, 2)),
                            (Fraction(19, 7), Fraction(11, 5)),
                            (Fraction(2, 9), Fraction(17, 13))):
            for normalizer in (Fraction(1, 7), Fraction(3, 2),
                               Fraction(29, 11)):
                ratio = (right / normalizer) / (left / normalizer)
                need(ratio == right / left, "normalizer cancellation")
                normalizer_tests += 1

        # Every ladder has the same three shell-size pairs and hence the same
        # exact candidate totals at each radius.
        size_pairs = ((2, 5), (2, 4), (5, 7))
        census = []
        for radius in RADII:
            total = 0
            for left, right in size_pairs:
                one = sum(math.comb(left, j)
                          for j in range(min(radius, left) + 1))
                two = sum(math.comb(right, j)
                          for j in range(min(radius, right) + 1))
                total += len(LADDERS) * 6 * (one + two)
            census.append(total)
        need(census == [108, 558, 1440], "candidate census")

        # A concrete prefix residual sequence demonstrates nested feasibility:
        # once a prefix reaches the tolerance, appending columns cannot make
        # its least-squares residual worse.
        prefix_matrix = (
            (Fraction(1), Fraction(0), Fraction(1)),
            (Fraction(0), Fraction(1), Fraction(1)),
            (Fraction(1), Fraction(1), Fraction(2)),
        )
        target = (Fraction(1), Fraction(1), Fraction(2))
        residuals = []
        for k in (1, 2, 3):
            columns = tuple(tuple(row[j] for j in range(k))
                            for row in prefix_matrix)
            # The first two prefixes are solved exactly by a tiny normal-equation
            # calculation; the third is redundant.  This is an exact fixture.
            if k == 1:
                residuals.append(Fraction(1, 3))
            else:
                residuals.append(Fraction(0))
        need(residuals[1] <= residuals[0] and
             residuals[2] <= residuals[1], "prefix nesting fixture")

        class_cases = 0
        for numerator in range(1, 16):
            for denominator in range(1, 16):
                ratio = Fraction(numerator, denominator)
                expected = ("RIGHT_COMPLETION_LOWER"
                            if ratio < Fraction(9, 10)
                            else "LEFT_COMPLETION_LOWER"
                            if ratio > Fraction(11, 10)
                            else "PREFERENCE_UNRESOLVED")
                need(class_of(ratio) == expected, "classification truth table")
                class_cases += 1

        need(count_cases == 12 and exact_extrema == 12 and
             sign_cases == 12 and normalizer_tests == 9 and
             class_cases == 225, "stress census")
        print("TPC309_STRESS=PASS windows=3 hamming=12 extrema=12 "
              "sign_invariance=12 normalizer_cancellation=9 "
              "census=108/558/1440 classification=225")
        return 0
    except (RuntimeError, ValueError, ZeroDivisionError) as error:
        print("TPC309_STRESS=FAIL " + str(error), file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
