#!/usr/bin/env python3
"""TPC-376: a response-blind holdout for the finite c=1 bandwidth rule."""

from __future__ import annotations

import argparse
import hashlib
import importlib.util
import json
import math
import os
from concurrent.futures import ThreadPoolExecutor
from fractions import Fraction
from pathlib import Path
from typing import Any

os.environ.setdefault("OMP_NUM_THREADS", "1")
os.environ.setdefault("OPENBLAS_NUM_THREADS", "1")
os.environ.setdefault("MKL_NUM_THREADS", "1")
import numpy as np

PROJECT = Path(__file__).resolve().parents[1]
ROOT = PROJECT.parents[1]
RESULT = PROJECT / "results/tpc376_certificate.json"
ENGINE_CODE = ROOT / (
    "papers/tpc-375-bandwidth-stability-minimal-cutoff/code/"
    "tpc375_bandwidth_stability_minimal_cutoff.py")
PARENT_CERT = ROOT / (
    "papers/tpc-375-bandwidth-stability-minimal-cutoff/results/"
    "tpc375_certificate.json")

ENGINE_CODE_SHA256 = (
    "f3fee82fb6306a65a5f83cc8a90b9b04e22e41a6df623784304305c863d12a15")
PARENT_CERT_SHA256 = (
    "3ad30c606b669512cfff63907f3876032efb9b566b03f01ff950e775e1b92e65")

SCHEMA = "TPC376_BANDWIDTH_HOLDOUT_REPLICATION_V1"
STATUS = "NUMERICALLY_CERTIFIED_FINITE_BANDWIDTH_HOLDOUT_REPLICATION"
ROUND2_CLUE = "TEST_C1_WINDOW_SCALE_HOLDOUT"

GRID_START = 1010001
GRID_STEP = 401
GRID_COUNT = 41
TRAINING_INDICES = (0, 20, 40)
HOLDOUT_INDICES = (5, 15, 30)
ORIGINS = tuple(GRID_START + GRID_STEP * j for j in HOLDOUT_INDICES)
WINDOW_COUNT = 2048
BLOCK_COUNT = 256
BLOCK_INDICES = tuple(range(8))
BAND_CUTOFF = 1
Q_ANCHORS = (512, 2048, 8192)
EXPONENT = 1
BETA = 2
LAW = "all_plus"
HEIGHT = 66
SPECTRAL_CAP = 0.64
SCHUR_CAP = 0.83
EXACT_INTERVAL = (1012006, 1012019)
EXACT_Q = 4


class CheckFailure(RuntimeError):
    pass


def need(condition: bool, message: str) -> None:
    if type(condition) is not bool or not condition:
        raise CheckFailure(message)
    if not condition:
        raise CheckFailure(message)


def canonical(value: Any) -> bytes:
    return (json.dumps(value, ensure_ascii=True, sort_keys=True,
                       separators=(",", ":")) + "\n").encode("ascii")


def digest(data: bytes) -> str:
    return hashlib.sha256(data.replace(b"\r\n", b"\n").replace(
        b"\r", b"\n")).hexdigest()


def show(value: float) -> str:
    return format(float(value), ".17g")


def load_engine():
    spec = importlib.util.spec_from_file_location("tpc375_engine_tpc376",
                                                  ENGINE_CODE)
    need(spec is not None and spec.loader is not None, "engine module")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


ENGINE = load_engine()


def load_parent() -> dict[str, Any]:
    raw = PARENT_CERT.read_bytes()
    need(digest(raw) == PARENT_CERT_SHA256, "parent certificate provenance")
    document = json.loads(raw)
    need(raw == canonical(document), "parent certificate canonicality")
    payload = document.get("payload")
    need(isinstance(payload, dict) and
         payload.get("schema") == "TPC375_BANDWIDTH_STABILITY_MINIMAL_CUTOFF_V1" and
         payload.get("status") ==
         "NUMERICALLY_CERTIFIED_FINITE_BANDWIDTH_STABILITY",
         "parent payload")
    return payload


