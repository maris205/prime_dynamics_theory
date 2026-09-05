#!/usr/bin/env python3
"""TPC-393: an adversarial scalar-normalization holdout audit.

TPC-391 localized a finite frozen-interface horizon crossing while its local
control remained below the transfer cap.  This release asks the next
minimal question on a fresh disjoint family: how much of the observed
trajectory is changed by the declared scalar normalization itself?  Four
response-blind normalizations are compared on a fixed near-block band.
The panel is deliberately restricted to the predeclared high-Q
alternating-index versus all-plus control.  Everything here is a c=1 proxy
calculation; no arithmetic or asymptotic claim is made.
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
RESULT = PROJECT / "results/tpc393_certificate.json"
PARENT_CODE = ROOT / (
    "papers/tpc-392-c1-normalization-phase-diagram/code/"
    "tpc392_c1_normalization_phase_diagram.py")
PARENT_CERT = ROOT / (
    "papers/tpc-392-c1-normalization-phase-diagram/results/"
    "tpc392_certificate.json")
PARENT_CODE_SHA256 = (
    "0b0847dee598e598875c73684176b67cafd2eae74c25f62c48b48267009f7b4e")
PARENT_CERT_SHA256 = (
    "8481c38adffdf5ef51ca30fbf85b79deafc4ac7c499718509b6d35b243fe7e14")

SCHEMA = "TPC393_C1_NORMALIZATION_ADVERSARIAL_HOLDOUT_V1"
STATUS = "NUMERICALLY_CERTIFIED_FINITE_C1_NORMALIZATION_ADVERSARIAL_HOLDOUT_AUDIT"
ROUND2_CLUE = "TEST_C1_ORIGIN_UNIFORMITY_AFTER_REPLICATION"
GRID_START = 4_200_001
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
BAND_MODES = ("fixed_c3",)
Q_ANCHORS = (8192,)
EXPONENT = 1
BETA = 2
HEIGHT = 66
LAWS = ("all_plus", "alternating_index")
NORMALIZATIONS = (
    "local_diagonal",
    "pooled_train_scalar",
    "origin_scalar",
    "frozen_train_1024_scalar",
)
SPREAD_CAP = 0.01
SPECTRAL_CAP = 0.64
SCHUR_CAP = 0.83
TRANSFER_ERROR_CAP = 0.03
EXACT_INTERVAL = (ORIGINS[0], ORIGINS[0] + 13)
EXACT_Q = 8
CELL_COUNT = len(BAND_MODES) * len(Q_ANCHORS) * len(LAWS) * len(NORMALIZATIONS)
ROW_COUNT = ((len(CALIBRATION_ORIGINS) * len(CALIBRATION_COUNTS) +
              len(HOLDOUT_ORIGINS)) * len(Q_ANCHORS) * len(LAWS) *
             len(NORMALIZATIONS) * len(BAND_MODES))

CLAIM_FIREWALL = {
    "TPC393_SELECTION_PROTOCOL":
        "PROVED_EXACT_FINITE_PREDECLARED_RESPONSE_BLIND",
    "TPC393_COORDINATE_DISJOINTNESS": "PROVED_EXACT_FINITE",
    "TPC393_PARENT_REFERENCE": "PROVED_EXACT_FINITE_HASHED",
    "TPC393_NORMALIZATION_PANEL":
        "NUMERICALLY_CERTIFIED_FINITE_64_ROWS",
    "TPC393_SCALAR_DEFINITIONS":
        "PROVED_EXACT_FINITE_DECLARED",
    "TPC393_PHASE_COMPARISON":
        "NUMERICALLY_CERTIFIED_FINITE_SCOPED",
    "TPC393_CALIBRATION_FORECAST":
        "NUMERICALLY_CERTIFIED_FINITE_SCOPED",
    "TPC393_ORIGIN_UNIFORMITY": "OPEN",
    "TPC393_COUNT_UNIFORMITY": "OPEN",
    "TPC393_SOURCE_NORMALIZATION_VALIDITY": "MODELING_CHOICE_OPEN",
    "TPC393_GROWING_OPERATOR_BOUND": "OPEN",
    "TPC393_SOURCE_UNIFORM_L2": "OPEN",
    "TPC393_ARITHMETIC_ADVANCE": "NO",
    "TPC393_FIXED_POWER_CREDIT": 0,
    "TPC393_FULL_GATE_B": "OPEN",
    "TPC393_TWIN_PRIME_RESULT": "NONE",
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
        frozen = train_scalars[1024]
        scalar_info[str(q0)] = {
            "by_calibration_count": {str(k): show(v)
                                     for k, v in train_scalars.items()},
            "geometry_log2_slope": show(gamma),
            "extrapolated_1536": show(extrapolated),
            "frozen_train_1024": show(frozen),
        }
        for (origin, count), (primes, matrices, geometry, weights) in packs.items():
            for mode in BAND_MODES:
                mask, cutoff = mask_for(mode, count)
                for norm in NORMALIZATIONS:
                    if norm == "local_diagonal":
                        denominator, denominator_role = 1.0, "local_diagonal"
                    elif norm == "pooled_train_scalar":
                        if count in train_scalars:
                            denominator, denominator_role = train_scalars[count], f"calibration_{count}"
                        else:
                            denominator, denominator_role = extrapolated, "calibration_extrapolated_1536"
                    elif norm == "origin_scalar":
                        denominator, denominator_role = float(geometry.mean()), \
                            f"origin_{origin}_{count}"
                    elif norm == "frozen_train_1024_scalar":
                        denominator, denominator_role = frozen, \
                            "calibration_1024_frozen"
                    else:
                        raise CheckFailure("unknown normalization")
                    for law in LAWS:
                        rows.append(make_row(
                            origin, count, q0, law, norm, mode, matrices[law],
                            geometry, denominator, denominator_role, primes,
                            weights, mask, cutoff))
    need(len(rows) == ROW_COUNT, "row census")
    return rows, scalar_info


def parent_reference() -> dict[str, Any]:
    raw = PARENT_CERT.read_bytes()
    need(digest(raw) == PARENT_CERT_SHA256, "parent certificate provenance")
    document = json.loads(raw)
    payload = document.get("payload", {})
    need(payload.get("schema") ==
         "TPC392_C1_NORMALIZATION_PHASE_DIAGRAM_V1", "parent schema")
    need(payload.get("status") ==
         "NUMERICALLY_CERTIFIED_FINITE_C1_NORMALIZATION_PHASE_DIAGRAM_AUDIT",
         "parent status")
    return {
        "schema": payload["schema"],
        "status": payload["status"],
        "parent_certificate_sha256": PARENT_CERT_SHA256,
    }


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


def _legacy_transfer_summary(rows: list[dict[str, Any]],
                             parents: dict[tuple[str, str, str, int], dict[str, Any]]) -> dict[str, Any]:
    """Retained TPC-391 template, intentionally unused by TPC-393.

    The active release summary is ``phase_summary`` below.  Keeping this
    quarantined helper makes the historical comparison explicit without
    allowing a parent-slope forecast to enter the current certificate.
    """
    raise CheckFailure("retired TPC-391 helper is not part of TPC-393")
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
                    trajectory = []
                    for count in HORIZON_LEVELS:
                        parent_prediction = means[1024] * (
                            count / 1024.0) ** parent_alpha
                        local_prediction = means[1024] * (
                            count / 1024.0) ** local_alpha
                        parent_error = means[count] / parent_prediction - 1.0
                        local_error = means[count] / local_prediction - 1.0
                        if count >= 1280:
                            stage1 = means[1024] * (
                                1280.0 / 1024.0) ** parent_alpha
                            recursive_prediction = stage1 * (
                                count / 1280.0) ** parent_alpha
                            direct_prediction = means[1024] * (
                                count / 1024.0) ** parent_alpha
                            composition_error = (
                                recursive_prediction / direct_prediction - 1.0)
                            recursive_error = (
                                means[count] / recursive_prediction - 1.0)
                        else:
                            recursive_prediction = None
                            direct_prediction = None
                            composition_error = None
                            recursive_error = None
                        trajectory.append({
                            "count": count,
                            "mean": show(means[count]),
                            "parent_prediction_from_N1024": show(parent_prediction),
                            "local_prediction_from_N1024": show(local_prediction),
                            "parent_error": show(parent_error),
                            "local_error": show(local_error),
                            "within_parent_cap": bool(
                                abs(parent_error) <= TRANSFER_ERROR_CAP),
                            "within_local_cap": bool(
                                abs(local_error) <= TRANSFER_ERROR_CAP),
                            "recursive_prediction_from_N1024":
                                "NOT_DEFINED" if recursive_prediction is None
                                else show(recursive_prediction),
                            "direct_prediction_from_N1024":
                                "NOT_DEFINED" if direct_prediction is None
                                else show(direct_prediction),
                            "recursive_error":
                                "NOT_DEFINED" if recursive_error is None
                                else show(recursive_error),
                            "composition_error":
                                "NOT_DEFINED" if composition_error is None
                                else show(composition_error),
                            "within_recursive_cap":
                                "NOT_DEFINED" if recursive_error is None
                                else bool(abs(recursive_error) <=
                                          TRANSFER_ERROR_CAP),
                        })
                    parent_crossing = next(
                        (count for count, item in
                         zip(HORIZON_LEVELS, trajectory)
                         if not item["within_parent_cap"]), "NONE")
                    local_crossing = next(
                        (count for count, item in
                         zip(HORIZON_LEVELS, trajectory)
                         if not item["within_local_cap"]), "NONE")
                    cells.append({
                        "band_mode": mode, "normalization": norm,
                        "law": law, "Q": q0,
                        "origins": [r["origin"] for r in selected],
                        "calibration_origins": list(CALIBRATION_ORIGINS),
                        "holdout_origins": list(HOLDOUT_ORIGINS),
                        "calibration_counts": list(CALIBRATION_COUNTS),
                        "holdout_count": HOLDOUT_COUNT,
                        "N1024": stats[1024], "N1152": stats[1152],
                        "N1280": stats[1280], "N1408": stats[1408],
                        "N1536_holdout": stats[1536],
                        "parent_horizon_log2_slope": show(parent_alpha),
                        "local_horizon_log2_slope": show(local_alpha),
                        "trajectory": trajectory,
                        "first_parent_cap_crossing": parent_crossing,
                        "first_local_cap_crossing": local_crossing,
                        "recursive_composition_max_abs_error": show(max(
                            abs(float(item["composition_error"]))
                            for item in trajectory
                            if item["composition_error"] != "NOT_DEFINED")),
                    })
    need(len(cells) == CELL_COUNT, "cell census")
    horizons = list(HORIZON_LEVELS)
    parent_passes = {
        str(count): sum(bool(cell["trajectory"][index]["within_parent_cap"])
                        for cell in cells)
        for index, count in enumerate(horizons)
    }
    local_passes = {
        str(count): sum(bool(cell["trajectory"][index]["within_local_cap"])
                        for cell in cells)
        for index, count in enumerate(horizons)
    }
    recursive_horizons = (1280, 1408, 1536)
    recursive_passes = {
        str(count): sum(cell["trajectory"][index]["within_recursive_cap"]
                        is True for cell in cells)
        for count in recursive_horizons
        for index in [horizons.index(count)]
    }
    parent_max = {
        str(count): show(max(abs(float(cell["trajectory"][index]["parent_error"]))
                             for cell in cells))
        for index, count in enumerate(horizons)
    }
    local_max = {
        str(count): show(max(abs(float(cell["trajectory"][index]["local_error"]))
                             for cell in cells))
        for index, count in enumerate(horizons)
    }
    recursive_max = {
        str(count): show(max(abs(float(cell["trajectory"][horizons.index(count)]
                                      ["recursive_error"]))
                            for cell in cells))
        for count in recursive_horizons
    }
    crossing_counts = {str(count): 0 for count in horizons}
    crossing_counts["NONE"] = 0
    local_crossing_counts = {str(count): 0 for count in horizons}
    local_crossing_counts["NONE"] = 0
    for cell in cells:
        crossing_counts[str(cell["first_parent_cap_crossing"])] += 1
        local_crossing_counts[str(cell["first_local_cap_crossing"])] += 1
    stable = {
        str(count): sum(bool(cell[f"N{count}"]["within_one_percent"])
                        for cell in cells)
        for count in (1024, 1152, 1280, 1408)
    }
    stable["1536_holdout"] = sum(
        bool(cell["N1536_holdout"]["within_one_percent"]) for cell in cells)
    failures = {
        f"{mode}_{norm}": {
            "spectral": sum(bool(r["spectral_failure"]) for r in rows
                             if r["band_mode"] == mode and r["normalization"] == norm),
            "schur": sum(bool(r["schur_failure"]) for r in rows
                          if r["band_mode"] == mode and r["normalization"] == norm),
        }
        for mode in BAND_MODES for norm in NORMALIZATIONS
    }
    composition_values = [
        abs(float(item["composition_error"]))
        for cell in cells for item in cell["trajectory"]
        if item["composition_error"] != "NOT_DEFINED"
    ]
    return {
        "cells": cells, "cell_count": CELL_COUNT, "row_count": ROW_COUNT,
        "horizon_levels": horizons,
        "recursive_horizon_levels": list(recursive_horizons),
        "stable_cells": stable,
        "failure_counts_by_mode_normalization": failures,
        "parent_pass_counts_by_horizon": parent_passes,
        "local_pass_counts_by_horizon": local_passes,
        "recursive_pass_counts_by_horizon": recursive_passes,
        "first_parent_crossing_counts": crossing_counts,
        "first_local_crossing_counts": local_crossing_counts,
        "parent_max_abs_error_by_horizon": parent_max,
        "local_max_abs_error_by_horizon": local_max,
        "recursive_max_abs_error_by_horizon": recursive_max,
        "recursive_composition_max_abs_error": show(max(composition_values)),
        "transfer_error_cap": show(TRANSFER_ERROR_CAP),
        "spread_cap": show(SPREAD_CAP),
        "spectral_cap": show(SPECTRAL_CAP), "schur_cap": show(SCHUR_CAP),
    }


def phase_summary(rows: list[dict[str, Any]]) -> dict[str, Any]:
    """Summarize the predeclared targeted normalization holdout panel."""
    cells: list[dict[str, Any]] = []
    definitions = {
        "local_diagonal":
            "entrywise division by sqrt(G(u)G(v))",
        "pooled_train_scalar":
            "calibration-origin mean geometry at each count, with log extrapolation at 1536",
        "origin_scalar":
            "current-origin mean geometry at each count",
        "frozen_train_1024_scalar":
            "single calibration-origin mean geometry at N=1024 for every count",
    }
    for norm in NORMALIZATIONS:
        for law in LAWS:
            for q0 in Q_ANCHORS:
                selected = [r for r in rows
                            if r["normalization"] == norm and
                            r["law"] == law and r["Q"] == q0]
                selected.sort(key=lambda r: (r["count"], r["origin"]))
                by_count = {
                    count: [float(r["band_spectral"]) for r in selected
                            if r["count"] == count]
                    for count in COUNT_LEVELS
                }
                stats = {count: finite_stats(by_count[count])
                         for count in COUNT_LEVELS}
                means = {count: float(stats[count]["mean"])
                         for count in COUNT_LEVELS}
                slope = math.log(means[1280] / means[1024]) / math.log(
                    1280.0 / 1024.0)
                forecast = means[1024] * (1536.0 / 1024.0) ** slope
                error = means[1536] / forecast - 1.0
                cells.append({
                    "band_mode": "fixed_c3", "normalization": norm,
                    "normalization_definition": definitions[norm],
                    "law": law, "Q": q0,
                    "origins": [r["origin"] for r in selected],
                    "calibration_origins": list(CALIBRATION_ORIGINS),
                    "holdout_origins": list(HOLDOUT_ORIGINS),
                    "calibration_counts": list(CALIBRATION_COUNTS),
                    "holdout_count": HOLDOUT_COUNT,
                    "N1024": stats[1024], "N1280": stats[1280],
                    "N1536_holdout": stats[1536],
                    "local_log2_slope": show(slope),
                    "forecast_1536": show(forecast),
                    "forecast_error": show(error),
                    "within_forecast_cap": bool(abs(error) <= TRANSFER_ERROR_CAP),
                    "spectral_failures_by_count": {
                        str(count): sum(bool(r["spectral_failure"])
                                         for r in selected
                                         if r["count"] == count)
                        for count in COUNT_LEVELS
                    },
                    "schur_failures_by_count": {
                        str(count): sum(bool(r["schur_failure"])
                                        for r in selected
                                        if r["count"] == count)
                        for count in COUNT_LEVELS
                    },
                })
    need(len(cells) == CELL_COUNT, "phase cell census")
    local_means = {}
    for cell in cells:
        if cell["normalization"] == "local_diagonal":
            for count in COUNT_LEVELS:
                local_means[cell["law"], cell["Q"], count] = float(
                    cell[f"N{count}" if count != HOLDOUT_COUNT
                         else "N1536_holdout"]["mean"])
    for cell in cells:
        cell["mean_ratio_to_local"] = {
            str(count): show(float(
                cell[f"N{count}" if count != HOLDOUT_COUNT
                     else "N1536_holdout"]["mean"]) /
                local_means[cell["law"], cell["Q"], count])
            for count in COUNT_LEVELS
        }
    forecast_passes = {
        norm: sum(cell["normalization"] == norm and
                  bool(cell["within_forecast_cap"]) for cell in cells)
        for norm in NORMALIZATIONS
    }
    forecast_max = {
        norm: show(max(abs(float(cell["forecast_error"]))
                        for cell in cells if cell["normalization"] == norm))
        for norm in NORMALIZATIONS
    }
    terminal_means = {
        norm: show(float(np.mean([
            float(cell["N1536_holdout"]["mean"]) for cell in cells
            if cell["normalization"] == norm])))
        for norm in NORMALIZATIONS
    }
    terminal_order = [
        norm for norm, _ in sorted(
            ((norm, float(terminal_means[norm])) for norm in NORMALIZATIONS),
            key=lambda item: (-item[1], item[0]))
    ]
    spectral_failures = {
        norm: sum(bool(r["spectral_failure"]) for r in rows
                  if r["normalization"] == norm)
        for norm in NORMALIZATIONS
    }
    schur_failures = {
        norm: sum(bool(r["schur_failure"]) for r in rows
                  if r["normalization"] == norm)
        for norm in NORMALIZATIONS
    }
    stable = {
        str(count): sum(bool(cell[
            f"N{count}" if count != HOLDOUT_COUNT else "N1536_holdout"
        ]["within_one_percent"]) for cell in cells)
        for count in COUNT_LEVELS
    }
    return {
        "cells": cells, "cell_count": CELL_COUNT, "row_count": ROW_COUNT,
        "normalizations": list(NORMALIZATIONS),
        "calibration_counts": list(CALIBRATION_COUNTS),
        "holdout_count": HOLDOUT_COUNT,
        "forecast_cap": show(TRANSFER_ERROR_CAP),
        "spectral_cap": show(SPECTRAL_CAP),
        "schur_cap": show(SCHUR_CAP),
        "forecast_pass_counts_by_normalization": forecast_passes,
        "forecast_max_abs_error_by_normalization": forecast_max,
        "terminal_mean_by_normalization": terminal_means,
        "terminal_mean_ordering": terminal_order,
        "spectral_failures_by_normalization": spectral_failures,
        "schur_failures_by_normalization": schur_failures,
        "stable_cells": stable,
    }


def coordinate_disjointness() -> bool:
    prior = [
        (3800001, 3800001 + 1024), (3804011, 3804011 + 1024),
        (3808021, 3808021 + 1024),
        (3812031, 3812031 + 1536), (3816041, 3816041 + 1536),
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
        (3000001, 3000001 + 1280), (3004011, 3004011 + 1280),
        (3008021, 3008021 + 1280), (3012031, 3012031 + 1536),
        (3016041, 3016041 + 1536),
        (3400001, 3400001 + 1408), (3404011, 3404011 + 1408),
        (3408021, 3408021 + 1408), (3412031, 3412031 + 1536),
        (3416041, 3416041 + 1536),
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
    parent = parent_reference()
    need(coordinate_disjointness(), "coordinate disjointness")
    rows, scalar_info = build_rows()
    summary = phase_summary(rows)
    return {
        "schema": SCHEMA, "status": STATUS,
        "parent_lock": {
            "parent_code_sha256": PARENT_CODE_SHA256,
            "parent_certificate_sha256": PARENT_CERT_SHA256,
            "parent_schema": parent["schema"],
            "parent_status": parent["status"],
            "parent_round2_clue": "TEST_C1_NORMALIZATION_ADVERSARIAL_HOLDOUT",
            "parent_interface_frozen": True,
            "parent_interface_used_for_current_fit": False,
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
            "parent_interface_read_before_current_response": True,
            "parent_interface_used_for_current_fit": False,
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
            "normalization_definitions": {
                "local_diagonal":
                    "entrywise division by sqrt(G(u)G(v))",
                "pooled_train_scalar":
                    "calibration-origin mean geometry at each count, log-extrapolated at 1536",
                "origin_scalar":
                    "current-origin mean geometry at each count",
                "frozen_train_1024_scalar":
                    "single calibration-origin mean geometry at N=1024 for every count",
            },
            "forecast_definition":
                "N=1024 mean times (N/1024) to the current-family 1024-to-1280 log2 slope",
            "phase_cap_definition": "absolute forecast ratio error <= 0.03",
            "normalization_selection_definition":
                "all four scalar/diagonal choices fixed before current responses",
        },
        "rows": rows,
        "row_digest": hashlib.sha256(canonical(rows)).hexdigest(),
        "geometry_scalar_summary": scalar_info,
        "transfer_summary": summary,
        "finite_audit": {
            "rows": ROW_COUNT, "cell_count": CELL_COUNT, "origin_count": 5,
            "calibration_origin_count": 3, "holdout_origin_count": 2,
            "calibration_count_levels": 2, "holdout_count_levels": 1,
            "calibration_counts": list(CALIBRATION_COUNTS),
            "holdout_count": HOLDOUT_COUNT,
            "band_mode_count": 1, "q_count": 1, "law_count": 2,
            "normalization_count": 4, "complete_cartesian_panel": True,
            "coordinate_disjoint_from_prior": True,
            "parent_interface_frozen": True, "fixed_power_credit": 0,
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
            print("TPC393_CERTIFICATE=WRITTEN")
        else:
            stored = json.loads(RESULT.read_bytes())
            need(stored == document, "certificate replay mismatch")
            summary = document["payload"]["transfer_summary"]
            print(f"TPC393_CERTIFICATE=PASS rows={ROW_COUNT} cells={CELL_COUNT} "
                  f"forecast_passes={summary['forecast_pass_counts_by_normalization']} "
                  f"spectral_failures={sum(summary['spectral_failures_by_normalization'].values())} "
                  f"schur_failures={sum(summary['schur_failures_by_normalization'].values())} "
                  f"stable_holdout={summary['stable_cells']['1536']}/{CELL_COUNT} "
                  f"terminal_order={summary['terminal_mean_ordering']}")
        return 0
    except (CheckFailure, OSError, ValueError, TypeError, KeyError,
            json.JSONDecodeError) as error:
        print("TPC393_CERTIFICATE=FAIL " + str(error), file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
