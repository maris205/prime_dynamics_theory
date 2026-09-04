#!/usr/bin/env python3
"""Independent reverse-order replay for TPC-385.

This checker deliberately does not import the producer.  It rebuilds the
prime shell, accumulates components in reverse shell order, and treats the
first three origins as the only source of the pooled training scalar.
"""

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
PROJECT = ROOT / "papers/tpc-385-c1-bandwidth-origin-holdout"
CERTIFICATE = PROJECT / "results/tpc385_certificate.json"
PARENT_CODE = ROOT / (
    "papers/tpc-384-c1-bandwidth-normalization-phase-diagram/code/"
    "tpc384_c1_bandwidth_normalization_phase_diagram.py")
PARENT_CERT = ROOT / (
    "papers/tpc-384-c1-bandwidth-normalization-phase-diagram/results/"
    "tpc384_certificate.json")
PARENT_CODE_SHA256 = "1a4e152e0753be3bc851a962aa92108334863795881571cbd7b97f119ee37896"
PARENT_CERT_SHA256 = "5e43adf62e172947b66a84c18da1509e57e0e015146cc6755c6a2d31b7135ee7"
CERTIFICATE_SHA256 = "ecac4403e2f803fd36c764509f2cd7cbb385e8c45aa5bba103f5b734341f391e"
SCHEMA = "TPC385_C1_BANDWIDTH_ORIGIN_HOLDOUT_V1"
STATUS = "NUMERICALLY_CERTIFIED_FINITE_C1_BANDWIDTH_ORIGIN_HOLDOUT"
ORIGINS = (2000001, 2004011, 2008021, 2012031, 2016041)
CALIBRATION_ORIGINS = (2000001, 2004011, 2008021)
HOLDOUT_ORIGINS = (2012031, 2016041)
WINDOW_COUNT = 512
BLOCK_LENGTH = 128
BLOCK_COUNT = 4
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
PARENT_FORECAST = {
    "c2_local_diagonal": 0.61397411407532332,
    "c3_local_diagonal": 0.62079971051100025,
    "c2_pooled_train_scalar": 0.6338401080191296,
    "c3_pooled_train_scalar": 0.63888760360944985,
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


def make_pack(origin: int, q0: int):
    values = np.arange(origin, origin + WINDOW_COUNT, dtype=np.int64)
    difference = values[:, None] - values[None, :]
    kernel = float(HEIGHT * HEIGHT) / (
        HEIGHT * HEIGHT + difference.astype(np.float64) ** 2)
    np.fill_diagonal(kernel, 0.0)
    primes = shell(q0)
    matrices = {law: np.zeros((WINDOW_COUNT, WINDOW_COUNT), dtype=np.float64)
                for law in LAWS}
    geometry = np.zeros(WINDOW_COUNT, dtype=np.float64)
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
    eig = np.linalg.eigvalsh(matrix)
    spectral = max(abs(float(eig[0])), abs(float(eig[-1])))
    frob = float(np.sqrt(np.sum(matrix * matrix)))
    need(symmetry <= 2e-12 and schur > 0 and frob > 0 and
         math.isfinite(spectral) and spectral <= schur + 1e-8 and
         spectral <= frob + 1e-8, "metric envelope")
    return spectral, schur, frob, symmetry


def replay() -> tuple[dict[tuple[int, int, str, str, int], tuple[float, ...]],
                       dict[int, float]]:
    values: dict[tuple[int, int, str, str, int], tuple[float, ...]] = {}
    pooled: dict[int, float] = {}
    block_ids = np.arange(WINDOW_COUNT) // BLOCK_LENGTH
    masks = {c: np.abs(block_ids[:, None] - block_ids[None, :]) <= c
             for c in BAND_CUTOFFS}
    for q0 in Q_ANCHORS:
        packs = [(origin, make_pack(origin, q0)) for origin in ORIGINS]
        pooled[q0] = float(np.mean([float(pack[1][2].mean()) for pack in packs
                                    if pack[0] in CALIBRATION_ORIGINS]))
        for origin, (primes, matrices, geometry) in packs:
            for cutoff in BAND_CUTOFFS:
                for norm in NORMALIZATIONS:
                    for law in LAWS:
                        if norm == "local_diagonal":
                            normalized = matrices[law] / np.sqrt(
                                geometry[:, None] * geometry[None, :])
                        else:
                            normalized = matrices[law] / pooled[q0]
                        spectral, schur, frob, symmetry = metric(
                            np.where(masks[cutoff], normalized, 0.0))
                        key = (origin, q0, law, norm, cutoff)
                        values[key] = (spectral, schur, frob, symmetry)
    need(len(values) == 160, "replay row count")
    return values, pooled


def stat(values: list[float]) -> dict[str, Any]:
    need(len(values) >= 2, "stat count")
    lo, hi = min(values), max(values)
    mean = sum(values) / len(values)
    spread = (hi - lo) / mean if mean else float("inf")
    return {"value_count": len(values), "minimum": lo, "maximum": hi,
            "mean": mean, "relative_spread": spread,
            "within_one_percent": spread <= SPREAD_CAP, "values": values}


def expected_cells(actual: dict[tuple[int, int, str, str, int], tuple[float, ...]]):
    cells = []
    for c in BAND_CUTOFFS:
        for norm in NORMALIZATIONS:
            for law in LAWS:
                for q in Q_ANCHORS:
                    selected = [(o, actual[(o, q, law, norm, c)][0])
                                for o in ORIGINS]
                    all_values = [v for _, v in selected]
                    cal_values = [v for o, v in selected
                                  if o in CALIBRATION_ORIGINS]
                    hold_values = [v for o, v in selected
                                   if o in HOLDOUT_ORIGINS]
                    cells.append((c, norm, law, q, stat(all_values),
                                  stat(cal_values), stat(hold_values)))
    return cells


def anchor_digests() -> tuple[str, dict[str, str]]:
    interval = (ORIGINS[0], ORIGINS[0] + 13)
    values = list(range(*interval))
    primes = shell(8)
    matrices: dict[str, list[list[Fraction]]] = {law: [] for law in LAWS}
    geometry: list[Fraction] = []
    for u in values:
        rows = {law: [] for law in LAWS}
        grow = Fraction(0)
        for t in values:
            components = []
            for p in primes:
                if u == t or u % p == 0 or t % p == 0:
                    base = Fraction(0)
                else:
                    centered = Fraction(int((u - t) % p == 0), 1) - Fraction(1, p - 1)
                    base = (p * Fraction(p, 8) ** BETA *
                            Fraction(HEIGHT * HEIGHT, HEIGHT * HEIGHT + (u - t) ** 2) * centered)
                components.append(base)
            grow += sum(x * x for x in components)
            for law in LAWS:
                rows[law].append(sum(
                    Fraction(1 if sign(law, i, p, len(primes)) > 0 else -1) * x
                    for i, (p, x) in enumerate(zip(primes, components))))
        geometry.append(grow)
        for law in LAWS:
            matrices[law].append(rows[law])

    def txt(x: Fraction) -> str:
        return f"{x.numerator}/{x.denominator}"

    geom_hash = hashlib.sha256(canonical([txt(x) for x in geometry])).hexdigest()
    matrix_hashes = {law: hashlib.sha256(canonical([
        [txt(x) for x in row] for row in matrix])).hexdigest()
                     for law, matrix in matrices.items()}
    return geom_hash, matrix_hashes


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
         selection.get("origin_indices") == [0, 10, 20, 30, 40] and
         selection.get("calibration_indices") == [0, 10, 20] and
         selection.get("holdout_indices") == [30, 40] and
         selection.get("window_count") == WINDOW_COUNT and
         selection.get("block_length") == BLOCK_LENGTH and
         selection.get("band_cutoffs") == list(BAND_CUTOFFS) and
         selection.get("q_anchors") == list(Q_ANCHORS) and
         selection.get("laws") == list(LAWS) and
         selection.get("normalizations") == list(NORMALIZATIONS) and
         selection.get("response_used_for_selection") is False and
         selection.get("metric_used_for_selection") is False and
         selection.get("holdout_role_fixed_before_readout") is True, "selection")
    rows = payload.get("rows")
    need(isinstance(rows, list) and len(rows) == 160, "rows")
    need(payload.get("row_digest") == hashlib.sha256(canonical(rows)).hexdigest(),
         "row digest")
    expected = {(o, q, law, norm, c) for o in ORIGINS for q in Q_ANCHORS
                for law in LAWS for norm in NORMALIZATIONS for c in BAND_CUTOFFS}
    observed = {(r.get("origin"), r.get("Q"), r.get("law"),
                 r.get("normalization"), r.get("band_cutoff")) for r in rows}
    need(observed == expected, "row keys")
    for row in rows:
        need(row.get("origin_role") ==
             ("calibration" if row.get("origin") in CALIBRATION_ORIGINS else "holdout"),
             "row role")
    phase = payload.get("phase_summary", {})
    need(phase.get("row_count") == 160 and phase.get("cell_count") == 32 and
         isinstance(phase.get("cells"), list) and len(phase["cells"]) == 32,
         "phase header")
    audit = payload.get("finite_audit", {})
    need(audit.get("rows") == 160 and audit.get("cell_count") == 32 and
         audit.get("holdout_origin_count") == 2 and
         audit.get("coordinate_disjoint_from_prior") is True and
         audit.get("arithmetic_advance") == "NO" and
         audit.get("fixed_power_credit") == 0, "audit")
    firewall = payload.get("claim_firewall", {})
    need(firewall.get("TPC385_ARITHMETIC_ADVANCE") == "NO" and
         firewall.get("TPC385_FIXED_POWER_CREDIT") == 0 and
         firewall.get("TPC385_FULL_GATE_B") == "OPEN" and
         firewall.get("TPC385_TWIN_PRIME_RESULT") == "NONE", "firewall")
    need(payload.get("round2_clue") == "TEST_C1_HOLDOUT_COUNT_BANDWIDTH", "clue")
    return payload


