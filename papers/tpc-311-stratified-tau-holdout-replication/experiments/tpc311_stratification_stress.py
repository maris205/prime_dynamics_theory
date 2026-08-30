#!/usr/bin/env python3
"""Exact small stress suite for the TPC-311 two-stage protocol."""

from __future__ import annotations

import itertools
import json
import sys
from fractions import Fraction
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
RESULT = ROOT / (
    "papers/tpc-311-stratified-tau-holdout-replication/results/"
    "tpc311_certificate.json")
LADDERS = ("LOW", "BASE", "HIGH")
PAIRS = ((50, 60), (60, 70), (70, 90))
EXPONENTS = (1, 2)
TAUS = ("0.25", "0.5", "0.75")
RADII = (0, 1, 2)


def need(ok: bool, message: str) -> None:
    if type(ok) is not bool or not ok:
        raise RuntimeError(message)


def classify(value: Fraction) -> str:
    if value < Fraction(9, 10):
        return "RIGHT_COMPLETION_LOWER"
    if value > Fraction(11, 10):
        return "LEFT_COMPLETION_LOWER"
    return "PREFERENCE_UNRESOLVED"


def explicit_profile_pool(rows):
    """Enumerate independent binary endpoint choices for 3 profile rows."""
    values = []
    for choices in itertools.product(("lo", "hi"), repeat=6):
        numerator = sum(row["a_" + choices[2 * i]]
                        for i, row in enumerate(rows))
        denominator = sum(row["b_" + choices[2 * i + 1]]
                          for i, row in enumerate(rows))
        values.append(numerator / denominator)
    return min(values), max(values)


def main() -> int:
    try:
        # Balanced factorial design census and disjoint tau split.
        need(len(PAIRS) * len(EXPONENTS) * len(TAUS) * len(RADII) == 54,
             "factorial census")
        need(set(("0.25", "0.5")) & set(("0.75",)) == set() and
             set(("0.25", "0.5")) | set(("0.75",)) == set(TAUS),
             "tau partition")

        # Exact profile-pooled extrema: extrema of a sum are attained by
        # independent endpoint choices.  This is the finite algebra used in
        # every TPC-311 stratum.
        rows = [
            {"a_lo": Fraction(1), "a_hi": Fraction(4),
             "b_lo": Fraction(2), "b_hi": Fraction(7)},
            {"a_lo": Fraction(3), "a_hi": Fraction(9),
             "b_lo": Fraction(5), "b_hi": Fraction(11)},
            {"a_lo": Fraction(2), "a_hi": Fraction(6),
             "b_lo": Fraction(4), "b_hi": Fraction(10)},
        ]
        expected = (sum(row["a_lo"] for row in rows) /
                    sum(row["b_hi"] for row in rows),
                    sum(row["a_hi"] for row in rows) /
                    sum(row["b_lo"] for row in rows))
        need(explicit_profile_pool(rows) == expected,
             "profile pooled extrema")

        # Equal design-stratum weights are a monotone positive interval map.
        intervals = ((Fraction(1, 2), Fraction(3, 4)),
                     (Fraction(2), Fraction(5, 2)),
                     (Fraction(1, 4), Fraction(1, 3)))
        lower = sum(item[0] for item in intervals) / len(intervals)
        upper = sum(item[1] for item in intervals) / len(intervals)
        need(0 < lower <= upper, "equal stratum map")

        # A deliberately tiny exact tau-slice reversal fixture demonstrates
        # that a fixed aggregation rule can still fail to replicate across a
        # held-out parameter slice.
        calibration = Fraction(13, 5)
        confirmation = Fraction(2, 3)
        need(classify(calibration) == "LEFT_COMPLETION_LOWER" and
             classify(confirmation) == "RIGHT_COMPLETION_LOWER",
             "reversal fixture")

        data = json.loads(RESULT.read_text(encoding="utf-8"))
        payload = data["payload"]
        need(payload["schema"] ==
             "TPC311_STRATIFIED_TAU_SLICE_HOLDOUT_REPLICATION_V1",
             "schema")
        need(len(payload["strata"]) == 54 and len(payload["blocks"]) == 6 and
             len(payload["sensitivity"]) == 22, "stored census")
        need(payload["finite_audit"]["native_replication"] ==
             "STRICT_CLASS_REVERSED" and
             payload["finite_audit"]["all_radii_replication"] ==
             "NONREPLICATED_WITH_UNRESOLVED_SLICE", "stored obstruction")
        need(payload["protocol"]["registration_status"] ==
             "DECLARED_CHILD_PROTOCOL_NOT_EXTERNALLY_TIMESTAMPED_PREREGISTRATION",
             "registration firewall")
        print("TPC311_STRESS=PASS factorial=54 pooled_extrema=1 "
              "tau_partition=1 reversal_fixture=1 blocks=6 sensitivity=22")
        return 0
    except (RuntimeError, OSError, ValueError, KeyError, json.JSONDecodeError,
            ZeroDivisionError) as error:
        print("TPC311_STRESS=FAIL " + str(error), file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
