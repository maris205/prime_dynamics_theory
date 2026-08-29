#!/usr/bin/env python3
"""Small exact stress suite for the TPC-310 aggregation protocol."""

from __future__ import annotations

import itertools
import json
import math
import sys
from fractions import Fraction
from pathlib import Path


ROOT = Path(__file__).resolve().parents[3]
RESULT = ROOT / "papers/tpc-310-cross-holdout-aggregation-order/results/tpc310_certificate.json"
LADDERS = ("LOW", "BASE", "HIGH")
RADII = (0, 1, 2)
MODES = ("POOLED_MSE", "BALANCED_RATIO", "GEOMETRIC_RATIO")


def need(ok: bool, message: str) -> None:
    if type(ok) is not bool or not ok:
        raise RuntimeError(message)


def subsets(values):
    return [tuple(values[i] for i in choice)
            for size in range(1, len(values) + 1)
            for choice in itertools.combinations(range(len(values)), size)]


def classify_fraction(value: Fraction) -> str:
    if value < Fraction(9, 10):
        return "RIGHT_COMPLETION_LOWER"
    if value > Fraction(11, 10):
        return "LEFT_COMPLETION_LOWER"
    return "PREFERENCE_UNRESOLVED"


def explicit_pooled(rows):
    values = []
    for choices in itertools.product(("lo", "hi"), repeat=len(rows) * 2):
        numer = Fraction(0)
        denom = Fraction(0)
        for index, row in enumerate(rows):
            numer += row["a_" + choices[2 * index]]
            denom += row["b_" + choices[2 * index + 1]]
        values.append(numer / denom)
    return min(values), max(values)


def main() -> int:
    try:
        # Selector family: every nonempty profile subset crossed with every
        # nonempty radius subset.
        ladder_subsets = subsets(LADDERS)
        radius_subsets = subsets(RADII)
        need(len(ladder_subsets) == 7 and len(radius_subsets) == 7,
             "subset census")
        need(len(ladder_subsets) * len(radius_subsets) == 49,
             "selector census")

        # Independent finite completion choices: extrema of a sum are sums of
        # extrema.  The explicit enumeration below is deliberately tiny and
        # uses exact rational arithmetic.
        rows = [
            {"a_lo": Fraction(1), "a_hi": Fraction(4),
             "b_lo": Fraction(2), "b_hi": Fraction(7)},
            {"a_lo": Fraction(3), "a_hi": Fraction(9),
             "b_lo": Fraction(5), "b_hi": Fraction(11)},
        ]
        expected = (sum(row["a_lo"] for row in rows) /
                    sum(row["b_hi"] for row in rows),
                    sum(row["a_hi"] for row in rows) /
                    sum(row["b_lo"] for row in rows))
        explicit = explicit_pooled(rows)
        need(explicit == expected, "pooled extrema")

        # The ratio-of-sums identity is a weighted mean identity.  This is the
        # algebraic reason that pooled and equal-case aggregation can disagree.
        a = (Fraction(1, 5), Fraction(22, 10))
        b = (Fraction(100), Fraction(1))
        ratios = tuple(x / y for x, y in zip(a, b))
        pooled = sum(a) / sum(b)
        weighted = sum(y * r for y, r in zip(b, ratios)) / sum(b)
        balanced = sum(ratios) / len(ratios)
        need(pooled == weighted, "weighted mean identity")
        need(classify_fraction(pooled) == "RIGHT_COMPLETION_LOWER" and
             classify_fraction(balanced) == "LEFT_COMPLETION_LOWER",
             "exact aggregation reversal fixture")

        # Monotone positive interval maps: arithmetic means preserve endpoint
        # order, and geometric means do so after log/exp on positive inputs.
        lower = (Fraction(1, 5), Fraction(2, 5), Fraction(3, 5))
        upper = (Fraction(2, 5), Fraction(4, 5), Fraction(9, 10))
        need(all(x > 0 and x <= y for x, y in zip(lower, upper)),
             "positive fixture")
        arithmetic = (sum(lower) / 3, sum(upper) / 3)
        need(arithmetic[0] <= arithmetic[1], "arithmetic interval map")
        geometric = (math.prod(float(x) for x in lower) ** (1 / 3),
                     math.prod(float(x) for x in upper) ** (1 / 3))
        need(0 < geometric[0] <= geometric[1], "geometric interval map")

        # Recheck the headline certificate shape and the finite class census.
        data = json.loads(RESULT.read_text(encoding="utf-8"))
        payload = data["payload"]
        selectors = payload["selectors"]
        need(len(selectors) == 49, "stored selectors")
        for selector in selectors:
            need(len(selector["aggregates"]) == 3 and
                 selector["observation_count"] > 0,
                 "stored aggregate shape")
            need({row["mode"] for row in selector["aggregates"]} ==
                 set(MODES), "stored modes")
        need(payload["finite_audit"]["class_counts_by_mode"] == {
            "POOLED_MSE": {"RIGHT_COMPLETION_LOWER": 42,
                           "LEFT_COMPLETION_LOWER": 1,
                           "PREFERENCE_UNRESOLVED": 6},
            "BALANCED_RATIO": {"RIGHT_COMPLETION_LOWER": 1,
                               "LEFT_COMPLETION_LOWER": 32,
                               "PREFERENCE_UNRESOLVED": 16},
            "GEOMETRIC_RATIO": {"RIGHT_COMPLETION_LOWER": 26,
                                 "LEFT_COMPLETION_LOWER": 0,
                                 "PREFERENCE_UNRESOLVED": 23},
        }, "stored class census")
        need(payload["finite_audit"]["full_selector_classes"] == {
            "POOLED_MSE": "RIGHT_COMPLETION_LOWER",
            "BALANCED_RATIO": "LEFT_COMPLETION_LOWER",
            "GEOMETRIC_RATIO": "RIGHT_COMPLETION_LOWER",
        }, "stored reversal")

        print("TPC310_STRESS=PASS selectors=49 pooled_extrema=1 "
              "weighted_identity=1 reversal=1 interval_maps=2 "
              "classes=147")
        return 0
    except (RuntimeError, OSError, ValueError, ZeroDivisionError) as error:
        print("TPC310_STRESS=FAIL " + str(error), file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
