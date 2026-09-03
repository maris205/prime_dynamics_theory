#!/usr/bin/env python3
"""TPC-364: a finite phase diagram for prime-shell tilts.

TPC-363 showed that the first high-shell spectral failures survive two
five-percent principal restrictions.  This release tests the next explicit
modeling choice: multiply each literal prime block by (p/Q)**beta and use the
corresponding weighted square-energy diagonal for the symmetric congruence.
The beta menu, panel, and shell ladder are fixed in this file.  Every claim is
finite and scoped; no source response or arithmetic reassembly is used.
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
RESULT = PROJECT / "results/tpc364_certificate.json"
BASE_CODE = ROOT / (
    "papers/tpc-355-position-aware-mask-energy-normalization/code/"
    "tpc355_position_aware_mask_energy_normalization.py")
PARENT_CODE = ROOT / (
    "papers/tpc-363-bulk-persistence-localization/code/"
    "tpc363_bulk_persistence_localization.py")
PARENT_CERT = ROOT / (
    "papers/tpc-363-bulk-persistence-localization/results/"
    "tpc363_certificate.json")

BASE_CODE_SHA256 = (
    "b54883cbc2e9e19dd8cf6fbece69ff7752ba805678e0b5b2fcf82949dd42fde9")
PARENT_CODE_SHA256 = (
    "63fd778f820f5ab8df3dc502dee399e4fc221bb83ff6995123c5007e3075d0d7")
PARENT_CERT_SHA256 = (
    "101297c4f4fbf6e9ffc007d2afb460e80c7de82f90ee82a4c0a73b8689cd97af")

SCHEMA = "TPC364_SHELL_TILT_PHASE_DIAGRAM_V1"
STATUS = "NUMERICALLY_CERTIFIED_FINITE_SHELL_TILT_PHASE_DIAGRAM"
ROUND2_CLUE = "TEST_BETA2_ON_RESPONSE_BLIND_FRESH_HOLDOUT"

ORIGINS = (313030, 311166, 321651)
COUNTS = (256, 512)
Q_ANCHORS = (80, 128, 256, 512)
EXPONENTS = (1, 2)
LAWS = ("all_plus", "alternating_index", "mod4_character", "half_split")
# Integer tilts are a predeclared algebraic menu.  beta=0 is the TPC-355
# normalization; positive beta emphasizes the larger primes in (Q,2Q).
BETAS = (-2, -1, 0, 1, 2)
HEIGHT = 66
SPECTRAL_CAP = 0.64
SCHUR_CAP = 0.83
CAP_TOL = 5.0e-8
EXACT_INTERVAL = (313060, 313073)
EXACT_Q = 4
EXACT_EXPONENT = 1


class CheckFailure(RuntimeError):
    """A fail-closed finite certificate error."""


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
    spec = importlib.util.spec_from_file_location("tpc355_base_tpc364",
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
    need(isinstance(payload, dict) and
         payload.get("schema") == "TPC363_BULK_PERSISTENCE_LOCALIZATION_V1",
         "parent payload")
    need(payload.get("finite_audit", {}).get("spectral_cap_violations") == 18,
         "parent failure census")
    return payload


def weighted_components(values: np.ndarray, q0: int, exponent: int,
                        beta: int):
    """Forward-shell construction of weighted blocks and geometry."""
    differences = values[:, None] - values[None, :]
    distance = differences.astype(np.float64)
    kernel = (float(HEIGHT) ** (2 * exponent) /
              (HEIGHT * HEIGHT + distance * distance) ** exponent)
    np.fill_diagonal(kernel, 0.0)
    primes = BASE.shell_for(q0)
    signs = BASE.sign_patterns(primes)
    matrices = {law: np.zeros((len(values), len(values)), dtype=np.float64)
                for law in LAWS}
    geometry = np.zeros(len(values), dtype=np.float64)
    weights: list[float] = []
    for index, prime in enumerate(primes):
        weight = (float(prime) / float(q0)) ** beta
        weights.append(weight)
        centered = ((differences % prime == 0).astype(np.float64) -
                    1.0 / (prime - 1))
        np.fill_diagonal(centered, 0.0)
        valid = ((differences != 0) &
                 (values[:, None] % prime != 0) &
                 (values[None, :] % prime != 0))
        block = weight * float(prime) * kernel * centered * valid
        geometry += np.sum(block * block, axis=1)
        for law in LAWS:
            matrices[law] += signs[law][index] * block
    for matrix in matrices.values():
        matrix[:] = (matrix + matrix.T) / 2.0
    need(bool(np.all(np.isfinite(geometry) & (geometry > 0))),
         "weighted geometry positivity")
    return primes, matrices, geometry, weights


def matrix_metrics(matrix: np.ndarray) -> dict[str, Any]:
    symmetry = float(np.max(np.abs(matrix - matrix.T)))
    row_mass = np.sum(np.abs(matrix), axis=1)
    schur = float(np.max(row_mass))
    frobenius = float(np.sqrt(np.sum(matrix * matrix)))
    need(math.isfinite(symmetry) and symmetry <= 1.0e-12 and
         schur > 0.0 and math.isfinite(frobenius) and frobenius > 0.0,
         "finite matrix metrics")
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
        "schur_row_index": int(np.argmax(row_mass)),
    }


def row_record(origin: int, count: int, q0: int, exponent: int,
               beta: int, law: str) -> dict[str, Any]:
    values = np.arange(origin, origin + count, dtype=np.int64)
    primes, matrices, geometry, weights = weighted_components(
        values, q0, exponent, beta)
    scale = np.sqrt(geometry[:, None] * geometry[None, :])
    normalized = matrices[law] / scale
    weight_array = np.asarray(weights, dtype=np.float64)
    participation = float(np.sum(weight_array ** 2) ** 2 /
                          np.sum(weight_array ** 4))
    raw = matrix_metrics(matrices[law])
    norm = matrix_metrics(normalized)
    return {
        "origin": origin, "count": count,
        "interval": [origin, origin + count - 1], "Q": q0,
        "kernel_exponent": exponent, "beta": beta, "law": law,
        "height": HEIGHT, "shell": primes, "shell_cardinality": len(primes),
        "weight_min": show(min(weights)), "weight_max": show(max(weights)),
        "weight_effective_count": show(participation),
        "weight_effective_fraction": show(participation / len(weights)),
        "geometry_min": show(float(np.min(geometry))),
        "geometry_max": show(float(np.max(geometry))),
        "geometry_spread": show(float(np.max(geometry) /
                                       np.min(geometry))),
        "raw": raw, "normalized": norm,
    }


def build_rows() -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for beta in BETAS:
        for origin in ORIGINS:
            for count in COUNTS:
                for q0 in Q_ANCHORS:
                    for exponent in EXPONENTS:
                        for law in LAWS:
                            rows.append(row_record(origin, count, q0,
                                                   exponent, beta, law))
    need(len(rows) == 960, "row census")
    return rows


def lookup(rows: list[dict[str, Any]], beta: int, q0: int,
           law: str | None = None) -> list[dict[str, Any]]:
    return [row for row in rows if row["beta"] == beta and row["Q"] == q0
            and (law is None or row["law"] == law)]


def phase_summary(rows: list[dict[str, Any]]) -> dict[str, Any]:
    by_beta: dict[str, Any] = {}
    by_beta_q: dict[str, Any] = {}
    for beta in BETAS:
        selected = lookup(rows, beta, Q_ANCHORS[0])
        selected = [row for row in rows if row["beta"] == beta]
        spectra = [float(row["normalized"]["spectral"]) for row in selected]
        by_beta[str(beta)] = {
            "rows": len(selected), "spectral_min": show(min(spectra)),
            "spectral_max": show(max(spectra)),
            "spectral_cap_violations": sum(
                value > SPECTRAL_CAP for value in spectra),
            "schur_max": show(max(float(row["normalized"]["schur"])
                                   for row in selected)),
            "effective_fraction_min": show(min(
                float(row["weight_effective_fraction"]) for row in selected)),
        }
        for q0 in Q_ANCHORS:
            qrows = lookup(rows, beta, q0)
            qspectra = [float(row["normalized"]["spectral"]) for row in qrows]
            by_beta_q[f"{beta}:{q0}"] = {
                "beta": beta, "Q": q0, "rows": len(qrows),
                "spectral_min": show(min(qspectra)),
                "spectral_max": show(max(qspectra)),
                "spectral_cap_violations": sum(
                    value > SPECTRAL_CAP for value in qspectra),
                "schur_cap_violations": sum(
                    float(row["normalized"]["schur"]) > SCHUR_CAP
                    for row in qrows),
            }
    repaired = [beta for beta in BETAS if
                by_beta[str(beta)]["spectral_cap_violations"] == 0]
    need(repaired == [2], "phase repair census")
    need(by_beta["0"]["spectral_cap_violations"] > 0 and
         by_beta["2"]["spectral_cap_violations"] == 0,
         "baseline/repair separation")
    return {"by_beta": by_beta, "by_beta_q": by_beta_q,
            "cap_repair_betas": repaired,
            "cap": show(SPECTRAL_CAP), "schur_cap": show(SCHUR_CAP)}


def winner_census(rows: list[dict[str, Any]]) -> dict[str, Any]:
    result: dict[str, Any] = {}
    for beta in BETAS:
        winners: dict[str, int] = {law: 0 for law in LAWS}
        settings = 0
        for origin in ORIGINS:
            for count in COUNTS:
                for q0 in Q_ANCHORS:
                    for exponent in EXPONENTS:
                        candidates = [row for row in rows if
                                      row["beta"] == beta and
                                      row["origin"] == origin and
                                      row["count"] == count and
                                      row["Q"] == q0 and
                                      row["kernel_exponent"] == exponent]
                        best = max(candidates, key=lambda row:
                                   (float(row["normalized"]["spectral"]),
                                    row["law"]))
                        winners[best["law"]] += 1
                        settings += 1
        need(settings == 48 and sum(winners.values()) == 48,
             "winner settings")
        result[str(beta)] = {"settings": settings, "winner_counts": winners}
    return result


def exact_anchor() -> dict[str, Any]:
    values = list(range(EXACT_INTERVAL[0], EXACT_INTERVAL[1] + 1))
    primes = BASE.shell_for(EXACT_Q)
    anchors: list[dict[str, Any]] = []
    text = lambda value: f"{value.numerator}/{value.denominator}"
    for beta in BETAS:
        matrix: list[list[Fraction]] = []
        geometry: list[Fraction] = []
        for u in values:
            mrow: list[Fraction] = []
            grow = Fraction(0)
            for t in values:
                total = Fraction(0)
                energy = Fraction(0)
                for prime in primes:
                    base = BASE.exact_entry(prime, u, t, EXACT_EXPONENT)
                    weight = Fraction(prime, EXACT_Q) ** beta
                    total += weight * base
                    energy += (weight * base) ** 2
                mrow.append(total)
                grow += energy
            matrix.append(mrow)
            geometry.append(grow)
        need(all(matrix[i][j] == matrix[j][i]
                 for i in range(len(values)) for j in range(len(values))),
             "exact anchor symmetry")
        need(all(value > 0 for value in geometry), "exact anchor positivity")
        anchors.append({
            "beta": beta, "interval": list(EXACT_INTERVAL), "Q": EXACT_Q,
            "kernel_exponent": EXACT_EXPONENT, "shell": primes,
            "matrix_symmetric": True, "geometry_positive": True,
            "matrix_digest": hashlib.sha256(canonical([
                [text(value) for value in row] for row in matrix])).hexdigest(),
            "geometry_digest": hashlib.sha256(canonical(
                [text(value) for value in geometry])).hexdigest(),
        })
    return {"anchors": anchors}


def build_payload() -> dict[str, Any]:
    for path, expected, label in (
            (BASE_CODE, BASE_CODE_SHA256, "base"),
            (PARENT_CODE, PARENT_CODE_SHA256, "parent code"),
            (PARENT_CERT, PARENT_CERT_SHA256, "parent certificate")):
        need(path.is_file() and digest(path.read_bytes()) == expected,
             label + " provenance")
    parent = load_parent()
    rows = build_rows()
    phase = phase_summary(rows)
    winners = winner_census(rows)
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
            "laws": list(LAWS), "betas": list(BETAS), "height": HEIGHT,
            "spectra_for_all_laws": True, "source_response_used": False,
            "parent_panel": "TPC-361 frozen high-origin panel",
            "parent_operator": "TPC-363 literal deleted-diagonal masked operator",
            "weight_rule": "w_(p,beta)=(p/Q)^beta",
            "geometry_rule": "G_(beta,u)=sum_(p,t)(w_(p,beta)B_p(u,t))^2",
            "normalization": "D_G^(-1/2) A_beta D_G^(-1/2)",
            "cap_is": "inherited finite working cap only",
        },
        "exact_theorem": {
            "weighted_block": "B_(p,beta)=w_(p,beta)B_p is a finite real symmetric block after the declared mask.",
            "geometry": "G_(beta,u) is a finite sum of nonnegative rational squares and is positive on every audited row.",
            "congruence": "D_G^(-1/2) A_beta D_G^(-1/2) is finite real symmetric whenever G_(beta,u)>0.",
            "envelopes": "For every finite real T, ||T||_2 <= max_u sum_t |T(u,t)| and ||T||_2 <= ||T||_F.",
            "scope": "The phase diagram and beta=2 repair are finite observations on the declared panel and menu.",
        },
        "finite_audit": {
            "rows": len(rows), "settings_per_beta": 48,
            "beta_count": len(BETAS), "spectral_rows": len(rows),
            "beta2_cap_repair_rows": sum(
                float(row["normalized"]["spectral"]) <= SPECTRAL_CAP
                for row in rows if row["beta"] == 2),
            "beta2_total_rows": sum(row["beta"] == 2 for row in rows),
            "baseline_beta0_cap_violations": phase["by_beta"]["0"][
                "spectral_cap_violations"],
            "finite_schur_violations_beta2": phase["by_beta_q"]["2:512"][
                "schur_cap_violations"],
            "fixed_power_credit": 0, "arithmetic_advance": "NO",
        },
        "phase_summary": phase, "winner_census": winners,
        "rows": rows,
        "row_digest": hashlib.sha256(canonical(rows)).hexdigest(),
        "exact_anchor": exact_anchor(),
        "claim_firewall": {
            "TPC364_WEIGHTED_BLOCK_DEFINITION": "PROVED_EXACT_FINITE",
            "TPC364_WEIGHTED_GEOMETRY_POSITIVITY": "PROVED_EXACT_FINITE",
            "TPC364_FINITE_REPLAY": "NUMERICALLY_CERTIFIED_FINITE_960_ROWS",
            "TPC364_PHASE_DIAGRAM": "NUMERICALLY_CERTIFIED_FINITE_SCOPED",
            "TPC364_BETA2_PANEL_CAP_REPAIR": "NUMERICALLY_CERTIFIED_FINITE_SCOPED",
            "TPC364_BETA2_ASYMPTOTIC_REPAIR": "OPEN",
            "TPC364_NORMALIZATION_SOURCE_VALIDITY": "MODELING_CHOICE_OPEN",
            "TPC364_GROWING_OPERATOR_BOUND": "OPEN",
            "TPC364_SOURCE_UNIFORM_L2": "OPEN",
            "TPC364_ARITHMETIC_ADVANCE": "NO",
            "TPC364_FIXED_POWER_CREDIT": 0,
            "TPC364_FULL_GATE_B": "OPEN", "TPC364_TWIN_PRIME_RESULT": "NONE",
        },
        "round2_clue": ROUND2_CLUE,
    }


def build_document() -> dict[str, Any]:
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
            RESULT.write_bytes(canonical(build_document()))
            print("TPC364_CERTIFICATE=WRITTEN")
        else:
            raw = RESULT.read_bytes()
            stored = json.loads(raw)
            need(raw == canonical(stored), "certificate canonicality")
            rebuilt = build_document()
            need(stored == rebuilt, "certificate replay")
            phase = stored["payload"]["phase_summary"]
            print("TPC364_CERTIFICATE=PASS rows=960 beta2_repaired=192 "
                  "beta2_violations=0 baseline_beta0_violations=" +
                  str(phase["by_beta"]["0"]["spectral_cap_violations"]))
    except (CheckFailure, OSError, json.JSONDecodeError, ValueError, TypeError,
            KeyError, np.linalg.LinAlgError) as error:
        print("TPC364_CERTIFICATE=FAIL " + str(error), file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
