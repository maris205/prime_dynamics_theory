#!/usr/bin/env python3
"""TPC-334: support attribution for the source polarization cross term.

TPC-333 found a stable finite cross-term coefficient.  This release asks
which coordinates create <Lambda,b>: twin pairs, non-twin prime shifts,
prime-power shifts, or the zero-support remainder.  The partition is exact
for the declared finite arrays; all proportions are finite observations.
"""

from __future__ import annotations

import argparse
import hashlib
import importlib.util
import json
import math
import sys
from fractions import Fraction
from pathlib import Path
from typing import Any

PROJECT = Path(__file__).resolve().parents[1]
ROOT = PROJECT.parents[1]
RESULT = PROJECT / "results/tpc334_certificate.json"
PARENT_PROJECT = ROOT / "papers/tpc-333-source-polarization-cross-term"
PARENT_CODE = PARENT_PROJECT / "code/tpc333_source_polarization_cross_term.py"
PARENT_CERT = PARENT_PROJECT / "results/tpc333_certificate.json"
PARENT_CODE_SHA256 = "1e8b104db281b6998875f2fb5b4691910c3a22ef365c796bdc879f396f8a6bde"
PARENT_CERT_SHA256 = "3722702ab29b397c836b5ceb4cddd0b063d35e10139952dd93eb849ced2f53eb"
SCHEMA = "TPC334_CROSS_TERM_SUPPORT_LEDGER_V1"
STATUS = "NUMERICALLY_CERTIFIED_FINITE_CROSS_TERM_SUPPORT_LEDGER"
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
         "TPC333 producer provenance")
    need(digest(PARENT_CERT.read_bytes()) == PARENT_CERT_SHA256,
         "TPC333 certificate provenance")
    raw = PARENT_CERT.read_bytes()
    document = json.loads(raw)
    need(raw == canonical(document), "TPC333 canonicality")
    need(document.get("claim_status") ==
         "NUMERICALLY_CERTIFIED_FINITE_SOURCE_POLARIZATION_LEDGER",
         "TPC333 status")
    return document


def parent_source_module() -> Any:
    spec = importlib.util.spec_from_file_location("tpc333_parent", PARENT_CODE)
    need(spec is not None and spec.loader is not None, "parent import spec")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.parent_source_module()


def exact_anchor() -> dict[str, Any]:
    # An explicit rational partition anchor.  The labels are abstract support
    # classes; it proves only additivity of the class masses.
    labels = ["twin_prime", "non_twin_prime_shift", "prime_power_shift",
              "zero_support"]
    lam = [Fraction(2), Fraction(3), Fraction(1), Fraction(4)]
    comp = [Fraction(5), Fraction(1), Fraction(2), Fraction(0)]
    masses = [a * b for a, b in zip(lam, comp)]
    total = sum(masses, Fraction(0))
    grouped = {label: masses[i] for i, label in enumerate(labels)}
    need(sum(grouped.values(), Fraction(0)) == total,
         "exact support partition")
    return {
        "labels": labels,
        "lambda": ["2", "3", "1", "4"],
        "comparison": ["5", "1", "2", "0"],
        "class_masses": {label: {"value": str(grouped[label]),
                                  "digest": hashlib.sha256(
                                      f"{grouped[label].numerator}/{grouped[label].denominator}\n".encode("ascii")).hexdigest()}
                         for label in labels},
        "total_cross_mass": "15",
        "partition_exact": True,
    }


def classify_coordinate(parent: Any, t: int, lambda_value: float,
                        comparison_value: float) -> str:
    cross = lambda_value * comparison_value
    if cross == 0.0:
        return "zero_support"
    shifted = t + 2
    shifted_power = parent.prime_power(shifted)
    if shifted_power is not None and shifted_power[1] == 1:
        return ("twin_prime" if parent.is_prime_small(t)
                else "non_twin_prime_shift")
    if shifted_power is not None and shifted_power[1] >= 2:
        return "prime_power_shift"
    # Under the source definition a nonzero Lambda coordinate must be a
    # prime power.  Keep this branch fail-closed if the model changes.
    raise Failure("nonzero cross coordinate outside declared support")


