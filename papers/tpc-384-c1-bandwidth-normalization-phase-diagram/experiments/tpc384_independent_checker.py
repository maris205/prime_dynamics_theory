#!/usr/bin/env python3
"""Independent reverse-shell replay for TPC-384.

This checker rebuilds the prime-shell matrices without importing the producer,
then crosses all four predeclared block bandwidths and both normalizations.
"""

from __future__ import annotations

import hashlib
import json
import math
import sys
from pathlib import Path
from typing import Any

import numpy as np

ROOT = Path(__file__).resolve().parents[3]
PROJECT = ROOT / "papers/tpc-384-c1-bandwidth-normalization-phase-diagram"
CERTIFICATE = PROJECT / "results/tpc384_certificate.json"
PARENT_CODE = ROOT / "papers/tpc-383-c1-pooled-normalization-audit/code/tpc383_c1_pooled_normalization_audit.py"
PARENT_CERT = ROOT / "papers/tpc-383-c1-pooled-normalization-audit/results/tpc383_certificate.json"
PARENT_CODE_SHA256 = "3593d9db35080d9aae3e8d7e6f2d8d9a5111a4ccd7e8c847a8a33d4eadc2ba48"
PARENT_CERT_SHA256 = "eb6be49c04a196e3cf0aed0fa996960058bc219f391047d090bde21d130d29ee"
CERTIFICATE_SHA256 = "5e43adf62e172947b66a84c18da1509e57e0e015146cc6755c6a2d31b7135ee7"
SCHEMA = "TPC384_C1_BANDWIDTH_NORMALIZATION_PHASE_DIAGRAM_V1"
STATUS = "NUMERICALLY_CERTIFIED_FINITE_C1_BANDWIDTH_NORMALIZATION_PHASE_DIAGRAM"
ORIGINS = (1800001, 1808021, 1816041)
WINDOW_COUNT = 512
BLOCK_LENGTH = 128
BLOCK_COUNT = 4
BAND_CUTOFFS = (0, 1, 2, 3)
Q_ANCHORS = (512, 2048, 8192)
EXPONENT = 1
BETA = 2
HEIGHT = 66
LAWS = ("all_plus", "alternating_index", "mod4_character", "half_split")
NORMALIZATIONS = ("local_diagonal", "pooled_scalar")
SPREAD_CAP = 0.01


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


def replay() -> tuple[dict[tuple[int, int, str, str, int], float], dict[int, float]]:
    values: dict[tuple[int, int, str, str, int], float] = {}
    pooled: dict[int, float] = {}
    block_ids = np.arange(WINDOW_COUNT) // BLOCK_LENGTH
    masks = {c: np.abs(block_ids[:, None] - block_ids[None, :]) <= c
             for c in BAND_CUTOFFS}
    for q0 in Q_ANCHORS:
        packs = [(origin, make_pack(origin, q0)) for origin in ORIGINS]
        pooled[q0] = float(np.mean([float(pack[1][2].mean()) for pack in packs]))
        for origin, (primes, matrices, geometry) in packs:
            for cutoff in BAND_CUTOFFS:
                for norm in NORMALIZATIONS:
                    for law in LAWS:
                        if norm == "local_diagonal":
                            normalized = matrices[law] / np.sqrt(
                                geometry[:, None] * geometry[None, :])
                        else:
                            normalized = matrices[law] / pooled[q0]
                        band = np.where(masks[cutoff], normalized, 0.0)
                        eig = np.linalg.eigvalsh(band)
                        values[(origin, q0, law, norm, cutoff)] = max(
                            abs(float(eig[0])), abs(float(eig[-1])))
    need(len(values) == 288, "replay row count")
    return values, pooled


def load_target() -> dict[str, Any]:
    raw = CERTIFICATE.read_bytes()
    need(CERTIFICATE_SHA256 != "TO_BE_FILLED" and
         digest(raw) == CERTIFICATE_SHA256, "certificate provenance")
    doc = json.loads(raw)
    need(raw == canonical(doc), "certificate canonicality")
    need(doc.get("certificate_version") == 1 and
         doc.get("claim_status") == STATUS, "header")
    payload = doc.get("payload")
    need(isinstance(payload, dict) and payload.get("schema") == SCHEMA and
         payload.get("status") == STATUS, "schema")
    need(doc.get("payload_sha256") == hashlib.sha256(
        canonical(payload)).hexdigest(), "payload hash")
    selection = payload.get("selection_protocol", {})
    need(selection.get("origins") == list(ORIGINS) and
         selection.get("origin_indices") == [0, 20, 40] and
         selection.get("window_count") == WINDOW_COUNT and
         selection.get("block_length") == BLOCK_LENGTH and
         selection.get("band_cutoffs") == list(BAND_CUTOFFS) and
         selection.get("q_anchors") == list(Q_ANCHORS) and
         selection.get("laws") == list(LAWS) and
         selection.get("normalizations") == list(NORMALIZATIONS) and
         selection.get("response_used_for_selection") is False and
         selection.get("metric_used_for_selection") is False, "selection")
    protocol = payload.get("protocol", {})
    need(protocol.get("band_cutoffs") == list(BAND_CUTOFFS) and
         protocol.get("normalizations") == list(NORMALIZATIONS) and
         protocol.get("bandwidth_selection_used") is False and
         protocol.get("source_response_used") is False, "protocol")
    rows = payload.get("rows")
    need(isinstance(rows, list) and len(rows) == 288, "rows")
    need(payload.get("row_digest") == hashlib.sha256(
        canonical(rows)).hexdigest(), "row digest")
    need({(r.get("origin"), r.get("Q"), r.get("law"),
            r.get("normalization"), r.get("band_cutoff")) for r in rows} ==
         {(o, q, law, norm, c) for o in ORIGINS for q in Q_ANCHORS
          for law in LAWS for norm in NORMALIZATIONS for c in BAND_CUTOFFS},
         "row keys")
    return payload


