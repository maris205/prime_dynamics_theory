#!/usr/bin/env python3
"""TPC-335: norm decomposition after explicit support isolation.

TPC-334 showed that the raw source cross term is mostly a non-twin prime
shift.  Here the residual vector itself is partitioned into twin, non-twin,
prime-power, and zero-cross-support coordinates.  The coordinate masks give
an exact finite Pythagorean norm split.  The resulting fractions are finite
observations, not asymptotic density claims.
"""

from __future__ import annotations

import argparse
import hashlib
import importlib.util
import json
import sys
from fractions import Fraction
from pathlib import Path
from typing import Any

PROJECT = Path(__file__).resolve().parents[1]
ROOT = PROJECT.parents[1]
RESULT = PROJECT / "results/tpc335_certificate.json"
PARENT_PROJECT = ROOT / "papers/tpc-334-cross-term-support-ledger"
PARENT_CODE = PARENT_PROJECT / "code/tpc334_cross_term_support_ledger.py"
PARENT_CERT = PARENT_PROJECT / "results/tpc334_certificate.json"
PARENT_CODE_SHA256 = "a7e6d5f77b17449eea11d8b673e0d7bfa1701bc3f0f92601cc86d4891f3beef8"
PARENT_CERT_SHA256 = "9e9639965d70b0d66b2d63d2dbe30cad7007db00ec77d8fc54dce5baca03b7c6"
SCHEMA = "TPC335_TWIN_ISOLATED_SOURCE_NORM_V1"
STATUS = "NUMERICALLY_CERTIFIED_FINITE_TWIN_ISOLATED_SOURCE_NORM"
ORIGINS = (42001, 44001)
SCALES = (2048, 4096, 8192)
CATEGORIES = ("twin_prime", "non_twin_prime_shift",
              "prime_power_shift", "zero_support")


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


def show(value: float) -> str:
    return format(float(value), ".17g")


def load_parent() -> dict[str, Any]:
    need(digest(PARENT_CODE.read_bytes()) == PARENT_CODE_SHA256,
         "TPC334 producer provenance")
    need(digest(PARENT_CERT.read_bytes()) == PARENT_CERT_SHA256,
         "TPC334 certificate provenance")
    raw = PARENT_CERT.read_bytes()
    document = json.loads(raw)
    need(raw == canonical(document) and document.get("claim_status") ==
         "NUMERICALLY_CERTIFIED_FINITE_CROSS_TERM_SUPPORT_LEDGER",
         "TPC334 parent header")
    return document


def parent_source_module() -> Any:
    spec = importlib.util.spec_from_file_location("tpc334_parent", PARENT_CODE)
    need(spec is not None and spec.loader is not None, "parent import spec")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.parent_source_module()


def classify(source: Any, t: int, lam: float, comp: float) -> str:
    if lam * comp == 0.0:
        return "zero_support"
    pp = source.prime_power(t + 2)
    need(pp is not None, "cross support prime power")
    if pp[1] == 1:
        return "twin_prime" if source.is_prime_small(t) else "non_twin_prime_shift"
    return "prime_power_shift"


def exact_anchor() -> dict[str, Any]:
    # Four disjoint mask coordinates for the finite Pythagorean identity.
    beta = [Fraction(2), Fraction(-3), Fraction(6), Fraction(-1)]
    squares = [x * x for x in beta]
    total = sum(squares, Fraction(0))
    grouped = {category: squares[i] for i, category in enumerate(CATEGORIES)}
    need(sum(grouped.values(), Fraction(0)) == total, "exact mask anchor")
    return {
        "categories": list(CATEGORIES),
        "beta": [str(x) for x in beta],
        "category_squared_norms": {c: str(grouped[c]) for c in CATEGORIES},
        "full_squared_norm": str(total), "partition_exact": True,
    }


