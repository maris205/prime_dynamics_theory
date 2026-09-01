#!/usr/bin/env python3
"""TPC-327: three-origin triangulation of the finite source-scale ladder.

The TPC-325/TPC-326 ladder is repeated at a third, disjoint source origin.
The released TPC-326 producer is loaded under a provenance lock and only the
source origin is changed.  In addition to the new 32-row panel, this module
records the three-origin envelope range.  All statements are finite; no
source-uniform or arithmetic theorem is inferred.
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
    raise SystemExit("TPC327 requires numpy: " + str(error))

if hasattr(sys, "set_int_max_str_digits"):
    sys.set_int_max_str_digits(0)

PROJECT = Path(__file__).resolve().parents[1]
ROOT = PROJECT.parents[1]
RESULT = PROJECT / "results/tpc327_certificate.json"
PARENT_PROJECT = ROOT / "papers/tpc-326-cross-origin-scale-replication"
PARENT_CERT = PARENT_PROJECT / "results/tpc326_certificate.json"
PARENT_ENGINE = PARENT_PROJECT / "code/tpc326_cross_origin_scale_replication.py"
GRANDPARENT_CERT = ROOT / "papers/tpc-325-scale-ladder-profile/results/tpc325_certificate.json"
PARENT_CERT_SHA256 = (
    "9b52f8f74fe2edd5fa8c512fcb7a87c9bfef06cb4e888c93945419006bcff2ec")
PARENT_ENGINE_SHA256 = (
    "2f9f5b813a070144affd20dc83d88f5a3cc3642b51e90a9fa3f48a69eb11d683")
GRANDPARENT_CERT_SHA256 = (
    "7afe4fcf56b4432dcf2e5320479cd144a53cdcea29ccbd5cb26c558fd9f06766")

SCHEMA = "TPC327_THREE_ORIGIN_SCALE_TRIANGULATION_V1"
STATUS = "NUMERICALLY_CERTIFIED_FINITE_THREE_ORIGIN_SCALE_TRIANGULATION"
ROUND2_CLUE = "TEST_ORIGIN_ENSEMBLE_SCALE_GROWTH_OR_SOURCE_NATIVE_ARITHMETIC_L2"

HEIGHT = 66
SOURCE_ORIGIN = 20001
PREVIOUS_ORIGINS = (12001, 16001)
ORIGINS = PREVIOUS_ORIGINS + (SOURCE_ORIGIN,)
SCALES = (320, 640, 1280, 2560)
Q_ANCHORS = (24, 36, 54, 80)
EXPONENTS = (1, 2)
LAW_NAMES = ("all_plus", "alternating_index", "mod4_character", "half_split")
LABELS = ("SIGNED_MAJORISES_DIRECT", "DIRECT_MAJORISES_SIGNED",
          "MIXED", "UNRESOLVED")
PROFILE_TOL = 1.0e-10
NUMERICAL_GUARD = 1.0e-12
TV_THRESHOLD = 1.0e-3
ENERGY_THRESHOLD = 5.0e-3
EXACT_INTERVAL = (20001, 20016)
EXACT_Q = 4
EXACT_EXPONENT = 1
EXACT_DIRECT_DIGEST = (
    "97225bdbd0cb628956b3701748cec3b2eca7b4d559c0d0b42044300f7c26889b")
EXACT_SIGNED_DIGEST = (
    "f38ac7229026dcd2ada592c5b245871d3ef1856e4bac21c86010e89766a9f9f7")


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
    need(PARENT_ENGINE.is_file(), "TPC326 parent engine missing")
    need(digest(PARENT_ENGINE.read_bytes()) == PARENT_ENGINE_SHA256,
         "TPC326 parent engine provenance")
    spec = importlib.util.spec_from_file_location(
        "tpc326_locked_engine_for_tpc327", PARENT_ENGINE)
    need(spec is not None and spec.loader is not None,
         "cannot load TPC326 producer")
    parent = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(parent)
    # TPC-326's loader owns the TPC-325 engine lock.  Changing this constant
    # before loading gives the same literal engine at the new origin.
    parent.SOURCE_ORIGIN = SOURCE_ORIGIN
    parent.EXACT_INTERVAL = EXACT_INTERVAL
    unused_parent, engine = parent.load_engine()
    engine.PANEL_INTERVALS = {
        "third_ladder": {
            scale: (SOURCE_ORIGIN, SOURCE_ORIGIN + scale // 2 - 1)
            for scale in SCALES
        }
    }
    engine.PANEL_NAMES = ("third_ladder",)
    engine.SCALES = SCALES
    return parent, engine


def load_payload(path: Path) -> dict[str, Any]:
    raw = path.read_bytes()
    document = json.loads(raw)
    need(raw == canonical(document), f"noncanonical parent: {path}")
    return document["payload"]


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

    direct_digest = fraction_digest(direct)
    signed_digest = fraction_digest(signed)
    need(direct > 0 and signed > 0, "exact anchor positivity")
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


def finite_values(payload: dict[str, Any]) -> tuple[dict[int, float], dict[int, float]]:
    ladder = payload["scale_ladder"]
    need([item["scale"] for item in ladder] == list(SCALES),
         "parent ladder order")
    tv = {item["scale"]: float(item["all_plus_tv_lower_envelope"])
          for item in ladder}
    energy = {item["scale"]: float(item["all_plus_energy_ratio_max"])
              for item in ladder}
    return tv, energy


def ensemble_summary(parent1: dict[str, Any], parent2: dict[str, Any],
                     child: list[dict[str, Any]]) -> dict[str, Any]:
    child_ladder = [scale_summary(child, scale) for scale in SCALES]
    ladders = {
        str(PREVIOUS_ORIGINS[0]): finite_values(parent1),
        str(PREVIOUS_ORIGINS[1]): finite_values(parent2),
        str(SOURCE_ORIGIN): (
            {item["scale"]: float(item["all_plus_tv_lower_envelope"])
             for item in child_ladder},
            {item["scale"]: float(item["all_plus_energy_ratio_max"])
             for item in child_ladder}),
    }
    per_scale = []
    max_tv = 0.0
    max_energy = 0.0
    for scale in SCALES:
        tv_by_origin = {origin: ladders[origin][0][scale]
                        for origin in ladders}
        energy_by_origin = {origin: ladders[origin][1][scale]
                            for origin in ladders}
        tv_range = max(tv_by_origin.values()) - min(tv_by_origin.values())
        energy_range = (max(energy_by_origin.values()) -
                        min(energy_by_origin.values()))
        max_tv = max(max_tv, tv_range)
        max_energy = max(max_energy, energy_range)
        per_scale.append({
            "scale": scale,
            "tv_lower_envelope_by_origin": {
                origin: display(value, 16)
                for origin, value in tv_by_origin.items()},
            "tv_range": display(tv_range, 16),
            "energy_upper_envelope_by_origin": {
                origin: display(value, 16)
                for origin, value in energy_by_origin.items()},
            "energy_range": display(energy_range, 16),
        })
    return {
        "origins": list(ORIGINS),
        "per_scale": per_scale,
        "max_pairwise_tv_difference": display(max_tv, 16),
        "max_pairwise_energy_difference": display(max_energy, 16),
        "tv_agreement_threshold": display(TV_THRESHOLD, 1),
        "energy_agreement_threshold": display(ENERGY_THRESHOLD, 1),
        "all_pairwise_tv_within_threshold": max_tv < TV_THRESHOLD,
        "all_pairwise_energy_within_threshold": max_energy < ENERGY_THRESHOLD,
        "nonzero_finite_origin_spread": max_tv > 0.0 and max_energy > 0.0,
    }


def build_payload(parent_module: Any, engine: Any) -> dict[str, Any]:
    need(PARENT_CERT.is_file() and digest(PARENT_CERT.read_bytes()) ==
         PARENT_CERT_SHA256, "TPC326 parent certificate lock")
    need(GRANDPARENT_CERT.is_file() and
         digest(GRANDPARENT_CERT.read_bytes()) == GRANDPARENT_CERT_SHA256,
         "TPC325 grandparent certificate lock")
    parent2 = load_payload(PARENT_CERT)
    parent1 = load_payload(GRANDPARENT_CERT)
    rows = [engine.row_record("third_ladder", scale, q0, exponent)
            for scale in SCALES for q0 in engine.Q_ANCHORS
            for exponent in engine.EXPONENTS]
    need(len(rows) == 32, "row census")
    class_counts = {
        name: {label: sum(row["laws"][name]["majorization"] == label
                          for row in rows) for label in LABELS}
        for name in LAW_NAMES
    }
    energy_counts = {
        name: {
            "below_one": sum(float(row["laws"][name]["energy_ratio_estimate"]) < 1
                             for row in rows),
            "above_one": sum(float(row["laws"][name]["energy_ratio_estimate"]) > 1
                             for row in rows),
        }
        for name in LAW_NAMES
    }
    need(class_counts == parent1["finite_audit"]["profile_majorization_counts"],
         "TPC325 profile census")
    need(class_counts == parent2["finite_audit"]["profile_majorization_counts"],
         "TPC326 profile census")
    need(energy_counts == parent1["finite_audit"]["energy_ratio_counts"],
         "TPC325 energy census")
    need(energy_counts == parent2["finite_audit"]["energy_ratio_counts"],
         "TPC326 energy census")
    summaries = [scale_summary(rows, scale) for scale in SCALES]
    need(all(item["all_plus_majorization_rows"] == 8 for item in summaries),
         "all-plus ladder")
    need(all(float(item["all_plus_minimum_prefix_lower"]) > 0
             for item in summaries), "prefix positivity")
    tv = [float(item["all_plus_tv_lower_envelope"]) for item in summaries]
    energy_max = [float(item["all_plus_energy_ratio_max"])
                  for item in summaries]
    need(all(a > b for a, b in zip(tv, tv[1:])), "TV trend")
    need(all(a > b for a, b in zip(energy_max, energy_max[1:])),
         "energy trend")
    ensemble = ensemble_summary(parent1, parent2, rows)
    need(ensemble["all_pairwise_tv_within_threshold"] is True and
         ensemble["all_pairwise_energy_within_threshold"] is True,
         "three-origin envelope agreement")
    need(ensemble["nonzero_finite_origin_spread"] is True,
         "nonvacuous origin spread")
    return {
        "schema": SCHEMA,
        "parent_lock": {
            "project": "TPC-326 cross-origin scale replication",
            "certificate_sha256": PARENT_CERT_SHA256,
            "producer_sha256": PARENT_ENGINE_SHA256,
            "grandparent_certificate_sha256": GRANDPARENT_CERT_SHA256,
        },
        "protocol": {
            "parent_origins": list(PREVIOUS_ORIGINS),
            "source_origin": SOURCE_ORIGIN,
            "origins": list(ORIGINS),
            "source_scales": list(SCALES),
            "source_counts": [scale // 2 for scale in SCALES],
            "nested_rule": "I_N=[20001,20000+N/2] with N in {320,640,1280,2560}",
            "height": HEIGHT,
            "Q_anchors": list(engine.Q_ANCHORS),
            "kernel_exponents": list(engine.EXPONENTS),
            "domain": "ell^2(I_N)",
            "direct_gram": "G_direct=sum_p B_p^T B_p",
            "signed_gram": "G_e=C_e^T C_e, C_e=sum_p e_p B_p",
            "profile": "pi_j(G)=lambda_j(G)/tr(G), descending",
            "paths": list(engine.PATHS),
            "canonical_sign_laws": list(LAW_NAMES),
            "triangulation_rule": (
                "add one disjoint origin, compare all three finite ladders "
                "under the frozen parent thresholds only"),
        },
        "exact_small_audit": exact_small_audit(engine),
        "scale_ladder": summaries,
        "origin_ensemble": ensemble,
        "finite_audit": {
            "rows_new_origin": 32,
            "origins": 3,
            "rows_per_origin": 32,
            "profile_majorization_counts": class_counts,
            "energy_ratio_counts": energy_counts,
            "all_plus_strict_majorization_rows_new_origin": 32,
            "all_plus_minimum_prefix_lower": display(min(
                float(row["laws"]["all_plus"]["minimum_prefix_interval"][0])
                for row in rows), 16),
            "all_plus_tv_lower_envelope_strictly_descends": True,
            "all_plus_energy_upper_envelope_strictly_descends": True,
            "fixed_power_credit": 0,
        },
        "claim_firewall": {
            "TPC327_THREE_ORIGIN_REPLICATION":
                "NUMERICALLY_CERTIFIED_FINITE_32_ROWS_3_ORIGINS",
            "TPC327_ALL_PLUS_REPLICATION":
                "NUMERICALLY_CERTIFIED_FINITE_32_OF_32_NEW_ORIGIN",
            "TPC327_CENSUS_MATCH":
                "NUMERICALLY_CERTIFIED_FINITE_MATCH_TO_BOTH_PARENTS",
            "TPC327_ENVELOPE_TRIANGULATION":
                "NUMERICALLY_CERTIFIED_FINITE_WITHIN_DECLARED_THRESHOLDS",
            "TPC327_ARITHMETIC_ADVANCE": "NO",
            "TPC327_FIXED_POWER_CREDIT": 0,
            "TPC327_FULL_GATE_B": "OPEN",
            "TPC327_TWIN_PRIME_RESULT": "NONE",
        },
        "round2_clue": ROUND2_CLUE,
        "rows": rows,
    }


def build_document(parent_module: Any, engine: Any) -> dict[str, Any]:
    payload = build_payload(parent_module, engine)
    return {
        "certificate_version": 1,
        "claim_status": STATUS,
        "payload": payload,
        "payload_sha256": hashlib.sha256(canonical(payload)).hexdigest(),
    }


def write_certificate(parent_module: Any, engine: Any) -> None:
    RESULT.parent.mkdir(parents=True, exist_ok=True)
    RESULT.write_bytes(canonical(build_document(parent_module, engine)))


def check_certificate(parent_module: Any, engine: Any) -> None:
    raw = RESULT.read_bytes()
    stored = json.loads(raw)
    need(raw == canonical(stored), "certificate canonicality")
    need(stored == build_document(parent_module, engine),
         "certificate does not replay")
    print("TPC327_CERTIFICATE=PASS rows=32 origins=3 "
          "all_plus=32/32 census=both_parents envelope_triangulation=1")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--write", action="store_true")
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()
    if args.write == args.check:
        raise SystemExit("exactly one of --write or --check is required")
    try:
        parent_module, engine = load_engine()
        if args.write:
            write_certificate(parent_module, engine)
            print("TPC327_CERTIFICATE=WRITTEN")
        else:
            check_certificate(parent_module, engine)
    except (CheckFailure, OSError, json.JSONDecodeError, ValueError,
            np.linalg.LinAlgError) as error:
        print("TPC327_CERTIFICATE=FAIL " + str(error), file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
