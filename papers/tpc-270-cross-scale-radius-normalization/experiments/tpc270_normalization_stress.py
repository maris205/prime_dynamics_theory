#!/usr/bin/env python3
"""Adversarial semantic checks for the TPC-270 normalization certificate."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

PROJECT = Path(__file__).resolve().parents[1]
RESULT = PROJECT / "results/tpc270_certificate.json"
STATUS = "NUMERICALLY_CERTIFIED_FINITE_CROSS_SCALE_RADIUS_NORMALIZATION_AUDIT"


def need(condition: bool, message: str) -> None:
    if type(condition) is not bool or not condition:
        raise RuntimeError(message)


def run() -> None:
    data = json.loads(RESULT.read_text(encoding="utf-8"))
    payload = data["payload"]
    theorem = payload["finite_theorem"]
    firewall = payload["firewall"]
    need(data["claim_status"] == STATUS, "status")
    need(payload["schema"] ==
         "TPC270_CROSS_SCALE_RADIUS_NORMALIZATION_CERTIFICATE_V1", "schema")
    need((theorem["base_rows"], theorem["profile_control_rows"],
          theorem["dyadic_ratio_rows"], theorem["adjacent_ratio_rows"],
          theorem["profile_ratio_rows"]) == (6, 3, 4, 5, 3), "counts")
    need(theorem["dyadic_pattern"] == "DROP_RISE_RISE_DROP", "pattern")
    need(payload["parameters"]["endpoint_baseline_exponent"] == "5/3",
         "endpoint exponent")
    need(payload["parameters"]["normalization"] ==
         "Xi=(R_squared)^3/N^10=(R/N^(5/3))^6", "normalization")
    schedule = {64: 4, 96: 4, 128: 4, 192: 5, 256: 5, 384: 5}
    for row in payload["base_rows"] + payload["profile_rows"]:
        need(row["comparison_cutoff_z"] == schedule[row["scale"]],
             "cutoff schedule")
        lo, hi = (float(x) for x in row["endpoint_normalized_sixth_interval"])
        need(0 < lo <= hi and row["positive_radius_certified"] is True,
             "normalized interval")
        need(row["normalization_identity"] ==
             "Xi=(R_squared)^3/N^10=(R/N^(5/3))^6", "identity")
    dyadic = payload["dyadic_ratios"]
    need([row["label"] for row in dyadic] ==
         ["64->128", "96->192", "128->256", "192->384"], "dyadic labels")
    expected = ["DROP_BELOW_ONE_QUARTER", "RISE_ABOVE_SIXTEEN",
                "RISE_ABOVE_SEVEN", "DROP_BETWEEN_THREE_QUARTERS_AND_ONE"]
    need([row["classification"] for row in dyadic] == expected,
         "dyadic classifications")
    bounds = ((0, 0.25), (16, float("inf")), (7, float("inf")), (0.75, 1))
    for row, (lower, upper) in zip(dyadic, bounds):
        lo, hi = (float(x) for x in row["ratio_interval"])
        need(0 < lo <= hi and lo > lower and hi < upper, "ratio separation")
    for row in payload["profile_ratios"]:
        lo, hi = (float(x) for x in row["ratio_interval"])
        need(0.5 < lo <= hi < 0.75, "profile control band")
    need(firewall["TPC270_ENDPOINT_NORMALIZATION"] ==
         "PROVED_EXACT_FINITE_IDENTITY", "identity firewall")
    need(firewall["TPC270_CROSS_SCALE_VARIATION"] ==
         "NUMERICALLY_CERTIFIED_FINITE", "variation firewall")
    need(firewall["TPC270_SOURCE_LEVEL_RADIUS"] == "OPEN_ASYMPTOTIC" and
         firewall["TPC270_FIXED_POWER_CREDIT"] == 0 and
         firewall["TPC270_ARITHMETIC_ADVANCE"] == "NO" and
         firewall["TPC270_FULL_GATE_B"] == "OPEN" and
         firewall["TPC270_TWIN_PRIME_RESULT"] == "NONE", "claim firewall")
    print("TPC270_NORMALIZATION_STRESS=PASS "
          f"base_rows={len(payload['base_rows'])} dyadic_rows={len(dyadic)} "
          "pattern=DROP_RISE_RISE_DROP profile_band=SEPARATED "
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
        print("TPC270_NORMALIZATION_STRESS=FAIL " + str(exc))
        raise SystemExit(1)