def source_record(parent: Any, origin: int, scale: int) -> dict[str, Any]:
    lo, hi = origin, origin + scale // 2 - 1
    lam, comp, residual, width = parent.source_vectors(lo, hi)
    masses = {category: 0.0 for category in CATEGORIES}
    counts = {category: 0 for category in CATEGORIES}
    for index, t in enumerate(range(lo, hi + 1)):
        category = classify_coordinate(parent, t, float(lam[index]),
                                       float(comp[index]))
        counts[category] += 1
        masses[category] += float(lam[index] * comp[index])
    total_cross = float(lam @ comp)
    mass_sum = sum(masses.values())
    need(abs(mass_sum - total_cross) <= 2.0e-10 * max(1.0, abs(total_cross)),
         "support mass partition")
    l2 = float(lam @ lam)
    c2 = float(comp @ comp)
    residual_l2 = float(residual @ residual)
    support = {}
    for category in CATEGORIES:
        support[category] = {
            "coordinate_count": counts[category],
            "cross_mass": show(masses[category]),
            "cross_mass_fraction": show(masses[category] / total_cross),
        }
    twin_share = masses["twin_prime"] / total_cross
    non_twin_share = masses["non_twin_prime_shift"] / total_cross
    pp_share = masses["prime_power_shift"] / total_cross
    return {
        "origin": origin,
        "scale": scale,
        "source_interval": [lo, hi],
        "source_count": scale // 2,
        "support": support,
        "total_cross_inner_product": show(total_cross),
        "cross_mass_partition_error": show(abs(mass_sum - total_cross)),
        "twin_cross_mass_fraction": show(twin_share),
        "non_twin_prime_shift_fraction": show(non_twin_share),
        "prime_power_shift_fraction": show(pp_share),
        "lambda_l2": show(l2),
        "comparison_l2": show(c2),
        "residual_l2": show(residual_l2),
        "source_weight_max_interval_width": show(width),
    }


