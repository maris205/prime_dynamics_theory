#!/usr/bin/env python3
"""Independent descending-shell checker for TPC-394.

The checker deliberately does not import the producer.  It reconstructs the
finite matrices in reverse prime-shell order, then verifies the canonical
certificate, row census, origin-spread aggregates, parent locks, and claim
firewall.  Its finite tolerances only account for floating-point summation
order; they do not widen any mathematical cap.
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
PROJECT = ROOT / "papers/tpc-394-c1-origin-uniformity-ladder"
CERTIFICATE = PROJECT / "results/tpc394_certificate.json"
PARENT_CERT = ROOT / (
    "papers/tpc-393-c1-normalization-adversarial-holdout/results/"
    "tpc393_certificate.json")

SCHEMA = "TPC394_C1_ORIGIN_UNIFORMITY_LADDER_V1"
STATUS = "NUMERICALLY_CERTIFIED_FINITE_C1_ORIGIN_UNIFORMITY_LADDER_AUDIT"
PARENT_CODE_SHA256 = (
    "73ee391f0d4f467ee6fefdc57a1bb42dea93f01df2e2b22e35054b7a95cc6229")
PARENT_CERT_SHA256 = (
    "b983f4bae7836df57a8654fe51c37e72e28e1c0ca013aaaff71c9bdf79a229f1")
ORIGINS = (5000001, 5002006, 5004011, 5006016,
           5008021, 5010026, 5012031, 5014036)
CALIBRATION_ORIGINS = ORIGINS[:5]
HOLDOUT_ORIGINS = ORIGINS[5:]
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
CELL_COUNT = 8
ROW_COUNT = 64


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
        result = {}
        for key, value in pairs:
            if key in result:
                raise Failure("duplicate JSON key")
            result[key] = value
        return result
    value = json.loads(raw, object_pairs_hook=hook)
    need(isinstance(value, dict), "document object")
    return value


def close(actual: float, recorded: Any, label: str,
          tolerance: float = 8.0e-8) -> None:
    try:
        target = float(recorded)
    except (TypeError, ValueError) as error:
        raise Failure(label + " is not numeric") from error
    need(math.isfinite(actual) and math.isfinite(target) and
         abs(actual - target) <= tolerance * max(1.0, abs(actual), abs(target)),
         label + " mismatch")


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
            [1.0 if i % 2 == 0 else -1.0 for i in range(len(primes))],
            dtype=np.float64),
    }


def weighted_components(values: np.ndarray, q0: int) -> tuple[Any, ...]:
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
    weights = []
    # Reverse order is independent of the ascending producer.
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


def make_row(origin: int, q0: int, law: str, norm: str,
             matrix: np.ndarray, geometry: np.ndarray, denominator: float,
             scalar_role: str, primes: list[int], weights: list[float],
             mask: np.ndarray, base: tuple[float, float, float, float]) -> dict[str, Any]:
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
        "Q": q0, "law": law,
        "normalization": norm, "band_mode": "fixed_c3",
        "effective_cutoff": 3, "count": WINDOW_COUNT,
        "interval": [origin, origin + WINDOW_COUNT],
        "block_length": BLOCK_LENGTH, "block_count": 8,
        "kernel_exponent": EXPONENT, "beta": BETA, "height": HEIGHT,
        "shell_cardinality": len(primes), "weight_min": min(weights),
        "weight_max": max(weights), "geometry_min": float(np.min(geometry)),
        "geometry_max": float(np.max(geometry)),
        "geometry_mean": float(np.mean(geometry)),
        "pooled_scalar_used": denominator, "pooled_scalar_role": scalar_role,
        "band_spectral": spectral, "band_schur": schur,
        "band_frobenius": frobenius, "symmetry_error": symmetry,
        "spectral_failure": bool(spectral > SPECTRAL_CAP),
        "schur_failure": bool(schur > SCHUR_CAP),
    }


def replay_rows() -> list[dict[str, Any]]:
    rows = []
    for q0 in Q_ANCHORS:
        packs = {}
        for origin in ORIGINS:
            packs[origin] = weighted_components(
                np.arange(origin, origin + WINDOW_COUNT, dtype=np.int64), q0)
        pooled = float(np.mean([packs[o][2].mean() for o in CALIBRATION_ORIGINS]))
        frozen = float(packs[CALIBRATION_ORIGINS[0]][2].mean())
        mask = np.abs((np.arange(WINDOW_COUNT) // BLOCK_LENGTH)[:, None] -
                     (np.arange(WINDOW_COUNT) // BLOCK_LENGTH)[None, :]) <= 3
        for origin in ORIGINS:
            primes, matrices, geometry, weights = packs[origin]
            base_metrics = {law: metrics(np.where(mask, matrices[law], 0.0))
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
                    raise Failure("unknown normalization")
                role = ("calibration_1024" if origin in CALIBRATION_ORIGINS
                        else "holdout_1024")
                for law in LAWS:
                    rows.append(make_row(
                        origin, Q_ANCHORS[0], law, norm, matrices[law], geometry,
                        denominator, scalar_role, primes, weights, mask,
                        base_metrics[law]))
    need(len(rows) == ROW_COUNT, "replayed row census")
    return rows


def finite_stats(values: list[float]) -> dict[str, Any]:
    need(len(values) > 0 and all(math.isfinite(x) and x >= 0 for x in values),
         "finite stats")
    minimum, maximum = min(values), max(values)
    mean = sum(values) / len(values)
    relative = (maximum - minimum) / mean if mean else float("inf")
    return {
        "value_count": len(values), "minimum": minimum, "maximum": maximum,
        "mean": mean, "absolute_spread": maximum - minimum,
        "relative_spread": relative, "within_one_percent": relative <= 0.01,
        "values": values,
    }


def check_rows(recorded: list[dict[str, Any]], replayed: list[dict[str, Any]]) -> None:
    need(len(recorded) == len(replayed) == ROW_COUNT, "row count")
    exact = ("origin", "origin_role", "Q", "law", "normalization",
             "band_mode", "effective_cutoff", "count", "interval",
             "block_length", "block_count", "kernel_exponent", "beta",
             "height", "shell_cardinality", "pooled_scalar_role")
    numeric = ("weight_min", "weight_max", "geometry_min", "geometry_max",
               "geometry_mean", "pooled_scalar_used", "band_spectral",
               "band_schur", "band_frobenius", "symmetry_error")
    booleans = ("spectral_failure", "schur_failure")
    for index, (stored, actual) in enumerate(zip(recorded, replayed)):
        for key in exact:
            need(stored.get(key) == actual[key], f"row {index} {key}")
        for key in numeric:
            close(actual[key], stored.get(key), f"row {index} {key}")
        for key in booleans:
            need(stored.get(key) is actual[key], f"row {index} {key}")


def check_summary(rows: list[dict[str, Any]], summary: dict[str, Any]) -> None:
    need(summary.get("row_count") == ROW_COUNT and
         summary.get("cell_count") == CELL_COUNT and
         summary.get("normalizations") == list(NORMALIZATIONS) and
         summary.get("laws") == list(LAWS), "summary dimensions")
    need(summary.get("origin_count") == 8 and
         summary.get("calibration_origin_count") == 5 and
         summary.get("holdout_origin_count") == 3, "summary roles")
    recorded_cells = summary.get("cells")
    need(isinstance(recorded_cells, list) and len(recorded_cells) == CELL_COUNT,
         "summary cells")
    recorded_map = {}
    for cell in recorded_cells:
        key = (cell.get("normalization"), cell.get("law"), cell.get("Q"))
        need(key not in recorded_map, "duplicate summary cell")
        recorded_map[key] = cell
    expected_keys = {(norm, law, Q_ANCHORS[0]) for norm in NORMALIZATIONS
                     for law in LAWS}
    need(set(recorded_map) == expected_keys, "summary keys")
    expected_origin_pass = {norm: 0 for norm in NORMALIZATIONS}
    expected_cal_pass = {norm: 0 for norm in NORMALIZATIONS}
    expected_hold_pass = {norm: 0 for norm in NORMALIZATIONS}
    expected_transfer_pass = {norm: 0 for norm in NORMALIZATIONS}
    expected_max_spread = {norm: 0.0 for norm in NORMALIZATIONS}
    expected_max_transfer = {norm: 0.0 for norm in NORMALIZATIONS}
    expected_spectral = {norm: 0 for norm in NORMALIZATIONS}
    expected_schur = {norm: 0 for norm in NORMALIZATIONS}
    expected_terminal = {norm: [] for norm in NORMALIZATIONS}
    expected_law_means = {}
    for norm in NORMALIZATIONS:
        for law in LAWS:
            selected = [r for r in rows if r["normalization"] == norm and
                        r["law"] == law and r["Q"] == Q_ANCHORS[0]]
            selected.sort(key=lambda r: r["origin"])
            need(len(selected) == 8, "summary row selection")
            values = [float(r["band_spectral"]) for r in selected]
            calibration = [float(r["band_spectral"]) for r in selected[:5]]
            holdout = [float(r["band_spectral"]) for r in selected[5:]]
            all_stats, cal_stats, hold_stats = map(
                finite_stats, (values, calibration, holdout))
            cal_mean, hold_mean = cal_stats["mean"], hold_stats["mean"]
            transfer = hold_mean / cal_mean - 1.0
            cell = recorded_map[(norm, law, Q_ANCHORS[0])]
            need(cell.get("band_mode") == "fixed_c3" and
                 cell.get("normalization_definition") in {
                     "entrywise division by sqrt(G(u)G(v))",
                     "mean geometry over five calibration origins",
                     "current-origin mean geometry",
                     "first calibration-origin mean geometry, frozen across origins",
                 } and cell.get("origins") == [r["origin"] for r in selected] and
                 cell.get("calibration_origins") == list(CALIBRATION_ORIGINS) and
                 cell.get("holdout_origins") == list(HOLDOUT_ORIGINS) and
                 cell.get("count") == WINDOW_COUNT, "cell protocol")
            for label, actual in (("all_origin_stats", all_stats),
                                  ("calibration_stats", cal_stats),
                                  ("holdout_stats", hold_stats)):
                stored = cell.get(label, {})
                need(stored.get("value_count") == actual["value_count"] and
                     stored.get("within_one_percent") ==
                     actual["within_one_percent"], label + " flags")
                for name in ("minimum", "maximum", "mean", "absolute_spread",
                             "relative_spread"):
                    close(actual[name], stored.get(name), label + "." + name)
                stored_values = stored.get("values")
                need(isinstance(stored_values, list) and
                     len(stored_values) == len(actual["values"]), label + " values")
                for j, value in enumerate(actual["values"]):
                    close(value, stored_values[j], f"{label}.value.{j}")
            close(hold_mean / cal_mean, cell.get("holdout_to_calibration_ratio"),
                  "holdout ratio")
            close(transfer, cell.get("holdout_transfer_error"), "transfer error")
            need(cell.get("within_holdout_transfer_cap") ==
                 (abs(transfer) <= HOLDOUT_TRANSFER_CAP), "transfer flag")
            need(cell.get("spectral_failures") ==
                 sum(bool(r["spectral_failure"]) for r in selected) and
                 cell.get("schur_failures") ==
                 sum(bool(r["schur_failure"]) for r in selected),
                 "cell failure counts")
            if all_stats["within_one_percent"]:
                expected_origin_pass[norm] += 1
            if cal_stats["within_one_percent"]:
                expected_cal_pass[norm] += 1
            if hold_stats["within_one_percent"]:
                expected_hold_pass[norm] += 1
            if abs(transfer) <= HOLDOUT_TRANSFER_CAP:
                expected_transfer_pass[norm] += 1
            expected_max_spread[norm] = max(expected_max_spread[norm],
                                            all_stats["relative_spread"])
            expected_max_transfer[norm] = max(expected_max_transfer[norm],
                                              abs(transfer))
            expected_spectral[norm] += sum(bool(r["spectral_failure"])
                                           for r in selected)
            expected_schur[norm] += sum(bool(r["schur_failure"])
                                        for r in selected)
            expected_terminal[norm].append(all_stats["mean"])
            expected_law_means[norm, law] = all_stats["mean"]
    need(summary.get("origin_uniformity_pass_counts") == expected_origin_pass,
         "origin pass census")
    need(summary.get("calibration_uniformity_pass_counts") == expected_cal_pass,
         "calibration pass census")
    need(summary.get("holdout_uniformity_pass_counts") == expected_hold_pass,
         "holdout pass census")
    need(summary.get("holdout_transfer_pass_counts") == expected_transfer_pass,
         "transfer pass census")
    for actual, stored, label in (
            (expected_max_spread, summary.get("maximum_all_origin_relative_spread"),
             "spread maxima"),
            (expected_max_transfer, summary.get("maximum_holdout_transfer_abs_error"),
             "transfer maxima"),
    ):
        need(set(actual) == set(stored or {}), label + " keys")
        for key, value in actual.items():
            close(value, (stored or {}).get(key), label + "." + key)
    need(summary.get("spectral_failures_by_normalization") == expected_spectral and
         summary.get("schur_failures_by_normalization") == expected_schur,
         "failure census")
    expected_terminal_strings = {
        norm: format(float(np.mean(values)), ".17g")
        for norm, values in expected_terminal.items()}
    for norm, value in expected_terminal_strings.items():
        close(float(value), summary.get("terminal_mean_by_normalization", {}).get(norm),
              "terminal mean " + norm)
    expected_ratio = {
        norm: expected_law_means[norm, "alternating_index"] /
        expected_law_means[norm, "all_plus"] for norm in NORMALIZATIONS}
    for norm, value in expected_ratio.items():
        close(value, summary.get("alternating_to_all_plus_mean_ratio", {}).get(norm),
              "law ratio " + norm)
    need(summary.get("origin_uniformity_stable_cells") == sum(expected_origin_pass.values()) and
         summary.get("holdout_transfer_stable_cells") == sum(expected_transfer_pass.values()),
         "stable totals")


def check_document(document: dict[str, Any], recompute: bool = True) -> None:
    need(finite_tree(document), "non-finite document")
    need(document.get("certificate_version") == 1 and
         document.get("claim_status") == STATUS, "document header")
    payload = document.get("payload")
    need(isinstance(payload, dict) and payload.get("schema") == SCHEMA and
         payload.get("status") == STATUS, "payload header")
    need(document.get("payload_sha256") == hashlib.sha256(
        canonical(payload)).hexdigest(), "payload hash")
    parent = payload.get("parent_lock", {})
    need(parent.get("parent_code_sha256") == PARENT_CODE_SHA256 and
         parent.get("parent_certificate_sha256") == PARENT_CERT_SHA256 and
         parent.get("parent_schema") ==
         "TPC393_C1_NORMALIZATION_ADVERSARIAL_HOLDOUT_V1" and
         parent.get("parent_status") ==
         "NUMERICALLY_CERTIFIED_FINITE_C1_NORMALIZATION_ADVERSARIAL_HOLDOUT_AUDIT" and
         parent.get("parent_interface_frozen") is True and
         parent.get("parent_interface_used_for_current_fit") is False,
         "parent lock")
    selection = payload.get("selection_protocol", {})
    need(selection.get("origins") == list(ORIGINS) and
         selection.get("calibration_origins") == list(CALIBRATION_ORIGINS) and
         selection.get("holdout_origins") == list(HOLDOUT_ORIGINS) and
         selection.get("window_count") == WINDOW_COUNT and
         selection.get("band_modes") == ["fixed_c3"] and
         selection.get("q_anchors") == [8192] and
         selection.get("laws") == list(LAWS) and
         selection.get("normalizations") == list(NORMALIZATIONS) and
         selection.get("response_used_for_selection") is False and
         selection.get("metric_used_for_selection") is False and
         selection.get("holdout_role_fixed_before_readout") is True and
         selection.get("parent_interface_used_for_current_fit") is False,
         "selection protocol")
    rows = payload.get("rows")
    need(isinstance(rows, list) and len(rows) == ROW_COUNT and
         payload.get("row_digest") == hashlib.sha256(canonical(rows)).hexdigest(),
         "row census")
    seen = set()
    for row in rows:
        key = (row.get("origin"), row.get("Q"), row.get("law"),
               row.get("normalization"))
        need(key not in seen, "duplicate row key")
        seen.add(key)
        need(row.get("origin") in ORIGINS and row.get("Q") == 8192 and
             row.get("law") in LAWS and row.get("normalization") in NORMALIZATIONS,
             "row key")
        for name in ("band_spectral", "band_schur", "band_frobenius",
                     "geometry_mean", "pooled_scalar_used"):
            value = float(row[name])
            need(math.isfinite(value) and value >= 0, "finite row metric")
    need(seen == {(o, 8192, law, norm) for o in ORIGINS for law in LAWS
                 for norm in NORMALIZATIONS}, "complete row keys")
    summary = payload.get("origin_summary")
    need(isinstance(summary, dict), "summary object")
    firewall = payload.get("claim_firewall", {})
    need(firewall.get("TPC394_ARITHMETIC_ADVANCE") == "NO" and
         firewall.get("TPC394_FIXED_POWER_CREDIT") == 0 and
         firewall.get("TPC394_FULL_GATE_B") == "OPEN" and
         firewall.get("TPC394_TWIN_PRIME_RESULT") == "NONE" and
         firewall.get("TPC394_ORIGIN_LADDER_PANEL") ==
         "NUMERICALLY_CERTIFIED_FINITE_64_ROWS", "claim firewall")
    need(payload.get("round2_clue") ==
         "TEST_C1_ORIGIN_CROSS_FAMILY_HOLDOUT", "round2 clue")
    anchor = payload.get("exact_anchor", {})
    need(anchor.get("interval") == [5000001, 5000014] and
         anchor.get("Q") == 8 and anchor.get("shell") == [11, 13] and
         anchor.get("geometry_positive") is True and
         anchor.get("matrix_symmetric_by_law") ==
         {law: True for law in LAWS}, "exact anchor")
    audit = payload.get("finite_audit", {})
    need(audit.get("rows") == ROW_COUNT and audit.get("cell_count") == CELL_COUNT and
         audit.get("complete_cartesian_panel") is True and
         audit.get("coordinate_disjoint_from_prior") is True and
         audit.get("same_count_across_all_origins") is True and
         audit.get("fixed_power_credit") == 0 and
         audit.get("arithmetic_advance") == "NO", "finite audit")
    if recompute:
        replayed = replay_rows()
        check_rows(rows, replayed)
        check_summary(replayed, summary)


def main() -> int:
    if sys.argv[1:] != ["--check"]:
        raise SystemExit("explicit --check is required")
    try:
        document = parse_no_duplicates(CERTIFICATE.read_bytes())
        check_document(document, recompute=True)
        summary = document["payload"]["origin_summary"]
        spectral = sum(summary["spectral_failures_by_normalization"].values())
        schur = sum(summary["schur_failures_by_normalization"].values())
        print(f"TPC394_INDEPENDENT_CHECK=PASS rows={ROW_COUNT} cells={CELL_COUNT} "
              f"origin_passes={summary['origin_uniformity_pass_counts']} "
              f"transfer_passes={summary['holdout_transfer_pass_counts']} "
              f"spectral_failures={spectral} schur_failures={schur}")
        return 0
    except (Failure, OSError, ValueError, TypeError, KeyError,
            json.JSONDecodeError) as error:
        print("TPC394_INDEPENDENT_CHECK=FAIL " + str(error), file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
