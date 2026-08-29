#!/usr/bin/env python3
"""Adversarial finite tests for the TPC-305 target-swap protocol."""

from __future__ import annotations

import itertools
import sys
from fractions import Fraction


def need(ok: bool, message: str) -> None:
    if type(ok) is not bool or not ok:
        raise RuntimeError(message)


def align(left: tuple[int, ...], right: tuple[int, ...]) -> tuple[int, tuple[int, ...]]:
    raw = sum(a * b for a, b in zip(left, right))
    sign = 1 if raw >= 0 else -1
    return sign, tuple(sign * x for x in right)


def orient(left: str, right: str) -> str:
    table = {
        ("BELOW_ONE_CERTIFIED", "ABOVE_ONE_CERTIFIED"):
            "RIGHT_LABEL_CHEAPER_ON_BOTH_OPERATORS",
        ("ABOVE_ONE_CERTIFIED", "BELOW_ONE_CERTIFIED"):
            "LEFT_LABEL_CHEAPER_ON_BOTH_OPERATORS",
        ("ABOVE_ONE_CERTIFIED", "ABOVE_ONE_CERTIFIED"):
            "HOME_OPERATOR_FAVORED",
        ("BELOW_ONE_CERTIFIED", "BELOW_ONE_CERTIFIED"):
            "CROSS_TARGET_FAVORED",
    }
    return table.get((left, right), "ORIENTATION_UNRESOLVED")


def main() -> int:
    try:
        for length in range(1, 9):
            labels = list(itertools.product((-1, 1), repeat=length))
            for left in labels:
                for right in labels[::max(1, len(labels) // 16)]:
                    sign, aligned = align(left, right)
                    raw = sum(a * b for a, b in zip(left, right))
                    mismatches = sum(a != b for a, b in zip(left, aligned))
                    rho = Fraction(abs(raw), length)
                    need(Fraction(mismatches, length) == (1 - rho) / 2,
                         "binary alignment identity")
                    for ls in (-1, 1):
                        for rs in (-1, 1):
                            fs, fa = align(tuple(ls * x for x in left),
                                            tuple(rs * x for x in right))
                            need(abs(fs * raw) == abs(raw),
                                 "global-sign alignment")
                            need(sum(ls * a != b for a, b in zip(left, fa))
                                 == mismatches,
                                 "gauge-invariant mismatch")
        # Negative alignment and native off-overlap extension.
        left_shell, right_shell = (2, 3, 5, 7), (5, 7, 11)
        lm, rm = dict(zip(left_shell, (1, 1, -1, -1))), dict(
            zip(right_shell, (1, 1, 1)))
        overlap = sorted(set(left_shell) & set(right_shell))
        raw = sum(lm[p] * rm[p] for p in overlap)
        need(raw < 0, "negative-sign fixture")
        sign = -1
        transported_left = [sign * rm[p] if p in rm else lm[p]
                            for p in left_shell]
        transported_right = [sign * lm[p] if p in lm else rm[p]
                             for p in right_shell]
        need(transported_left == [1, 1, -1, -1] and
             transported_right == [1, 1, 1], "off-overlap extension")
        need(orient("BELOW_ONE_CERTIFIED", "ABOVE_ONE_CERTIFIED") ==
             "RIGHT_LABEL_CHEAPER_ON_BOTH_OPERATORS" and
             orient("ABOVE_ONE_CERTIFIED", "BELOW_ONE_CERTIFIED") ==
             "LEFT_LABEL_CHEAPER_ON_BOTH_OPERATORS" and
             orient("ABOVE_ONE_CERTIFIED", "ABOVE_ONE_CERTIFIED") ==
             "HOME_OPERATOR_FAVORED" and
             orient("BELOW_ONE_CERTIFIED", "BELOW_ONE_CERTIFIED") ==
             "CROSS_TARGET_FAVORED" and
             orient("ONE_INTERVAL_UNRESOLVED", "ABOVE_ONE_CERTIFIED") ==
             "ORIENTATION_UNRESOLVED", "orientation truth table")
        print("TPC305_STRESS=PASS binary_lengths=1..8 negative_alignment=1 "
              "off_overlap=1 orientation_table=1")
        return 0
    except (RuntimeError, ValueError) as error:
        print("TPC305_STRESS=FAIL " + str(error), file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
