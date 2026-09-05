#!/usr/bin/env python3
"""Independent reverse-shell replay for TPC-395.

The implementation is intentionally separate from the producer.  It validates
the TPC-394 parent baseline, rebuilds the new family in descending prime order,
and recomputes the cross-family and within-family aggregates.
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
PROJECT = ROOT / "papers/tpc-395-c1-origin-cross-family-holdout"
CERTIFICATE = PROJECT / "results/tpc395_certificate.json"
PARENT_CODE = ROOT / (
    "papers/tpc-394-c1-origin-uniformity-ladder/code/"
    "tpc394_c1_origin_uniformity_ladder.py")
PARENT_CERT = ROOT / (
    "papers/tpc-394-c1-origin-uniformity-ladder/results/"
    "tpc394_certificate.json")
PARENT_CODE_SHA256 = (
    "48b097109cd725b160fc52a40ae035c223fc7790d52c4afb561e664afcd2b5b6")
PARENT_CERT_SHA256 = (
    "03d5dc25ea4ff135e2b3a5693ba3b24865371babefc394c76662ce12b410b753")
SCHEMA = "TPC395_C1_ORIGIN_CROSS_FAMILY_HOLDOUT_V1"
STATUS = "NUMERICALLY_CERTIFIED_FINITE_C1_ORIGIN_CROSS_FAMILY_HOLDOUT_AUDIT"
ORIGINS = (5600001, 5603209, 5606417, 5609625, 5612833, 5616041)
CALIBRATION_ORIGINS = ORIGINS[:3]
HOLDOUT_ORIGINS = ORIGINS[3:]
WINDOW_COUNT = 1024
BLOCK_LENGTH = 128
Q_ANCHORS = (8192,)
LAWS = ("all_plus", "alternating_index")
NORMALIZATIONS = (
    "local_diagonal", "pooled_train_scalar", "origin_scalar",
    "frozen_train_1024_scalar")
SPECTRAL_CAP = 0.64
SCHUR_CAP = 0.83
ORIGIN_SPREAD_CAP = 0.01
CROSS_FAMILY_CAP = 0.03
WITHIN_FAMILY_TRANSFER_CAP = 0.03
EXPONENT = 1
BETA = 2
HEIGHT = 66
CELL_COUNT = 8
ROW_COUNT = 48


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


def row(origin: int, law: str, norm: str, matrix: np.ndarray,
        geometry: np.ndarray, denominator: float, scalar_role: str,
        primes: list[int], weights: list[float], mask: np.ndarray,
        base: tuple[float, float, float, float]) -> dict[str, Any]:
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
        "Q": 8192, "law": law, "normalization": norm,
        "band_mode": "fixed_c3", "effective_cutoff": 3,
        "count": WINDOW_COUNT, "interval": [origin, origin + WINDOW_COUNT],
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


def parent_baseline() -> dict[tuple[str, str, int], float]:
    need(PARENT_CODE.is_file() and
         digest(PARENT_CODE.read_bytes()) == PARENT_CODE_SHA256,
         "parent code hash")
    raw = PARENT_CERT.read_bytes()
    need(digest(raw) == PARENT_CERT_SHA256, "parent certificate hash")
    document = parse_no_duplicates(raw)
    need(raw == canonical(document), "parent canonicality")
    payload = document.get("payload", {})
    need(payload.get("schema") == "TPC394_C1_ORIGIN_UNIFORMITY_LADDER_V1" and
         payload.get("status") ==
         "NUMERICALLY_CERTIFIED_FINITE_C1_ORIGIN_UNIFORMITY_LADDER_AUDIT",
         "parent header")
    result = {}
    for cell in payload.get("origin_summary", {}).get("cells", []):
        key = (cell["normalization"], cell["law"], cell["Q"])
        need(key not in result, "duplicate parent baseline")
        result[key] = float(cell["all_origin_stats"]["mean"])
    need(set(result) == {(norm, law, 8192) for norm in NORMALIZATIONS
                         for law in LAWS}, "parent baseline census")
    return result


def replay_rows() -> list[dict[str, Any]]:
    rows = []
    baseline = parent_baseline()
    block_ids = np.arange(WINDOW_COUNT) // BLOCK_LENGTH
    mask = np.abs(block_ids[:, None] - block_ids[None, :]) <= 3
    packs = {
        origin: weighted_components(
            np.arange(origin, origin + WINDOW_COUNT, dtype=np.int64), 8192)
        for origin in ORIGINS}
    calibration_geometry = [float(packs[o][2].mean())
                            for o in CALIBRATION_ORIGINS]
    pooled = float(np.mean(calibration_geometry))
    frozen = calibration_geometry[0]
    for origin in ORIGINS:
        primes, matrices, geometry, weights = packs[origin]
        base = {law: metrics(np.where(mask, matrices[law], 0.0))
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
            for law in LAWS:
                rows.append(row(origin, law, norm, matrices[law], geometry,
                                denominator, scalar_role, primes, weights,
                                mask, base[law]))
    need(len(rows) == ROW_COUNT, "replayed row census")
    return rows


def stats(values: list[float]) -> dict[str, Any]:
    need(values and all(math.isfinite(x) and x >= 0 for x in values),
         "finite stats")
    minimum, maximum = min(values), max(values)
    mean = sum(values) / len(values)
    relative = (maximum - minimum) / mean if mean else float("inf")
    return {"value_count": len(values), "minimum": minimum,
            "maximum": maximum, "mean": mean,
            "absolute_spread": maximum - minimum,
            "relative_spread": relative,
            "within_one_percent": relative <= ORIGIN_SPREAD_CAP,
            "values": values}


def check_summary(rows: list[dict[str, Any]], summary: dict[str, Any]) -> None:
    need(summary.get("row_count") == ROW_COUNT and
         summary.get("cell_count") == CELL_COUNT and
         summary.get("normalizations") == list(NORMALIZATIONS) and
         summary.get("laws") == list(LAWS), "summary header")
    recorded = {}
    for cell in summary.get("cells", []):
        key = (cell.get("normalization"), cell.get("law"), cell.get("Q"))
        need(key not in recorded, "duplicate summary cell")
        recorded[key] = cell
    need(set(recorded) == {(norm, law, 8192) for norm in NORMALIZATIONS
                           for law in LAWS}, "summary keys")
    baseline = parent_baseline()
    counters = {name: {norm: 0 for norm in NORMALIZATIONS} for name in
                ("origin", "cal", "hold", "within")}
    maxes = {name: {norm: 0.0 for norm in NORMALIZATIONS} for name in
             ("spread", "cal_error", "hold_error", "within_error")}
    spectral = {norm: 0 for norm in NORMALIZATIONS}
    schur = {norm: 0 for norm in NORMALIZATIONS}
    for norm in NORMALIZATIONS:
        for law in LAWS:
            selected = [r for r in rows if r["normalization"] == norm and
                        r["law"] == law]
            selected.sort(key=lambda r: r["origin"])
            values = [float(r["band_spectral"]) for r in selected]
            cal = values[:3]
            hold = values[3:]
            all_s, cal_s, hold_s = map(stats, (values, cal, hold))
            parent = baseline[norm, law, 8192]
            cal_error = cal_s["mean"] / parent - 1.0
            hold_error = hold_s["mean"] / parent - 1.0
            within_error = hold_s["mean"] / cal_s["mean"] - 1.0
            cell = recorded[(norm, law, 8192)]
            need(cell.get("origins") == [r["origin"] for r in selected] and
                 cell.get("calibration_origins") == list(CALIBRATION_ORIGINS) and
                 cell.get("holdout_origins") == list(HOLDOUT_ORIGINS) and
                 cell.get("count") == WINDOW_COUNT and
                 cell.get("parent_family") == "TPC394", "cell protocol")
            for label, actual in (("all_origin_stats", all_s),
                                  ("calibration_stats", cal_s),
                                  ("holdout_stats", hold_s)):
                stored = cell.get(label, {})
                need(stored.get("value_count") == actual["value_count"] and
                     stored.get("within_one_percent") ==
                     actual["within_one_percent"], label + " flags")
                for name in ("minimum", "maximum", "mean", "absolute_spread",
                             "relative_spread"):
                    close(actual[name], stored.get(name), label + "." + name)
                for a, b in zip(actual["values"], stored.get("values", [])):
                    close(a, b, label + ".value")
            close(parent, cell.get("parent_family_mean"), "parent mean")
            close(cal_error, cell.get("calibration_cross_family_error"), "cal error")
            close(hold_error, cell.get("holdout_cross_family_error"), "hold error")
            close(within_error, cell.get("within_family_holdout_transfer_error"),
                  "within error")
            need(cell.get("within_cross_family_calibration_cap") ==
                 (abs(cal_error) <= CROSS_FAMILY_CAP) and
                 cell.get("within_cross_family_holdout_cap") ==
                 (abs(hold_error) <= CROSS_FAMILY_CAP) and
                 cell.get("within_family_holdout_transfer_cap") ==
                 (abs(within_error) <= WITHIN_FAMILY_TRANSFER_CAP),
                 "cell flags")
            expected_spectral = sum(bool(r["spectral_failure"]) for r in selected)
            expected_schur = sum(bool(r["schur_failure"]) for r in selected)
            need(cell.get("spectral_failures") == expected_spectral and
                 cell.get("schur_failures") == expected_schur,
                 "cell envelopes")
            if all_s["within_one_percent"]: counters["origin"][norm] += 1
            if abs(cal_error) <= CROSS_FAMILY_CAP: counters["cal"][norm] += 1
            if abs(hold_error) <= CROSS_FAMILY_CAP: counters["hold"][norm] += 1
            if abs(within_error) <= WITHIN_FAMILY_TRANSFER_CAP:
                counters["within"][norm] += 1
            maxes["spread"][norm] = max(maxes["spread"][norm],
                                         all_s["relative_spread"])
            maxes["cal_error"][norm] = max(maxes["cal_error"][norm], abs(cal_error))
            maxes["hold_error"][norm] = max(maxes["hold_error"][norm], abs(hold_error))
            maxes["within_error"][norm] = max(maxes["within_error"][norm],
                                               abs(within_error))
            spectral[norm] += expected_spectral
            schur[norm] += expected_schur
    need(summary.get("within_family_origin_pass_counts") == counters["origin"] and
         summary.get("cross_family_calibration_pass_counts") == counters["cal"] and
         summary.get("cross_family_holdout_pass_counts") == counters["hold"] and
         summary.get("within_family_transfer_pass_counts") == counters["within"],
         "summary counters")
    for name, field in (("spread", "maximum_within_family_origin_relative_spread"),
                        ("cal_error", "maximum_cross_family_calibration_abs_error"),
                        ("hold_error", "maximum_cross_family_holdout_abs_error"),
                        ("within_error", "maximum_within_family_transfer_abs_error")):
        stored = summary.get(field, {})
        for norm, value in maxes[name].items():
            close(value, stored.get(norm), field + "." + norm)
    need(summary.get("spectral_failures_by_normalization") == spectral and
         summary.get("schur_failures_by_normalization") == schur and
         summary.get("origin_stable_cells") == sum(counters["origin"].values()) and
         summary.get("cross_family_calibration_stable_cells") == sum(counters["cal"].values()) and
         summary.get("cross_family_holdout_stable_cells") == sum(counters["hold"].values()) and
         summary.get("within_family_transfer_stable_cells") == sum(counters["within"].values()),
         "summary totals")


def check_document(document: dict[str, Any], recompute: bool = True) -> None:
    need(finite_tree(document), "non-finite document")
    need(document.get("certificate_version") == 1 and
         document.get("claim_status") == STATUS, "document header")
    payload = document.get("payload")
    need(isinstance(payload, dict) and payload.get("schema") == SCHEMA and
         payload.get("status") == STATUS, "payload header")
    need(document.get("payload_sha256") == hashlib.sha256(
        canonical(payload)).hexdigest(), "payload hash")
    lock = payload.get("parent_lock", {})
    need(lock.get("parent_code_sha256") == PARENT_CODE_SHA256 and
         lock.get("parent_certificate_sha256") == PARENT_CERT_SHA256 and
         lock.get("parent_schema") == "TPC394_C1_ORIGIN_UNIFORMITY_LADDER_V1" and
         lock.get("parent_interface_frozen") is True and
         lock.get("parent_interface_used_for_current_fit") is False and
         lock.get("parent_means_used_as_response_blind_baseline") is True,
         "parent lock")
    selection = payload.get("selection_protocol", {})
    need(selection.get("origins") == list(ORIGINS) and
         selection.get("calibration_origins") == list(CALIBRATION_ORIGINS) and
         selection.get("holdout_origins") == list(HOLDOUT_ORIGINS) and
         selection.get("window_count") == WINDOW_COUNT and
         selection.get("q_anchors") == [8192] and
         selection.get("laws") == list(LAWS) and
         selection.get("normalizations") == list(NORMALIZATIONS) and
         selection.get("response_used_for_selection") is False and
         selection.get("metric_used_for_selection") is False and
         selection.get("parent_means_frozen_before_current_readout") is True and
         selection.get("holdout_role_fixed_before_readout") is True,
         "selection")
    rows = payload.get("rows")
    need(isinstance(rows, list) and len(rows) == ROW_COUNT and
         payload.get("row_digest") == hashlib.sha256(canonical(rows)).hexdigest(),
         "rows")
    need({(r.get("origin"), r.get("law"), r.get("normalization")) for r in rows} ==
         {(o, law, norm) for o in ORIGINS for law in LAWS for norm in NORMALIZATIONS},
         "row keys")
    firewall = payload.get("claim_firewall", {})
    need(firewall.get("TPC395_ARITHMETIC_ADVANCE") == "NO" and
         firewall.get("TPC395_FIXED_POWER_CREDIT") == 0 and
         firewall.get("TPC395_FULL_GATE_B") == "OPEN" and
         firewall.get("TPC395_TWIN_PRIME_RESULT") == "NONE" and
         firewall.get("TPC395_CROSS_FAMILY_PANEL") ==
         "NUMERICALLY_CERTIFIED_FINITE_48_ROWS", "firewall")
    need(payload.get("round2_clue") == "TEST_C1_SIGNED_LAW_INTERPOLATION",
         "clue")
    anchor = payload.get("exact_anchor", {})
    need(anchor.get("interval") == [5600001, 5600014] and
         anchor.get("Q") == 8 and anchor.get("shell") == [11, 13] and
         anchor.get("geometry_positive") is True, "anchor")
    audit = payload.get("finite_audit", {})
    need(audit.get("rows") == ROW_COUNT and audit.get("cell_count") == CELL_COUNT and
         audit.get("complete_cartesian_panel") is True and
         audit.get("coordinate_disjoint_from_prior") is True and
         audit.get("parent_baseline_frozen") is True and
         audit.get("fixed_power_credit") == 0 and
         audit.get("arithmetic_advance") == "NO", "audit")
    if recompute:
        replayed = replay_rows()
        # Compare the full finite row contract after normalizing numeric strings.
        exact = ("origin", "origin_role", "Q", "law", "normalization",
                 "band_mode", "effective_cutoff", "count", "interval",
                 "block_length", "block_count", "kernel_exponent", "beta",
                 "height", "shell_cardinality", "pooled_scalar_role")
        numeric = ("weight_min", "weight_max", "geometry_min", "geometry_max",
                   "geometry_mean", "pooled_scalar_used", "band_spectral",
                   "band_schur", "band_frobenius", "symmetry_error")
        for i, (stored, actual) in enumerate(zip(rows, replayed)):
            for key in exact:
                need(stored.get(key) == actual[key], f"row {i} {key}")
            for key in numeric:
                close(actual[key], stored.get(key), f"row {i} {key}")
            for key in ("spectral_failure", "schur_failure"):
                need(stored.get(key) is actual[key], f"row {i} {key}")
        check_summary(replayed, payload.get("origin_summary", {}))


def main() -> int:
    if sys.argv[1:] != ["--check"]:
        raise SystemExit("explicit --check is required")
    try:
        document = parse_no_duplicates(CERTIFICATE.read_bytes())
        check_document(document, recompute=True)
        summary = document["payload"]["origin_summary"]
        spectral = sum(summary["spectral_failures_by_normalization"].values())
        schur = sum(summary["schur_failures_by_normalization"].values())
        print(f"TPC395_INDEPENDENT_CHECK=PASS rows={ROW_COUNT} cells={CELL_COUNT} "
              f"origin_passes={summary['within_family_origin_pass_counts']} "
              f"cross_holdout={summary['cross_family_holdout_pass_counts']} "
              f"transfer_passes={summary['within_family_transfer_pass_counts']} "
              f"spectral_failures={spectral} schur_failures={schur}")
        return 0
    except (Failure, OSError, ValueError, TypeError, KeyError,
            json.JSONDecodeError) as error:
        print("TPC395_INDEPENDENT_CHECK=FAIL " + str(error), file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
