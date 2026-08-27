#!/usr/bin/env python3
"""Hostile semantic mutations for the TPC-275 certificate."""

from __future__ import annotations

import copy
import json
from fractions import Fraction
from pathlib import Path

PROJECT = Path(__file__).resolve().parents[1]
RESULT = PROJECT / "results/tpc275_certificate.json"
STATUS = "NUMERICALLY_CERTIFIED_FINITE_SIGNED_FOUR_PACKET_REASSEMBLY_AUDIT"


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
        theorem = payload["finite_theorem"]
        firewall = payload["firewall"]
        rows = payload["rows"]
        if data["claim_status"] != STATUS or len(rows) != 12:
            return False
        if payload["parameters"]["diagonal_ratio_threshold"] != "1 < D/G < 12/5":
            return False
        if payload["parameters"]["diagonal_margin_threshold"] != "m_D^2<1/16":
            return False
        if theorem != {
            "claim": "literal signed packet cross terms sharpen but do not close the margin route",
            "diagonal_margin_below_quarter_rows": 12,
            "diagonal_ratio_between_rows": 12,
            "dft_parseval_rows": 12,
            "frobenius_above_fifty_rows": 12,
            "kernel_pair_rows": 6,
            "net_cross_negative_rows": 12,
            "polarization_probe_rows": 72,
            "scale_rows": 6,
            "status": "NUMERICALLY_CERTIFIED_FINITE",
            "total_rows": 12,
        }:
            return False
        if firewall["TPC275_FIXED_POWER_CREDIT"] != 0:
            return False
        if firewall["TPC275_DIAGONAL_ROUTE"] != "INSUFFICIENT_SCOPED":
            return False
        for row in rows:
            gram = [[frac(value) for value in line] for line in row["gram"]]
            diagonal = frac(row["diagonal_packet_energy"])
            signed = frac(row["signed_output_energy"])
            cross = frac(row["signed_cross_sum"])
            if any(gram[j][k] != gram[k][j] for j in range(4) for k in range(4)):
                return False
            if diagonal != sum(gram[j][j] for j in range(4)):
                return False
            if signed != sum(gram[j][k] for j in range(4) for k in range(4)):
                return False
            if cross != signed - diagonal or cross >= 0:
                return False
            ratio = frac(row["diagonal_to_signed_ratio"])
            f_ratio = frac(row["frobenius_to_signed_ratio"])
            if not (Fraction(1) < ratio < Fraction(12, 5) and f_ratio > 50):
                return False
            if interval(row["diagonal_margin_squared_interval"])[1] >= Fraction(1, 16):
                return False
            modes = [frac(row["dft_mode_energy"][str(k)]) for k in range(4)]
            if sum(modes) != diagonal or modes[0] * 4 != signed:
                return False
            if row["dft_parseval_identity"] is not True or row["dft_mode_zero_identity"] is not True:
                return False
            if row["net_cross_term_classification"] != "NEGATIVE_NET_CROSS_TERM":
                return False
            if row["diagonal_gain_classification"] != "BETWEEN_1_AND_12_OVER_5":
                return False
            if row["diagonal_margin_classification"] != "BELOW_QUARTER_MARGIN":
                return False
            for probe in row["polarization"]:
                if (frac(probe["plus_energy"]) - frac(probe["minus_energy"])) != 4 * frac(probe["recovered_cross_term"]):
                    return False
                if probe["recovered_cross_term"] != probe["gram_cross_term"] or probe["identity_holds"] is not True:
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
    candidate["payload"]["finite_theorem"]["net_cross_negative_rows"] = 11
    mutations.append(candidate)

    candidate = copy.deepcopy(original)
    candidate["payload"]["rows"][0]["signed_cross_sum"] = "1/1"
    mutations.append(candidate)

    candidate = copy.deepcopy(original)
    candidate["payload"]["rows"][0]["dft_mode_energy"]["0"] = "1/1"
    mutations.append(candidate)

    candidate = copy.deepcopy(original)
    candidate["payload"]["parameters"]["diagonal_ratio_threshold"] = "D/G <= 100"
    mutations.append(candidate)

    candidate = copy.deepcopy(original)
    candidate["payload"]["firewall"]["TPC275_FIXED_POWER_CREDIT"] = 1
    mutations.append(candidate)

    candidate = copy.deepcopy(original)
    candidate["payload"]["rows"][0]["polarization"][0]["identity_holds"] = False
    mutations.append(candidate)

    if any(valid(item) for item in mutations):
        raise RuntimeError("accepted hostile mutation")
    print("TPC275_REASSEMBLY_STRESS=PASS mutations=6 cross_sign=REJECTED "
          "dft_mutation=REJECTED polarization_mutation=REJECTED "
          "fixed_power_promotion=REJECTED")


if __name__ == "__main__":
    try:
        run()
    except Exception as error:
        print("TPC275_REASSEMBLY_STRESS=FAIL " + str(error))
        raise SystemExit(1)