def weighted_components(values: np.ndarray, q0: int):
    difference = values[:, None] - values[None, :]
    distance = difference.astype(np.float64)
    kernel = (float(HEIGHT) ** (2 * EXPONENT) /
              (HEIGHT * HEIGHT + distance * distance) ** EXPONENT)
    np.fill_diagonal(kernel, 0.0)
    primes = ENGINE.BASE.shell_for(q0)
    signs = ENGINE.BASE.sign_patterns(primes)
    need(bool(np.all(signs[LAW] == 1.0)), "all-plus sign lock")
    matrix = np.zeros((len(values), len(values)), dtype=np.float64)
    geometry = np.zeros(len(values), dtype=np.float64)
    weights: list[float] = []
    for index, prime in enumerate(primes):
        weight = (float(prime) / float(q0)) ** BETA
        weights.append(weight)
        centered = ((difference % prime == 0).astype(np.float64) -
                    1.0 / (prime - 1))
        np.fill_diagonal(centered, 0.0)
        valid = ((difference != 0) &
                 (values[:, None] % prime != 0) &
                 (values[None, :] % prime != 0))
        block = weight * float(prime) * kernel * centered * valid
        geometry += np.sum(block * block, axis=1)
        matrix += signs[LAW][index] * block
    matrix[:] = (matrix + matrix.T) / 2.0
    need(bool(np.all(np.isfinite(geometry) & (geometry > 0))),
         "geometry positivity")
    return primes, matrix, geometry, weights


def metrics(matrix: np.ndarray, eigenvalues: np.ndarray) -> dict[str, Any]:
    symmetry = float(np.max(np.abs(matrix - matrix.T)))
    row_mass = np.sum(np.abs(matrix), axis=1)
    schur = float(np.max(row_mass))
    frobenius = float(np.sqrt(np.sum(matrix * matrix)))
    lo, hi = float(eigenvalues[0]), float(eigenvalues[-1])
    spectral = max(abs(lo), abs(hi))
    need(symmetry <= 1.0e-12 and schur > 0.0 and frobenius > 0.0 and
         math.isfinite(frobenius) and math.isfinite(spectral) and
         spectral > 0.0 and
         spectral <= schur + 7.0e-9 * max(1.0, schur) and
         spectral <= frobenius + 7.0e-9 * max(1.0, frobenius),
         "finite metric envelope")
    return {
        "schur": show(schur), "frobenius": show(frobenius),
        "spectral": show(spectral), "minimum_eigenvalue": show(lo),
        "maximum_eigenvalue": show(hi), "symmetry_error": show(symmetry),
        "spectral_over_schur": show(spectral / schur),
        "spectral_over_frobenius": show(spectral / frobenius),
        "schur_row_index": int(np.argmax(row_mass)),
    }


