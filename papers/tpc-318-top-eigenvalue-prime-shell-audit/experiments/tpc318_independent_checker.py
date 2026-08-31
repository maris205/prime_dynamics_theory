#!/usr/bin/env python3
"""Independent replay for the TPC-318 top-eigenvalue certificate.

The replay does not import the producer.  It rebuilds the literal Gram matrix
with an einsum accumulation in reverse shell order and checks that its largest
eigenvalue lies in every stored finite interval.
"""

from __future__ import annotations

import hashlib
import json
import math
import sys
from fractions import Fraction
from pathlib import Path
from typing import Any

import numpy as np

ROOT = Path(__file__).resolve().parents[3]
PROJECT = ROOT / "papers/tpc-318-top-eigenvalue-prime-shell-audit"
RESULT = PROJECT / "results/tpc318_certificate.json"
PARENT = ROOT / (
    "papers/tpc-317-schatten-four-prime-shell-compression/results/"
    "tpc317_certificate.json")
PARENT_SHA256 = (
    "72bb54e0d50523e44b262092f1ad9305654114f16b7db4edbfd1e25caaa9f15a")
SCHEMA = "TPC318_TOP_EIGENVALUE_PRIME_SHELL_AUDIT_V1"
STATUS = "NUMERICALLY_CERTIFIED_FINITE_TOP_EIGENVALUE_AUDIT"
HEIGHT = 66
SCALES = (640, 1280, 2560)
Q_ANCHORS = (24, 36, 54, 80)
EXPONENTS = (1, 2)
SMALL_INTERVAL = (17, 32)
SMALL_PRIME = 5
SMALL_EXPONENT = 1


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


def fraction_digest(value: Fraction) -> str:
    return hashlib.sha256(
        f"{value.numerator}/{value.denominator}\n".encode("ascii")
    ).hexdigest()


def value(raw: str) -> float:
    return float(raw)


