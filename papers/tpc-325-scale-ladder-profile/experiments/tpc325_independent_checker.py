#!/usr/bin/env python3
"""Independent reverse-order replay for TPC-325.

This checker deliberately does not import the parent producer.  It rebuilds
the literal blocks, accumulates them in reverse order with einsum, and checks
the frozen scale-ladder labels and metric intervals in the certificate.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import math
import sys
from fractions import Fraction
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[3]
PROJECT = ROOT / "papers/tpc-325-scale-ladder-profile"
CERTIFICATE = PROJECT / "results/tpc325_certificate.json"
HEIGHT = 66
ORIGIN = 12001
SCALES = (320, 640, 1280, 2560)
Q_ANCHORS = (24, 36, 54, 80)
EXPONENTS = (1, 2)
LAW_NAMES = ("all_plus", "alternating_index", "mod4_character", "half_split")
LABELS = ("SIGNED_MAJORISES_DIRECT", "DIRECT_MAJORISES_SIGNED",
          "MIXED", "UNRESOLVED")
TOL = 2.0e-6
EXACT_INTERVAL = (12001, 12016)
EXACT_DIRECT_DIGEST = (
    "b21611beb065685432544b4ee8a103e17b3b4193930fe6e4e307916f29982990")
EXACT_SIGNED_DIGEST = (
    "6dd9a73a2269de9e4c50cc5af735da81c251533307dcaf850d75607be6d4a5d6")


class Failure(RuntimeError):
    pass


def need(condition: bool, message: str) -> None:
    if type(condition) is not bool or not condition:
        raise Failure(message)


def canonical(value: object) -> bytes:
    return (json.dumps(value, ensure_ascii=True, sort_keys=True,
                       separators=(",", ":")) + "\n").encode("ascii")


def primes_up_to(limit: int) -> list[int]:
    sieve = bytearray(b"\x01") * (limit + 1)
    sieve[0:2] = b"\x00\x00"
    for p in range(2, math.isqrt(limit) + 1):
        if sieve[p]:
            sieve[p * p:limit + 1:p] = b"\x00" * ((limit - p * p) // p + 1)
    return [p for p in range(2, limit + 1) if sieve[p]]


PRIMES = primes_up_to(160)


def shell(q0: int) -> list[int]:
    return [p for p in PRIMES if q0 < p <= 2 * q0]


def blocks(scale: int, q0: int, exponent: int) -> tuple[list[int], list[np.ndarray]]:
    lo, hi = ORIGIN, ORIGIN + scale // 2 - 1
    values = np.arange(lo, hi + 1, dtype=np.int64)
    differences = values[:, None] - values[None, :]
    dd = differences.astype(np.float64)
    kernel = (float(HEIGHT) ** (2 * exponent) /
              (HEIGHT * HEIGHT + dd * dd) ** exponent)
    result = []
    for p in shell(q0):
        valid = ((differences != 0) & (values[:, None] % p != 0) &
                 (values[None, :] % p != 0))
        centered = ((differences % p == 0).astype(np.float64) -
                    1.0 / (p - 1))
        result.append(p * kernel * centered * valid)
    return shell(q0), result


def profile(gram: np.ndarray) -> np.ndarray:
    values = np.linalg.eigvalsh((gram + gram.T) / 2.0)
    values = np.maximum(values, 0.0)
    total = float(np.sum(values, dtype=np.float64))
    need(total > 0 and math.isfinite(total), "spectral trace")
    answer = values[::-1] / total
    need(abs(float(np.sum(answer)) - 1.0) < 4.0e-14, "profile sum")
    return answer


def metric(signed: np.ndarray, direct: np.ndarray) -> tuple[str, float, float]:
    delta = np.cumsum(signed - direct, dtype=np.float64)[:-1]
    lo, hi = float(np.min(delta)), float(np.max(delta))
    if lo >= -1.0e-10 and hi > 1.0e-10:
        label = "SIGNED_MAJORISES_DIRECT"
    elif hi <= 1.0e-10 and lo < -1.0e-10:
        label = "DIRECT_MAJORISES_SIGNED"
    elif lo < -1.0e-10 and hi > 1.0e-10:
        label = "MIXED"
    else:
        label = "UNRESOLVED"
    tv = 0.5 * float(np.sum(np.abs(signed - direct), dtype=np.float64))
    return label, lo, tv


def sign_vectors(primes: list[int]) -> dict[str, np.ndarray]:
    m = len(primes)
    return {
        "all_plus": np.ones(m, dtype=np.float64),
        "alternating_index": np.asarray(
            [1 if i % 2 == 0 else -1 for i in range(m)], dtype=np.float64),
        "mod4_character": np.asarray(
            [1 if p % 4 == 1 else -1 for p in primes], dtype=np.float64),
        "half_split": np.asarray(
            [1 if i < m / 2 else -1 for i in range(m)], dtype=np.float64),
    }


def exact_anchor() -> tuple[str, str]:
    values = list(range(EXACT_INTERVAL[0], EXACT_INTERVAL[1] + 1))
    primes = shell(4)
    data = [[[Fraction(0) for _ in values] for _ in values]
            for _ in primes]
    for i, p in enumerate(primes):
        for u, value_u in enumerate(values):
            for t, value_t in enumerate(values):
                if value_u == value_t or value_u % p == 0 or value_t % p == 0:
                    continue
                centered = Fraction(1 if (value_u - value_t) % p == 0 else 0)
                centered -= Fraction(1, p - 1)
                data[i][u][t] = p * Fraction(HEIGHT * HEIGHT,
                    (HEIGHT * HEIGHT + (value_u - value_t) ** 2)) * centered
    gram = [[sum((data[i][u][t] * data[j][u][t]
                  for u in range(len(values)) for t in range(len(values))),
                 Fraction(0)) for j in range(len(primes))]
            for i in range(len(primes))]
    direct = sum((gram[i][i] for i in range(len(primes))), Fraction(0))
    signs = [1 if i % 2 == 0 else -1 for i in range(len(primes))]
    signed = sum((signs[i] * signs[j] * gram[i][j]
                  for i in range(len(primes)) for j in range(len(primes))),
                 Fraction(0))
    def h(value: Fraction) -> str:
        return hashlib.sha256(
            f"{value.numerator}/{value.denominator}\n".encode("ascii")
        ).hexdigest()
    return h(direct), h(signed)


def check() -> None:
    raw = CERTIFICATE.read_bytes()
    document = json.loads(raw)
    need(raw == canonical(document), "certificate canonicality")
    payload = document.get("payload", {})
    need(document.get("claim_status") ==
         "NUMERICALLY_CERTIFIED_FINITE_SOURCE_SCALE_LADDER_AUDIT",
         "status")
    need(payload.get("schema") == "TPC325_SCALE_LADDER_PROFILE_V1", "schema")
    rows = payload.get("rows", [])
    need(len(rows) == 32, "row count")
    positions = {(row.get("scale"), row.get("Q"), row.get("kernel_exponent"))
                 for row in rows}
    need(len(positions) == 32, "duplicate rows")
    counts = {name: {label: 0 for label in LABELS} for name in LAW_NAMES}
    energy = {name: {"below_one": 0, "above_one": 0} for name in LAW_NAMES}
    for row in rows:
        scale, q0, exponent = row["scale"], row["Q"], row["kernel_exponent"]
        need(scale in SCALES and q0 in Q_ANCHORS and exponent in EXPONENTS,
             "row protocol")
        need(row["source_interval"] == [ORIGIN, ORIGIN + scale // 2 - 1],
             "source interval")
        primes, data = blocks(scale, q0, exponent)
        direct = np.zeros((len(data[0]), len(data[0])), dtype=np.float64)
        for block in reversed(data):
            direct += np.einsum("ij,ik->jk", block, block, optimize=False)
        direct = (direct + direct.T) / 2.0
        direct_profile = profile(direct)
        for name, signs in sign_vectors(primes).items():
            coherent = np.zeros_like(data[0])
            for block, sign in zip(reversed(data), reversed(signs)):
                coherent += float(sign) * block
            signed = np.einsum("ij,ik->jk", coherent, coherent, optimize=False)
            signed = (signed + signed.T) / 2.0
            signed_profile = profile(signed)
            label, minimum, tv = metric(signed_profile, direct_profile)
            recorded = row["laws"][name]
            counts[name][label] += 1
            need(recorded["majorization"] == label, "label replay")
            need(float(recorded["profile_tv_interval"][0]) - TOL <= tv <=
                 float(recorded["profile_tv_interval"][1]) + TOL,
                 "TV interval")
            need(float(recorded["minimum_prefix_interval"][0]) - TOL <= minimum <=
                 float(recorded["minimum_prefix_interval"][1]) + TOL,
                 "prefix interval")
            ratio = float(np.trace(signed) / np.trace(direct))
            side = "below_one" if ratio < 1.0 else "above_one"
            energy[name][side] += 1
    need(counts == payload["finite_audit"]["profile_majorization_counts"],
         "aggregate profile census")
    need(energy == payload["finite_audit"]["energy_ratio_counts"],
         "aggregate energy census")
    need(exact_anchor() == (EXACT_DIRECT_DIGEST, EXACT_SIGNED_DIGEST),
         "exact anchor")
    print("TPC325_INDEPENDENT_CHECK=PASS rows=32 scales=4 "
          "reverse_einsum=1 exact_anchor=1")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--check", action="store_true")
    parser.parse_args()
    try:
        check()
    except (Failure, OSError, json.JSONDecodeError, ValueError,
            np.linalg.LinAlgError) as error:
        print("TPC325_INDEPENDENT_CHECK=FAIL " + str(error), file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
