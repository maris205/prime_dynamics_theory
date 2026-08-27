#!/usr/bin/env python3
"""Hostile mutation audit for the TPC-278 stability certificate."""

from __future__ import annotations

import copy
import json
import sys
from pathlib import Path

PROJECT = Path(__file__).resolve().parents[1]
RESULT = PROJECT / "results/tpc278_certificate.json"
STATUS = "NUMERICALLY_CERTIFIED_FINITE_CROSS_SCALE_GAIN_STABILITY_OBSTRUCTION"


def valid(data: object) -> bool:
    try:
        if not isinstance(data, dict) or data["claim_status"] != STATUS:
            return False
        payload = data["payload"]
        theorem = payload["finite_theorem"]
        rows = payload["rows"]
        if theorem["total_rows"] != 12 or theorem["natural_controls"] != 3:
            return False
        if theorem["negative_cross_rows"] != 8 or \
                theorem["positive_cross_rows"] != 4 or \
                theorem["shell_or_clock_sign_flips"] != 4:
            return False
        if payload["firewall"]["TPC278_FIXED_POWER_CREDIT"] != 0:
            return False
        if len(rows) != 12 or \
                sum(row["cross_sign"] == "NEGATIVE_CROSS" for row in rows) != 8 or \
                sum(row["cross_sign"] == "POSITIVE_CROSS" for row in rows) != 4:
            return False
        return all(
            row["cross_sign"] in {"NEGATIVE_CROSS", "POSITIVE_CROSS"}
            for row in rows)
    except (KeyError, TypeError, ValueError):
        return False


def run() -> None:
    original = json.loads(RESULT.read_text(encoding="utf-8"))
    if not valid(original):
        raise RuntimeError("baseline invalid")
    mutations = []
    candidate = copy.deepcopy(original)
    candidate["payload"]["finite_theorem"]["positive_cross_rows"] = 3
    mutations.append(candidate)
    candidate = copy.deepcopy(original)
    candidate["payload"]["finite_theorem"]["shell_or_clock_sign_flips"] = 0
    mutations.append(candidate)
    candidate = copy.deepcopy(original)
    candidate["payload"]["rows"][2]["cross_sign"] = "NEGATIVE_CROSS"
    mutations.append(candidate)
    candidate = copy.deepcopy(original)
    candidate["payload"]["firewall"]["TPC278_FIXED_POWER_CREDIT"] = 1
    mutations.append(candidate)
    if any(valid(item) for item in mutations):
        raise RuntimeError("accepted hostile mutation")
    print("TPC278_STABILITY_STRESS=PASS mutations=4 sign_census=REJECTED "
          "flip_count=REJECTED fixed_power_promotion=REJECTED")


if __name__ == "__main__":
    try:
        run()
    except Exception as error:
        print("TPC278_STABILITY_STRESS=FAIL " + str(error), file=sys.stderr)
        raise SystemExit(1)
