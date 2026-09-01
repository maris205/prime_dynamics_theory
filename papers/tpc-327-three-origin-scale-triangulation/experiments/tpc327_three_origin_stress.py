#!/usr/bin/env python3
"""Adversarial geometry and claim-firewall checks for TPC-327."""

from __future__ import annotations

import argparse
import hashlib
import json
import math
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
PROJECT = ROOT / "papers/tpc-327-three-origin-scale-triangulation"
CERTIFICATE = PROJECT / "results/tpc327_certificate.json"
PARENT_CERTIFICATE = ROOT / "papers/tpc-326-cross-origin-scale-replication/results/tpc326_certificate.json"
GRANDPARENT_CERTIFICATE = ROOT / "papers/tpc-325-scale-ladder-profile/results/tpc325_certificate.json"
PARENT_CERT_SHA256 = "9b52f8f74fe2edd5fa8c512fcb7a87c9bfef06cb4e888c93945419006bcff2ec"
GRANDPARENT_CERT_SHA256 = "7afe4fcf56b4432dcf2e5320479cd144a53cdcea29ccbd5cb26c558fd9f06766"

ORIGIN = 20001
PARENT_ORIGINS = (12001, 16001)
ORIGINS = (12001, 16001, 20001)
SCALES = (320, 640, 1280, 2560)
Q_ANCHORS = (24, 36, 54, 80)
TV_THRESHOLD = 0.001
ENERGY_THRESHOLD = 0.005


class Failure(RuntimeError):
    pass


def need(condition: bool, message: str) -> None:
    if type(condition) is not bool or not condition:
        raise Failure(message)


def canonical(value: object) -> bytes:
    return (json.dumps(value, ensure_ascii=True, sort_keys=True,
                       separators=(",", ":")) + "\n").encode("ascii")


def digest(data: bytes) -> str:
    return hashlib.sha256(data.replace(b"\r\n", b"\n").replace(
        b"\r", b"\n")).hexdigest()


def prime(p: int) -> bool:
    return p >= 2 and all(p % d for d in range(2, math.isqrt(p) + 1))


def load(path: Path, expected: str) -> dict[str, object]:
    raw = path.read_bytes()
    need(digest(raw) == expected, "locked certificate provenance")
    document = json.loads(raw)
    need(raw == canonical(document), "locked certificate canonicality")
    return document["payload"]


