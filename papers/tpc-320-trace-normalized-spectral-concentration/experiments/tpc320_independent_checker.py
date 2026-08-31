#!/usr/bin/env python3
"""Independent replay for TPC-320.

The producer uses a SciPy top-spectrum path and a NumPy full-spectrum path in
forward and reverse shell order.  This file deliberately does not import the
producer: it rebuilds the blocks with a reversed loop and ``einsum``, then
checks the stored trace-normalized intervals and diagnostics.
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
    raise SystemExit("TPC320 independent checker requires numpy: " + str(error))

PROJECT = Path(__file__).resolve().parents[1]
ROOT = PROJECT.parents[2]
CERTIFICATE = PROJECT / "results/tpc320_certificate.json"
HEIGHT = 66
SCALES = (640, 1280, 2560)
Q_ANCHORS = (24, 36, 54, 80)
EXPONENTS = (1, 2)
K_VALUES = (1, 2, 4, 8, 16)
MAX_K = max(K_VALUES)


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
            start = p * p
            sieve[start:limit + 1:p] = b"\x00" * (
                (limit - start) // p + 1)
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
    # Reverse order plus einsum makes this an independent accumulation path.
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
    return math.isclose(a, b, rel_tol=5.0e-8, abs_tol=5.0e-9)


def entropy(eigenvalues: np.ndarray, n: int) -> float:
    values = np.maximum(np.asarray(eigenvalues, dtype=np.float64), 0.0)
    total = float(np.sum(values, dtype=np.float64))
    need(total > 0, "positive entropy trace")
    p = values / total
    p = p[p > 0]
    return -float(np.sum(p * np.log(p), dtype=np.float64)) / math.log(n)


def check() -> None:
    raw = CERTIFICATE.read_bytes()
    document = json.loads(raw)
    need(raw == canonical(document), "certificate canonicality")
    need(document.get("certificate_version") == 1 and
         document.get("claim_status", "").startswith("NUMERICALLY_CERTIFIED"),
         "certificate header")
    payload = document["payload"]
    need(document["payload_sha256"] == hashlib.sha256(
        canonical(payload)).hexdigest(), "payload digest")
    need(payload["schema"] ==
         "TPC320_TRACE_NORMALIZED_SPECTRAL_CONCENTRATION_V1", "schema")
    need(payload["parent_lock"]["certificate_sha256"] ==
         "3bd20dfa30870b3e163861a6f712354d50e712f3a61ac1080939327a2da6d4f7",
         "parent lock")
    anchor = payload["exact_small_audit"]
    need((anchor["trace_digest"], anchor["trace_g2_digest"],
          anchor["rayleigh_digest"]) == exact_anchor(), "exact anchor")

    rows = payload["rows"]
    need(len(rows) == 24, "row count")
    indexed: dict[tuple[int, int, int], dict[str, Any]] = {}
    for row in rows:
        key = (row["scale"], row["Q"], row["kernel_exponent"])
        need(key not in indexed and row["scale"] in SCALES and
             row["Q"] in Q_ANCHORS and row["kernel_exponent"] in EXPONENTS,
             "row key")
        need(row["source_count"] == row["scale"] // 2 and
             row["source_interval"] ==
             [row["scale"] // 2 + 1, row["scale"]] and
             row["shell"] == shell(row["Q"]), "row geometry")
        gram = rebuild(*key)
        spectrum = np.linalg.eigvalsh(gram)[::-1]
        need(float(spectrum[0]) > 0 and float(spectrum[-1]) > -1.0e-7,
             "PSD replay")
        trace = float(np.sum(spectrum, dtype=np.float64))
        trace2 = float(np.sum(spectrum * spectrum, dtype=np.float64))
        top1 = float(spectrum[0])
        stable = trace / top1
        participation = trace * trace / trace2
        ent = entropy(spectrum, row["source_count"])
        stored_metrics = row["scale_invariant_metrics"]
        need(close(stable, float(stored_metrics["stable_rank"])),
             "stable-rank replay")
        need(close(participation,
                   float(stored_metrics["participation_rank"])),
             "participation replay")
        need(close(ent, float(stored_metrics["normalized_entropy"])),
             "entropy replay")
        for k in K_VALUES:
            mass = float(np.sum(spectrum[:k], dtype=np.float64))
            concentration = mass / trace
            stored = row["concentration"][str(k)]
            need(close(concentration,
                       float(stored["trace_normalized_estimate"])),
                 "concentration replay")
            low, high = map(float, stored["trace_normalized_interval"])
            need(0 <= low <= concentration <= high <= 1.0,
                 "concentration interval replay")
            gap = float(1.0 - spectrum[k] / spectrum[k - 1])
            need(close(gap, float(stored["edge_gap"])), "gap replay")
        indexed[key] = row

    comparisons = payload["comparisons"]
    need(len(comparisons) == 80, "comparison count")
    for item in comparisons:
        low = indexed[(item["lower_scale"], item["Q"],
                       item["kernel_exponent"])]
        high = indexed[(item["upper_scale"], item["Q"],
                        item["kernel_exponent"])]
        k = item["k"]
        low_interval = low["concentration"][str(k)][
            "trace_normalized_interval"]
        high_interval = high["concentration"][str(k)][
            "trace_normalized_interval"]
        need(float(high_interval[1]) < float(low_interval[0]) and
             item["strict_separation"] is True and
             0 < float(item["ratio"]) < 1 and
             close(float(item["ratio"]),
                   float(item["upper_estimate"]) /
                   float(item["lower_estimate"])),
             "trend replay")
    audit = payload["finite_audit"]
    need(audit["concentration_decrease_strict"] == 80 and
         audit["stable_rank_growth_observation"] == 16 and
         audit["participation_rank_growth_observation"] == 16 and
         audit["fixed_power_credit"] == 0, "audit totals")
    print("TPC320_INDEPENDENT_CHECK=PASS rows=24 comparisons=80 "
          "concentration_decreases=80")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()
    if not args.check:
        raise SystemExit("--check is required")
    try:
        check()
    except (Failure, OSError, json.JSONDecodeError, ValueError,
            np.linalg.LinAlgError) as error:
        print("TPC320_INDEPENDENT_CHECK=FAIL " + str(error),
              file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
