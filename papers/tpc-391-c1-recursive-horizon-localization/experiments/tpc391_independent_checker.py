#!/usr/bin/env python3
"""Independent reverse-shell replay for TPC-391.

This file intentionally does not import the TPC-391 producer.  It rebuilds
the finite c=1 matrices in descending prime-shell order and checks the
horizon-localization audit against the sealed certificate.
"""

from __future__ import annotations

import hashlib
import json
import math
import os
import sys
from pathlib import Path
from typing import Any

os.environ.setdefault("OMP_NUM_THREADS", "1")
os.environ.setdefault("OPENBLAS_NUM_THREADS", "1")
os.environ.setdefault("MKL_NUM_THREADS", "1")
import numpy as np

ROOT = Path(__file__).resolve().parents[3]
PROJECT = ROOT / "papers/tpc-391-c1-recursive-horizon-localization"
CERTIFICATE = PROJECT / "results/tpc391_certificate.json"
PARENT_CERT = ROOT / (
    "papers/tpc-390-c1-recursive-slope-composition/results/"
    "tpc390_certificate.json")
PARENT_CERT_SHA256 = (
    "870c92db4c697a1a822554256019657e1c3c27ab78f9e76a41b4ade5911d34d0")

SCHEMA = "TPC391_C1_RECURSIVE_HORIZON_LOCALIZATION_V1"
STATUS = "NUMERICALLY_CERTIFIED_FINITE_C1_RECURSIVE_HORIZON_LOCALIZATION_AUDIT"
ORIGINS = (3400001, 3404011, 3408021, 3412031, 3416041)
CALIBRATION_ORIGINS = ORIGINS[:3]
HOLDOUT_ORIGINS = ORIGINS[3:]
CALIBRATION_COUNTS = (1024, 1152, 1280, 1408)
HOLDOUT_COUNT = 1536
COUNT_LEVELS = CALIBRATION_COUNTS + (HOLDOUT_COUNT,)
HORIZON_LEVELS = (1152, 1280, 1408, 1536)
BLOCK_LENGTH = 128
BAND_MODES = ("fixed_c3", "full_relative")
Q_ANCHORS = (2048, 8192)
EXPONENT = 1
BETA = 2
HEIGHT = 66
LAWS = ("all_plus", "alternating_index", "mod4_character", "half_split")
NORMALIZATIONS = ("local_diagonal", "pooled_train_scalar")
SPECTRAL_CAP = 0.64
SCHUR_CAP = 0.83
TRANSFER_ERROR_CAP = 0.03


class Failure(RuntimeError):
    pass


def need(condition: bool, message: str) -> None:
    if type(condition) is not bool or not condition:
        raise Failure(message)


def canonical(value: Any) -> bytes:
    return (json.dumps(value, ensure_ascii=True, sort_keys=True,
                       separators=(",", ":")) + "\n").encode("ascii")


def digest(data: bytes) -> str:
    return hashlib.sha256(data.replace(b"\r\n", b"\n").replace(
        b"\r", b"\n")).hexdigest()


def parse_no_duplicates(raw: bytes) -> dict[str, Any]:
    def hook(pairs):
        out = {}
        for key, value in pairs:
            if key in out:
                raise Failure("duplicate JSON key")
            out[key] = value
        return out
    value = json.loads(raw, object_pairs_hook=hook)
    need(isinstance(value, dict), "document object")
    return value


def finite_tree(value: Any) -> bool:
    if isinstance(value, float):
        return math.isfinite(value)
    if isinstance(value, dict):
        return all(isinstance(k, str) and finite_tree(v)
                   for k, v in value.items())
    if isinstance(value, list):
        return all(finite_tree(v) for v in value)
    return True


def close(actual: float, recorded: Any, label: str,
          tolerance: float = 5.0e-8) -> None:
    try:
        target = float(recorded)
    except (TypeError, ValueError) as error:
        raise Failure(label + " is not numeric") from error
    need(math.isfinite(actual) and math.isfinite(target) and
         abs(actual - target) <= tolerance * max(1.0, abs(actual), abs(target)),
         label + " mismatch")


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
    result = {}
    for law in LAWS:
        result[law] = np.asarray([
            1.0 if (law == "all_plus" or
                    (law == "alternating_index" and i % 2 == 0) or
                    (law == "mod4_character" and p % 4 == 1) or
                    (law == "half_split" and i < len(primes) / 2)) else -1.0
            for i, p in enumerate(primes)], dtype=np.float64)
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
    weights = []
    # Descending shell order is the deliberate independent replay choice.
    for index, prime in reversed(tuple(enumerate(primes))):
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
    need(bool(np.all(np.isfinite(geometry) & (geometry > 0))), "geometry")
    return primes, matrices, geometry, weights


