#!/usr/bin/env python3
"""TPC-363: bulk persistence at the first shell-scale cap failure.

TPC-362 located the first failure of the inherited normalized spectral cap at
Q=128.  This release freezes that panel and asks a narrower question: does
the failure disappear after removing the five percent of rows selected by
either Schur row mass or principal-eigenvector mass?  The computation is a
finite diagnostic.  It is deliberately not an asymptotic operator theorem,
an arithmetic estimate, or a twin-prime result.
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
RESULT = PROJECT / "results/tpc363_certificate.json"
BASE_CODE = ROOT / (
    "papers/tpc-355-position-aware-mask-energy-normalization/code/"
    "tpc355_position_aware_mask_energy_normalization.py")
PARENT_CODE = ROOT / (
    "papers/tpc-362-shell-scale-cap-obstruction/code/"
    "tpc362_shell_scale_cap_obstruction.py")
PARENT_CERT = ROOT / (
    "papers/tpc-362-shell-scale-cap-obstruction/results/"
    "tpc362_certificate.json")

BASE_CODE_SHA256 = (
    "b54883cbc2e9e19dd8cf6fbece69ff7752ba805678e0b5b2fcf82949dd42fde9")
PARENT_CODE_SHA256 = (
    "47d0dc48e64869a3a68daa9798359014f31c1ecfac976d5338a0e346c658a121")
PARENT_CERT_SHA256 = (
    "7780856a7394f8060121dd41fc7a0b7cd066cd2c858e8b2a4891090e5577a4a6")

SCHEMA = "TPC363_BULK_PERSISTENCE_LOCALIZATION_V1"
STATUS = "NUMERICALLY_CERTIFIED_FINITE_BULK_PERSISTENCE_OBSTRUCTION"
ROUND2_CLUE = "TEST_RENORMALIZED_HIGH_Q_REPAIR_ON_EXPLICIT_HOLDOUT"

ORIGINS = (313030, 311166, 321651)
COUNTS = (256, 512)
Q_ANCHORS = (80, 128, 256)
EXPONENTS = (1, 2)
LAWS = ("all_plus", "alternating_index", "mod4_character", "half_split")
HEIGHT = 66
SPECTRAL_CAP = 0.64
SCHUR_CAP = 0.83
TRIM_DENOMINATOR = 20
TOL = 5.0e-5
EXACT_INTERVAL = (313060, 313073)


class CheckFailure(RuntimeError):
    """Raised when a finite certificate cannot be reconstructed."""


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
    spec = importlib.util.spec_from_file_location("tpc355_base_tpc363",
                                                  BASE_CODE)
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
         "TPC362_SHELL_SCALE_CAP_OBSTRUCTION_V1", "parent payload")
    audit = payload.get("finite_audit", {})
    need(audit.get("first_spectral_cap_failure_Q") == 128 and
         audit.get("spectral_cap_violations") == 30,
         "parent first-failure lock")
    return payload


def top_indices(values: np.ndarray, count: int) -> list[int]:
    """Stable descending order, with the original index as tie breaker."""
    need(count >= 1 and count < len(values), "trim count")
    return [int(index) for index in
            np.argsort(-np.asarray(values), kind="mergesort")[:count]]


def restricted_spectral(matrix: np.ndarray, removed: list[int]) -> float:
    keep = np.ones(matrix.shape[0], dtype=bool)
    keep[np.asarray(removed, dtype=np.int64)] = False
    reduced = matrix[np.ix_(keep, keep)]
    eigenvalues = np.linalg.eigvalsh(reduced)
    value = max(abs(float(eigenvalues[0])), abs(float(eigenvalues[-1])))
    need(math.isfinite(value) and value > 0.0, "restricted spectrum")
    return value


def metrics(matrix: np.ndarray) -> dict[str, Any]:
    symmetry = float(np.max(np.abs(matrix - matrix.T)))
    row_mass = np.sum(np.abs(matrix), axis=1)
    schur = float(np.max(row_mass))
    frobenius = float(np.sqrt(np.sum(matrix * matrix)))
    need(math.isfinite(symmetry) and symmetry <= 1.0e-12 and
         schur > 0.0 and math.isfinite(frobenius) and frobenius > 0.0,
         "finite matrix envelopes")
    eigenvalues, vectors = np.linalg.eigh(matrix)
    principal = int(np.argmax(np.abs(eigenvalues)))
    minimum = float(eigenvalues[0])
    maximum = float(eigenvalues[-1])
    spectral = max(abs(minimum), abs(maximum))
    vector = vectors[:, principal]
    mass = vector * vector
    trim_count = max(1, matrix.shape[0] // TRIM_DENOMINATOR)
    schur_indices = top_indices(row_mass, trim_count)
    eigen_indices = top_indices(mass, trim_count)
    trimmed_schur = restricted_spectral(matrix, schur_indices)
    trimmed_eigen = restricted_spectral(matrix, eigen_indices)
    need(math.isfinite(spectral) and spectral > 0.0 and
         spectral <= schur + 2.0e-10 * max(1.0, schur) and
         spectral <= frobenius + 2.0e-10 * max(1.0, frobenius),
         "finite spectral envelopes")
    need(math.isfinite(trimmed_schur) and math.isfinite(trimmed_eigen),
         "finite trimmed envelopes")
    top5 = min(5, len(mass))
    return {
        "schur": show(schur), "frobenius": show(frobenius),
        "spectral": show(spectral), "minimum_eigenvalue": show(minimum),
        "maximum_eigenvalue": show(maximum), "symmetry_error": show(symmetry),
        "spectral_over_schur": show(spectral / schur),
        "spectral_over_frobenius": show(spectral / frobenius),
        "schur_row_index": int(np.argmax(row_mass)),
        "schur_row_mass": show(float(np.max(row_mass))),
        "principal_eigen_index": principal,
        "principal_eigenvector_top1_mass": show(float(np.max(mass))),
        "principal_eigenvector_top5_mass": show(
            float(np.sort(mass)[-top5:].sum())),
        "principal_eigenvector_ipr": show(float(np.sum(mass * mass))),
        "principal_eigenvector_effective_support": show(
            float(1.0 / np.sum(mass * mass))),
        "principal_eigenvector_schur_alignment": show(
            float(mass[int(np.argmax(row_mass))])),
        "trim_count": trim_count,
        "schur_trim_indices": schur_indices,
        "eigenvector_trim_indices": eigen_indices,
        "trimmed_spectral_after_schur_rows": show(trimmed_schur),
        "trimmed_spectral_after_eigenvector_rows": show(trimmed_eigen),
        "trimmed_ratio_after_schur_rows": show(trimmed_schur / spectral),
        "trimmed_ratio_after_eigenvector_rows": show(trimmed_eigen / spectral),
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
                            "geometry_mean": show(float(np.mean(geometry))),
                            "geometry_cv": show(float(np.std(geometry) /
                                                       np.mean(geometry))),
                            "normalized": metrics(matrices[law] / scale),
                        })
    need(len(rows) == 144, "row census")
    return rows


def q_summary(rows: list[dict[str, Any]]) -> dict[str, Any]:
    result: dict[str, Any] = {}
    for q0 in Q_ANCHORS:
        selected = [row for row in rows if row["Q"] == q0]
        spectra = [float(row["normalized"]["spectral"]) for row in selected]
        trimmed = [float(row["normalized"][key]) for row in selected
                   for key in ("trimmed_spectral_after_schur_rows",
                               "trimmed_spectral_after_eigenvector_rows")]
        result[str(q0)] = {
            "rows": len(selected),
            "spectral_min": show(min(spectra)),
            "spectral_max": show(max(spectra)),
            "spectral_cap_violations": sum(v > SPECTRAL_CAP for v in spectra),
            "trimmed_spectral_min": show(min(trimmed)),
            "trimmed_spectral_max": show(max(trimmed)),
            "trimmed_spectral_cap_violations": sum(v > SPECTRAL_CAP
                                                    for v in trimmed),
        }
    return result


def law_census(rows: list[dict[str, Any]]) -> dict[str, Any]:
    violations = [row for row in rows
                  if float(row["normalized"]["spectral"]) > SPECTRAL_CAP]
    counts = {law: sum(row["law"] == law for row in violations)
              for law in LAWS}
    persistent_schur = sum(
        float(row["normalized"]["trimmed_spectral_after_schur_rows"]) >
        SPECTRAL_CAP for row in violations)
    persistent_eigen = sum(
        float(row["normalized"]["trimmed_spectral_after_eigenvector_rows"]) >
        SPECTRAL_CAP for row in violations)
    need(len(violations) == 18 and counts == {
        "all_plus": 18, "alternating_index": 0,
        "mod4_character": 0, "half_split": 0}, "violation census")
    need(persistent_schur == 18 and persistent_eigen == 18,
         "bulk persistence census")
    return {
        "spectral_cap": show(SPECTRAL_CAP),
        "violating_rows": len(violations), "violation_law_counts": counts,
        "persistent_after_schur_trim": persistent_schur,
        "persistent_after_eigenvector_trim": persistent_eigen,
        "rows": [
            {"origin": row["origin"], "count": row["count"],
             "Q": row["Q"], "kernel_exponent": row["kernel_exponent"],
             "law": row["law"],
             "spectral": row["normalized"]["spectral"],
             "trimmed_schur": row["normalized"][
                 "trimmed_spectral_after_schur_rows"],
             "trimmed_eigenvector": row["normalized"][
                 "trimmed_spectral_after_eigenvector_rows"],
             "top1_mass": row["normalized"][
                 "principal_eigenvector_top1_mass"],
             "ipr": row["normalized"]["principal_eigenvector_ipr"]}
            for row in violations
        ],
    }


def bulk_audit(rows: list[dict[str, Any]]) -> dict[str, Any]:
    violating = [row for row in rows
                 if float(row["normalized"]["spectral"]) > SPECTRAL_CAP]
    controls = [row for row in rows
                if float(row["normalized"]["spectral"]) <= SPECTRAL_CAP]
    trim_values = [float(row["normalized"][key]) for row in violating
                   for key in ("trimmed_spectral_after_schur_rows",
                               "trimmed_spectral_after_eigenvector_rows")]
    control_trim_values = [float(row["normalized"][key]) for row in controls
                           for key in ("trimmed_spectral_after_schur_rows",
                                       "trimmed_spectral_after_eigenvector_rows")]
    q128 = [row for row in violating if row["Q"] == 128]
    q256 = [row for row in violating if row["Q"] == 256]
    need(len(violating) == 18 and len(q128) == 6 and len(q256) == 12,
         "failure strata")
    need(max(control_trim_values) < SPECTRAL_CAP and
         min(trim_values) > SPECTRAL_CAP, "trim separation")
    top1 = [float(row["normalized"]["principal_eigenvector_top1_mass"])
            for row in violating]
    ipr = [float(row["normalized"]["principal_eigenvector_ipr"])
           for row in violating]
    return {
        "rows": len(rows), "settings": 36, "laws": len(LAWS),
        "spectral_rows": len(rows), "spectral_cap": show(SPECTRAL_CAP),
        "schur_cap": show(SCHUR_CAP),
        "spectral_cap_violations": len(violating),
        "spectral_cap_violations_Q128": len(q128),
        "spectral_cap_violations_Q256": len(q256),
        "first_spectral_cap_failure_Q": 128,
        "bulk_persistence_after_schur_trim": len(q128) + len(q256),
        "bulk_persistence_after_eigenvector_trim": len(q128) + len(q256),
        "min_trimmed_spectral_over_violations": show(min(trim_values)),
        "min_trimmed_spectral_Q128_over_violations": show(min(
            float(row["normalized"][key]) for row in q128
            for key in ("trimmed_spectral_after_schur_rows",
                        "trimmed_spectral_after_eigenvector_rows"))),
        "min_trimmed_spectral_Q256_over_violations": show(min(
            float(row["normalized"][key]) for row in q256
            for key in ("trimmed_spectral_after_schur_rows",
                        "trimmed_spectral_after_eigenvector_rows"))),
        "max_trimmed_spectral_Q80_control": show(max(
            float(row["normalized"][key]) for row in controls
            if row["Q"] == 80
            for key in ("trimmed_spectral_after_schur_rows",
                        "trimmed_spectral_after_eigenvector_rows"))),
        "max_violating_top1_mass": show(max(top1)),
        "max_violating_ipr": show(max(ipr)),
        "min_violating_effective_support_fraction": show(min(
            1.0 / float(row["normalized"]["principal_eigenvector_ipr"])
            / row["count"] for row in violating)),
        "finite_schur_violations": 0,
        "finite_frobenius_violations": 0,
        "fixed_power_credit": 0, "arithmetic_advance": "NO",
        "trim_rule": "remove floor(N/20) rows; stable descending score",
        "trim_fraction": "1/20",
    }


def exact_anchor() -> dict[str, Any]:
    values = list(range(EXACT_INTERVAL[0], EXACT_INTERVAL[1] + 1))
    shell = BASE.shell_for(4)

    def entry(prime: int, u: int, t: int) -> Fraction:
        if u == t or u % prime == 0 or t % prime == 0:
            return Fraction(0)
        centered = Fraction(int((u - t) % prime == 0), 1) - Fraction(1,
                                                                       prime - 1)
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
        "interval": list(EXACT_INTERVAL), "Q": 4,
        "kernel_exponent": 1, "shell": shell,
        "matrix_symmetric": True, "geometry_positive": True,
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
    rows = build_rows()
    audit = bulk_audit(rows)
    qstats = q_summary(rows)
    census = law_census(rows)
    need(qstats["80"]["spectral_cap_violations"] == 0 and
         qstats["128"]["spectral_cap_violations"] == 6 and
         qstats["256"]["spectral_cap_violations"] == 12,
         "Q failure census")
    return {
        "schema": SCHEMA, "status": STATUS,
        "parent_lock": {
            "base_code_sha256": BASE_CODE_SHA256,
            "parent_code_sha256": PARENT_CODE_SHA256,
            "parent_certificate_sha256": PARENT_CERT_SHA256,
            "parent_schema": parent["schema"],
        },
        "protocol": {
            "origins": list(ORIGINS), "counts": list(COUNTS),
            "q_anchors": list(Q_ANCHORS), "kernel_exponents": list(EXPONENTS),
            "height": HEIGHT, "laws": list(LAWS),
            "spectra_for_all_laws": True, "source_response_used": False,
            "parent_panel": "TPC-361 frozen high-origin panel",
            "trim_denominator": TRIM_DENOMINATOR,
            "trim_selection": "stable descending Schur row mass or principal eigenvector coordinate mass",
            "operator": "literal deleted-diagonal two-endpoint divisibility-masked prime-shell operator",
            "normalization": "TPC-355 unsigned mask-energy symmetric congruence",
        },
        "exact_theorem": {
            "schur": "For finite real symmetric T, ||T||_2 <= max_u sum_t |T(u,t)|.",
            "frobenius": "For finite real T, ||T||_2 <= ||T||_F.",
            "principal_restriction": "Deleting an index set produces the finite principal submatrix T[J^c,J^c]; its spectrum is recomputed independently.",
            "scope": "all persistence and localization statements are finite observations on the declared rows",
        },
        "finite_audit": audit, "q_summaries": qstats,
        "law_census": census,
        "rows": rows,
        "row_digest": hashlib.sha256(canonical(rows)).hexdigest(),
        "exact_anchor": exact_anchor(),
        "claim_firewall": {
            "TPC363_FINITE_REPLAY": "NUMERICALLY_CERTIFIED_FINITE_144_ROWS",
            "TPC363_FINITE_ENVELOPE_INEQUALITIES": "PROVED_EXACT_FINITE",
            "TPC363_FIRST_Q128_FAILURE": "NUMERICALLY_CERTIFIED_FINITE_SCOPED",
            "TPC363_BULK_PERSISTENCE": "NUMERICALLY_CERTIFIED_FINITE_SCOPED",
            "TPC363_SINGLE_ROW_SPIKE_EXPLANATION": "REFUTED_SCOPED_ON_DECLARED_TRIMS",
            "TPC363_EIGENVECTOR_DELOCALIZATION": "NUMERICALLY_CERTIFIED_FINITE_SCOPED",
            "TPC363_RENORMALIZED_REPAIR": "OPEN",
            "TPC363_GROWING_OPERATOR_BOUND": "OPEN",
            "TPC363_SOURCE_UNIFORM_L2": "OPEN",
            "TPC363_ARITHMETIC_ADVANCE": "NO",
            "TPC363_FIXED_POWER_CREDIT": 0,
            "TPC363_FULL_GATE_B": "OPEN", "TPC363_TWIN_PRIME_RESULT": "NONE",
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
            print("TPC363_CERTIFICATE=WRITTEN")
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
            print("TPC363_CERTIFICATE=PASS rows=144 violations=" +
                  str(payload["finite_audit"]["spectral_cap_violations"]) +
                  " persistent=18")
    except (CheckFailure, OSError, json.JSONDecodeError, ValueError, TypeError,
            KeyError, np.linalg.LinAlgError) as error:
        print("TPC363_CERTIFICATE=FAIL " + str(error), file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
