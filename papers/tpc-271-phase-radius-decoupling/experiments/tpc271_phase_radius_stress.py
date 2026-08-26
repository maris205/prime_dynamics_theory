#!/usr/bin/env python3
"""Adversarial metadata and threshold stress audit for TPC-271."""

from __future__ import annotations

import argparse
import copy
import json
from fractions import Fraction
from pathlib import Path

PROJECT = Path(__file__).resolve().parents[1]
RESULT = PROJECT / "results/tpc271_certificate.json"
STATUS = "NUMERICALLY_CERTIFIED_FINITE_PHASE_RADIUS_DECOUPLING_AUDIT"


def need(condition: bool, message: str) -> None:
    if type(condition) is not bool or not condition:
        raise RuntimeError(message)


def bounds(values: object) -> tuple[Fraction, Fraction]:
    need(isinstance(values, list) and len(values) == 2, "interval shape")
    return Fraction(str(values[0])), Fraction(str(values[1]))


def valid(data: object) -> bool:
    if not isinstance(data, dict):
        return False
    try:
        p = data["payload"]
        t = p["finite_theorem"]
        f = p["firewall"]
        d = p["dyadic_lane_ratios"]
        expected_source = [
            "SOURCE_DROP_BELOW_ONE_HALF", "SOURCE_DROP_BELOW_ONE_EIGHTH",
            "SOURCE_DROP_BELOW_ONE_HALF", "SOURCE_RISE_ABOVE_ONE",
        ]
        expected_output = [
            "OUTPUT_DROP_BELOW_THREE_QUARTERS", "OUTPUT_RISE_ABOVE_230",
            "OUTPUT_RISE_ABOVE_15", "OUTPUT_DROP_BELOW_THREE_QUARTERS",
        ]
        expected_radius = [
            "RADIUS_DROP_BELOW_ONE_QUARTER", "RADIUS_RISE_ABOVE_23",
            "RADIUS_RISE_ABOVE_SEVEN",
            "RADIUS_DROP_BETWEEN_THREE_QUARTERS_AND_ONE",
        ]
        threshold_shape = (
            bounds(d[0]["source_lane_ratio_interval"])[1] < Fraction(1, 2) and
            bounds(d[0]["output_lane_ratio_interval"])[1] < Fraction(3, 4) and
            bounds(d[0]["radius_ratio_interval"])[1] < Fraction(1, 4) and
            bounds(d[1]["source_lane_ratio_interval"])[1] < Fraction(1, 8) and
            bounds(d[1]["output_lane_ratio_interval"])[0] > Fraction(230) and
            bounds(d[1]["radius_ratio_interval"])[0] > Fraction(23) and
            bounds(d[2]["source_lane_ratio_interval"])[1] < Fraction(1, 2) and
            bounds(d[2]["output_lane_ratio_interval"])[0] > Fraction(15) and
            bounds(d[2]["radius_ratio_interval"])[0] > Fraction(7) and
            bounds(d[3]["source_lane_ratio_interval"])[0] > Fraction(1) and
            bounds(d[3]["output_lane_ratio_interval"])[1] < Fraction(3, 4) and
            bounds(d[3]["radius_ratio_interval"])[0] > Fraction(3, 4) and
            bounds(d[3]["radius_ratio_interval"])[1] < Fraction(1)
        )
        return (
            data["claim_status"] == STATUS and
            p["schema"] == "TPC271_PHASE_RADIUS_DECOUPLING_CERTIFICATE_V1" and
            t["dyadic_radius_pattern"] == "DROP_RISE_RISE_DROP" and
            t["phase_sign_pattern"] == "ALL_NEGATIVE_REAL_AXIS" and
            len(d) == 4 and
            all(x["phase_sign_preserved"] is True for x in d) and
            [x["source_classification"] for x in d] == expected_source and
            [x["output_classification"] for x in d] == expected_output and
            [x["radius_classification"] for x in d] == expected_radius and
            threshold_shape and
            f["TPC271_FIXED_POWER_CREDIT"] == 0 and
            f["TPC271_SOURCE_LEVEL_RADIUS"] == "OPEN_ASYMPTOTIC" and
            f["TPC271_SOURCE_LEVEL_SIGNED_PHASE"] == "OPEN_ASYMPTOTIC"
        )
    except (KeyError, TypeError, ValueError, IndexError):
        return False


def run() -> None:
    data = json.loads(RESULT.read_text(encoding="utf-8"))
    need(valid(data), "base semantics")
    ratios = data["payload"]["dyadic_lane_ratios"]
    expected = [
        (Fraction(1, 2), Fraction(3, 4), Fraction(1, 4)),
        (Fraction(1, 8), Fraction(230), Fraction(23)),
        (Fraction(1, 2), Fraction(15), Fraction(7)),
        (Fraction(1), Fraction(3, 4), Fraction(3, 4)),
    ]
    for item, (source_cut, output_cut, radius_cut) in zip(ratios, expected):
        source = bounds(item["source_lane_ratio_interval"])
        output = bounds(item["output_lane_ratio_interval"])
        radius = bounds(item["radius_ratio_interval"])
        if item["label"] == "192->384":
            need(source[0] > source_cut and output[1] < output_cut and
                 radius[0] > radius_cut and radius[1] < 1,
                 "last dyadic thresholds")
        elif item["label"] == "96->192":
            need(source[1] < source_cut and output[0] > output_cut and
                 radius[0] > radius_cut, "output-spike thresholds")
        elif item["label"] == "128->256":
            need(source[1] < source_cut and output[0] > output_cut and
                 radius[0] > radius_cut, "second-spike thresholds")
        else:
            need(source[1] < source_cut and output[1] < output_cut and
                 radius[1] < radius_cut, "first-drop thresholds")
    for item in data["payload"]["base_rows"] + data["payload"]["profile_rows"]:
        need(item["phase"] == "NEGATIVE_REAL_AXIS", "phase mutation")
        need(bounds(item["residual_scalar_interval"])[1] < 0,
             "signed scalar not negative")
    mutations = []
    candidate = copy.deepcopy(data)
    candidate["payload"]["dyadic_lane_ratios"][1]["output_lane_ratio_interval"] = ["0", "1"]
    mutations.append(candidate)
    candidate = copy.deepcopy(data)
    candidate["payload"]["dyadic_lane_ratios"][1]["phase_sign_preserved"] = False
    mutations.append(candidate)
    candidate = copy.deepcopy(data)
    candidate["payload"]["firewall"]["TPC271_SOURCE_LEVEL_RADIUS"] = "PROVED"
    mutations.append(candidate)
    need(valid(data), "canonical validity")
    need(all(not valid(item) for item in mutations), "accepted stress mutation")
    print("TPC271_PHASE_RADIUS_STRESS=PASS "
          f"dyadic_rows={len(ratios)} output_spike=96->192 "
          "phase_lock=ALL_NEGATIVE_REAL_AXIS mutations=3 "
          "asymptotic_promotion=REJECTED")


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
        print("TPC271_PHASE_RADIUS_STRESS=FAIL " + str(exc))
        raise SystemExit(1)