def record(origin: int, q0: int) -> dict[str, Any]:
    values = np.arange(origin, origin + WINDOW_COUNT, dtype=np.int64)
    primes, raw, geometry, weights = weighted_components(values, q0)
    full = raw / np.sqrt(geometry[:, None] * geometry[None, :])
    eigenvalues, eigenvectors = np.linalg.eigh(full)
    full_data = metrics(full, eigenvalues)
    lo, hi = float(eigenvalues[0]), float(eigenvalues[-1])
    index = 0 if abs(lo) >= abs(hi) else len(eigenvalues) - 1
    mode_name = "minimum_eigenvalue" if index == 0 else "maximum_eigenvalue"
    vector = np.asarray(eigenvectors[:, index], dtype=np.float64)
    selected = float(eigenvalues[index])
    residual = float(np.max(np.abs(full @ vector - selected * vector)))
    block_ids = np.arange(WINDOW_COUNT, dtype=np.int64) // BLOCK_COUNT
    mask = np.abs(block_ids[:, None] - block_ids[None, :]) <= BAND_CUTOFF
    band = np.where(mask, full, 0.0)
    tail = full - band
    band_eigenvalues = np.linalg.eigvalsh(band)
    band_data = metrics(band, band_eigenvalues)
    band_rayleigh = float(vector @ (band @ vector))
    tail_rayleigh = float(vector @ (tail @ vector))
    rayleigh_error = abs(band_rayleigh + tail_rayleigh - selected)
    tail_schur = float(np.max(np.sum(np.abs(tail), axis=1)))
    tail_frobenius = float(np.sqrt(np.sum(tail * tail)))
    tail_symmetry = float(np.max(np.abs(tail - tail.T)))
    need(residual <= 4.0e-9 and
         abs(float(np.dot(vector, vector)) - 1.0) <= 3.0e-11 and
         rayleigh_error <= 5.0e-12 and tail_symmetry <= 1.0e-12 and
         math.isfinite(tail_schur) and tail_schur > 0.0 and
         math.isfinite(tail_frobenius) and tail_frobenius > 0.0,
         "mode/band identity")
    return {
        "origin": origin, "count": WINDOW_COUNT,
        "interval": [origin, origin + WINDOW_COUNT - 1], "Q": q0,
        "kernel_exponent": EXPONENT, "beta": BETA, "law": LAW,
        "height": HEIGHT, "shell": primes, "shell_cardinality": len(primes),
        "weight_min": show(min(weights)), "weight_max": show(max(weights)),
        "geometry_min": show(float(np.min(geometry))),
        "geometry_max": show(float(np.max(geometry))),
        "geometry_spread": show(float(np.max(geometry) /
                                       np.min(geometry))),
        "full": full_data, "band": band_data,
        "tail": {"schur": show(tail_schur),
                 "frobenius": show(tail_frobenius),
                 "symmetry_error": show(tail_symmetry)},
        "mode": {
            "mode_rule": "largest absolute eigenvalue; minimum mode wins ties",
            "selected_mode": mode_name,
            "selected_eigenvalue": show(selected),
            "selected_eigenvalue_abs": show(abs(selected)),
            "eigen_residual_inf": show(residual),
            "full_mode_norm_error": show(abs(float(np.dot(vector, vector)) - 1.0)),
            "band_rayleigh": show(band_rayleigh),
            "tail_rayleigh": show(tail_rayleigh),
            "band_signed_retention": show(band_rayleigh / selected),
            "tail_signed_fraction": show(tail_rayleigh / selected),
            "band_rayleigh_abs_retention": show(
                abs(band_rayleigh) / abs(selected)),
            "tail_rayleigh_abs_fraction": show(
                abs(tail_rayleigh) / abs(selected)),
            "rayleigh_sum_error": show(rayleigh_error),
        },
        "band_failure": float(band_data["spectral"]) > SPECTRAL_CAP,
        "full_failure": float(full_data["spectral"]) > SPECTRAL_CAP,
    }


def build_rows() -> list[dict[str, Any]]:
    jobs = [(origin, q0) for origin in ORIGINS for q0 in Q_ANCHORS]
    with ThreadPoolExecutor(max_workers=3) as pool:
        rows = list(pool.map(lambda job: record(job[0], job[1]), jobs))
    need(len(rows) == 9, "row census")
    return rows


def phase_summary(rows: list[dict[str, Any]]) -> dict[str, Any]:
    failures = [row for row in rows if row["band_failure"]]
    by_q: dict[str, Any] = {}
    for q0 in Q_ANCHORS:
        setting = [row for row in rows if row["Q"] == q0]
        qfail = [row for row in setting if row["band_failure"]]
        by_q[str(q0)] = {
            "Q": q0, "rows": len(setting),
            "spectral_cap_violations": len(qfail),
            "spectral_values": [row["band"]["spectral"] for row in setting],
        }
    ret = [float(row["mode"]["band_rayleigh_abs_retention"]) for row in rows]
    tails = [float(row["mode"]["tail_rayleigh_abs_fraction"]) for row in rows]
    return {
        "rows": len(rows), "band_cutoff": BAND_CUTOFF,
        "band_definition": "block distance <= 1",
        "caps": {"spectral": show(SPECTRAL_CAP), "schur": show(SCHUR_CAP)},
        "spectral_cap_violations": len(failures),
        "schur_cap_violations": sum(
            float(row["band"]["schur"]) > SCHUR_CAP for row in rows),
        "failure_keys": [[row["origin"], row["count"], row["Q"],
                          row["kernel_exponent"], row["law"]]
                         for row in failures],
        "by_Q": by_q,
        "failure_profile_by_Q": [by_q[str(q)]["spectral_cap_violations"]
                                 for q in Q_ANCHORS],
        "band_abs_retention_min": show(min(ret)),
        "band_abs_retention_max": show(max(ret)),
        "tail_abs_fraction_max": show(max(tails)),
    }


