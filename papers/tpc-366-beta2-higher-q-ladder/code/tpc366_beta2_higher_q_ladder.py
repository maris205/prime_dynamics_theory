#!/usr/bin/env python3
"""TPC-366: fixed beta=2 on a higher-Q, new-scale ladder."""

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
RESULT = PROJECT / "results/tpc366_certificate.json"
BASE_CODE = ROOT / (
    "papers/tpc-355-position-aware-mask-energy-normalization/code/"
    "tpc355_position_aware_mask_energy_normalization.py")
PARENT_CODE = ROOT / (
    "papers/tpc-365-beta2-fresh-holdout/code/"
    "tpc365_beta2_fresh_holdout.py")
PARENT_CERT = ROOT / (
    "papers/tpc-365-beta2-fresh-holdout/results/"
    "tpc365_certificate.json")

BASE_CODE_SHA256 = (
    "b54883cbc2e9e19dd8cf6fbece69ff7752ba805678e0b5b2fcf82949dd42fde9")
PARENT_CODE_SHA256 = (
    "2017e42834eda4f015ae33c75a2b34516d6a0cc0c49a91aee98abb1adb0fb7db")
PARENT_CERT_SHA256 = (
    "39a55a6bd7c2ed05d02b7524236d0cbcb67c2a9467940825b170c138ad8ed5c8")

SCHEMA = "TPC366_BETA2_HIGHER_Q_LADDER_V1"
STATUS = "NUMERICALLY_CERTIFIED_FINITE_BETA2_HIGHER_Q_LADDER"
ROUND2_CLUE = "TEST_BETA2_ON_LONGER_WINDOWS_AND_UNSELECTED_ORIGINS"

CANDIDATE_ORIGINS = tuple(620001 + 307 * j for j in range(41))
PILOT_COUNT = 256
SELECTED_COUNT = 3
MIN_SEPARATION = 2048
ORIGINS = (623071, 631360, 629211)
COUNTS = (256, 512)
Q_ANCHORS = (512, 1024, 2048, 4096, 8192)
EXPONENTS = (1, 2)
LAWS = ("all_plus", "alternating_index", "mod4_character", "half_split")
BETAS = (0, 2)
SELECTION_BETA = 2
HEIGHT = 66
SPECTRAL_CAP = 0.64
SCHUR_CAP = 0.83
EXACT_INTERVAL = (623372, 623385)
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
    spec = importlib.util.spec_from_file_location("tpc355_base_tpc366",
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
         payload.get("schema") == "TPC365_BETA2_FRESH_HOLDOUT_V1",
         "parent payload")
    return payload


def weighted_geometry_only(values: np.ndarray, q0: int, exponent: int,
                           beta: int) -> np.ndarray:
    difference = values[:, None] - values[None, :]
    distance = difference.astype(np.float64)
    kernel = (float(HEIGHT) ** (2 * exponent) /
              (HEIGHT * HEIGHT + distance * distance) ** exponent)
    np.fill_diagonal(kernel, 0.0)
    geometry = np.zeros(len(values), dtype=np.float64)
    for prime in BASE.shell_for(q0):
        weight = (float(prime) / float(q0)) ** beta
        centered = ((difference % prime == 0).astype(np.float64) -
                    1.0 / (prime - 1))
        np.fill_diagonal(centered, 0.0)
        valid = ((difference != 0) &
                 (values[:, None] % prime != 0) &
                 (values[None, :] % prime != 0))
        block = weight * float(prime) * kernel * centered * valid
        geometry += np.sum(block * block, axis=1)
    need(bool(np.all(np.isfinite(geometry) & (geometry > 0))),
         "pilot geometry")
    return geometry


