#!/usr/bin/env python3
"""Independent reverse-shell replay for TPC-361.

This checker intentionally does not import the TPC-361 producer or the
TPC-355 implementation.  It rebuilds the sieve, geometry-only selection,
literal blocks, four sign laws, normalization, spectra, and rational anchor.
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
PROJECT = ROOT / "papers/tpc-361-independent-high-origin-tightness-replication"
CERTIFICATE = PROJECT / "results/tpc361_certificate.json"
BASE_CODE = ROOT / (
    "papers/tpc-355-position-aware-mask-energy-normalization/code/"
    "tpc355_position_aware_mask_energy_normalization.py")
BASE_SHA256 = (
    "b54883cbc2e9e19dd8cf6fbece69ff7752ba805678e0b5b2fcf82949dd42fde9")
SCHEMA = "TPC361_INDEPENDENT_HIGH_ORIGIN_TIGHTNESS_REPLICATION_V1"
STATUS = "NUMERICALLY_CERTIFIED_FINITE_INDEPENDENT_HIGH_ORIGIN_TIGHTNESS_REPLICATION"
CANDIDATE_START = 310001
CANDIDATE_STEP = 233
CANDIDATE_COUNT = 51
PILOT_COUNT = 256
MIN_SEPARATION = 1536
ORIGINS = (313030, 311166, 321651)
COUNTS = (256, 512, 1024, 2048)
Q_ANCHORS = (24, 54, 80)
EXPONENTS = (1, 2)
LAWS = ("all_plus", "alternating_index", "mod4_character", "half_split")
SHORT_COUNTS = (256, 512)
HEIGHT = 66
TOL = 5.0e-5
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
    need(abs(float(actual) - target) <= TOL * max(1.0, abs(actual), abs(target)),
         label)


def primes_up_to(limit: int) -> list[int]:
    sieve = bytearray(b"\x01") * (limit + 1)
    sieve[0] = 0
    sieve[1] = 0
    for p in range(2, math.isqrt(limit) + 1):
        if sieve[p]:
            start = p * p
            sieve[start:limit + 1:p] = b"\x00" * (
                (limit - start) // p + 1)
    return [p for p in range(2, limit + 1) if sieve[p]]


PRIMES = primes_up_to(50000)


def shell(q0: int) -> list[int]:
    return [p for p in PRIMES if q0 < p <= 2 * q0]


def signs(prime_shell: list[int]) -> dict[str, np.ndarray]:
    return {
        "all_plus": np.ones(len(prime_shell), dtype=np.float64),
        "alternating_index": np.asarray(
            [1.0 if i % 2 == 0 else -1.0
             for i in range(len(prime_shell))]),
        "mod4_character": np.asarray(
            [1.0 if p % 4 == 1 else -1.0 for p in prime_shell]),
        "half_split": np.asarray(
            [1.0 if i < len(prime_shell) / 2 else -1.0
             for i in range(len(prime_shell))]),
    }


def reverse_geometry(values: np.ndarray, q0: int, exponent: int) -> np.ndarray:
    difference = values[:, None] - values[None, :]
    distance = difference.astype(np.float64)
    kernel = (float(HEIGHT) ** (2 * exponent) /
              (HEIGHT * HEIGHT + distance * distance) ** exponent)
    np.fill_diagonal(kernel, 0.0)
    result = np.zeros(len(values), dtype=np.float64)
    for p in shell(q0):
        centered = ((difference % p == 0).astype(np.float64) - 1.0 / (p - 1))
        np.fill_diagonal(centered, 0.0)
        valid = ((difference != 0) & (values[:, None] % p != 0) &
                 (values[None, :] % p != 0))
        block = float(p) * kernel * centered * valid
        result += np.sum(block * block, axis=1)
    need(bool(np.all(np.isfinite(result) & (result > 0))), "geometry")
    return result


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
    # Reverse shell traversal is deliberate: it gives a different summation
    # order from the forward producer while representing the same finite sum.
    for index in range(len(prime_shell) - 1, -1, -1):
        p = prime_shell[index]
        centered = ((difference % p == 0).astype(np.float64) - 1.0 / (p - 1))
        np.fill_diagonal(centered, 0.0)
        valid = ((difference != 0) & (values[:, None] % p != 0) &
                 (values[None, :] % p != 0))
        block = float(p) * kernel * centered * valid
        geometry += np.sum(block * block, axis=1)
        for law in LAWS:
            matrices[law] += sign[law][index] * block
    for law in LAWS:
        matrices[law] = (matrices[law] + matrices[law].T) / 2.0
    need(bool(np.all(np.isfinite(geometry) & (geometry > 0))), "geometry")
    return prime_shell, matrices, geometry


def finite_metrics(matrix: np.ndarray, spectrum: bool) -> dict[str, Any]:
    symmetry = float(np.max(np.abs(matrix - matrix.T)))
    schur = float(np.max(np.sum(np.abs(matrix), axis=1)))
    frobenius = float(np.sqrt(np.sum(matrix * matrix)))
    need(symmetry <= 1.0e-10 and schur > 0 and frobenius > 0,
         "matrix metrics")
    result: dict[str, Any] = {
        "schur": schur, "frobenius": frobenius,
        "symmetry_error": symmetry, "spectrum_recorded": spectrum,
        "spectral": None, "minimum_eigenvalue": None,
        "maximum_eigenvalue": None, "spectral_over_schur": None,
        "spectral_over_frobenius": None,
    }
    if spectrum:
        eigenvalues = np.linalg.eigvalsh(matrix)
        lo, hi = float(eigenvalues[0]), float(eigenvalues[-1])
        spectral = max(abs(lo), abs(hi))
        need(spectral <= schur + 1.0e-8 and spectral <= frobenius + 1.0e-8,
             "finite envelope")
        result.update({"spectral": spectral, "minimum_eigenvalue": lo,
                       "maximum_eigenvalue": hi,
                       "spectral_over_schur": spectral / schur,
                       "spectral_over_frobenius": spectral / frobenius})
    return result


def candidate_scan() -> list[dict[str, Any]]:
    scan = []
    for j in range(CANDIDATE_COUNT):
        origin = CANDIDATE_START + CANDIDATE_STEP * j
        values = np.arange(origin, origin + PILOT_COUNT, dtype=np.int64)
        settings = []
        score = 0.0
        for q0 in Q_ANCHORS:
            for exponent in EXPONENTS:
                geometry = reverse_geometry(values, q0, exponent)
                minimum, maximum = float(np.min(geometry)), float(np.max(geometry))
                spread = maximum / minimum
                score = max(score, spread)
                settings.append({"Q": q0, "kernel_exponent": exponent,
                                 "geometry_min": minimum,
                                 "geometry_max": maximum, "spread": spread})
        scan.append({"origin": origin, "score": score, "settings": settings})
    return scan


def check_selection(payload: dict[str, Any]) -> None:
    recorded = payload["selection"]["scan"]
    need(len(recorded) == CANDIDATE_COUNT, "candidate scan census")
    fresh = candidate_scan()
    for actual, row in zip(fresh, recorded):
        need(actual["origin"] == row["origin"], "candidate origin")
        close(actual["score"], row["score"], "candidate score")
        need(len(actual["settings"]) == 6, "candidate settings")
        for a, b in zip(actual["settings"], row["settings"]):
            need((a["Q"], a["kernel_exponent"]) ==
                 (b["Q"], b["kernel_exponent"]), "candidate key")
            for field in ("geometry_min", "geometry_max", "spread"):
                close(a[field], b[field], "candidate " + field)
    ordered = sorted(fresh, key=lambda row: (-row["score"], row["origin"]))
    selected = []
    for row in ordered:
        if all(abs(row["origin"] - old) >= MIN_SEPARATION for old in selected):
            selected.append(row["origin"])
        if len(selected) == 3:
            break
    need(selected == list(ORIGINS) and
         payload["selection"]["selected_origins"] == list(ORIGINS),
         "selection replay")


def check_exact_anchor(recorded: dict[str, Any]) -> None:
    values = list(range(EXACT_INTERVAL[0], EXACT_INTERVAL[1] + 1))
    prime_shell = shell(4)

    def entry(p: int, u: int, t: int) -> Fraction:
        if u == t or u % p == 0 or t % p == 0:
            return Fraction(0)
        centered = Fraction(int((u - t) % p == 0), 1) - Fraction(1, p - 1)
        return p * Fraction(HEIGHT * HEIGHT,
                            HEIGHT * HEIGHT + (u - t) ** 2) * centered

    matrix = [[sum((entry(p, u, t) for p in prime_shell), Fraction(0))
               for t in values] for u in values]
    geometry = [sum((entry(p, u, t) ** 2 for p in prime_shell for t in values),
                    Fraction(0)) for u in values]
    need(all(matrix[i][j] == matrix[j][i]
             for i in range(len(values)) for j in range(len(values))),
         "anchor symmetry")
    need(all(value > 0 for value in geometry), "anchor positivity")
    text = lambda value: f"{value.numerator}/{value.denominator}"
    expected_matrix = hashlib.sha256(canonical(
        [[text(value) for value in row] for row in matrix])).hexdigest()
    expected_geometry = hashlib.sha256(canonical(
        [text(value) for value in geometry])).hexdigest()
    need(recorded.get("interval") == list(EXACT_INTERVAL) and
         recorded.get("Q") == 4 and recorded.get("shell") == prime_shell and
         recorded.get("kernel_exponent") == 1 and
         recorded.get("matrix_symmetric") is True and
         recorded.get("geometry_positive") is True and
         recorded.get("matrix_digest") == expected_matrix and
         recorded.get("geometry_digest") == expected_geometry,
         "exact anchor")


def main() -> int:
    if sys.argv[1:] != ["--check"]:
        raise SystemExit("--check is the only argument")
    try:
        raw = CERTIFICATE.read_bytes()
        document = json.loads(raw)
        need(raw == canonical(document), "certificate canonicality")
        need(document.get("certificate_version") == 1 and
             document.get("claim_status") == STATUS, "header")
        payload = document["payload"]
        need(payload.get("schema") == SCHEMA and
             document.get("payload_sha256") == hashlib.sha256(
                 canonical(payload)).hexdigest(), "schema/hash")
        need(digest(BASE_CODE.read_bytes()) == BASE_SHA256, "base provenance")
        protocol = payload["protocol"]
        need(protocol.get("candidate_origins") ==
             [CANDIDATE_START + CANDIDATE_STEP * j
              for j in range(CANDIDATE_COUNT)] and
             protocol.get("pilot_count") == PILOT_COUNT and
             protocol.get("minimum_separation") == MIN_SEPARATION and
             protocol.get("origins") == list(ORIGINS) and
             protocol.get("counts") == list(COUNTS) and
             protocol.get("q_anchors") == list(Q_ANCHORS) and
             protocol.get("kernel_exponents") == list(EXPONENTS) and
             protocol.get("laws") == list(LAWS) and
             protocol.get("spectral_short_counts") == list(SHORT_COUNTS) and
             protocol.get("source_response_used") is False and
             protocol.get("sign_response_used") is False, "protocol")
        check_selection(payload)
        rows = payload["rows"]
        need(len(rows) == 288 and len({
            (r["origin"], r["count"], r["Q"], r["kernel_exponent"], r["law"])
            for r in rows}) == 288, "row census")
        indexed = {(r["origin"], r["count"], r["Q"],
                    r["kernel_exponent"], r["law"]): r for r in rows}
        spectra_count = 0
        for origin in ORIGINS:
            for count in COUNTS:
                for q0 in Q_ANCHORS:
                    for exponent in EXPONENTS:
                        prime_shell, matrices, geometry = reverse_components(
                            origin, count, q0, exponent)
                        scale = np.sqrt(geometry[:, None] * geometry[None, :])
                        for law in LAWS:
                            row = indexed[(origin, count, q0, exponent, law)]
                            recorded = row["normalized"]
                            should_spectrum = count in SHORT_COUNTS or law == "all_plus"
                            need(recorded["spectrum_recorded"] is should_spectrum,
                                 "spectrum flag")
                            actual = finite_metrics(matrices[law] / scale,
                                                     should_spectrum)
                            need(row["shell"] == prime_shell and
                                 row["interval"] == [origin, origin + count - 1],
                                 "row metadata")
                            close(float(np.min(geometry)), row["geometry_min"], "gmin")
                            close(float(np.max(geometry)), row["geometry_max"], "gmax")
                            for field in ("schur", "frobenius", "symmetry_error"):
                                close(actual[field], recorded[field], field)
                            if should_spectrum:
                                spectra_count += 1
                                for field in ("spectral", "minimum_eigenvalue",
                                              "maximum_eigenvalue",
                                              "spectral_over_schur",
                                              "spectral_over_frobenius"):
                                    close(actual[field], recorded[field], field)
                            else:
                                need(all(recorded[field] is None for field in
                                         ("spectral", "minimum_eigenvalue",
                                          "maximum_eigenvalue",
                                          "spectral_over_schur",
                                          "spectral_over_frobenius")),
                                     "unrecorded spectrum")
        need(spectra_count == 180 and payload["finite_audit"]["spectral_rows"] == 180,
             "spectrum census")
        audit = payload["finite_audit"]
        need(audit["rows"] == 288 and audit["settings"] == 72 and
             audit["laws"] == 4 and audit["finite_schur_violations"] == 0 and
             audit["finite_frobenius_violations"] == 0 and
             audit["fixed_power_credit"] == 0 and
             audit["arithmetic_advance"] == "NO", "audit firewall")
        firewall = payload["claim_firewall"]
        need(firewall["TPC361_GEOMETRY_SELECTION"] ==
             "PROVED_EXACT_FINITE_RESPONSE_BLIND" and
             firewall["TPC361_HIGH_ORIGIN_REPLAY"] ==
             "NUMERICALLY_CERTIFIED_FINITE_288_ROWS" and
             firewall["TPC361_ARITHMETIC_ADVANCE"] == "NO" and
             firewall["TPC361_FIXED_POWER_CREDIT"] == 0 and
             firewall["TPC361_FULL_GATE_B"] == "OPEN" and
             firewall["TPC361_TWIN_PRIME_RESULT"] == "NONE", "firewall")
        check_exact_anchor(payload["exact_anchor"])
        print("TPC361_INDEPENDENT_CHECK=PASS rows=288 spectral_rows=180 "
              "selection=51 candidates origins=3")
        return 0
    except (Failure, OSError, ValueError, TypeError, KeyError,
            json.JSONDecodeError, np.linalg.LinAlgError) as error:
        print("TPC361_INDEPENDENT_CHECK=FAIL " + str(error), file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
