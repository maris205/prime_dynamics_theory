#!/usr/bin/env python3
"""Independent direct-matrix replay for TPC-383.

The producer is not imported.  Prime shells, centered residue blocks, both
normalizations, and the c=1 band are rebuilt here with reverse shell order.
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
PROJECT = ROOT / "papers/tpc-383-c1-pooled-normalization-audit"
CERTIFICATE = PROJECT / "results/tpc383_certificate.json"
PARENT_CODE = ROOT / "papers/tpc-382-c1-origin-family-magnitude-audit/code/tpc382_c1_origin_family_magnitude_audit.py"
PARENT_CERT = ROOT / "papers/tpc-382-c1-origin-family-magnitude-audit/results/tpc382_certificate.json"
PARENT_CODE_SHA256 = "d68231e2f547f6102373f3c34e013663eb350e6ede59cf805d7b2f7b35d3e215"
PARENT_CERT_SHA256 = "1bd35889f40e911aa2faa4f2f5a636583f905a388b0dda0417c1ed031f492b6e"
CERTIFICATE_SHA256 = "eb6be49c04a196e3cf0aed0fa996960058bc219f391047d090bde21d130d29ee"
SCHEMA = "TPC383_C1_POOLED_NORMALIZATION_AUDIT_V1"
STATUS = "NUMERICALLY_CERTIFIED_FINITE_C1_POOLED_NORMALIZATION_AUDIT"
ORIGINS = (1600001, 1608021, 1616041)
WINDOW_COUNT = 512
BLOCK_LENGTH = 128
BLOCK_COUNT = 4
BAND_CUTOFF = 1
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
          tolerance: float = 7e-8) -> None:
    try:
        target = float(recorded)
    except (TypeError, ValueError) as error:
        raise Failure(label + " nonnumeric") from error
    need(math.isfinite(target) and math.isfinite(actual) and
         abs(actual - target) <= tolerance * max(1.0, abs(actual),
                                                  abs(target)),
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


def sign(primes: list[int], law: str, i: int, p: int) -> float:
    if law == "all_plus":
        return 1.0
    if law == "alternating_index":
        return 1.0 if i % 2 == 0 else -1.0
    if law == "mod4_character":
        return 1.0 if p % 4 == 1 else -1.0
    return 1.0 if i < len(primes) / 2 else -1.0


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
    # Reverse order provides a distinct accumulation path from the producer.
    for i, p in reversed(tuple(enumerate(primes))):
        centered = ((difference % p == 0).astype(np.float64) - 1.0 / (p - 1))
        np.fill_diagonal(centered, 0.0)
        valid = ((difference != 0) & (values[:, None] % p != 0) &
                 (values[None, :] % p != 0))
        block = (float(p) / float(q0)) ** BETA * float(p) * kernel * centered * valid
        geometry += np.sum(block * block, axis=1)
        for law in LAWS:
            matrices[law] += sign(primes, law, i, p) * block
    for law in LAWS:
        matrices[law] = (matrices[law] + matrices[law].T) / 2.0
    return primes, matrices, geometry


def replay() -> tuple[dict[tuple[int, int, str, str], float], dict[int, float]]:
    block_ids = np.arange(WINDOW_COUNT) // BLOCK_LENGTH
    mask = np.abs(block_ids[:, None] - block_ids[None, :]) <= BAND_CUTOFF
    values: dict[tuple[int, int, str, str], float] = {}
    pooled: dict[int, float] = {}
    for q0 in Q_ANCHORS:
        packs = [(origin, make_pack(origin, q0)) for origin in ORIGINS]
        pooled[q0] = float(np.mean([float(item[1][2].mean()) for item in packs]))
        for origin, (primes, matrices, geometry) in packs:
            for norm in NORMALIZATIONS:
                for law in LAWS:
                    if norm == "local_diagonal":
                        matrix = matrices[law] / np.sqrt(
                            geometry[:, None] * geometry[None, :])
                    else:
                        matrix = matrices[law] / pooled[q0]
                    band = np.where(mask, matrix, 0.0)
                    eig = np.linalg.eigvalsh(band)
                    values[(origin, q0, law, norm)] = max(
                        abs(float(eig[0])), abs(float(eig[-1])))
    return values, pooled


def load_target() -> dict[str, Any]:
    raw = CERTIFICATE.read_bytes()
    need(digest(raw) == CERTIFICATE_SHA256, "certificate provenance")
    doc = json.loads(raw)
    need(raw == canonical(doc), "certificate canonicality")
    need(doc.get("certificate_version") == 1 and
         doc.get("claim_status") == STATUS, "certificate header")
    payload = doc.get("payload")
    need(isinstance(payload, dict) and payload.get("schema") == SCHEMA and
         payload.get("status") == STATUS, "schema")
    need(doc.get("payload_sha256") == hashlib.sha256(
        canonical(payload)).hexdigest(), "payload hash")
    need(payload.get("parent_lock") == {
        "parent_code_sha256": PARENT_CODE_SHA256,
        "parent_certificate_sha256": PARENT_CERT_SHA256,
        "parent_schema": "TPC382_C1_ORIGIN_FAMILY_MAGNITUDE_AUDIT_V1",
        "parent_round2_clue": "TEST_C1_POOLED_NORMALIZATION_CROSS_ORIGIN"},
         "parent lock")
    need(payload.get("selection_protocol", {}).get("origins") == list(ORIGINS),
         "origins")
    need(payload.get("protocol", {}).get("normalizations") ==
         list(NORMALIZATIONS), "normalizations")
    need(payload.get("finite_audit", {}).get("rows") == 72 and
         payload.get("finite_audit", {}).get("coordinate_disjoint_from_prior") is True,
         "finite audit")
    return payload


def verify() -> dict[str, Any]:
    target = load_target()
    # Check that the locked parent remains available, even though this replay
    # only consumes the fresh TPC-383 source definition.
    need(PARENT_CODE.is_file() and PARENT_CERT.is_file(), "parent files")
    need(digest(PARENT_CODE.read_bytes()) == PARENT_CODE_SHA256, "parent code")
    need(digest(PARENT_CERT.read_bytes()) == PARENT_CERT_SHA256, "parent cert")
    actual, pooled = replay()
    rows = target.get("rows")
    need(isinstance(rows, list) and len(rows) == 72, "row census")
    recorded = {(r.get("origin"), r.get("Q"), r.get("law"),
                 r.get("normalization")): r for r in rows}
    need(len(recorded) == 72, "row keys")
    for key, value in actual.items():
        need(key in recorded, "missing row")
        close(value, recorded[key].get("band_spectral"),
              "band spectral " + repr(key))
        close(pooled[key[1]], recorded[key].get("pooled_scalar"),
              "pooled scalar " + repr(key))
    cells = target.get("phase_summary", {}).get("cells")
    need(isinstance(cells, list) and len(cells) == 24, "phase cells")
    cell_map = {(x.get("normalization"), x.get("law"), x.get("Q")): x
                for x in cells}
    need(len(cell_map) == 24, "phase keys")
    for norm in NORMALIZATIONS:
        for law in LAWS:
            for q0 in Q_ANCHORS:
                vals = [actual[(origin, q0, law, norm)] for origin in ORIGINS]
                item = cell_map[(norm, law, q0)]
                lo, hi = min(vals), max(vals)
                mean = sum(vals) / len(vals)
                relative = (hi - lo) / mean
                close(lo, item.get("minimum"), "cell min")
                close(hi, item.get("maximum"), "cell max")
                close(mean, item.get("mean"), "cell mean")
                close(relative, item.get("relative_spread"), "cell spread")
                need(item.get("within_one_percent") is
                     (relative <= SPREAD_CAP), "cell flag")
    phase = target["phase_summary"]
    local_stable = sum(cell_map[("local_diagonal", law, q)]["within_one_percent"]
                       for law in LAWS for q in Q_ANCHORS)
    pooled_stable = sum(cell_map[("pooled_scalar", law, q)]["within_one_percent"]
                        for law in LAWS for q in Q_ANCHORS)
    need(phase.get("stable_cells_local") == local_stable == 9 and
         phase.get("stable_cells_pooled") == pooled_stable == 9,
         "stable census")
    need(phase.get("all_plus_high_q_local_stable") is True and
         phase.get("all_plus_high_q_pooled_stable") is True,
         "high-Q transfer")
    need(float(phase.get("all_plus_high_q_pooled_vs_local_relative_shift")) >
         0.03, "normalization shift")
    firewall = target.get("claim_firewall", {})
    need(firewall.get("TPC383_ARITHMETIC_ADVANCE") == "NO" and
         firewall.get("TPC383_FIXED_POWER_CREDIT") == 0 and
         firewall.get("TPC383_FULL_GATE_B") == "OPEN" and
         firewall.get("TPC383_TWIN_PRIME_RESULT") == "NONE", "firewall")
    need(target.get("round2_clue") ==
         "TEST_C1_BANDWIDTH_NORMALIZATION_PHASE_DIAGRAM", "clue")
    return target


def main() -> int:
    if sys.argv[1:] != ["--check"]:
        raise SystemExit("explicit --check is required")
    try:
        verify()
        print("TPC383_INDEPENDENT_CHECK=PASS rows=72 local_stable=9 "
              "pooled_stable=9 all_plus_high_q_transfer=True")
        return 0
    except (Failure, OSError, ValueError, TypeError, KeyError,
            json.JSONDecodeError) as error:
        print("TPC383_INDEPENDENT_CHECK=FAIL " + str(error), file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