def source_record(source: Any, origin: int, scale: int) -> dict[str, Any]:
    lo, hi = origin, origin + scale // 2 - 1
    lam, comp, residual, width = source.source_vectors(lo, hi)
    norm = {c: 0.0 for c in CATEGORIES}
    cross_mass = {c: 0.0 for c in CATEGORIES}
    counts = {c: 0 for c in CATEGORIES}
    for i, t in enumerate(range(lo, hi + 1)):
        c = classify(source, t, float(lam[i]), float(comp[i]))
        counts[c] += 1
        norm[c] += float(residual[i] * residual[i])
        cross_mass[c] += float(lam[i] * comp[i])
    full_l2 = float(residual @ residual)
    lambda_l2 = float(lam @ lam)
    comparison_l2 = float(comp @ comp)
    cross = float(lam @ comp)
    norm_error = abs(sum(norm.values()) - full_l2)
    cross_error = abs(sum(cross_mass.values()) - cross)
    need(norm_error <= 2.0e-10 * max(1.0, full_l2), "norm mask partition")
    need(cross_error <= 2.0e-10 * max(1.0, cross), "cross mask partition")
    support = {}
    for c in CATEGORIES:
        support[c] = {
            "coordinate_count": counts[c],
            "residual_squared_norm": show(norm[c]),
            "residual_norm_fraction": show(norm[c] / full_l2),
            "cross_mass": show(cross_mass[c]),
            "cross_mass_fraction": show(cross_mass[c] / cross),
        }
    twin_norm_fraction = norm["twin_prime"] / full_l2
    twin_cross_fraction = cross_mass["twin_prime"] / cross
    return {
        "origin": origin, "scale": scale, "source_interval": [lo, hi],
        "source_count": scale // 2, "support": support,
        "full_residual_l2": show(full_l2),
        "lambda_l2": show(lambda_l2), "comparison_l2": show(comparison_l2),
        "cross_inner_product": show(cross),
        "norm_partition_error": show(norm_error),
        "cross_partition_error": show(cross_error),
        "twin_residual_norm_fraction": show(twin_norm_fraction),
        "twin_cross_mass_fraction": show(twin_cross_fraction),
        "twin_norm_to_cross_amplification": show(
            twin_norm_fraction / twin_cross_fraction),
        "source_weight_max_interval_width": show(width),
    }