def build_payload() -> dict[str, Any]:
    parent_source = parent_source_module()
    rows = [source_record(parent_source, origin, scale)
            for origin in ORIGINS for scale in SCALES]
    twin = [float(row["twin_cross_mass_fraction"]) for row in rows]
    non_twin = [float(row["non_twin_prime_shift_fraction"]) for row in rows]
    pp = [float(row["prime_power_shift_fraction"]) for row in rows]
    return {
        "schema": SCHEMA,
        "parent_lock": {
            "TPC333_producer_sha256": PARENT_CODE_SHA256,
            "TPC333_certificate_sha256": PARENT_CERT_SHA256,
        },
        "protocol": {
            "origins": list(ORIGINS), "scales": list(SCALES),
            "source_counts": [scale // 2 for scale in SCALES],
            "categories": list(CATEGORIES),
            "support_rule": "cross coordinate = Lambda(t+2)*b(t)",
            "twin_rule": "prime(t) and prime(t+2)",
            "prime_power_rule": "t+2=p^k with k>=2",
            "cutoff": 50000,
        },
        "finite_audit": {
            "windows": len(rows), "categories": len(CATEGORIES),
            "partition_observations": len(rows), "arithmetic_advance": "NO",
            "fixed_power_credit": 0,
        },
        "rows": rows,
        "summary": {
            "twin_fraction_min": show(min(twin)),
            "twin_fraction_max": show(max(twin)),
            "non_twin_fraction_min": show(min(non_twin)),
            "non_twin_fraction_max": show(max(non_twin)),
            "prime_power_fraction_min": show(min(pp)),
            "prime_power_fraction_max": show(max(pp)),
            "twin_fraction_below_0.10": sum(x < .10 for x in twin),
            "non_twin_fraction_above_0.90": sum(x > .90 for x in non_twin),
        },
        "exact_anchor": exact_anchor(),
        "claim_firewall": {
            "TPC334_SUPPORT_PARTITION": "PROVED_EXACT_FINITE_DECLARED_MODEL",
            "TPC334_SIX_WINDOW_REPLAY": "NUMERICALLY_CERTIFIED_FINITE_6_WINDOWS",
            "TPC334_TWIN_SUPPORT_SHARE": "NUMERICALLY_CERTIFIED_FINITE_5.4_TO_7.2_PERCENT",
            "TPC334_NON_TWIN_BACKGROUND": "NUMERICALLY_CERTIFIED_FINITE_92.8_TO_94.6_PERCENT",
            "TPC334_ARITHMETIC_ADVANCE": "NO",
            "TPC334_FIXED_POWER_CREDIT": 0,
            "TPC334_SOURCE_UNIFORM_L2": "OPEN",
            "TPC334_TWIN_PRIME_RESULT": "NONE",
            "TPC334_FULL_GATE_B": "OPEN",
        },
        "round2_clue": "ISOLATE_TWIN_MASK_OR_COMPENSATED_SOURCE_BEFORE_OPERATOR_REASSEMBLY",
    }


def build_document() -> dict[str, Any]:
    load_parent()
    payload = build_payload()
    return {"certificate_version": 1, "claim_status": STATUS,
            "payload": payload,
            "payload_sha256": hashlib.sha256(canonical(payload)).hexdigest()}


def check_document(document: dict[str, Any]) -> None:
    need(document.get("certificate_version") == 1 and
         document.get("claim_status") == STATUS, "TPC334 header")
    payload = document.get("payload")
    need(isinstance(payload, dict) and payload.get("schema") == SCHEMA,
         "TPC334 schema")
    need(document.get("payload_sha256") == hashlib.sha256(
        canonical(payload)).hexdigest(), "TPC334 payload digest")
    need(payload.get("parent_lock") == {
        "TPC333_producer_sha256": PARENT_CODE_SHA256,
        "TPC333_certificate_sha256": PARENT_CERT_SHA256}, "parent lock")
    need(payload.get("finite_audit") == {
        "windows": 6, "categories": 4, "partition_observations": 6,
        "arithmetic_advance": "NO", "fixed_power_credit": 0},
         "finite audit")
    rows = payload.get("rows")
    need(isinstance(rows, list) and len(rows) == 6, "row count")
    parent_source = parent_source_module()
    rebuilt = [source_record(parent_source, o, s)
               for o in ORIGINS for s in SCALES]
    for actual, recorded in zip(rebuilt, rows):
        need(actual.keys() == recorded.keys(), "row fields")
        for key, value in actual.items():
            if isinstance(value, str):
                need(abs(float(value) - float(recorded[key])) <=
                     3.0e-11 * max(1.0, abs(float(value))),
                     "row value " + key)
            else:
                need(value == recorded[key], "row field " + key)
    twin = [float(row["twin_cross_mass_fraction"]) for row in rebuilt]
    non_twin = [float(row["non_twin_prime_shift_fraction"]) for row in rebuilt]
    pp = [float(row["prime_power_shift_fraction"]) for row in rebuilt]
    summary = payload["summary"]
    for key, value in {
        "twin_fraction_min": min(twin), "twin_fraction_max": max(twin),
        "non_twin_fraction_min": min(non_twin),
        "non_twin_fraction_max": max(non_twin),
        "prime_power_fraction_min": min(pp),
        "prime_power_fraction_max": max(pp),
    }.items():
        need(abs(float(summary[key]) - value) <=
             3.0e-11 * max(1.0, abs(value)), "summary " + key)
    need(summary["twin_fraction_below_0.10"] == 6 and
         summary["non_twin_fraction_above_0.90"] == 6, "support census")
    need(payload.get("exact_anchor") == exact_anchor(), "exact anchor")
    firewall = payload.get("claim_firewall", {})
    need(firewall.get("TPC334_ARITHMETIC_ADVANCE") == "NO" and
         firewall.get("TPC334_FIXED_POWER_CREDIT") == 0 and
         firewall.get("TPC334_SOURCE_UNIFORM_L2") == "OPEN",
         "claim firewall")


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
            need(raw == canonical(document), "certificate canonicality")
            load_parent()
            check_document(document)
            print("TPC334_CERTIFICATE=PASS windows=6 categories=4 "
                  "twin_below_10pct=6 non_twin_above_90pct=6 exact_anchor=1")
        return 0
    except (Failure, OSError, ValueError, TypeError, KeyError,
            json.JSONDecodeError) as error:
        print("TPC334_CERTIFICATE=FAIL " + str(error), file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