def metric(matrix: np.ndarray) -> tuple[float, float, float, float]:
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
    blocks = count // BLOCK_LENGTH
    cutoff = 3 if mode == "fixed_c3" else blocks - 1
    ids = np.arange(count) // BLOCK_LENGTH
    return np.abs(ids[:, None] - ids[None, :]) <= cutoff, cutoff


def make_row(origin: int, count: int, q0: int, law: str, norm: str,
             mode: str, matrix: np.ndarray, geometry: np.ndarray,
             denominator: float, denominator_role: str,
             primes: list[int], weights: list[float], mask: np.ndarray,
             cutoff: int) -> dict[str, Any]:
    if norm == "local_diagonal":
        normalized = matrix / np.sqrt(geometry[:, None] * geometry[None, :])
    else:
        normalized = matrix / denominator
    spectral, schur, frobenius, symmetry = metric(np.where(mask, normalized, 0.0))
    return {
        "origin": origin, "origin_role":
            f"calibration_{count}" if origin in CALIBRATION_ORIGINS else "holdout_1536",
        "Q": q0, "law": law, "normalization": norm, "band_mode": mode,
        "effective_cutoff": cutoff, "count": count,
        "interval": [origin, origin + count], "block_length": BLOCK_LENGTH,
        "block_count": count // BLOCK_LENGTH, "kernel_exponent": EXPONENT,
        "beta": BETA, "height": HEIGHT, "shell_cardinality": len(primes),
        "weight_min": min(weights), "weight_max": max(weights),
        "geometry_min": float(np.min(geometry)),
        "geometry_max": float(np.max(geometry)),
        "geometry_mean": float(np.mean(geometry)),
        "pooled_scalar_used": denominator, "pooled_scalar_role": denominator_role,
        "band_spectral": spectral, "band_schur": schur,
        "band_frobenius": frobenius, "symmetry_error": symmetry,
        "spectral_failure": bool(spectral > SPECTRAL_CAP),
        "schur_failure": bool(schur > SCHUR_CAP),
    }


def replay_rows() -> list[dict[str, Any]]:
    rows = []
    for q0 in Q_ANCHORS:
        packs = {}
        for origin in CALIBRATION_ORIGINS:
            for count in CALIBRATION_COUNTS:
                packs[origin, count] = weighted_components(
                    np.arange(origin, origin + count, dtype=np.int64), q0)
        for origin in HOLDOUT_ORIGINS:
            packs[origin, HOLDOUT_COUNT] = weighted_components(
                np.arange(origin, origin + HOLDOUT_COUNT, dtype=np.int64), q0)
        train = {count: float(np.mean([packs[o, count][2].mean()
                                       for o in CALIBRATION_ORIGINS])
                              ) for count in CALIBRATION_COUNTS}
        gamma = math.log(train[1280] / train[1024]) / math.log(1280.0 / 1024.0)
        extrapolated = train[1280] * (1536.0 / 1280.0) ** gamma
        for (origin, count), (primes, matrices, geometry, weights) in packs.items():
            for mode in BAND_MODES:
                mask, cutoff = mask_for(mode, count)
                for norm in NORMALIZATIONS:
                    if norm == "local_diagonal":
                        denominator, role = 1.0, "local_diagonal"
                    elif count in train:
                        denominator, role = train[count], f"calibration_{count}"
                    else:
                        denominator, role = extrapolated, "calibration_extrapolated_1536"
                    for law in LAWS:
                        rows.append(make_row(origin, count, q0, law, norm, mode,
                                             matrices[law], geometry, denominator,
                                             role, primes, weights, mask, cutoff))
    need(len(rows) == 448, "replayed row census")
    return rows


