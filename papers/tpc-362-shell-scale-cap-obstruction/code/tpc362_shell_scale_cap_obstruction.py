#!/usr/bin/env python3
"""TPC-362: shell-scale stress of the finite normalized cap.

TPC-361 replicated the cap on a fresh high-origin panel.  This release keeps
that panel fixed and widens the shell ladder, testing whether the cap is
stable in Q.  The result is deliberately allowed to be negative: a scoped
high-Q failure is an obstruction, not an arithmetic theorem.
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
RESULT = PROJECT / "results/tpc362_certificate.json"
BASE_CODE = ROOT / (
    "papers/tpc-355-position-aware-mask-energy-normalization/code/"
    "tpc355_position_aware_mask_energy_normalization.py")
PARENT_CODE = ROOT / (
    "papers/tpc-361-independent-high-origin-tightness-replication/code/"
    "tpc361_independent_high_origin_tightness_replication.py")
PARENT_CERT = ROOT / (
    "papers/tpc-361-independent-high-origin-tightness-replication/results/"
    "tpc361_certificate.json")
BASE_CODE_SHA256 = (
    "b54883cbc2e9e19dd8cf6fbece69ff7752ba805678e0b5b2fcf82949dd42fde9")
PARENT_CODE_SHA256 = (
    "5e48902f49f999cf314ea924796369310b48046a906189388fb9cfc43bcd418e")
PARENT_CERT_SHA256 = (
    "0b42332a836e8b0392ce8cd02ffc4840770952c15e0c0c9302b1adc34ea62d41")
SCHEMA = "TPC362_SHELL_SCALE_CAP_OBSTRUCTION_V1"
STATUS = "NUMERICALLY_CERTIFIED_FINITE_SHELL_SCALE_CAP_OBSTRUCTION"
ROUND2_CLUE = "LOCALIZE_HIGH_Q_OBSTRUCTION_BY_LAW_AND_ROW_GEOMETRY"
ORIGINS = (313030, 311166, 321651)
COUNTS = (256, 512)
Q_ANCHORS = (12, 24, 36, 54, 80, 128, 256, 512)
LOW_Q = (12, 24, 36, 54, 80)
HIGH_Q = (128, 256, 512)
EXPONENTS = (1, 2)
LAWS = ("all_plus", "alternating_index", "mod4_character", "half_split")
HEIGHT = 66
CAP_SCHUR = 0.83
CAP_SPECTRAL = 0.64
Q_GUARD = 1.0e-8
EXACT_INTERVAL = (313060, 313073)


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
    spec = importlib.util.spec_from_file_location("tpc355_base_tpc362", BASE_CODE)
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
    need(isinstance(payload, dict) and payload.get("schema") ==
         "TPC361_INDEPENDENT_HIGH_ORIGIN_TIGHTNESS_REPLICATION_V1",
         "parent payload")
    need(payload.get("protocol", {}).get("origins") == list(ORIGINS),
         "parent origins")
    return payload


def metrics(matrix: np.ndarray) -> dict[str, Any]:
    symmetry = float(np.max(np.abs(matrix - matrix.T)))
    schur = float(np.max(np.sum(np.abs(matrix), axis=1)))
    frobenius = float(np.sqrt(np.sum(matrix * matrix)))
    need(math.isfinite(symmetry) and symmetry <= 1.0e-12 and
         schur > 0.0 and math.isfinite(frobenius) and frobenius > 0.0,
         "finite matrix envelopes")
    eigenvalues = np.linalg.eigvalsh(matrix)
    lo, hi = float(eigenvalues[0]), float(eigenvalues[-1])
    spectral = max(abs(lo), abs(hi))
    need(math.isfinite(spectral) and spectral > 0.0 and
         spectral <= schur + 2.0e-10 * max(1.0, schur) and
         spectral <= frobenius + 2.0e-10 * max(1.0, frobenius),
         "finite spectral envelopes")
    return {
        "schur": show(schur), "frobenius": show(frobenius),
        "spectral": show(spectral), "minimum_eigenvalue": show(lo),
        "maximum_eigenvalue": show(hi), "symmetry_error": show(symmetry),
        "spectral_over_schur": show(spectral / schur),
        "spectral_over_frobenius": show(spectral / frobenius),
    }


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
                    for law in LAWS:
                        rows.append({
                            "origin": origin, "count": count,
                            "interval": [origin, origin + count - 1],
                            "Q": q0, "kernel_exponent": exponent,
                            "law": law, "shell": shell,
                            "geometry_min": show(float(np.min(geometry))),
                            "geometry_max": show(float(np.max(geometry))),
                            "normalized": metrics(matrices[law] / scale),
                        })
    need(len(rows) == 384, "row census")
    return rows


def q_summary(rows: list[dict[str, Any]]) -> dict[str, Any]:
    result: dict[str, Any] = {}
    for q0 in Q_ANCHORS:
        selected = [r for r in rows if r["Q"] == q0]
        spectra = [float(r["normalized"]["spectral"]) for r in selected]
        schur = [float(r["normalized"]["schur"]) for r in selected]
        frobenius = [float(r["normalized"]["frobenius"]) for r in selected]
        result[str(q0)] = {
            "rows": len(selected), "spectral_min": show(min(spectra)),
            "spectral_max": show(max(spectra)),
            "schur_min": show(min(schur)), "schur_max": show(max(schur)),
            "frobenius_max": show(max(frobenius)),
            "spectral_cap_violations": sum(v > CAP_SPECTRAL for v in spectra),
            "schur_cap_violations": sum(v > CAP_SCHUR for v in schur),
        }
    return result


def winner_audit(rows: list[dict[str, Any]]) -> dict[str, Any]:
    winners: list[dict[str, Any]] = []
    for origin in ORIGINS:
        for count in COUNTS:
            for q0 in Q_ANCHORS:
                for exponent in EXPONENTS:
                    setting = [r for r in rows if r["origin"] == origin and
                               r["count"] == count and r["Q"] == q0 and
                               r["kernel_exponent"] == exponent]
                    best = max(setting, key=lambda row:
                               (float(row["normalized"]["spectral"]), row["law"]))
                    winners.append({"origin": origin, "count": count,
                                    "Q": q0, "kernel_exponent": exponent,
                                    "winner": best["law"],
                                    "spectral": best["normalized"]["spectral"]})
    counts = {law: sum(row["winner"] == law for row in winners) for law in LAWS}
    need(len(winners) == 96 and sum(counts.values()) == 96, "winner census")
    return {"settings": winners, "winner_counts": counts}


def q_transition_audit(rows: list[dict[str, Any]]) -> dict[str, Any]:
    transitions: list[dict[str, Any]] = []
    for origin in ORIGINS:
        for count in COUNTS:
            for exponent in EXPONENTS:
                for law in LAWS:
                    values = [float(next(r for r in rows
                                        if r["origin"] == origin and
                                        r["count"] == count and r["Q"] == q0 and
                                        r["kernel_exponent"] == exponent and
                                        r["law"] == law)["normalized"]["spectral"])
                              for q0 in Q_ANCHORS]
                    for left, right, a, b in zip(Q_ANCHORS, Q_ANCHORS[1:],
                                                 values, values[1:]):
                        delta = b - a
                        kind = ("increase" if delta > Q_GUARD else
                                "decrease" if delta < -Q_GUARD else "flat")
                        transitions.append({"origin": origin, "count": count,
                                            "kernel_exponent": exponent,
                                            "law": law, "from_Q": left,
                                            "to_Q": right,
                                            "from_spectral": show(a),
                                            "to_spectral": show(b),
                                            "delta": show(delta), "kind": kind})
    counts = {kind: sum(row["kind"] == kind for row in transitions)
              for kind in ("increase", "decrease", "flat")}
    need(len(transitions) == 336 and sum(counts.values()) == 336,
         "Q transition census")
    return {"guard": show(Q_GUARD), "transitions": transitions,
            "counts": counts}


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
    need(all(g > 0 for g in geometry), "anchor positivity")
    text = lambda x: f"{x.numerator}/{x.denominator}"
    return {"interval": list(EXACT_INTERVAL), "Q": 4,
            "kernel_exponent": 1, "shell": shell,
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
    qstats = q_summary(rows)
    spectra = [float(r["normalized"]["spectral"]) for r in rows]
    schur = [float(r["normalized"]["schur"]) for r in rows]
    frobenius = [float(r["normalized"]["frobenius"]) for r in rows]
    max_spectral, max_schur = max(spectra), max(schur)
    max_frobenius = max(frobenius)
    low_rows = [r for r in rows if r["Q"] in LOW_Q]
    high_rows = [r for r in rows if r["Q"] in HIGH_Q]
    low_spectral = [float(r["normalized"]["spectral"]) for r in low_rows]
    low_schur = [float(r["normalized"]["schur"]) for r in low_rows]
    high_spectral = [float(r["normalized"]["spectral"]) for r in high_rows]
    high_schur = [float(r["normalized"]["schur"]) for r in high_rows]
    need(max(spectra) > CAP_SPECTRAL and max(schur) > CAP_SCHUR,
         "expected high-Q obstruction")
    need(max(low_spectral) < CAP_SPECTRAL and max(low_schur) < CAP_SCHUR,
         "low-Q cap transfer")
    audit = {
        "rows": len(rows), "settings": 96, "laws": len(LAWS),
        "spectral_rows": len(rows), "normalized_schur_max": show(max_schur),
        "normalized_frobenius_max": show(max_frobenius),
        "normalized_spectral_max": show(max_spectral),
        "low_q": list(LOW_Q), "high_q": list(HIGH_Q),
        "low_q_normalized_schur_max": show(max(low_schur)),
        "low_q_normalized_spectral_max": show(max(low_spectral)),
        "high_q_normalized_schur_min": show(min(high_schur)),
        "high_q_normalized_spectral_min": show(min(high_spectral)),
        "schur_cap": show(CAP_SCHUR), "spectral_cap": show(CAP_SPECTRAL),
        "schur_cap_violations": sum(v >= CAP_SCHUR for v in schur),
        "spectral_cap_violations": sum(v >= CAP_SPECTRAL for v in spectra),
        "finite_schur_violations": 0, "finite_frobenius_violations": 0,
        "fixed_power_credit": 0, "arithmetic_advance": "NO",
    }
    first_schur_failure = next(q for q in Q_ANCHORS
                               if qstats[str(q)]["schur_cap_violations"])
    first_spectral_failure = next(q for q in Q_ANCHORS
                                  if qstats[str(q)]["spectral_cap_violations"])
    audit["first_schur_cap_failure_Q"] = first_schur_failure
    audit["first_spectral_cap_failure_Q"] = first_spectral_failure
    winners = winner_audit(rows)
    qtrans = q_transition_audit(rows)
    return {
        "schema": SCHEMA, "status": STATUS,
        "parent_lock": {"base_code_sha256": BASE_CODE_SHA256,
                         "parent_code_sha256": PARENT_CODE_SHA256,
                         "parent_certificate_sha256": PARENT_CERT_SHA256,
                         "parent_schema": parent["schema"]},
        "protocol": {
            "origins": list(ORIGINS), "counts": list(COUNTS),
            "q_anchors": list(Q_ANCHORS), "low_q": list(LOW_Q),
            "high_q": list(HIGH_Q), "kernel_exponents": list(EXPONENTS),
            "height": HEIGHT, "laws": list(LAWS),
            "spectra_for_all_laws": True, "source_response_used": False,
            "selection_inherited_from": "TPC-361 frozen panel",
            "operator": "literal deleted-diagonal two-endpoint divisibility-masked prime-shell operator",
            "normalization": "TPC-355 unsigned mask-energy symmetric congruence",
        },
        "exact_theorem": {
            "schur": "For finite real symmetric T, ||T||_2 <= max_u sum_t |T(u,t)|.",
            "frobenius": "For finite real T, ||T||_2 <= ||T||_F.",
            "scope": "finite declared matrices only; high-Q failure is scoped and not asymptotic",
        },
        "finite_audit": audit, "q_summaries": qstats,
        "law_winner_audit": winners, "q_transition_audit": qtrans,
        "rows": rows,
        "row_digest": hashlib.sha256(canonical(rows)).hexdigest(),
        "exact_anchor": exact_anchor(),
        "claim_firewall": {
            "TPC362_SHELL_SCALE_REPLAY": "NUMERICALLY_CERTIFIED_FINITE_384_ROWS",
            "TPC362_FINITE_SCHUR_ENVELOPE": "PROVED_EXACT_FINITE",
            "TPC362_FINITE_FROBENIUS_ENVELOPE": "PROVED_EXACT_FINITE",
            "TPC362_LOW_Q_CAP": "NUMERICALLY_CERTIFIED_FINITE_SCOPED",
            "TPC362_HIGH_Q_CAP_EXTENSION": "REFUTED_SCOPED_ON_DECLARED_Q_LADDER",
            "TPC362_LAW_WINNER_CENSUS": "NUMERICALLY_CERTIFIED_FINITE_SCOPED",
            "TPC362_GROWING_OPERATOR_BOUND": "OPEN",
            "TPC362_SOURCE_UNIFORM_L2": "OPEN",
            "TPC362_ARITHMETIC_ADVANCE": "NO",
            "TPC362_FIXED_POWER_CREDIT": 0,
            "TPC362_FULL_GATE_B": "OPEN", "TPC362_TWIN_PRIME_RESULT": "NONE",
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
            print("TPC362_CERTIFICATE=WRITTEN")
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
            print("TPC362_CERTIFICATE=PASS rows=384 all_law_spectral=384 "
                  "first_spectral_failure_Q=" +
                  str(payload["finite_audit"]["first_spectral_cap_failure_Q"]))
    except (CheckFailure, OSError, json.JSONDecodeError, ValueError,
            TypeError, KeyError, np.linalg.LinAlgError) as error:
        print("TPC362_CERTIFICATE=FAIL " + str(error), file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
