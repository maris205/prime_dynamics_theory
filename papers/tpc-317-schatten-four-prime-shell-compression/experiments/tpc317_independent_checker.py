#!/usr/bin/env python3
"""Independent replay for the TPC-317 Schatten-4 certificate.

This file deliberately does not import the producer.  It rebuilds the literal
matrix and both shell-order Gram accumulations, checks the exact small panel,
and verifies that every stored large-panel interval contains the replayed
quantities and has the declared trend.
"""

from __future__ import annotations

import hashlib
import json
import math
import sys
from decimal import Decimal
from fractions import Fraction
from pathlib import Path
from typing import Any

import numpy as np

ROOT = Path(__file__).resolve().parents[3]
PROJECT = ROOT / "papers/tpc-317-schatten-four-prime-shell-compression"
RESULT = PROJECT / "results/tpc317_certificate.json"
PARENT = ROOT / (
    "papers/tpc-316-literal-arithmetic-l2-fresh-panel/results/"
    "tpc316_certificate.json")
PARENT_SHA256 = (
    "3bb9f3463daf7583ca07a672bf19be827af5404c2c7005b6e6bf6b766bd8ef26")
SCHEMA = "TPC317_SCHATTEN4_PRIME_SHELL_COMPRESSION_V1"
STATUS = (
    "NUMERICALLY_CERTIFIED_FINITE_SCHATTEN4_COMPRESSION_AND_"
    "OPERATOR_ENVELOPE")
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
    return float(Decimal(raw))


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


def interval(scale: int) -> tuple[int, int, int]:
    lo, hi = scale // 2 + 1, scale
    return lo, hi, hi - lo + 1


def exact_entry(prime: int, u: int, t: int, exponent: int) -> Fraction:
    if u == t or u % prime == 0 or t % prime == 0:
        return Fraction(0)
    centered = (Fraction(1) if (u - t) % prime == 0 else Fraction(0))
    centered -= Fraction(1, prime - 1)
    return prime * Fraction(
        HEIGHT ** (2 * exponent),
        (HEIGHT * HEIGHT + (u - t) ** 2) ** exponent) * centered


def exact_small() -> tuple[Fraction, Fraction]:
    lo, hi = SMALL_INTERVAL
    values = list(range(lo, hi + 1))
    n = len(values)
    rows = [[exact_entry(SMALL_PRIME, u, t, SMALL_EXPONENT)
             for t in values] for u in values]
    gram = [[sum((row[i] * row[j] for row in rows), Fraction(0))
             for j in range(n)] for i in range(n)]
    trace = sum((gram[i][i] for i in range(n)), Fraction(0))
    trace2 = sum((gram[i][j] * gram[j][i]
                  for i in range(n) for j in range(n)), Fraction(0))
    return trace, trace2


def gram(scale: int, q0: int, exponent: int,
         reverse_shell: bool) -> np.ndarray:
    lo, hi, n = interval(scale)
    values = np.arange(lo, hi + 1, dtype=np.int64)
    differences = values[:, None] - values[None, :]
    dd = differences.astype(np.float64)
    kernel = (float(HEIGHT ** (2 * exponent)) /
              (float(HEIGHT * HEIGHT) + dd * dd) ** exponent)
    result = np.zeros((n, n), dtype=np.float64)
    primes = shell(q0)
    if reverse_shell:
        primes = list(reversed(primes))
    for prime in primes:
        valid = ((differences != 0) &
                 (values[:, None] % prime != 0) &
                 (values[None, :] % prime != 0))
        centered = ((differences % prime == 0).astype(np.float64) -
                    1.0 / (prime - 1))
        matrix = prime * kernel * centered * valid
        result += matrix.T @ matrix
    return (result + result.T) / 2.0


def check_metric_interval(raw: Any, replay: float, label: str) -> None:
    need(isinstance(raw, list) and len(raw) == 2, label + " interval type")
    lo, hi = value(raw[0]), value(raw[1])
    need(0 <= lo <= hi and lo <= replay <= hi,
         label + " replay outside interval")


