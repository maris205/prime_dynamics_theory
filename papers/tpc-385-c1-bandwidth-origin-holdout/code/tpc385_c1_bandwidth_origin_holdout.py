#!/usr/bin/env python3
"""TPC-385: a response-blind origin holdout for the c=1 bandwidth phase.

The parent TPC-384 phase values are frozen as forecasts.  Three origins are
used only to define a pooled geometry scalar; two later, coordinate-disjoint
origins are then evaluated without changing the bandwidth or normalization
menu.  This is a finite transfer audit, not an asymptotic theorem.
"""

from __future__ import annotations

import argparse
import hashlib
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
RESULT = PROJECT / "results/tpc385_certificate.json"
PARENT_CODE = ROOT / (
    "papers/tpc-384-c1-bandwidth-normalization-phase-diagram/code/"
    "tpc384_c1_bandwidth_normalization_phase_diagram.py")
PARENT_CERT = ROOT / (
    "papers/tpc-384-c1-bandwidth-normalization-phase-diagram/results/"
    "tpc384_certificate.json")
PARENT_CODE_SHA256 = (
    "1a4e152e0753be3bc851a962aa92108334863795881571cbd7b97f119ee37896")
PARENT_CERT_SHA256 = (
    "5e43adf62e172947b66a84c18da1509e57e0e015146cc6755c6a2d31b7135ee7")

SCHEMA = "TPC385_C1_BANDWIDTH_ORIGIN_HOLDOUT_V1"
STATUS = "NUMERICALLY_CERTIFIED_FINITE_C1_BANDWIDTH_ORIGIN_HOLDOUT"
ROUND2_CLUE = "TEST_C1_HOLDOUT_COUNT_BANDWIDTH"
GRID_START = 2_000_001
GRID_STEP = 401
GRID_COUNT = 41
ORIGIN_INDICES = (0, 10, 20, 30, 40)
CALIBRATION_INDICES = (0, 10, 20)
HOLDOUT_INDICES = (30, 40)
ORIGINS = tuple(GRID_START + GRID_STEP * i for i in ORIGIN_INDICES)
CALIBRATION_ORIGINS = tuple(
    GRID_START + GRID_STEP * i for i in CALIBRATION_INDICES)
HOLDOUT_ORIGINS = tuple(
    GRID_START + GRID_STEP * i for i in HOLDOUT_INDICES)
WINDOW_COUNT = 512
BLOCK_LENGTH = 128
BLOCK_COUNT = WINDOW_COUNT // BLOCK_LENGTH
BAND_CUTOFFS = (2, 3)
Q_ANCHORS = (2048, 8192)
EXPONENT = 1
BETA = 2
HEIGHT = 66
LAWS = ("all_plus", "alternating_index", "mod4_character", "half_split")
NORMALIZATIONS = ("local_diagonal", "pooled_train_scalar")
SPREAD_CAP = 0.01
SPECTRAL_CAP = 0.64
SCHUR_CAP = 0.83
FORECAST_ERROR_CAP = 0.01
EXACT_INTERVAL = (ORIGINS[0], ORIGINS[0] + 13)
EXACT_Q = 8

# These are copied from the locked TPC-384 certificate before this panel is
# evaluated.  They are references, not fitted parameters.
PARENT_PHASE_FORECAST = {
    "c2_local_diagonal": "0.61397411407532332",
    "c3_local_diagonal": "0.62079971051100025",
    "c2_pooled_train_scalar": "0.6338401080191296",
    "c3_pooled_train_scalar": "0.63888760360944985",
}

