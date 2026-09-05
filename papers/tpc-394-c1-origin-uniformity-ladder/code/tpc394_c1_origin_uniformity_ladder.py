#!/usr/bin/env python3
"""TPC-394: a fresh finite c=1 origin-uniformity ladder.

TPC-393 left a deliberately narrow clue: repeat the origin-spread test on a
new family after the adversarial normalization holdout.  This producer fixes
an eight-origin ladder before reading any current response.  Five origins are
the calibration cohort and three are a held-out cohort; every origin uses the
same window length, so the primary statistic is genuinely an origin-spread
comparison rather than a count-transfer forecast.

The calculation is a finite c=1 proxy.  It does not assert arithmetic
validity, a growing operator estimate, Route-A/Route-B closure, or a twin
prime theorem.
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
RESULT = PROJECT / "results/tpc394_certificate.json"
PARENT_CODE = ROOT / (
    "papers/tpc-393-c1-normalization-adversarial-holdout/code/"
    "tpc393_c1_normalization_adversarial_holdout.py")
PARENT_CERT = ROOT / (
    "papers/tpc-393-c1-normalization-adversarial-holdout/results/"
    "tpc393_certificate.json")
PARENT_CODE_SHA256 = (
    "73ee391f0d4f467ee6fefdc57a1bb42dea93f01df2e2b22e35054b7a95cc6229")
PARENT_CERT_SHA256 = (
    "b983f4bae7836df57a8654fe51c37e72e28e1c0ca013aaaff71c9bdf79a229f1")

SCHEMA = "TPC394_C1_ORIGIN_UNIFORMITY_LADDER_V1"
STATUS = "NUMERICALLY_CERTIFIED_FINITE_C1_ORIGIN_UNIFORMITY_LADDER_AUDIT"
ROUND2_CLUE = "TEST_C1_ORIGIN_CROSS_FAMILY_HOLDOUT"

# The grid, roles, count, and caps are fixed before the current response is
# read.  The unused candidates make the selection protocol auditable.
GRID_START = 5_000_001
GRID_STEP = 401
GRID_COUNT = 41
ORIGIN_INDICES = (0, 5, 10, 15, 20, 25, 30, 35)
CALIBRATION_INDICES = (0, 5, 10, 15, 20)
HOLDOUT_INDICES = (25, 30, 35)
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
LAWS = ("all_plus", "alternating_index")
NORMALIZATIONS = (
    "local_diagonal", "pooled_train_scalar", "origin_scalar",
    "frozen_train_1024_scalar")
ORIGIN_SPREAD_CAP = 0.01
HOLDOUT_TRANSFER_CAP = 0.03
SPECTRAL_CAP = 0.64
SCHUR_CAP = 0.83
EXACT_INTERVAL = (ORIGINS[0], ORIGINS[0] + 13)
EXACT_Q = 8
CELL_COUNT = len(BAND_MODES) * len(Q_ANCHORS) * len(LAWS) * len(NORMALIZATIONS)
ROW_COUNT = len(ORIGINS) * len(Q_ANCHORS) * len(LAWS) * len(NORMALIZATIONS)

CLAIM_FIREWALL = {
    "TPC394_SELECTION_PROTOCOL":
        "PROVED_EXACT_FINITE_PREDECLARED_RESPONSE_BLIND",
    "TPC394_COORDINATE_DISJOINTNESS": "PROVED_EXACT_FINITE",
    "TPC394_PARENT_REFERENCE": "PROVED_EXACT_FINITE_HASHED",
    "TPC394_ORIGIN_LADDER_PANEL":
        "NUMERICALLY_CERTIFIED_FINITE_64_ROWS",
    "TPC394_ORIGIN_UNIFORMITY_AUDIT":
        "NUMERICALLY_CERTIFIED_FINITE_SCOPED",
    "TPC394_CALIBRATION_HOLDOUT_TRANSFER":
        "NUMERICALLY_CERTIFIED_FINITE_SCOPED",
    "TPC394_SPECTRAL_ENVELOPE":
        "REFUTED_ON_DECLARED_FINITE_PANEL",
    "TPC394_SCHUR_ENVELOPE":
        "NUMERICALLY_CERTIFIED_FINITE_SCOPED_ONLY",
    "TPC394_SOURCE_NORMALIZATION_VALIDITY": "MODELING_CHOICE_OPEN",
    "TPC394_GROWING_OPERATOR_BOUND": "OPEN",
    "TPC394_SOURCE_UNIFORM_L2": "OPEN",
    "TPC394_ARITHMETIC_ADVANCE": "NO",
    "TPC394_FIXED_POWER_CREDIT": 0,
    "TPC394_FULL_GATE_B": "OPEN",
    "TPC394_TWIN_PRIME_RESULT": "NONE",
}


class CheckFailure(RuntimeError):
    """Raised when a finite certificate contract is violated."""


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
    """Build the common geometry and the two signed finite matrices."""
    difference = values[:, None] - values[None, :]
    distance = difference.astype(np.float64)
    kernel = (float(HEIGHT) ** (2 * EXPONENT) /
              (HEIGHT * HEIGHT + distance * distance) ** EXPONENT)
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
    need(symmetry <= 2e-12 and schur > 0.0 and frobenius > 0.0 and
         math.isfinite(spectral) and spectral <= schur + 1e-8 and
         spectral <= frobenius + 1e-8, "finite metric envelope")
    return spectral, schur, frobenius, symmetry


def mask_for(mode: str, count: int) -> tuple[np.ndarray, int]:
    need(mode == "fixed_c3" and count % BLOCK_LENGTH == 0,
         "fixed band protocol")
    block_ids = np.arange(count) // BLOCK_LENGTH
    cutoff = 3
    return np.abs(block_ids[:, None] - block_ids[None, :]) <= cutoff, cutoff


def role_for(origin: int) -> str:
    return "calibration_1024" if origin in CALIBRATION_ORIGINS else "holdout_1024"


def make_row(origin: int, q0: int, law: str, norm: str,
             mode: str, matrix: np.ndarray, geometry: np.ndarray,
             denominator: float, denominator_role: str,
             primes: list[int], weights: list[float], mask: np.ndarray,
             effective_cutoff: int,
             unnormalized_metrics: tuple[float, float, float, float]) -> dict[str, Any]:
    if norm == "local_diagonal":
        normalized = matrix / np.sqrt(geometry[:, None] * geometry[None, :])
        spectral, schur, frobenius, symmetry = metrics(
            np.where(mask, normalized, 0.0))
    else:
        # The scalar normalizations are positive homotheties of the same
        # masked matrix.  Reusing the unnormalized eigensystem is exact up to
        # floating-point scaling and avoids four redundant 1024-dimensional
        # eigensolves per origin/law.
        spectral, schur, frobenius, symmetry = tuple(
            value / denominator for value in unnormalized_metrics)
    return {
        "origin": origin, "origin_role": role_for(origin), "Q": q0,
        "law": law, "normalization": norm, "band_mode": mode,
        "effective_cutoff": effective_cutoff, "count": WINDOW_COUNT,
        "interval": [origin, origin + WINDOW_COUNT],
        "block_length": BLOCK_LENGTH, "block_count": WINDOW_COUNT // BLOCK_LENGTH,
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
            primes, matrices, geometry, weights = packs[origin]
            for mode in BAND_MODES:
                mask, cutoff = mask_for(mode, WINDOW_COUNT)
                base_metrics = {
                    law: metrics(np.where(mask, matrices[law], 0.0))
                    for law in LAWS}
                for norm in NORMALIZATIONS:
                    if norm == "local_diagonal":
                        denominator, denominator_role = 1.0, "local_diagonal"
                    elif norm == "pooled_train_scalar":
                        denominator, denominator_role = pooled, "calibration_origin_mean"
                    elif norm == "origin_scalar":
                        denominator, denominator_role = float(geometry.mean()), \
                            f"origin_{origin}_1024"
                    elif norm == "frozen_train_1024_scalar":
                        denominator, denominator_role = frozen, \
                            "first_calibration_origin_1024_frozen"
                    else:
                        raise CheckFailure("unknown normalization")
                    for law in LAWS:
                        rows.append(make_row(
                            origin, q0, law, norm, mode, matrices[law], geometry,
                            denominator, denominator_role, primes, weights,
                            mask, cutoff, base_metrics[law]))
    need(len(rows) == ROW_COUNT, "row census")
    return rows, scalar_info


def finite_stats(values: list[float]) -> dict[str, Any]:
    need(len(values) > 0 and all(math.isfinite(x) and x >= 0 for x in values),
         "finite origin stats")
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


def origin_summary(rows: list[dict[str, Any]]) -> dict[str, Any]:
    """Aggregate the predeclared origin ladder without response selection."""
    definitions = {
        "local_diagonal": "entrywise division by sqrt(G(u)G(v))",
        "pooled_train_scalar": "mean geometry over five calibration origins",
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
                need(len(selected) == len(ORIGINS), "cell origin census")
                values = [float(r["band_spectral"]) for r in selected]
                calibration = [float(r["band_spectral"]) for r in selected
                               if r["origin"] in CALIBRATION_ORIGINS]
                holdout = [float(r["band_spectral"]) for r in selected
                           if r["origin"] in HOLDOUT_ORIGINS]
                all_stats = finite_stats(values)
                calibration_stats = finite_stats(calibration)
                holdout_stats = finite_stats(holdout)
                cal_mean = float(calibration_stats["mean"])
                hold_mean = float(holdout_stats["mean"])
                transfer_error = hold_mean / cal_mean - 1.0
                cells.append({
                    "band_mode": "fixed_c3", "normalization": norm,
                    "normalization_definition": definitions[norm],
                    "law": law, "Q": q0,
                    "origins": [r["origin"] for r in selected],
                    "calibration_origins": list(CALIBRATION_ORIGINS),
                    "holdout_origins": list(HOLDOUT_ORIGINS),
                    "count": WINDOW_COUNT,
                    "all_origin_stats": all_stats,
                    "calibration_stats": calibration_stats,
                    "holdout_stats": holdout_stats,
                    "holdout_to_calibration_ratio": show(hold_mean / cal_mean),
                    "holdout_transfer_error": show(transfer_error),
                    "within_holdout_transfer_cap": bool(
                        abs(transfer_error) <= HOLDOUT_TRANSFER_CAP),
                    "spectral_failures": sum(bool(r["spectral_failure"])
                                              for r in selected),
                    "schur_failures": sum(bool(r["schur_failure"])
                                           for r in selected),
                })
    need(len(cells) == CELL_COUNT, "summary cell census")
    by_key = {(c["normalization"], c["law"], c["Q"]): c for c in cells}
    origin_passes = {
        norm: sum(bool(c["all_origin_stats"]["within_one_percent"])
                  for c in cells if c["normalization"] == norm)
        for norm in NORMALIZATIONS}
    calibration_passes = {
        norm: sum(bool(c["calibration_stats"]["within_one_percent"])
                  for c in cells if c["normalization"] == norm)
        for norm in NORMALIZATIONS}
    holdout_passes = {
        norm: sum(bool(c["holdout_stats"]["within_one_percent"])
                  for c in cells if c["normalization"] == norm)
        for norm in NORMALIZATIONS}
    transfer_passes = {
        norm: sum(bool(c["within_holdout_transfer_cap"])
                  for c in cells if c["normalization"] == norm)
        for norm in NORMALIZATIONS}
    max_spread = {
        norm: show(max(float(c["all_origin_stats"]["relative_spread"])
                      for c in cells if c["normalization"] == norm))
        for norm in NORMALIZATIONS}
    max_transfer = {
        norm: show(max(abs(float(c["holdout_transfer_error"]))
                      for c in cells if c["normalization"] == norm))
        for norm in NORMALIZATIONS}
    spectral_failures = {
        norm: sum(c["spectral_failures"] for c in cells
                  if c["normalization"] == norm)
        for norm in NORMALIZATIONS}
    schur_failures = {
        norm: sum(c["schur_failures"] for c in cells
                  if c["normalization"] == norm)
        for norm in NORMALIZATIONS}
    terminal_means = {
        norm: show(float(np.mean([
            float(by_key[norm, law, q0]["all_origin_stats"]["mean"])
            for law in LAWS for q0 in Q_ANCHORS])))
        for norm in NORMALIZATIONS}
    law_ratio = {}
    for norm in NORMALIZATIONS:
        plus = float(by_key[norm, "all_plus", Q_ANCHORS[0]]
                     ["all_origin_stats"]["mean"])
        alternating = float(by_key[norm, "alternating_index", Q_ANCHORS[0]]
                             ["all_origin_stats"]["mean"])
        law_ratio[norm] = show(alternating / plus)
    return {
        "cells": cells, "cell_count": CELL_COUNT, "row_count": ROW_COUNT,
        "normalizations": list(NORMALIZATIONS), "laws": list(LAWS),
        "origin_count": len(ORIGINS),
        "calibration_origin_count": len(CALIBRATION_ORIGINS),
        "holdout_origin_count": len(HOLDOUT_ORIGINS),
        "origin_spread_cap": show(ORIGIN_SPREAD_CAP),
        "holdout_transfer_cap": show(HOLDOUT_TRANSFER_CAP),
        "spectral_cap": show(SPECTRAL_CAP), "schur_cap": show(SCHUR_CAP),
        "origin_uniformity_pass_counts": origin_passes,
        "calibration_uniformity_pass_counts": calibration_passes,
        "holdout_uniformity_pass_counts": holdout_passes,
        "holdout_transfer_pass_counts": transfer_passes,
        "maximum_all_origin_relative_spread": max_spread,
        "maximum_holdout_transfer_abs_error": max_transfer,
        "spectral_failures_by_normalization": spectral_failures,
        "schur_failures_by_normalization": schur_failures,
        "terminal_mean_by_normalization": terminal_means,
        "alternating_to_all_plus_mean_ratio": law_ratio,
        "origin_uniformity_stable_cells": sum(
            bool(c["all_origin_stats"]["within_one_percent"]) for c in cells),
        "holdout_transfer_stable_cells": sum(
            bool(c["within_holdout_transfer_cap"]) for c in cells),
    }


def prior_intervals() -> list[tuple[int, int]]:
    # Every interval is explicit so the disjointness claim is independently
    # checkable; these are the recent finite c=1 panels that could otherwise
    # be confused with the current family.
    return [
        (3800001, 3800001 + 1024), (3804011, 3804011 + 1024),
        (3808021, 3808021 + 1024), (3812031, 3812031 + 1536),
        (3816041, 3816041 + 1536),
        (4200001, 4200001 + 1024), (4204011, 4204011 + 1280),
        (4208021, 4208021 + 1280), (4212031, 4212031 + 1536),
        (4216041, 4216041 + 1536),
        (3400001, 3400001 + 1408), (3404011, 3404011 + 1408),
        (3408021, 3408021 + 1408), (3412031, 3412031 + 1536),
        (3416041, 3416041 + 1536),
        (3000001, 3000001 + 1280), (3004011, 3004011 + 1280),
        (3008021, 3008021 + 1280), (3012031, 3012031 + 1536),
        (3016041, 3016041 + 1536),
        (2800001, 2800001 + 1024), (2804011, 2804011 + 1024),
        (2808021, 2808021 + 1024), (2812031, 2812031 + 1280),
        (2816041, 2816041 + 1280),
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
    sign_vectors = signs(primes)
    matrices: dict[str, list[list[Fraction]]] = {law: [] for law in LAWS}
    geometry: list[Fraction] = []
    for u in values:
        row_values = {law: [] for law in LAWS}
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


def parent_reference() -> dict[str, Any]:
    need(PARENT_CODE.is_file() and
         digest(PARENT_CODE.read_bytes()) == PARENT_CODE_SHA256,
         "parent code provenance")
    raw = PARENT_CERT.read_bytes()
    need(digest(raw) == PARENT_CERT_SHA256, "parent certificate provenance")
    document = json.loads(raw)
    need(raw == canonical(document), "parent certificate canonicality")
    payload = document.get("payload", {})
    need(payload.get("schema") ==
         "TPC393_C1_NORMALIZATION_ADVERSARIAL_HOLDOUT_V1" and
         payload.get("status") ==
         "NUMERICALLY_CERTIFIED_FINITE_C1_NORMALIZATION_ADVERSARIAL_HOLDOUT_AUDIT",
         "parent header")
    return {"schema": payload["schema"], "status": payload["status"]}


def build_payload() -> dict[str, Any]:
    parent = parent_reference()
    need(coordinate_disjointness(), "coordinate disjointness")
    rows, scalar_info = build_rows()
    summary = origin_summary(rows)
    candidate_origins = [GRID_START + GRID_STEP * i for i in range(GRID_COUNT)]
    return {
        "schema": SCHEMA, "status": STATUS,
        "parent_lock": {
            "parent_code_sha256": PARENT_CODE_SHA256,
            "parent_certificate_sha256": PARENT_CERT_SHA256,
            "parent_schema": parent["schema"], "parent_status": parent["status"],
            "parent_round2_clue": "TEST_C1_ORIGIN_UNIFORMITY_AFTER_REPLICATION",
            "parent_interface_frozen": True,
            "parent_interface_used_for_current_fit": False,
        },
        "selection_protocol": {
            "grid_start": GRID_START, "grid_step": GRID_STEP,
            "grid_count": GRID_COUNT, "candidate_origins": candidate_origins,
            "origin_indices": list(ORIGIN_INDICES), "origins": list(ORIGINS),
            "calibration_indices": list(CALIBRATION_INDICES),
            "calibration_origins": list(CALIBRATION_ORIGINS),
            "holdout_indices": list(HOLDOUT_INDICES),
            "holdout_origins": list(HOLDOUT_ORIGINS),
            "window_count": WINDOW_COUNT, "block_length": BLOCK_LENGTH,
            "band_modes": list(BAND_MODES), "q_anchors": list(Q_ANCHORS),
            "laws": list(LAWS), "normalizations": list(NORMALIZATIONS),
            "origin_spread_cap": show(ORIGIN_SPREAD_CAP),
            "holdout_transfer_cap": show(HOLDOUT_TRANSFER_CAP),
            "response_used_for_selection": False,
            "metric_used_for_selection": False,
            "holdout_role_fixed_before_readout": True,
            "parent_interface_used_for_current_fit": False,
        },
        "protocol": {
            "origins": list(ORIGINS),
            "calibration_origins": list(CALIBRATION_ORIGINS),
            "holdout_origins": list(HOLDOUT_ORIGINS),
            "window_count": WINDOW_COUNT, "block_length": BLOCK_LENGTH,
            "band_modes": list(BAND_MODES), "q_anchors": list(Q_ANCHORS),
            "kernel_exponents": [EXPONENT], "betas": [BETA], "height": HEIGHT,
            "laws": list(LAWS), "normalizations": list(NORMALIZATIONS),
            "metric": "fixed-c3 band spectral diagnostic",
            "origin_spread_definition": "(max-min)/mean over locked origins",
            "holdout_transfer_definition":
                "holdout mean / calibration mean - 1 at fixed count",
            "source_response_used": False, "origin_selection_used": False,
            "law_selection_used": False, "normalization_selection_used": False,
            "row_selection_used": False,
            "normalization_definitions": {
                "local_diagonal": "entrywise division by sqrt(G(u)G(v))",
                "pooled_train_scalar": "mean geometry over five calibration origins",
                "origin_scalar": "current-origin mean geometry",
                "frozen_train_1024_scalar":
                    "first calibration-origin mean geometry, frozen across origins",
            },
            "origin_uniformity_definition":
                "all-origin relative spread <= 0.01",
            "holdout_transfer_definition":
                "absolute holdout/calibration mean ratio error <= 0.03",
        },
        "rows": rows,
        "row_digest": hashlib.sha256(canonical(rows)).hexdigest(),
        "geometry_scalar_summary": scalar_info,
        "origin_summary": summary,
        "finite_audit": {
            "rows": ROW_COUNT, "cell_count": CELL_COUNT,
            "origin_count": len(ORIGINS),
            "calibration_origin_count": len(CALIBRATION_ORIGINS),
            "holdout_origin_count": len(HOLDOUT_ORIGINS),
            "complete_cartesian_panel": True,
            "coordinate_disjoint_from_prior": True,
            "same_count_across_all_origins": True,
            "response_blind_roles": True, "fixed_power_credit": 0,
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
            print("TPC394_CERTIFICATE=WRITTEN")
        else:
            raw = RESULT.read_bytes()
            stored = json.loads(raw)
            need(raw == canonical(stored), "certificate canonicality")
            need(stored == document, "certificate replay mismatch")
            summary = document["payload"]["origin_summary"]
            spectral = sum(summary["spectral_failures_by_normalization"].values())
            schur = sum(summary["schur_failures_by_normalization"].values())
            print(f"TPC394_CERTIFICATE=PASS rows={ROW_COUNT} cells={CELL_COUNT} "
                  f"origin_passes={summary['origin_uniformity_pass_counts']} "
                  f"transfer_passes={summary['holdout_transfer_pass_counts']} "
                  f"spectral_failures={spectral} schur_failures={schur}")
        return 0
    except (CheckFailure, OSError, ValueError, TypeError, KeyError,
            json.JSONDecodeError) as error:
        print("TPC394_CERTIFICATE=FAIL " + str(error))
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
