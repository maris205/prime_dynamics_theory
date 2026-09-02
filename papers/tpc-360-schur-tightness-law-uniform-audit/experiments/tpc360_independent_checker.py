#!/usr/bin/env python3
"""Independent reverse-shell checker for the TPC-360 tightness audit."""

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
PROJECT = ROOT / "papers/tpc-360-schur-tightness-law-uniform-audit"
CERTIFICATE = PROJECT / "results/tpc360_certificate.json"
BASE_CODE = ROOT / ("papers/tpc-355-position-aware-mask-energy-normalization/"
                    "code/tpc355_position_aware_mask_energy_normalization.py")
BASE_SHA256 = "b54883cbc2e9e19dd8cf6fbece69ff7752ba805678e0b5b2fcf82949dd42fde9"
SCHEMA = "TPC360_SCHUR_TIGHTNESS_LAW_UNIFORM_AUDIT_V1"
STATUS = "NUMERICALLY_CERTIFIED_FINITE_SCHUR_TIGHTNESS_LAW_UNIFORM_AUDIT"
ORIGINS = (267175, 261267, 269074)
COUNTS = (256, 512)
Q_ANCHORS = (24, 54, 80)
EXPONENTS = (1, 2)
LAWS = ("all_plus", "alternating_index", "mod4_character", "half_split")
HEIGHT = 66
TOL = 3.0e-5
EXACT_INTERVAL = (267205, 267218)


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


