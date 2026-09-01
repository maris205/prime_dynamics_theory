#!/usr/bin/env python3
"""Adversarial geometry and cross-origin stress checks for TPC-326."""

from __future__ import annotations

import argparse
import json
import math
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
PROJECT = ROOT / "papers/tpc-326-cross-origin-scale-replication"
CERTIFICATE = PROJECT / "results/tpc326_certificate.json"
SCALES = (320, 640, 1280, 2560)
Q_ANCHORS = (24, 36, 54, 80)
ORIGIN = 16001
PARENT_ORIGIN = 12001
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


def prime(p: int) -> bool:
    return p >= 2 and all(p % d for d in range(2, math.isqrt(p) + 1))


def check() -> None:
    raw = CERTIFICATE.read_bytes()
    document = json.loads(raw)
    need(raw == canonical(document), "certificate canonicality")
    payload = document["payload"]
    protocol = payload["protocol"]
    need(protocol["source_origin"] == ORIGIN and
         protocol["parent_origin"] == PARENT_ORIGIN and
         protocol["source_scales"] == list(SCALES) and
         protocol["Q_anchors"] == list(Q_ANCHORS), "protocol")
    rows = payload["rows"]
    need(len(rows) == 32, "row census")
    for scale in SCALES:
        selected = [row for row in rows if row["scale"] == scale]
        need(len(selected) == 8, "per-scale census")
        interval = (ORIGIN, ORIGIN + scale // 2 - 1)
        need({tuple(row["source_interval"]) for row in selected} == {interval},
             "interval lock")
        need(all(row["laws"]["all_plus"]["majorization"] ==
                 "SIGNED_MAJORISES_DIRECT" for row in selected),
             "all-plus label")
        need(all(float(row["laws"]["all_plus"]["minimum_prefix_interval"][0]) > 0
                 for row in selected), "prefix lower")
    intervals = [(ORIGIN, ORIGIN + scale // 2 - 1) for scale in SCALES]
    need(all(a[0] == b[0] and a[1] < b[1]
             for a, b in zip(intervals, intervals[1:])), "strict nesting")
    for interval in intervals:
        need(all(interval[1] < lo or hi < interval[0]
                 for lo, hi in PARENT_INTERVALS), "disjoint from parent panels")

    changed = 0
    for scale in SCALES:
        values = range(ORIGIN, ORIGIN + scale // 2)
        shifted = range(ORIGIN + 1, ORIGIN + scale // 2 + 1)
        for q0 in Q_ANCHORS:
            shell = [p for p in range(q0 + 1, 2 * q0 + 1) if prime(p)]
            if any(tuple(v % p == 0 for v in values) !=
                   tuple(v % p == 0 for v in shifted) for p in shell):
                changed += 1
    need(changed == len(SCALES) * len(Q_ANCHORS), "residue perturbation")

    ladder = payload["scale_ladder"]
    tv = [float(item["all_plus_tv_lower_envelope"]) for item in ladder]
    energy = [float(item["all_plus_energy_ratio_max"]) for item in ladder]
    need([item["scale"] for item in ladder] == list(SCALES) and
         all(a > b for a, b in zip(tv, tv[1:])) and
         all(a > b for a, b in zip(energy, energy[1:])), "new ladder trends")
    comparison = payload["cross_origin"]
    need(comparison["profile_census_matches_parent"] is True and
         comparison["energy_census_matches_parent"] is True and
         float(comparison["max_tv_envelope_difference"]) < 0.001 and
         float(comparison["max_energy_upper_envelope_difference"]) < 0.005,
         "cross-origin agreement")
    firewall = payload["claim_firewall"]
    need(firewall["TPC326_ARITHMETIC_ADVANCE"] == "NO" and
         firewall["TPC326_FULL_GATE_B"] == "OPEN" and
         firewall["TPC326_TWIN_PRIME_RESULT"] == "NONE", "firewall")
    print("TPC326_STRESS=PASS disjoint=1 nesting=1 residue_perturbation=1 "
          "all_plus=32/32 parent_census=1 envelope_agreement=1 firewall=fail_closed")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--check", action="store_true")
    parser.parse_args()
    try:
        check()
    except (Failure, OSError, json.JSONDecodeError, ValueError) as error:
        print("TPC326_STRESS=FAIL " + str(error), file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