def verify() -> dict[str, Any]:
    target = load_target()
    need(digest(PARENT_CODE.read_bytes()) == PARENT_CODE_SHA256 and
         digest(PARENT_CERT.read_bytes()) == PARENT_CERT_SHA256, "parent locks")
    actual, pooled = replay()
    rows = target["rows"]
    recorded = {(r["origin"], r["Q"], r["law"], r["normalization"],
                 r["band_cutoff"]): r for r in rows}
    for key, value in actual.items():
        need(key in recorded, "missing actual row")
        close(value, recorded[key]["band_spectral"], "spectral " + repr(key))
        close(pooled[key[1]], recorded[key]["pooled_scalar"],
              "pooled " + repr(key))
    cells = target["phase_summary"]["cells"]
    need(len(cells) == 96, "cells")
    cmap = {(x["band_cutoff"], x["normalization"], x["law"], x["Q"]): x
            for x in cells}
    need(len(cmap) == 96, "cell keys")
    for cutoff in BAND_CUTOFFS:
        for norm in NORMALIZATIONS:
            for law in LAWS:
                for q0 in Q_ANCHORS:
                    vals = [actual[(origin, q0, law, norm, cutoff)]
                            for origin in ORIGINS]
                    item = cmap[(cutoff, norm, law, q0)]
                    lo, hi = min(vals), max(vals)
                    mean = sum(vals) / 3.0
                    spread = (hi - lo) / mean
                    close(lo, item["minimum"], "cell min")
                    close(hi, item["maximum"], "cell max")
                    close(mean, item["mean"], "cell mean")
                    close(spread, item["relative_spread"], "cell spread")
                    need(item["within_one_percent"] is (spread <= SPREAD_CAP),
                         "cell flag")
    phase = target["phase_summary"]
    need(phase["stable_cells_by_cutoff_normalization"] == {
        "c0_local_diagonal": 6, "c0_pooled_scalar": 7,
        "c1_local_diagonal": 8, "c1_pooled_scalar": 7,
        "c2_local_diagonal": 8, "c2_pooled_scalar": 8,
        "c3_local_diagonal": 8, "c3_pooled_scalar": 8}, "stable census")
    need(all(v["spectral"] == 0 and v["schur"] == 0
             for v in phase["failure_counts_by_cutoff_normalization"].values()),
         "failure census")
    high = phase["all_plus_high_q_by_cutoff_normalization"]
    need(float(high["c3_pooled_scalar"]["mean"]) > 0.63 and
         float(high["c3_pooled_scalar"]["mean"]) < 0.65 and
         float(phase["all_plus_high_q_pooled_vs_local_relative_shift"]["c0"]) < -0.05 and
         float(phase["all_plus_high_q_pooled_vs_local_relative_shift"]["c1"]) > 0.03,
         "phase signal")
    firewall = target["claim_firewall"]
    need(firewall["TPC384_ARITHMETIC_ADVANCE"] == "NO" and
         firewall["TPC384_FIXED_POWER_CREDIT"] == 0 and
         firewall["TPC384_FULL_GATE_B"] == "OPEN" and
         firewall["TPC384_TWIN_PRIME_RESULT"] == "NONE", "firewall")
    need(target["round2_clue"] == "TEST_C1_BANDWIDTH_ORIGIN_HOLDOUT", "clue")
    return target


def main() -> int:
    if sys.argv[1:] != ["--check"]:
        raise SystemExit("explicit --check is required")
    try:
        verify()
        print("TPC384_INDEPENDENT_CHECK=PASS rows=288 cells=96 "
              "bandwidths=4 normalizations=2")
        return 0
    except (Failure, OSError, ValueError, TypeError, KeyError,
            json.JSONDecodeError) as error:
        print("TPC384_INDEPENDENT_CHECK=FAIL " + str(error), file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
