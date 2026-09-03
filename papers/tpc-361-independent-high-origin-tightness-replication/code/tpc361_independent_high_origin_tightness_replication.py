#!/usr/bin/env python3
"""TPC-361: independent high-origin replication of the tightness ledger.

TPC-360 found finite Schur slack and a law-uniform spectral cap on the
TPC-359 origins.  This release freezes a new geometry-only candidate grid,
selects a separated high-origin panel before signed matrices are evaluated,
and repeats the ledger.  It is a finite response-blind replay; it does not
assert an asymptotic operator estimate or an arithmetic advance.
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
RESULT = PROJECT / "results/tpc361_certificate.json"
BASE_CODE = ROOT / (
    "papers/tpc-355-position-aware-mask-energy-normalization/code/"
    "tpc355_position_aware_mask_energy_normalization.py")
PARENT_CODE = ROOT / (
    "papers/tpc-360-schur-tightness-law-uniform-audit/code/"
    "tpc360_schur_tightness_law_uniform_audit.py")
PARENT_CERT = ROOT / (
    "papers/tpc-360-schur-tightness-law-uniform-audit/results/"
    "tpc360_certificate.json")

BASE_CODE_SHA256 = (
    "b54883cbc2e9e19dd8cf6fbece69ff7752ba805678e0b5b2fcf82949dd42fde9")
PARENT_CODE_SHA256 = (
    "0c12d88546fdf11a02e26c588c23c8298cb2a6caa8d841efb2dfd814deb3c10e")
PARENT_CERT_SHA256 = (
    "3d2e07983768d421757ff75c2122366de4e676fbe3f088fc688bff5046ecfadf")

SCHEMA = "TPC361_INDEPENDENT_HIGH_ORIGIN_TIGHTNESS_REPLICATION_V1"
STATUS = "NUMERICALLY_CERTIFIED_FINITE_INDEPENDENT_HIGH_ORIGIN_TIGHTNESS_REPLICATION"
ROUND2_CLUE = "TEST_SCALE_LADDER_AND_SIGN_LAW_INTERACTION_ON_A_NEW_PANEL"

CANDIDATE_START = 310001
CANDIDATE_STEP = 233
CANDIDATE_COUNT = 51
PILOT_COUNT = 256
MIN_SEPARATION = 1536
ORIGINS = (313030, 311166, 321651)
COUNTS = (256, 512, 1024, 2048)
Q_ANCHORS = (24, 54, 80)
EXPONENTS = (1, 2)
LAWS = ("all_plus", "alternating_index", "mod4_character", "half_split")
SPECTRAL_SHORT_COUNTS = (256, 512)
HEIGHT = 66
EXACT_INTERVAL = (313060, 313073)
SPECTRAL_GUARD = 1.0e-6


class CheckFailure(RuntimeError):
    """Raised when a finite certificate does not replay exactly."""


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
    spec = importlib.util.spec_from_file_location("tpc355_base_tpc361", BASE_CODE)
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
    need(payload.get("schema") ==
         "TPC360_SCHUR_TIGHTNESS_LAW_UNIFORM_AUDIT_V1", "parent schema")
    return payload


def primes(q0: int) -> list[int]:
    return list(BASE.shell_for(q0))


def geometry_only(values: np.ndarray, q0: int, exponent: int) -> np.ndarray:
    """Build only the unsigned mask-energy diagonal used by selection."""
    difference = values[:, None] - values[None, :]
    distance = difference.astype(np.float64)
    kernel = (float(HEIGHT) ** (2 * exponent) /
              (HEIGHT * HEIGHT + distance * distance) ** exponent)
    np.fill_diagonal(kernel, 0.0)
    geometry = np.zeros(len(values), dtype=np.float64)
    for prime in primes(q0):
        centered = ((difference % prime == 0).astype(np.float64) -
                    1.0 / (prime - 1))
        np.fill_diagonal(centered, 0.0)
        valid = ((difference != 0) &
                 (values[:, None] % prime != 0) &
                 (values[None, :] % prime != 0))
        block = float(prime) * kernel * centered * valid
        geometry += np.sum(block * block, axis=1)
    need(bool(np.all(np.isfinite(geometry) & (geometry > 0))),
         "pilot geometry")
    return geometry


def candidate_origins() -> list[int]:
    return [CANDIDATE_START + CANDIDATE_STEP * j
            for j in range(CANDIDATE_COUNT)]


def scan_candidates() -> list[dict[str, Any]]:
    scan: list[dict[str, Any]] = []
    for origin in candidate_origins():
        values = np.arange(origin, origin + PILOT_COUNT, dtype=np.int64)
        setting_scores: list[dict[str, Any]] = []
        score = 0.0
        for q0 in Q_ANCHORS:
            for exponent in EXPONENTS:
                g = geometry_only(values, q0, exponent)
                minimum, maximum = float(np.min(g)), float(np.max(g))
                local = maximum / minimum
                score = max(score, local)
                setting_scores.append({
                    "Q": q0, "kernel_exponent": exponent,
                    "geometry_min": show(minimum),
                    "geometry_max": show(maximum),
                    "spread": show(local),
                })
        scan.append({"origin": origin, "score": show(score),
                     "settings": setting_scores})
    need(len(scan) == CANDIDATE_COUNT, "candidate census")
    return scan


def select(scan: list[dict[str, Any]]) -> list[int]:
    ordered = sorted(scan, key=lambda row: (-float(row["score"]),
                                             int(row["origin"])))
    selected: list[int] = []
    for row in ordered:
        origin = int(row["origin"])
        if all(abs(origin - old) >= MIN_SEPARATION for old in selected):
            selected.append(origin)
        if len(selected) == len(ORIGINS):
            break
    need(selected == list(ORIGINS), "frozen selection")
    return selected


def metrics(matrix: np.ndarray, spectrum: bool) -> dict[str, Any]:
    symmetry = float(np.max(np.abs(matrix - matrix.T)))
    schur = float(np.max(np.sum(np.abs(matrix), axis=1)))
    frobenius = float(np.sqrt(np.sum(matrix * matrix)))
    need(math.isfinite(symmetry) and symmetry <= 1.0e-12 and
         schur > 0.0 and math.isfinite(frobenius) and frobenius > 0.0,
         "finite envelopes")
    result: dict[str, Any] = {
        "schur": show(schur), "frobenius": show(frobenius),
        "symmetry_error": show(symmetry), "spectrum_recorded": spectrum,
        "spectral": None, "minimum_eigenvalue": None,
        "maximum_eigenvalue": None, "spectral_over_schur": None,
        "spectral_over_frobenius": None,
    }
    if spectrum:
        eigenvalues = np.linalg.eigvalsh(matrix)
        minimum, maximum = float(eigenvalues[0]), float(eigenvalues[-1])
        spectral = max(abs(minimum), abs(maximum))
        need(math.isfinite(spectral) and spectral > 0.0 and
             spectral <= schur + 2.0e-10 * max(1.0, schur) and
             spectral <= frobenius + 2.0e-10 * max(1.0, frobenius),
             "finite spectral envelopes")
        result.update({
            "spectral": show(spectral),
            "minimum_eigenvalue": show(minimum),
            "maximum_eigenvalue": show(maximum),
            "spectral_over_schur": show(spectral / schur),
            "spectral_over_frobenius": show(spectral / frobenius),
        })
    return result


def build_rows() -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for origin in ORIGINS:
        for count in COUNTS:
            values = np.arange(origin, origin + count, dtype=np.int64)
            for q0 in Q_ANCHORS:
                for exponent in EXPONENTS:
                    shell, matrices, geometry = BASE.component_matrices(
                        values, q0, exponent)
                    scale = np.sqrt(geometry[:, None] * geometry[None, :])
                    spectrum_laws = (LAWS if count in SPECTRAL_SHORT_COUNTS
                                     else ("all_plus",))
                    for law in LAWS:
                        normalized = matrices[law] / scale
                        rows.append({
                            "origin": origin, "count": count,
                            "interval": [origin, origin + count - 1],
                            "Q": q0, "kernel_exponent": exponent,
                            "law": law, "shell": shell,
                            "geometry_min": show(float(np.min(geometry))),
                            "geometry_max": show(float(np.max(geometry))),
                            "normalized": metrics(
                                normalized, law in spectrum_laws),
                        })
    need(len(rows) == 288, "row census")
    need(sum(r["normalized"]["spectrum_recorded"] for r in rows) == 180,
         "spectrum census")
    return rows


def law_summary(rows: list[dict[str, Any]]) -> dict[str, Any]:
    result: dict[str, Any] = {}
    for law in LAWS:
        selected = [r for r in rows if r["law"] == law]
        spectra = [float(r["normalized"]["spectral"]) for r in selected
                   if r["normalized"]["spectrum_recorded"]]
        ratios_s = [float(r["normalized"]["spectral_over_schur"])
                    for r in selected
                    if r["normalized"]["spectrum_recorded"]]
        ratios_f = [float(r["normalized"]["spectral_over_frobenius"])
                    for r in selected
                    if r["normalized"]["spectrum_recorded"]]
        result[law] = {
            "rows": len(selected), "spectral_rows": len(spectra),
            "spectral_min": show(min(spectra)),
            "spectral_max": show(max(spectra)),
            "spectral_mean": show(sum(spectra) / len(spectra)),
            "spectral_over_schur_max": show(max(ratios_s)),
            "spectral_over_frobenius_max": show(max(ratios_f)),
        }
    return result


def winner_audit(rows: list[dict[str, Any]]) -> dict[str, Any]:
    winners: list[dict[str, Any]] = []
    for origin in ORIGINS:
        for count in SPECTRAL_SHORT_COUNTS:
            for q0 in Q_ANCHORS:
                for exponent in EXPONENTS:
                    setting = [r for r in rows if r["origin"] == origin and
                               r["count"] == count and r["Q"] == q0 and
                               r["kernel_exponent"] == exponent]
                    best = max(setting, key=lambda row:
                               (float(row["normalized"]["spectral"]),
                                row["law"]))
                    winners.append({"origin": origin, "count": count,
                                    "Q": q0, "kernel_exponent": exponent,
                                    "winner": best["law"],
                                    "spectral": best["normalized"]["spectral"]})
    counts = {law: sum(row["winner"] == law for row in winners)
              for law in LAWS}
    need(len(winners) == 36 and sum(counts.values()) == 36,
         "winner census")
    return {"settings": winners, "winner_counts": counts}


def transition_audit(rows: list[dict[str, Any]]) -> dict[str, Any]:
    transitions: list[dict[str, Any]] = []
    for origin in ORIGINS:
        for q0 in Q_ANCHORS:
            for exponent in EXPONENTS:
                ladder = []
                for count in COUNTS:
                    row = next(r for r in rows if r["origin"] == origin and
                               r["count"] == count and r["Q"] == q0 and
                               r["kernel_exponent"] == exponent and
                               r["law"] == "all_plus")
                    ladder.append(float(row["normalized"]["spectral"]))
                for left, right, a, b in zip(COUNTS, COUNTS[1:], ladder,
                                             ladder[1:]):
                    delta = b - a
                    kind = ("increase" if delta > SPECTRAL_GUARD else
                            "decrease" if delta < -SPECTRAL_GUARD else "flat")
                    transitions.append({"origin": origin, "Q": q0,
                                        "kernel_exponent": exponent,
                                        "from_count": left, "to_count": right,
                                        "from_spectral": show(a),
                                        "to_spectral": show(b),
                                        "delta": show(delta), "kind": kind})
    counts = {kind: sum(row["kind"] == kind for row in transitions)
              for kind in ("increase", "decrease", "flat")}
    need(len(transitions) == 54 and sum(counts.values()) == 54,
         "transition census")
    return {"guard": show(SPECTRAL_GUARD), "transitions": transitions,
            "counts": counts,
            "monotone_decay_claim": ("REFUTED_SCOPED_ON_DECLARED_LADDER"
                                      if counts["increase"] else
                                      "NOT_TESTED")}


def exact_anchor() -> dict[str, Any]:
    values = list(range(EXACT_INTERVAL[0], EXACT_INTERVAL[1] + 1))
    shell = BASE.shell_for(4)

    def entry(prime: int, u: int, t: int) -> Fraction:
        if u == t or u % prime == 0 or t % prime == 0:
            return Fraction(0)
        centered = Fraction(int((u - t) % prime == 0), 1) - Fraction(1, prime - 1)
        return prime * Fraction(HEIGHT * HEIGHT,
                                HEIGHT * HEIGHT + (u - t) ** 2) * centered

    matrix = [[sum((entry(p, u, t) for p in shell), Fraction(0))
               for t in values] for u in values]
    geometry = [sum((entry(p, u, t) ** 2 for p in shell for t in values),
                    Fraction(0)) for u in values]
    need(all(matrix[i][j] == matrix[j][i]
             for i in range(len(values)) for j in range(len(values))),
         "anchor symmetry")
    need(all(value > 0 for value in geometry), "anchor positivity")
    text = lambda value: f"{value.numerator}/{value.denominator}"
    return {
        "interval": list(EXACT_INTERVAL), "Q": 4, "shell": shell,
        "kernel_exponent": 1, "matrix_symmetric": True,
        "geometry_positive": True,
        "matrix_digest": hashlib.sha256(canonical([
            [text(value) for value in row] for row in matrix])).hexdigest(),
        "geometry_digest": hashlib.sha256(canonical(
            [text(value) for value in geometry])).hexdigest(),
    }


def build_payload() -> dict[str, Any]:
    for path, expected, label in ((BASE_CODE, BASE_CODE_SHA256, "base"),
                                  (PARENT_CODE, PARENT_CODE_SHA256, "parent code"),
                                  (PARENT_CERT, PARENT_CERT_SHA256, "parent cert")):
        need(path.is_file() and digest(path.read_bytes()) == expected,
             label + " provenance")
    parent = load_parent()
    scan = scan_candidates()
    selected = select(scan)
    rows = build_rows()
    spectra = [r for r in rows if r["normalized"]["spectrum_recorded"]]
    max_schur = max(float(r["normalized"]["schur"]) for r in rows)
    max_frobenius = max(float(r["normalized"]["frobenius"]) for r in rows)
    max_spectral = max(float(r["normalized"]["spectral"]) for r in spectra)
    max_ratio_s = max(float(r["normalized"]["spectral_over_schur"])
                      for r in spectra)
    max_ratio_f = max(float(r["normalized"]["spectral_over_frobenius"])
                      for r in spectra)
    need(max_schur < 0.83 and max_spectral < 0.64 and
         max_ratio_s < 0.78 and max_ratio_f < 0.63,
         "finite cap thresholds")
    winners = winner_audit(rows)
    transitions = transition_audit(rows)
    audit = {
        "rows": len(rows), "origins": len(ORIGINS), "settings": 72,
        "laws": len(LAWS), "spectral_rows": len(spectra),
        "all_law_short_spectral_rows": 144,
        "all_plus_long_spectral_rows": 36,
        "normalized_schur_max": show(max_schur),
        "normalized_frobenius_max": show(max_frobenius),
        "normalized_spectral_max": show(max_spectral),
        "max_spectral_over_schur": show(max_ratio_s),
        "max_spectral_over_frobenius": show(max_ratio_f),
        "relative_schur_slack_at_least": show(1.0 - max_ratio_s),
        "relative_frobenius_slack_at_least": show(1.0 - max_ratio_f),
        "finite_schur_violations": 0, "finite_frobenius_violations": 0,
        "fixed_power_credit": 0, "arithmetic_advance": "NO",
    }
    return {
        "schema": SCHEMA, "status": STATUS,
        "parent_lock": {"base_code_sha256": BASE_CODE_SHA256,
                         "parent_code_sha256": PARENT_CODE_SHA256,
                         "parent_certificate_sha256": PARENT_CERT_SHA256,
                         "parent_schema": parent["schema"]},
        "protocol": {
            "candidate_origins": candidate_origins(),
            "pilot_count": PILOT_COUNT, "minimum_separation": MIN_SEPARATION,
            "origins": list(ORIGINS), "counts": list(COUNTS),
            "q_anchors": list(Q_ANCHORS), "kernel_exponents": list(EXPONENTS),
            "height": HEIGHT, "laws": list(LAWS),
            "spectral_short_counts": list(SPECTRAL_SHORT_COUNTS),
            "source_response_used": False, "sign_response_used": False,
            "selection_rule": "max over six unsigned geometry spreads, descending score then origin, greedy separation",
            "operator": "literal deleted-diagonal two-endpoint divisibility-masked prime-shell operator",
            "normalization": "TPC-355 unsigned mask-energy symmetric congruence",
        },
        "selection": {"selected_origins": selected, "scan": scan},
        "exact_theorem": {
            "schur": "For finite real symmetric T, ||T||_2 <= max_u sum_t |T(u,t)|.",
            "frobenius": "For finite real T, ||T||_2 <= ||T||_F.",
            "scope": "finite declared matrices only; observed caps and slack are not asymptotic theorems",
        },
        "finite_audit": audit,
        "law_summaries": law_summary(rows),
        "law_winner_audit": winners,
        "transition_audit": transitions,
        "rows": rows,
        "row_digest": hashlib.sha256(canonical(rows)).hexdigest(),
        "exact_anchor": exact_anchor(),
        "claim_firewall": {
            "TPC361_GEOMETRY_SELECTION": "PROVED_EXACT_FINITE_RESPONSE_BLIND",
            "TPC361_HIGH_ORIGIN_REPLAY": "NUMERICALLY_CERTIFIED_FINITE_288_ROWS",
            "TPC361_FINITE_SCHUR_ENVELOPE": "PROVED_EXACT_FINITE",
            "TPC361_FINITE_FROBENIUS_ENVELOPE": "PROVED_EXACT_FINITE",
            "TPC361_TIGHTNESS_REPLICATION": "NUMERICALLY_CERTIFIED_FINITE_SCOPED",
            "TPC361_LAW_UNIFORM_SHORT_CAP": "NUMERICALLY_CERTIFIED_FINITE_SCOPED",
            "TPC361_SCALE_MONOTONE_DECAY": transitions["monotone_decay_claim"],
            "TPC361_GROWING_OPERATOR_BOUND": "OPEN",
            "TPC361_SOURCE_UNIFORM_L2": "OPEN",
            "TPC361_ARITHMETIC_ADVANCE": "NO",
            "TPC361_FIXED_POWER_CREDIT": 0,
            "TPC361_FULL_GATE_B": "OPEN", "TPC361_TWIN_PRIME_RESULT": "NONE",
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
            print("TPC361_CERTIFICATE=WRITTEN")
        else:
            raw = RESULT.read_bytes()
            stored = json.loads(raw)
            need(raw == canonical(stored), "certificate canonicality")
            need(stored.get("certificate_version") == 1 and
                 stored.get("claim_status") == STATUS, "certificate header")
            payload = stored["payload"]
            need(stored.get("payload_sha256") == hashlib.sha256(
                canonical(payload)).hexdigest() and payload == build_payload(),
                 "certificate replay")
            print("TPC361_CERTIFICATE=PASS rows=288 spectral_rows=180 "
                  "normalized_spectral_max=" +
                  payload["finite_audit"]["normalized_spectral_max"])
    except (CheckFailure, OSError, json.JSONDecodeError, ValueError,
            TypeError, KeyError, np.linalg.LinAlgError) as error:
        print("TPC361_CERTIFICATE=FAIL " + str(error), file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