def verify() -> dict[str, Any]:
    target = load_target()
    need(digest(PARENT_CODE.read_bytes()) == PARENT_CODE_SHA256 and
         digest(PARENT_CERT.read_bytes()) == PARENT_CERT_SHA256, "parent files")
    actual, pooled = replay()
    rows = target["rows"]
    recorded = {(r["origin"], r["Q"], r["law"], r["normalization"],
                 r["band_cutoff"]): r for r in rows}
    for key, metrics in actual.items():
        row = recorded.get(key)
        need(row is not None, "missing row")
        for value, field in zip(metrics, ("band_spectral", "band_schur",
                                          "band_frobenius", "symmetry_error")):
            close(value, row[field], field + repr(key))
        close(pooled[key[1]], row["pooled_train_scalar"], "pooled" + repr(key))

    cells = {(x["band_cutoff"], x["normalization"], x["law"], x["Q"]): x
             for x in target["phase_summary"]["cells"]}
    need(len(cells) == 32, "cell keys")
    computed = expected_cells(actual)
    for c, norm, law, q, all_stat, cal_stat, hold_stat in computed:
        item = cells[(c, norm, law, q)]
        for section, expected_stat in (("all_origin", all_stat),
                                       ("calibration", cal_stat),
                                       ("holdout", hold_stat)):
            recorded_stat = item[section]
            for field in ("minimum", "maximum", "mean", "relative_spread"):
                close(expected_stat[field], recorded_stat[field],
                      section + field)
            need(recorded_stat["value_count"] == expected_stat["value_count"] and
                 recorded_stat["within_one_percent"] is
                 (expected_stat["within_one_percent"]), section + " flag")
    phase = target["phase_summary"]
    need(phase["stable_calibration_cells"] == sum(
        x[5]["within_one_percent"] for x in computed), "calibration census")
    need(phase["stable_holdout_cells"] == sum(
        x[6]["within_one_percent"] for x in computed), "holdout census")
    for key, count in phase["failure_counts_by_cutoff_normalization"].items():
        c = int(key[1])
        norm = key.split("_", 1)[1]
        subset = [row for k, row in recorded.items() if k[4] == c and k[3] == norm]
        need(count["spectral"] == sum(bool(row["spectral_failure"]) for row in subset) and
             count["schur"] == sum(bool(row["schur_failure"]) for row in subset),
             "failure census")
    forecasts = {(x["key"]): x for x in phase["forecast_summary"]}
    need(len(forecasts) == 4, "forecast census")
    for c in BAND_CUTOFFS:
        for norm in NORMALIZATIONS:
            key = f"c{c}_{norm}"
            cell = cells[(c, norm, "all_plus", 8192)]
            hold_mean = float(cell["holdout"]["mean"])
            error = (hold_mean - PARENT_FORECAST[key]) / PARENT_FORECAST[key]
            item = forecasts[key]
            close(hold_mean, item["holdout_mean"], "forecast hold")
            close(error, item["holdout_forecast_relative_error"], "forecast error")
            close(PARENT_FORECAST[key], item["parent_forecast"], "parent forecast")
            need(item["within_one_percent"] is (abs(error) <= FORECAST_ERROR_CAP),
                 "forecast flag")
    geom_hash, matrix_hashes = anchor_digests()
    anchor = target["exact_anchor"]
    need(anchor.get("interval") == [2000001, 2000014] and
         anchor.get("Q") == 8 and anchor.get("shell") == [11, 13] and
         anchor.get("geometry_positive") is True and
         anchor.get("geometry_digest") == geom_hash and
         anchor.get("law_matrix_digests") == matrix_hashes, "anchor")
    return target


def main() -> int:
    if sys.argv[1:] != ["--check"]:
        raise SystemExit("explicit --check is required")
    try:
        verify()
        print("TPC385_INDEPENDENT_CHECK=PASS rows=160 cells=32 "
              "holdout_forecasts=4/4 stable_holdout=28/32")
        return 0
    except (Failure, OSError, ValueError, TypeError, KeyError,
            json.JSONDecodeError) as error:
        print("TPC385_INDEPENDENT_CHECK=FAIL " + str(error), file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