def primes_up_to(limit: int) -> list[int]:
    sieve = bytearray(b"\x01") * (limit + 1)
    sieve[:2] = b"\x00\x00"
    for p in range(2, math.isqrt(limit) + 1):
        if sieve[p]:
            start = p * p
            sieve[start:limit + 1:p] = b"\x00" * (
                (limit - start) // p + 1)
    return [p for p in range(2, limit + 1) if sieve[p]]


PRIMES = primes_up_to(160)


def shell(q0: int) -> list[int]:
    return [p for p in PRIMES if q0 < p <= 2 * q0]


def exact_entry(p: int, u: int, t: int, exponent: int) -> Fraction:
    if u == t or u % p == 0 or t % p == 0:
        return Fraction(0)
    centered = (Fraction(1) if (u - t) % p == 0 else Fraction(0))
    centered -= Fraction(1, p - 1)
    return p * Fraction(HEIGHT ** (2 * exponent),
                         (HEIGHT * HEIGHT + (u - t) ** 2) ** exponent) * centered


def exact_small() -> tuple[Fraction, Fraction, Fraction]:
    values = list(range(SMALL_INTERVAL[0], SMALL_INTERVAL[1] + 1))
    n = len(values)
    rows = [[exact_entry(SMALL_PRIME, u, t, SMALL_EXPONENT)
             for t in values] for u in values]
    gram = [[sum((row[i] * row[j] for row in rows), Fraction(0))
             for j in range(n)] for i in range(n)]
    trace = sum((gram[i][i] for i in range(n)), Fraction(0))
    trace2 = sum((gram[i][j] * gram[j][i]
                  for i in range(n) for j in range(n)), Fraction(0))
    # The first coordinate is a positive exact Rayleigh witness.
    rayleigh = gram[0][0]
    return trace, trace2, rayleigh


def independent_gram(scale: int, q0: int, exponent: int) -> np.ndarray:
    lo, hi = scale // 2 + 1, scale
    values = np.arange(lo, hi + 1, dtype=np.int64)
    differences = values[:, None] - values[None, :]
    dd = differences.astype(np.float64)
    kernel = (float(HEIGHT ** (2 * exponent)) /
              (float(HEIGHT * HEIGHT) + dd * dd) ** exponent)
    # Reverse order plus einsum gives a second accumulation route.
    result = np.zeros((len(values), len(values)), dtype=np.float64)
    for p in reversed(shell(q0)):
        valid = ((differences != 0) &
                 (values[:, None] % p != 0) &
                 (values[None, :] % p != 0))
        centered = ((differences % p == 0).astype(np.float64) -
                    1.0 / (p - 1))
        block = p * kernel * centered * valid
        result += np.einsum("ki,kj->ij", block, block, optimize=True)
    return (result + result.T) / 2.0


def interval_contains(raw: Any, number: float, label: str) -> None:
    need(isinstance(raw, list) and len(raw) == 2, label + " type")
    low, high = value(raw[0]), value(raw[1])
    need(0 <= low <= number <= high, label + " containment")


def main() -> int:
    try:
        need(digest(PARENT.read_bytes()) == PARENT_SHA256,
             "parent certificate lock")
        raw = RESULT.read_bytes()
        document = json.loads(raw)
        need(raw == canonical(document), "certificate canonicality")
        need(document.get("certificate_version") == 1 and
             document.get("claim_status") == STATUS, "header")
        payload = document.get("payload", {})
        need(payload.get("schema") == SCHEMA and
             document.get("payload_sha256") == hashlib.sha256(
                 canonical(payload)).hexdigest(), "payload lock")
        protocol = payload.get("protocol", {})
        need(protocol.get("source_scales") == list(SCALES) and
             protocol.get("height") == HEIGHT and
             protocol.get("Q_anchors") == list(Q_ANCHORS) and
             protocol.get("kernel_exponents") == list(EXPONENTS) and
             protocol.get("domain") == "ell^2(I_X)" and
             protocol.get("codomain") == "ell^2(S_Q x I_X)", "protocol")

        trace, trace2, rayleigh = exact_small()
        small = payload.get("exact_small_audit", {})
        need(small.get("interval") == list(SMALL_INTERVAL) and
             small.get("prime") == SMALL_PRIME and
             small.get("kernel_exponent") == SMALL_EXPONENT and
             small.get("trace_digest") == fraction_digest(trace) and
             small.get("trace_g2_digest") == fraction_digest(trace2) and
             small.get("rayleigh_digest") == fraction_digest(rayleigh),
             "exact anchor")

        rows = payload.get("rows", [])
        need(isinstance(rows, list) and len(rows) == 24, "row census")
        indexed: dict[tuple[int, int, int], dict[str, Any]] = {}
        for row in rows:
            scale, q0, exponent = (int(row["scale"]), int(row["Q"]),
                                   int(row["kernel_exponent"]))
            lo, hi = scale // 2 + 1, scale
            n = hi - lo + 1
            sh = shell(q0)
            need(row["source_interval"] == [lo, hi] and
                 row["source_count"] == n and row["height"] == HEIGHT and
                 row["shell"] == sh and row["shell_cardinality"] == len(sh) and
                 row["operator_rows"] == n * len(sh) and
                 row["operator_columns"] == n, "row geometry")
            top = row["top_eigenvalue"]
            interval = top["normalized_interval"]
            gram = independent_gram(scale, q0, exponent)
            replay = float(np.linalg.eigvalsh(gram)[-1]) / n
            interval_contains(interval, replay, "top interval")
            need(float(top["relative_top_gap"]) >= 0 and
                 float(top["top_to_schatten4"]) > 0 and
                 float(top["residual_forward"]) >= 0 and
                 float(top["residual_reverse"]) >= 0, "spectral fields")
            guard = top["guard"]
            need(guard["uniform_entry_bound"] == "160" and
                 guard["model"] == "binary64 dual solver plus finite Weyl guard",
                 "guard fields")
            indexed[(scale, q0, exponent)] = row
        need(len(indexed) == 24, "unique rows")

        comparisons = payload.get("top_comparisons", [])
        need(isinstance(comparisons, list) and len(comparisons) == 16,
             "comparison census")
        for item in comparisons:
            lower = indexed[(int(item["lower_scale"]), int(item["Q"]),
                             int(item["kernel_exponent"]))]
            upper = indexed[(int(item["upper_scale"]), int(item["Q"]),
                             int(item["kernel_exponent"]))]
            low_interval = lower["top_eigenvalue"]["normalized_interval"]
            high_interval = upper["top_eigenvalue"]["normalized_interval"]
            need(float(high_interval[1]) < float(low_interval[0]) and
                 item["direction"] == "decrease" and
                 item["strict_interval_separation"] is True,
                 "comparison trend")
        audit = payload.get("finite_audit", {})
        need(audit.get("top_eigenvalue_rows") == 24 and
             audit.get("top_decrease_strict") == 16 and
             audit.get("dual_solver_rows") == 24 and
             audit.get("residual_rows") == 24 and
             audit.get("fixed_power_credit") == 0 and
             audit.get("growing_top_eigenvalue_theorem") == "OPEN",
             "audit fields")
        firewall = payload.get("claim_firewall", {})
        need(firewall.get("TPC318_TOP_EIGENVALUE_AUDIT") ==
             "NUMERICALLY_CERTIFIED_FINITE_24_OF_24" and
             firewall.get("TPC318_TOP_EIGENVALUE_DECREASE") ==
             "NUMERICALLY_CERTIFIED_FINITE_16_OF_16" and
             firewall.get("TPC318_ARITHMETIC_ADVANCE") == "NO" and
             firewall.get("TPC318_FIXED_POWER_CREDIT") == 0 and
             firewall.get("TPC318_FULL_GATE_B") == "OPEN" and
             firewall.get("TPC318_TWIN_PRIME_RESULT") == "NONE",
             "firewall")
    except (Failure, OSError, json.JSONDecodeError, KeyError, TypeError,
            ValueError, np.linalg.LinAlgError) as error:
        print("TPC318_INDEPENDENT_CHECK=FAIL " + str(error),
              file=sys.stderr)
        return 1
    print("TPC318_INDEPENDENT_CHECK=PASS exact_anchor=3 rows=24 "
          "top_decreases=16 replay=einsum_reverse")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