def main() -> int:
    try:
        need(digest(PARENT.read_bytes()) == PARENT_SHA256,
             "parent certificate lock")
        raw = RESULT.read_bytes()
        document = json.loads(raw)
        need(raw == canonical(document), "certificate canonicality")
        need(document.get("certificate_version") == 1 and
             document.get("claim_status") == STATUS, "certificate header")
        payload = document.get("payload")
        need(isinstance(payload, dict) and
             payload.get("schema") == SCHEMA and
             document.get("payload_sha256") == hashlib.sha256(
                 canonical(payload)).hexdigest(), "payload lock")
        parent = payload.get("parent_lock", {})
        need(parent.get("certificate_sha256") == PARENT_SHA256,
             "parent payload lock")
        protocol = payload.get("protocol", {})
        need(protocol.get("source_scales") == list(SCALES) and
             protocol.get("height") == HEIGHT and
             protocol.get("Q_anchors") == list(Q_ANCHORS) and
             protocol.get("kernel_exponents") == list(EXPONENTS) and
             protocol.get("domain") == "ell^2(I_X)" and
             protocol.get("codomain") == "ell^2(S_Q x I_X)",
             "protocol lock")

        exact_trace, exact_trace2 = exact_small()
        small = payload.get("small_exact_audit", {})
        need(small.get("interval") == list(SMALL_INTERVAL) and
             small.get("prime") == SMALL_PRIME and
             small.get("kernel_exponent") == SMALL_EXPONENT and
             small.get("trace_digest") == fraction_digest(exact_trace) and
             small.get("trace_g2_digest") == fraction_digest(exact_trace2),
             "exact small trace audit")

        rows = payload.get("rows", [])
        need(isinstance(rows, list) and len(rows) == 24, "row census")
        indexed: dict[tuple[int, int, int], dict[str, Any]] = {}
        for row in rows:
            scale, q0, exponent = (int(row["scale"]), int(row["Q"]),
                                   int(row["kernel_exponent"]))
            lo, hi, n = interval(scale)
            sh = shell(q0)
            need(row["source_interval"] == [lo, hi] and
                 row["source_count"] == n and row["height"] == HEIGHT and
                 row["shell"] == sh and
                 row["shell_cardinality"] == len(sh) and
                 row["operator_rows"] == n * len(sh) and
                 row["operator_columns"] == n, "row geometry")
            g = gram(scale, q0, exponent, False)
            gr = gram(scale, q0, exponent, True)
            g80 = np.asarray(gr, dtype=np.longdouble)
            trace = float(np.trace(g))
            trace_r = float(np.trace(gr))
            trace80 = float(np.trace(g80))
            trace2 = float(np.sum(g * g, dtype=np.float64))
            trace2_r = float(np.sum(gr * gr, dtype=np.float64))
            trace2_80 = float(np.sum(g80 * g80, dtype=np.longdouble))
            s4 = math.sqrt(trace2)
            s4_r = math.sqrt(trace2_r)
            s4_80 = math.sqrt(trace2_80)
            metrics = row["metrics"]
            check_metric_interval(
                metrics["trace_g_normalized"]["interval"], trace / n,
                "trace interval")
            check_metric_interval(
                metrics["trace_g_normalized"]["interval"], trace_r / n,
                "reverse trace interval")
            check_metric_interval(
                metrics["schatten4_normalized"]["interval"], s4 / n,
                "Schatten-4 interval")
            check_metric_interval(
                metrics["schatten4_normalized"]["interval"], s4_r / n,
                "reverse Schatten-4 interval")
            check_metric_interval(
                metrics["schatten4_normalized"]["interval"], s4_80 / n,
                "extended-reduction Schatten-4 interval")
            need(float(metrics["effective_rank"]) > 0,
                 "effective rank")
            indexed[(scale, q0, exponent)] = row
        need(len(indexed) == 24, "unique row census")

        schatten = payload.get("schatten_comparisons", [])
        frobenius = payload.get("frobenius_comparisons", [])
        need(len(schatten) == 16 and len(frobenius) == 16,
             "comparison census")
        for comparison in schatten:
            q0, exponent = int(comparison["Q"]), int(
                comparison["kernel_exponent"])
            low = indexed[(int(comparison["lower_scale"]), q0, exponent)]
            high = indexed[(int(comparison["upper_scale"]), q0, exponent)]
            low_hi = value(low["metrics"]["schatten4_normalized"]
                           ["interval"][1])
            high_lo = value(high["metrics"]["schatten4_normalized"]
                            ["interval"][0])
            need(comparison["quantity"] == "schatten4_normalized" and
                 comparison["direction"] == "decrease" and
                 comparison["strict_interval_separation"] is True and
                 high_lo > 0 and high_lo < low_hi,
                 "Schatten trend")
        for comparison in frobenius:
            q0, exponent = int(comparison["Q"]), int(
                comparison["kernel_exponent"])
            low = indexed[(int(comparison["lower_scale"]), q0, exponent)]
            high = indexed[(int(comparison["upper_scale"]), q0, exponent)]
            low_hi = value(low["metrics"]["trace_g_normalized"]
                           ["interval"][1])
            high_lo = value(high["metrics"]["trace_g_normalized"]
                            ["interval"][0])
            need(comparison["quantity"] == "trace_g_normalized" and
                 comparison["direction"] == "increase" and
                 comparison["strict_interval_separation"] is True and
                 high_lo > low_hi,
                 "Frobenius trend")

        audit = payload.get("finite_audit", {})
        need(audit.get("scales") == 3 and audit.get("rows") == 24 and
             audit.get("schatten4_strict_decreases") == 16 and
             audit.get("frobenius_strict_increases") == 16 and
             audit.get("fixed_power_credit") == 0 and
             audit.get("growing_operator_theorem") == "OPEN",
             "audit firewall")
        firewall = payload.get("claim_firewall", {})
        need(firewall.get("TPC317_SCHATTEN4_IDENTITY") ==
             "PROVED_EXACT_FINITE" and
             firewall.get("TPC317_SCHATTEN4_DECREASE") ==
             "NUMERICALLY_CERTIFIED_FINITE_16_OF_16" and
             firewall.get("TPC317_FROBENIUS_INCREASE") ==
             "NUMERICALLY_CERTIFIED_FINITE_16_OF_16" and
             firewall.get("TPC317_FIXED_POWER_CREDIT") == 0 and
             firewall.get("TPC317_ARITHMETIC_ADVANCE") == "NO" and
             firewall.get("TPC317_TRUE_OPERATOR_NORM") == "OPEN" and
             firewall.get("TPC317_FULL_GATE_B") == "OPEN" and
             firewall.get("TPC317_TWIN_PRIME_RESULT") == "NONE",
             "claim firewall")
    except (Failure, OSError, json.JSONDecodeError, KeyError, TypeError,
            ValueError, OverflowError) as error:
        print("TPC317_INDEPENDENT_CHECK=FAIL " + str(error),
              file=sys.stderr)
        return 1
    print("TPC317_INDEPENDENT_CHECK=PASS exact_small=2 rows=24 "
          "schatten_decreases=16 frobenius_increases=16")
    return 0


if __name__ == "__main__":
    if "--check" not in sys.argv[1:]:
        raise SystemExit("explicit --check is required")
    raise SystemExit(main())
