#!/usr/bin/env python3
"""Adversarial semantic checks for the TPC-269 transfer certificate."""

from __future__ import annotations

import argparse
import json
import math
from pathlib import Path

PROJECT = Path(__file__).resolve().parents[1]
RESULT = PROJECT / "results/tpc269_certificate.json"
THRESHOLD = 1.0 / 16.0


def need(condition: bool, message: str) -> None:
    if type(condition) is not bool or not condition:
        raise RuntimeError(message)


def run() -> None:
    data = json.loads(RESULT.read_text(encoding="utf-8"))
    payload = data["payload"]
    cases = payload["cases"]
    need(data["claim_status"] == "NUMERICALLY_CERTIFIED_FINITE_GROWING_CUTOFF_PROFILE_TRANSFER", "status")
    need(len(cases) == 12, "case count")
    scales = {64: 4, 96: 4, 128: 4, 192: 5, 256: 5, 384: 5}
    for case in cases:
        need(case["comparison_cutoff_z"] == scales[case["scale"]], "growing schedule")
        lo, hi = (float(x) for x in case["rho_squared_interval"])
        need(0 < lo <= hi, "interval order")
        if case["classification"] == "CONTRACTION":
            need(hi < THRESHOLD and case["quarter_contraction"] is True, "contraction")
        elif case["classification"] == "OBSTRUCTION":
            need(lo > THRESHOLD and case["certified_obstruction"] is True, "obstruction")
        else:
            raise RuntimeError("unresolved row")
    def find(theta: str) -> dict:
        matches = [case for case in cases if case["profile_theta"] == theta]
        need(len(matches) == 1, "profile row missing")
        return matches[0]
    need(find("9/10")["classification"] == "OBSTRUCTION", "profile obstruction")
    need(find("24/25")["classification"] == "CONTRACTION", "profile contraction")
    need(find("1/1")["classification"] == "CONTRACTION", "profile endpoint")
    base = [c for c in cases if c["role"] == "GROWING_CUTOFF_BASE"]
    need(len(base) == 6 and any(c["classification"] == "OBSTRUCTION" for c in base), "base obstruction")
    margins = []
    for c in cases:
        lo, hi = (float(x) for x in c["rho_squared_interval"])
        margins.append(min(abs(lo - THRESHOLD), abs(hi - THRESHOLD)))
    need(min(margins) > 1e-5, "threshold margin")
    need(payload["finite_theorem"]["matched_profile_flip"] == "9/10_OBSTRUCTION_TO_24/25_CONTRACTION", "flip ledger")
    need(payload["firewall"]["TPC269_GROWING_UNIFORMITY"] == "OPEN_ASYMPTOTIC", "growth firewall")
    print("TPC269_PROFILE_STRESS=PASS "
          f"cases={len(cases)} schedule_rows={len(base)} "
          "profile_flip=YES threshold_margin=SEPARATED "
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
        print("TPC269_PROFILE_STRESS=FAIL " + str(exc))
        raise SystemExit(1)