CLAIM_FIREWALL = {
    "TPC385_SELECTION_PROTOCOL":
        "PROVED_EXACT_FINITE_PREDECLARED_RESPONSE_BLIND",
    "TPC385_COORDINATE_DISJOINTNESS": "PROVED_EXACT_FINITE",
    "TPC385_PARENT_PHASE_REFERENCE": "PROVED_EXACT_FINITE_HASHED",
    "TPC385_ORIGIN_HOLDOUT_PANEL":
        "NUMERICALLY_CERTIFIED_FINITE_160_ROWS",
    "TPC385_HOLDOUT_HIGH_Q_TRANSFER":
        "NUMERICALLY_CERTIFIED_FINITE_SCOPED",
    "TPC385_FORECAST_ERROR_CENSUS":
        "NUMERICALLY_CERTIFIED_FINITE_SCOPED",
    "TPC385_BANDWIDTH_MONOTONICITY": "OPEN",
    "TPC385_LAW_UNIFORMITY": "OPEN",
    "TPC385_ORIGIN_UNIFORMITY": "OPEN",
    "TPC385_COUNT_SCALE_UNIFORMITY": "OPEN",
    "TPC385_SOURCE_NORMALIZATION_VALIDITY": "MODELING_CHOICE_OPEN",
    "TPC385_GROWING_OPERATOR_BOUND": "OPEN",
    "TPC385_SOURCE_UNIFORM_L2": "OPEN",
    "TPC385_ARITHMETIC_ADVANCE": "NO",
    "TPC385_FIXED_POWER_CREDIT": 0,
    "TPC385_FULL_GATE_B": "OPEN",
    "TPC385_TWIN_PRIME_RESULT": "NONE",
}


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


def finite_tree(value: Any) -> bool:
    if isinstance(value, float):
        return math.isfinite(value)
    if isinstance(value, dict):
        return all(isinstance(k, str) and finite_tree(v)
                   for k, v in value.items())
    if isinstance(value, list):
        return all(finite_tree(v) for v in value)
    return True


