#!/usr/bin/env python3
"""Hostile mutation audit for the TPC-276 signed-gain budget ledger."""

from __future__ import annotations

import copy
import json
from fractions import Fraction
from pathlib import Path

PROJECT = Path(__file__).resolve().parents[1]
RESULT = PROJECT / "results/tpc276_certificate.json"
STATUS = "PROVED_CONDITIONAL_SIGNED_GAIN_STRICT_ENDPOINT_BUDGET_PLUS_FINITE_TRANSFER"


def frac(value: object) -> Fraction:
    if not isinstance(value, str):
        raise ValueError("fraction text")
    return Fraction(value)


def interval(value: object) -> tuple[Fraction, Fraction]:
    if not isinstance(value, list) or len(value) != 2:
        raise ValueError("interval shape")
    lo, hi = frac(value[0]), frac(value[1])
    if lo > hi:
        raise ValueError("interval order")
    return lo, hi


def valid(data: object) -> bool:
    if not isinstance(data, dict):
        return False
    try:
        payload = data["payload"]
        rows = payload["rows"]
        theorem = payload["finite_theorem"]
        firewall = payload["firewall"]
        if data["claim_status"] != STATUS or len(rows) != 12:
            return False
        if payload["budget_compiler"]["strict_target_condition"] != \
                "sigma-eta_eff>1/400":
            return False
        if theorem["signed_above_quarter_rows"] != 3 or \
                theorem["signed_above_eighth_rows"] != 5:
            return False
        if firewall["TPC276_FIXED_POWER_CREDIT"] != 0:
            return False
        for row in rows:
            gain = frac(row["signed_gain_factor"])
            diagonal = interval(row["diagonal_margin_squared_interval"])
            signed = interval(row["signed_margin_squared_interval"])
            if gain <= 1 or signed != (gain * diagonal[0], gain * diagonal[1]):
                return False
            if row["signed_gain_identity"] != "m^2=(D/G)m_D^2":
                return False
            if row["finite_transfer_exact"] is not True:
                return False
            if row["signed_quarter_classification"] == "ABOVE_THRESHOLD" and \
                    signed[0] <= Fraction(1, 16):
                return False
        return True
    except (KeyError, TypeError, ValueError, ZeroDivisionError):
        return False


def run() -> None:
    original = json.loads(RESULT.read_text(encoding="utf-8"))
    if not valid(original):
        raise RuntimeError("baseline invalid")
    mutations = []

    candidate = copy.deepcopy(original)
    candidate["payload"]["rows"][0]["signed_gain_factor"] = "1/1"
    mutations.append(candidate)

    candidate = copy.deepcopy(original)
    candidate["payload"]["rows"][0]["signed_margin_squared_interval"][0] = "0/1"
    mutations.append(candidate)

    candidate = copy.deepcopy(original)
    candidate["payload"]["finite_theorem"]["signed_above_quarter_rows"] = 4
    mutations.append(candidate)

    candidate = copy.deepcopy(original)
    candidate["payload"]["budget_compiler"]["strict_target_condition"] = \
        "sigma-eta_D+gamma>1/400"
    mutations.append(candidate)

    candidate = copy.deepcopy(original)
    candidate["payload"]["firewall"]["TPC276_FIXED_POWER_CREDIT"] = 1
    mutations.append(candidate)

    candidate = copy.deepcopy(original)
    candidate["payload"]["rows"][0]["signed_gain_identity"] = "m^2=m_D^2"
    mutations.append(candidate)

    if any(valid(item) for item in mutations):
        raise RuntimeError("accepted hostile mutation")
    print("TPC276_BUDGET_STRESS=PASS mutations=6 gain_identity=REJECTED "
          "threshold_counts=REJECTED budget_condition=REJECTED "
          "fixed_power_promotion=REJECTED")


if __name__ == "__main__":
    try:
        run()
    except Exception as error:
        print("TPC276_BUDGET_STRESS=FAIL " + str(error))
        raise SystemExit(1)
