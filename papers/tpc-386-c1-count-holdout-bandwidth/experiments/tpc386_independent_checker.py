#!/usr/bin/env python3
"""Independent reverse-order replay for the TPC-386 certificate."""

from __future__ import annotations

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

ROOT = Path(__file__).resolve().parents[3]
PROJECT = ROOT / "papers/tpc-386-c1-count-holdout-bandwidth"
CERTIFICATE = PROJECT / "results/tpc386_certificate.json"
PARENT_CODE = ROOT / (
    "papers/tpc-385-c1-bandwidth-origin-holdout/code/"
    "tpc385_c1_bandwidth_origin_holdout.py")
PARENT_CERT = ROOT / (
    "papers/tpc-385-c1-bandwidth-origin-holdout/results/"
    "tpc385_certificate.json")
PARENT_CODE_SHA256 = "68825812bfffd90733472103fd4de200adb7b81ed3d02b57f992cc8d0d21e4b0"
PARENT_CERT_SHA256 = "ecac4403e2f803fd36c764509f2cd7cbb385e8c45aa5bba103f5b734341f391e"
CERTIFICATE_SHA256 = "4f34aee5970006efce06586c90ad599a7b484fdb9fea3921ffcfab7560d2a285"
SCHEMA = "TPC386_C1_COUNT_HOLDOUT_BANDWIDTH_V1"
STATUS = "NUMERICALLY_CERTIFIED_FINITE_C1_COUNT_HOLDOUT_BANDWIDTH"
ROUND2_CLUE = "TEST_C1_COUNT_LADDER_RENORMALIZATION"
ORIGINS = (2200001, 2204011, 2208021, 2212031, 2216041)
CALIBRATION_ORIGINS = (2200001, 2204011, 2208021)
HOLDOUT_ORIGINS = (2212031, 2216041)
COUNTS = {origin: (512 if origin in CALIBRATION_ORIGINS else 1024)
          for origin in ORIGINS}
BLOCK_LENGTH = 128
BAND_MODES = ("fixed_c3", "full_relative")
QS = (2048, 8192)
EXPONENT = 1
BETA = 2
HEIGHT = 66
LAWS = ("all_plus", "alternating_index", "mod4_character", "half_split")
NORMS = ("local_diagonal", "pooled_train_scalar")
SPREAD_CAP = 0.01
SPECTRAL_CAP = 0.64
SCHUR_CAP = 0.83
COUNT_TRANSFER_CAP = 0.20
PARENT_FORECAST = {
    "local_diagonal": 0.62079971051100025,
    "pooled_train_scalar": 0.63888760360944985,
}


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


def close(actual: float, recorded: Any, label: str,
          tolerance: float = 8e-8) -> None:
    try:
        target = float(recorded)
    except (TypeError, ValueError) as error:
        raise Failure(label + " nonnumeric") from error
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


def sign(law: str, index: int, prime: int, cardinality: int) -> float:
    if law == "all_plus":
        return 1.0
    if law == "alternating_index":
        return 1.0 if index % 2 == 0 else -1.0
    if law == "mod4_character":
        return 1.0 if prime % 4 == 1 else -1.0
    return 1.0 if index < cardinality / 2 else -1.0


def pack(origin: int, q0: int):
    count = COUNTS[origin]
    values = np.arange(origin, origin + count, dtype=np.int64)
    difference = values[:, None] - values[None, :]
    kernel = float(HEIGHT * HEIGHT) / (
        HEIGHT * HEIGHT + difference.astype(np.float64) ** 2)
    np.fill_diagonal(kernel, 0.0)
    primes = shell(q0)
    matrices = {law: np.zeros((count, count), dtype=np.float64)
                for law in LAWS}
    geometry = np.zeros(count, dtype=np.float64)
    # Reverse shell order is intentional: it is an independent summation path.
    for index, p in reversed(tuple(enumerate(primes))):
        centered = ((difference % p == 0).astype(np.float64) - 1.0 / (p - 1))
        np.fill_diagonal(centered, 0.0)
        valid = ((difference != 0) & (values[:, None] % p != 0) &
                 (values[None, :] % p != 0))
        block = (float(p) / float(q0)) ** BETA * float(p) * kernel * centered * valid
        geometry += np.sum(block * block, axis=1)
        for law in LAWS:
            matrices[law] += sign(law, index, p, len(primes)) * block
    for law in LAWS:
        matrices[law] = (matrices[law] + matrices[law].T) / 2.0
    need(bool(np.all(np.isfinite(geometry) & (geometry > 0))), "geometry")
    return primes, matrices, geometry


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


