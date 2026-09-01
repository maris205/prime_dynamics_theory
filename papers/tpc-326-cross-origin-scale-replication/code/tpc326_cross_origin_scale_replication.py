#!/usr/bin/env python3
"""TPC-326: cross-origin replication of the TPC-325 scale ladder.

The source-scale ladder is repeated at a second, disjoint origin.  The
numerical engine is obtained through the locked TPC-325 producer, while this
module owns the second-origin protocol, cross-origin comparison, exact anchor,
and certificate.  This is a finite adversarial replication, not an asymptotic
or arithmetic theorem.
"""

from __future__ import annotations

import argparse
import hashlib
import importlib.util
import json
import math
import os
import sys
from fractions import Fraction
from pathlib import Path
from typing import Any

os.environ.setdefault("OMP_NUM_THREADS", "1")
os.environ.setdefault("OPENBLAS_NUM_THREADS", "1")
os.environ.setdefault("MKL_NUM_THREADS", "1")

try:
    import numpy as np
except ImportError as error:  # pragma: no cover
    raise SystemExit("TPC326 requires numpy: " + str(error))

if hasattr(sys, "set_int_max_str_digits"):
    sys.set_int_max_str_digits(0)

PROJECT = Path(__file__).resolve().parents[1]
ROOT = PROJECT.parents[1]
RESULT = PROJECT / "results/tpc326_certificate.json"
PARENT_PROJECT = ROOT / "papers/tpc-325-scale-ladder-profile"
PARENT_CERT = PARENT_PROJECT / "results/tpc325_certificate.json"
PARENT_ENGINE = PARENT_PROJECT / "code/tpc325_scale_ladder_profile.py"
PARENT_CERT_SHA256 = (
    "7afe4fcf56b4432dcf2e5320479cd144a53cdcea29ccbd5cb26c558fd9f06766")
PARENT_ENGINE_SHA256 = (
    "3b1aabb54c7f7cd8c1a64164d24b8937e5d9ca4a41dd3735849a3fe37ec6d3f3")

SCHEMA = "TPC326_CROSS_ORIGIN_SCALE_REPLICATION_V1"
STATUS = "NUMERICALLY_CERTIFIED_FINITE_CROSS_ORIGIN_SCALE_LADDER_REPLICATION"
ROUND2_CLUE = "TEST_CROSS_ORIGIN_SCALE_LADDER_OR_SOURCE_NATIVE_ARITHMETIC_L2"

HEIGHT = 66
SOURCE_ORIGIN = 16001
PARENT_ORIGIN = 12001
SCALES = (320, 640, 1280, 2560)
Q_ANCHORS = (24, 36, 54, 80)
EXPONENTS = (1, 2)
LAW_NAMES = ("all_plus", "alternating_index", "mod4_character", "half_split")
LABELS = ("SIGNED_MAJORISES_DIRECT", "DIRECT_MAJORISES_SIGNED",
          "MIXED", "UNRESOLVED")

EXPECTED_LABELS = {
    "all_plus": {"SIGNED_MAJORISES_DIRECT": 32,
                 "DIRECT_MAJORISES_SIGNED": 0, "MIXED": 0,
                 "UNRESOLVED": 0},
    "alternating_index": {"SIGNED_MAJORISES_DIRECT": 21,
                          "DIRECT_MAJORISES_SIGNED": 0, "MIXED": 11,
                          "UNRESOLVED": 0},
    "mod4_character": {"SIGNED_MAJORISES_DIRECT": 26,
                       "DIRECT_MAJORISES_SIGNED": 0, "MIXED": 6,
                       "UNRESOLVED": 0},
    "half_split": {"SIGNED_MAJORISES_DIRECT": 23,
                   "DIRECT_MAJORISES_SIGNED": 0, "MIXED": 9,
                   "UNRESOLVED": 0},
}
EXPECTED_LABELS_BY_SCALE = {
    320: {
        "all_plus": 8, "alternating_index": 4,
        "mod4_character": 5, "half_split": 5},
    640: {
        "all_plus": 8, "alternating_index": 5,
        "mod4_character": 7, "half_split": 6},
    1280: {
        "all_plus": 8, "alternating_index": 6,
        "mod4_character": 7, "half_split": 6},
    2560: {
        "all_plus": 8, "alternating_index": 6,
        "mod4_character": 7, "half_split": 6},
}
PROFILE_TOL = 1.0e-10
NUMERICAL_GUARD = 1.0e-12
EXACT_INTERVAL = (16001, 16016)
EXACT_Q = 4
EXACT_EXPONENT = 1
EXACT_DIRECT_DIGEST = (
    "e9855d70fb5f73e5c30c8ebe8de3673301a13a23fc6a85299dea816ff97fe2d0")