def exact_anchor() -> dict[str, Any]:
    values = list(range(*EXACT_INTERVAL))
    primes = ENGINE.BASE.shell_for(EXACT_Q)

    def text(value: Fraction) -> str:
        return f"{value.numerator}/{value.denominator}"

    matrix: list[list[Fraction]] = []
    geometry: list[Fraction] = []
    for u in values:
        row: list[Fraction] = []
        grow = Fraction(0)
        for t in values:
            total = Fraction(0)
            energy = Fraction(0)
            for prime in primes:
                if u == t or u % prime == 0 or t % prime == 0:
                    base = Fraction(0)
                else:
                    centered = Fraction(int((u - t) % prime == 0), 1)
                    centered -= Fraction(1, prime - 1)
                    base = (prime * Fraction(HEIGHT * HEIGHT,
                                             HEIGHT * HEIGHT + (u - t) ** 2)
                            * centered)
                weighted = Fraction(prime, EXACT_Q) ** BETA * base
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
    return {
        "interval": list(EXACT_INTERVAL), "Q": EXACT_Q,
        "kernel_exponent": EXPONENT, "beta": BETA, "shell": primes,
        "matrix_symmetric": True, "geometry_positive": True,
        "matrix_digest": hashlib.sha256(canonical([
            [text(value) for value in row] for row in matrix])).hexdigest(),
        "geometry_digest": hashlib.sha256(canonical(
            [text(value) for value in geometry])).hexdigest(),
    }