def mask(mode: str, count: int) -> tuple[np.ndarray, int]:
    blocks = count // BLOCK_LENGTH
    cutoff = 3 if mode == "fixed_c3" else blocks - 1
    ids = np.arange(count) // BLOCK_LENGTH
    return np.abs(ids[:, None] - ids[None, :]) <= cutoff, cutoff


def replay() -> tuple[dict[tuple[int, int, str, str, str], tuple[float, ...]],
                       dict[int, float]]:
    values: dict[tuple[int, int, str, str, str], tuple[float, ...]] = {}
    pooled: dict[int, float] = {}
    for q0 in QS:
        packs = [(origin, pack(origin, q0)) for origin in ORIGINS]
        pooled[q0] = float(np.mean([float(item[1][2].mean()) for item in packs
                                    if item[0] in CALIBRATION_ORIGINS]))
        for origin, (primes, matrices, geometry) in packs:
            count = COUNTS[origin]
            for mode in BAND_MODES:
                band, _ = mask(mode, count)
                for norm in NORMS:
                    for law in LAWS:
                        normalized = (matrices[law] /
                                      np.sqrt(geometry[:, None] * geometry[None, :])
                                      if norm == "local_diagonal" else
                                      matrices[law] / pooled[q0])
                        spectral, schur, frob, symmetry = metric(
                            np.where(band, normalized, 0.0))
                        values[(origin, q0, law, norm, mode)] = (
                            spectral, schur, frob, symmetry)
    need(len(values) == 160, "replay row count")
    return values, pooled


def stat(values: list[float]) -> dict[str, Any]:
    need(len(values) >= 2 and all(math.isfinite(x) and x >= 0 for x in values),
         "stat values")
    lo, hi = min(values), max(values)
    mean = sum(values) / len(values)
    spread = (hi - lo) / mean if mean else float("inf")
    return {"value_count": len(values), "minimum": lo, "maximum": hi,
            "mean": mean, "relative_spread": spread,
            "within_one_percent": spread <= SPREAD_CAP, "values": values}


def expected_cells(actual: dict[tuple[int, int, str, str, str], tuple[float, ...]]):
    cells = []
    for mode in BAND_MODES:
        for norm in NORMS:
            for law in LAWS:
                for q in QS:
                    selected = [(o, actual[(o, q, law, norm, mode)][0])
                                for o in ORIGINS]
                    all_values = [v for _, v in selected]
                    cal_values = [v for o, v in selected
                                  if o in CALIBRATION_ORIGINS]
                    hold_values = [v for o, v in selected
                                   if o in HOLDOUT_ORIGINS]
                    cal_mean = sum(cal_values) / len(cal_values)
                    hold_mean = sum(hold_values) / len(hold_values)
                    ratio = hold_mean / cal_mean
                    cells.append((mode, norm, law, q, stat(all_values),
                                  stat(cal_values), stat(hold_values), ratio,
                                  math.log(ratio, 2)))
    return cells


def anchor_digests() -> tuple[str, dict[str, str]]:
    values = list(range(ORIGINS[0], ORIGINS[0] + 13))
    primes = shell(8)
    matrices: dict[str, list[list[Fraction]]] = {law: [] for law in LAWS}
    geometry: list[Fraction] = []
    for u in values:
        row_values = {law: [] for law in LAWS}
        grow = Fraction(0)
        for t in values:
            components = []
            for p in primes:
                if u == t or u % p == 0 or t % p == 0:
                    base = Fraction(0)
                else:
                    centered = Fraction(int((u - t) % p == 0), 1) - Fraction(1, p - 1)
                    base = (p * Fraction(p, 8) ** BETA *
                            Fraction(HEIGHT * HEIGHT,
                                     HEIGHT * HEIGHT + (u - t) ** 2) * centered)
                components.append(base)
            grow += sum(x * x for x in components)
            for law in LAWS:
                row_values[law].append(sum(
                    Fraction(1 if sign(law, i, p, len(primes)) > 0 else -1) * x
                    for i, (p, x) in enumerate(zip(primes, components))))
        geometry.append(grow)
        for law in LAWS:
            matrices[law].append(row_values[law])

    def txt(x: Fraction) -> str:
        return f"{x.numerator}/{x.denominator}"

    return (hashlib.sha256(canonical([txt(x) for x in geometry])).hexdigest(),
            {law: hashlib.sha256(canonical([
                [txt(x) for x in row] for row in matrix
            ])).hexdigest() for law, matrix in matrices.items()})


