#!/usr/bin/env python3
"""Independent interval-census replay for TPC-303."""

from __future__ import annotations

import hashlib
import json
import sys
from decimal import Decimal, getcontext
from pathlib import Path
from typing import Any

getcontext().prec = 80
PROJECT = Path(__file__).resolve().parents[1]
ROOT = PROJECT.parents[1]
PARENT = ROOT / (
    "papers/tpc-302-growing-shell-budget-gap-audit/results/"
    "tpc302_certificate.json")
CERTIFICATE = PROJECT / "results/tpc303_certificate.json"
PARENT_SHA256 = "469431136dd2b80ccdddeeedeabe48be8e74405c6df36eead2ae58936a8c24d6"
SCHEMA = "TPC303_CARDINALITY_MONOTONICITY_OBSTRUCTION_V1"
Q_SPINE = (50, 60, 70, 90)
TAUS = ("0.25", "0.5", "0.75")
NORMALIZERS = (
    "beta_norm_squared", "profile_trace_mean", "first_profile_norm_squared")


class Failure(RuntimeError):
    pass


def need(condition: bool, message: str) -> None:
    if type(condition) is not bool or not condition:
        raise Failure(message)


def canonical(value: Any) -> bytes:
    return (json.dumps(value, ensure_ascii=True, sort_keys=True,
                       separators=(",", ":")) + "\n").encode("ascii")


def digest(data: bytes) -> str:
    return hashlib.sha256(data.replace(b"\r\n", b"\n").replace(
        b"\r", b"\n")).hexdigest()


def bounds(row: dict[str, Any], tau: str,
           normalizer: str) -> tuple[Decimal, Decimal, int]:
    target = row["tolerance_audits"][tau]["contexts"]["common_prefix"][
        "targets"]["weighted"]
    value = target["budget_over_normalizer"][normalizer]
    return Decimal(value[0]), Decimal(value[1]), int(target["k"])


def check() -> None:
    raw_parent = PARENT.read_bytes()
    need(digest(raw_parent) == PARENT_SHA256, "parent provenance")
    parent = json.loads(raw_parent)
    need(raw_parent == canonical(parent), "parent canonicality")
    selected = {(int(row["Q"]), int(row["kernel_exponent"])): row
                for row in parent["payload"]["rows"]
                if row["axis"] == "GROWTH_PATH" and row["scale"] == 512 and
                row["H"] == 58 and row["comparison_cutoff_z"] == 5 and
                row["Q"] in Q_SPINE}
    need(len(selected) == 8, "spine rows")

    descents = ascents = unresolved = same_prefix_descents = 0
    nonmonotone = 0
    strongest = Decimal(2)
    strongest_same = Decimal(2)
    for exponent in (1, 2):
        for tau in TAUS:
            for normalizer in NORMALIZERS:
                values = [bounds(selected[q, exponent], tau, normalizer)
                          for q in Q_SPINE]
                local_d = local_a = 0
                for left, right in zip(values, values[1:]):
                    left_lo, left_hi, left_k = left
                    right_lo, right_hi, right_k = right
                    if right_hi < left_lo:
                        descents += 1
                        local_d += 1
                        ratio = right_hi / left_lo
                        strongest = min(strongest, ratio)
                        if left_k == right_k:
                            same_prefix_descents += 1
                            strongest_same = min(strongest_same, ratio)
                    elif right_lo > left_hi:
                        ascents += 1
                        local_a += 1
                    else:
                        unresolved += 1
                nonmonotone += local_d > 0 and local_a > 0

    raw = CERTIFICATE.read_bytes()
    data = json.loads(raw)
    need(raw == canonical(data), "certificate canonicality")
    need(data["payload"]["schema"] == SCHEMA, "certificate schema")
    audit = data["payload"]["finite_audit"]
    need((descents, ascents, unresolved, same_prefix_descents, nonmonotone) ==
         (21, 33, 0, 9, 18), "independent census")
    need(audit["certified_descents"] == descents and
         audit["certified_ascents"] == ascents and
         audit["unresolved_transitions"] == unresolved and
         audit["same_prefix_descents"] == same_prefix_descents and
         audit["nonmonotone_series"] == nonmonotone,
         "published census")
    published = audit["strongest_descent"]["right_over_left_interval"][1]
    published_same = audit["strongest_same_prefix_descent"][
        "right_over_left_interval"][1]
    need(published == format(strongest, ".38g") and
         published_same == format(strongest_same, ".38g"),
         "strongest witness replay")
    need(data["payload_sha256"] == hashlib.sha256(
        canonical(data["payload"])).hexdigest(), "payload hash")
    print("TPC303_INDEPENDENT_CHECK=PASS series=18 transitions=54 "
          "descents=21 ascents=33 same_prefix_descents=9")


if __name__ == "__main__":
    try:
        check()
    except (Failure, OSError, KeyError, TypeError, ValueError,
            json.JSONDecodeError) as error:
        print("TPC303_INDEPENDENT_CHECK=FAIL " + str(error), file=sys.stderr)
        raise SystemExit(1)
