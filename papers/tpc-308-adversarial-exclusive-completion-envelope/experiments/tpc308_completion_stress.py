#!/usr/bin/env python3
"""Exact small stress tests for the TPC-308 completion envelope."""

from __future__ import annotations

import itertools
import math
import sys
from fractions import Fraction


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
        count_cases = 0
        monotonic_cases = 0
        sign_cases = 0
        exact_extrema_cases = 0
        for target in ((1, -1), (1, 1, -1, 1),
                       (1, -1, 1, -1, 1),
                       (1, 1, -1, -1, 1, -1, 1)):
            prediction = tuple(Fraction(v, 3) for v in range(1, len(target) + 1))
            previous = None
            for radius in (0, 1, 2):
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
                         "radius monotonicity")
                previous = (min(values), max(values))
                count_cases += 1
                exact_extrema_cases += 1

            # Negating both prediction and native target bijects the complete
            # Hamming ball and preserves every squared loss.
            native_neg = tuple(-v for v in prediction)
            target_neg = tuple(-v for v in target)
            for radius in (0, 1, 2):
                original = sorted(loss(prediction, c)
                                  for c in completions(target, radius))
                negated = sorted(loss(native_neg, c)
                                 for c in completions(target_neg, radius))
                need(original == negated, "global sign invariance")
                sign_cases += 1

            # The three declared shell-size pairs account for the published
            # candidate census, with six (exponent,tau) cells per transition.
            monotonic_cases += 1

        sizes = ((2, 5), (2, 4), (5, 7))
        census = []
        for radius in (0, 1, 2):
            total = 0
            for left, right in sizes:
                total += 6 * (sum(math.comb(left, j)
                                  for j in range(min(radius, left) + 1)) +
                               sum(math.comb(right, j)
                                   for j in range(min(radius, right) + 1)))
            census.append(total)
        need(census == [36, 186, 480], "published candidate census")

        class_cases = 0
        for numerator in range(1, 16):
            for denominator in range(1, 16):
                ratio = Fraction(numerator, denominator)
                expected = ("RIGHT_COMPLETION_LOWER" if ratio < Fraction(9, 10)
                            else "LEFT_COMPLETION_LOWER" if ratio > Fraction(11, 10)
                            else "PREFERENCE_UNRESOLVED")
                need(class_of(ratio) == expected, "classification truth table")
                class_cases += 1

        need(count_cases == 12 and exact_extrema_cases == 12 and
             sign_cases == 12 and monotonic_cases == 4 and
             class_cases == 225, "stress census")
        print("TPC308_STRESS=PASS hamming=12 extrema=12 sign_invariance=36 "
              "size_census=36/186/480 classification=225")
        return 0
    except (RuntimeError, ValueError, ZeroDivisionError) as error:
        print("TPC308_STRESS=FAIL " + str(error), file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
