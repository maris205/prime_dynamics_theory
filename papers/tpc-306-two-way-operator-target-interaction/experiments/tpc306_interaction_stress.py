#!/usr/bin/env python3
"""Finite algebra and adversarial orientation tests for TPC-306."""

from __future__ import annotations

import itertools
import sys
from fractions import Fraction


def need(ok: bool, message: str) -> None:
    if type(ok) is not bool or not ok:
        raise RuntimeError(message)


def effects(ll: Fraction, lr: Fraction, rl: Fraction, rr: Fraction
            ) -> tuple[Fraction, Fraction]:
    # Positive rational stand-ins for the two row-wise budget ratios.
    return lr / ll, rr / rl


def classify(dl: Fraction, dr: Fraction) -> tuple[str, str]:
    if dl < 0 and dr < 0:
        preference = "RIGHT_LABEL_CHEAPER_ON_BOTH_OPERATORS"
    elif dl > 0 and dr > 0:
        preference = "LEFT_LABEL_CHEAPER_ON_BOTH_OPERATORS"
    else:
        preference = "MIXED_OPERATOR_PREFERENCE"
    gap = dl * dr
    dominance = ("TARGET_MAIN_DOMINATES" if gap > 0 else
                 "OPERATOR_INTERACTION_DOMINATES" if gap < 0 else
                 "DOMINANCE_UNRESOLVED")
    return preference, dominance


def main() -> int:
    try:
        values = tuple(Fraction(x) for x in range(1, 6))
        checked = 0
        for ll, lr, rl, rr in itertools.product(values, repeat=4):
            # Treat the four positive numbers as a small table of budget
            # cells; row-wise rescaling must not change either effect.
            x, y = effects(ll, lr, rl, rr)
            sx, sy = effects(7 * ll, 7 * lr, 13 * rl, 13 * rr)
            need(x == sx and y == sy, "row scaling invariance")
            # Use signed rational log-effect surrogates to test the exact
            # decomposition identity independently of transcendental logs.
            for dl in (Fraction(-3), Fraction(-1), Fraction(1), Fraction(2)):
                for dr in (Fraction(-2), Fraction(-1), Fraction(1), Fraction(4)):
                    m = (dl + dr) / 2
                    i = (dl - dr) / 2
                    need(m * m - i * i == dl * dr,
                         "squared contrast identity")
                    pref, dom = classify(dl, dr)
                    need((dl * dr > 0) == (dom == "TARGET_MAIN_DOMINATES"),
                         "dominance sign")
                    if dl < 0 and dr < 0:
                        need(pref == "RIGHT_LABEL_CHEAPER_ON_BOTH_OPERATORS",
                             "right preference")
                    if dl > 0 and dr > 0:
                        need(pref == "LEFT_LABEL_CHEAPER_ON_BOTH_OPERATORS",
                             "left preference")
            checked += 1
        need(checked == 625, "table census")
        print("TPC306_STRESS=PASS rational_tables=625 row_scaling=1 "
              "contrast_identity=1 orientation_sign=1")
        return 0
    except (RuntimeError, ValueError, ZeroDivisionError) as error:
        print("TPC306_STRESS=FAIL " + str(error), file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
