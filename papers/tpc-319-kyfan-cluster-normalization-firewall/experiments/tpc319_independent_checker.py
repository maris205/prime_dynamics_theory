#!/usr/bin/env python3
"""Independent replay for TPC-319.

This checker does not import the producer.  It rebuilds the blocks with an
einsum accumulation and uses NumPy's full symmetric eigensolver, then checks
the stored Ky Fan intervals and the exact small rational anchor.
"""

from __future__ import annotations

import argparse
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

try:
    import numpy as np
except ImportError as error:  # pragma: no cover
    raise SystemExit("TPC319 independent checker requires numpy: " + str(error))

PROJECT = Path(__file__).resolve().parents[1]
CERTIFICATE = PROJECT / "results/tpc319_certificate.json"
HEIGHT = 66
SCALES = (640, 1280, 2560)
Q_ANCHORS = (24, 36, 54, 80)
EXPONENTS = (1, 2)
K_VALUES = (1, 2, 4, 8, 16)
MAX_K = max(K_VALUES)
PRIMES = None


class Failure(RuntimeError):
    pass


def need(condition: bool, message: str) -> None:
    if type(condition) is not bool or not condition:
        raise Failure(message)


def canonical(value: Any) -> bytes:
    return (json.dumps(value, ensure_ascii=True, sort_keys=True,
                       separators=(",", ":")) + "\n").encode("ascii")


