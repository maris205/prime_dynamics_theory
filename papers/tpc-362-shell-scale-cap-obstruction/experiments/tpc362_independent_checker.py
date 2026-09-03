#!/usr/bin/env python3
"""Independent reverse-shell checker for the TPC-362 Q-scale audit."""

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
PROJECT = ROOT / "papers/tpc-362-shell-scale-cap-obstruction"
CERTIFICATE = PROJECT / "results/tpc362_certificate.json"
BASE_CODE = ROOT / (
    "papers/tpc-355-position-aware-mask-energy-normalization/code/"
    "tpc355_position_aware_mask_energy_normalization.py")
BASE_SHA256 = (
    "b54883cbc2e9e19dd8cf6fbece69ff7752ba805678e0b5b2fcf82949dd42fde9")
SCHEMA = "TPC362_SHELL_SCALE_CAP_OBSTRUCTION_V1"
STATUS = "NUMERICALLY_CERTIFIED_FINITE_SHELL_SCALE_CAP_OBSTRUCTION"
ORIGINS = (313030, 311166, 321651)
COUNTS = (256, 512)
Q_ANCHORS = (12, 24, 36, 54, 80, 128, 256, 512)
EXPONENTS = (1, 2)
LAWS = ("all_plus", "alternating_index", "mod4_character", "half_split")
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
    sieve[0] = sieve[1] = 0
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


def metrics(matrix: np.ndarray) -> dict[str, float]:
    symmetry = float(np.max(np.abs(matrix - matrix.T)))
    schur = float(np.max(np.sum(np.abs(matrix), axis=1)))
    frobenius = float(np.sqrt(np.sum(matrix * matrix)))
    ev = np.linalg.eigvalsh(matrix)
    lo, hi = float(ev[0]), float(ev[-1])
    spectral = max(abs(lo), abs(hi))
    need(symmetry <= 1.0e-10 and spectral <= schur + 1.0e-7 and
         spectral <= frobenius + 1.0e-7, "finite envelope")
    return {"schur": schur, "frobenius": frobenius,
            "spectral": spectral, "minimum_eigenvalue": lo,
            "maximum_eigenvalue": hi, "symmetry_error": symmetry,
            "spectral_over_schur": spectral / schur,
            "spectral_over_frobenius": spectral / frobenius}


def exact_anchor(recorded: dict[str, Any]) -> None:
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
    need(all(g > 0 for g in geometry), "anchor positivity")
    text = lambda x: f"{x.numerator}/{x.denominator}"
    md = hashlib.sha256(canonical(
        [[text(x) for x in row] for row in matrix])).hexdigest()
    gd = hashlib.sha256(canonical([text(x) for x in geometry])).hexdigest()
    need(recorded.get("interval") == list(EXACT_INTERVAL) and
         recorded.get("Q") == 4 and recorded.get("shell") == prime_shell and
         recorded.get("matrix_digest") == md and
         recorded.get("geometry_digest") == gd and
         recorded.get("matrix_symmetric") is True and
         recorded.get("geometry_positive") is True, "exact anchor")


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
        need(protocol.get("origins") == list(ORIGINS) and
             protocol.get("counts") == list(COUNTS) and
             protocol.get("q_anchors") == list(Q_ANCHORS) and
             protocol.get("kernel_exponents") == list(EXPONENTS) and
             protocol.get("laws") == list(LAWS) and
             protocol.get("spectra_for_all_laws") is True and
             protocol.get("source_response_used") is False, "protocol")
        rows = payload["rows"]
        need(len(rows) == 384 and len({
            (r["origin"], r["count"], r["Q"], r["kernel_exponent"], r["law"])
            for r in rows}) == 384, "row census")
        indexed = {(r["origin"], r["count"], r["Q"],
                    r["kernel_exponent"], r["law"]): r for r in rows}
        for origin in ORIGINS:
            for count in COUNTS:
                for q0 in Q_ANCHORS:
                    for exponent in EXPONENTS:
                        prime_shell, matrices, geometry = reverse_components(
                            origin, count, q0, exponent)
                        scale = np.sqrt(geometry[:, None] * geometry[None, :])
                        for law in LAWS:
                            row = indexed[(origin, count, q0, exponent, law)]
                            actual = metrics(matrices[law] / scale)
                            recorded = row["normalized"]
                            need(row["shell"] == prime_shell and
                                 row["interval"] == [origin, origin + count - 1],
                                 "row metadata")
                            close(float(np.min(geometry)), row["geometry_min"], "gmin")
                            close(float(np.max(geometry)), row["geometry_max"], "gmax")
                            for field in ("schur", "frobenius", "spectral",
                                          "minimum_eigenvalue",
                                          "maximum_eigenvalue", "symmetry_error",
                                          "spectral_over_schur",
                                          "spectral_over_frobenius"):
                                close(actual[field], recorded[field], field)
        need(payload["finite_audit"]["rows"] == 384 and
             payload["finite_audit"]["spectral_rows"] == 384 and
             payload["finite_audit"]["first_schur_cap_failure_Q"] == 128 and
             payload["finite_audit"]["first_spectral_cap_failure_Q"] == 128,
             "audit")
        need(payload["law_winner_audit"]["winner_counts"] == {
            "all_plus": 78, "alternating_index": 4,
            "mod4_character": 14, "half_split": 0}, "winner census")
        need(payload["q_transition_audit"]["counts"] == {
            "increase": 200, "decrease": 136, "flat": 0},
             "Q transition census")
        firewall = payload["claim_firewall"]
        need(firewall["TPC362_HIGH_Q_CAP_EXTENSION"] ==
             "REFUTED_SCOPED_ON_DECLARED_Q_LADDER" and
             firewall["TPC362_ARITHMETIC_ADVANCE"] == "NO" and
             firewall["TPC362_FIXED_POWER_CREDIT"] == 0 and
             firewall["TPC362_FULL_GATE_B"] == "OPEN" and
             firewall["TPC362_TWIN_PRIME_RESULT"] == "NONE", "firewall")
        exact_anchor(payload["exact_anchor"])
        print("TPC362_INDEPENDENT_CHECK=PASS rows=384 all_laws=4 "
              "first_cap_failure_Q=128")
        return 0
    except (Failure, OSError, ValueError, TypeError, KeyError,
            json.JSONDecodeError, np.linalg.LinAlgError) as error:
        print("TPC362_INDEPENDENT_CHECK=FAIL " + str(error), file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