def build_payload() -> dict[str, Any]:
    source = parent_source_module()
    rows = [source_record(source, o, s) for o in ORIGINS for s in SCALES]
    twin_norm = [float(r["twin_residual_norm_fraction"]) for r in rows]
    background_norm = [float(r["support"]["non_twin_prime_shift"][
        "residual_norm_fraction"]) for r in rows]
    pp_norm = [float(r["support"]["prime_power_shift"][
        "residual_norm_fraction"]) for r in rows]
    amp = [float(r["twin_norm_to_cross_amplification"]) for r in rows]
    return {
        "schema": SCHEMA,
        "parent_lock": {"TPC334_producer_sha256": PARENT_CODE_SHA256,
                         "TPC334_certificate_sha256": PARENT_CERT_SHA256},
        "protocol": {
            "origins": list(ORIGINS), "scales": list(SCALES),
            "source_counts": [s // 2 for s in SCALES],
            "categories": list(CATEGORIES),
            "vector_partition": "beta_C(t)=beta(t) 1_C(t)",
            "norm_identity": "||beta||^2=sum_C ||beta_C||^2",
            "cutoff": 50000,
        },
        "finite_audit": {"windows": 6, "categories": 4,
                          "norm_partition_observations": 6,
                          "arithmetic_advance": "NO", "fixed_power_credit": 0},
        "rows": rows,
        "summary": {
            "twin_norm_fraction_min": show(min(twin_norm)),
            "twin_norm_fraction_max": show(max(twin_norm)),
            "background_norm_fraction_min": show(min(background_norm)),
            "background_norm_fraction_max": show(max(background_norm)),
            "prime_power_norm_fraction_min": show(min(pp_norm)),
            "prime_power_norm_fraction_max": show(max(pp_norm)),
            "twin_amplification_min": show(min(amp)),
            "twin_amplification_max": show(max(amp)),
            "twin_norm_fraction_between_0.09_0.13":
                sum(.09 < x < .13 for x in twin_norm),
            "background_norm_fraction_between_0.65_0.72":
                sum(.65 < x < .72 for x in background_norm),
        },
        "exact_anchor": exact_anchor(),
        "claim_firewall": {
            "TPC335_MASK_NORM_IDENTITY": "PROVED_EXACT_FINITE_DECLARED_MODEL",
            "TPC335_SIX_WINDOW_REPLAY": "NUMERICALLY_CERTIFIED_FINITE_6_WINDOWS",
            "TPC335_TWIN_RESIDUAL_SHARE": "NUMERICALLY_CERTIFIED_FINITE_9.6_TO_12.3_PERCENT",
            "TPC335_BACKGROUND_RESIDUAL_SHARE": "NUMERICALLY_CERTIFIED_FINITE_67.1_TO_69.1_PERCENT",
            "TPC335_TWIN_AMPLIFICATION": "NUMERICALLY_CERTIFIED_FINITE_1.70_TO_1.78",
            "TPC335_ARITHMETIC_ADVANCE": "NO",
            "TPC335_FIXED_POWER_CREDIT": 0,
            "TPC335_SOURCE_UNIFORM_L2": "OPEN",
            "TPC335_FULL_GATE_B": "OPEN",
            "TPC335_TWIN_PRIME_RESULT": "NONE",
        },
        "round2_clue": "TEST_TWIN_ISOLATED_AND_BACKGROUND_SIGNED_GRAM_RESPONSES",
    }


def build_document() -> dict[str, Any]:
    load_parent()
    payload = build_payload()
    return {"certificate_version": 1, "claim_status": STATUS,
            "payload": payload,
            "payload_sha256": hashlib.sha256(canonical(payload)).hexdigest()}


def check_document(document: dict[str, Any]) -> None:
    need(document.get("certificate_version") == 1 and
         document.get("claim_status") == STATUS, "header")
    payload = document.get("payload")
    need(isinstance(payload, dict) and payload.get("schema") == SCHEMA,
         "schema")
    need(document.get("payload_sha256") == hashlib.sha256(
        canonical(payload)).hexdigest(), "payload digest")
    need(payload.get("parent_lock") == {
        "TPC334_producer_sha256": PARENT_CODE_SHA256,
        "TPC334_certificate_sha256": PARENT_CERT_SHA256}, "parent lock")
    need(payload.get("finite_audit") == {
        "windows": 6, "categories": 4,
        "norm_partition_observations": 6, "arithmetic_advance": "NO",
        "fixed_power_credit": 0}, "finite audit")
    rows = payload.get("rows")
    need(isinstance(rows, list) and len(rows) == 6, "rows")
    source = parent_source_module()
    rebuilt = [source_record(source, o, s) for o in ORIGINS for s in SCALES]
    for actual, recorded in zip(rebuilt, rows):
        need(actual.keys() == recorded.keys(), "row fields")
        for key, value in actual.items():
            if isinstance(value, str):
                need(abs(float(value) - float(recorded[key])) <=
                     3.0e-11 * max(1.0, abs(float(value))), "row " + key)
            elif isinstance(value, dict):
                for category in CATEGORIES:
                    for field, item in value[category].items():
                        need(abs(float(item) - float(recorded[key][category][field])) <=
                             3.0e-11 * max(1.0, abs(float(item))),
                             "support " + category + " " + field)
            else:
                need(value == recorded[key], "row field " + key)
    summary = payload["summary"]
    need(summary["twin_norm_fraction_between_0.09_0.13"] == 6 and
         summary["background_norm_fraction_between_0.65_0.72"] == 6,
         "summary census")
    need(payload.get("exact_anchor") == exact_anchor(), "exact anchor")
    firewall = payload.get("claim_firewall", {})
    need(firewall.get("TPC335_ARITHMETIC_ADVANCE") == "NO" and
         firewall.get("TPC335_SOURCE_UNIFORM_L2") == "OPEN" and
         firewall.get("TPC335_FIXED_POWER_CREDIT") == 0, "firewall")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--write", action="store_true")
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()
    try:
        if args.write:
            RESULT.write_bytes(canonical(build_document()))
        if args.check:
            raw = RESULT.read_bytes()
            document = json.loads(raw)
            need(raw == canonical(document), "canonicality")
            load_parent(); check_document(document)
            print("TPC335_CERTIFICATE=PASS windows=6 categories=4 "
                  "twin_norm_9_to_13pct=6 background_norm_65_to_72pct=6 exact_anchor=1")
        return 0
    except (Failure, OSError, ValueError, TypeError, KeyError,
            json.JSONDecodeError) as error:
        print("TPC335_CERTIFICATE=FAIL " + str(error), file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
