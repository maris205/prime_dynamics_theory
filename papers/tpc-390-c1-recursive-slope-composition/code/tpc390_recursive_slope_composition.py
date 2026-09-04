#!/usr/bin/env python3
"""TPC-390: a recursive-composition audit for a frozen count slope.

TPC-389 transferred a frozen count slope through the 768 -> 1024 -> 1280
ladder.  This release moves to a fourth coordinate-disjoint family, calibrates
at 1024 and 1280, and tests the next endpoint 1536.  It compares a one-step
parent forecast, a same-family control, and a two-step recursive composition of
the frozen parent slope.  Everything here is a c=1 proxy calculation; no
arithmetic or asymptotic claim is made.
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
RESULT = PROJECT / "results/tpc390_certificate.json"
PARENT_CODE = ROOT / (
    "papers/tpc-389-c1-long-horizon-slope-stress/code/"
    "tpc389_long_horizon_slope_stress.py")
PARENT_CERT = ROOT / (
    "papers/tpc-389-c1-long-horizon-slope-stress/results/"
    "tpc389_certificate.json")
PARENT_CODE_SHA256 = (
    "b914b8a3b4896e40b907e10f5a6dd8c0fef0d2680abf9fd7fa0b43fe890c576b")
PARENT_CERT_SHA256 = (
    "776f98611560907fe3d2822e545875aa32b74d7880872f6e3ee1919ec85e7390")

SCHEMA = "TPC390_C1_RECURSIVE_SLOPE_COMPOSITION_V1"
STATUS = "NUMERICALLY_CERTIFIED_FINITE_C1_RECURSIVE_SLOPE_COMPOSITION_AUDIT"
ROUND2_CLUE = "LOCALIZE_C1_RECURSIVE_HORIZON_OBSTRUCTION"
GRID_START = 3_000_001
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
CALIBRATION_COUNTS = (1024, 1280)
HOLDOUT_COUNT = 1536
COUNT_LEVELS = CALIBRATION_COUNTS + (HOLDOUT_COUNT,)
BLOCK_LENGTH = 128
BAND_MODES = ("fixed_c3", "full_relative")
Q_ANCHORS = (2048, 8192)
EXPONENT = 1
BETA = 2
HEIGHT = 66
LAWS = ("all_plus", "alternating_index", "mod4_character", "half_split")
NORMALIZATIONS = ("local_diagonal", "pooled_train_scalar")
SPREAD_CAP = 0.01
SPECTRAL_CAP = 0.64
SCHUR_CAP = 0.83
TRANSFER_ERROR_CAP = 0.03
EXACT_INTERVAL = (ORIGINS[0], ORIGINS[0] + 13)
EXACT_Q = 8

CLAIM_FIREWALL = {
    "TPC390_SELECTION_PROTOCOL":
        "PROVED_EXACT_FINITE_PREDECLARED_RESPONSE_BLIND",
    "TPC390_COORDINATE_DISJOINTNESS": "PROVED_EXACT_FINITE",
    "TPC390_PARENT_REFERENCE": "PROVED_EXACT_FINITE_HASHED",
    "TPC390_RECURSIVE_PANEL":
        "NUMERICALLY_CERTIFIED_FINITE_256_ROWS",
    "TPC390_PARENT_ONE_STEP_TRANSFER":
        "NUMERICALLY_CERTIFIED_FINITE_SCOPED",
    "TPC390_LOCAL_CONTROL": "NUMERICALLY_CERTIFIED_FINITE_SCOPED",
    "TPC390_RECURSIVE_COMPOSITION":
        "NUMERICALLY_CERTIFIED_FINITE_SCOPED",
    "TPC390_COMPOSITION_IDENTITY":
        "PROVED_EXACT_FINITE_NUMERICAL_IDENTITY",
    "TPC390_ORIGIN_UNIFORMITY": "OPEN",
    "TPC390_COUNT_UNIFORMITY": "OPEN",
    "TPC390_SOURCE_NORMALIZATION_VALIDITY": "MODELING_CHOICE_OPEN",
    "TPC390_GROWING_OPERATOR_BOUND": "OPEN",
    "TPC390_SOURCE_UNIFORM_L2": "OPEN",
    "TPC390_ARITHMETIC_ADVANCE": "NO",
    "TPC390_FIXED_POWER_CREDIT": 0,
    "TPC390_FULL_GATE_B": "OPEN",
    "TPC390_TWIN_PRIME_RESULT": "NONE",
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
    for p in range(2, math.isqrt(limit) + 1):
        if flags[p]:
            flags[p * p:limit + 1:p] = b"\x00" * (
                ((limit - p * p) // p) + 1)
    return [p for p in range(2, limit + 1) if flags[p]]


PRIMES = sieve(20000)


def shell(q0: int) -> list[int]:
    return [p for p in PRIMES if q0 < p <= 2 * q0]


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


def weighted_components(values: np.ndarray, q0: int) -> tuple[Any, ...]:
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
    schur = float(np.max(np.sum(np.abs(matrix), axis=1)))
    eigenvalues = np.linalg.eigvalsh(matrix)
    spectral = max(abs(float(eigenvalues[0])), abs(float(eigenvalues[-1])))
    frobenius = float(np.sqrt(np.sum(matrix * matrix)))
    need(symmetry <= 2e-12 and schur > 0 and frobenius > 0 and
         math.isfinite(spectral) and spectral <= schur + 1e-8 and
         spectral <= frobenius + 1e-8, "metric envelope")
    return spectral, schur, frobenius, symmetry


def mask_for(mode: str, count: int) -> tuple[np.ndarray, int]:
    need(count % BLOCK_LENGTH == 0, "count divisible by block length")
    blocks = count // BLOCK_LENGTH
    cutoff = 3 if mode == "fixed_c3" else blocks - 1
    ids = np.arange(count) // BLOCK_LENGTH
    return np.abs(ids[:, None] - ids[None, :]) <= cutoff, cutoff


def role_for(origin: int, count: int) -> str:
    if origin in CALIBRATION_ORIGINS:
        return f"calibration_{count}"
    return "holdout_1536"


def make_row(origin: int, count: int, q0: int, law: str, norm: str,
             mode: str, matrix: np.ndarray, geometry: np.ndarray,
             denominator: float, denominator_role: str,
             primes: list[int], weights: list[float], mask: np.ndarray,
             effective_cutoff: int) -> dict[str, Any]:
    if norm == "local_diagonal":
        normalized = matrix / np.sqrt(geometry[:, None] * geometry[None, :])
    else:
        normalized = matrix / denominator
    spectral, schur, frobenius, symmetry = metrics(
        np.where(mask, normalized, 0.0))
    return {
        "origin": origin, "origin_role": role_for(origin, count),
        "Q": q0, "law": law, "normalization": norm,
        "band_mode": mode, "effective_cutoff": effective_cutoff,
        "count": count, "interval": [origin, origin + count],
        "block_length": BLOCK_LENGTH, "block_count": count // BLOCK_LENGTH,
        "kernel_exponent": EXPONENT, "beta": BETA, "height": HEIGHT,
        "shell_cardinality": len(primes), "weight_min": show(min(weights)),
        "weight_max": show(max(weights)),
        "geometry_min": show(float(np.min(geometry))),
        "geometry_max": show(float(np.max(geometry))),
        "geometry_mean": show(float(np.mean(geometry))),
        "pooled_scalar_used": show(denominator),
        "pooled_scalar_role": denominator_role,
        "band_spectral": show(spectral), "band_schur": show(schur),
        "band_frobenius": show(frobenius), "symmetry_error": show(symmetry),
        "spectral_failure": bool(spectral > SPECTRAL_CAP),
        "schur_failure": bool(schur > SCHUR_CAP),
    }


def build_rows() -> tuple[list[dict[str, Any]], dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    scalar_info: dict[str, Any] = {}
    for q0 in Q_ANCHORS:
        packs: dict[tuple[int, int], Any] = {}
        for origin in CALIBRATION_ORIGINS:
            for count in CALIBRATION_COUNTS:
                values = np.arange(origin, origin + count, dtype=np.int64)
                packs[origin, count] = weighted_components(values, q0)
        for origin in HOLDOUT_ORIGINS:
            values = np.arange(origin, origin + HOLDOUT_COUNT, dtype=np.int64)
            packs[origin, HOLDOUT_COUNT] = weighted_components(values, q0)
        train_scalars = {
            count: float(np.mean([packs[origin, count][2].mean()
                                  for origin in CALIBRATION_ORIGINS]))
            for count in CALIBRATION_COUNTS
        }
        gamma = math.log(train_scalars[1280] / train_scalars[1024]) / math.log(1280.0 / 1024.0)
        extrapolated = train_scalars[1280] * (1536.0 / 1280.0) ** gamma
        scalar_info[str(q0)] = {
            "by_calibration_count": {str(k): show(v)
                                     for k, v in train_scalars.items()},
            "geometry_log2_slope": show(gamma),
            "extrapolated_1536": show(extrapolated),
        }
        for (origin, count), (primes, matrices, geometry, weights) in packs.items():
            for mode in BAND_MODES:
                mask, cutoff = mask_for(mode, count)
                for norm in NORMALIZATIONS:
                    if norm == "pooled_train_scalar":
                        if count in train_scalars:
                            denominator, denominator_role = train_scalars[count], f"calibration_{count}"
                        else:
                            denominator, denominator_role = extrapolated, "calibration_extrapolated_1536"
                    else:
                        denominator, denominator_role = 1.0, "local_diagonal"
                    for law in LAWS:
                        rows.append(make_row(
                            origin, count, q0, law, norm, mode, matrices[law],
                            geometry, denominator, denominator_role, primes,
                            weights, mask, cutoff))
    need(len(rows) == 256, "row census")
    return rows, scalar_info


def parent_cells() -> dict[tuple[str, str, str, int], dict[str, Any]]:
    raw = PARENT_CERT.read_bytes()
    need(digest(raw) == PARENT_CERT_SHA256, "parent certificate provenance")
    document = json.loads(raw)
    payload = document.get("payload", {})
    need(payload.get("schema") ==
         "TPC389_C1_LONG_HORIZON_SLOPE_STRESS_V1", "parent schema")
    cells = payload.get("transfer_summary", {}).get("cells", [])
    result = {}
    for cell in cells:
        key = (cell["band_mode"], cell["normalization"], cell["law"],
               cell["Q"])
        result[key] = cell
    need(len(result) == 32, "parent cell census")
    return result


def finite_stats(values: list[float]) -> dict[str, Any]:
    need(len(values) in (2, 3) and
         all(math.isfinite(x) and x >= 0 for x in values),
         "finite cell stats")
    minimum, maximum = min(values), max(values)
    mean = sum(values) / len(values)
    relative = (maximum - minimum) / mean if mean else float("inf")
    return {
        "value_count": len(values), "minimum": show(minimum), "maximum": show(maximum),
        "mean": show(mean), "relative_spread": show(relative),
        "within_one_percent": bool(relative <= SPREAD_CAP),
        "values": [show(value) for value in values],
    }


def transfer_summary(rows: list[dict[str, Any]],
                     parents: dict[tuple[str, str, str, int], dict[str, Any]]) -> dict[str, Any]:
    cells: list[dict[str, Any]] = []
    for mode in BAND_MODES:
        for norm in NORMALIZATIONS:
            for law in LAWS:
                for q0 in Q_ANCHORS:
                    selected = [r for r in rows if
                                r["band_mode"] == mode and
                                r["normalization"] == norm and
                                r["law"] == law and r["Q"] == q0]
                    selected.sort(key=lambda r: (r["count"], r["origin"]))
                    by_count = {count: [float(r["band_spectral"]) for r in selected
                                        if r["count"] == count]
                                for count in COUNT_LEVELS}
                    stats = {count: finite_stats(by_count[count])
                             for count in COUNT_LEVELS}
                    means = {count: float(stats[count]["mean"])
                             for count in COUNT_LEVELS}
                    local_alpha = math.log(means[1280] / means[1024]) / math.log(1280.0 / 1024.0)
                    parent_alpha = float(parents[(mode, norm, law, q0)][
                        "parent_horizon_log2_slope"])
                    local_prediction = means[1280] * (1536.0 / 1280.0) ** local_alpha
                    parent_prediction = means[1280] * (1536.0 / 1280.0) ** parent_alpha
                    stage1_parent_prediction = means[1024] * (1280.0 / 1024.0) ** parent_alpha
                    recursive_parent_prediction = stage1_parent_prediction * (
                        1536.0 / 1280.0) ** parent_alpha
                    direct_recursive_prediction = means[1024] * (
                        1536.0 / 1024.0) ** parent_alpha
                    local_ratio = means[1536] / local_prediction
                    parent_ratio = means[1536] / parent_prediction
                    recursive_parent_ratio = means[1536] / recursive_parent_prediction
                    composition_error = (recursive_parent_prediction /
                                         direct_recursive_prediction - 1.0)
                    cells.append({
                        "band_mode": mode, "normalization": norm,
                        "law": law, "Q": q0,
                        "origins": [r["origin"] for r in selected],
                        "calibration_origins": list(CALIBRATION_ORIGINS),
                        "holdout_origins": list(HOLDOUT_ORIGINS),
                        "calibration_counts": [1024, 1280],
                        "holdout_count": 1536,
                        "N1024": stats[1024], "N1280": stats[1280],
                        "N1536_holdout": stats[1536],
                        "parent_horizon_log2_slope": show(parent_alpha),
                        "local_horizon_log2_slope": show(local_alpha),
                        "parent_prediction_N1536_from_N1280": show(parent_prediction),
                        "local_prediction_N1536_from_N1280": show(local_prediction),
                        "parent_stage1_prediction_N1280_from_N1024": show(
                            stage1_parent_prediction),
                        "recursive_parent_prediction_N1536_from_N1024": show(
                            recursive_parent_prediction),
                        "direct_recursive_prediction_N1536_from_N1024": show(
                            direct_recursive_prediction),
                        "recursive_composition_error": show(composition_error),
                        "parent_holdout_to_prediction_ratio": show(parent_ratio),
                        "local_holdout_to_prediction_ratio": show(local_ratio),
                        "recursive_parent_holdout_to_prediction_ratio": show(recursive_parent_ratio),
                        "parent_horizon_error": show(parent_ratio - 1.0),
                        "local_control_error": show(local_ratio - 1.0),
                        "recursive_parent_error": show(recursive_parent_ratio - 1.0),
                        "within_parent_horizon_cap": bool(
                            abs(parent_ratio - 1.0) <= TRANSFER_ERROR_CAP),
                        "within_local_control_cap": bool(
                            abs(local_ratio - 1.0) <= TRANSFER_ERROR_CAP),
                        "within_recursive_parent_cap": bool(
                            abs(recursive_parent_ratio - 1.0) <= TRANSFER_ERROR_CAP),
                    })
    need(len(cells) == 32, "cell census")
    parent_errors = [abs(float(c["parent_horizon_error"])) for c in cells]
    local_errors = [abs(float(c["local_control_error"])) for c in cells]
    recursive_errors = [abs(float(c["recursive_parent_error"])) for c in cells]
    composition_errors = [abs(float(c["recursive_composition_error"]))
                          for c in cells]
    stable = {
        str(count): sum(bool(c[f"N{count}"]["within_one_percent"])
                        for c in cells)
        for count in (1024, 1280)
    }
    stable["1536_holdout"] = sum(
        bool(c["N1536_holdout"]["within_one_percent"]) for c in cells)
    failures = {
        f"{mode}_{norm}": {
            "spectral": sum(bool(r["spectral_failure"]) for r in rows
                             if r["band_mode"] == mode and r["normalization"] == norm),
            "schur": sum(bool(r["schur_failure"]) for r in rows
                          if r["band_mode"] == mode and r["normalization"] == norm),
        }
        for mode in BAND_MODES for norm in NORMALIZATIONS
    }
    return {
        "cells": cells, "cell_count": 32, "row_count": 256,
        "stable_cells": stable,
        "failure_counts_by_mode_normalization": failures,
        "parent_horizon_pass_count": sum(
            bool(c["within_parent_horizon_cap"]) for c in cells),
        "local_control_pass_count": sum(
            bool(c["within_local_control_cap"]) for c in cells),
        "recursive_parent_pass_count": sum(
            bool(c["within_recursive_parent_cap"]) for c in cells),
        "parent_horizon_max_abs_error": show(max(parent_errors)),
        "local_control_max_abs_error": show(max(local_errors)),
        "recursive_parent_max_abs_error": show(max(recursive_errors)),
        "recursive_composition_max_abs_error": show(max(composition_errors)),
        "transfer_error_cap": show(TRANSFER_ERROR_CAP),
        "spread_cap": show(SPREAD_CAP),
        "spectral_cap": show(SPECTRAL_CAP), "schur_cap": show(SCHUR_CAP),
    }


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
        (2000001, 2000001 + 512), (2004011, 2004011 + 512),
        (2008021, 2008021 + 512), (2012031, 2012031 + 512),
        (2016041, 2016041 + 512),
        (2200001, 2200001 + 1024), (2204011, 2204011 + 1024),
        (2208021, 2208021 + 1024), (2212031, 2212031 + 1024),
        (2216041, 2216041 + 1024),
        (2400001, 2400001 + 768), (2404011, 2404011 + 768),
        (2408021, 2408021 + 768), (2412031, 2412031 + 1024),
        (2416041, 2416041 + 1024),
        (2600001, 2600001 + 1024), (2604011, 2604011 + 1024),
        (2608021, 2608021 + 1024), (2612031, 2612031 + 1024),
        (2616041, 2616041 + 1024),
        (2800001, 2800001 + 1024),
        (2804011, 2804011 + 1024),
        (2808021, 2808021 + 1024),
        (2812031, 2812031 + 1280), (2816041, 2816041 + 1280),
    ]
    current = [(o, o + max(CALIBRATION_COUNTS)) for o in CALIBRATION_ORIGINS]
    current += [(o, o + HOLDOUT_COUNT) for o in HOLDOUT_ORIGINS]
    intervals = prior + current
    return all(a[1] <= b[0] or b[1] <= a[0]
               for i, a in enumerate(intervals)
               for b in intervals[i + 1:])


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
        "laws": list(LAWS), "band_modes": list(BAND_MODES),
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
    need(coordinate_disjointness(), "coordinate disjointness")
    rows, scalar_info = build_rows()
    summary = transfer_summary(rows, parent_cells())
    return {
        "schema": SCHEMA, "status": STATUS,
        "parent_lock": {
            "parent_code_sha256": PARENT_CODE_SHA256,
            "parent_certificate_sha256": PARENT_CERT_SHA256,
            "parent_schema": "TPC389_C1_LONG_HORIZON_SLOPE_STRESS_V1",
            "parent_round2_clue": "TEST_C1_RECURSIVE_SLOPE_COMPOSITION",
            "parent_slopes_frozen": True,
            "parent_slopes_refit_on_current_family": False,
        },
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
            "calibration_counts": list(CALIBRATION_COUNTS),
            "holdout_count": HOLDOUT_COUNT,
            "block_length": BLOCK_LENGTH, "band_modes": list(BAND_MODES),
            "q_anchors": list(Q_ANCHORS), "laws": list(LAWS),
            "normalizations": list(NORMALIZATIONS),
            "response_used_for_selection": False,
            "metric_used_for_selection": False,
            "parent_slope_read_before_current_response": True,
            "parent_slope_refit": False,
            "holdout_role_fixed_before_readout": True,
        },
        "protocol": {
            "origins": list(ORIGINS),
            "calibration_origins": list(CALIBRATION_ORIGINS),
            "holdout_origins": list(HOLDOUT_ORIGINS),
            "calibration_counts": list(CALIBRATION_COUNTS),
            "holdout_count": HOLDOUT_COUNT,
            "block_length": BLOCK_LENGTH, "band_modes": list(BAND_MODES),
            "q_anchors": list(Q_ANCHORS), "kernel_exponents": [EXPONENT],
            "betas": [BETA], "height": HEIGHT, "laws": list(LAWS),
            "normalizations": list(NORMALIZATIONS),
            "source_response_used": False, "origin_selection_used": False,
            "count_selection_used": False, "bandwidth_selection_used": False,
            "law_selection_used": False, "normalization_selection_used": False,
            "row_selection_used": False,
            "pooled_scalar_definition":
                "current-family calibration-origin mean geometry",
            "parent_transfer_definition":
                "current-family N=1280 mean times (6/5) to parent TPC389 slope",
            "local_control_definition":
                "current-family N=1280 mean times (6/5) to current-family 1024 -> 1280 slope",
            "recursive_parent_definition":
                "current-family N=1024 mean, first forecast to N=1280 and then to N=1536, using parent TPC389 slope",
            "direct_recursive_definition":
                "same parent slope applied once from N=1024 to N=1536 as a composition identity control",
            "transfer_cap_definition": "absolute ratio error <= 0.03",
        },
        "rows": rows,
        "row_digest": hashlib.sha256(canonical(rows)).hexdigest(),
        "geometry_scalar_summary": scalar_info,
        "transfer_summary": summary,
        "finite_audit": {
            "rows": 256, "cell_count": 32, "origin_count": 5,
            "calibration_origin_count": 3, "holdout_origin_count": 2,
            "calibration_count_levels": 2, "holdout_count_levels": 1,
            "calibration_counts": [1024, 1280], "holdout_count": 1536,
            "band_mode_count": 2, "q_count": 2, "law_count": 4,
            "normalization_count": 2, "complete_cartesian_panel": True,
            "coordinate_disjoint_from_prior": True,
            "parent_slope_frozen": True, "fixed_power_credit": 0,
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
            print("TPC390_CERTIFICATE=WRITTEN")
        else:
            stored = json.loads(RESULT.read_bytes())
            need(stored == document, "certificate replay mismatch")
            summary = document["payload"]["transfer_summary"]
            failures = summary["failure_counts_by_mode_normalization"]
            print("TPC390_CERTIFICATE=PASS rows=256 cells=32 "
                  f"parent_pass={summary['parent_horizon_pass_count']}/32 "
                  f"local_pass={summary['local_control_pass_count']}/32 "
                  f"recursive_parent_pass={summary['recursive_parent_pass_count']}/32 "
                  f"spectral_failures={sum(v['spectral'] for v in failures.values())} "
                  f"stable_holdout={summary['stable_cells']['1536_holdout']}/32 "
                  f"composition_max={summary['recursive_composition_max_abs_error']}")
        return 0
    except (CheckFailure, OSError, ValueError, TypeError, KeyError,
            json.JSONDecodeError) as error:
        print("TPC390_CERTIFICATE=FAIL " + str(error), file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