def geometry_selection() -> tuple[dict[str, Any], list[int]]:
    records: list[dict[str, Any]] = []
    for origin in CANDIDATE_ORIGINS:
        values = np.arange(origin, origin + PILOT_COUNT, dtype=np.int64)
        settings: list[dict[str, Any]] = []
        for q0 in Q_ANCHORS:
            for exponent in EXPONENTS:
                geometry = weighted_geometry_only(values, q0, exponent,
                                                  SELECTION_BETA)
                settings.append({
                    "Q": q0, "kernel_exponent": exponent,
                    "geometry_min": show(float(np.min(geometry))),
                    "geometry_max": show(float(np.max(geometry))),
                    "spread": show(float(np.max(geometry) /
                                         np.min(geometry))),
                    "coefficient_of_variation": show(float(
                        np.std(geometry) / np.mean(geometry))),
                })
        best = max(settings, key=lambda item: (
            float(item["spread"]), -item["Q"], -item["kernel_exponent"]))
        records.append({
            "origin": origin, "pilot_count": PILOT_COUNT,
            "selection_beta": SELECTION_BETA, "score": best["spread"],
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
        if all(abs(record["origin"] - old) >= MIN_SEPARATION
               for old in chosen):
            chosen.append(record["origin"])
        if len(chosen) == SELECTED_COUNT:
            break
    need(tuple(chosen) == ORIGINS, "selected-origin rule")
    return {
        "candidate_origins": list(CANDIDATE_ORIGINS),
        "candidate_count": len(CANDIDATE_ORIGINS),
        "pilot_count": PILOT_COUNT, "selection_beta": SELECTION_BETA,
        "minimum_separation": MIN_SEPARATION,
        "selected_origins": chosen,
        "ranked_records": records,
        "selection_rule": "descending geometry spread; origin tie-break; greedy separation",
    }, chosen


def weighted_components(values: np.ndarray, q0: int, exponent: int,
                        beta: int):
    difference = values[:, None] - values[None, :]
    distance = difference.astype(np.float64)
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
        centered = ((difference % prime == 0).astype(np.float64) -
                    1.0 / (prime - 1))
        np.fill_diagonal(centered, 0.0)
        valid = ((difference != 0) &
                 (values[:, None] % prime != 0) &
                 (values[None, :] % prime != 0))
        block = weight * float(prime) * kernel * centered * valid
        geometry += np.sum(block * block, axis=1)
        for law in LAWS:
            matrices[law] += signs[law][index] * block
    for matrix in matrices.values():
        matrix[:] = (matrix + matrix.T) / 2.0
    need(bool(np.all(np.isfinite(geometry) & (geometry > 0))),
         "geometry positivity")
    return primes, matrices, geometry, weights


def matrix_metrics(matrix: np.ndarray) -> dict[str, Any]:
    symmetry = float(np.max(np.abs(matrix - matrix.T)))
    row_mass = np.sum(np.abs(matrix), axis=1)
    schur = float(np.max(row_mass))
    frobenius = float(np.sqrt(np.sum(matrix * matrix)))
    need(math.isfinite(symmetry) and symmetry <= 1.0e-12 and
         schur > 0.0 and math.isfinite(frobenius) and frobenius > 0.0,
         "finite metrics")
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
    effective = float(np.sum(np.asarray(weights) ** 2) ** 2 /
                      np.sum(np.asarray(weights) ** 4))
    return {
        "origin": origin, "count": count,
        "interval": [origin, origin + count - 1], "Q": q0,
        "kernel_exponent": exponent, "beta": beta, "law": law,
        "height": HEIGHT, "shell": primes, "shell_cardinality": len(primes),
        "weight_min": show(min(weights)), "weight_max": show(max(weights)),
        "weight_effective_count": show(effective),
        "weight_effective_fraction": show(effective / len(weights)),
        "geometry_min": show(float(np.min(geometry))),
        "geometry_max": show(float(np.max(geometry))),
        "geometry_spread": show(float(np.max(geometry) /
                                       np.min(geometry))),
        "raw": matrix_metrics(matrices[law]),
        "normalized": matrix_metrics(normalized),
    }


def build_rows(origins: list[int]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for beta in BETAS:
        for origin in origins:
            for count in COUNTS:
                for q0 in Q_ANCHORS:
                    for exponent in EXPONENTS:
                        for law in LAWS:
                            rows.append(row_record(origin, count, q0,
                                                   exponent, beta, law))
    need(len(rows) == 480, "row census")
    return rows


def phase_summary(rows: list[dict[str, Any]]) -> dict[str, Any]:
    by_beta: dict[str, Any] = {}
    by_beta_q: dict[str, Any] = {}
    for beta in BETAS:
        selected = [row for row in rows if row["beta"] == beta]
        spectra = [float(row["normalized"]["spectral"]) for row in selected]
        by_beta[str(beta)] = {
            "rows": len(selected), "spectral_min": show(min(spectra)),
            "spectral_max": show(max(spectra)),
            "spectral_cap_violations": sum(v > SPECTRAL_CAP for v in spectra),
            "schur_max": show(max(float(row["normalized"]["schur"])
                                   for row in selected)),
            "schur_cap_violations": sum(
                float(row["normalized"]["schur"]) > SCHUR_CAP
                for row in selected),
            "effective_fraction_min": show(min(
                float(row["weight_effective_fraction"]) for row in selected)),
        }
        for q0 in Q_ANCHORS:
            qrows = [row for row in selected if row["Q"] == q0]
            qvalues = [float(row["normalized"]["spectral"]) for row in qrows]
            by_beta_q[f"{beta}:{q0}"] = {
                "beta": beta, "Q": q0, "rows": len(qrows),
                "spectral_min": show(min(qvalues)),
                "spectral_max": show(max(qvalues)),
                "spectral_cap_violations": sum(v > SPECTRAL_CAP
                                                for v in qvalues),
                "schur_cap_violations": sum(
                    float(row["normalized"]["schur"]) > SCHUR_CAP
                    for row in qrows),
            }
    need(by_beta["0"]["spectral_cap_violations"] == 60,
         "baseline violation census")
    need(by_beta["2"]["spectral_cap_violations"] == 0,
         "beta2 higher-Q census")
    need(by_beta["0"]["schur_cap_violations"] == 60,
         "baseline Schur census")
    need(by_beta["2"]["schur_cap_violations"] == 0,
         "beta2 Schur census")
    return {"by_beta": by_beta, "by_beta_q": by_beta_q,
            "cap_repair_betas": [2], "cap": show(SPECTRAL_CAP),
            "schur_cap": show(SCHUR_CAP)}


def exact_anchor() -> dict[str, Any]:
    values = list(range(*EXACT_INTERVAL))
    primes = BASE.shell_for(EXACT_Q)
    text = lambda value: f"{value.numerator}/{value.denominator}"
    anchors: list[dict[str, Any]] = []
    for beta in BETAS:
        matrix: list[list[Fraction]] = []
        geometry: list[Fraction] = []
        for u in values:
            row: list[Fraction] = []
            grow = Fraction(0)
            for t in values:
                total = Fraction(0)
                energy = Fraction(0)
                for prime in primes:
                    base = BASE.exact_entry(prime, u, t, EXACT_EXPONENT)
                    weighted = Fraction(prime, EXACT_Q) ** beta * base
                    total += weighted
                    energy += weighted * weighted
                row.append(total)
                grow += energy
            matrix.append(row)
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
    selection, origins = geometry_selection()
    rows = build_rows(origins)
    phase = phase_summary(rows)
    parent_phase = parent["phase_summary"]["by_beta"]["2"]
    higher_max = float(phase["by_beta"]["2"]["spectral_max"])
    parent_max = float(parent_phase["spectral_max"])
    need(higher_max <= SPECTRAL_CAP, "higher-Q beta2 cap")
    return {
        "schema": SCHEMA, "status": STATUS,
        "parent_lock": {
            "base_code_sha256": BASE_CODE_SHA256,
            "parent_code_sha256": PARENT_CODE_SHA256,
            "parent_certificate_sha256": PARENT_CERT_SHA256,
            "parent_schema": parent["schema"],
        },
        "selection": selection,
        "protocol": {
            "origins": origins, "counts": list(COUNTS),
            "q_anchors": list(Q_ANCHORS), "kernel_exponents": list(EXPONENTS),
            "laws": list(LAWS), "betas": list(BETAS),
            "selection_beta": SELECTION_BETA, "pilot_count": PILOT_COUNT,
            "minimum_separation": MIN_SEPARATION, "height": HEIGHT,
            "spectra_for_all_laws": True, "source_response_used": False,
            "selection_response_blind": True,
            "weight_rule": "w_(p,beta)=(p/Q)^beta",
            "normalization": "weighted square-energy symmetric congruence",
            "parent_panel": "TPC-365 beta=2 response-blind finite holdout",
        },
        "exact_theorem": {
            "selection": "The declared score and greedy rule are finite deterministic operations on unsigned weighted geometry.",
            "geometry": "The weighted geometry is a finite sum of nonnegative rational squares.",
            "congruence": "Positive geometry makes the finite weighted symmetric congruence well-defined.",
            "envelopes": "For finite real T, ||T||_2 <= max row absolute sum and ||T||_2 <= ||T||_F.",
            "scale_scope": "The higher-Q result is restricted to the declared five-anchor ladder and three selected origins.",
        },
        "finite_audit": {
            "rows": len(rows), "settings_per_beta": 240,
            "beta_count": len(BETAS), "spectral_rows": len(rows),
            "beta2_rows": 240, "beta2_cap_violations": 0,
            "beta2_schur_cap_violations": 0,
            "baseline_beta0_cap_violations": 60,
            "baseline_beta0_schur_cap_violations": 60,
            "q_min": min(Q_ANCHORS), "q_max": max(Q_ANCHORS),
            "parent_beta2_max_spectral": show(parent_max),
            "higher_q_beta2_max_spectral": show(higher_max),
            "higher_q_minus_parent_max_spectral": show(higher_max - parent_max),
            "fixed_power_credit": 0, "arithmetic_advance": "NO",
        },
        "phase_summary": phase,
        "rows": rows,
        "row_digest": hashlib.sha256(canonical(rows)).hexdigest(),
        "exact_anchor": exact_anchor(),
        "claim_firewall": {
            "TPC366_GEOMETRY_SELECTION": "PROVED_EXACT_FINITE_RESPONSE_BLIND",
            "TPC366_WEIGHTED_GEOMETRY_POSITIVITY": "PROVED_EXACT_FINITE",
            "TPC366_FINITE_REPLAY": "NUMERICALLY_CERTIFIED_FINITE_480_ROWS",
            "TPC366_HIGHER_Q_LADDER": "NUMERICALLY_CERTIFIED_FINITE_SCOPED",
            "TPC366_BETA2_HIGHER_Q_CAP": "NUMERICALLY_CERTIFIED_FINITE_SCOPED",
            "TPC366_BETA2_SCALE_UNIFORMITY": "OPEN",
            "TPC366_BETA2_ASYMPTOTIC_REPAIR": "OPEN",
            "TPC366_NORMALIZATION_SOURCE_VALIDITY": "MODELING_CHOICE_OPEN",
            "TPC366_GROWING_OPERATOR_BOUND": "OPEN",
            "TPC366_SOURCE_UNIFORM_L2": "OPEN",
            "TPC366_ARITHMETIC_ADVANCE": "NO",
            "TPC366_FIXED_POWER_CREDIT": 0,
            "TPC366_FULL_GATE_B": "OPEN", "TPC366_TWIN_PRIME_RESULT": "NONE",
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
            print("TPC366_CERTIFICATE=WRITTEN")
        else:
            raw = RESULT.read_bytes()
            stored = json.loads(raw)
            need(raw == canonical(stored), "certificate canonicality")
            need(stored == build_document(), "certificate replay")
            print("TPC366_CERTIFICATE=PASS rows=480 beta2_rows=240 "
                  "beta2_violations=0 baseline_beta0_violations=60")
    except (CheckFailure, OSError, json.JSONDecodeError, ValueError, TypeError,
            KeyError, np.linalg.LinAlgError) as error:
        print("TPC366_CERTIFICATE=FAIL " + str(error), file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
