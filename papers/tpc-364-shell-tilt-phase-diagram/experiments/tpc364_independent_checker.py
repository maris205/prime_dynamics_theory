#!/usr/bin/env python3
"""Reverse-shell independent checker for the TPC-364 certificate."""

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
PROJECT = ROOT / "papers/tpc-364-shell-tilt-phase-diagram"
CERTIFICATE = PROJECT / "results/tpc364_certificate.json"
BASE_CODE = ROOT / (
    "papers/tpc-355-position-aware-mask-energy-normalization/code/"
    "tpc355_position_aware_mask_energy_normalization.py")
BASE_SHA256 = (
    "b54883cbc2e9e19dd8cf6fbece69ff7752ba805678e0b5b2fcf82949dd42fde9")

SCHEMA = "TPC364_SHELL_TILT_PHASE_DIAGRAM_V1"
STATUS = "NUMERICALLY_CERTIFIED_FINITE_SHELL_TILT_PHASE_DIAGRAM"
ORIGINS = (313030, 311166, 321651)
COUNTS = (256, 512)
Q_ANCHORS = (80, 128, 256, 512)
EXPONENTS = (1, 2)
LAWS = ("all_plus", "alternating_index", "mod4_character", "half_split")
BETAS = (-2, -1, 0, 1, 2)
HEIGHT = 66
SPECTRAL_CAP = 0.64
SCHUR_CAP = 0.83
EXACT_INTERVAL = (313060, 313073)


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


def show(value: float) -> str:
    return format(float(value), ".17g")


