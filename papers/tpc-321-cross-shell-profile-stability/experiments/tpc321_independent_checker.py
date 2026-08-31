#!/usr/bin/env python3
"""Independent reverse-order replay for TPC-321.

This checker does not import the producer.  It rebuilds every Gram matrix in
reverse prime order with an ``einsum`` accumulation and verifies the stored
cross-shell profile distances, thresholds, and majorization labels.
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
    raise SystemExit("TPC321 independent checker requires numpy: " + str(error))

PROJECT = Path(__file__).resolve().parents[1]
ROOT = PROJECT.parents[1]
CERTIFICATE = PROJECT / "results/tpc321_certificate.json"
PARENT_CERT = ROOT / (
    "papers/tpc-320-trace-normalized-spectral-concentration/results/"
    "tpc320_certificate.json")
PARENT_SHA256 = (
    "e8f272423fc14a1d5396549ced921eb66aeae28fbfc978e141230f1d1b0e6230")
HEIGHT = 66
SCALES = (640, 1280, 2560)
Q_ANCHORS = (24, 36, 54, 80)
EXPONENTS = (1, 2)
SIGN_TOL = 1.0e-8
TV_THRESHOLD = 0.03
KS_THRESHOLD = 0.02


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


def close(left: float, right: float) -> bool:
    return math.isclose(left, right, rel_tol=8.0e-7, abs_tol=2.0e-9)


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


def rebuild(scale: int, q0: int, exponent: int) -> np.ndarray:
    values = np.arange(scale // 2 + 1, scale + 1, dtype=np.int64)
    differences = values[:, None] - values[None, :]
    dd = differences.astype(np.float64)
    kernel = HEIGHT ** (2 * exponent) / (
        HEIGHT * HEIGHT + dd * dd) ** exponent
    gram = np.zeros((len(values), len(values)), dtype=np.float64)
    for prime in reversed(shell(q0)):
        valid = ((differences != 0) &
                 (values[:, None] % prime != 0) &
                 (values[None, :] % prime != 0))
        centered = (np.equal(np.mod(differences, prime), 0).astype(
            np.float64) - 1.0 / (prime - 1))
        block = prime * kernel * centered * valid
        gram += np.einsum("ki,kj->ij", block, block, optimize=False)
    return (gram + gram.T) * 0.5


def profile(gram: np.ndarray) -> np.ndarray:
    values = np.linalg.eigvalsh(gram)[::-1]
    need(bool(np.all(np.isfinite(values))), "finite replay spectrum")
    values = np.maximum(values, 0.0)
    total = float(np.sum(values, dtype=np.float64))
    need(total > 0, "positive replay trace")
    result = values / total
    need(math.isclose(float(np.sum(result, dtype=np.float64)), 1.0,
                      rel_tol=3.0e-14, abs_tol=3.0e-14),
         "replay profile normalization")
    return result


def metrics(left: np.ndarray, right: np.ndarray) -> dict[str, Any]:
    delta = np.cumsum(left - right, dtype=np.float64)[:-1]
    tv = 0.5 * float(np.sum(np.abs(left - right), dtype=np.float64))
    ks = float(np.max(np.abs(delta)))
    integrated = float(np.mean(np.abs(delta)))
    minimum = float(np.min(delta))
    maximum = float(np.max(delta))
    if minimum >= -SIGN_TOL and maximum > SIGN_TOL:
        label = "P_MAJORIZES_Q"
    elif maximum <= SIGN_TOL and minimum < -SIGN_TOL:
        label = "Q_MAJORIZES_P"
    elif minimum < -SIGN_TOL and maximum > SIGN_TOL:
        label = "MIXED"
    else:
        label = "UNRESOLVED"
    return {"tv": tv, "ks": ks, "integrated": integrated,
            "minimum": minimum, "maximum": maximum, "label": label}


def exact_anchor() -> tuple[str, str, str]:
    values = list(range(17, 33))

    def entry(p: int, u: int, t: int) -> Fraction:
        if u == t or u % p == 0 or t % p == 0:
            return Fraction(0)
        centered = Fraction(1) if (u - t) % p == 0 else Fraction(0)
        centered -= Fraction(1, p - 1)
        return p * Fraction(HEIGHT ** 2,
                            (HEIGHT * HEIGHT + (u - t) ** 2)) * centered

    rows = [[entry(5, u, t) for t in values] for u in values]
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


def check() -> None:
    need(PARENT_CERT.is_file() and digest(PARENT_CERT.read_bytes()) ==
         PARENT_SHA256, "parent certificate provenance")
    raw = CERTIFICATE.read_bytes()
    document = json.loads(raw)
    need(raw == canonical(document), "certificate canonicality")
    need(document.get("certificate_version") == 1 and
         document.get("claim_status") ==
         "NUMERICALLY_CERTIFIED_FINITE_CROSS_SHELL_PROFILE_SEPARATION_AUDIT",
         "certificate header")
    payload = document["payload"]
    need(payload["schema"] == "TPC321_CROSS_SHELL_PROFILE_STABILITY_V1" and
         document["payload_sha256"] == hashlib.sha256(
             canonical(payload)).hexdigest(), "payload digest")
    need(payload["parent_lock"]["certificate_sha256"] == PARENT_SHA256,
         "payload parent lock")
    protocol = payload["protocol"]
    need(protocol["source_scales"] == list(SCALES) and
         protocol["height"] == HEIGHT and
         protocol["Q_anchors"] == list(Q_ANCHORS) and
         protocol["kernel_exponents"] == list(EXPONENTS), "protocol")
    anchor = payload["exact_small_audit"]
    need((anchor["trace_digest"], anchor["trace_g2_digest"],
          anchor["rayleigh_digest"]) == exact_anchor(), "exact anchor")

    rows = payload["rows"]
    need(len(rows) == 24, "row count")
    indexed: dict[tuple[int, int, int], dict[str, Any]] = {}
    profiles: dict[tuple[int, int, int], np.ndarray] = {}
    for row in rows:
        key = (row["scale"], row["Q"], row["kernel_exponent"])
        need(key not in indexed and key[0] in SCALES and
             key[1] in Q_ANCHORS and key[2] in EXPONENTS,
             "row key")
        need(row["source_count"] == key[0] // 2 and
             row["source_interval"] == [key[0] // 2 + 1, key[0]] and
             row["shell"] == shell(key[1]) and
             row["profile_dimension"] == key[0] // 2,
             "row geometry")
        replay = profile(rebuild(*key))
        need(close(float(replay[0]), float(row["top_share"])),
             "top-share replay")
        profiles[key] = replay
        indexed[key] = row

    comparisons = payload["comparisons"]
    need(len(comparisons) == 18, "comparison count")
    counts = {"P_MAJORIZES_Q": 0, "Q_MAJORIZES_P": 0, "MIXED": 0}
    for item in comparisons:
        low_key = (item["scale"], item["lower_Q"],
                   item["kernel_exponent"])
        high_key = (item["scale"], item["upper_Q"],
                    item["kernel_exponent"])
        need(low_key in indexed and high_key in indexed and
             high_key[1] > low_key[1], "comparison geometry")
        got = metrics(profiles[low_key], profiles[high_key])
        need(got["label"] == item["majorization"] and
             got["label"] in counts, "majorization replay")
        counts[got["label"]] += 1
        need(close(got["tv"], float(item["tv_estimate"])) and
             close(got["ks"], float(item["lorenz_ks_estimate"])) and
             close(got["integrated"],
                   float(item["integrated_lorenz_estimate"])),
             "profile distance replay")
        tv_low, tv_high = map(float, item["tv_interval"])
        ks_low, ks_high = map(float, item["lorenz_ks_interval"])
        need(tv_low <= got["tv"] <= tv_high and
             ks_low <= got["ks"] <= ks_high and
             tv_low > TV_THRESHOLD and ks_low > KS_THRESHOLD and
             item["strict_profile_separation"] is True,
             "profile interval replay")
    need(counts == {"P_MAJORIZES_Q": 3, "Q_MAJORIZES_P": 2,
                    "MIXED": 13}, "majorization census")
    audit = payload["finite_audit"]
    need(audit["profile_separation_strict"] == 18 and
         audit["fixed_power_credit"] == 0 and
         audit["uniform_shell_profile"] == "REFUTED_FINITE_PANEL" and
         audit["uniform_majorization_direction"] ==
         "REFUTED_FINITE_PANEL", "audit")
    firewall = payload["claim_firewall"]
    need(firewall["TPC321_ARITHMETIC_ADVANCE"] == "NO" and
         firewall["TPC321_FIXED_POWER_CREDIT"] == 0 and
         firewall["TPC321_FULL_GATE_B"] == "OPEN" and
         firewall["TPC321_TWIN_PRIME_RESULT"] == "NONE",
         "claim firewall")
    print("TPC321_INDEPENDENT_CHECK=PASS rows=24 comparisons=18 "
          "profile_separation=18 majorization=3/2/13")


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
        print("TPC321_INDEPENDENT_CHECK=FAIL " + str(error), file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