def load_target() -> dict[str, Any]:
    raw = CERTIFICATE.read_bytes()
    need(CERTIFICATE_SHA256 != "TO_BE_FILLED" and digest(raw) == CERTIFICATE_SHA256,
         "certificate provenance")
    doc = json.loads(raw)
    need(raw == canonical(doc), "certificate canonicality")
    need(doc.get("certificate_version") == 1 and doc.get("claim_status") == STATUS,
         "header")
    payload = doc.get("payload")
    need(isinstance(payload, dict) and payload.get("schema") == SCHEMA and
         payload.get("status") == STATUS, "schema")
    need(doc.get("payload_sha256") == hashlib.sha256(canonical(payload)).hexdigest(),
         "payload hash")
    parent = payload.get("parent_lock", {})
    need(parent.get("parent_code_sha256") == PARENT_CODE_SHA256 and
         parent.get("parent_certificate_sha256") == PARENT_CERT_SHA256 and
         parent.get("forecast_is_fitted") is False, "parent lock")
    selection = payload.get("selection_protocol", {})
    need(selection.get("origins") == list(ORIGINS) and
         selection.get("calibration_origins") == list(CALIBRATION_ORIGINS) and
         selection.get("holdout_origins") == list(HOLDOUT_ORIGINS) and
         selection.get("calibration_count") == 512 and
         selection.get("holdout_count") == 1024 and
         selection.get("band_modes") == list(BAND_MODES) and
         selection.get("q_anchors") == list(QS) and
         selection.get("laws") == list(LAWS) and
         selection.get("normalizations") == list(NORMS) and
         selection.get("response_used_for_selection") is False and
         selection.get("metric_used_for_selection") is False and
         selection.get("holdout_role_fixed_before_readout") is True, "selection")
    rows = payload.get("rows")
    need(isinstance(rows, list) and len(rows) == 160, "rows")
    expected = {(o, q, law, norm, mode) for o in ORIGINS for q in QS
                for law in LAWS for norm in NORMS for mode in BAND_MODES}
    observed = {(r.get("origin"), r.get("Q"), r.get("law"),
                 r.get("normalization"), r.get("band_mode")) for r in rows}
    need(observed == expected, "row keys")
    need(all(r.get("origin_role") ==
             ("calibration" if r.get("origin") in CALIBRATION_ORIGINS else "holdout")
             and r.get("count") == COUNTS.get(r.get("origin"))
             for r in rows), "row roles/counts")
    summary = payload.get("count_summary", {})
    need(summary.get("row_count") == 160 and summary.get("cell_count") == 32 and
         isinstance(summary.get("cells"), list) and len(summary["cells"]) == 32 and
         isinstance(summary.get("forecast_summary"), list) and
         len(summary["forecast_summary"]) == 4, "summary")
    audit = payload.get("finite_audit", {})
    need(audit.get("rows") == 160 and audit.get("cell_count") == 32 and
         audit.get("calibration_count") == 512 and
         audit.get("holdout_count") == 1024 and
         audit.get("coordinate_disjoint_from_prior") is True and
         audit.get("arithmetic_advance") == "NO" and
         audit.get("fixed_power_credit") == 0, "audit")
    firewall = payload.get("claim_firewall", {})
    need(firewall.get("TPC386_ARITHMETIC_ADVANCE") == "NO" and
         firewall.get("TPC386_FIXED_POWER_CREDIT") == 0 and
         firewall.get("TPC386_FULL_GATE_B") == "OPEN" and
         firewall.get("TPC386_TWIN_PRIME_RESULT") == "NONE", "firewall")
    need(payload.get("round2_clue") == ROUND2_CLUE, "clue")
    return payload


