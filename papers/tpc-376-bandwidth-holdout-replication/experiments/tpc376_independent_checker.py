#!/usr/bin/env python3
"""Independent descending-shell replay for TPC-376."""

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
    "papers/tpc-376-bandwidth-holdout-replication/results/"
    "tpc376_certificate.json")
ENGINE_CODE = ROOT / (
    "papers/tpc-375-bandwidth-stability-minimal-cutoff/code/"
    "tpc375_bandwidth_stability_minimal_cutoff.py")
ENGINE_CODE_SHA256 = (
    "f3fee82fb6306a65a5f83cc8a90b9b04e22e41a6df623784304305c863d12a15")
PARENT_CERT = ROOT / (
    "papers/tpc-375-bandwidth-stability-minimal-cutoff/results/"
    "tpc375_certificate.json")
PARENT_CERT_SHA256 = (
    "3ad30c606b669512cfff63907f3876032efb9b566b03f01ff950e775e1b92e65")

SCHEMA = "TPC376_BANDWIDTH_HOLDOUT_REPLICATION_V1"
STATUS = "NUMERICALLY_CERTIFIED_FINITE_BANDWIDTH_HOLDOUT_REPLICATION"
ORIGINS = [1012006, 1016016, 1022031]
Q_ANCHORS = [512, 2048, 8192]
WINDOW_COUNT = 2048
BLOCK_COUNT = 256
BAND_CUTOFF = 1
HEIGHT = 66
SPECTRAL_CAP = 0.64
SCHUR_CAP = 0.83
BETA = 2
EXACT_INTERVAL = (1012006, 1012019)
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
          tolerance: float = 3.0e-5) -> None:
    target = float(recorded)
    need(math.isfinite(actual) and math.isfinite(target) and
         abs(actual - target) <= tolerance * max(1.0, abs(actual), abs(target)),
         label)


