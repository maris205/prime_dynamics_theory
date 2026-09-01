#!/usr/bin/env python3
"""Adversarial geometry and certificate stress checks for TPC-325."""

from __future__ import annotations

import argparse
import hashlib
import json
import math
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
PROJECT = ROOT / "papers/tpc-325-scale-ladder-profile"
CERTIFICATE = PROJECT / "results/tpc325_certificate.json"
SCALES = (320, 640, 1280, 2560)
ORIGIN = 12001
Q_ANCHORS = (24, 36, 54, 80)
EXPONENTS = (1, 2)
LAW_NAMES = ("all_plus", "alternating_index", "mod4_character", "half_split")
PARENT_INTERVALS = (
    (321, 2560), (2561, 2880), (2881, 3520), (3521, 4800),
    (5001, 5320), (6001, 6640), (8001, 9280),
)


class Failure(RuntimeError):
    pass


def need(condition: bool, message: str) -> None:
    if type(condition) is not bool or not condition:
        raise Failure(message)


def canonical(value: object) -> bytes:
    return (json.dumps(value, ensure_ascii=True, sort_keys=True,
                       separators=(",", ":")) + "\n").encode("ascii")


def check() -> None:
    raw = CERTIFICATE.read_bytes()
    document = json.loads(raw)
    need(raw == canonical(document), "certificate canonicality")
    payload = document["payload"]
    protocol = payload["protocol"]
    need(protocol["source_origin"] == ORIGIN and
         tuple(protocol["source_scales"]) == SCALES and
         tuple(protocol["Q_anchors"]) == Q_ANCHORS and
         tuple(protocol["kernel_exponents"]) == EXPONENTS, "protocol")
    rows = payload["rows"]
    need(len(rows) == 32, "row count")
    for scale in SCALES:
        scale_rows = [row for row in rows if row["scale"] == scale]
        need(len(scale_rows) == 8, "scale census")
        lo, hi = ORIGIN, ORIGIN + scale // 2 - 1
        need({tuple(row["source_interval"]) for row in scale_rows} == {(lo, hi)},
             "nested interval")
        need(all(row["laws"]["all_plus"]["majorization"] ==
                 "SIGNED_MAJORISES_DIRECT" for row in scale_rows),
             "all-plus scale label")
        need(all(float(row["laws"]["all_plus"]["minimum_prefix_interval"][0]) > 0
                 for row in scale_rows), "all-plus prefix positivity")
    intervals = [(ORIGIN, ORIGIN + scale // 2 - 1) for scale in SCALES]
    need(all(a[0] == b[0] and a[1] < b[1]
             for a, b in zip(intervals, intervals[1:])), "strict nesting")
    for interval in intervals:
        need(all(interval[1] < lo or hi < interval[0]
                 for lo, hi in PARENT_INTERVALS), "fresh source interval")

    # A source shift by one changes at least one active residue mask on every
    # declared shell; this guards against a vacuous copy of the parent panel.
    changed = 0
    for scale in SCALES:
        values = range(ORIGIN, ORIGIN + scale // 2)
        shifted = range(ORIGIN + 1, ORIGIN + scale // 2 + 1)
        for q0 in Q_ANCHORS:
            primes = [p for p in range(q0 + 1, 2 * q0 + 1)
                      if all(p % d for d in range(2, math.isqrt(p) + 1))]
            if any(tuple(v % p == 0 for v in values) !=
                   tuple(v % p == 0 for v in shifted) for p in primes):
                changed += 1
    need(changed == len(SCALES) * len(Q_ANCHORS), "residue perturbation")

    ladder = payload["scale_ladder"]
    need([item["scale"] for item in ladder] == list(SCALES), "ladder order")
    tv = [float(item["all_plus_tv_lower_envelope"]) for item in ladder]
    energy = [float(item["all_plus_energy_ratio_max"]) for item in ladder]
    need(all(a > b for a, b in zip(tv, tv[1:])), "TV envelope trend")
    need(all(a > b for a, b in zip(energy, energy[1:])), "energy envelope trend")
    need(payload["finite_audit"]["fixed_power_credit"] == 0, "power credit")
    firewall = payload["claim_firewall"]
    need(firewall["TPC325_ARITHMETIC_ADVANCE"] == "NO" and
         firewall["TPC325_FULL_GATE_B"] == "OPEN" and
         firewall["TPC325_TWIN_PRIME_RESULT"] == "NONE", "firewall")
    print("TPC325_STRESS=PASS nesting=1 fresh_source=1 residue_perturbation=1 "
          "all_plus=32/32 envelope_trends=2 firewall=fail_closed")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--check", action="store_true")
    parser.parse_args()
    try:
        check()
    except (Failure, OSError, json.JSONDecodeError, ValueError) as error:
        print("TPC325_STRESS=FAIL " + str(error), file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
