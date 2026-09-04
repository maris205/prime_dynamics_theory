#!/usr/bin/env python3
"""Independent reverse-shell replay for TPC-378.

This file deliberately does not import the TPC-378 producer.  It rebuilds the
finite masked matrices from integer arithmetic, then compares every recorded
row and the exact rational anchor with the certificate.
"""

from __future__ import annotations

import hashlib
import json
import math
import sys
from concurrent.futures import ThreadPoolExecutor
from fractions import Fraction
from pathlib import Path
from typing import Any

import numpy as np

ROOT = Path(__file__).resolve().parents[3]
CERTIFICATE = ROOT / (
    "papers/tpc-378-c1-scale-origin-crossholdout/results/"
    "tpc378_certificate.json")
PARENT_CODE = ROOT / (
    "papers/tpc-377-c1-window-scale-holdout/code/"
    "tpc377_c1_window_scale_holdout.py")
PARENT_CERT = ROOT / (
    "papers/tpc-377-c1-window-scale-holdout/results/"
    "tpc377_certificate.json")
PARENT_CODE_SHA256 = (
    "5200e29c0c26f61cb190de6dfcc186dd3ea80c9b7ebd0dc76b21f712b93ba966")
PARENT_CERT_SHA256 = (
    "2e3061e406a0bb6542b27789411b3518207024f92bcf943ef67afa37b200668c")

SCHEMA = "TPC378_C1_SCALE_ORIGIN_CROSSHOLDOUT_V1"
STATUS = "NUMERICALLY_CERTIFIED_FINITE_C1_SCALE_ORIGIN_CROSSHOLDOUT"
ORIGINS = [1100001, 1108021, 1116041]
COUNTS = [1024, 2048]
BLOCK_LENGTH = 256
Q_ANCHORS = [512, 2048, 8192]
BAND_CUTOFF = 1
HEIGHT = 66
BETA = 2
SPECTRAL_CAP = 0.64
SCHUR_CAP = 0.83
EXACT_INTERVAL = (1100001, 1100014)
EXACT_Q = 4


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
          tolerance: float = 6.0e-5) -> None:
    target = float(recorded)
    need(math.isfinite(actual) and math.isfinite(target) and
         abs(actual - target) <= tolerance *
         max(1.0, abs(actual), abs(target)), label)


