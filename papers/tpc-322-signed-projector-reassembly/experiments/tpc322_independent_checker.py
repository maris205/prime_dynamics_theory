#!/usr/bin/env python3
"""Independent reverse-order replay for TPC-322.

This file intentionally reimplements the block construction and the small
operator-level sign search.  It does not import the producer.
"""

from __future__ import annotations

import argparse
import hashlib
import itertools
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
    raise SystemExit("TPC322 independent checker requires numpy: " + str(error))

PROJECT = Path(__file__).resolve().parents[1]
ROOT = PROJECT.parents[1]
CERTIFICATE = PROJECT / "results/tpc322_certificate.json"
PARENT_CERT = ROOT / (
    "papers/tpc-321-cross-shell-profile-stability/results/"
    "tpc321_certificate.json")
PARENT_SHA256 = (
    "f7048edce7260bceb14acc674311ce0268fb5ae4fdb9914edc0138a5cb7cc6be")
HEIGHT = 66
SCALES = (640, 1280, 2560)
Q_ANCHORS = (24, 36, 54, 80)
EXPONENTS = (1, 2)
GUARD = 1.0e-12
PATH_TOL = 3.0e-8


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
    sieve[0] = 0
    sieve[1] = 0
    for p in range(2, math.isqrt(limit) + 1):
        if sieve[p]:
            start = p * p
            sieve[start:limit + 1:p] = b"\x00" * (
                (limit - start) // p + 1)
    return [p for p in range(2, limit + 1) if sieve[p]]


PRIMES = primes_up_to(160)


def shell(q0: int) -> list[int]:
    return [p for p in PRIMES if q0 < p <= 2 * q0]


def reverse_blocks(scale: int, q0: int, exponent: int
                   ) -> tuple[list[int], list[np.ndarray]]:
    values = np.arange(scale // 2 + 1, scale + 1, dtype=np.int64)
    differences = values[:, None] - values[None, :]
    dd = differences.astype(np.float64)
    kernel = HEIGHT ** (2 * exponent) / (
        HEIGHT * HEIGHT + dd * dd) ** exponent
    primes = list(reversed(shell(q0)))
    blocks = []
    for p in primes:
        valid = ((differences != 0) &
                 (values[:, None] % p != 0) &
                 (values[None, :] % p != 0))
        centered = (np.equal(np.mod(differences, p), 0).astype(np.float64)
                    - 1.0 / (p - 1))
        blocks.append(p * kernel * centered * valid)
    return list(reversed(primes)), list(reversed(blocks))


def block_gram(blocks: list[np.ndarray]) -> np.ndarray:
    m = len(blocks)
    result = np.zeros((m, m), dtype=np.float64)
    # einsum is a separate accumulation path from the producer's elementwise
    # products and explicit summation.
    for i in range(m):
        for j in range(m):
            result[i, j] = float(np.einsum(
                "ij,ij->", blocks[i], blocks[j], optimize=False))
    return (result + result.T) / 2.0


def signs_for(name: str, primes: list[int]) -> np.ndarray:
    if name == "all_plus":
        return np.ones(len(primes), dtype=np.float64)
    if name == "alternating_index":
        return np.asarray([1 if i % 2 == 0 else -1
                           for i in range(len(primes))], dtype=np.float64)
    if name == "mod4_character":
        return np.asarray([1 if p % 4 == 1 else -1
                           for p in primes], dtype=np.float64)
    if name == "half_split":
        return np.asarray([1 if i < len(primes) / 2 else -1
                           for i in range(len(primes))], dtype=np.float64)
    raise Failure("unknown sign pattern")


def ratio(gram: np.ndarray, signs: np.ndarray) -> float:
    direct = float(np.trace(gram))
    value = float(signs @ gram @ signs)
    need(direct > 0 and value >= -1.0e-8, "signed ratio domain")
    return max(0.0, value / direct)


def extrema(gram: np.ndarray) -> tuple[float, float]:
    m = len(gram)
    values = []
    for tail in itertools.product((1, -1), repeat=m - 1):
        values.append(ratio(gram, np.asarray((1,) + tail, dtype=np.float64)))
    return min(values), max(values)


def exact_anchor() -> tuple[str, str]:
    values = list(range(17, 33))
    primes = shell(4)

    def entry(p: int, u: int, t: int) -> Fraction:
        if u == t or u % p == 0 or t % p == 0:
            return Fraction(0)
        centered = Fraction(1) if (u - t) % p == 0 else Fraction(0)
        centered -= Fraction(1, p - 1)
        return p * Fraction(HEIGHT ** 2,
                            (HEIGHT * HEIGHT + (u - t) ** 2)) * centered

    blocks = [[[entry(p, u, t) for t in values] for u in values]
              for p in primes]
    gram = [[sum((blocks[i][u][t] * blocks[j][u][t]
                  for u in range(len(values)) for t in range(len(values))),
                 Fraction(0)) for j in range(len(primes))]
            for i in range(len(primes))]
    direct = sum((gram[i][i] for i in range(len(primes))), Fraction(0))
    signed = sum((((1, -1)[i]) * ((1, -1)[j]) * gram[i][j]
                  for i in range(len(primes)) for j in range(len(primes))),
                 Fraction(0))
    def fd(value: Fraction) -> str:
        return hashlib.sha256(
            f"{value.numerator}/{value.denominator}\n".encode("ascii")
        ).hexdigest()
    return fd(direct), fd(signed)


def close(a: float, b: float) -> bool:
    return math.isclose(a, b, rel_tol=PATH_TOL, abs_tol=PATH_TOL)


def check() -> None:
    need(PARENT_CERT.is_file() and digest(PARENT_CERT.read_bytes()) ==
         PARENT_SHA256, "parent certificate provenance")
    raw = CERTIFICATE.read_bytes()
    document = json.loads(raw)
    need(raw == canonical(document), "certificate canonicality")
    need(document.get("certificate_version") == 1 and
         document.get("claim_status") ==
         "NUMERICALLY_CERTIFIED_FINITE_OPERATOR_LEVEL_SIGNED_PROJECTOR_REASSEMBLY_ATLAS",
         "certificate header")
    payload = document["payload"]
    need(payload["schema"] == "TPC322_SIGNED_PROJECTOR_REASSEMBLY_V1" and
         document["payload_sha256"] == hashlib.sha256(
             canonical(payload)).hexdigest(), "payload digest")
    need(payload["parent_lock"]["certificate_sha256"] == PARENT_SHA256,
         "parent lock")
    need((payload["exact_small_audit"]["direct_energy_digest"],
          payload["exact_small_audit"]["signed_energy_digest"]) ==
         exact_anchor(), "exact anchor")

    rows = payload["rows"]
    need(len(rows) == 24, "row census")
    names = ("all_plus", "alternating_index", "mod4_character", "half_split")
    counts = {name: {"below_one": 0, "above_one": 0} for name in names}
    for row in rows:
        key = (row["scale"], row["Q"], row["kernel_exponent"])
        need(key[0] in SCALES and key[1] in Q_ANCHORS and
             key[2] in EXPONENTS and row["shell"] == shell(key[1]),
             "row geometry")
        need(row["source_interval"] == [key[0] // 2 + 1, key[0]] and
             row["source_count"] == key[0] // 2 and
             row["operator_columns"] == key[0] // 2 and
             row["operator_rows"] == (key[0] // 2) * len(row["shell"]),
             "source geometry")
        primes, blocks = reverse_blocks(*key)
        need(primes == row["shell"], "reverse shell replay")
        gram = block_gram(blocks)
        need(close(float(np.trace(gram)),
                   float(row["direct_hilbert_schmidt_energy"])),
             "direct energy replay")
        for name in names:
            got = ratio(gram, signs_for(name, primes))
            stored = row["pattern_records"][name]
            need(close(got, float(stored["ratio_estimate"])),
                 "pattern ratio replay")
            low, high = map(float, stored["ratio_interval"])
            need(low <= got <= high and
                 low <= float(stored["ratio_estimate"]) <= high,
                 "pattern interval")
            counts[name]["below_one" if got < 1.0 else "above_one"] += 1
        low, high = extrema(gram)
        stored_min = row["minimum"]["ratio_interval"]
        stored_max = row["maximum"]["ratio_interval"]
        min_low, min_high = map(float, stored_min)
        max_low, max_high = map(float, stored_max)
        need(min_low <= low <= min_high and min_low < 1.0 and
             max_low <= high <= max_high and max_low > 1.0,
             "extreme replay")
        need(float(row["minimum"]["projected_fraction_interval"][1]) <= 1.0 and
             float(row["maximum"]["projected_fraction_interval"][1]) <= 1.0,
             "projector fraction")
    need(counts["all_plus"] == {"below_one": 3, "above_one": 21} and
         counts["alternating_index"] == {"below_one": 21, "above_one": 3},
         "pattern census")
    audit = payload["finite_audit"]
    need(audit["minimum_sign_below_one"] == 24 and
         audit["maximum_sign_above_one"] == 24 and
         audit["fixed_power_credit"] == 0 and
         audit["all_plus_law"] == "REFUTED_FINITE_PANEL" and
         audit["alternating_law"] == "REFUTED_FINITE_PANEL",
         "audit firewall")
    firewall = payload["claim_firewall"]
    need(firewall["TPC322_ARITHMETIC_ADVANCE"] == "NO" and
         firewall["TPC322_FIXED_POWER_CREDIT"] == 0 and
         firewall["TPC322_FULL_GATE_B"] == "OPEN" and
         firewall["TPC322_TWIN_PRIME_RESULT"] == "NONE",
         "claim firewall")
    print("TPC322_INDEPENDENT_CHECK=PASS rows=24 min_sign=24/24 "
          "max_sign=24/24 all_plus=3/21 alternating=21/3")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()
    if not args.check:
        raise SystemExit("--check is required")
    try:
        check()
    except (Failure, OSError, json.JSONDecodeError, ValueError) as error:
        print("TPC322_INDEPENDENT_CHECK=FAIL " + str(error),
              file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