def verify() -> dict[str, Any]:
    target = load_target()
    need(digest(PARENT_CODE.read_bytes()) == PARENT_CODE_SHA256 and
         digest(PARENT_CERT.read_bytes()) == PARENT_CERT_SHA256, "parent files")
    actual, pooled = replay()
    rows = target["rows"]
    recorded = {(r["origin"], r["Q"], r["law"], r["normalization"],
                 r["band_mode"]): r for r in rows}
    for key, metrics in actual.items():
        row = recorded.get(key)
        need(row is not None, "missing row")
        for value, field in zip(metrics, ("band_spectral", "band_schur",
                                          "band_frobenius", "symmetry_error")):
            close(value, row[field], field + repr(key))
        close(pooled[key[1]], row["pooled_train_scalar"], "pooled" + repr(key))
    cells = {(x["band_mode"], x["normalization"], x["law"], x["Q"]): x
             for x in target["count_summary"]["cells"]}
    need(len(cells) == 32, "cell keys")
    computed = expected_cells(actual)
    for mode, norm, law, q, all_stat, cal_stat, hold_stat, ratio, logratio in computed:
        item = cells[(mode, norm, law, q)]
        for section, expected_stat in (("all_origin", all_stat),
                                       ("calibration", cal_stat),
                                       ("holdout", hold_stat)):
            rec = item[section]
            for field in ("minimum", "maximum", "mean", "relative_spread"):
                close(expected_stat[field], rec[field], section + field)
            need(rec["value_count"] == expected_stat["value_count"] and
                 rec["within_one_percent"] is expected_stat["within_one_percent"],
                 section + " flag")
        close(ratio, item["holdout_to_calibration_ratio"], "ratio")
        close(logratio, item["count_log2_ratio"], "log ratio")
        need(item["within_count_transfer_cap"] is
             (abs(ratio - 1.0) <= COUNT_TRANSFER_CAP), "transfer flag")
    summary = target["count_summary"]
    need(summary["stable_calibration_cells"] == sum(
        x[5]["within_one_percent"] for x in computed), "cal census")
    need(summary["stable_holdout_cells"] == sum(
        x[6]["within_one_percent"] for x in computed), "hold census")
    for key, counts in summary["failure_counts_by_mode_normalization"].items():
        mode = next((candidate for candidate in BAND_MODES
                     if key.startswith(candidate + "_")), None)
        need(mode is not None, "failure mode key")
        norm = key[len(mode) + 1:]
        subset = [row for k, row in recorded.items()
                  if k[4] == mode and k[3] == norm]
        need(counts["spectral"] == sum(bool(r["spectral_failure"]) for r in subset) and
             counts["schur"] == sum(bool(r["schur_failure"]) for r in subset),
             "failure census")
    forecasts = {(x["band_mode"], x["normalization"]): x
                 for x in summary["forecast_summary"]}
    need(len(forecasts) == 4, "forecast census")
    for mode in BAND_MODES:
        for norm in NORMS:
            item = forecasts[(mode, norm)]
            cell = cells[(mode, norm, "all_plus", 8192)]
            hold = float(cell["holdout"]["mean"])
            cal = float(cell["calibration"]["mean"])
            error = (hold - PARENT_FORECAST[norm]) / PARENT_FORECAST[norm]
            ratio = hold / cal
            close(hold, item["holdout_mean"], "forecast hold")
            close(cal, item["calibration_mean"], "forecast cal")
            close(error, item["holdout_forecast_relative_error"], "forecast error")
            close(ratio, item["holdout_to_calibration_ratio"], "forecast ratio")
            close(PARENT_FORECAST[norm], item["parent_forecast"], "parent forecast")
            need(item["within_count_transfer_cap"] is
                 (abs(ratio - 1.0) <= COUNT_TRANSFER_CAP) and
                 item["within_parent_reference_cap"] is
                 (abs(error) <= COUNT_TRANSFER_CAP), "forecast flags")
    geometry_hash, matrix_hashes = anchor_digests()
    anchor = target["exact_anchor"]
    need(anchor.get("interval") == [2200001, 2200014] and
         anchor.get("Q") == 8 and anchor.get("shell") == [11, 13] and
         anchor.get("geometry_positive") is True and
         anchor.get("geometry_digest") == geometry_hash and
         anchor.get("law_matrix_digests") == matrix_hashes, "anchor")
    return target


def main() -> int:
    if sys.argv[1:] != ["--check"]:
        raise SystemExit("explicit --check is required")
    try:
        target = verify()
        summary = target["count_summary"]
        passed = sum(bool(x["within_parent_reference_cap"])
                     for x in summary["forecast_summary"])
        failures = sum(v["spectral"] for v in
                       summary["failure_counts_by_mode_normalization"].values())
        print("TPC386_INDEPENDENT_CHECK=PASS rows=160 cells=32 "
              f"forecast_cap={passed}/4 spectral_failures={failures} "
              f"stable_holdout={summary['stable_holdout_cells']}/32")
        return 0
    except (Failure, OSError, ValueError, TypeError, KeyError,
            json.JSONDecodeError) as error:
        print("TPC386_INDEPENDENT_CHECK=FAIL " + str(error), file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