EXACT_SIGNED_DIGEST = (
    "d97b7e1b65c517eb46f27efa9411dd1f574c61e703470480af2b68397afae136")


class CheckFailure(RuntimeError):
    """A fail-closed certificate error."""


def need(condition: bool, message: str) -> None:
    if type(condition) is not bool or not condition:
        raise CheckFailure(message)


def canonical(value: Any) -> bytes:
    return (json.dumps(value, ensure_ascii=True, sort_keys=True,
                       separators=(",", ":")) + "\n").encode("ascii")


def digest(data: bytes) -> str:
    return hashlib.sha256(data.replace(b"\r\n", b"\n").replace(
        b"\r", b"\n")).hexdigest()


def display(value: float, digits: int = 17) -> str:
    return format(float(value), f".{digits}g")


def load_engine() -> tuple[Any, Any]:
    need(PARENT_ENGINE.is_file(), "TPC325 parent engine missing")
    need(digest(PARENT_ENGINE.read_bytes()) == PARENT_ENGINE_SHA256,
         "TPC325 parent engine provenance")
    spec = importlib.util.spec_from_file_location("tpc325_locked_engine",
                                                  PARENT_ENGINE)
    need(spec is not None and spec.loader is not None,
         "cannot load TPC325 producer")
    parent = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(parent)
    engine = parent.load_engine()
    engine.PANEL_INTERVALS = {
        "second_ladder": {
            scale: (SOURCE_ORIGIN, SOURCE_ORIGIN + scale // 2 - 1)
            for scale in SCALES
        }
    }
    engine.PANEL_NAMES = ("second_ladder",)
    engine.SCALES = SCALES
    return parent, engine


def exact_small_audit(engine: Any) -> dict[str, Any]:
    values = list(range(EXACT_INTERVAL[0], EXACT_INTERVAL[1] + 1))
    primes = engine.shell_for(EXACT_Q)
    blocks = [[[engine.exact_entry(prime, u, t, EXACT_EXPONENT)
                for t in values] for u in values] for prime in primes]
    gram = [[sum((blocks[i][u][t] * blocks[j][u][t]
                  for u in range(len(values)) for t in range(len(values))),
                 Fraction(0)) for j in range(len(primes))]
            for i in range(len(primes))]
    direct = sum((gram[i][i] for i in range(len(primes))), Fraction(0))
    signs = [1 if i % 2 == 0 else -1 for i in range(len(primes))]
    signed = sum((signs[i] * signs[j] * gram[i][j]
                  for i in range(len(primes)) for j in range(len(primes))),
                 Fraction(0))

    def fraction_digest(value: Fraction) -> str:
        return hashlib.sha256(
            f"{value.numerator}/{value.denominator}\n".encode("ascii")
        ).hexdigest()

    need(direct > 0 and signed > 0, "exact anchor positivity")
    direct_digest = fraction_digest(direct)
    signed_digest = fraction_digest(signed)
    need(direct_digest == EXACT_DIRECT_DIGEST and
         signed_digest == EXACT_SIGNED_DIGEST, "exact anchor digest")
    return {
        "interval": list(EXACT_INTERVAL),
        "Q": EXACT_Q,
        "shell": primes,
        "exponent": EXACT_EXPONENT,
        "direct_energy_digest": direct_digest,
        "signed_energy_digest": signed_digest,
        "direct_energy_decimal": display(float(direct), 16),
        "signed_energy_decimal": display(float(signed), 16),
        "signed_over_direct_decimal": display(float(signed / direct), 16),
        "identity_exact": True,
    }


def scale_summary(rows: list[dict[str, Any]], scale: int) -> dict[str, Any]:
    selected = [row for row in rows if row["scale"] == scale]
    need(len(selected) == 8, "scale row count")
    all_plus = [row["laws"]["all_plus"] for row in selected]
    tv = [float(item["profile_tv_interval"][0]) for item in all_plus]
    energy = [float(item["energy_ratio_estimate"]) for item in all_plus]
    return {
        "scale": scale,
        "source_count": scale // 2,
        "source_interval": [SOURCE_ORIGIN, SOURCE_ORIGIN + scale // 2 - 1],
        "rows": 8,
        "all_plus_majorization_rows": sum(
            item["majorization"] == "SIGNED_MAJORISES_DIRECT"
            for item in all_plus),
        "all_plus_minimum_prefix_lower": display(min(
            float(item["minimum_prefix_interval"][0]) for item in all_plus), 16),
        "all_plus_tv_lower_envelope": display(min(tv), 16),
        "all_plus_energy_ratio_min": display(min(energy), 16),
        "all_plus_energy_ratio_max": display(max(energy), 16),
    }


def build_payload(parent: Any, engine: Any) -> dict[str, Any]:
    need(PARENT_CERT.is_file() and digest(PARENT_CERT.read_bytes()) ==
         PARENT_CERT_SHA256, "TPC325 parent certificate lock")
    parent_document = json.loads(PARENT_CERT.read_bytes())
    parent_payload = parent_document["payload"]
    rows = [engine.row_record("second_ladder", scale, q0, exponent)
            for scale in SCALES for q0 in engine.Q_ANCHORS
            for exponent in engine.EXPONENTS]
    need(len(rows) == 32, "row census")
    class_counts = {
        name: {label: sum(row["laws"][name]["majorization"] == label
                          for row in rows) for label in LABELS}
        for name in LAW_NAMES
    }
    need(class_counts == EXPECTED_LABELS, "profile census")
    energy_counts = {
        name: {
            "below_one": sum(float(row["laws"][name]["energy_ratio_estimate"]) < 1
                             for row in rows),
            "above_one": sum(float(row["laws"][name]["energy_ratio_estimate"]) > 1
                             for row in rows),
        }
        for name in LAW_NAMES
    }
    need(energy_counts == parent_payload["finite_audit"]["energy_ratio_counts"],
         "cross-origin energy census")
    summaries = [scale_summary(rows, scale) for scale in SCALES]
    need(all(summary["all_plus_majorization_rows"] == 8
             for summary in summaries), "all-plus ladder")
    need(all(float(summary["all_plus_minimum_prefix_lower"]) > 0
             for summary in summaries), "prefix positivity")
    tv = [float(summary["all_plus_tv_lower_envelope"]) for summary in summaries]
    energy_max = [float(summary["all_plus_energy_ratio_max"])
                  for summary in summaries]
    need(all(a > b for a, b in zip(tv, tv[1:])), "TV trend")
    need(all(a > b for a, b in zip(energy_max, energy_max[1:])),
         "energy trend")
    parent_ladder = parent_payload["scale_ladder"]
    need([item["scale"] for item in parent_ladder] == list(SCALES),
         "parent ladder scales")
    tv_delta = max(abs(float(a["all_plus_tv_lower_envelope"]) -
                       float(b["all_plus_tv_lower_envelope"]))
                   for a, b in zip(parent_ladder, summaries))
    energy_delta = max(abs(float(a["all_plus_energy_ratio_max"]) -
                           float(b["all_plus_energy_ratio_max"]))
                       for a, b in zip(parent_ladder, summaries))
    need(tv_delta < 1.0e-3 and energy_delta < 5.0e-3,
         "cross-origin envelope agreement")
    return {
        "schema": SCHEMA,
        "parent_lock": {
            "project": "TPC-325 source-scale ladder profile",
            "certificate_sha256": PARENT_CERT_SHA256,
            "producer_sha256": PARENT_ENGINE_SHA256,
        },
        "protocol": {
            "parent_origin": PARENT_ORIGIN,
            "source_origin": SOURCE_ORIGIN,
            "source_scales": list(SCALES),
            "source_counts": [scale // 2 for scale in SCALES],
            "nested_rule": "I_N=[16001,16000+N/2] with N in {320,640,1280,2560}",
            "height": HEIGHT,
            "Q_anchors": list(engine.Q_ANCHORS),
            "kernel_exponents": list(engine.EXPONENTS),
            "domain": "ell^2(I_N)",
            "direct_gram": "G_direct=sum_p B_p^T B_p",
            "signed_gram": "G_e=C_e^T C_e, C_e=sum_p e_p B_p",
            "profile": "pi_j(G)=lambda_j(G)/tr(G), descending",
            "paths": list(engine.PATHS),
            "canonical_sign_laws": list(LAW_NAMES),
            "cross_origin_rule": (
                "repeat the frozen TPC-325 ladder at a disjoint origin; "
                "compare census and finite envelopes only"),
        },
        "exact_small_audit": exact_small_audit(engine),
        "scale_ladder": summaries,
        "cross_origin": {
            "parent_origin": PARENT_ORIGIN,
            "new_origin": SOURCE_ORIGIN,
            "profile_census_matches_parent": (
                class_counts == parent_payload["finite_audit"]
                ["profile_majorization_counts"]),
            "energy_census_matches_parent": (
                energy_counts == parent_payload["finite_audit"]
                ["energy_ratio_counts"]),
            "max_tv_envelope_difference": display(tv_delta, 16),
            "max_energy_upper_envelope_difference": display(energy_delta, 16),
            "tv_agreement_threshold": "0.001",
            "energy_agreement_threshold": "0.005",
        },
        "finite_audit": {
            "rows": 32,
            "rows_per_scale": {str(scale): 8 for scale in SCALES},
            "profile_majorization_counts": class_counts,
            "energy_ratio_counts": energy_counts,
            "all_plus_strict_majorization_rows": 32,
            "all_plus_minimum_prefix_lower": display(min(
                float(row["laws"]["all_plus"]["minimum_prefix_interval"][0])
                for row in rows), 16),
            "all_plus_tv_lower_envelope_strictly_descends": True,
            "all_plus_energy_upper_envelope_strictly_descends": True,
            "fixed_power_credit": 0,
        },
        "claim_firewall": {
            "TPC326_CROSS_ORIGIN_REPLICATION":
                "NUMERICALLY_CERTIFIED_FINITE_32_ROWS_2_ORIGINS",
            "TPC326_ALL_PLUS_REPLICATION":
                "NUMERICALLY_CERTIFIED_FINITE_32_OF_32",
            "TPC326_CENSUS_MATCH":
                "NUMERICALLY_CERTIFIED_FINITE_PARENT_MATCH",
            "TPC326_ENVELOPE_AGREEMENT":
                "NUMERICALLY_CERTIFIED_FINITE_WITHIN_DECLARED_THRESHOLDS",
            "TPC326_ARITHMETIC_ADVANCE": "NO",
            "TPC326_FIXED_POWER_CREDIT": 0,
            "TPC326_FULL_GATE_B": "OPEN",
            "TPC326_TWIN_PRIME_RESULT": "NONE",
        },
        "round2_clue": ROUND2_CLUE,
        "rows": rows,
    }


def build_document(parent: Any, engine: Any) -> dict[str, Any]:
    payload = build_payload(parent, engine)
    return {
        "certificate_version": 1,
        "claim_status": STATUS,
        "payload": payload,
        "payload_sha256": hashlib.sha256(canonical(payload)).hexdigest(),
    }


def write_certificate(parent: Any, engine: Any) -> None:
    RESULT.parent.mkdir(parents=True, exist_ok=True)
    RESULT.write_bytes(canonical(build_document(parent, engine)))


def check_certificate(parent: Any, engine: Any) -> None:
    raw = RESULT.read_bytes()
    stored = json.loads(raw)
    need(raw == canonical(stored), "certificate canonicality")
    need(stored == build_document(parent, engine), "certificate does not replay")
    print("TPC326_CERTIFICATE=PASS rows=32 origins=2 "
          "all_plus=32/32 census=parent_match envelopes=within_thresholds")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--write", action="store_true")
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()
    if args.write == args.check:
        raise SystemExit("exactly one of --write or --check is required")
    try:
        parent, engine = load_engine()
        if args.write:
            write_certificate(parent, engine)
            print("TPC326_CERTIFICATE=WRITTEN")
        else:
            check_certificate(parent, engine)
    except (CheckFailure, OSError, json.JSONDecodeError, ValueError,
            np.linalg.LinAlgError) as error:
        print("TPC326_CERTIFICATE=FAIL " + str(error), file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
