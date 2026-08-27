#!/usr/bin/env python3
"""Hostile schema and claim mutation audit for TPC-277."""

from __future__ import annotations

import copy
import json
import sys
from fractions import Fraction
from pathlib import Path

PROJECT = Path(__file__).resolve().parents[1]
RESULT = PROJECT / "results/tpc277_certificate.json"
STATUS = "PROVED_EXACT_UNIVERSAL_FOUR_PACKET_GAIN_FLOOR_PLUS_NUMERICALLY_CERTIFIED_SOURCE_SCAN"


def valid(data: object) -> bool:
    try:
        if not isinstance(data, dict) or data.get("claim_status") != STATUS:
            return False
        payload = data["payload"]
        theorem = payload["finite_theorem"]
        universal = payload["universal_theorem"]
        rows = payload["rows"]
        if universal["sharp_general_floor"] != "1/4" or \
                universal["sharp_signed_floor"] != "1":
            return False
        if theorem["total_rows"] != 8 or theorem["gain_above_one_rows"] != 8:
            return False
        if theorem["minimum_gain_target_status"] != \
                "REFUTED_SCOPED_FINITE":
            return False
        if len(rows) != 8:
            return False
        for row in rows:
            gain = Fraction(row["gain_interval"][0])
            high = Fraction(row["gain_interval"][1])
            if gain <= 1 or high < gain:
                return False
            if row["gain_above_one"] is not True:
                return False
        return payload["firewall"]["TPC277_FIXED_POWER_CREDIT"] == 0
    except (KeyError, TypeError, ValueError, ZeroDivisionError):
        return False


def run() -> None:
    original = json.loads(RESULT.read_text(encoding="utf-8"))
    if not valid(original):
        raise RuntimeError("baseline invalid")
    mutations = []
    candidate = copy.deepcopy(original)
    candidate["payload"]["universal_theorem"]["sharp_general_floor"] = "1/2"
    mutations.append(candidate)
    candidate = copy.deepcopy(original)
    candidate["payload"]["finite_theorem"]["gain_above_one_rows"] = 7
    mutations.append(candidate)
    candidate = copy.deepcopy(original)
    candidate["payload"]["rows"][0]["gain_above_one"] = False
    mutations.append(candidate)
    candidate = copy.deepcopy(original)
    candidate["payload"]["firewall"]["TPC277_FIXED_POWER_CREDIT"] = 1
    mutations.append(candidate)
    if any(valid(item) for item in mutations):
        raise RuntimeError("accepted hostile mutation")
    print("TPC277_GAIN_STRESS=PASS mutations=4 universal_floor=REJECTED "
          "counts=REJECTED fixed_power_promotion=REJECTED")


if __name__ == "__main__":
    try:
        run()
    except Exception as error:
        print("TPC277_GAIN_STRESS=FAIL " + str(error), file=sys.stderr)
        raise SystemExit(1)
