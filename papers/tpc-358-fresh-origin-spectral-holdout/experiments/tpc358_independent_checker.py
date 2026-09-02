#!/usr/bin/env python3
"""Independent reverse-shell replay for TPC-358.

The producer is not imported.  Fresh origins, masks, geometry, envelopes and
the all-plus spectrum are rebuilt with reverse shell accumulation.
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
PROJECT = ROOT / "papers/tpc-358-fresh-origin-spectral-holdout"
CERTIFICATE = PROJECT / "results/tpc358_certificate.json"
BASE_CODE = ROOT / (
    "papers/tpc-355-position-aware-mask-energy-normalization/code/"
    "tpc355_position_aware_mask_energy_normalization.py")
PARENT_CODE = ROOT / (
    "papers/tpc-357-operator-norm-scale-ladder/code/"
    "tpc357_operator_norm_scale_ladder.py")
PARENT_CERT = ROOT / (
    "papers/tpc-357-operator-norm-scale-ladder/results/tpc357_certificate.json")
BASE_CODE_SHA256 = (
    "b54883cbc2e9e19dd8cf6fbece69ff7752ba805678e0b5b2fcf82949dd42fde9")
PARENT_CODE_SHA256 = (
    "44217207664b8bf08218458f102dacbdb03cf48c85a6fa0d72e7f23fe84a36a1")
PARENT_CERT_SHA256 = (
    "9eda189321af2233b6ff39eed97f8ead46ebe6853556b6baf3614e752a6e5fee")
SCHEMA = "TPC358_FRESH_ORIGIN_SPECTRAL_HOLDOUT_V1"
STATUS = "NUMERICALLY_CERTIFIED_FINITE_FRESH_ORIGIN_SPECTRAL_HOLDOUT"
ORIGINS = (52_001, 120_001, 220_001)
COUNTS = (256, 512, 1024, 2048)
Q_ANCHORS = (24, 54, 80)
EXPONENTS = (1, 2)
LAW_NAMES = ("all_plus", "alternating_index", "mod4_character", "half_split")
SPECTRAL_LAWS = ("all_plus",)
HEIGHT = 66
BOUND_TOL = 3.0e-5
EXACT_INTERVAL = (52_031, 52_044)
EXACT_Q = 4
EXACT_EXPONENT = 1


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


def close(actual: float, recorded: Any, label: str) -> None:
    try:
        target = float(recorded)
    except (TypeError, ValueError) as error:
        raise Failure(label + " nonnumeric") from error
    need(math.isfinite(actual) and math.isfinite(target), label + " nonfinite")
    need(abs(actual - target) <= BOUND_TOL * max(1.0, abs(actual), abs(target)),
         label + " mismatch")


def primes_up_to(limit: int) -> list[int]:
    sieve = bytearray(b"\x01") * (limit + 1)
    sieve[0] = sieve[1] = 0
    for prime in range(2, math.isqrt(limit) + 1):
        if sieve[prime]:
            start = prime * prime
            sieve[start:limit + 1:prime] = b"\x00" * (
                (limit - start) // prime + 1)
    return [value for value in range(2, limit + 1) if sieve[value]]


TAIL_PRIMES = primes_up_to(50_000)


def shell(q0: int) -> list[int]:
    return [prime for prime in TAIL_PRIMES if q0 < prime <= 2 * q0]


def sign_map(primes: list[int]) -> dict[str, np.ndarray]:
    return {
        "all_plus": np.ones(len(primes), dtype=np.float64),
        "alternating_index": np.asarray(
            [1.0 if index % 2 == 0 else -1.0
             for index in range(len(primes))]),
        "mod4_character": np.asarray(
            [1.0 if prime % 4 == 1 else -1.0 for prime in primes]),
        "half_split": np.asarray(
            [1.0 if index < len(primes) / 2 else -1.0
             for index in range(len(primes))]),
    }


def reverse_components(origin: int, count: int, q0: int, exponent: int
                       ) -> tuple[list[int], dict[str, np.ndarray], np.ndarray]:
    values = np.arange(origin, origin + count, dtype=np.int64)
    difference = values[:, None] - values[None, :]
    distance = difference.astype(np.float64)
    kernel = (float(HEIGHT) ** (2 * exponent) /
              (HEIGHT * HEIGHT + distance * distance) ** exponent)
    np.fill_diagonal(kernel, 0.0)
    primes = shell(q0)
    signs = sign_map(primes)
    matrices = {law: np.zeros((count, count), dtype=np.float64)
                for law in LAW_NAMES}
    geometry = np.zeros(count, dtype=np.float64)
    for index, prime in reversed(list(enumerate(primes))):
        centered = ((difference % prime == 0).astype(np.float64) -
                    1.0 / (prime - 1))
        np.fill_diagonal(centered, 0.0)
        valid = ((difference != 0) & (values[:, None] % prime != 0) &
                 (values[None, :] % prime != 0))
        block = float(prime) * kernel * centered * valid
        geometry += np.sum(block * block, axis=1)
        for law in LAW_NAMES:
            matrices[law] += signs[law][index] * block
    for law in LAW_NAMES:
        matrices[law] = (matrices[law] + matrices[law].T) / 2.0
    need(bool(np.all(np.isfinite(geometry) & (geometry > 0))),
         "reverse geometry positivity")
    return primes, matrices, geometry


def metrics(matrix: np.ndarray, spectrum: bool) -> dict[str, Any]:
    symmetry = float(np.max(np.abs(matrix - matrix.T)))
    need(symmetry <= 1.0e-12, "reverse symmetry")
    schur = float(np.max(np.sum(np.abs(matrix), axis=1)))
    frobenius = float(np.sqrt(np.sum(matrix * matrix)))
    result: dict[str, Any] = {
        "schur_row_sum_bound": show(schur),
        "frobenius_bound": show(frobenius),
        "symmetry_error": show(symmetry),
        "spectral_norm": None,
        "minimum_eigenvalue": None,
        "maximum_eigenvalue": None,
        "spectral_over_schur": None,
        "spectral_over_frobenius": None,
    }
    if spectrum:
        eigenvalues = np.linalg.eigvalsh(matrix)
        lo, hi = float(eigenvalues[0]), float(eigenvalues[-1])
        spectral = max(abs(lo), abs(hi))
        need(spectral <= schur + BOUND_TOL and
             spectral <= frobenius + BOUND_TOL, "reverse envelope")
        result.update({
            "spectral_norm": show(spectral),
            "minimum_eigenvalue": show(lo),
            "maximum_eigenvalue": show(hi),
            "spectral_over_schur": show(spectral / schur),
            "spectral_over_frobenius": show(spectral / frobenius),
        })
    return result


def exact_entry(prime: int, u: int, t: int, exponent: int) -> Fraction:
    if u == t or u % prime == 0 or t % prime == 0:
        return Fraction(0)
    centered = Fraction(int((u - t) % prime == 0), 1)
    centered -= Fraction(1, prime - 1)
    return (prime * Fraction(HEIGHT ** (2 * exponent),
                             (HEIGHT * HEIGHT + (u - t) ** 2) ** exponent)
            * centered)


def exact_anchor() -> dict[str, Any]:
    values = list(range(EXACT_INTERVAL[0], EXACT_INTERVAL[1] + 1))
    primes = shell(EXACT_Q)
    matrix = [[sum((exact_entry(prime, u, t, EXACT_EXPONENT)
                    for prime in primes), Fraction(0))
               for t in values] for u in values]
    row_sums = [sum((abs(value) for value in row), Fraction(0))
                for row in matrix]
    geometry = [sum((exact_entry(prime, u, t, EXACT_EXPONENT) ** 2
                     for prime in primes for t in values), Fraction(0))
                for u in values]
    need(all(matrix[i][j] == matrix[j][i]
             for i in range(len(values)) for j in range(len(values))),
         "exact symmetry")
    need(all(value > 0 for value in geometry), "exact geometry")

    def text(value: Fraction) -> str:
        return f"{value.numerator}/{value.denominator}"

    return {
        "row_sums_digest": hashlib.sha256(canonical(
            [text(value) for value in row_sums])).hexdigest(),
        "geometry_digest": hashlib.sha256(canonical(
            [text(value) for value in geometry])).hexdigest(),
        "matrix_symmetric": True, "geometry_positive": True,
        "shell": primes,
    }


def load_certificate() -> dict[str, Any]:
    raw = CERTIFICATE.read_bytes()
    document = json.loads(raw)
    need(raw == canonical(document), "certificate canonicality")
    need(document.get("certificate_version") == 1 and
         document.get("claim_status") == STATUS, "certificate header")
    payload = document.get("payload")
    need(isinstance(payload, dict) and payload.get("schema") == SCHEMA,
         "certificate schema")
    need(document.get("payload_sha256") == hashlib.sha256(
        canonical(payload)).hexdigest(), "certificate payload hash")
    return payload


def check_static(payload: dict[str, Any]) -> None:
    for path, expected, label in (
            (BASE_CODE, BASE_CODE_SHA256, "TPC355 code"),
            (PARENT_CODE, PARENT_CODE_SHA256, "TPC357 code"),
            (PARENT_CERT, PARENT_CERT_SHA256, "TPC357 certificate")):
        need(path.is_file() and digest(path.read_bytes()) == expected,
             label + " provenance")
    lock = payload.get("parent_lock", {})
    need(lock.get("TPC355_code_sha256") == BASE_CODE_SHA256 and
         lock.get("TPC357_code_sha256") == PARENT_CODE_SHA256 and
         lock.get("TPC357_certificate_sha256") == PARENT_CERT_SHA256,
         "parent lock")
    protocol = payload.get("protocol", {})
    need(protocol.get("origins") == list(ORIGINS) and
         protocol.get("counts") == list(COUNTS) and
         protocol.get("q_anchors") == list(Q_ANCHORS) and
         protocol.get("kernel_exponents") == list(EXPONENTS) and
         protocol.get("laws") == list(LAW_NAMES) and
         protocol.get("spectral_laws") == list(SPECTRAL_LAWS) and
         protocol.get("source_response_used") is False and
         protocol.get("disjoint_from_tpc356") is True,
         "protocol")
    rows = payload.get("rows")
    need(isinstance(rows, list) and len(rows) == 288, "row census")
    keys = {(row.get("origin"), row.get("count"), row.get("Q"),
             row.get("kernel_exponent"), row.get("law")) for row in rows}
    need(len(keys) == 288, "row uniqueness")
    need(payload.get("row_digest") == hashlib.sha256(
        canonical(rows)).hexdigest(), "row digest")
    audit = payload.get("finite_audit", {})
    need(audit.get("rows") == 288 and
         audit.get("origins") == 3 and
         audit.get("all_plus_spectral_rows") == 72 and
         audit.get("finite_schur_violations") == 0 and
         audit.get("finite_frobenius_violations") == 0 and
         audit.get("fixed_power_credit") == 0 and
         audit.get("arithmetic_advance") == "NO",
         "finite audit")
    need(float(audit["normalized_schur_max"]) < 0.83 and
         float(audit["normalized_all_plus_spectral_max"]) < 0.64 and
         float(audit["raw_all_plus_spectral_max"]) > 1500.0,
         "finite thresholds")
    census = payload.get("scale_transition_audit", {}).get("census", {})
    need(census.get("normalized_spectral", {}).get("increase", 0) > 0 and
         census.get("normalized_spectral", {}).get("decrease", 0) > 0,
         "scale obstruction")
    firewall = payload.get("claim_firewall", {})
    for key, value in (
            ("TPC358_FINITE_SCHUR_ENVELOPE", "PROVED_EXACT_FINITE"),
            ("TPC358_FINITE_FROBENIUS_ENVELOPE", "PROVED_EXACT_FINITE"),
            ("TPC358_FRESH_ORIGIN_REPLAY", "NUMERICALLY_CERTIFIED_FINITE_288_ROWS"),
            ("TPC358_PARENT_CAP_TRANSFER", "NUMERICALLY_CERTIFIED_FINITE_SCOPED"),
            ("TPC358_NORMALIZED_SCHUR_CAP", "NUMERICALLY_CERTIFIED_FINITE_SCOPED"),
            ("TPC358_ALL_PLUS_SPECTRAL_CAP", "NUMERICALLY_CERTIFIED_FINITE_SCOPED"),
            ("TPC358_SCALE_MONOTONE_DECAY", "REFUTED_SCOPED_ON_DECLARED_LADDER"),
            ("TPC358_GROWING_OPERATOR_BOUND", "OPEN"),
            ("TPC358_SOURCE_UNIFORM_L2", "OPEN"),
            ("TPC358_ARITHMETIC_ADVANCE", "NO"),
            ("TPC358_FULL_GATE_B", "OPEN"),
            ("TPC358_TWIN_PRIME_RESULT", "NONE")):
        need(firewall.get(key) == value, "firewall " + key)


def replay(payload: dict[str, Any]) -> None:
    expected = {(row["origin"], row["count"], row["Q"],
                 row["kernel_exponent"], row["law"]): row
                for row in payload["rows"]}
    for origin in ORIGINS:
        for count in COUNTS:
            values = np.arange(origin, origin + count, dtype=np.int64)
            for q0 in Q_ANCHORS:
                for exponent in EXPONENTS:
                    primes, matrices, geometry = reverse_components(
                        origin, count, q0, exponent)
                    scale = np.sqrt(geometry[:, None] * geometry[None, :])
                    for law in LAW_NAMES:
                        row = expected[(origin, count, q0, exponent, law)]
                        need(row["shell"] == primes and
                             row["shell_cardinality"] == len(primes),
                             "shell metadata")
                        normalized = matrices[law] / scale
                        spectrum = law in SPECTRAL_LAWS
                        actual_raw = metrics(matrices[law], spectrum)
                        actual_norm = metrics(normalized, spectrum)
                        close(float(np.min(geometry)),
                              row["unsigned_geometry_energy_min"],
                              "geometry min")
                        close(float(np.max(geometry)),
                              row["unsigned_geometry_energy_max"],
                              "geometry max")
                        close(float(np.max(geometry) / np.min(geometry)),
                              row["unsigned_geometry_spread"],
                              "geometry spread")
                        for family, actual in (("raw_metrics", actual_raw),
                                               ("normalized_metrics", actual_norm)):
                            recorded = row[family]
                            for field in ("schur_row_sum_bound",
                                          "frobenius_bound", "symmetry_error"):
                                close(float(actual[field]), recorded[field],
                                      family + "/" + field)
                            if spectrum:
                                for field in ("spectral_norm",
                                              "minimum_eigenvalue",
                                              "maximum_eigenvalue",
                                              "spectral_over_schur",
                                              "spectral_over_frobenius"):
                                    close(float(actual[field]), recorded[field],
                                          family + "/" + field)
                            else:
                                need(recorded["spectral_norm"] is None,
                                     "unexpected spectral row")
    anchor = exact_anchor()
    recorded = payload["exact_anchor"]
    for field in ("row_sums_digest", "geometry_digest", "shell"):
        need(anchor[field] == recorded.get(field), "exact anchor " + field)


def main() -> int:
    if any(arg != "--check" for arg in sys.argv[1:]) or len(sys.argv) != 2:
        raise SystemExit("--check is the only argument")
    try:
        payload = load_certificate()
        check_static(payload)
        replay(payload)
        print("TPC358_INDEPENDENT_CHECK=PASS rows=288 spectral_rows=72 "
              "fresh_origins=3 reverse_shell=1")
        return 0
    except (Failure, OSError, ValueError, TypeError, KeyError,
            json.JSONDecodeError, np.linalg.LinAlgError) as error:
        print("TPC358_INDEPENDENT_CHECK=FAIL " + str(error), file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