def check() -> None:
    raw = CERTIFICATE.read_bytes()
    document = json.loads(raw)
    need(raw == canonical(document), "certificate canonicality")
    payload = document["payload"]
    protocol = payload["protocol"]
    need(protocol["source_origin"] == ORIGIN and
         protocol["parent_origins"] == list(PARENT_ORIGINS) and
         protocol["origins"] == list(ORIGINS) and
         protocol["source_scales"] == list(SCALES) and
         protocol["Q_anchors"] == list(Q_ANCHORS), "protocol")
    rows = payload["rows"]
    need(len(rows) == 32, "row census")
    intervals = []
    for scale in SCALES:
        selected = [row for row in rows if row["scale"] == scale]
        need(len(selected) == 8, "per-scale census")
        interval = (ORIGIN, ORIGIN + scale // 2 - 1)
        intervals.append(interval)
        need({tuple(row["source_interval"]) for row in selected} == {interval},
             "interval lock")
        need(all(row["laws"]["all_plus"]["majorization"] ==
                 "SIGNED_MAJORISES_DIRECT" for row in selected),
             "all-plus label")
        need(all(float(row["laws"]["all_plus"]
                   ["minimum_prefix_interval"][0]) > 0
                 for row in selected), "prefix lower")
    need(all(a[0] == b[0] and a[1] < b[1]
             for a, b in zip(intervals, intervals[1:])), "strict nesting")

    previous_intervals = [
        (12001, 12160), (12001, 12320), (12001, 12640), (12001, 13280),
        (16001, 16160), (16001, 16320), (16001, 16640), (16001, 17280),
        (321, 2560), (2561, 2880), (2881, 3520), (3521, 4800),
        (5001, 5320), (6001, 6640), (8001, 9281),
    ]
    for lo, hi in intervals:
        need(all(hi < old_lo or old_hi < lo
                 for old_lo, old_hi in previous_intervals),
             "overlap with a previous source panel")

    # A one-step source move must alter at least one active residue mask in
    # every scale/shell cell; otherwise the third panel would be a vacuous copy.
    changed = 0
    for scale in SCALES:
        values = range(ORIGIN, ORIGIN + scale // 2)
        shifted = range(ORIGIN + 1, ORIGIN + scale // 2 + 1)
        for q0 in Q_ANCHORS:
            shell = [p for p in range(q0 + 1, 2 * q0 + 1) if prime(p)]
            if any(tuple(v % p == 0 for v in values) !=
                   tuple(v % p == 0 for v in shifted) for p in shell):
                changed += 1
    need(changed == len(SCALES) * len(Q_ANCHORS),
         "residue perturbation is vacuous")

    parent1 = load(GRANDPARENT_CERTIFICATE, GRANDPARENT_CERT_SHA256)
    parent2 = load(PARENT_CERTIFICATE, PARENT_CERT_SHA256)
    counts = payload["finite_audit"]["profile_majorization_counts"]
    energies = payload["finite_audit"]["energy_ratio_counts"]
    need(counts == parent1["finite_audit"]["profile_majorization_counts"] and
         counts == parent2["finite_audit"]["profile_majorization_counts"] and
         energies == parent1["finite_audit"]["energy_ratio_counts"] and
         energies == parent2["finite_audit"]["energy_ratio_counts"],
         "three-origin census")
    ensemble = payload["origin_ensemble"]
    need(ensemble["origins"] == list(ORIGINS) and
         ensemble["all_pairwise_tv_within_threshold"] is True and
         ensemble["all_pairwise_energy_within_threshold"] is True and
         ensemble["nonzero_finite_origin_spread"] is True and
         float(ensemble["max_pairwise_tv_difference"]) < TV_THRESHOLD and
         float(ensemble["max_pairwise_energy_difference"]) < ENERGY_THRESHOLD,
         "triangulation envelope")
    need(len(ensemble["per_scale"]) == len(SCALES), "ensemble scale census")
    for item in ensemble["per_scale"]:
        need(set(map(int, item["tv_lower_envelope_by_origin"])) == set(ORIGINS) and
             set(map(int, item["energy_upper_envelope_by_origin"])) == set(ORIGINS),
             "origin keys")
        need(float(item["tv_range"]) > 0 and float(item["energy_range"]) > 0,
             "nonzero per-scale spread")
    # The new exact anchor must not accidentally equal the prior origin's
    # rational anchor; this is a small, deterministic residue-environment check.
    anchor = payload["exact_small_audit"]
    old_anchor = parent2["exact_small_audit"]
    need(anchor["direct_energy_digest"] != old_anchor["direct_energy_digest"] and
         anchor["signed_energy_digest"] != old_anchor["signed_energy_digest"],
         "anchor did not change across origins")
    firewall = payload["claim_firewall"]
    need(firewall["TPC327_ARITHMETIC_ADVANCE"] == "NO" and
         firewall["TPC327_FIXED_POWER_CREDIT"] == 0 and
         firewall["TPC327_FULL_GATE_B"] == "OPEN" and
         firewall["TPC327_TWIN_PRIME_RESULT"] == "NONE", "firewall")
    print("TPC327_STRESS=PASS disjoint=1 nesting=1 residue_perturbation=1 "
          "three_origin_census=1 envelope_triangulation=1 firewall=fail_closed")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--check", action="store_true")
    parser.parse_args()
    try:
        check()
    except (Failure, OSError, json.JSONDecodeError, ValueError) as error:
        print("TPC327_STRESS=FAIL " + str(error), file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
