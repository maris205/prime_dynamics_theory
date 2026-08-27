#!/usr/bin/env python3
"""Hostile semantic mutations for the TPC-272 margin certificate."""

from __future__ import annotations

import copy
import json
from fractions import Fraction
from pathlib import Path

PROJECT = Path(__file__).resolve().parents[1]
RESULT = PROJECT / "results/tpc272_certificate.json"
STATUS = "PROVED_CONDITIONAL_CORRELATION_MARGIN_TO_RADIUS_BUDGET_COMPILER"


def need(condition: bool, message: str) -> None:
    if type(condition) is not bool or not condition:
        raise RuntimeError(message)


def bounds(value: object) -> tuple[Fraction, Fraction]:
    need(isinstance(value, list) and len(value) == 2, "interval")
    return Fraction(str(value[0])), Fraction(str(value[1]))


def valid(data: object) -> bool:
    if not isinstance(data, dict):
        return False
    try:
        p = data["payload"]
        rows = p["rows"]
        d = p["dyadic_margin_ratios"]
        f = p["firewall"]
        if data["claim_status"] != STATUS or len(rows) != 9 or len(d) != 4:
            return False
        if p["conditional_theorem"]["strict_gate"] != "sigma_c-eta>1/400":
            return False
        if p["converse"]["status"] != "PROVED_EXACT":
            return False
        if f["TPC272_FIXED_POWER_CREDIT"] != 0:
            return False
        if f["TPC272_SOURCE_LEVEL_MARGIN"] != "OPEN_ASYMPTOTIC":
            return False
        if f["TPC272_FULL_GATE_B"] != "OPEN":
            return False
        for row in rows:
            lo, hi = bounds(row["margin_sixth_interval"])
            alo, ahi = bounds(row["amplification_interval"])
            if not (0 < lo <= hi and 0 < alo <= ahi and
                    row["phase"] == "NEGATIVE_REAL_AXIS" and
                    row["phase_sign_locked"] is True):
                return False
        if d[1]["margin_ratio_classification"] != "MARGIN_COLLAPSE_BELOW_ONE_THIRTY_SECOND":
            return False
        lo, hi = bounds(d[1]["margin_sixth_ratio_interval"])
        if not (hi < Fraction(1, 32**6) and d[1]["phase_sign_preserved"] is True):
            return False
        return True
    except (KeyError, TypeError, ValueError, IndexError, ZeroDivisionError):
        return False


def run() -> None:
    original = json.loads(RESULT.read_text(encoding="utf-8"))
    need(valid(original), "baseline invalid")
    mutations = []
    candidate = copy.deepcopy(original)
    candidate["payload"]["dyadic_margin_ratios"][1]["margin_sixth_ratio_interval"][1] = "1/1"
    mutations.append(candidate)
    candidate = copy.deepcopy(original)
    candidate["payload"]["dyadic_margin_ratios"][1]["phase_sign_preserved"] = False
    mutations.append(candidate)
    candidate = copy.deepcopy(original)
    candidate["payload"]["conditional_theorem"]["strict_gate"] = "sigma_c-eta>=1/400"
    mutations.append(candidate)
    candidate = copy.deepcopy(original)
    candidate["payload"]["firewall"]["TPC272_FIXED_POWER_CREDIT"] = 1
    mutations.append(candidate)
    candidate = copy.deepcopy(original)
    candidate["payload"]["converse"]["status"] = "HEURISTIC"
    mutations.append(candidate)
    need(all(not valid(item) for item in mutations), "accepted hostile mutation")
    print("TPC272_MARGIN_STRESS=PASS mutations=5 "
          "collapse_threshold=1/32^6 phase_lock=REQUIRED "
          "asymptotic_promotion=REJECTED")


if __name__ == "__main__":
    try:
        run()
    except Exception as exc:
        print("TPC272_MARGIN_STRESS=FAIL " + str(exc))
        raise SystemExit(1)
