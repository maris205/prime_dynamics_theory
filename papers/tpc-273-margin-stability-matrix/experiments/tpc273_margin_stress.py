#!/usr/bin/env python3
"""Adversarial semantic stress for the TPC-273 stability matrix."""

from __future__ import annotations

import copy
import json
from fractions import Fraction
from pathlib import Path

PROJECT = Path(__file__).resolve().parents[1]
RESULT = PROJECT / "results/tpc273_certificate.json"
STATUS = "NUMERICALLY_CERTIFIED_FINITE_MARGIN_STABILITY_OBSTRUCTION"


def bounds(value: object) -> tuple[Fraction, Fraction]:
    if not isinstance(value, list) or len(value) != 2:
        raise ValueError("interval")
    return Fraction(str(value[0])), Fraction(str(value[1]))


def valid(data: object) -> bool:
    if not isinstance(data, dict):
        return False
    try:
        p = data["payload"]
        t = p["finite_theorem"]
        f = p["firewall"]
        if data["claim_status"] != STATUS or len(p["cases"]) != 32:
            return False
        if p["parameters"]["margin_squared_thresholds"] != {"low": "1/64", "high": "1/16"}:
            return False
        if (t["low_margin_cases"], t["middle_margin_cases"],
                t["high_margin_cases"], t["negative_phase_cases"],
                t["positive_phase_cases"]) != (12, 11, 9, 30, 2):
            return False
        if t["cutoff_flip_transitions"] != 2 or len(p["transitions"]) != 3:
            return False
        if f["TPC273_FIXED_POWER_CREDIT"] != 0 or f["TPC273_FULL_GATE_B"] != "OPEN":
            return False
        if f["TPC273_SOURCE_LEVEL_MARGIN"] != "OPEN_ASYMPTOTIC":
            return False
        counts = {name: 0 for name in ("MARGIN_BELOW_ONE_EIGHTH",
                                       "MARGIN_MIDDLE_BAND",
                                       "MARGIN_ABOVE_ONE_QUARTER")}
        phases = {name: 0 for name in ("NEGATIVE_REAL_AXIS", "POSITIVE_REAL_AXIS",
                                       "CROSSES_ZERO")}
        for row in p["cases"]:
            lo, hi = bounds(row["margin_squared_interval"])
            if not (0 < lo <= hi and row["classification"] in
                    ("MARGIN_BELOW_ONE_EIGHTH", "MARGIN_MIDDLE_BAND",
                     "MARGIN_ABOVE_ONE_QUARTER")):
                return False
            expected = ("MARGIN_BELOW_ONE_EIGHTH" if hi < Fraction(1, 64)
                        else "MARGIN_ABOVE_ONE_QUARTER" if lo > Fraction(1, 16)
                        else "MARGIN_MIDDLE_BAND")
            if row["classification"] != expected:
                return False
            if row["phase"] not in phases:
                return False
            counts[row["classification"]] += 1
            phases[row["phase"]] += 1
        if counts != {"MARGIN_BELOW_ONE_EIGHTH": 12,
                      "MARGIN_MIDDLE_BAND": 11,
                      "MARGIN_ABOVE_ONE_QUARTER": 9}:
            return False
        if phases != {"NEGATIVE_REAL_AXIS": 30, "POSITIVE_REAL_AXIS": 2,
                      "CROSSES_ZERO": 0}:
            return False
        first, second = p["transitions"][:2]
        return (first["low_classification"] == "MARGIN_MIDDLE_BAND" and
                first["high_classification"] == "MARGIN_ABOVE_ONE_QUARTER" and
                second["low_classification"] == "MARGIN_MIDDLE_BAND" and
                second["high_classification"] == "MARGIN_BELOW_ONE_EIGHTH")
    except (KeyError, TypeError, ValueError, IndexError):
        return False


def run() -> None:
    original = json.loads(RESULT.read_text(encoding="utf-8"))
    if not valid(original):
        raise RuntimeError("baseline invalid")
    mutations = []
    candidate = copy.deepcopy(original)
    candidate["payload"]["cases"][0]["classification"] = "MARGIN_ABOVE_ONE_QUARTER"
    mutations.append(candidate)
    candidate = copy.deepcopy(original)
    candidate["payload"]["transitions"][0]["high_classification"] = "MARGIN_MIDDLE_BAND"
    mutations.append(candidate)
    candidate = copy.deepcopy(original)
    candidate["payload"]["firewall"]["TPC273_FIXED_POWER_CREDIT"] = 1
    mutations.append(candidate)
    candidate = copy.deepcopy(original)
    candidate["payload"]["finite_theorem"]["positive_phase_cases"] = 0
    mutations.append(candidate)
    candidate = copy.deepcopy(original)
    candidate["payload"]["parameters"]["margin_squared_thresholds"]["low"] = "1/32"
    mutations.append(candidate)
    if any(valid(item) for item in mutations):
        raise RuntimeError("accepted hostile mutation")
    print("TPC273_MARGIN_STRESS=PASS mutations=5 "
          "thresholds=1/64,1/16 phase_flip=2 asymptotic_promotion=REJECTED")


if __name__ == "__main__":
    try:
        run()
    except Exception as exc:
        print("TPC273_MARGIN_STRESS=FAIL " + str(exc))
        raise SystemExit(1)