def parent_cells() -> dict[tuple[str, str, str, int], dict[str, Any]]:
    raw = PARENT_CERT.read_bytes()
    need(digest(raw) == PARENT_CERT_SHA256, "parent hash")
    doc = parse_no_duplicates(raw)
    parent_payload = doc.get("payload", {})
    need(parent_payload.get("schema") ==
         "TPC390_C1_RECURSIVE_SLOPE_COMPOSITION_V1", "parent schema")
    cells = parent_payload.get("transfer_summary", {}).get("cells", [])
    result = {}
    for cell in cells:
        result[(cell["band_mode"], cell["normalization"], cell["law"],
               cell["Q"])] = cell
    need(len(result) == 32, "parent cells")
    return result


def finite_stats(values: list[float]) -> dict[str, Any]:
    need(len(values) in (2, 3) and
         all(math.isfinite(value) and value >= 0 for value in values),
         "finite stats")
    minimum, maximum = min(values), max(values)
    mean = sum(values) / len(values)
    relative = (maximum - minimum) / mean if mean else float("inf")
    return {
        "value_count": len(values), "minimum": minimum, "maximum": maximum,
        "mean": mean, "relative_spread": relative,
        "within_one_percent": bool(relative <= 0.01), "values": values,
    }


def check_summary_from_rows(rows: list[dict[str, Any]],
                            summary: dict[str, Any]) -> None:
    """Recompute the trajectory independently from the replayed rows."""
    parents = parent_cells()
    recorded_cells = summary.get("cells", [])
    need(len(recorded_cells) == 32, "recorded cell count")
    recorded_map = {}
    for cell in recorded_cells:
        key = (cell.get("band_mode"), cell.get("normalization"),
               cell.get("law"), cell.get("Q"))
        need(key not in recorded_map, "duplicate summary cell")
        recorded_map[key] = cell
    expected_keys = {(mode, norm, law, q0) for mode in BAND_MODES
                     for norm in NORMALIZATIONS for law in LAWS
                     for q0 in Q_ANCHORS}
    need(set(recorded_map) == expected_keys, "summary cell keys")
    parent_passes = {str(count): 0 for count in HORIZON_LEVELS}
    local_passes = {str(count): 0 for count in HORIZON_LEVELS}
    recursive_passes = {str(count): 0 for count in (1280, 1408, 1536)}
    parent_max = {str(count): 0.0 for count in HORIZON_LEVELS}
    local_max = {str(count): 0.0 for count in HORIZON_LEVELS}
    recursive_max = {str(count): 0.0 for count in (1280, 1408, 1536)}
    crossing_counts = {str(count): 0 for count in HORIZON_LEVELS}
    crossing_counts["NONE"] = 0
    local_crossing_counts = {str(count): 0 for count in HORIZON_LEVELS}
    local_crossing_counts["NONE"] = 0
    stable = {str(count): 0 for count in (1024, 1152, 1280, 1408)}
    stable["1536_holdout"] = 0
    failures = {f"{mode}_{norm}": {"spectral": 0, "schur": 0}
                for mode in BAND_MODES for norm in NORMALIZATIONS}
    composition_values = []

    for mode in BAND_MODES:
        for norm in NORMALIZATIONS:
            for law in LAWS:
                for q0 in Q_ANCHORS:
                    key = (mode, norm, law, q0)
                    selected = [row for row in rows
                                if (row["band_mode"], row["normalization"],
                                    row["law"], row["Q"]) == key]
                    selected.sort(key=lambda row: (row["count"],
                                                   row["origin"]))
                    by_count = {
                        count: [float(row["band_spectral"]) for row in selected
                                if row["count"] == count]
                        for count in COUNT_LEVELS
                    }
                    stats = {count: finite_stats(by_count[count])
                             for count in COUNT_LEVELS}
                    means = {count: stats[count]["mean"]
                             for count in COUNT_LEVELS}
                    parent_alpha = float(parents[key]["parent_horizon_log2_slope"])
                    local_alpha = math.log(means[1280] / means[1024]) / math.log(
                        1280.0 / 1024.0)
                    cell = recorded_map[key]
                    need(cell.get("origins") == [row["origin"] for row in selected],
                         "cell origin order")
                    need(cell.get("calibration_origins") == list(CALIBRATION_ORIGINS) and
                         cell.get("holdout_origins") == list(HOLDOUT_ORIGINS) and
                         cell.get("calibration_counts") == list(CALIBRATION_COUNTS) and
                         cell.get("holdout_count") == HOLDOUT_COUNT,
                         "cell roles")
                    for count in COUNT_LEVELS:
                        field = "N1536_holdout" if count == 1536 else f"N{count}"
                        stored = cell.get(field, {})
                        need(stored.get("value_count") == stats[count]["value_count"] and
                             stored.get("within_one_percent") ==
                             stats[count]["within_one_percent"],
                             field + " census")
                        for name in ("minimum", "maximum", "mean",
                                     "relative_spread"):
                            close(stats[count][name], stored.get(name),
                                  field + "." + name)
                        values = stored.get("values")
                        need(isinstance(values, list) and
                             len(values) == len(by_count[count]),
                             field + ".values")
                        for actual, target in zip(by_count[count], values):
                            close(actual, target, field + ".value")
                        if stats[count]["within_one_percent"]:
                            stable["1536_holdout" if count == 1536
                                   else str(count)] += 1

                    trajectory = cell.get("trajectory")
                    need(isinstance(trajectory, list) and
                         len(trajectory) == len(HORIZON_LEVELS),
                         "trajectory census")
                    first_parent = "NONE"
                    first_local = "NONE"
                    for index, count in enumerate(HORIZON_LEVELS):
                        item = trajectory[index]
                        mean = means[count]
                        parent_prediction = means[1024] * (
                            count / 1024.0) ** parent_alpha
                        local_prediction = means[1024] * (
                            count / 1024.0) ** local_alpha
                        parent_error = mean / parent_prediction - 1.0
                        local_error = mean / local_prediction - 1.0
                        for name, actual in (
                                ("count", count), ("mean", mean),
                                ("parent_prediction_from_N1024",
                                 parent_prediction),
                                ("local_prediction_from_N1024",
                                 local_prediction),
                                ("parent_error", parent_error),
                                ("local_error", local_error)):
                            if name == "count":
                                need(item.get(name) == actual, "trajectory count")
                            else:
                                close(actual, item.get(name),
                                      f"trajectory.{count}.{name}")
                        parent_ok = abs(parent_error) <= TRANSFER_ERROR_CAP
                        local_ok = abs(local_error) <= TRANSFER_ERROR_CAP
                        need(item.get("within_parent_cap") == parent_ok and
                             item.get("within_local_cap") == local_ok,
                             "trajectory pass flags")
                        if not parent_ok and first_parent == "NONE":
                            first_parent = count
                        if not local_ok and first_local == "NONE":
                            first_local = count
                        if parent_ok:
                            parent_passes[str(count)] += 1
                        if local_ok:
                            local_passes[str(count)] += 1
                        parent_max[str(count)] = max(
                            parent_max[str(count)], abs(parent_error))
                        local_max[str(count)] = max(
                            local_max[str(count)], abs(local_error))
                        if count < 1280:
                            for name in ("recursive_prediction_from_N1024",
                                         "direct_prediction_from_N1024",
                                         "recursive_error",
                                         "composition_error",
                                         "within_recursive_cap"):
                                need(item.get(name) == "NOT_DEFINED",
                                     f"trajectory.{count}.{name}")
                        else:
                            stage1 = means[1024] * (
                                1280.0 / 1024.0) ** parent_alpha
                            recursive_prediction = stage1 * (
                                count / 1280.0) ** parent_alpha
                            direct_prediction = means[1024] * (
                                count / 1024.0) ** parent_alpha
                            recursive_error = mean / recursive_prediction - 1.0
                            composition_error = (
                                recursive_prediction / direct_prediction - 1.0)
                            recursive_ok = abs(recursive_error) <= TRANSFER_ERROR_CAP
                            for name, actual in (
                                    ("recursive_prediction_from_N1024",
                                     recursive_prediction),
                                    ("direct_prediction_from_N1024",
                                     direct_prediction),
                                    ("recursive_error", recursive_error),
                                    ("composition_error", composition_error)):
                                close(actual, item.get(name),
                                      f"trajectory.{count}.{name}")
                            need(item.get("within_recursive_cap") == recursive_ok,
                                 "recursive pass flag")
                            if recursive_ok:
                                recursive_passes[str(count)] += 1
                            recursive_max[str(count)] = max(
                                recursive_max[str(count)], abs(recursive_error))
                            composition_values.append(abs(composition_error))
                    need(cell.get("first_parent_cap_crossing") == first_parent and
                         cell.get("first_local_cap_crossing") == first_local,
                         "first crossing")
                    crossing_counts[str(first_parent)] += 1
                    local_crossing_counts[str(first_local)] += 1
                    close(parent_alpha, cell.get("parent_horizon_log2_slope"),
                          "parent slope")
                    close(local_alpha, cell.get("local_horizon_log2_slope"),
                          "local slope")
                    close(max(abs(float(item["composition_error"]))
                               for item in trajectory
                               if item["composition_error"] != "NOT_DEFINED"),
                          cell.get("recursive_composition_max_abs_error"),
                          "cell composition maximum")
                    for row in selected:
                        bucket = failures[f"{mode}_{norm}"]
                        bucket["spectral"] += int(row["spectral_failure"])
                        bucket["schur"] += int(row["schur_failure"])

    need(summary.get("row_count") == 448 and summary.get("cell_count") == 32,
         "summary dimensions")
    need(summary.get("horizon_levels") == list(HORIZON_LEVELS) and
         summary.get("recursive_horizon_levels") == [1280, 1408, 1536],
         "summary horizons")
    need(summary.get("stable_cells") == stable, "stable census")
    need(summary.get("failure_counts_by_mode_normalization") == failures,
         "failure census replay")
    need(summary.get("parent_pass_counts_by_horizon") == parent_passes and
         summary.get("local_pass_counts_by_horizon") == local_passes and
         summary.get("recursive_pass_counts_by_horizon") == recursive_passes,
         "pass census replay")
    need(summary.get("first_parent_crossing_counts") == crossing_counts and
         summary.get("first_local_crossing_counts") == local_crossing_counts,
         "crossing census")
    for actual, stored, label in (
            (parent_max, summary.get("parent_max_abs_error_by_horizon"),
             "parent maxima"),
            (local_max, summary.get("local_max_abs_error_by_horizon"),
             "local maxima"),
            (recursive_max, summary.get("recursive_max_abs_error_by_horizon"),
             "recursive maxima")):
        need(set(actual) == set(stored or {}), label + " keys")
        for key, value in actual.items():
            close(value, (stored or {}).get(key), label + "." + key)
    close(max(composition_values),
          summary.get("recursive_composition_max_abs_error"),
          "composition maximum")


