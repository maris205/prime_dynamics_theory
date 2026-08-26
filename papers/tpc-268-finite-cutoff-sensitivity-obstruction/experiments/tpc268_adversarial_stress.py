#!/usr/bin/env python3
"""Hostile semantic checks for the TPC-268 finite obstruction."""

from __future__ import annotations

import argparse
import json
from pathlib import Path


PROJECT = Path(__file__).resolve().parents[1]
RESULT = PROJECT / "results/tpc268_certificate.json"
THRESHOLD = 1.0 / 16.0


def need(condition: bool, message: str) -> None:
    if type(condition) is not bool or not condition:
        raise RuntimeError(message)


def run() -> None:
    data = json.loads(RESULT.read_text(encoding="utf-8"))
    cases = data["payload"]["cases"]
    need(len(cases) == 16, "case count")
    controls = [c for c in cases if c["role"] == "CONTROL_Z2"]
    obstructions = [c for c in cases if c["classification"] == "OBSTRUCTION"]
    need(len(controls) == 6 and len(obstructions) == 6, "role counts")
    for case in cases:
        lo, hi = (float(value) for value in case["rho_squared_interval"])
        need(0.0 < lo <= hi, "interval order")
        if case["classification"] == "CONTRACTION":
            need(hi < THRESHOLD and case["certified_obstruction"] is False,
                 "contraction threshold")
        elif case["classification"] == "OBSTRUCTION":
            need(lo > THRESHOLD and case["certified_obstruction"] is True,
                 "obstruction threshold")
        else:
            need(False, "unresolved classification")

    def find(scale: int, height: int, q0: int, exponent: int, z: int) -> dict:
        matches = [c for c in cases
                   if (c["scale"], c["H"], c["Q"], c["kernel_exponent"],
                       c["comparison_cutoff_z"]) ==
                   (scale, height, q0, exponent, z)]
        need(len(matches) == 1, "missing designated row")
        return matches[0]

    baseline = find(64, 15, 4, 1, 2)
    cutoff = find(64, 15, 4, 1, 3)
    need(baseline["classification"] == "CONTRACTION" and
         cutoff["classification"] == "OBSTRUCTION",
         "matched cutoff flip")
    for height in (13, 17):
        need(find(64, height, 4, 1, 3)["classification"] == "OBSTRUCTION",
             "clock neighborhood")
    need(find(64, 15, 4, 2, 3)["classification"] == "CONTRACTION",
         "kernel control")
    need(find(64, 15, 4, 1, 5)["classification"] == "OBSTRUCTION",
         "larger cutoff witness")
    print("TPC268_ADVERSARIAL_STRESS=PASS "
          f"cases={len(cases)} controls={len(controls)} "
          f"obstructions={len(obstructions)} matched_cutoff_flip=YES "
          "interval_threshold=1/16 asymptotic_promotion=REJECTED")


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
        print("TPC268_ADVERSARIAL_STRESS=FAIL " + str(exc))
        raise SystemExit(1)
