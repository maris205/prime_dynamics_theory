#!/usr/bin/env python3
"""Exact stress replay for the TPC-266 hostile composition matrix."""

from __future__ import annotations

import argparse
import sys
from fractions import Fraction


REQUIRED = Fraction(1, 400)


def need(condition: bool, message: str) -> None:
    if type(condition) is not bool or not condition:
        raise RuntimeError(message)


def shape(dimension: int, a: Fraction, b: Fraction) -> str:
    need(dimension >= 0 and a >= 0 and b >= 0, "shape inputs")
    if dimension >= 2 and a > 0 and b > 0:
        return "DISK"
    if dimension == 1 and a > 0 and b > 0:
        return "CIRCLE"
    return "SINGLETON"


def radial(center: Fraction, radius: Fraction) -> tuple[Fraction, Fraction]:
    need(radius >= 0, "radius")
    upper = abs(center) + radius
    lower = max(abs(center) - radius, Fraction(0))
    need(upper >= lower, "radial order")
    return upper, lower


def classify(kind: str, delta: Fraction | None,
             loss: Fraction | None) -> str:
    if kind == "FIXED_LOG":
        return "NO_FIXED_POWER"
    if kind == "MISSING":
        return "MISSING"
    if kind == "DELETED":
        return "DELETED"
    need(kind in {"POWER", "SIGNED_PHASE"}, "lane kind")
    need(delta is not None and loss is not None, "lane parameters")
    effective = delta - loss
    if effective > REQUIRED:
        return "STRICT"
    if effective == REQUIRED:
        return "BORDERLINE"
    return "INSUFFICIENT"


def decision(center_kind: str, center_delta: Fraction | None,
             center_loss: Fraction | None, radius_kind: str,
             radius_delta: Fraction | None, radius_loss: Fraction | None,
             retained: bool) -> str:
    if not retained:
        return "UNSOUND_RESIDUAL_DELETION"
    if center_kind == "FIXED_LOG":
        return "OPEN_LOG_CENTER"
    if radius_kind == "MISSING":
        return "OPEN_RADIUS"
    if center_kind == "DELETED" or radius_kind == "DELETED":
        return "UNSOUND_LANE_DELETION"
    c = classify(center_kind, center_delta, center_loss)
    r = classify(radius_kind, radius_delta, radius_loss)
    if c == "BORDERLINE" or r == "BORDERLINE":
        return "BORDERLINE"
    if c == "INSUFFICIENT" or r == "INSUFFICIENT":
        return "INSUFFICIENT"
    if c == "STRICT" and r == "STRICT":
        return "CLOSED_CONDITIONAL"
    return "OPEN_UNPAID"


def run() -> None:
    endpoint_cases = 0
    for center in (Fraction(-7), Fraction(-2), Fraction(0), Fraction(2), Fraction(7)):
        for radius in (Fraction(0), Fraction(1), Fraction(3), Fraction(8)):
            upper, lower = radial(center, radius)
            need(upper == abs(center) + radius, "upper formula")
            need(lower == max(abs(center) - radius, Fraction(0)), "lower formula")
            endpoint_cases += 1

    dimension_cases = 0
    for dimension in (0, 1, 2, 4):
        for a, b in ((Fraction(0), Fraction(2)),
                     (Fraction(2), Fraction(0)),
                     (Fraction(2), Fraction(3))):
            result = shape(dimension, a, b)
            if a == 0 or b == 0 or dimension == 0:
                need(result == "SINGLETON", "degenerate Schur shape")
            elif dimension == 1:
                need(result == "CIRCLE", "one-dimensional Schur shape")
            else:
                need(result == "DISK", "multi-dimensional Schur shape")
            dimension_cases += 1

    strict = Fraction(1, 320)
    loss = Fraction(1, 1200)
    states = [
        ("CLOSED_CONDITIONAL", decision("POWER", strict, Fraction(0),
                                         "SIGNED_PHASE", strict, Fraction(0), True)),
        ("OPEN_LOG_CENTER", decision("FIXED_LOG", None, None,
                                     "POWER", strict, Fraction(0), True)),
        ("OPEN_RADIUS", decision("POWER", strict, Fraction(0),
                                 "MISSING", None, None, True)),
        ("BORDERLINE", decision("POWER", REQUIRED, Fraction(0),
                                "POWER", strict, Fraction(0), True)),
        ("INSUFFICIENT", decision("POWER", strict, loss,
                                  "POWER", strict, loss, True)),
        ("UNSOUND_RESIDUAL_DELETION", decision("POWER", strict, Fraction(0),
                                                "POWER", strict, Fraction(0), False)),
    ]
    for expected, actual in states:
        need(actual == expected, "state matrix")

    proxy = [Fraction(2 ** m, m ** 3) for m in (10, 20, 40)]
    need(proxy[0] < proxy[1] < proxy[2], "log firewall proxy")
    need(decision("POWER", strict, Fraction(0), "POWER", strict,
                  Fraction(0), True) != "OPEN_LOG_CENTER",
         "strict lane accidentally logged")
    need(decision("FIXED_LOG", None, None, "POWER", strict,
                  Fraction(0), True) != "CLOSED_CONDITIONAL",
         "log promotion accepted")
    need(decision("POWER", strict, Fraction(0), "POWER", strict,
                  Fraction(0), False) != "CLOSED_CONDITIONAL",
         "deleted residual accepted")

    print("TPC266_HOSTILE_MATRIX=PASS "
          f"endpoint_cases={endpoint_cases} dimension_cases={dimension_cases} "
          "states=6 strict=1 borderline=1 insufficient=1 "
          "firewalls=3")


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
        print("TPC266_HOSTILE_MATRIX=FAIL " + str(exc), file=sys.stderr)
        raise SystemExit(1)