def primes_up_to(limit: int) -> list[int]:
    sieve = bytearray(b"\x01") * (limit + 1)
    sieve[0] = sieve[1] = 0
    for p in range(2, math.isqrt(limit) + 1):
        if sieve[p]:
            start = p * p
            sieve[start:limit + 1:p] = b"\x00" * ((limit - start) // p + 1)
    return [p for p in range(2, limit + 1) if sieve[p]]


PRIMES = primes_up_to(50000)


def shell(q0: int) -> list[int]:
    return [p for p in PRIMES if q0 < p <= 2 * q0]


def sign_vectors(primes: list[int]) -> dict[str, np.ndarray]:
    return {
        "all_plus": np.ones(len(primes)),
        "alternating_index": np.asarray([1.0 if i % 2 == 0 else -1.0
                                          for i in range(len(primes))]),
        "mod4_character": np.asarray([1.0 if p % 4 == 1 else -1.0
                                       for p in primes]),
        "half_split": np.asarray([1.0 if i < len(primes) / 2 else -1.0
                                   for i in range(len(primes))]),
    }


def reverse_components(origin: int, count: int, q0: int, exponent: int):
    values = np.arange(origin, origin + count, dtype=np.int64)
    difference = values[:, None] - values[None, :]
    distance = difference.astype(np.float64)
    kernel = (float(HEIGHT) ** (2 * exponent) /
              (HEIGHT * HEIGHT + distance * distance) ** exponent)
    np.fill_diagonal(kernel, 0.0)
    primes = shell(q0)
    signs = sign_vectors(primes)
    matrices = {law: np.zeros((count, count)) for law in LAWS}
    geometry = np.zeros(count)
    for index, p in reversed(list(enumerate(primes))):
        centered = ((difference % p == 0).astype(np.float64) - 1.0 / (p - 1))
        np.fill_diagonal(centered, 0.0)
        valid = ((difference != 0) & (values[:, None] % p != 0) &
                 (values[None, :] % p != 0))
        block = float(p) * kernel * centered * valid
        geometry += np.sum(block * block, axis=1)
        for law in LAWS:
            matrices[law] += signs[law][index] * block
    for law in LAWS:
        matrices[law] = (matrices[law] + matrices[law].T) / 2.0
    need(bool(np.all(np.isfinite(geometry) & (geometry > 0))), "geometry")
    return primes, matrices, geometry


def metrics(matrix: np.ndarray) -> dict[str, float]:
    symmetry = float(np.max(np.abs(matrix - matrix.T)))
    schur = float(np.max(np.sum(np.abs(matrix), axis=1)))
    frob = float(np.sqrt(np.sum(matrix * matrix)))
    ev = np.linalg.eigvalsh(matrix)
    lo, hi = float(ev[0]), float(ev[-1])
    spectral = max(abs(lo), abs(hi))
    need(symmetry <= 1.0e-12 and spectral <= schur + TOL and
         spectral <= frob + TOL, "finite envelope")
    return {"schur": schur, "frobenius": frob, "spectral": spectral,
            "minimum_eigenvalue": lo, "maximum_eigenvalue": hi,
            "symmetry_error": symmetry,
            "spectral_over_schur": spectral / schur,
            "spectral_over_frobenius": spectral / frob}


def close(actual: float, recorded: Any, label: str) -> None:
    target = float(recorded)
    error = abs(float(actual) - target)
    need(bool(error <= TOL * max(1.0, abs(float(actual)), abs(target))), label)


def exact_anchor() -> dict[str, Any]:
    values = list(range(EXACT_INTERVAL[0], EXACT_INTERVAL[1] + 1))
    primes = shell(4)

    def entry(p: int, u: int, t: int) -> Fraction:
        if u == t or u % p == 0 or t % p == 0:
            return Fraction(0)
        centered = Fraction(int((u - t) % p == 0), 1) - Fraction(1, p - 1)
        return p * Fraction(HEIGHT * HEIGHT,
                            HEIGHT * HEIGHT + (u - t) ** 2) * centered

    matrix = [[sum((entry(p, u, t) for p in primes), Fraction(0))
               for t in values] for u in values]
    geometry = [sum((entry(p, u, t) ** 2 for p in primes for t in values),
                    Fraction(0)) for u in values]
    need(all(matrix[i][j] == matrix[j][i]
             for i in range(14) for j in range(14)), "anchor symmetry")
    need(all(g > 0 for g in geometry), "anchor geometry")
    text = lambda x: f"{x.numerator}/{x.denominator}"
    return {"shell": primes,
            "matrix_digest": hashlib.sha256(canonical([
                [text(x) for x in row] for row in matrix])).hexdigest(),
            "geometry_digest": hashlib.sha256(canonical(
                [text(x) for x in geometry])).hexdigest()}


def main() -> int:
    if sys.argv[1:] != ["--check"]:
        raise SystemExit("--check is the only argument")
    try:
        raw = CERTIFICATE.read_bytes()
        doc = json.loads(raw)
        need(raw == canonical(doc), "certificate canonicality")
        need(doc.get("certificate_version") == 1 and
             doc.get("claim_status") == STATUS, "header")
        payload = doc["payload"]
        need(payload.get("schema") == SCHEMA and
             doc.get("payload_sha256") == hashlib.sha256(
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
        need(len(rows) == 144 and len({(r["origin"], r["count"], r["Q"],
                                        r["kernel_exponent"], r["law"])
                                       for r in rows}) == 144, "rows")
        expected = {(r["origin"], r["count"], r["Q"],
                     r["kernel_exponent"], r["law"]): r for r in rows}
        for origin in ORIGINS:
            for count in COUNTS:
                for q0 in Q_ANCHORS:
                    for exponent in EXPONENTS:
                        primes, matrices, geometry = reverse_components(
                            origin, count, q0, exponent)
                        scale = np.sqrt(geometry[:, None] * geometry[None, :])
                        for law in LAWS:
                            row = expected[(origin, count, q0, exponent, law)]
                            need(row["shell"] == primes, "shell")
                            actual = metrics(matrices[law] / scale)
                            recorded = row["normalized"]
                            for field in ("schur", "frobenius", "spectral",
                                          "minimum_eigenvalue",
                                          "maximum_eigenvalue", "symmetry_error",
                                          "spectral_over_schur",
                                          "spectral_over_frobenius"):
                                close(actual[field], recorded[field], field)
                            close(np.min(geometry), row["geometry_min"], "gmin")
                            close(np.max(geometry), row["geometry_max"], "gmax")
        need(payload["law_winner_audit"]["winner_counts"] == {
            "all_plus": 30, "alternating_index": 0,
            "mod4_character": 6, "half_split": 0}, "winner census")
        anchor = exact_anchor()
        for field in ("shell", "matrix_digest", "geometry_digest"):
            need(anchor[field] == payload["exact_anchor"].get(field),
                 "anchor " + field)
        print("TPC360_INDEPENDENT_CHECK=PASS rows=144 all_laws=4 spectra=144")
        return 0
    except (Failure, OSError, ValueError, TypeError, KeyError,
            json.JSONDecodeError, np.linalg.LinAlgError) as error:
        print("TPC360_INDEPENDENT_CHECK=FAIL " + str(error), file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