def primes_up_to(limit: int) -> list[int]:
    sieve = bytearray(b"\x01") * (limit + 1)
    sieve[0] = sieve[1] = 0
    for prime in range(2, math.isqrt(limit) + 1):
        if sieve[prime]:
            start = prime * prime
            sieve[start:limit + 1:prime] = b"\x00" * (
                (limit - start) // prime + 1)
    return [value for value in range(2, limit + 1) if sieve[value]]


PRIMES = primes_up_to(20_000)


def shell_for(q0: int) -> list[int]:
    return [p for p in PRIMES if q0 < p <= 2 * q0]


def metrics(matrix: np.ndarray, eigenvalues: np.ndarray) -> dict[str, float]:
    symmetry = float(np.max(np.abs(matrix - matrix.T)))
    mass = np.sum(np.abs(matrix), axis=1)
    schur = float(np.max(mass))
    frobenius = float(np.sqrt(np.sum(matrix * matrix)))
    lo, hi = float(eigenvalues[0]), float(eigenvalues[-1])
    spectral = max(abs(lo), abs(hi))
    need(symmetry <= 1.0e-12 and schur > 0 and frobenius > 0 and
         math.isfinite(spectral) and spectral > 0 and
         spectral <= schur + 8.0e-9 * max(1.0, schur) and
         spectral <= frobenius + 8.0e-9 * max(1.0, frobenius),
         "metric envelope")
    return {"schur": schur, "frobenius": frobenius,
            "spectral": spectral, "minimum_eigenvalue": lo,
            "maximum_eigenvalue": hi, "symmetry_error": symmetry}


def replay(origin: int, q0: int) -> dict[str, float | bool | str]:
    values = np.arange(origin, origin + WINDOW_COUNT, dtype=np.int64)
    difference = values[:, None] - values[None, :]
    distance = difference.astype(np.float64)
    kernel = float(HEIGHT * HEIGHT) / (HEIGHT * HEIGHT +
                                         distance * distance)
    np.fill_diagonal(kernel, 0.0)
    primes = shell_for(q0)
    matrix = np.zeros((WINDOW_COUNT, WINDOW_COUNT), dtype=np.float64)
    geometry = np.zeros(WINDOW_COUNT, dtype=np.float64)
    # Reverse order and direct all-plus accumulation are independent of the
    # producer's forward loop and imported sign vector.
    for prime in reversed(primes):
        centered = ((difference % prime == 0).astype(np.float64) -
                    1.0 / (prime - 1))
        np.fill_diagonal(centered, 0.0)
        valid = ((difference != 0) &
                 (values[:, None] % prime != 0) &
                 (values[None, :] % prime != 0))
        block = ((float(prime) / float(q0)) ** BETA * float(prime) *
                 kernel * centered * valid)
        geometry += np.sum(block * block, axis=1)
        matrix += block
    matrix[:] = (matrix + matrix.T) / 2.0
    need(bool(np.all(np.isfinite(geometry) & (geometry > 0))),
         "geometry")
    full = matrix / np.sqrt(geometry[:, None] * geometry[None, :])
    full_values, full_vectors = np.linalg.eigh(full)
    full_metrics = metrics(full, full_values)
    index = 0 if abs(full_values[0]) >= abs(full_values[-1]) else -1
    vector = np.asarray(full_vectors[:, index], dtype=np.float64)
    selected = float(full_values[index])
    residual = float(np.max(np.abs(full @ vector - selected * vector)))
    blocks = np.arange(WINDOW_COUNT, dtype=np.int64) // BLOCK_COUNT
    band = np.where(np.abs(blocks[:, None] - blocks[None, :]) <=
                    BAND_CUTOFF, full, 0.0)
    tail = full - band
    band_values = np.linalg.eigvalsh(band)
    band_metrics = metrics(band, band_values)
    band_rayleigh = float(vector @ (band @ vector))
    tail_rayleigh = float(vector @ (tail @ vector))
    error = abs(band_rayleigh + tail_rayleigh - selected)
    need(residual <= 6.0e-9 and
         abs(float(np.dot(vector, vector)) - 1.0) <= 5.0e-11 and
         error <= 8.0e-12 and
         float(np.max(np.abs(tail - tail.T))) <= 1.0e-12,
         "eigen/rayleigh replay")
    return {
        "full_spectral": full_metrics["spectral"],
        "full_schur": full_metrics["schur"],
        "band_spectral": band_metrics["spectral"],
        "band_schur": band_metrics["schur"],
        "selected": selected,
        "residual": residual,
        "norm_error": abs(float(np.dot(vector, vector)) - 1.0),
        "band_rayleigh": band_rayleigh,
        "tail_rayleigh": tail_rayleigh,
        "retention": abs(band_rayleigh) / abs(selected),
        "tail_fraction": abs(tail_rayleigh) / abs(selected),
        "band_failure": band_metrics["spectral"] > SPECTRAL_CAP,
        "schur_failure": band_metrics["schur"] > SCHUR_CAP,
        "mode": "minimum_eigenvalue" if index == 0 else "maximum_eigenvalue",
    }


def exact_anchor() -> dict[str, Any]:
    values = list(range(*EXACT_INTERVAL))
    primes = shell_for(EXACT_Q)

    def text(value: Fraction) -> str:
        return f"{value.numerator}/{value.denominator}"

    matrix: list[list[Fraction]] = []
    geometry: list[Fraction] = []
    for u in values:
        row: list[Fraction] = []
        grow = Fraction(0)
        for t in values:
            total = Fraction(0)
            energy = Fraction(0)
            for prime in primes:
                if u == t or u % prime == 0 or t % prime == 0:
                    base = Fraction(0)
                else:
                    centered = Fraction(int((u - t) % prime == 0), 1)
                    centered -= Fraction(1, prime - 1)
                    base = (prime * Fraction(HEIGHT * HEIGHT,
                                             HEIGHT * HEIGHT + (u - t) ** 2)
                            * centered)
                weighted = Fraction(prime, EXACT_Q) ** BETA * base
                total += weighted
                energy += weighted * weighted
            row.append(total)
            grow += energy
        matrix.append(row)
        geometry.append(grow)
    need(all(matrix[i][j] == matrix[j][i]
             for i in range(len(values)) for j in range(len(values))),
         "anchor symmetry")
    need(all(value > 0 for value in geometry), "anchor positivity")
    return {
        "interval": list(EXACT_INTERVAL), "Q": EXACT_Q,
        "kernel_exponent": 1, "beta": BETA, "shell": primes,
        "matrix_symmetric": True, "geometry_positive": True,
        "matrix_digest": hashlib.sha256(canonical([
            [text(value) for value in row] for row in matrix])).hexdigest(),
        "geometry_digest": hashlib.sha256(canonical(
            [text(value) for value in geometry])).hexdigest(),
    }


def validate(document: dict[str, Any]) -> None:
    need(document.get("certificate_version") == 1 and
         document.get("claim_status") == STATUS, "header")
    payload = document.get("payload")
    need(isinstance(payload, dict) and payload.get("schema") == SCHEMA and
         payload.get("status") == STATUS, "schema")
    need(document.get("payload_sha256") == hashlib.sha256(
        canonical(payload)).hexdigest(), "payload hash")
    need(digest(ENGINE_CODE.read_bytes()) == ENGINE_CODE_SHA256,
         "engine lock")
    need(digest(PARENT_CERT.read_bytes()) == PARENT_CERT_SHA256,
         "parent lock")
    parent = json.loads(PARENT_CERT.read_bytes())
    need(parent["payload"]["schema"] ==
         "TPC375_BANDWIDTH_STABILITY_MINIMAL_CUTOFF_V1", "parent schema")
    selection = payload.get("selection_protocol")
    need(selection == {
        "grid_start": 1010001, "grid_step": 401, "grid_count": 41,
        "candidate_rule": "a_j=1010001+401j, 0<=j<41",
        "training_indices": [0, 20, 40],
        "training_origins": [1010001, 1018021, 1026041],
        "holdout_indices": [5, 15, 30],
        "holdout_origins": ORIGINS,
        "holdout_rule": "first three predeclared reserved indices (5,15,30)",
        "response_used_for_selection": False,
        "signed_metric_used_for_selection": False,
    }, "selection protocol")
    protocol = payload.get("protocol")
    need(protocol == {
        "origins": ORIGINS, "window_count": 2048, "block_count": 256,
        "block_indices": list(range(8)),
        "partition": "fixed eight contiguous 256-point blocks",
        "band_cutoff": 1,
        "band_definition": "sum of layers with block distance <= 1",
        "q_anchors": Q_ANCHORS, "kernel_exponents": [1],
        "laws": ["all_plus"], "betas": [2], "height": 66,
        "common_normalization": True, "source_response_used": False,
        "origin_selection_used": False, "row_selection_used": False,
        "mode_rule": "largest absolute eigenvalue; minimum mode wins ties",
        "panel_complete_before_metric_read": True,
    }, "protocol")
    rows = payload.get("rows")
    need(isinstance(rows, list) and len(rows) == 9, "rows")
    need({(r.get("origin"), r.get("Q")) for r in rows} ==
         {(o, q) for o in ORIGINS for q in Q_ANCHORS}, "row keys")
    need(payload.get("exact_anchor") == exact_anchor(), "exact anchor")
    jobs = [(origin, q0) for origin in ORIGINS for q0 in Q_ANCHORS]
    with ThreadPoolExecutor(max_workers=3) as pool:
        values = list(pool.map(lambda job: replay(job[0], job[1]), jobs))
    independent = [(job[0], job[1], value)
                   for job, value in zip(jobs, values)]
    for origin, q0, actual in independent:
        row = next(r for r in rows if r["origin"] == origin and r["Q"] == q0)
        for field, value in (
                ("spectral", actual["full_spectral"]),
                ("schur", actual["full_schur"])):
            close(value, row["full"][field], f"{origin}/{q0}/full/{field}")
        for field, value in (
                ("spectral", actual["band_spectral"]),
                ("schur", actual["band_schur"])):
            close(value, row["band"][field], f"{origin}/{q0}/band/{field}")
        close(actual["retention"],
              row["mode"]["band_rayleigh_abs_retention"],
              f"{origin}/{q0}/retention")
        close(actual["tail_fraction"],
              row["mode"]["tail_rayleigh_abs_fraction"],
              f"{origin}/{q0}/tail")
        close(actual["residual"], row["mode"]["eigen_residual_inf"],
              f"{origin}/{q0}/residual", 2.0e-5)
        need(actual["band_failure"] == row["band_failure"],
             f"{origin}/{q0}/failure")
        need(actual["mode"] == row["mode"]["selected_mode"],
             f"{origin}/{q0}/mode")
    phase = payload["phase_summary"]
    need(phase["spectral_cap_violations"] == 6 and
         phase["schur_cap_violations"] == 0 and
         phase["failure_profile_by_Q"] == [0, 3, 3],
         "phase profile")
    audit = payload["finite_audit"]
    need(audit["rows"] == 9 and audit["spectral_cap_violations"] == 6 and
         audit["schur_cap_violations"] == 0 and
         audit["failure_profile_by_Q"] == [0, 3, 3] and
         audit["fixed_power_credit"] == 0 and
         audit["arithmetic_advance"] == "NO", "audit")
    need(payload["round2_clue"] == "TEST_C1_WINDOW_SCALE_HOLDOUT", "clue")


def main() -> int:
    if sys.argv[1:] != ["--check"]:
        raise SystemExit("--check is the only argument")
    try:
        raw = CERTIFICATE.read_bytes()
        document = json.loads(raw)
        need(raw == canonical(document), "certificate canonicality")
        validate(document)
        print("TPC376_INDEPENDENT_CHECK=PASS rows=9 failures=6 profile=0,3,3")
        return 0
    except (Failure, OSError, ValueError, TypeError, KeyError,
            json.JSONDecodeError) as error:
        print("TPC376_INDEPENDENT_CHECK=FAIL " + str(error), file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
