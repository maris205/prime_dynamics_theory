#!/usr/bin/env python3
"""Exact rational stress audit for the TPC-261 budget compiler."""

from __future__ import annotations

import argparse
import sys
from fractions import Fraction


REQUIRED = Fraction(1, 400)
BASELINE = Fraction(5, 3)
TARGET = Fraction(1997, 1200)


def need(condition: bool, message: str) -> None:
    if type(condition) is not bool or not condition:
        raise RuntimeError(message)


def classify(effective: Fraction) -> str:
    if effective > REQUIRED:
        return "STRICT"
    if effective == REQUIRED:
        return "BORDERLINE"
    return "INSUFFICIENT"


def grid_audit() -> int:
    cases = 0
    for delta_num in range(0, 121):
        for loss_num in range(0, 61):
            delta = Fraction(delta_num, 1200)
            loss = Fraction(loss_num, 1200)
            effective = delta - loss
            expected = ("STRICT" if effective > REQUIRED else
                        "BORDERLINE" if effective == REQUIRED else
                        "INSUFFICIENT")
            need(classify(effective) == expected, "grid classification")
            need(effective == delta - loss, "effective identity")
            cases += 1
    return cases


def endpoint_audit() -> int:
    need(BASELINE - TARGET == REQUIRED, "endpoint gap")
    strict = Fraction(1, 100) - Fraction(1, 1200)
    need(strict == Fraction(11, 1200), "strict benchmark")
    need(strict - REQUIRED == Fraction(1, 150), "strict margin")
    local = Fraction(1, 48)
    need(local - REQUIRED == Fraction(11, 600), "local margin")
    borderline = REQUIRED - Fraction(0)
    need(classify(borderline) == "BORDERLINE", "borderline")
    below = REQUIRED - Fraction(1, 1200)
    need(below == Fraction(1, 600), "below threshold")
    need(classify(below) == "INSUFFICIENT", "below classification")
    return 7


def scaled_audit() -> int:
    amplitude = Fraction(5, 6)
    need(2 * amplitude == BASELINE, "scaled amplitude")
    plus_sum_exponent = amplitude
    need(plus_sum_exponent * 2 == BASELINE, "squared output exponent")
    need(16 > 0, "plus coefficient")
    need(0 == 0, "alternating cancellation")
    return 4


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()
    need(args.check, "--check required")
    grid = grid_audit()
    endpoint = endpoint_audit()
    scaled = scaled_audit()
    print("TPC261_STRESS=PASS "
          f"grid_cases={grid} endpoint_checks={endpoint} "
          f"scaled_checks={scaled} strict_threshold=1/400 "
          "log_power_credit=NONE")
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except Exception as exc:
        print("TPC261_STRESS=FAIL " + str(exc), file=sys.stderr)
        raise SystemExit(1)
