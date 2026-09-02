#!/usr/bin/env python3
"""TPC-333: a source-only polarization and cross-term ledger.

TPC-332 showed that the control-average decomposition is reproducible while
the source-native residual has mixed signs.  This project isolates the source
identity ||Lambda-b||^2 = ||Lambda||^2 + ||b||^2 - 2 <Lambda,b> on the same
six windows.  It is deliberately source-only: no new operator claim is
smuggled in.  The parent source routine is loaded only after its normalized
hash and certificate lock have been checked.
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
RESULT = PROJECT / "results/tpc333_certificate.json"
PARENT_PROJECT = ROOT / "papers/tpc-332-growing-control-average-ensemble"
PARENT_CODE = PARENT_PROJECT / "code/tpc332_growing_control_average_ensemble.py"
PARENT_CERT = PARENT_PROJECT / "results/tpc332_certificate.json"
PARENT_CODE_SHA256 = "ea742cfaaf7aa2be3c4cfad2ca603baadd65dc77619d8a1ba5ef686dd1fea5d9"
PARENT_CERT_SHA256 = "ddb0c33d09edf648df9a32c0e7cec6e8bac638cae6aba895ebf8084da5d580b9"
SCHEMA = "TPC333_SOURCE_POLARIZATION_CROSS_TERM_V1"
STATUS = "NUMERICALLY_CERTIFIED_FINITE_SOURCE_POLARIZATION_LEDGER"
ORIGINS = (42001, 44001)
SCALES = (2048, 4096, 8192)
RATIO_GUARD = 5.0e-8


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


def fraction_digest(value: Fraction) -> str:
    return hashlib.sha256(
        f"{value.numerator}/{value.denominator}\n".encode("ascii")
    ).hexdigest()


def load_parent() -> dict[str, Any]:
    need(PARENT_CODE.is_file() and
         digest(PARENT_CODE.read_bytes()) == PARENT_CODE_SHA256,
         "TPC332 producer parent lock")
    need(PARENT_CERT.is_file() and
         digest(PARENT_CERT.read_bytes()) == PARENT_CERT_SHA256,
         "TPC332 certificate parent lock")
    raw = PARENT_CERT.read_bytes()
    document = json.loads(raw)
    need(raw == canonical(document), "TPC332 certificate canonicality")
    need(document.get("certificate_version") == 1 and
         document.get("claim_status") ==
         "NUMERICALLY_CERTIFIED_FINITE_GROWING_CONTROL_AVERAGE_ENSEMBLE",
         "TPC332 certificate header")
    payload = document.get("payload")
    need(isinstance(payload, dict) and
         payload.get("schema") ==
         "TPC332_GROWING_CONTROL_AVERAGE_ENSEMBLE_V1",
         "TPC332 payload schema")
    return document


def parent_source_module() -> Any:
    spec = importlib.util.spec_from_file_location("tpc332_parent", PARENT_CODE)
    need(spec is not None and spec.loader is not None, "parent import spec")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def exact_anchor() -> dict[str, Any]:
    lam = [Fraction(3), Fraction(-2), Fraction(5), Fraction(1)]
    comp = [Fraction(1), Fraction(1), Fraction(-1), Fraction(2)]
    beta = [a - b for a, b in zip(lam, comp)]
    l2 = sum((x * x for x in lam), Fraction(0))
    c2 = sum((x * x for x in comp), Fraction(0))
    cross = sum((a * b for a, b in zip(lam, comp)), Fraction(0))
    r2 = sum((x * x for x in beta), Fraction(0))
    need(r2 == l2 + c2 - 2 * cross, "exact polarization anchor")
    return {
        "lambda": ["3", "-2", "5", "1"],
        "comparison": ["1", "1", "-1", "2"],
        "residual": ["2", "-3", "6", "-1"],
        "lambda_l2": {"value": "39", "digest": fraction_digest(l2)},
        "comparison_l2": {"value": "7", "digest": fraction_digest(c2)},
        "cross_inner_product": {"value": "-2", "digest": fraction_digest(cross)},
        "residual_l2": {"value": "50", "digest": fraction_digest(r2)},
        "identity_exact": True,
    }


def source_record(parent: Any, origin: int, scale: int) -> dict[str, Any]:
    lo, hi = origin, origin + scale // 2 - 1
    lam, comp, residual, width = parent.source_vectors(lo, hi)
    lambda_l2 = float(lam @ lam)
    comparison_l2 = float(comp @ comp)
    cross = float(lam @ comp)
    residual_l2 = float(residual @ residual)
    total = lambda_l2 + comparison_l2
    identity_error = abs(residual_l2 - total + 2.0 * cross)
    kappa = 2.0 * cross / total
    residual_fraction = residual_l2 / total
    correlation = cross / math.sqrt(lambda_l2 * comparison_l2)
    need(all(math.isfinite(x) for x in (
        lambda_l2, comparison_l2, cross, residual_l2, identity_error,
        kappa, residual_fraction, correlation)), "finite source record")
    need(lambda_l2 > 0 and comparison_l2 > 0 and residual_l2 > 0,
         "positive source norms")
    return {
        "origin": origin,
        "scale": scale,
        "source_interval": [lo, hi],
        "source_count": scale // 2,
        "lambda_l2": show(lambda_l2),
        "comparison_l2": show(comparison_l2),
        "cross_inner_product": show(cross),
        "residual_l2": show(residual_l2),
        "total_component_l2": show(total),
        "cancellation_coefficient": show(kappa),
        "residual_fraction_of_component_sum": show(residual_fraction),
        "normalized_cross_correlation": show(correlation),
        "identity_error": show(identity_error),
        "source_weight_max_interval_width": show(width),
        "lambda_nonzero": int((lam != 0).sum()),
        "comparison_nonzero": int((comp != 0).sum()),
        "residual_nonzero": int((residual != 0).sum()),
        "cross_positive_coordinate_count": int(((lam * comp) > 0).sum()),
        "cross_negative_coordinate_count": int(((lam * comp) < 0).sum()),
    }


def growth_pairs(rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    pairs: list[dict[str, Any]] = []
    for origin in ORIGINS:
        for small, large in zip(SCALES, SCALES[1:]):
            a = next(r for r in rows if r["origin"] == origin and
                     r["scale"] == small)
            b = next(r for r in rows if r["origin"] == origin and
                     r["scale"] == large)
            pairs.append({
                "origin": origin,
                "small_scale": small,
                "large_scale": large,
                "lambda_l2_growth": show(float(b["lambda_l2"]) /
                                          float(a["lambda_l2"])),
                "comparison_l2_growth": show(float(b["comparison_l2"]) /
                                              float(a["comparison_l2"])),
                "cross_growth": show(float(b["cross_inner_product"]) /
                                     float(a["cross_inner_product"])),
                "residual_l2_growth": show(float(b["residual_l2"]) /
                                            float(a["residual_l2"])),
                "cancellation_coefficient_drift": show(
                    float(b["cancellation_coefficient"]) -
                    float(a["cancellation_coefficient"])),
            })
    return pairs


def build_payload(parent_document: dict[str, Any]) -> dict[str, Any]:
    parent = parent_source_module()
    rows = [source_record(parent, origin, scale)
            for origin in ORIGINS for scale in SCALES]
    pairs = growth_pairs(rows)
    kappas = [float(row["cancellation_coefficient"]) for row in rows]
    fractions = [float(row["residual_fraction_of_component_sum"])
                 for row in rows]
    correlations = [float(row["normalized_cross_correlation"])
                    for row in rows]
    max_error = max(float(row["identity_error"]) for row in rows)
    return {
        "schema": SCHEMA,
        "parent_lock": {
            "TPC332_producer_sha256": PARENT_CODE_SHA256,
            "TPC332_certificate_sha256": PARENT_CERT_SHA256,
        },
        "protocol": {
            "origins": list(ORIGINS),
            "scales": list(SCALES),
            "source_counts": [scale // 2 for scale in SCALES],
            "source_model": "beta_x^(2)(t)=Lambda(t+2)-b_x^(2)(t)",
            "cutoff_inherited_from_parent": 50000,
            "recorded_terms": ["lambda_l2", "comparison_l2",
                               "cross_inner_product", "residual_l2"],
            "guard": "float64 replay; no asymptotic extrapolation",
        },
        "finite_audit": {
            "windows": len(rows),
            "growth_pairs": len(pairs),
            "source_uniform_theorem": "OPEN",
            "arithmetic_advance": "NO",
            "fixed_power_credit": 0,
        },
        "rows": rows,
        "growth_pairs": pairs,
        "summary": {
            "cancellation_coefficient_min": show(min(kappas)),
            "cancellation_coefficient_max": show(max(kappas)),
            "cancellation_coefficient_mean": show(sum(kappas) / len(kappas)),
            "residual_fraction_min": show(min(fractions)),
            "residual_fraction_max": show(max(fractions)),
            "normalized_correlation_min": show(min(correlations)),
            "normalized_correlation_max": show(max(correlations)),
            "max_identity_error": show(max_error),
            "kappa_within_[.35,.37]": sum(.35 < x < .37 for x in kappas),
        },
        "exact_anchor": exact_anchor(),
        "claim_firewall": {
            "TPC333_POLARIZATION_IDENTITY": "PROVED_EXACT_FINITE_DECLARED_MODEL",
            "TPC333_SIX_WINDOW_REPLAY": "NUMERICALLY_CERTIFIED_FINITE_6_WINDOWS",
            "TPC333_CANCELLATION_COEFFICIENT":
                "NUMERICALLY_CERTIFIED_FINITE_0.35_TO_0.37",
            "TPC333_NEAR_ORTHOGONALITY": "REFUTED_SCOPED_FINITE_PANEL",
            "TPC333_SOURCE_UNIFORM_L2": "OPEN",
            "TPC333_ARITHMETIC_ADVANCE": "NO",
            "TPC333_FIXED_POWER_CREDIT": 0,
            "TPC333_FULL_GATE_B": "OPEN",
            "TPC333_TWIN_PRIME_RESULT": "NONE",
        },
        "round2_clue": "CLASSIFY_CROSS_TERM_SUPPORT_BY_PRIME_POWER_AND_TWIN_MASK",
    }


def build_document() -> dict[str, Any]:
    parent = load_parent()
    payload = build_payload(parent["payload"])
    return {
        "certificate_version": 1,
        "claim_status": STATUS,
        "payload": payload,
        "payload_sha256": hashlib.sha256(canonical(payload)).hexdigest(),
    }


def check_document(document: dict[str, Any]) -> None:
    need(document.get("certificate_version") == 1 and
         document.get("claim_status") == STATUS, "TPC333 header")
    payload = document.get("payload")
    need(isinstance(payload, dict) and payload.get("schema") == SCHEMA,
         "TPC333 schema")
    need(document.get("payload_sha256") ==
         hashlib.sha256(canonical(payload)).hexdigest(),
         "TPC333 payload digest")
    need(payload.get("parent_lock") == {
        "TPC332_producer_sha256": PARENT_CODE_SHA256,
        "TPC332_certificate_sha256": PARENT_CERT_SHA256,
    }, "TPC333 parent lock")
    need(payload.get("finite_audit") == {
        "windows": 6, "growth_pairs": 4,
        "source_uniform_theorem": "OPEN", "arithmetic_advance": "NO",
        "fixed_power_credit": 0}, "TPC333 finite audit")
    rows = payload.get("rows")
    need(isinstance(rows, list) and len(rows) == 6, "TPC333 row count")
    expected = {(o, s) for o in ORIGINS for s in SCALES}
    need({(r.get("origin"), r.get("scale")) for r in rows} == expected,
         "TPC333 row geometry")
    parent = parent_source_module()
    rebuilt = [source_record(parent, o, s) for o in ORIGINS for s in SCALES]
    for actual, recorded in zip(rebuilt, rows):
        need(actual.keys() == recorded.keys(), "TPC333 row fields")
        for key, value in actual.items():
            if isinstance(value, str):
                need(abs(float(value) - float(recorded[key])) <
                     2.0e-12 * max(1.0, abs(float(value))),
                     "TPC333 row value " + key)
            else:
                need(value == recorded[key], "TPC333 row field " + key)
    pairs = growth_pairs(rebuilt)
    need(payload.get("growth_pairs") == pairs, "TPC333 growth ledger")
    kappa = [float(r["cancellation_coefficient"]) for r in rebuilt]
    summary = payload.get("summary", {})
    for key, value in {
        "cancellation_coefficient_min": min(kappa),
        "cancellation_coefficient_max": max(kappa),
        "cancellation_coefficient_mean": sum(kappa) / len(kappa),
        "residual_fraction_min": min(float(r["residual_fraction_of_component_sum"]) for r in rebuilt),
        "residual_fraction_max": max(float(r["residual_fraction_of_component_sum"]) for r in rebuilt),
        "normalized_correlation_min": min(float(r["normalized_cross_correlation"]) for r in rebuilt),
        "normalized_correlation_max": max(float(r["normalized_cross_correlation"]) for r in rebuilt),
        "max_identity_error": max(float(r["identity_error"]) for r in rebuilt),
    }.items():
        need(abs(float(summary[key]) - value) < 2.0e-12 * max(1.0, abs(value)),
             "TPC333 summary " + key)
    need(summary.get("kappa_within_[.35,.37]") == 6,
         "TPC333 kappa interval census")
    need(payload.get("exact_anchor") == exact_anchor(), "TPC333 exact anchor")
    need(payload.get("claim_firewall") == {
        "TPC333_POLARIZATION_IDENTITY": "PROVED_EXACT_FINITE_DECLARED_MODEL",
        "TPC333_SIX_WINDOW_REPLAY": "NUMERICALLY_CERTIFIED_FINITE_6_WINDOWS",
        "TPC333_CANCELLATION_COEFFICIENT":
            "NUMERICALLY_CERTIFIED_FINITE_0.35_TO_0.37",
        "TPC333_NEAR_ORTHOGONALITY": "REFUTED_SCOPED_FINITE_PANEL",
        "TPC333_SOURCE_UNIFORM_L2": "OPEN", "TPC333_ARITHMETIC_ADVANCE": "NO",
        "TPC333_FIXED_POWER_CREDIT": 0, "TPC333_FULL_GATE_B": "OPEN",
        "TPC333_TWIN_PRIME_RESULT": "NONE",
    }, "TPC333 firewall")
    need(payload.get("round2_clue") ==
         "CLASSIFY_CROSS_TERM_SUPPORT_BY_PRIME_POWER_AND_TWIN_MASK",
         "TPC333 clue")


def write_document() -> None:
    document = build_document()
    RESULT.write_bytes(canonical(document))


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--write", action="store_true")
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()
    if args.write:
        write_document()
    if not args.check:
        return 0
    try:
        load_parent()
        raw = RESULT.read_bytes()
        document = json.loads(raw)
        need(raw == canonical(document), "TPC333 certificate canonicality")
        check_document(document)
        print("TPC333_CERTIFICATE=PASS windows=6 growth_pairs=4 "
              "kappa_interval_census=6 exact_anchor=1")
        return 0
    except (Failure, OSError, ValueError, TypeError, json.JSONDecodeError) as error:
        print("TPC333_CERTIFICATE=FAIL " + str(error), file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