def primes_up_to(limit: int) -> list[int]:
    sieve = bytearray(b"\x01") * (limit + 1)
    sieve[0] = sieve[1] = 0
    for p in range(2, math.isqrt(limit) + 1):
        if sieve[p]:
            start = p * p
            sieve[start:limit + 1:p] = b"\x00" * (
                (limit - start) // p + 1)
    return [p for p in range(2, limit + 1) if sieve[p]]


PRIMES = primes_up_to(20_000)


def shell(q0: int) -> list[int]:
    return [p for p in PRIMES if q0 < p <= 2 * q0]


def metrics(matrix: np.ndarray, values: np.ndarray) -> dict[str, float]:
    symmetry = float(np.max(np.abs(matrix - matrix.T)))
    mass = np.sum(np.abs(matrix), axis=1)
    schur = float(np.max(mass))
    frobenius = float(np.sqrt(np.sum(matrix * matrix)))
    lo, hi = float(values[0]), float(values[-1])
    spectral = max(abs(lo), abs(hi))
    need(symmetry <= 2.0e-12 and schur > 0 and frobenius > 0 and
         math.isfinite(spectral) and spectral <= schur + 2.0e-8 and
         spectral <= frobenius + 2.0e-8, "metric envelope")
    return {"schur": schur, "frobenius": frobenius,
            "spectral": spectral, "minimum_eigenvalue": lo,
            "maximum_eigenvalue": hi, "symmetry_error": symmetry}


def replay(origin: int, count: int, q0: int) -> dict[str, Any]:
    values = np.arange(origin, origin + count, dtype=np.int64)
    difference = values[:, None] - values[None, :]
    kernel = float(HEIGHT * HEIGHT) / (HEIGHT * HEIGHT +
                                       difference.astype(np.float64) ** 2)
    np.fill_diagonal(kernel, 0.0)
    matrix = np.zeros((count, count), dtype=np.float64)
    geometry = np.zeros(count, dtype=np.float64)
    for p in reversed(shell(q0)):
        centered = ((difference % p == 0).astype(np.float64) -
                    1.0 / (p - 1))
        np.fill_diagonal(centered, 0.0)
        valid = ((difference != 0) & (values[:, None] % p != 0) &
                 (values[None, :] % p != 0))
        block = ((float(p) / float(q0)) ** BETA * float(p) * kernel *
                 centered * valid)
        geometry += np.sum(block * block, axis=1)
        matrix += block
    need(bool(np.all(np.isfinite(geometry) & (geometry > 0))), "geometry")
    full = matrix / np.sqrt(geometry[:, None] * geometry[None, :])
    values_full, vectors = np.linalg.eigh(full)
    full_metrics = metrics(full, values_full)
    index = 0 if abs(values_full[0]) >= abs(values_full[-1]) else -1
    vector = np.asarray(vectors[:, index], dtype=np.float64)
    selected = float(values_full[index])
    residual = float(np.max(np.abs(full @ vector - selected * vector)))
    blocks = np.arange(count, dtype=np.int64) // BLOCK_LENGTH
    band = np.where(np.abs(blocks[:, None] - blocks[None, :]) <=
                    BAND_CUTOFF, full, 0.0)
    tail = full - band
    band_values = np.linalg.eigvalsh(band)
    band_metrics = metrics(band, band_values)
    band_rayleigh = float(vector @ (band @ vector))
    tail_rayleigh = float(vector @ (tail @ vector))
    need(residual <= 1.0e-8 and
         abs(float(np.dot(vector, vector)) - 1.0) <= 1.0e-10 and
         abs(band_rayleigh + tail_rayleigh - selected) <= 2.0e-11 and
         float(np.max(np.abs(tail - tail.T))) <= 2.0e-12,
         "eigen/rayleigh identity")
    return {
        "full": full_metrics, "band": band_metrics,
        "selected": selected, "residual": residual,
        "norm_error": abs(float(np.dot(vector, vector)) - 1.0),
        "band_rayleigh": band_rayleigh, "tail_rayleigh": tail_rayleigh,
        "retention": abs(band_rayleigh) / abs(selected),
        "tail_fraction": abs(tail_rayleigh) / abs(selected),
        "band_failure": band_metrics["spectral"] > SPECTRAL_CAP,
        "schur_failure": band_metrics["schur"] > SCHUR_CAP,
        "mode": "minimum_eigenvalue" if index == 0 else "maximum_eigenvalue",
    }


def exact_anchor() -> dict[str, Any]:
    values = list(range(*EXACT_INTERVAL))
    primes = shell(EXACT_Q)

    def as_text(value: Fraction) -> str:
        return f"{value.numerator}/{value.denominator}"

    matrix: list[list[Fraction]] = []
    geometry: list[Fraction] = []
    for u in values:
        row: list[Fraction] = []
        grow = Fraction(0)
        for t in values:
            total = Fraction(0)
            energy = Fraction(0)
            for p in primes:
                if u == t or u % p == 0 or t % p == 0:
                    base = Fraction(0)
                else:
                    centered = Fraction(int((u - t) % p == 0), 1)
                    centered -= Fraction(1, p - 1)
                    base = (p * Fraction(HEIGHT * HEIGHT,
                                         HEIGHT * HEIGHT + (u - t) ** 2)
                            * centered)
                weighted = Fraction(p, EXACT_Q) ** BETA * base
                total += weighted
                energy += weighted * weighted
            row.append(total)
            grow += energy
        matrix.append(row)
        geometry.append(grow)
    need(all(matrix[i][j] == matrix[j][i]
             for i in range(len(values)) for j in range(len(values))),
         "anchor symmetry")
    need(all(g > 0 for g in geometry), "anchor positivity")
    return {
        "interval": list(EXACT_INTERVAL), "Q": EXACT_Q,
        "kernel_exponent": 1, "beta": BETA, "shell": primes,
        "matrix_symmetric": True, "geometry_positive": True,
        "matrix_digest": hashlib.sha256(canonical([
            [as_text(x) for x in row] for row in matrix])).hexdigest(),
        "geometry_digest": hashlib.sha256(canonical(
            [as_text(x) for x in geometry])).hexdigest(),
    }


def validate(document: dict[str, Any]) -> None:
    need(document.get("certificate_version") == 1 and
         document.get("claim_status") == STATUS, "header")
    payload = document.get("payload")
    need(isinstance(payload, dict) and payload.get("schema") == SCHEMA and
         payload.get("status") == STATUS, "schema")
    need(document.get("payload_sha256") == hashlib.sha256(
        canonical(payload)).hexdigest(), "payload hash")
    need(digest(PARENT_CODE.read_bytes()) == PARENT_CODE_SHA256,
         "parent code lock")
    need(digest(PARENT_CERT.read_bytes()) == PARENT_CERT_SHA256,
         "parent certificate lock")
    need(payload.get("parent_lock") == {
        "parent_code_sha256": PARENT_CODE_SHA256,
        "parent_certificate_sha256": PARENT_CERT_SHA256,
        "parent_schema": "TPC377_C1_WINDOW_SCALE_HOLDOUT_V1",
        "parent_round2_clue": "TEST_C1_SCALE_ORIGIN_CROSSHOLDOUT",
        "parent_failure_profile_by_count_Q":
            [[0, 3, 3], [0, 3, 3], [0, 3, 3]],
    }, "parent lock")
    selection = payload.get("selection_protocol", {})
    candidates = [1100001 + 401 * i for i in range(41)]
    need(selection.get("grid_start") == 1100001 and
         selection.get("grid_step") == 401 and
         selection.get("grid_count") == 41 and
         selection.get("candidate_origins") == candidates and
         selection.get("origin_indices") == [0, 20, 40] and
         selection.get("origins") == ORIGINS and
         selection.get("counts") == COUNTS and
         selection.get("block_length") == 256 and
         selection.get("block_counts") == [4, 8] and
         selection.get("q_anchors") == Q_ANCHORS and
         selection.get("response_used_for_selection") is False and
         selection.get("signed_metric_used_for_selection") is False and
         selection.get("panel_complete_before_metric_read") is True,
         "selection protocol")
    protocol = payload.get("protocol", {})
    need(protocol.get("origins") == ORIGINS and
         protocol.get("window_counts") == COUNTS and
         protocol.get("block_length") == 256 and
         protocol.get("block_counts") == [4, 8] and
         protocol.get("band_cutoff") == 1 and
         protocol.get("q_anchors") == Q_ANCHORS and
         protocol.get("kernel_exponents") == [1] and
         protocol.get("laws") == ["all_plus"] and
         protocol.get("betas") == [2] and
         protocol.get("height") == 66 and
         protocol.get("common_normalization") is True and
         protocol.get("source_response_used") is False and
         protocol.get("origin_selection_used") is False and
         protocol.get("count_selection_used") is False and
         protocol.get("row_selection_used") is False,
         "protocol")
    rows = payload.get("rows")
    need(isinstance(rows, list) and len(rows) == 18, "row count")
    expected_keys = {(o, n, q) for o in ORIGINS for n in COUNTS
                     for q in Q_ANCHORS}
    need({(r.get("origin"), r.get("count"), r.get("Q")) for r in rows} ==
         expected_keys, "row keys")
    for row in rows:
        result = replay(row["origin"], row["count"], row["Q"])
        for part in ("full", "band"):
            for metric in ("schur", "frobenius", "spectral",
                           "minimum_eigenvalue", "maximum_eigenvalue"):
                close(result[part][metric], row[part][metric],
                      f"{part}.{metric}")
        close(result["selected"], row["mode"]["selected_eigenvalue"],
              "selected")
        close(result["residual"], row["mode"]["eigen_residual_inf"],
              "residual", 2.0e-5)
        close(result["retention"], row["mode"]["band_rayleigh_abs_retention"],
              "retention")
        close(result["tail_fraction"], row["mode"]["tail_rayleigh_abs_fraction"],
              "tail fraction")
        need(result["band_failure"] == row["band_failure"] and
             result["schur_failure"] == row["schur_failure"] and
             result["mode"] == row["mode"]["selected_mode"], "row decision")
    phase = payload.get("phase_summary", {})
    need(phase.get("rows") == 18 and
         phase.get("spectral_cap_violations") == 12 and
         phase.get("schur_cap_violations") == 0 and
         phase.get("failure_profile_by_count_Q") ==
         [[0, 3, 3], [0, 3, 3]], "phase summary")
    audit = payload.get("finite_audit", {})
    need(audit.get("rows") == 18 and
         audit.get("origin_count") == 3 and audit.get("count_count") == 2 and
         audit.get("q_count") == 3 and
         audit.get("spectral_cap_violations") == 12 and
         audit.get("schur_cap_violations") == 0 and
         audit.get("failure_profile_by_count_Q") == [[0, 3, 3], [0, 3, 3]] and
         audit.get("coordinate_disjoint_from_prior") is True and
         audit.get("profile_transfer") is True and
         audit.get("fixed_power_credit") == 0 and
         audit.get("arithmetic_advance") == "NO", "finite audit")
    need(payload.get("exact_anchor") == exact_anchor(), "exact anchor")
    need(payload.get("round2_clue") == "TEST_C1_CROSSHOLDOUT_LAW_CONTROL",
         "round2 clue")
    need(payload.get("claim_firewall", {}).get(
        "TPC378_ARITHMETIC_ADVANCE") == "NO" and
         payload["claim_firewall"].get("TPC378_FIXED_POWER_CREDIT") == 0 and
         payload["claim_firewall"].get("TPC378_FULL_GATE_B") == "OPEN",
         "claim firewall")


def main() -> int:
    if sys.argv[1:] != ["--check"]:
        raise SystemExit("explicit --check is required")
    try:
        document = json.loads(CERTIFICATE.read_bytes())
        validate(document)
        print("TPC378_INDEPENDENT_CHECK=PASS rows=18 failures=12 "
              "profiles=0,3,3;0,3,3")
        return 0
    except (Failure, OSError, ValueError, TypeError, KeyError,
            json.JSONDecodeError) as error:
        print("TPC378_INDEPENDENT_CHECK=FAIL " + str(error), file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