def primes_up_to(limit: int) -> list[int]:
    sieve = bytearray(b"\x01") * (limit + 1)
    sieve[0] = 0
    sieve[1] = 0
    for prime in range(2, math.isqrt(limit) + 1):
        if sieve[prime]:
            start = prime * prime
            sieve[start:limit + 1:prime] = b"\x00" * (
                (limit - start) // prime + 1)
    return [value for value in range(2, limit + 1) if sieve[value]]


PRIMES = primes_up_to(50_000)


def shell_for(q0: int) -> list[int]:
    return [prime for prime in PRIMES if q0 < prime <= 2 * q0]


def sign_patterns(primes: list[int]) -> dict[str, np.ndarray]:
    return {
        "all_plus": np.ones(len(primes), dtype=np.float64),
        "alternating_index": np.asarray(
            [1.0 if i % 2 == 0 else -1.0
             for i in range(len(primes))], dtype=np.float64),
        "mod4_character": np.asarray(
            [1.0 if prime % 4 == 1 else -1.0
             for prime in primes], dtype=np.float64),
        "half_split": np.asarray(
            [1.0 if i < len(primes) / 2 else -1.0
             for i in range(len(primes))], dtype=np.float64),
    }


def reverse_components(values: np.ndarray, q0: int, exponent: int,
                       beta: int):
    difference = values[:, None] - values[None, :]
    distance = difference.astype(np.float64)
    kernel = (float(HEIGHT) ** (2 * exponent) /
              (HEIGHT * HEIGHT + distance * distance) ** exponent)
    np.fill_diagonal(kernel, 0.0)
    primes = shell_for(q0)
    signs = sign_patterns(primes)
    matrices = {law: np.zeros((len(values), len(values)), dtype=np.float64)
                for law in LAWS}
    geometry = np.zeros(len(values), dtype=np.float64)
    weights: list[float] = []
    # The reverse order is intentional: it does not import the producer's
    # accumulation order.
    for index in range(len(primes) - 1, -1, -1):
        prime = primes[index]
        weight = (float(prime) / float(q0)) ** beta
        weights.insert(0, weight)
        centered = ((difference % prime == 0).astype(np.float64) -
                    1.0 / (prime - 1))
        np.fill_diagonal(centered, 0.0)
        valid = ((difference != 0) &
                 (values[:, None] % prime != 0) &
                 (values[None, :] % prime != 0))
        block = weight * float(prime) * kernel * centered * valid
        geometry += np.sum(block * block, axis=1)
        for law in LAWS:
            matrices[law] += signs[law][index] * block
    for matrix in matrices.values():
        matrix[:] = (matrix + matrix.T) / 2.0
    need(bool(np.all(np.isfinite(geometry) & (geometry > 0))),
         "geometry")
    return primes, matrices, geometry, weights


def metrics(matrix: np.ndarray) -> dict[str, Any]:
    symmetry = float(np.max(np.abs(matrix - matrix.T)))
    row_mass = np.sum(np.abs(matrix), axis=1)
    schur = float(np.max(row_mass))
    frobenius = float(np.sqrt(np.sum(matrix * matrix)))
    need(math.isfinite(symmetry) and symmetry <= 1.0e-12 and
         schur > 0.0 and math.isfinite(frobenius) and frobenius > 0.0,
         "metrics")
    eigenvalues = np.linalg.eigvalsh(matrix)
    lo, hi = float(eigenvalues[0]), float(eigenvalues[-1])
    spectral = max(abs(lo), abs(hi))
    need(math.isfinite(spectral) and spectral > 0.0 and
         spectral <= schur + 3.0e-9 * max(1.0, schur) and
         spectral <= frobenius + 3.0e-9 * max(1.0, frobenius),
         "spectral envelopes")
    return {
        "schur": schur, "frobenius": frobenius, "spectral": spectral,
        "minimum_eigenvalue": lo, "maximum_eigenvalue": hi,
        "symmetry_error": symmetry,
        "spectral_over_schur": spectral / schur,
        "spectral_over_frobenius": spectral / frobenius,
        "schur_row_index": int(np.argmax(row_mass)),
    }


def close(actual: float, recorded: Any, label: str) -> None:
    target = float(recorded)
    need(abs(float(actual) - target) <= 4.0e-6 *
         max(1.0, abs(float(actual)), abs(target)), label)


def exact_anchor_check(payload: dict[str, Any]) -> None:
    values = list(range(EXACT_INTERVAL[0], EXACT_INTERVAL[1] + 1))
    primes = shell_for(4)
    text = lambda value: f"{value.numerator}/{value.denominator}"
    expected: list[dict[str, Any]] = []
    for beta in BETAS:
        matrix: list[list[Fraction]] = []
        geometry: list[Fraction] = []
        for u in values:
            row: list[Fraction] = []
            grow = Fraction(0)
            for t in values:
                total = Fraction(0)
                energy = Fraction(0)
                for prime in primes:
                    base = Fraction(0) if u == t else (
                        Fraction(0) if u % prime == 0 or t % prime == 0 else
                        Fraction(int((u - t) % prime == 0), 1) -
                        Fraction(1, prime - 1))
                    if base != 0:
                        base *= Fraction(prime * HEIGHT * HEIGHT,
                                          HEIGHT * HEIGHT + (u - t) ** 2)
                    weight = Fraction(prime, 4) ** beta
                    total += weight * base
                    energy += (weight * base) ** 2
                row.append(total)
                grow += energy
            matrix.append(row)
            geometry.append(grow)
        expected.append({
            "beta": beta, "interval": list(EXACT_INTERVAL), "Q": 4,
            "kernel_exponent": 1, "shell": primes,
            "matrix_symmetric": True, "geometry_positive": True,
            "matrix_digest": hashlib.sha256(canonical([
                [text(value) for value in row] for row in matrix])).hexdigest(),
            "geometry_digest": hashlib.sha256(canonical(
                [text(value) for value in geometry])).hexdigest(),
        })
    need(payload.get("exact_anchor") == {"anchors": expected},
         "exact anchor")


def validate_header(document: dict[str, Any]) -> dict[str, Any]:
    need(document.get("certificate_version") == 1 and
         document.get("claim_status") == STATUS, "header")
    payload = document.get("payload")
    need(isinstance(payload, dict) and payload.get("schema") == SCHEMA,
         "schema")
    need(document.get("payload_sha256") == hashlib.sha256(
        canonical(payload)).hexdigest(), "payload hash")
    protocol = payload.get("protocol", {})
    need(protocol.get("origins") == list(ORIGINS) and
         protocol.get("counts") == list(COUNTS) and
         protocol.get("q_anchors") == list(Q_ANCHORS) and
         protocol.get("kernel_exponents") == list(EXPONENTS) and
         protocol.get("laws") == list(LAWS) and
         protocol.get("betas") == list(BETAS) and
         protocol.get("spectra_for_all_laws") is True and
         protocol.get("source_response_used") is False, "protocol")
    need(digest(BASE_CODE.read_bytes()) == BASE_SHA256, "base provenance")
    rows = payload.get("rows")
    need(isinstance(rows, list) and len(rows) == 960, "rows")
    need(len({(row.get("origin"), row.get("count"), row.get("Q"),
               row.get("kernel_exponent"), row.get("beta"), row.get("law"))
              for row in rows}) == 960, "row keys")
    need(payload.get("row_digest") == hashlib.sha256(
        canonical(rows)).hexdigest(), "row digest")
    firewall = payload.get("claim_firewall", {})
    expected = {
        "TPC364_WEIGHTED_BLOCK_DEFINITION": "PROVED_EXACT_FINITE",
        "TPC364_WEIGHTED_GEOMETRY_POSITIVITY": "PROVED_EXACT_FINITE",
        "TPC364_FINITE_REPLAY": "NUMERICALLY_CERTIFIED_FINITE_960_ROWS",
        "TPC364_PHASE_DIAGRAM": "NUMERICALLY_CERTIFIED_FINITE_SCOPED",
        "TPC364_BETA2_PANEL_CAP_REPAIR": "NUMERICALLY_CERTIFIED_FINITE_SCOPED",
        "TPC364_BETA2_ASYMPTOTIC_REPAIR": "OPEN",
        "TPC364_NORMALIZATION_SOURCE_VALIDITY": "MODELING_CHOICE_OPEN",
        "TPC364_GROWING_OPERATOR_BOUND": "OPEN",
        "TPC364_SOURCE_UNIFORM_L2": "OPEN",
        "TPC364_ARITHMETIC_ADVANCE": "NO",
        "TPC364_FIXED_POWER_CREDIT": 0,
        "TPC364_FULL_GATE_B": "OPEN", "TPC364_TWIN_PRIME_RESULT": "NONE",
    }
    for key, value in expected.items():
        need(firewall.get(key) == value, "firewall " + key)
    return payload


def main() -> int:
    if sys.argv[1:] != ["--check"]:
        raise SystemExit("--check is the only argument")
    try:
        document = json.loads(CERTIFICATE.read_bytes())
        payload = validate_header(document)
        exact_anchor_check(payload)
        recorded = {(row["origin"], row["count"], row["Q"],
                     row["kernel_exponent"], row["beta"], row["law"]): row
                    for row in payload["rows"]}
        checked = 0
        phase_violations = {beta: 0 for beta in BETAS}
        for beta in BETAS:
            for origin in ORIGINS:
                for count in COUNTS:
                    values = np.arange(origin, origin + count,
                                       dtype=np.int64)
                    for q0 in Q_ANCHORS:
                        for exponent in EXPONENTS:
                            primes, matrices, geometry, weights = \
                                reverse_components(values, q0, exponent, beta)
                            scale = np.sqrt(geometry[:, None] * geometry[None, :])
                            for law in LAWS:
                                key = (origin, count, q0, exponent, beta, law)
                                row = recorded[key]
                                need(row["shell"] == primes and
                                     row["shell_cardinality"] == len(primes),
                                     "shell")
                                close(float(min(weights)), row["weight_min"],
                                      "weight min")
                                close(float(max(weights)), row["weight_max"],
                                      "weight max")
                                participation = (sum(x * x for x in weights) ** 2 /
                                                 sum(x ** 4 for x in weights))
                                close(participation,
                                      row["weight_effective_count"],
                                      "effective count")
                                close(float(np.min(geometry)), row["geometry_min"],
                                      "geometry min")
                                close(float(np.max(geometry)), row["geometry_max"],
                                      "geometry max")
                                matrix = matrices[law]
                                norm = matrix / scale
                                for label, actual in (
                                        ("raw", metrics(matrix)),
                                        ("normalized", metrics(norm))):
                                    target = row[label]
                                    for field in ("schur", "frobenius", "spectral",
                                                  "minimum_eigenvalue",
                                                  "maximum_eigenvalue",
                                                  "spectral_over_schur",
                                                  "spectral_over_frobenius"):
                                        close(actual[field], target[field],
                                              label + " " + field)
                                    need(actual["schur_row_index"] ==
                                         target["schur_row_index"],
                                         label + " row index")
                                if float(row["normalized"]["spectral"]) > \
                                        SPECTRAL_CAP:
                                    phase_violations[beta] += 1
                                checked += 1
        need(checked == 960 and phase_violations == {
            -2: 63, -1: 36, 0: 30, 1: 30, 2: 0},
             "phase census")
        need(payload["phase_summary"]["cap_repair_betas"] == [2],
             "repair beta")
        need(payload["finite_audit"]["beta2_cap_repair_rows"] == 192 and
             payload["finite_audit"]["beta2_total_rows"] == 192,
             "beta2 rows")
        print("TPC364_INDEPENDENT_CHECK=PASS rows=960 betas=5 "
              "beta2_violations=0 baseline_beta0_violations=30")
        return 0
    except (Failure, OSError, ValueError, TypeError, KeyError,
            json.JSONDecodeError, np.linalg.LinAlgError) as error:
        print("TPC364_INDEPENDENT_CHECK=FAIL " + str(error), file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
