#!/usr/bin/env python3
"""Independent reverse-shell replay for TPC-359.

This checker does not import the TPC-359 producer.  It rebuilds the prime
sieve, the response-blind selection score, literal masked components, the
normalization, finite envelopes, spectra, and the rational anchor.
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
PROJECT = ROOT / "papers/tpc-359-geometry-adversarial-high-origin-holdout"
CERTIFICATE = PROJECT / "results/tpc359_certificate.json"
BASE_CODE = ROOT / ("papers/tpc-355-position-aware-mask-energy-normalization/"
                    "code/tpc355_position_aware_mask_energy_normalization.py")
BASE_CODE_SHA256 = "b54883cbc2e9e19dd8cf6fbece69ff7752ba805678e0b5b2fcf82949dd42fde9"
SCHEMA = "TPC359_GEOMETRY_ADVERSARIAL_HIGH_ORIGIN_HOLDOUT_V1"
STATUS = "NUMERICALLY_CERTIFIED_FINITE_GEOMETRY_ADVERSARIAL_HIGH_ORIGIN_HOLDOUT"
CANDIDATES = tuple(range(260001, 270552, 211))
ORIGINS = (267175, 261267, 269074)
COUNTS = (256, 512, 1024, 2048)
Q_ANCHORS = (24, 54, 80)
EXPONENTS = (1, 2)
LAWS = ("all_plus", "alternating_index", "mod4_character", "half_split")
HEIGHT = 66
BOUND_TOL = 3.0e-5
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


def show(value: float) -> str:
    return format(float(value), ".17g")


def primes_up_to(limit: int) -> list[int]:
    sieve = bytearray(b"\x01") * (limit + 1)
    sieve[0] = sieve[1] = 0
    for p in range(2, math.isqrt(limit) + 1):
        if sieve[p]:
            start = p * p
            sieve[start:limit + 1:p] = b"\x00" * ((limit - start) // p + 1)
    return [p for p in range(2, limit + 1) if sieve[p]]


PRIMES = primes_up_to(50_000)


def shell(q0: int) -> list[int]:
    return [p for p in PRIMES if q0 < p <= 2 * q0]


def signs(primes: list[int]) -> dict[str, np.ndarray]:
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
    sign = signs(primes)
    matrices = {law: np.zeros((count, count), dtype=np.float64) for law in LAWS}
    geometry = np.zeros(count, dtype=np.float64)
    for index, prime in reversed(list(enumerate(primes))):
        centered = ((difference % prime == 0).astype(np.float64) -
                    1.0 / (prime - 1))
        np.fill_diagonal(centered, 0.0)
        valid = ((difference != 0) & (values[:, None] % prime != 0) &
                 (values[None, :] % prime != 0))
        block = float(prime) * kernel * centered * valid
        geometry += np.sum(block * block, axis=1)
        for law in LAWS:
            matrices[law] += sign[law][index] * block
    for law in LAWS:
        matrices[law] = (matrices[law] + matrices[law].T) / 2.0
    need(bool(np.all(np.isfinite(geometry) & (geometry > 0))), "geometry")
    return primes, matrices, geometry


def geometry_score(origin: int) -> tuple[float, int, int]:
    best = (-1.0, 0, 0)
    for q0 in Q_ANCHORS:
        for exponent in EXPONENTS:
            _, _, g = reverse_components(origin, 256, q0, exponent)
            value = float(np.max(g) / np.min(g))
            candidate = (value, q0, exponent)
            if (candidate[0], -candidate[1], -candidate[2]) > \
                    (best[0], -best[1], -best[2]):
                best = candidate
    return best


def select_origins() -> list[int]:
    ranked = sorted(((geometry_score(o), o) for o in CANDIDATES),
                    key=lambda item: (-item[0][0], item[1]))
    chosen: list[int] = []
    for _, origin in ranked:
        if all(abs(origin - old) >= 1536 for old in chosen):
            chosen.append(origin)
        if len(chosen) == 3:
            break
    return chosen


def metrics(matrix: np.ndarray, spectrum: bool) -> dict[str, Any]:
    symmetry = float(np.max(np.abs(matrix - matrix.T)))
    schur = float(np.max(np.sum(np.abs(matrix), axis=1)))
    frob = float(np.sqrt(np.sum(matrix * matrix)))
    need(symmetry <= 1.0e-12 and schur > 0 and frob > 0, "envelope")
    result = {"schur": schur, "frobenius": frob,
              "symmetry_error": symmetry, "spectral": None,
              "minimum_eigenvalue": None, "maximum_eigenvalue": None,
              "spectral_over_schur": None, "spectral_over_frobenius": None}
    if spectrum:
        ev = np.linalg.eigvalsh(matrix)
        lo, hi = float(ev[0]), float(ev[-1])
        spectral = max(abs(lo), abs(hi))
        need(spectral <= schur + BOUND_TOL and spectral <= frob + BOUND_TOL,
             "finite spectral envelope")
        result.update({"spectral": spectral, "minimum_eigenvalue": lo,
                       "maximum_eigenvalue": hi,
                       "spectral_over_schur": spectral / schur,
                       "spectral_over_frobenius": spectral / frob})
    return result


def close(actual: Any, recorded: Any, label: str) -> None:
    need(abs(float(actual) - float(recorded)) <=
         BOUND_TOL * max(1.0, abs(float(actual)), abs(float(recorded))),
         label)


def exact_anchor() -> dict[str, Any]:
    values = list(range(EXACT_INTERVAL[0], EXACT_INTERVAL[1] + 1))
    primes = shell(4)

    def entry(p: int, u: int, t: int) -> Fraction:
        if u == t or u % p == 0 or t % p == 0:
            return Fraction(0)
        centered = Fraction(int((u - t) % p == 0), 1) - Fraction(1, p - 1)
        return p * Fraction(HEIGHT * HEIGHT, (HEIGHT * HEIGHT + (u - t) ** 2)) * centered

    matrix = [[sum((entry(p, u, t) for p in primes), Fraction(0))
               for t in values] for u in values]
    geometry = [sum((entry(p, u, t) ** 2 for p in primes for t in values),
                    Fraction(0)) for u in values]
    need(all(matrix[i][j] == matrix[j][i]
             for i in range(14) for j in range(14)), "exact symmetry")
    need(all(g > 0 for g in geometry), "exact positivity")
    text = lambda x: f"{x.numerator}/{x.denominator}"
    return {"shell": primes, "matrix_symmetric": True,
            "geometry_positive": True,
            "row_sums_digest": hashlib.sha256(canonical([
                [text(abs(x)) for x in row] for row in matrix])).hexdigest(),
            "geometry_digest": hashlib.sha256(canonical(
                [text(x) for x in geometry])).hexdigest()}


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
        need(digest(BASE_CODE.read_bytes()) == BASE_CODE_SHA256, "base lock")
        protocol = payload["protocol"]
        need(protocol["candidate_origins"] == list(CANDIDATES) and
             protocol["origins"] == list(ORIGINS) and
             protocol["counts"] == list(COUNTS) and
             protocol["q_anchors"] == list(Q_ANCHORS) and
             protocol["kernel_exponents"] == list(EXPONENTS) and
             protocol["source_response_used"] is False and
             protocol["sign_response_used"] is False, "protocol")
        need(select_origins() == list(ORIGINS), "independent selection")
        rows = payload["rows"]
        need(isinstance(rows, list) and len(rows) == 288 and
             len({(r["origin"], r["count"], r["Q"], r["kernel_exponent"],
                   r["law"]) for r in rows}) == 288, "rows")
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
                            need(row["shell"] == primes, "shell metadata")
                            normalized = matrices[law] / scale
                            for name, actual in (("raw", metrics(
                                    matrices[law], law == "all_plus")),
                                                  ("normalized", metrics(
                                    normalized, law == "all_plus"))):
                                recorded = row[name]
                                for field in ("schur", "frobenius", "symmetry_error"):
                                    close(actual[field], recorded[field], name + field)
                                if law == "all_plus":
                                    for field in ("spectral", "minimum_eigenvalue",
                                                  "maximum_eigenvalue",
                                                  "spectral_over_schur",
                                                  "spectral_over_frobenius"):
                                        close(actual[field], recorded[field], name + field)
                            close(np.min(geometry), row["geometry_min"], "geometry min")
                            close(np.max(geometry), row["geometry_max"], "geometry max")
                            close(np.max(geometry) / np.min(geometry),
                                  row["geometry_spread"], "geometry spread")
        anchor = exact_anchor()
        for field in ("shell", "row_sums_digest", "geometry_digest"):
            need(anchor[field] == payload["exact_anchor"].get(field),
                 "anchor " + field)
        print("TPC359_INDEPENDENT_CHECK=PASS rows=288 origins=3 selection=PASS")
        return 0
    except (Failure, OSError, ValueError, TypeError, KeyError,
            json.JSONDecodeError, np.linalg.LinAlgError) as error:
        print("TPC359_INDEPENDENT_CHECK=FAIL " + str(error), file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
