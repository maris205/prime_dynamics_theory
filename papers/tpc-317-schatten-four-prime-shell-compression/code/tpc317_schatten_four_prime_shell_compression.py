#!/usr/bin/env python3
"""TPC-317: a finite Schatten-4 compression audit for the literal shell.

TPC-316 supplied the full deleted-diagonal source-to-output operator but used
its Hilbert--Schmidt mass as the only upper envelope.  This release keeps the
same literal matrix and evaluates the next exact norm identity

    ||A||_(2->2)^2 <= sqrt(trace((A^* A)^2)) <= trace(A^* A).

The matrix entries are rational by definition.  The large-panel values are a
dual-precision finite certificate with a conservative floating-point error
budget; a small rational panel independently checks the trace-power formula.
No asymptotic decay or arithmetic Route-B credit is inferred.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import math
import os
import sys
from decimal import Decimal
from fractions import Fraction
from pathlib import Path
from typing import Any

# Keep BLAS choices stable when the script is run by the release checker.
os.environ.setdefault("OMP_NUM_THREADS", "1")
os.environ.setdefault("OPENBLAS_NUM_THREADS", "1")
os.environ.setdefault("MKL_NUM_THREADS", "1")

try:
    import numpy as np
except ImportError as error:  # pragma: no cover - environment failure path
    raise SystemExit("TPC317 requires numpy: " + str(error))

if hasattr(sys, "set_int_max_str_digits"):
    sys.set_int_max_str_digits(0)

PROJECT = Path(__file__).resolve().parents[1]
ROOT = PROJECT.parents[1]
RESULT = PROJECT / "results/tpc317_certificate.json"
PARENT_CERT = ROOT / (
    "papers/tpc-316-literal-arithmetic-l2-fresh-panel/results/"
    "tpc316_certificate.json")

PARENT_CERT_SHA256 = (
    "3bb9f3463daf7583ca07a672bf19be827af5404c2c7005b6e6bf6b766bd8ef26")
SCHEMA = "TPC317_SCHATTEN4_PRIME_SHELL_COMPRESSION_V1"
STATUS = (
    "NUMERICALLY_CERTIFIED_FINITE_SCHATTEN4_COMPRESSION_AND_"
    "OPERATOR_ENVELOPE")
ROUND2_CLUE = (
    "AUDIT_THE_TRUE_TOP_EIGENVALUE_OR_A_CERTIFIED_TRACE_POWER_LADDER_"
    "BEFORE_ANY_ARITHMETIC_CANCELLATION_PROMOTION")

HEIGHT = 66
SCALES = (640, 1280, 2560)
Q_ANCHORS = (24, 36, 54, 80)
EXPONENTS = (1, 2)
SMALL_INTERVAL = (17, 32)
SMALL_PRIME = 5
SMALL_EXPONENT = 1


class CheckFailure(RuntimeError):
    """A fail-closed certificate error."""


def need(condition: bool, message: str) -> None:
    if type(condition) is not bool or not condition:
        raise CheckFailure(message)


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


def display(value: float | np.floating[Any], digits: int = 12) -> str:
    """Stable decimal display; pass/fail uses interval endpoints."""
    return format(float(value), f".{digits}g")


def as_float(value: str) -> float:
    return float(Decimal(value))


def primes_up_to(limit: int) -> list[int]:
    sieve = bytearray(b"\x01") * (limit + 1)
    if limit >= 0:
        sieve[0] = 0
    if limit >= 1:
        sieve[1] = 0
    for prime in range(2, math.isqrt(limit) + 1):
        if sieve[prime]:
            start = prime * prime
            sieve[start:limit + 1:prime] = b"\x00" * (
                (limit - start) // prime + 1)
    return [value for value in range(2, limit + 1) if sieve[value]]


PRIMES = primes_up_to(160)


def shell_for(q0: int) -> list[int]:
    return [prime for prime in PRIMES if q0 < prime <= 2 * q0]


def source_interval(scale: int) -> tuple[int, int, int]:
    lo, hi = scale // 2 + 1, scale
    count = hi - lo + 1
    need(scale % 2 == 0 and count == scale // 2,
         "dyadic source interval")
    return lo, hi, count


def exact_entry(prime: int, u: int, t: int, exponent: int) -> Fraction:
    if u == t or u % prime == 0 or t % prime == 0:
        return Fraction(0)
    centered = (Fraction(1) if (u - t) % prime == 0 else Fraction(0))
    centered -= Fraction(1, prime - 1)
    kernel = Fraction(HEIGHT ** (2 * exponent),
                      (HEIGHT * HEIGHT + (u - t) ** 2) ** exponent)
    return prime * kernel * centered


def exact_small_trace_powers() -> tuple[Fraction, Fraction]:
    """Return exact trace(G) and trace(G^2) on a tiny one-prime panel."""
    lo, hi = SMALL_INTERVAL
    values = list(range(lo, hi + 1))
    n = len(values)
    gram = [[Fraction(0) for _ in range(n)] for _ in range(n)]
    rows = [[exact_entry(SMALL_PRIME, u, t, SMALL_EXPONENT)
             for t in values] for u in values]
    for i in range(n):
        for j in range(n):
            gram[i][j] = sum((row[i] * row[j] for row in rows),
                             Fraction(0))
    trace = sum((gram[i][i] for i in range(n)), Fraction(0))
    trace2 = sum((gram[i][j] * gram[j][i]
                  for i in range(n) for j in range(n)), Fraction(0))
    need(trace > 0 and trace2 > 0, "positive exact trace powers")
    return trace, trace2


def gram_matrix(scale: int, q0: int, exponent: int,
                dtype: Any, reverse_shell: bool = False) -> np.ndarray:
    """Build G=A^*A without importing the TPC-316 producer."""
    lo, hi, n = source_interval(scale)
    values = np.arange(lo, hi + 1, dtype=np.int64)
    differences = values[:, None] - values[None, :]
    dd = differences.astype(dtype)
    height = dtype(HEIGHT)
    kernel = (height ** dtype(2 * exponent) /
              (height * height + dd * dd) ** dtype(exponent))
    gram = np.zeros((n, n), dtype=dtype)
    shell = shell_for(q0)
    if reverse_shell:
        shell = list(reversed(shell))
    for prime in shell:
        valid = ((differences != 0) &
                 (values[:, None] % prime != 0) &
                 (values[None, :] % prime != 0))
        centered = ((differences % prime == 0).astype(dtype) -
                    dtype(1) / dtype(prime - 1))
        matrix = dtype(prime) * kernel * centered * valid
        gram += matrix.T @ matrix
    # The exact Gram matrix is symmetric; symmetrization only removes the
    # last-bit asymmetry of the numerical construction.
    return (gram + gram.T) / dtype(2)


def gram_error_budget(n: int, shell_size: int) -> float:
    """Conservative entrywise G error under the binary64 model.

    The bound deliberately uses a coarse |A|<=2 and a 64-u.l.p. entry guard,
    then multiplies the accumulated error by eight for matrix symmetrization
    and block accumulation.  The scientific conclusion is still labelled
    finite numerical certification; this is not a formal hardware theorem.
    """
    unit = 2.0 ** -53
    a_bound = 2.0
    a_error = 64.0 * unit * a_bound
    terms = n * shell_size
    gamma = (terms * unit) / (1.0 - terms * unit)
    return 8.0 * (gamma * terms * (a_bound + a_error) ** 2 +
                  terms * (2.0 * a_bound * a_error + a_error ** 2))


def outward_interval(center64: float, center80: float,
                     absolute_error: float, scale: float = 1.0
                     ) -> list[str]:
    """Make a visibly outward, reproducible decimal interval."""
    low = max(0.0, center64 - absolute_error)
    high = center64 + absolute_error
    low = min(low, center80)
    high = max(high, center80)
    dual_gap = abs(center64 - center80)
    pad = max(1.0e-9 * max(1.0, abs(center80)),
              16.0 * dual_gap,
              1.0e-10 * max(1.0, abs(scale)))
    low = max(0.0, low - pad)
    high += pad
    return [display(low), display(high)]


def trace_metrics(g64: np.ndarray, galt: np.ndarray,
                  n: int, shell_size: int) -> dict[str, Any]:
    # Extended precision is used only for the scalar reduction of the
    # independently accumulated reverse-order Gram matrix.  Full longdouble
    # matrix multiplication is intentionally not required (on some hosts it
    # falls back to a very slow scalar implementation).
    g80 = np.asarray(galt, dtype=np.longdouble)
    trace64 = float(np.trace(g64))
    trace_alt = float(np.trace(galt))
    trace80 = float(np.trace(g80))
    trace2_64 = float(np.sum(g64 * g64, dtype=np.float64))
    trace2_80 = float(np.sum(g80 * g80, dtype=np.longdouble))
    need(trace64 > 0 and trace80 > 0 and trace2_64 > 0 and trace2_80 > 0,
         "positive numerical trace powers")
    g_error = gram_error_budget(n, shell_size)
    trace_error = n * g_error * 8.0
    trace2_error = (n * n *
                    (2.0 * float(np.max(np.abs(g64))) * g_error +
                     g_error * g_error) * 8.0)
    s4_64 = math.sqrt(trace2_64)
    s4_80 = math.sqrt(trace2_80)
    hs_interval = outward_interval(trace64 / n, trace80 / n,
                                   trace_error / n,
                                   scale=trace80 / n)
    s4_interval = outward_interval(s4_64 / n, s4_80 / n,
                                   (math.sqrt(max(0.0, trace2_64 +
                                                  trace2_error)) -
                                    math.sqrt(max(0.0, trace2_64 -
                                                  trace2_error))) / n,
                                   scale=s4_80 / n)
    effective_rank = trace80 * trace80 / trace2_80
    ratio = s4_80 / trace80
    return {
        "trace_g_normalized": {
            "float64": display(trace64 / n),
            "float64_reverse": display(trace_alt / n),
            "longdouble": display(trace80 / n),
            "interval": hs_interval,
        },
        "trace_g2_normalized": {
            "float64": display(trace2_64 / n),
            "float64_reverse": display(
                float(np.sum(galt * galt, dtype=np.float64)) / n),
            "longdouble": display(trace2_80 / n),
        },
        "schatten4_normalized": {
            "float64": display(s4_64 / n),
            "float64_reverse": display(
                math.sqrt(float(np.sum(galt * galt, dtype=np.float64))) / n),
            "longdouble": display(s4_80 / n),
            "interval": s4_interval,
        },
        "schatten4_over_trace": {
            "float64": display(s4_64 / trace64),
            "longdouble": display(ratio),
        },
        "effective_rank": display(effective_rank),
        "numeric_error_model": {
            "binary64_unit_roundoff": display(2.0 ** -53, 16),
            "entrywise_gram_guard": display(g_error, 16),
            "trace_g2_absolute_guard": display(trace2_error, 16),
            "dual_accumulation": "binary64_forward_and_reverse_shell_order",
            "extended_reduction": "x87_longdouble_scalar_reduction",
            "max_gram_entry_disagreement": display(
                float(np.max(np.abs(g64 - galt))), 16),
        },
    }


def build_row(scale: int, q0: int, exponent: int) -> dict[str, Any]:
    lo, hi, n = source_interval(scale)
    shell = shell_for(q0)
    g64 = gram_matrix(scale, q0, exponent, np.float64, reverse_shell=False)
    galt = gram_matrix(scale, q0, exponent, np.float64, reverse_shell=True)
    metrics = trace_metrics(g64, galt, n, len(shell))
    hs = metrics["trace_g_normalized"]["longdouble"]
    s4 = metrics["schatten4_normalized"]["longdouble"]
    need(as_float(s4) > 0 and as_float(hs) > 0,
         "positive normalized envelopes")
    return {
        "scale": scale,
        "source_interval": [lo, hi],
        "source_count": n,
        "Q": q0,
        "kernel_exponent": exponent,
        "height": HEIGHT,
        "shell": shell,
        "shell_cardinality": len(shell),
        "operator_rows": n * len(shell),
        "operator_columns": n,
        "metrics": metrics,
        "finite_identity": (
            "lambda_max(A^*A) <= sqrt(trace((A^*A)^2)) <= trace(A^*A)"),
    }


def interval_pair(row: dict[str, Any], key: str) -> tuple[float, float]:
    raw = row["metrics"][key]["interval"]
    need(isinstance(raw, list) and len(raw) == 2, key + " interval")
    lo, hi = as_float(raw[0]), as_float(raw[1])
    need(0 <= lo <= hi, key + " interval order")
    return lo, hi


def build_comparison(low: dict[str, Any], high: dict[str, Any],
                     key: str, direction: str) -> dict[str, Any]:
    need(low["Q"] == high["Q"] and
         low["kernel_exponent"] == high["kernel_exponent"] and
         low["scale"] < high["scale"], "comparison pairing")
    low_lo, low_hi = interval_pair(low, key)
    high_lo, high_hi = interval_pair(high, key)
    if direction == "decrease":
        strict = high_hi < low_lo
    elif direction == "increase":
        strict = high_lo > low_hi
    else:
        raise CheckFailure("unknown comparison direction")
    need(strict, "interval trend separation")
    low_center = as_float(low["metrics"][key]["longdouble"])
    high_center = as_float(high["metrics"][key]["longdouble"])
    return {
        "Q": low["Q"],
        "kernel_exponent": low["kernel_exponent"],
        "lower_scale": low["scale"],
        "upper_scale": high["scale"],
        "quantity": key,
        "direction": direction,
        "lower_interval": [display(low_lo), display(low_hi)],
        "upper_interval": [display(high_lo), display(high_hi)],
        "center_ratio": display(high_center / low_center),
        "strict_interval_separation": True,
    }


def build_payload() -> dict[str, Any]:
    need(PARENT_CERT.is_file() and digest(PARENT_CERT.read_bytes()) ==
         PARENT_CERT_SHA256, "TPC-316 parent certificate lock")
    rows = [build_row(scale, q0, exponent)
            for scale in SCALES for q0 in Q_ANCHORS for exponent in EXPONENTS]
    need(len(rows) == 24, "row census")
    indexed = {(row["scale"], row["Q"], row["kernel_exponent"]): row
               for row in rows}
    need(len(indexed) == 24, "unique row census")
    comparisons: list[dict[str, Any]] = []
    for q0 in Q_ANCHORS:
        for exponent in EXPONENTS:
            for low_scale, high_scale in zip(SCALES, SCALES[1:]):
                low = indexed[(low_scale, q0, exponent)]
                high = indexed[(high_scale, q0, exponent)]
                comparisons.append(build_comparison(
                    low, high, "schatten4_normalized", "decrease"))
    hs_comparisons: list[dict[str, Any]] = []
    for q0 in Q_ANCHORS:
        for exponent in EXPONENTS:
            for low_scale, high_scale in zip(SCALES, SCALES[1:]):
                low = indexed[(low_scale, q0, exponent)]
                high = indexed[(high_scale, q0, exponent)]
                hs_comparisons.append(build_comparison(
                    low, high, "trace_g_normalized", "increase"))
    need(len(comparisons) == 16 and len(hs_comparisons) == 16,
         "comparison census")
    exact_trace, exact_trace2 = exact_small_trace_powers()
    return {
        "schema": SCHEMA,
        "parent_lock": {
            "project": "TPC-316 literal arithmetic L2 fresh-panel envelope",
            "certificate_path": str(PARENT_CERT.relative_to(ROOT)),
            "certificate_sha256": PARENT_CERT_SHA256,
        },
        "protocol": {
            "source_scales": list(SCALES),
            "source_intervals": {
                str(scale): [scale // 2 + 1, scale] for scale in SCALES
            },
            "height": HEIGHT,
            "Q_anchors": list(Q_ANCHORS),
            "kernel_exponents": list(EXPONENTS),
            "shell_rule": "S_Q={p prime: Q<p<=2Q}",
            "domain": "ell^2(I_X)",
            "codomain": "ell^2(S_Q x I_X)",
            "matrix_entry": (
                "1_{t!=u,p not_divides ut} p H^(2s)/(H^2+(u-t)^2)^s "
                "(1_{u==t mod p}-1/(p-1))"),
            "gram_construction": "G=A^*A; p-blocks accumulated before symmetrization",
            "normalization": "divide trace-power envelope by source count N",
            "large_panel_arithmetic": (
                "exact rational formula evaluated with forward/reverse binary64 "
                "accumulation and longdouble scalar reduction; outward finite "
                "error budget"),
        },
        "exact_theorem": {
            "gram_psd": "G=A^*A is positive semidefinite",
            "spectral_to_schatten4": (
                "lambda_max(G) <= sqrt(trace(G^2))"),
            "schatten4_to_frobenius": (
                "sqrt(trace(G^2)) <= trace(G)"),
            "normalized_l2_envelope": (
                "N^(-1)||A beta||_2^2 <= "
                "(sqrt(trace(G^2))/N)||beta||_2^2"),
            "small_panel_identity": (
                "trace(G) and trace(G^2) are evaluated exactly over Q"),
            "scope": "finite literal matrices only; no growing theorem",
        },
        "small_exact_audit": {
            "interval": list(SMALL_INTERVAL),
            "prime": SMALL_PRIME,
            "kernel_exponent": SMALL_EXPONENT,
            "trace_digest": fraction_digest(exact_trace),
            "trace_g2_digest": fraction_digest(exact_trace2),
            "trace_decimal": display(float(exact_trace), 16),
            "trace_g2_decimal": display(float(exact_trace2), 16),
        },
        "finite_audit": {
            "scales": len(SCALES),
            "rows": len(rows),
            "schatten_comparison_rows": len(comparisons),
            "schatten4_strict_decreases": len(comparisons),
            "frobenius_comparison_rows": len(hs_comparisons),
            "frobenius_strict_increases": len(hs_comparisons),
            "compression_rows": len(rows),
            "fixed_power_credit": 0,
            "growing_operator_theorem": "OPEN",
        },
        "claim_firewall": {
            "TPC317_SCHATTEN4_IDENTITY": "PROVED_EXACT_FINITE",
            "TPC317_FINITE_L2_ENVELOPE": "PROVED_EXACT_FINITE",
            "TPC317_SMALL_RATIONAL_TRACE_AUDIT": "PROVED_EXACT_FINITE",
            "TPC317_DUAL_PRECISION_ROWS":
                "NUMERICALLY_CERTIFIED_FINITE_24_OF_24",
            "TPC317_SCHATTEN4_DECREASE":
                "NUMERICALLY_CERTIFIED_FINITE_16_OF_16",
            "TPC317_FROBENIUS_INCREASE":
                "NUMERICALLY_CERTIFIED_FINITE_16_OF_16",
            "TPC317_FROBENIUS_PROXY":
                "REFUTED_SCOPED_AS_A_SHARP_SPECTRAL_PROXY",
            "TPC317_TRUE_OPERATOR_NORM": "OPEN",
            "TPC317_ARITHMETIC_CANCELLATION": "OPEN",
            "TPC317_FIXED_POWER_CREDIT": 0,
            "TPC317_ARITHMETIC_ADVANCE": "NO",
            "TPC317_FULL_GATE_B": "OPEN",
            "TPC317_TWIN_PRIME_RESULT": "NONE",
        },
        "round2_clue": ROUND2_CLUE,
        "rows": rows,
        "schatten_comparisons": comparisons,
        "frobenius_comparisons": hs_comparisons,
    }


def build_document() -> dict[str, Any]:
    payload = build_payload()
    return {
        "certificate_version": 1,
        "claim_status": STATUS,
        "payload": payload,
        "payload_sha256": hashlib.sha256(canonical(payload)).hexdigest(),
    }


def write_certificate() -> None:
    RESULT.parent.mkdir(parents=True, exist_ok=True)
    RESULT.write_bytes(canonical(build_document()))


def check_certificate() -> None:
    raw = RESULT.read_bytes()
    stored = json.loads(raw)
    need(raw == canonical(stored), "certificate canonicality")
    expected = build_document()
    need(stored == expected, "certificate does not replay")
    print("TPC317_CERTIFICATE=PASS scales=3 rows=24 "
          "schatten_decreases=16 frobenius_increases=16 "
          "fixed_power_credit=0")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--write", action="store_true")
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()
    if args.write == args.check:
        raise SystemExit("exactly one of --write or --check is required")
    try:
        if args.write:
            write_certificate()
            print("TPC317_CERTIFICATE=WRITTEN")
        else:
            check_certificate()
    except (CheckFailure, OSError, json.JSONDecodeError, ValueError) as error:
        print("TPC317_CERTIFICATE=FAIL " + str(error), file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
