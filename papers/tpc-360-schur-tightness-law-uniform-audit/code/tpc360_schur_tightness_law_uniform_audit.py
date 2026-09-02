#!/usr/bin/env python3
"""TPC-360: Schur-tightness and law-uniformity audit.

TPC-359 transferred a finite cap under hostile geometry selection.  This
project asks whether the Schur/Frobenius envelopes are close to the measured
operator norm and whether all-plus is representative of the four fixed sign
laws.  It is a new finite replay on the already locked TPC-359 origins; no
source response or arithmetic reassembly is introduced.
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
RESULT = PROJECT / "results/tpc360_certificate.json"
BASE_CODE = ROOT / ("papers/tpc-355-position-aware-mask-energy-normalization/"
                    "code/tpc355_position_aware_mask_energy_normalization.py")
PARENT_CODE = ROOT / ("papers/tpc-359-geometry-adversarial-high-origin-holdout/code/"
                      "tpc359_geometry_adversarial_high_origin_holdout.py")
PARENT_CERT = ROOT / ("papers/tpc-359-geometry-adversarial-high-origin-holdout/results/"
                      "tpc359_certificate.json")
BASE_CODE_SHA256 = "b54883cbc2e9e19dd8cf6fbece69ff7752ba805678e0b5b2fcf82949dd42fde9"
PARENT_CODE_SHA256 = "ff5088daefb615fb02077662cded3d3c8493789ffa1064609072efe6c0216bb5"
PARENT_CERT_SHA256 = "b4edaf61b951acb79222e7d8f7b0cbc7a9278b3de802b11bea5908da89b7bced"

SCHEMA = "TPC360_SCHUR_TIGHTNESS_LAW_UNIFORM_AUDIT_V1"
STATUS = "NUMERICALLY_CERTIFIED_FINITE_SCHUR_TIGHTNESS_LAW_UNIFORM_AUDIT"
ROUND2_CLUE = "TEST_INDEPENDENT_HIGH_ORIGIN_REPLICATION_WITH_TIGHTNESS_LEDGER"
ORIGINS = (267175, 261267, 269074)
COUNTS = (256, 512)
Q_ANCHORS = (24, 54, 80)
EXPONENTS = (1, 2)
LAWS = ("all_plus", "alternating_index", "mod4_character", "half_split")
HEIGHT = 66
BOUND_TOL = 2.0e-10
EXACT_INTERVAL = (267205, 267218)


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
    spec = importlib.util.spec_from_file_location("tpc355_base_tpc360", BASE_CODE)
    need(spec is not None and spec.loader is not None, "base module")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


BASE = load_base()


def load_parent() -> dict[str, Any]:
    raw = PARENT_CERT.read_bytes()
    need(digest(raw) == PARENT_CERT_SHA256, "parent certificate lock")
    document = json.loads(raw)
    need(raw == canonical(document), "parent canonicality")
    payload = document.get("payload")
    need(isinstance(payload, dict), "parent payload")
    need(payload.get("protocol", {}).get("origins") == list(ORIGINS),
         "parent origin protocol")
    return payload


def metrics(matrix: np.ndarray) -> dict[str, Any]:
    symmetry = float(np.max(np.abs(matrix - matrix.T)))
    schur = float(np.max(np.sum(np.abs(matrix), axis=1)))
    frob = float(np.sqrt(np.sum(matrix * matrix)))
    need(math.isfinite(symmetry) and symmetry <= 1.0e-12 and schur > 0 and
         frob > 0, "finite matrix metrics")
    ev = np.linalg.eigvalsh(matrix)
    lo, hi = float(ev[0]), float(ev[-1])
    spectral = max(abs(lo), abs(hi))
    need(math.isfinite(spectral) and spectral > 0 and
         spectral <= schur + BOUND_TOL * max(1.0, schur) and
         spectral <= frob + BOUND_TOL * max(1.0, frob), "finite envelopes")
    return {
        "schur": show(schur), "frobenius": show(frob),
        "spectral": show(spectral), "minimum_eigenvalue": show(lo),
        "maximum_eigenvalue": show(hi), "symmetry_error": show(symmetry),
        "spectral_over_schur": show(spectral / schur),
        "spectral_over_frobenius": show(spectral / frob),
    }


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
                    for law in LAWS:
                        normalized = matrices[law] / scale
                        rows.append({
                            "origin": origin, "count": count,
                            "interval": [origin, origin + count - 1],
                            "Q": q0, "kernel_exponent": exponent,
                            "law": law, "shell": primes,
                            "geometry_min": show(np.min(geometry)),
                            "geometry_max": show(np.max(geometry)),
                            "normalized": metrics(normalized),
                        })
    need(len(rows) == 144, "row census")
    return rows


def summary(rows: list[dict[str, Any]]) -> dict[str, Any]:
    result: dict[str, Any] = {}
    for law in LAWS:
        selected = [r for r in rows if r["law"] == law]
        values = [float(r["normalized"]["spectral"]) for r in selected]
        ratio_s = [float(r["normalized"]["spectral_over_schur"])
                   for r in selected]
        ratio_f = [float(r["normalized"]["spectral_over_frobenius"])
                   for r in selected]
        result[law] = {
            "rows": len(selected), "spectral_min": show(min(values)),
            "spectral_max": show(max(values)),
            "spectral_mean": show(sum(values) / len(values)),
            "spectral_over_schur_max": show(max(ratio_s)),
            "spectral_over_schur_mean": show(sum(ratio_s) / len(ratio_s)),
            "spectral_over_frobenius_max": show(max(ratio_f)),
        }
    return result


def winner_audit(rows: list[dict[str, Any]]) -> dict[str, Any]:
    winners: list[dict[str, Any]] = []
    for origin in ORIGINS:
        for count in COUNTS:
            for q0 in Q_ANCHORS:
                for exponent in EXPONENTS:
                    selected = [r for r in rows if r["origin"] == origin and
                                r["count"] == count and r["Q"] == q0 and
                                r["kernel_exponent"] == exponent]
                    best = max(selected, key=lambda r:
                               (float(r["normalized"]["spectral"]), r["law"]))
                    winners.append({"origin": origin, "count": count,
                                    "Q": q0, "kernel_exponent": exponent,
                                    "winner": best["law"],
                                    "spectral": best["normalized"]["spectral"]})
    counts = {law: sum(w["winner"] == law for w in winners) for law in LAWS}
    need(len(winners) == 36 and counts == {
        "all_plus": 30, "alternating_index": 0,
        "mod4_character": 6, "half_split": 0}, "law winner census")
    return {"settings": winners, "winner_counts": counts}


def exact_anchor() -> dict[str, Any]:
    values = list(range(EXACT_INTERVAL[0], EXACT_INTERVAL[1] + 1))
    primes = BASE.shell_for(4)
    matrix = [[sum((BASE.exact_entry(p, u, t, 1) for p in primes), Fraction(0))
               for t in values] for u in values]
    geometry = [sum((BASE.exact_entry(p, u, t, 1) ** 2
                     for p in primes for t in values), Fraction(0))
                for u in values]
    need(all(matrix[i][j] == matrix[j][i]
             for i in range(14) for j in range(14)), "exact symmetry")
    need(all(g > 0 for g in geometry), "exact geometry")
    text = lambda x: f"{x.numerator}/{x.denominator}"
    return {"interval": list(EXACT_INTERVAL), "Q": 4, "shell": primes,
            "matrix_symmetric": True, "geometry_positive": True,
            "matrix_digest": hashlib.sha256(canonical([
                [text(x) for x in row] for row in matrix])).hexdigest(),
            "geometry_digest": hashlib.sha256(canonical(
                [text(x) for x in geometry])).hexdigest()}


def build_payload() -> dict[str, Any]:
    for path, expected, label in ((BASE_CODE, BASE_CODE_SHA256, "base"),
                                  (PARENT_CODE, PARENT_CODE_SHA256, "parent code"),
                                  (PARENT_CERT, PARENT_CERT_SHA256, "parent cert")):
        need(path.is_file() and digest(path.read_bytes()) == expected,
             label + " provenance")
    parent = load_parent()
    rows = build_rows()
    summaries = summary(rows)
    winners = winner_audit(rows)
    all_rows = [r for r in rows]
    max_schur_ratio = max(float(r["normalized"]["spectral_over_schur"])
                          for r in all_rows)
    max_frob_ratio = max(float(r["normalized"]["spectral_over_frobenius"])
                         for r in all_rows)
    max_spectral = max(float(r["normalized"]["spectral"]) for r in all_rows)
    need(max_schur_ratio < 0.78 and max_frob_ratio < 0.63,
         "finite slack thresholds")
    need(max_spectral < 0.64, "law-uniform finite cap")
    audit = {
        "rows": len(rows), "origins": len(ORIGINS), "settings": 36,
        "laws": len(LAWS), "max_spectral": show(max_spectral),
        "max_spectral_over_schur": show(max_schur_ratio),
        "max_spectral_over_frobenius": show(max_frob_ratio),
        "relative_schur_slack_at_least": show(1.0 - max_schur_ratio),
        "relative_frobenius_slack_at_least": show(1.0 - max_frob_ratio),
        "finite_schur_violations": 0, "finite_frobenius_violations": 0,
        "fixed_power_credit": 0, "arithmetic_advance": "NO",
    }
    return {
        "schema": SCHEMA, "status": STATUS,
        "parent_lock": {"base_code_sha256": BASE_CODE_SHA256,
                         "parent_code_sha256": PARENT_CODE_SHA256,
                         "parent_certificate_sha256": PARENT_CERT_SHA256},
        "protocol": {"origins": list(ORIGINS), "counts": list(COUNTS),
                     "q_anchors": list(Q_ANCHORS),
                     "kernel_exponents": list(EXPONENTS), "height": HEIGHT,
                     "laws": list(LAWS), "spectra_for_all_laws": True,
                     "source_response_used": False,
                     "selection_inherited_from": "TPC-359 fixed panel",
                     "operator": "literal deleted-diagonal two-endpoint divisibility-masked prime-shell operator",
                     "normalization": "TPC-355 unsigned mask-energy symmetric congruence"},
        "exact_theorem": {
            "schur": "For finite real symmetric T, ||T||_2 <= max_u sum_t |T(u,t)|.",
            "frobenius": "For finite real T, ||T||_2 <= ||T||_F.",
            "scope": "finite declared matrices only; observed slack is not an asymptotic theorem",
        },
        "finite_audit": audit, "law_summaries": summaries,
        "law_winner_audit": winners, "rows": rows,
        "row_digest": hashlib.sha256(canonical(rows)).hexdigest(),
        "exact_anchor": exact_anchor(),
        "claim_firewall": {
            "TPC360_SCHUR_ENVELOPE": "PROVED_EXACT_FINITE",
            "TPC360_FROBENIUS_ENVELOPE": "PROVED_EXACT_FINITE",
            "TPC360_ALL_LAW_SPECTRAL_REPLAY": "NUMERICALLY_CERTIFIED_FINITE_144_ROWS",
            "TPC360_SCHUR_SLACK": "NUMERICALLY_CERTIFIED_FINITE_SCOPED",
            "TPC360_LAW_UNIFORM_CAP": "NUMERICALLY_CERTIFIED_FINITE_SCOPED",
            "TPC360_GROWING_OPERATOR_BOUND": "OPEN",
            "TPC360_SOURCE_UNIFORM_L2": "OPEN", "TPC360_ARITHMETIC_ADVANCE": "NO",
            "TPC360_FIXED_POWER_CREDIT": 0, "TPC360_FULL_GATE_B": "OPEN",
            "TPC360_TWIN_PRIME_RESULT": "NONE",
        },
        "round2_clue": ROUND2_CLUE,
    }


def document() -> dict[str, Any]:
    payload = build_payload()
    return {"certificate_version": 1, "claim_status": STATUS,
            "payload": payload,
            "payload_sha256": hashlib.sha256(canonical(payload)).hexdigest()}


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--write", action="store_true")
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()
    if args.write == args.check:
        raise SystemExit("exactly one of --write or --check is required")
    try:
        if args.write:
            RESULT.write_bytes(canonical(document()))
            print("TPC360_CERTIFICATE=WRITTEN")
        else:
            raw = RESULT.read_bytes()
            stored = json.loads(raw)
            need(raw == canonical(stored), "certificate canonicality")
            need(stored.get("certificate_version") == 1 and
                 stored.get("claim_status") == STATUS, "header")
            payload = stored["payload"]
            need(stored.get("payload_sha256") == hashlib.sha256(
                canonical(payload)).hexdigest() and payload == build_payload(),
                 "certificate replay")
            print("TPC360_CERTIFICATE=PASS rows=144 all_law_spectral=144 "
                  "max_schur_ratio=" +
                  payload["finite_audit"]["max_spectral_over_schur"])
    except (CheckFailure, OSError, json.JSONDecodeError, ValueError,
            TypeError, KeyError, np.linalg.LinAlgError) as error:
        print("TPC360_CERTIFICATE=FAIL " + str(error), file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
