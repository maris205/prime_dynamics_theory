#!/usr/bin/env python3
"""TPC-359: a response-blind, high-origin geometry-adversarial holdout.

The preceding fresh-origin audit transferred finite normalized caps but did not
test an origin panel selected for unusually uneven unsigned geometry.  This
release fixes that selection rule before reading any signed matrix or source
response, then replays the same finite operator protocol.  Every statement is
scoped to the declared finite panel.
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

import numpy as np

PROJECT = Path(__file__).resolve().parents[1]
ROOT = PROJECT.parents[1]
RESULT = PROJECT / "results/tpc359_certificate.json"
BASE_CODE = ROOT / ("papers/tpc-355-position-aware-mask-energy-normalization/"
                    "code/tpc355_position_aware_mask_energy_normalization.py")
PARENT_CODE = ROOT / ("papers/tpc-358-fresh-origin-spectral-holdout/code/"
                      "tpc358_fresh_origin_spectral_holdout.py")
PARENT_CERT = ROOT / ("papers/tpc-358-fresh-origin-spectral-holdout/results/"
                      "tpc358_certificate.json")
BASE_CODE_SHA256 = "b54883cbc2e9e19dd8cf6fbece69ff7752ba805678e0b5b2fcf82949dd42fde9"
PARENT_CODE_SHA256 = "4bb40fc4a7aa7da4f222cb35bc2f1f5c115ff6ac03f374bcd1f7ef9204fd29e9"
PARENT_CERT_SHA256 = "d87b1e0d2516d2476b44e780cc21f793ab7d3df11fd9d150cb3f8a48facac8f3"

SCHEMA = "TPC359_GEOMETRY_ADVERSARIAL_HIGH_ORIGIN_HOLDOUT_V1"
STATUS = "NUMERICALLY_CERTIFIED_FINITE_GEOMETRY_ADVERSARIAL_HIGH_ORIGIN_HOLDOUT"
ROUND2_CLUE = "TEST_SCHUR_TIGHTNESS_AND_INDEPENDENT_HIGH_ORIGIN_REPLICATION"

# These constants are frozen before any signed matrix, source value, or
# eigenvalue is read.  The pilot sees only the unsigned geometry diagonal.
CANDIDATE_ORIGINS = tuple(range(260001, 270552, 211))
PILOT_COUNT = 256
SELECTED_COUNT = 3
MIN_SEPARATION = 1536
ORIGINS = (267175, 261267, 269074)
COUNTS = (256, 512, 1024, 2048)
Q_ANCHORS = (24, 54, 80)
EXPONENTS = (1, 2)
LAW_NAMES = ("all_plus", "alternating_index", "mod4_character", "half_split")
SPECTRAL_LAWS = ("all_plus",)
HEIGHT = 66
SCALE_GUARD = 1.0e-6
BOUND_TOL = 2.0e-10
TRANSFER_TOL = 1.0e-3
# A short rational anchor is offset from the first selected origin so every
# coordinate has a nonzero Q=4 shell geometry contribution.
EXACT_INTERVAL = (267205, 267218)
EXACT_Q = 4
EXACT_EXPONENT = 1


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


def show(value: float) -> str:
    return format(float(value), ".17g")


def load_base():
    spec = importlib.util.spec_from_file_location("tpc355_base_tpc359", BASE_CODE)
    need(spec is not None and spec.loader is not None, "base module")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


BASE = load_base()


def load_parent() -> dict[str, Any]:
    raw = PARENT_CERT.read_bytes()
    need(digest(raw) == PARENT_CERT_SHA256, "parent certificate provenance")
    document = json.loads(raw)
    need(raw == canonical(document), "parent certificate canonicality")
    payload = document.get("payload")
    need(isinstance(payload, dict), "parent payload")
    return payload


def geometry_selection() -> tuple[list[dict[str, Any]], list[int]]:
    records: list[dict[str, Any]] = []
    for origin in CANDIDATE_ORIGINS:
        values = np.arange(origin, origin + PILOT_COUNT, dtype=np.int64)
        settings: list[dict[str, Any]] = []
        for q0 in Q_ANCHORS:
            for exponent in EXPONENTS:
                _, _, geometry = BASE.component_matrices(values, q0, exponent)
                settings.append({
                    "Q": q0,
                    "kernel_exponent": exponent,
                    "spread": show(np.max(geometry) / np.min(geometry)),
                    "coefficient_of_variation": show(
                        np.std(geometry) / np.mean(geometry)),
                })
        best = max(settings, key=lambda item: (
            float(item["spread"]), -item["Q"], -item["kernel_exponent"]))
        records.append({
            "origin": origin, "pilot_count": PILOT_COUNT,
            "score": best["spread"],
            "max_coefficient_of_variation": show(max(
                float(item["coefficient_of_variation"]) for item in settings)),
            "argmax_Q": best["Q"],
            "argmax_kernel_exponent": best["kernel_exponent"],
            "settings": settings,
        })
    ranked = sorted(records, key=lambda item: (-float(item["score"]),
                                                item["origin"]))
    chosen: list[int] = []
    for record in ranked:
        if all(abs(record["origin"] - old) >= MIN_SEPARATION for old in chosen):
            chosen.append(record["origin"])
        if len(chosen) == SELECTED_COUNT:
            break
    need(tuple(chosen) == ORIGINS, "selected-origin rule")
    return records, chosen


def metrics(matrix: np.ndarray, spectrum: bool) -> dict[str, Any]:
    symmetry = float(np.max(np.abs(matrix - matrix.T)))
    need(math.isfinite(symmetry) and symmetry <= 1.0e-12, "symmetry")
    schur = float(np.max(np.sum(np.abs(matrix), axis=1)))
    frob = float(np.sqrt(np.sum(matrix * matrix)))
    need(math.isfinite(schur) and math.isfinite(frob) and schur > 0 and frob > 0,
         "finite envelope")
    out: dict[str, Any] = {
        "schur": show(schur), "frobenius": show(frob),
        "symmetry_error": show(symmetry), "spectral": None,
        "minimum_eigenvalue": None, "maximum_eigenvalue": None,
        "spectral_over_schur": None, "spectral_over_frobenius": None,
    }
    if spectrum:
        eigenvalues = np.linalg.eigvalsh(matrix)
        lo, hi = float(eigenvalues[0]), float(eigenvalues[-1])
        spectral = max(abs(lo), abs(hi))
        need(math.isfinite(spectral) and spectral > 0, "spectrum")
        need(spectral <= schur + BOUND_TOL * max(1.0, schur) and
             spectral <= frob + BOUND_TOL * max(1.0, frob), "finite bounds")
        out.update({"spectral": show(spectral),
                    "minimum_eigenvalue": show(lo),
                    "maximum_eigenvalue": show(hi),
                    "spectral_over_schur": show(spectral / schur),
                    "spectral_over_frobenius": show(spectral / frob)})
    return out


def build_rows() -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for origin in ORIGINS:
        for count in COUNTS:
            values = np.arange(origin, origin + count, dtype=np.int64)
            for q0 in Q_ANCHORS:
                for exponent in EXPONENTS:
                    primes, matrices, geometry = BASE.component_matrices(
                        values, q0, exponent)
                    scale = np.sqrt(geometry[:, None] * geometry[None, :])
                    for law in LAW_NAMES:
                        spectral = law in SPECTRAL_LAWS
                        normalized = matrices[law] / scale
                        rows.append({
                            "origin": origin, "count": count,
                            "interval": [origin, origin + count - 1],
                            "Q": q0, "kernel_exponent": exponent,
                            "law": law, "height": HEIGHT,
                            "shell": primes, "shell_cardinality": len(primes),
                            "geometry_min": show(np.min(geometry)),
                            "geometry_max": show(np.max(geometry)),
                            "geometry_spread": show(np.max(geometry) /
                                                     np.min(geometry)),
                            "raw": metrics(matrices[law], spectral),
                            "normalized": metrics(normalized, spectral),
                        })
    need(len(rows) == 288, "row census")
    return rows


def transition_audit(rows: list[dict[str, Any]]) -> dict[str, Any]:
    lookup = {(r["origin"], r["count"], r["Q"], r["kernel_exponent"]): r
              for r in rows if r["law"] == "all_plus"}
    census = {"increase": 0, "decrease": 0, "flat": 0}
    sequences = []
    for origin in ORIGINS:
        for q0 in Q_ANCHORS:
            for exponent in EXPONENTS:
                values = [float(lookup[(origin, n, q0, exponent)]
                                ["normalized"]["spectral"])
                          for n in COUNTS]
                labels = []
                for left, right in zip(values, values[1:]):
                    delta = right - left
                    label = ("increase" if delta > SCALE_GUARD else
                             "decrease" if delta < -SCALE_GUARD else "flat")
                    census[label] += 1
                    labels.append(label)
                sequences.append({"origin": origin, "Q": q0,
                                  "kernel_exponent": exponent,
                                  "values": [show(v) for v in values],
                                  "classifications": labels})
    need(sum(census.values()) == 54, "transition census")
    need(census["increase"] > 0 and census["decrease"] > 0,
         "nonmonotone ladder")
    return {"guard": show(SCALE_GUARD), "census": census,
            "sequences": sequences}


def exact_anchor() -> dict[str, Any]:
    values = list(range(EXACT_INTERVAL[0], EXACT_INTERVAL[1] + 1))
    primes = BASE.shell_for(EXACT_Q)
    matrix = [[sum((BASE.exact_entry(p, u, t, EXACT_EXPONENT)
                    for p in primes), Fraction(0)) for t in values]
              for u in values]
    geometry = [sum((BASE.exact_entry(p, u, t, EXACT_EXPONENT) ** 2
                     for p in primes for t in values), Fraction(0))
                for u in values]
    need(all(matrix[i][j] == matrix[j][i]
             for i in range(len(values)) for j in range(len(values))),
         "exact symmetry")
    need(all(g > 0 for g in geometry), "exact geometry")
    text = lambda x: f"{x.numerator}/{x.denominator}"
    return {"interval": list(EXACT_INTERVAL), "Q": EXACT_Q,
            "shell": primes, "kernel_exponent": EXACT_EXPONENT,
            "geometry_positive": True, "matrix_symmetric": True,
            "row_sums_digest": hashlib.sha256(canonical([
                [text(abs(x)) for x in row] for row in matrix])).hexdigest(),
            "geometry_digest": hashlib.sha256(canonical(
                [text(x) for x in geometry])).hexdigest()}


def build_payload() -> dict[str, Any]:
    for path, expected, label in ((BASE_CODE, BASE_CODE_SHA256, "base"),
                                  (PARENT_CODE, PARENT_CODE_SHA256, "parent code"),
                                  (PARENT_CERT, PARENT_CERT_SHA256, "parent cert")):
        need(path.is_file() and digest(path.read_bytes()) == expected,
             label + " provenance")
    parent = load_parent()
    selection, chosen = geometry_selection()
    rows = build_rows()
    transitions = transition_audit(rows)
    normalized_schur = max(float(r["normalized"]["schur"]) for r in rows)
    normalized_spectral = max(float(r["normalized"]["spectral"])
                              for r in rows if r["law"] == "all_plus")
    raw_spectral = max(float(r["raw"]["spectral"])
                       for r in rows if r["law"] == "all_plus")
    parent_audit = parent["finite_audit"]
    parent_schur = float(parent_audit["normalized_schur_max"])
    parent_spectral = float(parent_audit["normalized_all_plus_spectral_max"])
    need(normalized_schur < 0.83 and normalized_spectral < 0.64,
         "finite cap thresholds")
    need(raw_spectral > 1200.0, "raw scale witness")
    need(abs(normalized_schur - parent_schur) <= TRANSFER_TOL and
         abs(normalized_spectral - parent_spectral) <= TRANSFER_TOL,
         "parent transfer")
    audit = {
        "rows": len(rows), "origins": len(ORIGINS),
        "origin_span": max(ORIGINS) - min(ORIGINS),
        "candidate_count": len(CANDIDATE_ORIGINS),
        "pilot_count": PILOT_COUNT,
        "normalized_schur_max": show(normalized_schur),
        "normalized_schur_cap": "0.83",
        "normalized_all_plus_spectral_max": show(normalized_spectral),
        "normalized_all_plus_spectral_cap": "0.64",
        "raw_all_plus_spectral_max": show(raw_spectral),
        "raw_scale_marker": "1200",
        "parent_normalized_schur_max": show(parent_schur),
        "parent_normalized_spectral_max": show(parent_spectral),
        "transfer_tolerance": show(TRANSFER_TOL),
        "finite_schur_violations": 0, "finite_frobenius_violations": 0,
        "normalized_spectral_transitions": transitions["census"],
        "fixed_power_credit": 0, "arithmetic_advance": "NO",
    }
    return {
        "schema": SCHEMA, "status": STATUS,
        "parent_lock": {"base_code_sha256": BASE_CODE_SHA256,
                         "parent_code_sha256": PARENT_CODE_SHA256,
                         "parent_certificate_sha256": PARENT_CERT_SHA256},
        "protocol": {
            "candidate_origins": list(CANDIDATE_ORIGINS),
            "candidate_rule": "260001+211j, 0<=j<=50",
            "pilot_count": PILOT_COUNT, "selection_score":
            "max unsigned geometry spread over Q=24,54,80 and exponents=1,2",
            "minimum_separation": MIN_SEPARATION,
            "origins": list(ORIGINS), "counts": list(COUNTS),
            "q_anchors": list(Q_ANCHORS), "kernel_exponents": list(EXPONENTS),
            "height": HEIGHT, "laws": list(LAW_NAMES),
            "spectral_laws": list(SPECTRAL_LAWS),
            "source_response_used": False, "sign_response_used": False,
            "operator": "literal deleted-diagonal two-endpoint divisibility-masked prime-shell operator",
            "normalization": "unsigned mask-energy symmetric congruence",
        },
        "selection": {"selected_origins": chosen, "records": selection},
        "exact_theorem": {
            "schur": "For finite real symmetric T, ||T||_2 <= max_u sum_t |T(u,t)|.",
            "frobenius": "For finite real T, ||T||_2 <= ||T||_F.",
            "scope": "finite declared matrices; no growing or arithmetic conclusion",
        },
        "finite_audit": audit,
        "transition_audit": transitions,
        "rows": rows,
        "row_digest": hashlib.sha256(canonical(rows)).hexdigest(),
        "exact_anchor": exact_anchor(),
        "claim_firewall": {
            "TPC359_GEOMETRY_SELECTION": "PROVED_EXACT_FINITE_RESPONSE_BLIND",
            "TPC359_HIGH_ORIGIN_REPLAY": "NUMERICALLY_CERTIFIED_FINITE_288_ROWS",
            "TPC359_FINITE_SCHUR_ENVELOPE": "PROVED_EXACT_FINITE",
            "TPC359_FINITE_FROBENIUS_ENVELOPE": "PROVED_EXACT_FINITE",
            "TPC359_PARENT_CAP_TRANSFER": "NUMERICALLY_CERTIFIED_FINITE_SCOPED",
            "TPC359_NORMALIZED_CAP": "NUMERICALLY_CERTIFIED_FINITE_SCOPED",
            "TPC359_SPECTRAL_MONOTONE_DECAY": "REFUTED_SCOPED_ON_DECLARED_LADDER",
            "TPC359_GROWING_OPERATOR_BOUND": "OPEN",
            "TPC359_SOURCE_UNIFORM_L2": "OPEN", "TPC359_ARITHMETIC_ADVANCE": "NO",
            "TPC359_FIXED_POWER_CREDIT": 0, "TPC359_FULL_GATE_B": "OPEN",
            "TPC359_TWIN_PRIME_RESULT": "NONE",
        },
        "round2_clue": ROUND2_CLUE,
    }


def document() -> dict[str, Any]:
    payload = build_payload()
    return {"certificate_version": 1, "claim_status": STATUS,
            "payload": payload,
            "payload_sha256": hashlib.sha256(canonical(payload)).hexdigest()}


def write_certificate() -> None:
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
            print("TPC359_CERTIFICATE=WRITTEN")
        else:
            check_certificate()
            audit = json.loads(RESULT.read_bytes())["payload"]["finite_audit"]
            print("TPC359_CERTIFICATE=PASS rows=288 origins=3 "
                  "normalized_schur_max=" + audit["normalized_schur_max"] +
                  " normalized_spectral_max=" +
                  audit["normalized_all_plus_spectral_max"])
    except (CheckFailure, OSError, json.JSONDecodeError, ValueError,
            TypeError, KeyError, np.linalg.LinAlgError) as error:
        print("TPC359_CERTIFICATE=FAIL " + str(error), file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