def build_payload() -> dict[str, Any]:
    need(ENGINE_CODE.is_file() and
         digest(ENGINE_CODE.read_bytes()) == ENGINE_CODE_SHA256,
         "engine provenance")
    parent = load_parent()
    rows = build_rows()
    phase = phase_summary(rows)
    need(phase["failure_profile_by_Q"] == [0, 3, 3],
         "holdout failure profile")
    need(phase["spectral_cap_violations"] == 6, "holdout failure count")
    return {
        "schema": SCHEMA, "status": STATUS,
        "parent_lock": {
            "engine_code_sha256": ENGINE_CODE_SHA256,
            "parent_certificate_sha256": PARENT_CERT_SHA256,
            "parent_schema": parent["schema"],
            "parent_round2_clue": parent["round2_clue"],
            "parent_failure_profile_by_Q": [0, 3, 3],
        },
        "selection_protocol": {
            "grid_start": GRID_START, "grid_step": GRID_STEP,
            "grid_count": GRID_COUNT,
            "candidate_rule": "a_j=1010001+401j, 0<=j<41",
            "training_indices": list(TRAINING_INDICES),
            "training_origins": [
                GRID_START + GRID_STEP * j for j in TRAINING_INDICES],
            "holdout_indices": list(HOLDOUT_INDICES),
            "holdout_origins": list(ORIGINS),
            "holdout_rule":
                "first three predeclared reserved indices (5,15,30)",
            "response_used_for_selection": False,
            "signed_metric_used_for_selection": False,
        },
        "protocol": {
            "origins": list(ORIGINS), "window_count": WINDOW_COUNT,
            "block_count": BLOCK_COUNT, "block_indices": list(BLOCK_INDICES),
            "partition": "fixed eight contiguous 256-point blocks",
            "band_cutoff": BAND_CUTOFF,
            "band_definition": "sum of layers with block distance <= 1",
            "q_anchors": list(Q_ANCHORS), "kernel_exponents": [EXPONENT],
            "laws": [LAW], "betas": [BETA], "height": HEIGHT,
            "common_normalization": True, "source_response_used": False,
            "origin_selection_used": False, "row_selection_used": False,
            "mode_rule": "largest absolute eigenvalue; minimum mode wins ties",
            "panel_complete_before_metric_read": True,
        },
        "exact_theorem": {
            "common_normalization":
                "The full-window square-energy geometry is shared by T, B1, and T-B1.",
            "band_identity":
                "The fixed block-distance mask gives T=B1+(T-B1) entrywise.",
            "rayleigh_identity":
                "For the selected full eigenvector, band and tail Rayleigh terms sum to its eigenvalue.",
            "geometry":
                "The normalization diagonal is a finite sum of nonnegative rational squares.",
            "grid_index_holdout":
                "The holdout indices are distinct from the training indices; the grid-index protocol, not interval disjointness, defines the holdout.",
            "parent_inheritance":
                "The c=1 rule and count-2048 protocol are inherited from TPC-375.",
        },
        "finite_audit": {
            "rows": len(rows), "origin_count": len(ORIGINS),
            "q_count": len(Q_ANCHORS), "spectral_rows": len(rows),
            "spectral_cap_violations": phase["spectral_cap_violations"],
            "schur_cap_violations": phase["schur_cap_violations"],
            "failure_keys": phase["failure_keys"],
            "failure_profile_by_Q": phase["failure_profile_by_Q"],
            "fixed_power_credit": 0, "arithmetic_advance": "NO",
        },
        "phase_summary": phase, "rows": rows,
        "row_digest": hashlib.sha256(canonical(rows)).hexdigest(),
        "exact_anchor": exact_anchor(),
        "claim_firewall": {
            "TPC376_SELECTION_PROTOCOL":
                "PROVED_EXACT_FINITE_PREDECLARED_RESPONSE_BLIND",
            "TPC376_COMMON_NORMALIZATION": "PROVED_EXACT_FINITE_INHERITED",
            "TPC376_HOLDOUT_REPLAY":
                "NUMERICALLY_CERTIFIED_FINITE_9_ROWS",
            "TPC376_C1_FAILURE_PROFILE":
                "NUMERICALLY_CERTIFIED_FINITE_SCOPED",
            "TPC376_PARENT_Q_PROFILE_REPLICATION":
                "NUMERICALLY_CERTIFIED_FINITE_SCOPED",
            "TPC376_RAYLEIGH_TAIL":
                "NUMERICALLY_CERTIFIED_FINITE_SCOPED",
            "TPC376_ORIGIN_UNIFORMITY": "OPEN",
            "TPC376_WINDOW_UNIFORMITY": "OPEN",
            "TPC376_C1_SCALE_STABILITY": "OPEN",
            "TPC376_CROSS_BLOCK_CAUSALITY": "OPEN",
            "TPC376_NORMALIZATION_SOURCE_VALIDITY": "MODELING_CHOICE_OPEN",
            "TPC376_GROWING_OPERATOR_BOUND": "OPEN",
            "TPC376_SOURCE_UNIFORM_L2": "OPEN",
            "TPC376_ARITHMETIC_ADVANCE": "NO",
            "TPC376_FIXED_POWER_CREDIT": 0,
            "TPC376_FULL_GATE_B": "OPEN",
            "TPC376_TWIN_PRIME_RESULT": "NONE",
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
            RESULT.parent.mkdir(parents=True, exist_ok=True)
            RESULT.write_bytes(canonical(build_document()))
            print("TPC376_CERTIFICATE=WRITTEN")
        else:
            raw = RESULT.read_bytes()
            stored = json.loads(raw)
            need(raw == canonical(stored), "certificate canonicality")
            rebuilt = build_document()
            need(stored == rebuilt, "certificate replay")
            audit = rebuilt["payload"]["finite_audit"]
            print("TPC376_CERTIFICATE=PASS rows=" + str(audit["rows"]) +
                  " failures=" + str(audit["spectral_cap_violations"]) +
                  " profile=" +
                  ",".join(str(x) for x in audit["failure_profile_by_Q"]))
        return 0
    except (CheckFailure, OSError, ValueError, TypeError, KeyError,
            json.JSONDecodeError) as error:
        print("TPC376_CERTIFICATE=FAIL " + str(error), file=os.sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
