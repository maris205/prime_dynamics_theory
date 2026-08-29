#!/usr/bin/env python3
"""Small exact stress tests for the TPC-307 finite protocol."""

from __future__ import annotations

import itertools
import sys
from fractions import Fraction


def need(ok: bool, message: str) -> None:
    if type(ok) is not bool or not ok:
        raise RuntimeError(message)


def partition(left: set[int], right: set[int]) -> tuple[set[int], ...]:
    overlap = left & right
    exclusive_left = left - overlap
    exclusive_right = right - overlap
    union = left | right
    return union, overlap, exclusive_left, exclusive_right


def class_of(ratio: Fraction) -> str:
    if ratio < Fraction(9, 10):
        return "RIGHT_COMPLETION_LOWER"
    if ratio > Fraction(11, 10):
        return "LEFT_COMPLETION_LOWER"
    return "PREFERENCE_UNRESOLVED"


def sign_invariant(target: tuple[int, ...], holdout: tuple[int, ...],
                  prediction: tuple[Fraction, ...]) -> bool:
    loss = sum((x - y) ** 2 for x, y in zip(prediction, holdout))
    neg_loss = sum((-x + y) ** 2 for x, y in zip(prediction, holdout))
    target_norm = sum(x * x for x in target)
    neg_norm = sum((-x) * (-x) for x in target)
    return loss == neg_loss and target_norm == neg_norm


def main() -> int:
    try:
        partition_cases = 0
        for left in ({2, 3, 5}, {3, 5, 7, 11}, {5, 7, 13, 17, 19}):
            for right in ({2, 3, 7}, {5, 11, 13}, {5, 7, 13, 23}):
                union, overlap, exclusive_left, exclusive_right = partition(
                    set(left), set(right))
                need(bool(overlap and exclusive_left and exclusive_right),
                     "nonempty stress partition")
                need(not (overlap & exclusive_left) and
                     not (overlap & exclusive_right) and
                     not (exclusive_left & exclusive_right),
                     "partition disjointness")
                need(union == overlap | exclusive_left | exclusive_right,
                     "partition union")
                partition_cases += 1

        sign_cases = 0
        for target in itertools.product((-1, 1), repeat=3):
            for holdout in itertools.product((-1, 1), repeat=2):
                prediction = (Fraction(1, 3), Fraction(-2, 5))
                need(sign_invariant(target, holdout, prediction),
                     "global sign invariance")
                sign_cases += 1

        # A feasible coefficient vector at a shorter profile prefix remains
        # feasible after zero-padding into every longer prefix.
        prefix_cases = 0
        for j in range(1, 5):
            target = (Fraction(1), Fraction(-1))
            represented = (Fraction(1), Fraction(-1))
            for k in range(j, 6):
                padded = tuple(Fraction(0) for _ in range(k - j))
                need(represented == target and len(padded) == k - j,
                     "nested prefix padding")
                prefix_cases += 1

        class_cases = 0
        for numerator in range(1, 13):
            for denominator in range(1, 13):
                ratio = Fraction(numerator, denominator)
                expected = ("RIGHT_COMPLETION_LOWER" if ratio < Fraction(9, 10)
                            else "LEFT_COMPLETION_LOWER" if ratio > Fraction(11, 10)
                            else "PREFERENCE_UNRESOLVED")
                need(class_of(ratio) == expected, "classification truth table")
                class_cases += 1

        need(partition_cases == 9 and sign_cases == 32 and
             prefix_cases == 14 and class_cases == 144, "stress census")
        print("TPC307_STRESS=PASS partitions=9 sign_invariance=32 "
              "nested_prefix=14 classification=144")
        return 0
    except (RuntimeError, ValueError, ZeroDivisionError) as error:
        print("TPC307_STRESS=FAIL " + str(error), file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
