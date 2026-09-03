#!/usr/bin/env python3
"""Independent reverse-shell checker for the TPC-363 finite certificate."""

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
PROJECT = ROOT / "papers/tpc-363-bulk-persistence-localization"
CERTIFICATE = PROJECT / "results/tpc363_certificate.json"
BASE_CODE = ROOT / (
    "papers/tpc-355-position-aware-mask-energy-normalization/code/"
    "tpc355_position_aware_mask_energy_normalization.py")
PARENT_CERT = ROOT / (
    "papers/tpc-362-shell-scale-cap-obstruction/results/"
    "tpc362_certificate.json")

BASE_SHA256 = (
    "b54883cbc2e9e19dd8cf6fbece69ff7752ba805678e0b5b2fcf82949dd42fde9")
PARENT_CERT_SHA256 = (
    "7780856a7394f8060121dd41fc7a0b7cd066cd2c858e8b2a4891090e5577a4a6")
SCHEMA = "TPC363_BULK_PERSISTENCE_LOCALIZATION_V1"
STATUS = "NUMERICALLY_CERTIFIED_FINITE_BULK_PERSISTENCE_OBSTRUCTION"
ORIGINS = (313030, 311166, 321651)
COUNTS = (256, 512)
Q_ANCHORS = (80, 128, 256)
EXPONENTS = (1, 2)
LAWS = ("all_plus", "alternating_index", "mod4_character", "half_split")
HEIGHT = 66
SPECTRAL_CAP = 0.64
TRIM_DENOMINATOR = 20
TOL = 8.0e-5
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


def close(actual: float, recorded: Any, label: str) -> None:
    target = float(recorded)
    need(abs(float(actual) - target) <= TOL *
         max(1.0, abs(float(actual)), abs(target)), label)


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


PRIMES = primes_up_to(50000)


def shell(q0: int) -> list[int]:
    return [prime for prime in PRIMES if q0 < prime <= 2 * q0]


def signs(prime_shell: list[int]) -> dict[str, np.ndarray]:
    return {
        "all_plus": np.ones(len(prime_shell), dtype=np.float64),
        "alternating_index": np.asarray(
            [1.0 if i % 2 == 0 else -1.0
             for i in range(len(prime_shell))]),
        "mod4_character": np.asarray(
            [1.0 if prime % 4 == 1 else -1.0 for prime in prime_shell]),
        "half_split": np.asarray(
            [1.0 if i < len(prime_shell) / 2 else -1.0
             for i in range(len(prime_shell))], dtype=np.float64),
    }


def reverse_components(origin: int, count: int, q0: int, exponent: int):
    values = np.arange(origin, origin + count, dtype=np.int64)
    difference = values[:, None] - values[None, :]
    distance = difference.astype(np.float64)
    kernel = (float(HEIGHT) ** (2 * exponent) /
              (HEIGHT * HEIGHT + distance * distance) ** exponent)
    np.fill_diagonal(kernel, 0.0)
    prime_shell = shell(q0)
    sign = signs(prime_shell)
    matrices = {law: np.zeros((count, count), dtype=np.float64)
                for law in LAWS}
    geometry = np.zeros(count, dtype=np.float64)
    for index in range(len(prime_shell) - 1, -1, -1):
        prime = prime_shell[index]
        centered = ((difference % prime == 0).astype(np.float64) -
                    1.0 / (prime - 1))
        np.fill_diagonal(centered, 0.0)
        valid = ((difference != 0) &
                 (values[:, None] % prime != 0) &
                 (values[None, :] % prime != 0))
        block = float(prime) * kernel * centered * valid
        geometry += np.sum(block * block, axis=1)
        for law in LAWS:
            matrices[law] += sign[law][index] * block
    for law in LAWS:
        matrices[law] = (matrices[law] + matrices[law].T) / 2.0
    need(bool(np.all(np.isfinite(geometry) & (geometry > 0))), "geometry")
    return prime_shell, matrices, geometry


def top_indices(values: np.ndarray, count: int) -> list[int]:
    return [int(index) for index in
            np.argsort(-np.asarray(values), kind="mergesort")[:count]]


def restricted_spectral(matrix: np.ndarray, removed: list[int]) -> float:
    keep = np.ones(matrix.shape[0], dtype=bool)
    keep[np.asarray(removed, dtype=np.int64)] = False
    reduced = matrix[np.ix_(keep, keep)]
    ev = np.linalg.eigvalsh(reduced)
    return max(abs(float(ev[0])), abs(float(ev[-1])))