def check_document(document: dict[str, Any], recompute: bool = True) -> dict[str, Any]:
    need(finite_tree(document), "non-finite document")
    need(document.get("certificate_version") == 1 and
         document.get("claim_status") == STATUS, "header")
    payload = document.get("payload")
    need(isinstance(payload, dict) and payload.get("schema") == SCHEMA and
         payload.get("status") == STATUS, "payload header")
    need(document.get("payload_sha256") == hashlib.sha256(
        canonical(payload)).hexdigest(), "payload hash")
    parent = payload.get("parent_lock", {})
    need(parent.get("parent_schema") ==
         "TPC390_C1_RECURSIVE_SLOPE_COMPOSITION_V1" and
         parent.get("parent_certificate_sha256") == PARENT_CERT_SHA256 and
         parent.get("parent_slopes_frozen") is True and
         parent.get("parent_slopes_refit_on_current_family") is False,
         "parent lock")
    selection = payload.get("selection_protocol", {})
    need(selection.get("origins") == list(ORIGINS) and
         selection.get("calibration_origins") == list(CALIBRATION_ORIGINS) and
         selection.get("holdout_origins") == list(HOLDOUT_ORIGINS) and
         selection.get("calibration_counts") == list(CALIBRATION_COUNTS) and
         selection.get("holdout_count") == HOLDOUT_COUNT and
         selection.get("response_used_for_selection") is False and
         selection.get("parent_slope_refit") is False and
         selection.get("holdout_role_fixed_before_readout") is True,
         "selection")
    rows = payload.get("rows")
    need(isinstance(rows, list) and len(rows) == 448, "certificate rows")
    expected = {(o, n, q, law, norm, mode)
                for o in CALIBRATION_ORIGINS for n in CALIBRATION_COUNTS
                for q in Q_ANCHORS for law in LAWS for norm in NORMALIZATIONS
                for mode in BAND_MODES}
    expected |= {(o, HOLDOUT_COUNT, q, law, norm, mode)
                 for o in HOLDOUT_ORIGINS for q in Q_ANCHORS for law in LAWS
                 for norm in NORMALIZATIONS for mode in BAND_MODES}
    observed = {(r.get("origin"), r.get("count"), r.get("Q"), r.get("law"),
                 r.get("normalization"), r.get("band_mode")) for r in rows}
    need(observed == expected, "row keys")
    row_map = {(
        r["origin"], r["count"], r["Q"], r["law"], r["normalization"],
        r["band_mode"]): r for r in rows}
    for key, row in row_map.items():
        origin, count, q0, law, norm, mode = key
        role = (f"calibration_{count}" if origin in CALIBRATION_ORIGINS
                else "holdout_1536")
        need(row.get("origin_role") == role and
             isinstance(row.get("spectral_failure"), bool) and
             isinstance(row.get("schur_failure"), bool), "row role")
    if recompute:
        replayed = replay_rows()
        for fresh in replayed:
            key = (fresh["origin"], fresh["count"], fresh["Q"], fresh["law"],
                   fresh["normalization"], fresh["band_mode"])
            recorded = row_map[key]
            for field in ("origin", "count", "Q", "law", "normalization",
                          "band_mode", "effective_cutoff", "block_length",
                          "block_count", "kernel_exponent", "beta", "height",
                          "shell_cardinality", "pooled_scalar_role"):
                need(recorded.get(field) == fresh[field], field + " mismatch")
            for field in ("weight_min", "weight_max", "geometry_min",
                          "geometry_max", "geometry_mean", "pooled_scalar_used",
                          "band_spectral", "band_schur", "band_frobenius",
                          "symmetry_error"):
                close(fresh[field], recorded.get(field), field)
            need(recorded.get("spectral_failure") == fresh["spectral_failure"] and
                 recorded.get("schur_failure") == fresh["schur_failure"],
                 "failure flags")
    summary = payload.get("transfer_summary", {})
    check_summary_from_rows(rows, summary)
    finite_audit = payload.get("finite_audit", {})
    need(finite_audit.get("rows") == 448 and
         finite_audit.get("cell_count") == 32 and
         finite_audit.get("calibration_counts") == list(CALIBRATION_COUNTS) and
         finite_audit.get("holdout_count") == HOLDOUT_COUNT and
         finite_audit.get("parent_slope_frozen") is True and
         finite_audit.get("fixed_power_credit") == 0 and
         finite_audit.get("arithmetic_advance") == "NO",
         "finite audit")
    firewall = payload.get("claim_firewall", {})
    need(firewall.get("TPC391_ARITHMETIC_ADVANCE") == "NO" and
         firewall.get("TPC391_FIXED_POWER_CREDIT") == 0 and
         firewall.get("TPC391_FULL_GATE_B") == "OPEN" and
         firewall.get("TPC391_TWIN_PRIME_RESULT") == "NONE", "firewall")
    anchor = payload.get("exact_anchor", {})
    need(anchor.get("interval") == [3400001, 3400014] and
         anchor.get("Q") == 8 and anchor.get("shell") == [11, 13] and
         anchor.get("geometry_positive") is True, "anchor")
    return summary


def main() -> int:
    if sys.argv[1:] != ["--check"]:
        raise SystemExit("explicit --check is required")
    try:
        raw = CERTIFICATE.read_bytes()
        document = parse_no_duplicates(raw)
        need(raw == canonical(document), "noncanonical certificate")
        summary = check_document(document)
        print("TPC391_INDEPENDENT_CHECK=PASS rows=448 cells=32 "
              f"parent_pass_1536={summary['parent_pass_counts_by_horizon']['1536']}/32 "
              f"local_pass_1536={summary['local_pass_counts_by_horizon']['1536']}/32 "
              f"recursive_pass_1536={summary['recursive_pass_counts_by_horizon']['1536']}/32 "
              f"spectral_failures={sum(v['spectral'] for v in summary['failure_counts_by_mode_normalization'].values())} "
              f"stable_holdout={summary['stable_cells']['1536_holdout']}/32 "
              f"first_crossing_1536={summary['first_parent_crossing_counts']['1536']} "
              f"composition_max={summary['recursive_composition_max_abs_error']}")
        return 0
    except (Failure, OSError, ValueError, TypeError, KeyError,
            json.JSONDecodeError) as error:
        print("TPC391_INDEPENDENT_CHECK=FAIL " + str(error), file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
