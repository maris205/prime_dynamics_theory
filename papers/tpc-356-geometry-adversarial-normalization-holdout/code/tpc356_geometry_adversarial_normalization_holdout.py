#!/usr/bin/env python3
"""TPC-356: geometry-adversarial holdout for a frozen position normalization.

TPC-355 proposed the response-independent congruence
    A# = D_G^(-1/2) A D_G^(-1/2)
with G_u the unsigned mask-energy diagonal.  TPC-356 fixes the rule before
looking at any source response: scan a declared grid of origins, rank origins
by the largest pilot geometry spread max(G)/min(G), and greedily retain three
origins separated by at least 1536.  The selected origins are then replayed
with the complete TPC-355 protocol.

This is a finite adversarial-selection audit.  It does not assert a growing
geometry bound, an arithmetic estimate, a Route-B passage, or a twin-prime
result.
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
    raise SystemExit("TPC356 requires numpy: " + str(error))

PROJECT = Path(__file__).resolve().parents[1]
ROOT = PROJECT.parents[1]
RESULT = PROJECT / "results/tpc356_certificate.json"
PARENT_CODE = ROOT / (
    "papers/tpc-355-position-aware-mask-energy-normalization/code/"
    "tpc355_position_aware_mask_energy_normalization.py")
PARENT_CERT = ROOT / (
    "papers/tpc-355-position-aware-mask-energy-normalization/results/"
    "tpc355_certificate.json")
PARENT_CODE_SHA256 = (
    "b54883cbc2e9e19dd8cf6fbece69ff7752ba805678e0b5b2fcf82949dd42fde9")
PARENT_CERT_SHA256 = (
    "29c5e824b415e675c931396567337cbb583b8f952b489ea2a386a63c649fff7b")
SCHEMA = "TPC356_GEOMETRY_ADVERSARIAL_NORMALIZATION_HOLDOUT_V1"
STATUS = "NUMERICALLY_CERTIFIED_FINITE_GEOMETRY_ADVERSARIAL_NORMALIZATION_HOLDOUT"
ROUND2_CLUE = (
    "TEST_ORIGIN_SCALE_STABILITY_OR_OPERATOR_NORM_CERTIFICATE_BEFORE_"
    "ANY_ARITHMETIC_REASSEMBLY")

PANEL_NAME = "geometry_adversarial_holdout"
CANDIDATE_ORIGINS = tuple(range(38001, 48552, 211))
PILOT_COUNT = 256
SELECTED_COUNT = 3
MIN_SEPARATION = 1536
SELECTED_ORIGINS = (38423, 42010, 45597)
COUNTS = (256, 512, 1024)
Q_ANCHORS = (24, 54, 80)
EXPONENTS = (1, 2)
HEIGHT = 66
COMPARISON_CUTOFF = 2
TAIL_CUTOFF = 50_000
KAPPA_GUARD = 1.0e-7
IDENTITY_TOL = 4.0e-6
LAW_NAMES = ("all_plus", "alternating_index", "mod4_character", "half_split")
EXACT_INTERVAL = (38431, 38444)
EXACT_Q = 4
EXACT_EXPONENT = 1
EXACT_LEFT = (1, -1, 0, 2, -1, 0, 1, 0, 0, -1, 1, 0, 0, 1)
EXACT_RIGHT = (0, 1, 1, -1, 0, 2, 0, -1, 1, 0, -1, 0, 1, 0)


class CheckFailure(RuntimeError):
    pass


def need(condition: bool, message: str) -> None:
    if type(condition) is not bool or not condition:
        raise CheckFailure(message)


def canonical(value: Any) -> bytes:
    return (json.dumps(value, ensure_ascii=True, sort_keys=True,
                       separators=(",", ":")) + "\n").encode("ascii")


def digest(data: bytes) -> str:
    return hashlib.sha256(data.replace(b"\r\n", b"\n").replace(
        b"\r", b"\n")).hexdigest()


def show(value: float, digits: int = 17) -> str:
    return format(float(value), f".{digits}g")


def load_parent_module():
    spec = importlib.util.spec_from_file_location("tpc355_parent", PARENT_CODE)
    need(spec is not None and spec.loader is not None, "parent module spec")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


PARENT = load_parent_module()


def load_parent_payload() -> dict[str, Any]:
    raw = PARENT_CERT.read_bytes()
    need(digest(raw) == PARENT_CERT_SHA256, "TPC355 certificate digest")
    document = json.loads(raw)
    need(raw == canonical(document), "TPC355 certificate canonicality")
    payload = document.get("payload")
    need(isinstance(payload, dict), "TPC355 payload")
    return payload


def geometry_selection() -> tuple[list[dict[str, Any]], list[int]]:
    records: list[dict[str, Any]] = []
    for origin in CANDIDATE_ORIGINS:
        values = np.arange(origin, origin + PILOT_COUNT, dtype=np.int64)
        settings: list[dict[str, Any]] = []
        for q0 in Q_ANCHORS:
            for exponent in EXPONENTS:
                _, _, geometry = PARENT.component_matrices(
                    values, q0, exponent)
                settings.append({
                    "Q": q0,
                    "kernel_exponent": exponent,
                    "spread": show(float(np.max(geometry) /
                                          np.min(geometry))),
                    "coefficient_of_variation": show(
                        float(np.std(geometry) / np.mean(geometry))),
                })
        best = max(settings, key=lambda item: (
            float(item["spread"]), -item["Q"], -item["kernel_exponent"]))
        records.append({
            "origin": origin,
            "pilot_count": PILOT_COUNT,
            "score": best["spread"],
            "max_coefficient_of_variation": show(max(
                float(item["coefficient_of_variation"]) for item in settings)),
            "argmax_Q": best["Q"],
            "argmax_kernel_exponent": best["kernel_exponent"],
            "settings": settings,
        })
    ranked = sorted(records, key=lambda item: (
        -float(item["score"]), item["origin"]))
    chosen: list[int] = []
    for record in ranked:
        if all(abs(record["origin"] - old) >= MIN_SEPARATION
               for old in chosen):
            chosen.append(record["origin"])
        if len(chosen) == SELECTED_COUNT:
            break
    need(tuple(chosen) == SELECTED_ORIGINS, "deterministic selected origins")
    return records, chosen


def row_record(origin: int, count: int, q0: int, exponent: int,
                law: str) -> dict[str, Any]:
    lo, hi = origin, origin + count - 1
    values = np.arange(lo, hi + 1, dtype=np.int64)
    lam, comp, residual, width = PARENT.source_vectors(lo, hi)
    source_denom = float(np.dot(lam, lam) + np.dot(comp, comp))
    source_kappa = 2.0 * float(np.dot(lam, comp)) / source_denom
    primes, matrices, geometry = PARENT.component_matrices(
        values, q0, exponent)
    normalized = matrices[law] / np.sqrt(geometry[:, None] * geometry[None, :])
    return {
        "panel": PANEL_NAME,
        "origin": origin,
        "count": count,
        "source_interval": [lo, hi],
        "source_count": count,
        "Q": q0,
        "kernel_exponent": exponent,
        "law": law,
        "height": HEIGHT,
        "comparison_cutoff": COMPARISON_CUTOFF,
        "shell": primes,
        "shell_cardinality": len(primes),
        "operator_shape": [count, count],
        "source_model": "finite V59 beta=Lambda(t+2)-b^(2)(t)",
        "source_weight_max_interval_width": show(width, 8),
        "unsigned_geometry_energy_min": show(float(np.min(geometry))),
        "unsigned_geometry_energy_max": show(float(np.max(geometry))),
        "raw_metrics": PARENT.polarization(
            matrices[law], lam, comp, residual, source_kappa),
        "normalized_metrics": PARENT.polarization(
            normalized, lam, comp, residual, source_kappa),
    }


def summarize(rows: list[dict[str, Any]], law: str,
              metric: str) -> dict[str, Any]:
    selected = [row for row in rows if row["law"] == law]
    need(len(selected) == 54, "summary census")
    values = [float(row[metric]["output_polarization_kappa"])
              for row in selected]
    fractions = [float(row[metric]["residual_fraction_of_component_sum"])
                 for row in selected]
    return {
        "rows": len(values),
        "positive_alignment": sum(v > KAPPA_GUARD for v in values),
        "negative_alignment": sum(v < -KAPPA_GUARD for v in values),
        "unresolved": sum(abs(v) <= KAPPA_GUARD for v in values),
        "kappa_min": show(min(values)),
        "kappa_max": show(max(values)),
        "kappa_mean": show(sum(values) / len(values)),
        "residual_fraction_min": show(min(fractions)),
        "residual_fraction_max": show(max(fractions)),
    }


def exact_anchor() -> dict[str, Any]:
    values = list(range(EXACT_INTERVAL[0], EXACT_INTERVAL[1] + 1))
    primes = PARENT.shell_for(EXACT_Q)

    def entry(prime: int, u: int, t: int) -> Fraction:
        return PARENT.exact_entry(prime, u, t, EXACT_EXPONENT)

    matrix = [[sum((entry(prime, u, t) for prime in primes),
                   Fraction(0)) for t in values] for u in values]
    geometry = [sum((entry(prime, u, t) ** 2 for prime in primes
                     for t in values), Fraction(0)) for u in values]
    need(all(g > 0 for g in geometry), "exact anchor geometry")
    geometry_digest = hashlib.sha256(canonical([
        f"{value.numerator}/{value.denominator}" for value in geometry
    ])).hexdigest()
    left = [Fraction(v) for v in EXACT_LEFT]
    right = [Fraction(v) for v in EXACT_RIGHT]

    def image(vector: list[Fraction]) -> list[Fraction]:
        return [sum((matrix[i][j] * vector[j]
                     for j in range(len(values))), Fraction(0))
                for i in range(len(values))]

    li, ri = image(left), image(right)
    residual = [a - b for a, b in zip(li, ri)]
    left_energy = sum((v * v for v in li), Fraction(0))
    right_energy = sum((v * v for v in ri), Fraction(0))
    cross = sum((a * b for a, b in zip(li, ri)), Fraction(0))
    residual_energy = sum((v * v for v in residual), Fraction(0))
    need(residual_energy == left_energy + right_energy - 2 * cross,
         "exact anchor polarization")
    return {
        "interval": list(EXACT_INTERVAL),
        "Q": EXACT_Q,
        "shell": primes,
        "exponent": EXACT_EXPONENT,
        "left_vector": list(EXACT_LEFT),
        "right_vector": list(EXACT_RIGHT),
        "left_energy_digest": hashlib.sha256(
            f"{left_energy.numerator}/{left_energy.denominator}\n".encode()
        ).hexdigest(),
        "right_energy_digest": hashlib.sha256(
            f"{right_energy.numerator}/{right_energy.denominator}\n".encode()
        ).hexdigest(),
        "cross_digest": hashlib.sha256(
            f"{cross.numerator}/{cross.denominator}\n".encode()).hexdigest(),
        "residual_energy_digest": hashlib.sha256(
            f"{residual_energy.numerator}/{residual_energy.denominator}\n"
            .encode()).hexdigest(),
        "geometry_digest": geometry_digest,
        "geometry_positive": True,
        "identity_exact": True,
    }


def build_payload() -> dict[str, Any]:
    for path, expected, label in (
        (PARENT_CODE, PARENT_CODE_SHA256, "TPC355 code"),
        (PARENT_CERT, PARENT_CERT_SHA256, "TPC355 certificate")):
        need(path.is_file() and digest(path.read_bytes()) == expected,
             label + " provenance")
    parent = load_parent_payload()
    selection, chosen = geometry_selection()
    rows = [row_record(origin, count, q0, exponent, law)
            for origin in chosen for count in COUNTS for q0 in Q_ANCHORS
            for exponent in EXPONENTS for law in LAW_NAMES]
    need(len(rows) == 216, "row census")
    summaries = {law: {metric: summarize(rows, law, metric)
                       for metric in ("raw_metrics", "normalized_metrics")}
                 for law in LAW_NAMES}
    values = {metric: [float(row[metric]["output_polarization_kappa"])
                       for row in rows]
              for metric in ("raw_metrics", "normalized_metrics")}
    counts = {metric: {
        "positive": sum(v > KAPPA_GUARD for v in vals),
        "negative": sum(v < -KAPPA_GUARD for v in vals),
        "unresolved": sum(abs(v) <= KAPPA_GUARD for v in vals)}
        for metric, vals in values.items()}
    need(counts == {
        "raw_metrics": {"positive": 216, "negative": 0, "unresolved": 0},
        "normalized_metrics": {"positive": 216, "negative": 0,
                               "unresolved": 0}}, "alignment census")
    identity_max = max(float(row[m]["identity_error"]) for row in rows
                       for m in ("raw_metrics", "normalized_metrics"))
    all_plus = summaries["all_plus"]
    raw_min = float(all_plus["raw_metrics"]["kappa_min"])
    norm_min = float(all_plus["normalized_metrics"]["kappa_min"])
    raw_mean = float(all_plus["raw_metrics"]["kappa_mean"])
    norm_mean = float(all_plus["normalized_metrics"]["kappa_mean"])
    need(norm_min > raw_min and norm_mean > raw_mean,
         "scoped all-plus normalization gain")
    parent_summaries = parent.get("panel_summaries", {})
    parent_fresh = parent_summaries["fresh_holdout"]
    parent_higher = parent_summaries["higher_parent"]
    transfer: dict[str, Any] = {}
    for law in LAW_NAMES:
        transfer[law] = {}
        for metric in ("raw_metrics", "normalized_metrics"):
            current = summaries[law][metric]
            transfer[law][metric] = {
                "minus_tpc355_fresh_min": show(
                    float(current["kappa_min"]) -
                    float(parent_fresh[law][metric]["kappa_min"])),
                "minus_tpc355_higher_min": show(
                    float(current["kappa_min"]) -
                    float(parent_higher[law][metric]["kappa_min"])),
                "minus_tpc355_fresh_mean": show(
                    float(current["kappa_mean"]) -
                    float(parent_fresh[law][metric]["kappa_mean"])),
            }
    return {
        "schema": SCHEMA,
        "parent_lock": {
            "TPC355_code_sha256": PARENT_CODE_SHA256,
            "TPC355_certificate_sha256": PARENT_CERT_SHA256,
        },
        "protocol": {
            "panel_name": PANEL_NAME,
            "candidate_origins": list(CANDIDATE_ORIGINS),
            "pilot_count": PILOT_COUNT,
            "selected_origins": list(chosen),
            "selected_count": SELECTED_COUNT,
            "minimum_separation": MIN_SEPARATION,
            "source_counts": list(COUNTS),
            "q_anchors": list(Q_ANCHORS),
            "kernel_exponents": list(EXPONENTS),
            "height": HEIGHT,
            "laws": list(LAW_NAMES),
            "source_cutoff": TAIL_CUTOFF,
            "selection_score": "max over Q,s of max_u G_u/min_u G_u on unsigned pilot geometry",
            "selection_uses_response": False,
            "selection_uses_source": False,
            "operator": "literal deleted-diagonal two-endpoint divisibility-masked shell operator",
            "normalization": "TPC-355 unsigned mask-energy symmetric congruence",
        },
        "selection_audit": {
            "candidate_count": len(selection),
            "ranked_records": selection,
            "selected_origins": chosen,
            "selection_rule": "descending score, origin tie-break, greedy separation >= 1536",
        },
        "exact_theorem": {
            "selection_determinism": "The declared finite scan and greedy rule determine a unique selected-origin triple.",
            "selection_independence": "The score uses only unsigned geometry and is fixed before source responses and sign laws.",
            "diagonal_congruence": "On every replay row, TPC-355's positive geometry diagonal defines a finite real congruence.",
            "polarization": "For either raw or normalized finite operator, the exact finite polarization identity holds.",
            "scope": "finite declared grid, finite rows, and inherited finite V59 source model only",
        },
        "finite_audit": {
            "rows": 216,
            "origins": len(chosen),
            "raw_positive_alignment": counts["raw_metrics"]["positive"],
            "raw_negative_alignment": counts["raw_metrics"]["negative"],
            "normalized_positive_alignment": counts["normalized_metrics"]["positive"],
            "normalized_negative_alignment": counts["normalized_metrics"]["negative"],
            "max_identity_error": show(identity_max),
            "all_plus_raw_min": all_plus["raw_metrics"]["kappa_min"],
            "all_plus_normalized_min": all_plus["normalized_metrics"]["kappa_min"],
            "all_plus_raw_mean": all_plus["raw_metrics"]["kappa_mean"],
            "all_plus_normalized_mean": all_plus["normalized_metrics"]["kappa_mean"],
            "normalization_min_gain": show(norm_min - raw_min),
            "normalization_mean_gain": show(norm_mean - raw_mean),
            "fixed_power_credit": 0,
            "arithmetic_advance": "NO",
        },
        "law_summaries": summaries,
        "transfer_summary": transfer,
        "claim_firewall": {
            "TPC356_GEOMETRY_SELECTION": "PROVED_EXACT_FINITE_DETERMINISTIC",
            "TPC356_SELECTION_RESPONSE_INDEPENDENCE": "PROVED_EXACT_FINITE",
            "TPC356_PANEL_REPLAY": "NUMERICALLY_CERTIFIED_FINITE_216_ROWS",
            "TPC356_RAW_REPLAY": "NUMERICALLY_CERTIFIED_FINITE_216_ROWS",
            "TPC356_NORMALIZED_REPLAY": "NUMERICALLY_CERTIFIED_FINITE_216_ROWS",
            "TPC356_ALL_PLUS_MIN_GAIN": "NUMERICALLY_CERTIFIED_FINITE_SCOPED",
            "TPC356_ALL_PLUS_MEAN_GAIN": "NUMERICALLY_CERTIFIED_FINITE_SCOPED",
            "TPC356_UNIFORM_TRANSFER": "OPEN",
            "TPC356_SOURCE_UNIFORM_L2": "OPEN",
            "TPC356_MASKED_OPERATOR_BOUND": "OPEN",
            "TPC356_ARITHMETIC_ADVANCE": "NO",
            "TPC356_FIXED_POWER_CREDIT": 0,
            "TPC356_FULL_GATE_B": "OPEN",
            "TPC356_TWIN_PRIME_RESULT": "NONE",
            "TPC356_STRONGEST_OBSTRUCTION": "FINITE_ADVERSARIAL_HOLDOUT_DOES_NOT_SUPPLY_A_GROWING_BOUND",
        },
        "exact_anchor": exact_anchor(),
        "row_digest": hashlib.sha256(canonical(rows)).hexdigest(),
        "rows": rows,
        "round2_clue": ROUND2_CLUE,
    }


def document() -> dict[str, Any]:
    payload = build_payload()
    return {"certificate_version": 1, "claim_status": STATUS,
            "payload": payload,
            "payload_sha256": hashlib.sha256(canonical(payload)).hexdigest()}


def write_certificate() -> None:
    RESULT.parent.mkdir(parents=True, exist_ok=True)
    RESULT.write_bytes(canonical(document()))


def check_certificate() -> None:
    raw = RESULT.read_bytes()
    stored = json.loads(raw)
    need(raw == canonical(stored), "certificate canonicality")
    need(stored.get("certificate_version") == 1 and
         stored.get("claim_status") == STATUS, "certificate header")
    payload = stored.get("payload")
    need(isinstance(payload, dict) and
         stored.get("payload_sha256") == hashlib.sha256(
             canonical(payload)).hexdigest(), "payload hash")
    need(payload == build_payload(), "certificate replay")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--write", action="store_true")
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()
    if args.write == args.check:
        raise SystemExit("exactly one of --write or --check is required")
    try:
        if args.write:
            write_certificate()
            print("TPC356_CERTIFICATE=WRITTEN")
        else:
            check_certificate()
            print("TPC356_CERTIFICATE=PASS rows=216 origins=3 "
                  "raw_positive=216/216 normalized_positive=216/216")
    except (CheckFailure, OSError, json.JSONDecodeError, ValueError,
            TypeError, KeyError) as error:
        print("TPC356_CERTIFICATE=FAIL " + str(error), file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
