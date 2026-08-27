#!/usr/bin/env python3
"""Hostile semantic mutations for the TPC-274 envelope certificate."""

from __future__ import annotations

import copy
import json
from fractions import Fraction
from pathlib import Path

PROJECT = Path(__file__).resolve().parents[1]
RESULT = PROJECT / "results/tpc274_certificate.json"
STATUS = "NUMERICALLY_CERTIFIED_FINITE_PROJECTED_FROBENIUS_ENVELOPE_GAP"


def fraction(value: object) -> Fraction:
    return Fraction(str(value))


def interval(value: object) -> tuple[Fraction, Fraction]:
    if not isinstance(value, list) or len(value) != 2:
        raise ValueError("interval shape")
    lo, hi = fraction(value[0]), fraction(value[1])
    if lo > hi:
        raise ValueError("interval order")
    return lo, hi


def valid(data: object) -> bool:
    if not isinstance(data, dict):
        return False
    try:
        payload = data["payload"]
        theorem = payload["finite_theorem"]
        firewall = payload["firewall"]
        if data["claim_status"] != STATUS or len(payload["rows"]) != 12:
            return False
        if payload["parameters"]["gap_threshold"] != "G_F/G_perp > 50":
            return False
        if payload["parameters"]["margin_threshold"] != "m_F^2<1/64":
            return False
        if (theorem["total_rows"], theorem["scale_rows"],
                theorem["kernel_pair_rows"], theorem["gap_above_fifty_rows"],
                theorem["envelope_margin_below_one_eighth_rows"]) != (12, 6, 6, 12, 12):
            return False
        if theorem["operator_envelope"] != "PROVED_EXACT_FINITE_INEQUALITY":
            return False
        if firewall["TPC274_FIXED_POWER_CREDIT"] != 0:
            return False
        if firewall["TPC274_CANCELLATION_FREE_ROUTE"] != "INSUFFICIENT_SCOPED":
            return False
        for row in payload["rows"]:
            f2 = fraction(row["projected_frobenius_squared"])
            b2 = fraction(row["beta_norm_squared"])
            env = fraction(row["output_envelope_squared"])
            if f2 <= 0 or b2 <= 0 or env != f2 * b2:
                return False
            gap_lo, _ = interval(row["envelope_to_actual_ratio_interval"])
            _, margin_hi = interval(row["envelope_margin_squared_interval"])
            if gap_lo <= 50 or margin_hi >= Fraction(1, 64):
                return False
            if row["envelope_gap_classification"] != "GAP_ABOVE_FIFTY":
                return False
            if row["envelope_margin_classification"] != "ENVELOPE_MARGIN_BELOW_ONE_EIGHTH":
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
    candidate["payload"]["finite_theorem"]["gap_above_fifty_rows"] = 11
    mutations.append(candidate)

    candidate = copy.deepcopy(original)
    candidate["payload"]["rows"][0]["output_envelope_squared"] = "1/1"
    mutations.append(candidate)

    candidate = copy.deepcopy(original)
    candidate["payload"]["parameters"]["gap_threshold"] = "G_F/G_perp > 1"
    mutations.append(candidate)

    candidate = copy.deepcopy(original)
    candidate["payload"]["finite_theorem"]["operator_envelope"] = "HEURISTIC"
    mutations.append(candidate)

    candidate = copy.deepcopy(original)
    candidate["payload"]["firewall"]["TPC274_FIXED_POWER_CREDIT"] = 1
    mutations.append(candidate)

    if any(valid(item) for item in mutations):
        raise RuntimeError("accepted hostile mutation")
    print("TPC274_ENVELOPE_STRESS=PASS mutations=5 gap_threshold=50 "
          "margin_threshold=1/64 fixed_power_promotion=REJECTED")


if __name__ == "__main__":
    try:
        run()
    except Exception as error:
        print("TPC274_ENVELOPE_STRESS=FAIL " + str(error))
        raise SystemExit(1)
