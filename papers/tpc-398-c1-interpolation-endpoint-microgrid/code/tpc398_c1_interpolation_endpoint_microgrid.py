#!/usr/bin/env python3
"""TPC-398: a finite endpoint microgrid on a fresh c=1 family.

TPC-397 replicated a finite transition panel and left the segment from
``lambda=3/4`` to ``lambda=1`` unresolved.  TPC-398 tests a finer grid inside
that segment on a new coordinate-disjoint family.  The current matrices are
exact linear combinations of the two endpoint matrices; the parent comparison
is a frozen, response-blind interpolation of TPC-397's two endpoint means.
Nothing here is an arithmetic sign law or an asymptotic operator statement.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import math
import os
from fractions import Fraction
from pathlib import Path
from typing import Any

os.environ.setdefault("OMP_NUM_THREADS", "1")
os.environ.setdefault("OPENBLAS_NUM_THREADS", "1")
os.environ.setdefault("MKL_NUM_THREADS", "1")
import numpy as np

PROJECT = Path(__file__).resolve().parents[1]
ROOT = PROJECT.parents[1]
RESULT = PROJECT / "results/tpc398_certificate.json"
PARENT_CODE = ROOT / (
    "papers/tpc-397-c1-interpolation-transition-replication/code/"
    "tpc397_c1_interpolation_transition_replication.py")
PARENT_CERT = ROOT / (
    "papers/tpc-397-c1-interpolation-transition-replication/results/"
    "tpc397_certificate.json")
PARENT_CODE_SHA256 = (
    "1a395050d130398161afba90e741e54ecbcd93eed0169018db8084aac91504b9")
PARENT_CERT_SHA256 = (
    "3d7a8241df38ffd3f4e527dd02f29d6e1653ed0d53a5a693dcd9c2a120e13fc2")

SCHEMA = "TPC398_C1_INTERPOLATION_ENDPOINT_MICROGRID_V1"
STATUS = "NUMERICALLY_CERTIFIED_FINITE_C1_INTERPOLATION_ENDPOINT_MICROGRID_AUDIT"
ROUND2_CLUE = "TEST_C1_ENDPOINT_MICROGRID_CROSS_FAMILY_REPLICATION"

GRID_START = 6_800_001
GRID_STEP = 401
GRID_COUNT = 41
ORIGIN_INDICES = (0, 8, 16, 24, 32, 40)
CALIBRATION_INDICES = (0, 8, 16)
HOLDOUT_INDICES = (24, 32, 40)
ORIGINS = tuple(GRID_START + GRID_STEP * i for i in ORIGIN_INDICES)
CALIBRATION_ORIGINS = tuple(
    GRID_START + GRID_STEP * i for i in CALIBRATION_INDICES)
HOLDOUT_ORIGINS = tuple(
    GRID_START + GRID_STEP * i for i in HOLDOUT_INDICES)
WINDOW_COUNT = 1024
BLOCK_LENGTH = 128
BAND_MODES = ("fixed_c3",)
Q_ANCHORS = (8192,)
EXPONENT = 1
BETA = 2
HEIGHT = 66
LAWS = ("blend_7_8", "blend_15_16", "blend_31_32", "blend_1")
LAMBDA_FRACTIONS = {
    "blend_7_8": Fraction(7, 8),
    "blend_15_16": Fraction(15, 16),
    "blend_31_32": Fraction(31, 32),
    "blend_1": Fraction(1, 1),
}
SEGMENT_START = Fraction(3, 4)
SEGMENT_END = Fraction(1, 1)
NORMALIZATIONS = (
    "local_diagonal", "pooled_train_scalar", "origin_scalar",
    "frozen_train_1024_scalar")
ORIGIN_SPREAD_CAP = 0.01
CROSS_FAMILY_CAP = 0.03
WITHIN_FAMILY_TRANSFER_CAP = 0.03
SPECTRAL_CAP = 0.64
SCHUR_CAP = 0.83
EXACT_INTERVAL = (ORIGINS[0], ORIGINS[0] + 13)
EXACT_Q = 8
CELL_COUNT = 16
ROW_COUNT = len(ORIGINS) * len(Q_ANCHORS) * len(LAWS) * len(NORMALIZATIONS)

CLAIM_FIREWALL = {
    "TPC398_SELECTION_PROTOCOL":
        "PROVED_EXACT_FINITE_PREDECLARED_RESPONSE_BLIND",
    "TPC398_COORDINATE_DISJOINTNESS": "PROVED_EXACT_FINITE",
    "TPC398_PARENT_REFERENCE": "PROVED_EXACT_FINITE_HASHED",
    "TPC398_INTERPOLATION_IDENTITY":
        "PROVED_EXACT_FINITE_LINEAR_MATRIX_IDENTITY",
    "TPC398_INTERPOLATION_PANEL":
        "NUMERICALLY_CERTIFIED_FINITE_96_ROWS",
    "TPC398_ORIGIN_PHASE":
        "NUMERICALLY_CERTIFIED_FINITE_SCOPED",
    "TPC398_PARENT_INTERPOLATED_TRANSFER":
        "NUMERICALLY_CERTIFIED_FINITE_SCOPED",
    "TPC398_SPECTRAL_ENVELOPE":
        "NUMERICALLY_CERTIFIED_FINITE_SCOPED_ONLY",
    "TPC398_SCHUR_ENVELOPE":
        "NUMERICALLY_CERTIFIED_FINITE_SCOPED_ONLY",
    "TPC398_SOURCE_NORMALIZATION_VALIDITY": "MODELING_CHOICE_OPEN",
    "TPC398_GROWING_OPERATOR_BOUND": "OPEN",
    "TPC398_SOURCE_UNIFORM_L2": "OPEN",
    "TPC398_ARITHMETIC_ADVANCE": "NO",
    "TPC398_FIXED_POWER_CREDIT": 0,
    "TPC398_FULL_GATE_B": "OPEN",
    "TPC398_TWIN_PRIME_RESULT": "NONE",
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
    return {
        "all_plus": np.ones(len(primes), dtype=np.float64),
        "alternating_index": np.asarray(
            [1.0 if i % 2 == 0 else -1.0
             for i in range(len(primes))], dtype=np.float64),
    }


def weighted_components(values: np.ndarray, q0: int) -> tuple[Any, ...]:
    difference = values[:, None] - values[None, :]
    distance = difference.astype(np.float64)
    kernel = (float(HEIGHT) ** (2 * EXPONENT) /
              (HEIGHT * HEIGHT + distance * distance) ** EXPONENT)
    np.fill_diagonal(kernel, 0.0)
    primes = shell(q0)
    sign_vectors = signs(primes)
    endpoints = {
        "all_plus": np.zeros((len(values), len(values)), dtype=np.float64),
        "alternating_index": np.zeros((len(values), len(values)),
                                       dtype=np.float64),
    }
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
        for law in endpoints:
            endpoints[law] += sign_vectors[law][index] * block
    for law in endpoints:
        endpoints[law][:] = (endpoints[law] + endpoints[law].T) / 2.0
    matrices: dict[str, np.ndarray] = {}
    interpolation_residuals: dict[str, float] = {}
    for law in LAWS:
        lam = float(LAMBDA_FRACTIONS[law])
        matrices[law] = ((1.0 - lam) * endpoints["all_plus"] +
                         lam * endpoints["alternating_index"])
        interpolation_residuals[law] = float(np.max(np.abs(
            matrices[law] - ((1.0 - lam) * endpoints["all_plus"] +
                             lam * endpoints["alternating_index"]))))
    need(bool(np.all(np.isfinite(geometry) & (geometry > 0))),
         "geometry positivity")
    return primes, matrices, geometry, weights, interpolation_residuals


def metrics(matrix: np.ndarray) -> tuple[float, float, float, float]:
    symmetry = float(np.max(np.abs(matrix - matrix.T)))
    schur = float(np.max(np.sum(np.abs(matrix), axis=1)))
    eigenvalues = np.linalg.eigvalsh(matrix)
    spectral = max(abs(float(eigenvalues[0])), abs(float(eigenvalues[-1])))
    frobenius = float(np.sqrt(np.sum(matrix * matrix)))
    need(symmetry <= 2e-12 and schur > 0 and frobenius > 0 and
         math.isfinite(spectral) and spectral <= schur + 1e-8 and
         spectral <= frobenius + 1e-8, "finite metric envelope")
    return spectral, schur, frobenius, symmetry


def make_row(origin: int, law: str, norm: str, matrix: np.ndarray,
             geometry: np.ndarray, denominator: float, scalar_role: str,
             primes: list[int], weights: list[float], mask: np.ndarray,
             base: tuple[float, float, float, float],
             interpolation_residual: float) -> dict[str, Any]:
    coefficient = LAMBDA_FRACTIONS[law]
    if norm == "local_diagonal":
        normalized = matrix / np.sqrt(geometry[:, None] * geometry[None, :])
        spectral, schur, frobenius, symmetry = metrics(
            np.where(mask, normalized, 0.0))
    else:
        spectral, schur, frobenius, symmetry = tuple(
            value / denominator for value in base)
    return {
        "origin": origin,
        "origin_role": ("calibration_1024" if origin in CALIBRATION_ORIGINS
                         else "holdout_1024"),
        "Q": Q_ANCHORS[0], "law": law, "normalization": norm,
        "interpolation_lambda":
            f"{coefficient.numerator}/{coefficient.denominator}",
        "interpolation_lambda_numerator": coefficient.numerator,
        "interpolation_lambda_denominator": coefficient.denominator,
        "interpolation_residual": show(interpolation_residual),
        "band_mode": "fixed_c3", "effective_cutoff": 3,
        "count": WINDOW_COUNT, "interval": [origin, origin + WINDOW_COUNT],
        "block_length": BLOCK_LENGTH, "block_count": 8,
        "kernel_exponent": EXPONENT, "beta": BETA, "height": HEIGHT,
        "shell_cardinality": len(primes), "weight_min": show(min(weights)),
        "weight_max": show(max(weights)),
        "geometry_min": show(float(np.min(geometry))),
        "geometry_max": show(float(np.max(geometry))),
        "geometry_mean": show(float(np.mean(geometry))),
        "pooled_scalar_used": show(denominator),
        "pooled_scalar_role": scalar_role,
        "band_spectral": show(spectral), "band_schur": show(schur),
        "band_frobenius": show(frobenius), "symmetry_error": show(symmetry),
        "spectral_failure": bool(spectral > SPECTRAL_CAP),
        "schur_failure": bool(schur > SCHUR_CAP),
    }


def load_parent_endpoints() -> dict[tuple[str, str, int], float]:
    need(PARENT_CODE.is_file() and
         digest(PARENT_CODE.read_bytes()) == PARENT_CODE_SHA256,
         "parent code provenance")
    raw = PARENT_CERT.read_bytes()
    need(digest(raw) == PARENT_CERT_SHA256, "parent certificate provenance")
    document = json.loads(raw)
    need(raw == canonical(document), "parent certificate canonicality")
    payload = document.get("payload", {})
    need(payload.get("schema") ==
         "TPC397_C1_SIGNED_LAW_INTERPOLATION_V1" and
         payload.get("status") ==
         "NUMERICALLY_CERTIFIED_FINITE_C1_INTERPOLATION_TRANSITION_REPLICATION_AUDIT",
         "parent header")
    cells = payload.get("origin_summary", {}).get("cells", [])
    baseline: dict[tuple[str, str, int], float] = {}
    for cell in cells:
        current_law = cell.get("law")
        if current_law not in ("blend_3_4", "blend_1"):
            continue
        endpoint = ("segment_start" if current_law == "blend_3_4"
                    else "segment_end")
        key = (cell.get("normalization"), endpoint, cell.get("Q"))
        need(key not in baseline, "duplicate parent endpoint")
        baseline[key] = float(cell["all_origin_stats"]["mean"])
    need(set(baseline) == {
        (norm, law, Q_ANCHORS[0])
        for norm in NORMALIZATIONS
        for law in ("segment_start", "segment_end")},
         "parent baseline census")
    return baseline


def load_parent_baseline() -> dict[tuple[str, str, int], float]:
    endpoints = load_parent_endpoints()
    baseline: dict[tuple[str, str, int], float] = {}
    for norm in NORMALIZATIONS:
        start = endpoints[norm, "segment_start", Q_ANCHORS[0]]
        end = endpoints[norm, "segment_end", Q_ANCHORS[0]]
        for law in LAWS:
            lam = LAMBDA_FRACTIONS[law]
            segment_coordinate = ((lam - SEGMENT_START) /
                                  (SEGMENT_END - SEGMENT_START))
            baseline[norm, law, Q_ANCHORS[0]] = (
                float((1 - segment_coordinate) * Fraction(str(start)) +
                      segment_coordinate * Fraction(str(end))))
    return baseline


def build_rows() -> tuple[list[dict[str, Any]], dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    scalar_info: dict[str, Any] = {}
    for q0 in Q_ANCHORS:
        packs: dict[int, Any] = {}
        for origin in ORIGINS:
            values = np.arange(origin, origin + WINDOW_COUNT, dtype=np.int64)
            packs[origin] = weighted_components(values, q0)
        pooled = float(np.mean([packs[o][2].mean() for o in CALIBRATION_ORIGINS]))
        frozen = float(packs[CALIBRATION_ORIGINS[0]][2].mean())
        scalar_info[str(q0)] = {
            "calibration_geometry_means": {
                str(o): show(float(packs[o][2].mean()))
                for o in CALIBRATION_ORIGINS},
            "pooled_calibration_scalar": show(pooled),
            "frozen_first_calibration_scalar": show(frozen),
        }
        for origin in ORIGINS:
            primes, matrices, geometry, weights, residuals = packs[origin]
            block_ids = np.arange(WINDOW_COUNT) // BLOCK_LENGTH
            mask = np.abs(block_ids[:, None] - block_ids[None, :]) <= 3
            base_metrics = {
                law: metrics(np.where(mask, matrices[law], 0.0))
                for law in LAWS}
            for norm in NORMALIZATIONS:
                if norm == "local_diagonal":
                    denominator, scalar_role = 1.0, "local_diagonal"
                elif norm == "pooled_train_scalar":
                    denominator, scalar_role = pooled, "calibration_origin_mean"
                elif norm == "origin_scalar":
                    denominator, scalar_role = float(geometry.mean()), \
                        f"origin_{origin}_1024"
                elif norm == "frozen_train_1024_scalar":
                    denominator, scalar_role = frozen, \
                        "first_calibration_origin_1024_frozen"
                else:
                    raise CheckFailure("unknown normalization")
                for law in LAWS:
                    rows.append(make_row(
                        origin, law, norm, matrices[law], geometry, denominator,
                        scalar_role, primes, weights, mask, base_metrics[law],
                        residuals[law]))
    need(len(rows) == ROW_COUNT, "row census")
    return rows, scalar_info


def finite_stats(values: list[float]) -> dict[str, Any]:
    need(len(values) > 0 and all(math.isfinite(x) and x >= 0 for x in values),
         "finite stats")
    minimum, maximum = min(values), max(values)
    mean = sum(values) / len(values)
    relative = (maximum - minimum) / mean if mean else float("inf")
    return {
        "value_count": len(values), "minimum": show(minimum),
        "maximum": show(maximum), "mean": show(mean),
        "absolute_spread": show(maximum - minimum),
        "relative_spread": show(relative),
        "within_one_percent": bool(relative <= ORIGIN_SPREAD_CAP),
        "values": [show(value) for value in values],
    }


def origin_summary(rows: list[dict[str, Any]],
                   baseline: dict[tuple[str, str, int], float],
                   parent_endpoints: dict[tuple[str, str, int], float]
                   ) -> dict[str, Any]:
    definitions = {
        "local_diagonal": "entrywise division by sqrt(G(u)G(v))",
        "pooled_train_scalar": "mean geometry over three calibration origins",
        "origin_scalar": "current-origin mean geometry",
        "frozen_train_1024_scalar":
            "first calibration-origin mean geometry, frozen across origins",
    }
    cells: list[dict[str, Any]] = []
    for norm in NORMALIZATIONS:
        for law in LAWS:
            for q0 in Q_ANCHORS:
                selected = [r for r in rows if r["normalization"] == norm and
                            r["law"] == law and r["Q"] == q0]
                selected.sort(key=lambda r: r["origin"])
                values = [float(r["band_spectral"]) for r in selected]
                calibration = [float(r["band_spectral"]) for r in selected[:3]]
                holdout = [float(r["band_spectral"]) for r in selected[3:]]
                all_stats = finite_stats(values)
                calibration_stats = finite_stats(calibration)
                holdout_stats = finite_stats(holdout)
                cal_mean = float(calibration_stats["mean"])
                hold_mean = float(holdout_stats["mean"])
                parent_mean = baseline[norm, law, q0]
                coefficient = LAMBDA_FRACTIONS[law]
                parent_start = parent_endpoints[norm, "segment_start", q0]
                parent_end = parent_endpoints[norm, "segment_end", q0]
                segment_coordinate = ((coefficient - SEGMENT_START) /
                                      (SEGMENT_END - SEGMENT_START))
                cal_error = cal_mean / parent_mean - 1.0
                hold_error = hold_mean / parent_mean - 1.0
                within_transfer = hold_mean / cal_mean - 1.0
                cells.append({
                    "band_mode": "fixed_c3", "normalization": norm,
                    "normalization_definition": definitions[norm],
                    "law": law, "Q": q0,
                    "origins": [r["origin"] for r in selected],
                    "calibration_origins": list(CALIBRATION_ORIGINS),
                    "holdout_origins": list(HOLDOUT_ORIGINS),
                    "count": WINDOW_COUNT,
                    "parent_family": "TPC397",
                    "parent_interpolation_definition":
                        "(1-t)*TPC397 blend_3_4 + t*TPC397 blend_1, "
                        "t=(lambda-3/4)/(1/4)",
                    "interpolation_lambda":
                        f"{coefficient.numerator}/{coefficient.denominator}",
                    "parent_segment_endpoint_means": {
                        "blend_3_4": show(parent_start),
                        "blend_1": show(parent_end),
                    },
                    "parent_segment_coordinate":
                        f"{segment_coordinate.numerator}/"
                        f"{segment_coordinate.denominator}",
                    "parent_family_mean": show(parent_mean),
                    "all_origin_stats": all_stats,
                    "calibration_stats": calibration_stats,
                    "holdout_stats": holdout_stats,
                    "calibration_cross_family_error": show(cal_error),
                    "holdout_cross_family_error": show(hold_error),
                    "within_family_holdout_transfer_error": show(within_transfer),
                    "within_cross_family_calibration_cap": bool(
                        abs(cal_error) <= CROSS_FAMILY_CAP),
                    "within_cross_family_holdout_cap": bool(
                        abs(hold_error) <= CROSS_FAMILY_CAP),
                    "within_family_holdout_transfer_cap": bool(
                        abs(within_transfer) <= WITHIN_FAMILY_TRANSFER_CAP),
                    "spectral_failures": sum(bool(r["spectral_failure"])
                                              for r in selected),
                    "schur_failures": sum(bool(r["schur_failure"])
                                           for r in selected),
                })
    need(len(cells) == CELL_COUNT, "summary cell census")
    origin_passes = {
        norm: sum(bool(c["all_origin_stats"]["within_one_percent"])
                  for c in cells if c["normalization"] == norm)
        for norm in NORMALIZATIONS}
    cal_passes = {
        norm: sum(bool(c["within_cross_family_calibration_cap"])
                  for c in cells if c["normalization"] == norm)
        for norm in NORMALIZATIONS}
    hold_passes = {
        norm: sum(bool(c["within_cross_family_holdout_cap"])
                  for c in cells if c["normalization"] == norm)
        for norm in NORMALIZATIONS}
    within_passes = {
        norm: sum(bool(c["within_family_holdout_transfer_cap"])
                  for c in cells if c["normalization"] == norm)
        for norm in NORMALIZATIONS}
    max_spread = {
        norm: show(max(float(c["all_origin_stats"]["relative_spread"])
                      for c in cells if c["normalization"] == norm))
        for norm in NORMALIZATIONS}
    max_cal = {
        norm: show(max(abs(float(c["calibration_cross_family_error"]))
                      for c in cells if c["normalization"] == norm))
        for norm in NORMALIZATIONS}
    max_hold = {
        norm: show(max(abs(float(c["holdout_cross_family_error"]))
                      for c in cells if c["normalization"] == norm))
        for norm in NORMALIZATIONS}
    max_within = {
        norm: show(max(abs(float(c["within_family_holdout_transfer_error"]))
                      for c in cells if c["normalization"] == norm))
        for norm in NORMALIZATIONS}
    spectral = {norm: sum(c["spectral_failures"] for c in cells
                          if c["normalization"] == norm)
                for norm in NORMALIZATIONS}
    schur = {norm: sum(c["schur_failures"] for c in cells
                       if c["normalization"] == norm)
             for norm in NORMALIZATIONS}
    return {
        "cells": cells, "cell_count": CELL_COUNT, "row_count": ROW_COUNT,
        "normalizations": list(NORMALIZATIONS), "laws": list(LAWS),
        "origin_count": len(ORIGINS), "calibration_origin_count": 3,
        "holdout_origin_count": 3, "parent_family": "TPC397",
        "parent_interpolation":
            "linear interpolation of frozen TPC397 blend_3_4 and blend_1 "
            "means on the segment lambda in [3/4,1]",
        "origin_spread_cap": show(ORIGIN_SPREAD_CAP),
        "cross_family_cap": show(CROSS_FAMILY_CAP),
        "within_family_transfer_cap": show(WITHIN_FAMILY_TRANSFER_CAP),
        "spectral_cap": show(SPECTRAL_CAP), "schur_cap": show(SCHUR_CAP),
        "within_family_origin_pass_counts": origin_passes,
        "cross_family_calibration_pass_counts": cal_passes,
        "cross_family_holdout_pass_counts": hold_passes,
        "within_family_transfer_pass_counts": within_passes,
        "maximum_within_family_origin_relative_spread": max_spread,
        "maximum_cross_family_calibration_abs_error": max_cal,
        "maximum_cross_family_holdout_abs_error": max_hold,
        "maximum_within_family_transfer_abs_error": max_within,
        "spectral_failures_by_normalization": spectral,
        "schur_failures_by_normalization": schur,
        "origin_stable_cells": sum(origin_passes.values()),
        "cross_family_calibration_stable_cells": sum(cal_passes.values()),
        "cross_family_holdout_stable_cells": sum(hold_passes.values()),
        "within_family_transfer_stable_cells": sum(within_passes.values()),
    }


def prior_intervals() -> list[tuple[int, int]]:
    return [
        (6400001, 6400001 + 1024), (6403209, 6403209 + 1024),
        (6406417, 6406417 + 1024), (6409625, 6409625 + 1024),
        (6412833, 6412833 + 1024), (6416041, 6416041 + 1024),
        (6000001, 6000001 + 1024), (6003209, 6003209 + 1024),
        (6006417, 6006417 + 1024), (6009625, 6009625 + 1024),
        (6012833, 6012833 + 1024), (6016041, 6016041 + 1024),
        (5600001, 5600001 + 1024), (5603209, 5603209 + 1024),
        (5606417, 5606417 + 1024), (5609625, 5609625 + 1024),
        (5612833, 5612833 + 1024), (5616041, 5616041 + 1024),
        (5000001, 5000001 + 1024), (5002006, 5002006 + 1024),
        (5004011, 5004011 + 1024), (5006016, 5006016 + 1024),
        (5008021, 5008021 + 1024), (5010026, 5010026 + 1024),
        (5012031, 5012031 + 1024), (5014036, 5014036 + 1024),
        (4200001, 4200001 + 1024), (4204011, 4204011 + 1280),
        (4208021, 4208021 + 1280), (4212031, 4212031 + 1536),
        (4216041, 4216041 + 1536),
        (3800001, 3800001 + 1024), (3804011, 3804011 + 1024),
        (3808021, 3808021 + 1024), (3812031, 3812031 + 1536),
        (3816041, 3816041 + 1536),
    ]


def coordinate_disjointness() -> bool:
    current = [(origin, origin + WINDOW_COUNT) for origin in ORIGINS]
    intervals = prior_intervals() + current
    return all(a[1] <= b[0] or b[1] <= a[0]
               for i, a in enumerate(intervals)
               for b in intervals[i + 1:])


def exact_anchor() -> dict[str, Any]:
    values = list(range(*EXACT_INTERVAL))
    primes = shell(EXACT_Q)
    endpoint_matrices: dict[str, list[list[Fraction]]] = {
        law: [] for law in ("all_plus", "alternating_index")}
    geometry: list[Fraction] = []
    for u in values:
        row_values = {law: [] for law in endpoint_matrices}
        grow = Fraction(0)
        for v in values:
            components: list[Fraction] = []
            for prime in primes:
                if u == v or u % prime == 0 or v % prime == 0:
                    base = Fraction(0)
                else:
                    centered = Fraction(int((u - v) % prime == 0), 1)
                    centered -= Fraction(1, prime - 1)
                    base = (prime * Fraction(prime, EXACT_Q) ** BETA *
                            Fraction(HEIGHT * HEIGHT,
                                     HEIGHT * HEIGHT + (u - v) ** 2) * centered)
                components.append(base)
            grow += sum(value * value for value in components)
            row_values["all_plus"].append(sum(components))
            row_values["alternating_index"].append(sum(
                Fraction(1 if index % 2 == 0 else -1, 1) * value
                for index, value in enumerate(components)))
        geometry.append(grow)
        for law in endpoint_matrices:
            endpoint_matrices[law].append(row_values[law])
    need(all(value > 0 for value in geometry), "anchor positivity")
    for law in endpoint_matrices:
        need(all(endpoint_matrices[law][i][j] ==
                 endpoint_matrices[law][j][i]
                 for i in range(len(values)) for j in range(len(values))),
             "anchor symmetry")

    matrices: dict[str, list[list[Fraction]]] = {}
    interpolation_identity = {}
    for law in LAWS:
        lam = LAMBDA_FRACTIONS[law]
        matrices[law] = [
            [(1 - lam) * endpoint_matrices["all_plus"][i][j] +
             lam * endpoint_matrices["alternating_index"][i][j]
             for j in range(len(values))]
            for i in range(len(values))]
        interpolation_identity[law] = all(
            matrices[law][i][j] ==
            ((1 - lam) * endpoint_matrices["all_plus"][i][j] +
             lam * endpoint_matrices["alternating_index"][i][j])
            for i in range(len(values)) for j in range(len(values)))
        need(interpolation_identity[law], "anchor interpolation identity")

    def txt(value: Fraction) -> str:
        return f"{value.numerator}/{value.denominator}"

    return {
        "interval": list(EXACT_INTERVAL), "Q": EXACT_Q, "shell": primes,
        "laws": list(LAWS), "band_modes": list(BAND_MODES),
        "interpolation_coefficients": {
            law: [LAMBDA_FRACTIONS[law].numerator,
                  LAMBDA_FRACTIONS[law].denominator] for law in LAWS},
        "geometry_positive": True,
        "matrix_symmetric_by_law": {law: True for law in LAWS},
        "interpolation_identity_exact": interpolation_identity,
        "geometry_digest": hashlib.sha256(canonical(
            [txt(value) for value in geometry])).hexdigest(),
        "endpoint_law_matrix_digests": {
            law: hashlib.sha256(canonical([
                [txt(value) for value in values] for values in matrix
            ])).hexdigest() for law, matrix in endpoint_matrices.items()},
        "law_matrix_digests": {
            law: hashlib.sha256(canonical([
                [txt(value) for value in values] for values in matrix
            ])).hexdigest() for law, matrix in matrices.items()},
    }


def build_payload() -> dict[str, Any]:
    parent_endpoints = load_parent_endpoints()
    parent = load_parent_baseline()
    need(coordinate_disjointness(), "coordinate disjointness")
    rows, scalar_info = build_rows()
    summary = origin_summary(rows, parent, parent_endpoints)
    return {
        "schema": SCHEMA, "status": STATUS,
        "parent_lock": {
            "parent_code_sha256": PARENT_CODE_SHA256,
            "parent_certificate_sha256": PARENT_CERT_SHA256,
            "parent_schema": "TPC397_C1_SIGNED_LAW_INTERPOLATION_V1",
            "parent_status":
                "NUMERICALLY_CERTIFIED_FINITE_C1_INTERPOLATION_TRANSITION_REPLICATION_AUDIT",
            "parent_interface_frozen": True,
            "parent_interface_used_for_current_fit": False,
            "parent_means_used_as_response_blind_baseline": True,
            "parent_endpoint_laws": ["blend_3_4", "blend_1"],
            "parent_segment": "lambda in [3/4,1]",
            "parent_interpolation_is_modeling_choice": True,
        },
        "selection_protocol": {
            "grid_start": GRID_START, "grid_step": GRID_STEP,
            "grid_count": GRID_COUNT,
            "candidate_origins": [GRID_START + GRID_STEP * i
                                  for i in range(GRID_COUNT)],
            "origin_indices": list(ORIGIN_INDICES), "origins": list(ORIGINS),
            "calibration_indices": list(CALIBRATION_INDICES),
            "calibration_origins": list(CALIBRATION_ORIGINS),
            "holdout_indices": list(HOLDOUT_INDICES),
            "holdout_origins": list(HOLDOUT_ORIGINS),
            "window_count": WINDOW_COUNT, "block_length": BLOCK_LENGTH,
            "band_modes": list(BAND_MODES), "q_anchors": list(Q_ANCHORS),
            "laws": list(LAWS), "normalizations": list(NORMALIZATIONS),
            "origin_spread_cap": show(ORIGIN_SPREAD_CAP),
            "cross_family_cap": show(CROSS_FAMILY_CAP),
            "within_family_transfer_cap": show(WITHIN_FAMILY_TRANSFER_CAP),
            "response_used_for_selection": False,
            "metric_used_for_selection": False,
            "parent_means_frozen_before_current_readout": True,
            "holdout_role_fixed_before_readout": True,
            "parent_interface_used_for_current_fit": False,
            "interpolation_coefficients": {
                law: [LAMBDA_FRACTIONS[law].numerator,
                      LAMBDA_FRACTIONS[law].denominator] for law in LAWS},
            "intermediate_laws_are_modeling_probes": True,
        },
        "protocol": {
            "origins": list(ORIGINS), "calibration_origins": list(CALIBRATION_ORIGINS),
            "holdout_origins": list(HOLDOUT_ORIGINS), "window_count": WINDOW_COUNT,
            "block_length": BLOCK_LENGTH, "band_modes": list(BAND_MODES),
            "q_anchors": list(Q_ANCHORS), "kernel_exponents": [EXPONENT],
            "betas": [BETA], "height": HEIGHT, "laws": list(LAWS),
            "normalizations": list(NORMALIZATIONS),
            "metric": "fixed-c3 band spectral diagnostic",
            "origin_spread_definition": "(max-min)/mean over locked origins",
            "cross_family_definition":
                "new-family cohort mean / linearly interpolated TPC397 segment endpoint mean - 1",
            "within_family_transfer_definition":
                "new holdout mean / new calibration mean - 1",
            "source_response_used": False, "origin_selection_used": False,
            "parent_response_used_for_selection": False,
            "law_selection_used": False, "normalization_selection_used": False,
            "row_selection_used": False,
            "interpolation_definition":
                "M_lambda=(1-lambda)M_all_plus+lambda M_alternating_index",
            "parent_segment_coordinate_definition":
                "t=(lambda-3/4)/(1/4), with TPC397 blend_3_4 and blend_1 means",
            "interpolation_is_exact_at_anchor": True,
        },
        "rows": rows,
        "row_digest": hashlib.sha256(canonical(rows)).hexdigest(),
        "geometry_scalar_summary": scalar_info,
        "origin_summary": summary,
        "finite_audit": {
            "rows": ROW_COUNT, "cell_count": CELL_COUNT,
            "origin_count": len(ORIGINS), "calibration_origin_count": 3,
            "holdout_origin_count": 3, "complete_cartesian_panel": True,
            "coordinate_disjoint_from_prior": True,
            "same_count_across_all_origins": True,
            "parent_baseline_frozen": True, "response_blind_roles": True,
            "interpolation_identity_exact_at_anchor": True,
            "interpolation_panel_complete": True,
            "fixed_power_credit": 0, "arithmetic_advance": "NO",
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
            print("TPC398_CERTIFICATE=WRITTEN")
        else:
            raw = RESULT.read_bytes()
            stored = json.loads(raw)
            need(raw == canonical(stored), "certificate canonicality")
            need(stored == document, "certificate replay mismatch")
            summary = document["payload"]["origin_summary"]
            spectral = sum(summary["spectral_failures_by_normalization"].values())
            schur = sum(summary["schur_failures_by_normalization"].values())
            print(f"TPC398_CERTIFICATE=PASS rows={ROW_COUNT} cells={CELL_COUNT} "
                  f"origin_passes={summary['within_family_origin_pass_counts']} "
                  f"cross_holdout={summary['cross_family_holdout_pass_counts']} "
                  f"transfer_passes={summary['within_family_transfer_pass_counts']} "
                  f"spectral_failures={spectral} schur_failures={schur}")
        return 0
    except (CheckFailure, OSError, ValueError, TypeError, KeyError,
            json.JSONDecodeError) as error:
        print("TPC398_CERTIFICATE=FAIL " + str(error))
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
