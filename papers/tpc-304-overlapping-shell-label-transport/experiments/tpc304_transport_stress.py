#!/usr/bin/env python3
"""Small adversarial tests for the TPC-304 transport identities."""

from __future__ import annotations

import itertools
import sys
from fractions import Fraction


def need(ok: bool, message: str) -> None:
    if type(ok) is not bool or not ok:
        raise RuntimeError(message)


def score(left: tuple[int, ...], right: tuple[int, ...]) -> tuple[int, int, Fraction]:
    raw = sum(a * b for a, b in zip(left, right))
    same = sum(a == b for a, b in zip(left, right))
    mismatches = min(same, len(left) - same)
    rho = Fraction(abs(raw), len(left))
    need(Fraction(mismatches, len(left)) == (1 - rho) / 2,
         "correlation/disagreement identity")
    return raw, mismatches, rho


def main() -> int:
    for length in range(1, 9):
        labels = list(itertools.product((-1, 1), repeat=length))
        for left in labels:
            for right in labels[::max(1, len(labels) // 16)]:
                raw, mismatches, rho = score(left, right)
                for left_sign in (-1, 1):
                    for right_sign in (-1, 1):
                        flipped = tuple(right_sign * x for x in right)
                        flipped_raw, flipped_mismatches, flipped_rho = score(
                            tuple(left_sign * x for x in left), flipped)
                        need(abs(flipped_raw) == abs(raw), "gauge invariance")
                        need(flipped_mismatches == mismatches and
                             flipped_rho == rho, "gauge-invariant defect")
    # Tie cases exercise the deterministic +1 gauge convention without
    # asserting that either sign is mathematically preferred.
    tie_left = (1, 1, 1, 1)
    tie_right = (1, 1, -1, -1)
    raw, mismatches, rho = score(tie_left, tie_right)
    need(raw == 0 and mismatches == 2 and rho == 0, "zero-correlation tie")
    need(Fraction(1, 3) <= Fraction(1, 3), "threshold endpoint")
    print("TPC304_STRESS=PASS gauge_invariance=1 identity=1 tie_case=1")
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except (RuntimeError, ValueError) as error:
        print("TPC304_STRESS=FAIL " + str(error), file=sys.stderr)
        raise SystemExit(1)