def sieve(limit: int) -> list[int]:
    flags = bytearray(b"\x01") * (limit + 1)
    flags[0:2] = b"\x00\x00"
    for prime in range(2, math.isqrt(limit) + 1):
        if flags[prime]:
            flags[prime * prime:limit + 1:prime] = b"\x00" * (
                ((limit - prime * prime) // prime) + 1)
    return [prime for prime in range(2, limit + 1) if flags[prime]]


PRIMES = sieve(20000)


def shell(q0: int) -> list[int]:
    return [prime for prime in PRIMES if q0 < prime <= 2 * q0]


def signs(primes: list[int]) -> dict[str, np.ndarray]:
    result: dict[str, np.ndarray] = {}
    for law in LAWS:
        values = []
        for index, prime in enumerate(primes):
            positive = (law == "all_plus" or
                        (law == "alternating_index" and index % 2 == 0) or
                        (law == "mod4_character" and prime % 4 == 1) or
                        (law == "half_split" and index < len(primes) / 2))
            values.append(1.0 if positive else -1.0)
        result[law] = np.asarray(values, dtype=np.float64)
    return result


def coordinate_disjointness() -> bool:
    prior = [
        (1200001, 1200001 + 1024), (1208021, 1208021 + 1024),
        (1216041, 1216041 + 1024),
        (1300001, 1300001 + 2048), (1308021, 1308021 + 2048),
        (1316041, 1316041 + 2048),
        (1400001, 1400001 + 2048), (1408021, 1408021 + 2048),
        (1416041, 1416041 + 2048),
        (1600001, 1600001 + 512), (1608021, 1608021 + 512),
        (1616041, 1616041 + 512),
        (1800001, 1800001 + 512), (1808021, 1808021 + 512),
        (1816041, 1816041 + 512),
    ]
    current = [(origin, origin + WINDOW_COUNT) for origin in ORIGINS]
    intervals = prior + current
    return all(a[1] <= b[0] or b[1] <= a[0]
               for i, a in enumerate(intervals)
               for b in intervals[i + 1:])


def weighted_components(values: np.ndarray, q0: int):
    difference = values[:, None] - values[None, :]
    kernel = (float(HEIGHT) ** (2 * EXPONENT) /
              (HEIGHT * HEIGHT + difference.astype(np.float64) ** 2) ** EXPONENT)
    np.fill_diagonal(kernel, 0.0)
    primes = shell(q0)
    sign_vectors = signs(primes)
    matrices = {law: np.zeros((len(values), len(values)), dtype=np.float64)
                for law in LAWS}
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
        for law in LAWS:
            matrices[law] += sign_vectors[law][index] * block
    for law in LAWS:
        matrices[law][:] = (matrices[law] + matrices[law].T) / 2.0
    need(bool(np.all(np.isfinite(geometry) & (geometry > 0))),
         "geometry positivity")
    return primes, matrices, geometry, weights


def metrics(matrix: np.ndarray) -> tuple[float, float, float, float]:
    symmetry = float(np.max(np.abs(matrix - matrix.T)))
    row_mass = np.sum(np.abs(matrix), axis=1)
    schur = float(np.max(row_mass))
    eigenvalues = np.linalg.eigvalsh(matrix)
    spectral = max(abs(float(eigenvalues[0])), abs(float(eigenvalues[-1])))
    frobenius = float(np.sqrt(np.sum(matrix * matrix)))
    need(symmetry <= 2e-12 and schur > 0 and frobenius > 0 and
         math.isfinite(spectral) and spectral <= schur + 1e-8 and
         spectral <= frobenius + 1e-8, "metric envelope")
    return spectral, schur, frobenius, symmetry


def mask_for(cutoff: int) -> np.ndarray:
    block_ids = np.arange(WINDOW_COUNT) // BLOCK_LENGTH
    return np.abs(block_ids[:, None] - block_ids[None, :]) <= cutoff


def make_row(origin: int, q0: int, law: str, norm: str, cutoff: int,
             matrix: np.ndarray, geometry: np.ndarray, pooled: float,
             primes: list[int], weights: list[float], mask: np.ndarray) -> dict[str, Any]:
    if norm == "local_diagonal":
        normalized = matrix / np.sqrt(geometry[:, None] * geometry[None, :])
    else:
        normalized = matrix / pooled
    spectral, schur, frobenius, symmetry = metrics(np.where(mask, normalized, 0.0))
    role = "calibration" if origin in CALIBRATION_ORIGINS else "holdout"
    forecast_key = f"c{cutoff}_{norm}"
    return {
        "origin": origin, "origin_role": role, "Q": q0, "law": law,
        "normalization": norm, "band_cutoff": cutoff,
        "count": WINDOW_COUNT, "interval": [origin, origin + WINDOW_COUNT],
        "block_length": BLOCK_LENGTH, "block_count": BLOCK_COUNT,
        "kernel_exponent": EXPONENT, "beta": BETA, "height": HEIGHT,
        "shell_cardinality": len(primes), "weight_min": show(min(weights)),
        "weight_max": show(max(weights)), "geometry_min": show(float(np.min(geometry))),
        "geometry_max": show(float(np.max(geometry))),
        "geometry_mean": show(float(np.mean(geometry))),
        "pooled_train_scalar": show(pooled), "forecast_key": forecast_key,
        "band_spectral": show(spectral), "band_schur": show(schur),
        "band_frobenius": show(frobenius), "symmetry_error": show(symmetry),
        "spectral_failure": bool(spectral > SPECTRAL_CAP),
        "schur_failure": bool(schur > SCHUR_CAP),
    }


def build_rows() -> tuple[list[dict[str, Any]], dict[int, float]]:
    rows: list[dict[str, Any]] = []
    pooled: dict[int, float] = {}
    masks = {cutoff: mask_for(cutoff) for cutoff in BAND_CUTOFFS}
    for q0 in Q_ANCHORS:
        packs = []
        for origin in ORIGINS:
            values = np.arange(origin, origin + WINDOW_COUNT, dtype=np.int64)
            packs.append((origin, weighted_components(values, q0)))
        pooled[q0] = float(np.mean([
            float(item[1][2].mean()) for item in packs
            if item[0] in CALIBRATION_ORIGINS]))
        for origin, (primes, matrices, geometry, weights) in packs:
            for cutoff in BAND_CUTOFFS:
                for norm in NORMALIZATIONS:
                    for law in LAWS:
                        rows.append(make_row(
                            origin, q0, law, norm, cutoff, matrices[law],
                            geometry, pooled[q0], primes, weights, masks[cutoff]))
    need(len(rows) == 160, "row census")
    return rows, pooled


def stats(values: list[float]) -> dict[str, Any]:
    need(len(values) >= 2 and all(math.isfinite(x) and x >= 0 for x in values),
         "finite stats")
    minimum, maximum = min(values), max(values)
    mean = sum(values) / len(values)
    relative = (maximum - minimum) / mean if mean else float("inf")
    return {
        "value_count": len(values), "minimum": show(minimum),
        "maximum": show(maximum), "mean": show(mean),
        "relative_spread": show(relative),
        "within_one_percent": bool(relative <= SPREAD_CAP),
        "values": [show(value) for value in values],
    }


def phase_summary(rows: list[dict[str, Any]]) -> dict[str, Any]:
    cells: list[dict[str, Any]] = []
    for cutoff in BAND_CUTOFFS:
        for norm in NORMALIZATIONS:
            for law in LAWS:
                for q0 in Q_ANCHORS:
                    selected = [r for r in rows if
                                r["band_cutoff"] == cutoff and
                                r["normalization"] == norm and
                                r["law"] == law and r["Q"] == q0]
                    selected.sort(key=lambda r: r["origin"])
                    all_values = [float(r["band_spectral"]) for r in selected]
                    cal_values = [float(r["band_spectral"]) for r in selected
                                  if r["origin_role"] == "calibration"]
                    hold_values = [float(r["band_spectral"]) for r in selected
                                   if r["origin_role"] == "holdout"]
                    cells.append({
                        "band_cutoff": cutoff, "normalization": norm,
                        "law": law, "Q": q0,
                        "origins": [r["origin"] for r in selected],
                        "calibration_origins": list(CALIBRATION_ORIGINS),
                        "holdout_origins": list(HOLDOUT_ORIGINS),
                        "all_origin": stats(all_values),
                        "calibration": stats(cal_values),
                        "holdout": stats(hold_values),
                    })
    need(len(cells) == 32, "cell census")
    stable_cal = sum(bool(c["calibration"]["within_one_percent"])
                     for c in cells)
    stable_hold = sum(bool(c["holdout"]["within_one_percent"])
                      for c in cells)
    failure_counts = {
        f"c{cutoff}_{norm}": {
            "spectral": sum(bool(r["spectral_failure"]) for r in rows
                             if r["band_cutoff"] == cutoff and
                             r["normalization"] == norm),
            "schur": sum(bool(r["schur_failure"]) for r in rows
                          if r["band_cutoff"] == cutoff and
                          r["normalization"] == norm),
        }
        for cutoff in BAND_CUTOFFS for norm in NORMALIZATIONS
    }
    forecasts: list[dict[str, Any]] = []
    for cutoff in BAND_CUTOFFS:
        for norm in NORMALIZATIONS:
            key = f"c{cutoff}_{norm}"
            cell = next(c for c in cells if
                        c["band_cutoff"] == cutoff and
                        c["normalization"] == norm and
                        c["law"] == "all_plus" and c["Q"] == 8192)
            hold_mean = float(cell["holdout"]["mean"])
            cal_mean = float(cell["calibration"]["mean"])
            forecast = float(PARENT_PHASE_FORECAST[key])
            error = (hold_mean - forecast) / forecast
            forecasts.append({
                "key": key, "Q": 8192, "law": "all_plus",
                "calibration_mean": show(cal_mean),
                "holdout_mean": show(hold_mean),
                "parent_forecast": show(forecast),
                "holdout_forecast_relative_error": show(error),
                "within_one_percent": bool(abs(error) <= FORECAST_ERROR_CAP),
            })
    return {
        "cells": cells, "cell_count": len(cells), "row_count": len(rows),
        "stable_calibration_cells": stable_cal,
        "stable_holdout_cells": stable_hold,
        "failure_counts_by_cutoff_normalization": failure_counts,
        "forecast_summary": forecasts,
        "forecast_error_cap": show(FORECAST_ERROR_CAP),
        "spread_cap": show(SPREAD_CAP),
        "spectral_cap": show(SPECTRAL_CAP), "schur_cap": show(SCHUR_CAP),
    }


def exact_anchor() -> dict[str, Any]:
    values = list(range(*EXACT_INTERVAL))
    primes = shell(EXACT_Q)
    sign_vectors = signs(primes)
    matrices: dict[str, list[list[Fraction]]] = {law: [] for law in LAWS}
    geometry: list[Fraction] = []
    for u in values:
        row_values = {law: [] for law in LAWS}
        grow = Fraction(0)
        for t in values:
            components: list[Fraction] = []
            for prime in primes:
                if u == t or u % prime == 0 or t % prime == 0:
                    base = Fraction(0)
                else:
                    centered = Fraction(int((u - t) % prime == 0), 1)
                    centered -= Fraction(1, prime - 1)
                    base = (prime * Fraction(prime, EXACT_Q) ** BETA *
                            Fraction(HEIGHT * HEIGHT,
                                     HEIGHT * HEIGHT + (u - t) ** 2) * centered)
                components.append(base)
            grow += sum(value * value for value in components)
            for law in LAWS:
                row_values[law].append(sum(
                    Fraction(int(sign_vectors[law][index])) * value
                    for index, value in enumerate(components)))
        geometry.append(grow)
        for law in LAWS:
            matrices[law].append(row_values[law])
    need(all(value > 0 for value in geometry), "anchor positivity")
    for law in LAWS:
        need(all(matrices[law][i][j] == matrices[law][j][i]
                 for i in range(len(values)) for j in range(len(values))),
             "anchor symmetry")

    def txt(value: Fraction) -> str:
        return f"{value.numerator}/{value.denominator}"

    return {
        "interval": list(EXACT_INTERVAL), "Q": EXACT_Q, "shell": primes,
        "laws": list(LAWS), "band_cutoffs": list(BAND_CUTOFFS),
        "geometry_positive": True,
        "matrix_symmetric_by_law": {law: True for law in LAWS},
        "geometry_digest": hashlib.sha256(canonical(
            [txt(value) for value in geometry])).hexdigest(),
        "law_matrix_digests": {
            law: hashlib.sha256(canonical([
                [txt(value) for value in values] for values in matrix
            ])).hexdigest() for law, matrix in matrices.items()},
    }


def build_payload() -> dict[str, Any]:
    need(PARENT_CODE.is_file() and digest(PARENT_CODE.read_bytes()) ==
         PARENT_CODE_SHA256, "parent code provenance")
    raw_parent = PARENT_CERT.read_bytes()
    need(digest(raw_parent) == PARENT_CERT_SHA256,
         "parent certificate provenance")
    parent_doc = json.loads(raw_parent)
    need(parent_doc.get("payload", {}).get("schema") ==
         "TPC384_C1_BANDWIDTH_NORMALIZATION_PHASE_DIAGRAM_V1",
         "parent schema")
    need(coordinate_disjointness(), "coordinate disjointness")
    rows, pooled = build_rows()
    phase = phase_summary(rows)
    return {
        "schema": SCHEMA, "status": STATUS,
        "parent_lock": {
            "parent_code_sha256": PARENT_CODE_SHA256,
            "parent_certificate_sha256": PARENT_CERT_SHA256,
            "parent_schema": "TPC384_C1_BANDWIDTH_NORMALIZATION_PHASE_DIAGRAM_V1",
            "parent_round2_clue": "TEST_C1_BANDWIDTH_ORIGIN_HOLDOUT",
            "forecast_is_fitted": False,
        },
        "parent_phase_forecast": PARENT_PHASE_FORECAST,
        "selection_protocol": {
            "grid_start": GRID_START, "grid_step": GRID_STEP,
            "grid_count": GRID_COUNT,
            "candidate_origins": [GRID_START + GRID_STEP * i
                                  for i in range(GRID_COUNT)],
            "origin_indices": list(ORIGIN_INDICES),
            "origins": list(ORIGINS),
            "calibration_indices": list(CALIBRATION_INDICES),
            "calibration_origins": list(CALIBRATION_ORIGINS),
            "holdout_indices": list(HOLDOUT_INDICES),
            "holdout_origins": list(HOLDOUT_ORIGINS),
            "window_count": WINDOW_COUNT, "block_length": BLOCK_LENGTH,
            "block_count": BLOCK_COUNT, "band_cutoffs": list(BAND_CUTOFFS),
            "q_anchors": list(Q_ANCHORS), "laws": list(LAWS),
            "normalizations": list(NORMALIZATIONS),
            "spread_cap": show(SPREAD_CAP),
            "forecast_error_cap": show(FORECAST_ERROR_CAP),
            "spectral_cap": show(SPECTRAL_CAP), "schur_cap": show(SCHUR_CAP),
            "response_used_for_selection": False,
            "metric_used_for_selection": False,
            "holdout_role_fixed_before_readout": True,
        },
        "protocol": {
            "origins": list(ORIGINS), "calibration_origins": list(CALIBRATION_ORIGINS),
            "holdout_origins": list(HOLDOUT_ORIGINS),
            "window_count": WINDOW_COUNT, "block_length": BLOCK_LENGTH,
            "block_count": BLOCK_COUNT, "band_cutoffs": list(BAND_CUTOFFS),
            "q_anchors": list(Q_ANCHORS), "kernel_exponents": [EXPONENT],
            "betas": [BETA], "height": HEIGHT, "laws": list(LAWS),
            "normalizations": list(NORMALIZATIONS),
            "source_response_used": False, "origin_selection_used": False,
            "bandwidth_selection_used": False, "law_selection_used": False,
            "normalization_selection_used": False, "row_selection_used": False,
            "pooled_train_scalar_definition":
                "mean of coordinate geometries over calibration origins only at fixed Q",
            "parent_forecast_definition":
                "locked TPC384 all-plus Q=8192 phase mean; no TPC385 response fit",
        },
        "rows": rows,
        "row_digest": hashlib.sha256(canonical(rows)).hexdigest(),
        "pooled_train_scalar_by_Q": {str(q): show(value) for q, value in pooled.items()},
        "phase_summary": phase,
        "finite_audit": {
            "rows": 160, "cell_count": 32, "origin_count": 5,
            "calibration_origin_count": 3, "holdout_origin_count": 2,
            "q_count": 2, "law_count": 4, "bandwidth_count": 2,
            "normalization_count": 2, "complete_cartesian_panel": True,
            "coordinate_disjoint_from_prior": True, "fixed_power_credit": 0,
            "arithmetic_advance": "NO",
        },
        "claim_firewall": CLAIM_FIREWALL,
        "round2_clue": ROUND2_CLUE,
        "exact_anchor": exact_anchor(),
    }


def build_document() -> dict[str, Any]:
    payload = build_payload()
    return {"certificate_version": 1, "claim_status": STATUS,
            "payload_sha256": hashlib.sha256(canonical(payload)).hexdigest(),
            "payload": payload}


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--write", action="store_true")
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()
    if args.write == args.check:
        raise SystemExit("exactly one of --write or --check is required")
    try:
        document = build_document()
        need(finite_tree(document), "non-finite document")
        if args.write:
            RESULT.write_bytes(canonical(document))
            print("TPC385_CERTIFICATE=WRITTEN")
        else:
            stored = json.loads(RESULT.read_bytes())
            need(stored == document, "certificate replay mismatch")
            phase = document["payload"]["phase_summary"]
            forecast = sum(bool(x["within_one_percent"])
                           for x in phase["forecast_summary"])
            print("TPC385_CERTIFICATE=PASS rows=160 cells=32 "
                  f"holdout_forecasts={forecast}/4 "
                  f"stable_holdout={phase['stable_holdout_cells']}/32")
        return 0
    except (CheckFailure, OSError, ValueError, TypeError, KeyError,
            json.JSONDecodeError) as error:
        print("TPC385_CERTIFICATE=FAIL " + str(error), file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