def primes_up_to(limit: int) -> list[int]:
    sieve = bytearray(b"\x01") * (limit + 1)
    sieve[0:2] = b"\x00\x00"
    for p in range(2, math.isqrt(limit) + 1):
        if sieve[p]:
            sieve[p * p:limit + 1:p] = b"\x00" * (
                (limit - p * p) // p + 1)
    return [p for p in range(2, limit + 1) if sieve[p]]


PRIMES = primes_up_to(160)


def shell(q0: int) -> list[int]:
    return [p for p in PRIMES if q0 < p <= 2 * q0]


def source(scale: int) -> np.ndarray:
    return np.arange(scale // 2 + 1, scale + 1, dtype=np.int64)


def rebuild(scale: int, q0: int, exponent: int) -> np.ndarray:
    values = source(scale)
    differences = values[:, None] - values[None, :]
    dd = differences.astype(np.float64)
    kernel = HEIGHT ** (2 * exponent) / (
        HEIGHT * HEIGHT + dd * dd) ** exponent
    gram = np.zeros((len(values), len(values)), dtype=np.float64)
    # Reverse order and einsum deliberately differ from the producer's path.
    for p in reversed(shell(q0)):
        valid = ((differences != 0) &
                 (values[:, None] % p != 0) &
                 (values[None, :] % p != 0))
        centered = (np.equal(np.mod(differences, p), 0).astype(np.float64)
                    - 1.0 / (p - 1))
        block = p * kernel * centered * valid
        gram += np.einsum("ki,kj->ij", block, block, optimize=False)
    return (gram + gram.T) * 0.5


def exact_entry(prime: int, u: int, t: int, exponent: int) -> Fraction:
    if u == t or u % prime == 0 or t % prime == 0:
        return Fraction(0)
    centered = Fraction(1) if (u - t) % prime == 0 else Fraction(0)
    centered -= Fraction(1, prime - 1)
    return prime * Fraction(HEIGHT ** (2 * exponent),
                            (HEIGHT * HEIGHT + (u - t) ** 2) ** exponent) * centered


def exact_anchor() -> tuple[str, str, str]:
    values = list(range(17, 33))
    rows = [[exact_entry(5, u, t, 1) for t in values] for u in values]
    gram = [[sum((row[i] * row[j] for row in rows), Fraction(0))
             for j in range(len(values))] for i in range(len(values))]
    trace = sum((gram[i][i] for i in range(len(values))), Fraction(0))
    trace2 = sum((gram[i][j] * gram[j][i]
                  for i in range(len(values)) for j in range(len(values))),
                 Fraction(0))
    rayleigh = gram[0][0]
    return tuple(hashlib.sha256(
        f"{value.numerator}/{value.denominator}\n".encode("ascii")
    ).hexdigest() for value in (trace, trace2, rayleigh))


def close(a: float, b: float) -> bool:
    return math.isclose(a, b, rel_tol=4.0e-10, abs_tol=2.0e-7)


def check() -> None:
    raw = CERTIFICATE.read_bytes()
    document = json.loads(raw)
    need(raw == canonical(document), "certificate canonicality")
    payload = document["payload"]
    need(document["payload_sha256"] == hashlib.sha256(
        canonical(payload)).hexdigest(), "payload digest")
    need(payload["schema"] ==
         "TPC319_KY_FAN_CLUSTER_NORMALIZATION_FIREWALL_V1", "schema")
    need(payload["parent_lock"]["certificate_sha256"] ==
         "2465c91d3dcc5edb24bd1cdc8d5cd0748ddfa28efa7e352c2edbffcee2229ffa",
         "parent lock")
    anchor = payload["exact_small_audit"]
    hashes = exact_anchor()
    need(anchor["trace_digest"] == hashes[0] and
         anchor["trace_g2_digest"] == hashes[1] and
         anchor["rayleigh_digest"] == hashes[2], "exact anchor")
    rows = payload["rows"]
    need(len(rows) == 24, "row count")
    indexed = {}
    for row in rows:
        key = (row["scale"], row["Q"], row["kernel_exponent"])
        need(key not in indexed and row["source_count"] == row["scale"] // 2,
             "row geometry")
        need(row["shell"] == shell(row["Q"]), "shell convention")
        spectrum = np.linalg.eigvalsh(
            rebuild(row["scale"], row["Q"], row["kernel_exponent"]))[-(MAX_K + 1):][::-1]
        indexed[key] = row
        for k in K_VALUES:
            mass = float(np.sum(spectrum[:k], dtype=np.float64))
            normalized = mass / row["source_count"]
            stored = row["ky_fan"][str(k)]
            need(close(normalized, float(stored["normalized_estimate"])),
                 "normalized replay")
            need(close(mass, float(stored["unnormalized_estimate"])),
                 "unnormalized replay")
            nlo, nhi = map(float, stored["normalized_interval"])
            ulo, uhi = map(float, stored["unnormalized_interval"])
            need(nlo <= normalized <= nhi and ulo <= mass <= uhi,
                 "interval replay")
            gap = 1.0 - float(spectrum[k] / spectrum[k - 1])
            need(close(gap, float(stored["edge_gap"])), "gap replay")
    comparisons = payload["comparisons"]
    need(len(comparisons) == 80, "comparison count")
    for item in comparisons:
        low = indexed[(item["lower_scale"], item["Q"], item["kernel_exponent"])]
        high = indexed[(item["upper_scale"], item["Q"], item["kernel_exponent"])]
        k = item["k"]
        low_n = low["ky_fan"][str(k)]["normalized_interval"]
        high_n = high["ky_fan"][str(k)]["normalized_interval"]
        low_u = low["ky_fan"][str(k)]["unnormalized_interval"]
        high_u = high["ky_fan"][str(k)]["unnormalized_interval"]
        need(float(high_n[1]) < float(low_n[0]) and
             float(high_u[0]) > float(low_u[1]), "strict trend replay")
        ratio = float(item["unnormalized_ratio"])
        need(1.0 < ratio < 2.0 and
             close(float(item["normalized_ratio"]), ratio / 2.0),
             "normalization identity replay")
    audit = payload["finite_audit"]
    need(audit["normalized_decrease_strict"] == 80 and
         audit["unnormalized_increase_strict"] == 80 and
         audit["normalization_flip_transitions"] == 80, "audit totals")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()
    if not args.check:
        raise SystemExit("explicit --check is required")
    try:
        check()
    except (Failure, OSError, json.JSONDecodeError, KeyError, TypeError,
            ValueError, np.linalg.LinAlgError) as error:
        print("TPC319_INDEPENDENT_CHECK=FAIL " + str(error), file=sys.stderr)
        return 1
    print("TPC319_INDEPENDENT_CHECK=PASS exact_anchor=3 rows=24 k_values=5 "
          "normalized_decreases=80 unnormalized_increases=80 replay=einsum_reverse")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