def metrics(matrix: np.ndarray) -> dict[str, Any]:
    symmetry = float(np.max(np.abs(matrix - matrix.T)))
    row_mass = np.sum(np.abs(matrix), axis=1)
    schur = float(np.max(row_mass))
    frobenius = float(np.sqrt(np.sum(matrix * matrix)))
    ev, vectors = np.linalg.eigh(matrix)
    principal = int(np.argmax(np.abs(ev)))
    vector_mass = vectors[:, principal] ** 2
    spectral = max(abs(float(ev[0])), abs(float(ev[-1])))
    trim_count = max(1, matrix.shape[0] // TRIM_DENOMINATOR)
    schur_indices = top_indices(row_mass, trim_count)
    eigen_indices = top_indices(vector_mass, trim_count)
    trimmed_schur = restricted_spectral(matrix, schur_indices)
    trimmed_eigen = restricted_spectral(matrix, eigen_indices)
    return {
        "schur": schur, "frobenius": frobenius, "spectral": spectral,
        "minimum_eigenvalue": float(ev[0]),
        "maximum_eigenvalue": float(ev[-1]), "symmetry_error": symmetry,
        "spectral_over_schur": spectral / schur,
        "spectral_over_frobenius": spectral / frobenius,
        "schur_row_index": int(np.argmax(row_mass)),
        "schur_row_mass": schur,
        "principal_eigen_index": principal,
        "principal_eigenvector_top1_mass": float(np.max(vector_mass)),
        "principal_eigenvector_top5_mass": float(
            np.sort(vector_mass)[-min(5, len(vector_mass)):].sum()),
        "principal_eigenvector_ipr": float(np.sum(vector_mass ** 2)),
        "principal_eigenvector_effective_support": float(
            1.0 / np.sum(vector_mass ** 2)),
        "principal_eigenvector_schur_alignment": float(
            vector_mass[int(np.argmax(row_mass))]),
        "trim_count": trim_count,
        "schur_trim_indices": schur_indices,
        "eigenvector_trim_indices": eigen_indices,
        "trimmed_spectral_after_schur_rows": trimmed_schur,
        "trimmed_spectral_after_eigenvector_rows": trimmed_eigen,
        "trimmed_ratio_after_schur_rows": trimmed_schur / spectral,
        "trimmed_ratio_after_eigenvector_rows": trimmed_eigen / spectral,
    }


def check_exact_anchor(recorded: dict[str, Any]) -> None:
    values = list(range(EXACT_INTERVAL[0], EXACT_INTERVAL[1] + 1))
    prime_shell = shell(4)

    def entry(prime: int, u: int, t: int) -> Fraction:
        if u == t or u % prime == 0 or t % prime == 0:
            return Fraction(0)
        centered = Fraction(int((u - t) % prime == 0), 1) - Fraction(
            1, prime - 1)
        return prime * Fraction(HEIGHT * HEIGHT,
                                HEIGHT * HEIGHT + (u - t) ** 2) * centered

    matrix = [[sum((entry(p, u, t) for p in prime_shell), Fraction(0))
               for t in values] for u in values]
    geometry = [sum((entry(p, u, t) ** 2 for p in prime_shell
                     for t in values), Fraction(0)) for u in values]
    text = lambda value: f"{value.numerator}/{value.denominator}"
    md = hashlib.sha256(canonical(
        [[text(value) for value in row] for row in matrix])).hexdigest()
    gd = hashlib.sha256(canonical([text(value) for value in geometry])).hexdigest()
    need(recorded.get("interval") == list(EXACT_INTERVAL) and
         recorded.get("Q") == 4 and recorded.get("kernel_exponent") == 1 and
         recorded.get("shell") == prime_shell and
         recorded.get("matrix_digest") == md and
         recorded.get("geometry_digest") == gd and
         recorded.get("matrix_symmetric") is True and
         recorded.get("geometry_positive") is True, "exact anchor")


def validate(document: dict[str, Any]) -> None:
    need(document.get("certificate_version") == 1 and
         document.get("claim_status") == STATUS, "header")
    payload = document.get("payload")
    need(isinstance(payload, dict) and payload.get("schema") == SCHEMA,
         "schema")
    need(document.get("payload_sha256") == hashlib.sha256(
        canonical(payload)).hexdigest(), "payload hash")
    need(digest(BASE_CODE.read_bytes()) == BASE_SHA256, "base provenance")
    need(digest(PARENT_CERT.read_bytes()) == PARENT_CERT_SHA256,
         "parent provenance")
    protocol = payload.get("protocol", {})
    need(protocol.get("origins") == list(ORIGINS) and
         protocol.get("counts") == list(COUNTS) and
         protocol.get("q_anchors") == list(Q_ANCHORS) and
         protocol.get("kernel_exponents") == list(EXPONENTS) and
         protocol.get("laws") == list(LAWS) and
         protocol.get("spectra_for_all_laws") is True and
         protocol.get("source_response_used") is False and
         protocol.get("trim_denominator") == TRIM_DENOMINATOR,
         "protocol")
    rows = payload.get("rows")
    need(isinstance(rows, list) and len(rows) == 144, "rows")
    need(len({(row.get("origin"), row.get("count"), row.get("Q"),
               row.get("kernel_exponent"), row.get("law"))
              for row in rows}) == 144, "row keys")
    need(payload.get("row_digest") == hashlib.sha256(
        canonical(rows)).hexdigest(), "row digest")
    audit = payload.get("finite_audit", {})
    need(audit.get("rows") == 144 and audit.get("settings") == 36 and
         audit.get("laws") == 4 and audit.get("spectral_rows") == 144 and
         audit.get("first_spectral_cap_failure_Q") == 128 and
         audit.get("spectral_cap_violations") == 18 and
         audit.get("spectral_cap_violations_Q128") == 6 and
         audit.get("spectral_cap_violations_Q256") == 12 and
         audit.get("bulk_persistence_after_schur_trim") == 18 and
         audit.get("bulk_persistence_after_eigenvector_trim") == 18 and
         audit.get("finite_schur_violations") == 0 and
         audit.get("finite_frobenius_violations") == 0 and
         audit.get("fixed_power_credit") == 0 and
         audit.get("arithmetic_advance") == "NO" and
         float(audit["min_trimmed_spectral_over_violations"]) >
         SPECTRAL_CAP and
         float(audit["max_trimmed_spectral_Q80_control"]) <
         SPECTRAL_CAP, "audit")
    need(payload.get("law_census", {}).get("violation_law_counts") == {
        "all_plus": 18, "alternating_index": 0,
        "mod4_character": 0, "half_split": 0}, "law census")
    expected = {
        "TPC363_FINITE_REPLAY": "NUMERICALLY_CERTIFIED_FINITE_144_ROWS",
        "TPC363_FINITE_ENVELOPE_INEQUALITIES": "PROVED_EXACT_FINITE",
        "TPC363_FIRST_Q128_FAILURE": "NUMERICALLY_CERTIFIED_FINITE_SCOPED",
        "TPC363_BULK_PERSISTENCE": "NUMERICALLY_CERTIFIED_FINITE_SCOPED",
        "TPC363_SINGLE_ROW_SPIKE_EXPLANATION": "REFUTED_SCOPED_ON_DECLARED_TRIMS",
        "TPC363_EIGENVECTOR_DELOCALIZATION": "NUMERICALLY_CERTIFIED_FINITE_SCOPED",
        "TPC363_RENORMALIZED_REPAIR": "OPEN",
        "TPC363_GROWING_OPERATOR_BOUND": "OPEN",
        "TPC363_SOURCE_UNIFORM_L2": "OPEN",
        "TPC363_ARITHMETIC_ADVANCE": "NO",
        "TPC363_FIXED_POWER_CREDIT": 0,
        "TPC363_FULL_GATE_B": "OPEN", "TPC363_TWIN_PRIME_RESULT": "NONE",
    }
    for key, value in expected.items():
        need(payload.get("claim_firewall", {}).get(key) == value,
             "firewall " + key)
    check_exact_anchor(payload.get("exact_anchor", {}))

    indexed = {(row["origin"], row["count"], row["Q"],
                row["kernel_exponent"], row["law"]): row for row in rows}
    for origin in ORIGINS:
        for count in COUNTS:
            values = np.arange(origin, origin + count, dtype=np.int64)
            for q0 in Q_ANCHORS:
                for exponent in EXPONENTS:
                    prime_shell, matrices, geometry = reverse_components(
                        origin, count, q0, exponent)
                    scale = np.sqrt(geometry[:, None] * geometry[None, :])
                    for law in LAWS:
                        key = (origin, count, q0, exponent, law)
                        row = indexed[key]
                        actual = metrics(matrices[law] / scale)
                        need(row["shell"] == prime_shell and
                             row["interval"] == [origin, origin + count - 1],
                             "row metadata")
                        close(float(np.min(geometry)), row["geometry_min"],
                              "geometry min")
                        close(float(np.max(geometry)), row["geometry_max"],
                              "geometry max")
                        close(float(np.mean(geometry)), row["geometry_mean"],
                              "geometry mean")
                        close(float(np.std(geometry) / np.mean(geometry)),
                              row["geometry_cv"], "geometry cv")
                        recorded = row["normalized"]
                        for field in (
                                "schur", "frobenius", "spectral",
                                "minimum_eigenvalue", "maximum_eigenvalue",
                                "symmetry_error", "spectral_over_schur",
                                "spectral_over_frobenius", "schur_row_mass",
                                "principal_eigenvector_top1_mass",
                                "principal_eigenvector_top5_mass",
                                "principal_eigenvector_ipr",
                                "principal_eigenvector_effective_support",
                                "principal_eigenvector_schur_alignment",
                                "trimmed_spectral_after_schur_rows",
                                "trimmed_spectral_after_eigenvector_rows",
                                "trimmed_ratio_after_schur_rows",
                                "trimmed_ratio_after_eigenvector_rows"):
                            close(actual[field], recorded[field], field)
                        for field in ("schur_row_index", "principal_eigen_index",
                                      "trim_count", "schur_trim_indices",
                                      "eigenvector_trim_indices"):
                            need(actual[field] == recorded[field], field)


def main() -> int:
    if sys.argv[1:] != ["--check"]:
        raise SystemExit("--check is the only argument")
    try:
        document = json.loads(CERTIFICATE.read_bytes())
        validate(document)
        print("TPC363_INDEPENDENT_CHECK=PASS rows=144 violations=18 "
              "persistent_schur=18 persistent_eigenvector=18")
        return 0
    except (Failure, OSError, ValueError, TypeError, KeyError,
            json.JSONDecodeError, np.linalg.LinAlgError) as error:
        print("TPC363_INDEPENDENT_CHECK=FAIL " + str(error), file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
