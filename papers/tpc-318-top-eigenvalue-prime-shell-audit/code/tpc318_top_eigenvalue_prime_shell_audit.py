#!/usr/bin/env python3
"""TPC-318: finite top-eigenvalue audit for the literal prime-shell operator.

TPC-317 replaced the Frobenius mass by the Schatten-4 envelope but left the
actual spectral radius open.  This release computes the largest eigenvalue of
the same finite Gram matrices with two independent symmetric eigensolver
paths, records an a-posteriori residual, and propagates a safe entrywise
rounding guard to a finite interval.  The result is deliberately finite and
numerical: it is not an asymptotic arithmetic estimate.
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

os.environ.setdefault("OMP_NUM_THREADS", "1")
os.environ.setdefault("OPENBLAS_NUM_THREADS", "1")
os.environ.setdefault("MKL_NUM_THREADS", "1")

try:
    import numpy as np
    from scipy.linalg import eigh
except ImportError as error:  # pragma: no cover - environment failure path
    raise SystemExit("TPC318 requires numpy and scipy: " + str(error))

if hasattr(sys, "set_int_max_str_digits"):
    sys.set_int_max_str_digits(0)

PROJECT = Path(__file__).resolve().parents[1]
ROOT = PROJECT.parents[1]
RESULT = PROJECT / "results/tpc318_certificate.json"
PARENT_CERT = ROOT / (
    "papers/tpc-317-schatten-four-prime-shell-compression/results/"
    "tpc317_certificate.json")
PARENT_CERT_SHA256 = (
    "72bb54e0d50523e44b262092f1ad9305654114f16b7db4edbfd1e25caaa9f15a")

SCHEMA = "TPC318_TOP_EIGENVALUE_PRIME_SHELL_AUDIT_V1"
STATUS = "NUMERICALLY_CERTIFIED_FINITE_TOP_EIGENVALUE_AUDIT"
ROUND2_CLUE = (
    "AUDIT_THE_TOP_EIGENSPACE_CLUSTER_AND_NORMALIZATION_LAW_BEFORE_"
    "ANY_ARITHMETIC_CANCELLATION_PROMOTION")

HEIGHT = 66
SCALES = (640, 1280, 2560)
Q_ANCHORS = (24, 36, 54, 80)
EXPONENTS = (1, 2)
SMALL_INTERVAL = (17, 32)
SMALL_PRIME = 5
SMALL_EXPONENT = 1
A_ENTRY_BOUND = 160.0
ERROR_MULTIPLIER = 32.0
NEAR_GAP_THRESHOLD = 0.01


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


def display(value: float, digits: int = 14) -> str:
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


def exact_small_audit() -> tuple[Fraction, Fraction, Fraction]:
    """Exact trace powers and a rational Rayleigh lower witness."""
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
    vector = [Fraction(0)] * n
    vector[0] = Fraction(1)
    rayleigh = gram[0][0]
    need(trace > 0 and trace2 > 0 and rayleigh > 0,
         "positive exact anchor")
    return trace, trace2, rayleigh


def gram_matrix(scale: int, q0: int, exponent: int,
                reverse_shell: bool = False) -> np.ndarray:
    """Rebuild the literal source Gram with a specified shell order."""
    lo, hi, n = source_interval(scale)
    values = np.arange(lo, hi + 1, dtype=np.int64)
    differences = values[:, None] - values[None, :]
    dd = differences.astype(np.float64)
    height = float(HEIGHT)
    kernel = (height ** (2 * exponent) /
              (height * height + dd * dd) ** exponent)
    gram = np.zeros((n, n), dtype=np.float64)
    shell = shell_for(q0)
    if reverse_shell:
        shell = list(reversed(shell))
    for prime in shell:
        valid = ((differences != 0) &
                 (values[:, None] % prime != 0) &
                 (values[None, :] % prime != 0))
        centered = ((differences % prime == 0).astype(np.float64) -
                    1.0 / (prime - 1))
        matrix = prime * kernel * centered * valid
        gram += matrix.T @ matrix
    return (gram + gram.T) / 2.0


def gram_entry_guard(n: int, shell_size: int) -> float:
    """A deliberately generous finite binary64 entrywise Gram guard."""
    unit = 2.0 ** -53
    a_error = 128.0 * unit * A_ENTRY_BOUND
    terms = n * shell_size
    gamma = (terms * unit) / (1.0 - terms * unit)
    return ERROR_MULTIPLIER * (
        gamma * terms * (A_ENTRY_BOUND + a_error) ** 2 +
        terms * (2.0 * A_ENTRY_BOUND * a_error + a_error ** 2))


def top_spectrum(gram: np.ndarray) -> dict[str, Any]:
    """Return top two eigenvalues, vector residual, and a second solver value."""
    n = gram.shape[0]
    values, vectors = eigh(gram, subset_by_index=[n - 2, n - 1],
                           check_finite=False, driver="evr")
    top = float(values[-1])
    second = float(values[0])
    vector = np.asarray(vectors[:, -1], dtype=np.float64)
    residual = float(np.linalg.norm(gram @ vector - top * vector))
    alternate = float(np.linalg.eigvalsh(gram)[-1])
    need(top > 0 and second >= 0 and alternate > 0 and
         math.isfinite(residual), "positive top spectrum")
    return {
        "scipy_top": top,
        "scipy_second": second,
        "scipy_residual": residual,
        "numpy_top": alternate,
    }


def spectral_interval(records: list[dict[str, Any]], n: int,
                      shell_size: int) -> tuple[list[str], dict[str, Any]]:
    estimates = [float(record["scipy_top"]) for record in records]
    estimates += [float(record["numpy_top"]) for record in records]
    low_estimate = min(estimates)
    high_estimate = max(estimates)
    center = sum(estimates) / len(estimates)
    spread = high_estimate - low_estimate
    residual_guard = max(float(record["scipy_residual"])
                         for record in records)
    entry_guard = gram_entry_guard(n, shell_size)
    # ||E||_2 <= ||E||_F <= n max_ij |E_ij|.  Two paths are covered by
    # doubling this term; solver spread and a last-bit guard are added too.
    matrix_spectral_guard = 2.0 * n * entry_guard
    round_guard = 256.0 * (2.0 ** -53) * max(1.0, abs(center))
    absolute_guard = (matrix_spectral_guard + spread + residual_guard +
                      round_guard)
    low = max(0.0, low_estimate - absolute_guard) / n
    high = (high_estimate + absolute_guard) / n
    pad = max(1.0e-9 * max(1.0, abs(center / n)),
              16.0 * spread / n, 1.0e-10)
    low = max(0.0, low - pad)
    high += pad
    need(low <= center / n <= high, "top interval containment")
    return [display(low), display(high)], {
        "estimate_normalized": display(center / n),
        "estimate_unnormalized": display(center),
        "solver_spread_unnormalized": display(spread, 16),
        "largest_residual": display(residual_guard, 16),
        "entrywise_gram_guard": display(entry_guard, 16),
        "spectral_guard_unnormalized": display(matrix_spectral_guard, 16),
        "absolute_guard_unnormalized": display(absolute_guard, 16),
        "uniform_entry_bound": display(A_ENTRY_BOUND, 16),
        "error_multiplier": display(ERROR_MULTIPLIER, 16),
        "model": "binary64 dual solver plus finite Weyl guard",
    }


def build_row(scale: int, q0: int, exponent: int) -> dict[str, Any]:
    lo, hi, n = source_interval(scale)
    shell = shell_for(q0)
    forward = gram_matrix(scale, q0, exponent, False)
    reverse = gram_matrix(scale, q0, exponent, True)
    f = top_spectrum(forward)
    r = top_spectrum(reverse)
    interval, guard = spectral_interval([f, r], n, len(shell))
    top_center = as_float(guard["estimate_normalized"])
    second_center = (f["scipy_second"] / n)
    trace2 = float(np.sum(forward * forward, dtype=np.float64))
    s4 = math.sqrt(trace2) / n
    relative_gap = max(0.0, 1.0 - f["scipy_second"] / f["scipy_top"])
    need(top_center > 0 and s4 > 0 and relative_gap >= 0,
         "row metrics")
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
        "top_eigenvalue": {
            "scipy_forward": display(f["scipy_top"], 16),
            "scipy_reverse": display(r["scipy_top"], 16),
            "numpy_forward": display(f["numpy_top"], 16),
            "numpy_reverse": display(r["numpy_top"], 16),
            "normalized_interval": interval,
            "normalized_estimate": display(top_center, 16),
            "residual_forward": display(f["scipy_residual"], 16),
            "residual_reverse": display(r["scipy_residual"], 16),
            "second_eigenvalue_normalized": display(second_center, 16),
            "relative_top_gap": display(relative_gap, 16),
            "top_to_schatten4": display(top_center / s4, 16),
            "guard": guard,
        },
        "trace_power_reference": {
            "schatten4_normalized": display(s4, 16),
            "trace_g2_normalized": display(trace2 / n, 16),
        },
        "finite_identity": (
            "lambda_max(G) is the top eigenvalue of the literal PSD Gram G=A^*A"),
    }


def interval_pair(row: dict[str, Any]) -> tuple[float, float]:
    raw = row["top_eigenvalue"]["normalized_interval"]
    need(isinstance(raw, list) and len(raw) == 2, "top interval")
    low, high = as_float(raw[0]), as_float(raw[1])
    need(0 <= low <= high, "top interval order")
    return low, high


def build_comparison(low: dict[str, Any], high: dict[str, Any]) -> dict[str, Any]:
    need(low["Q"] == high["Q"] and
         low["kernel_exponent"] == high["kernel_exponent"] and
         low["scale"] < high["scale"], "comparison pairing")
    low_interval = interval_pair(low)
    high_interval = interval_pair(high)
    need(high_interval[1] < low_interval[0], "top decrease not separated")
    low_center = as_float(low["top_eigenvalue"]["normalized_estimate"])
    high_center = as_float(high["top_eigenvalue"]["normalized_estimate"])
    need(high_center < low_center, "top center trend")
    return {
        "Q": low["Q"],
        "kernel_exponent": low["kernel_exponent"],
        "lower_scale": low["scale"],
        "upper_scale": high["scale"],
        "quantity": "top_eigenvalue_normalized",
        "direction": "decrease",
        "lower_interval": [display(low_interval[0]), display(low_interval[1])],
        "upper_interval": [display(high_interval[0]), display(high_interval[1])],
        "center_ratio": display(high_center / low_center, 16),
        "finite_log2_slope": display(math.log2(high_center / low_center), 16),
        "strict_interval_separation": True,
    }


def build_payload() -> dict[str, Any]:
    need(PARENT_CERT.is_file() and digest(PARENT_CERT.read_bytes()) ==
         PARENT_CERT_SHA256, "TPC-317 parent certificate lock")
    rows = [build_row(scale, q0, exponent)
            for scale in SCALES for q0 in Q_ANCHORS for exponent in EXPONENTS]
    need(len(rows) == 24, "row census")
    indexed = {(row["scale"], row["Q"], row["kernel_exponent"]): row
               for row in rows}
    need(len(indexed) == 24, "unique row census")
    comparisons = []
    for q0 in Q_ANCHORS:
        for exponent in EXPONENTS:
            for lower, upper in zip(SCALES, SCALES[1:]):
                comparisons.append(build_comparison(
                    indexed[(lower, q0, exponent)],
                    indexed[(upper, q0, exponent)]))
    need(len(comparisons) == 16, "comparison census")
    exact_trace, exact_trace2, rayleigh = exact_small_audit()
    gaps = [as_float(row["top_eigenvalue"]["relative_top_gap"])
            for row in rows]
    slopes = [as_float(item["finite_log2_slope"]) for item in comparisons]
    near = sum(gap < NEAR_GAP_THRESHOLD for gap in gaps)
    return {
        "schema": SCHEMA,
        "parent_lock": {
            "project": "TPC-317 corrected Schatten-4 finite compression",
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
            "spectral_method": (
                "SciPy symmetric subset eigensolver plus NumPy full eigvalsh "
                "on forward and reverse shell accumulations"),
            "normalization": "divide top eigenvalue by source count N",
            "error_model": (
                "safe |K|<=160, dual-path solver spread, residual, and finite "
                "Weyl entrywise guard; numerical only"),
        },
        "exact_small_audit": {
            "interval": list(SMALL_INTERVAL),
            "prime": SMALL_PRIME,
            "kernel_exponent": SMALL_EXPONENT,
            "trace_digest": fraction_digest(exact_trace),
            "trace_g2_digest": fraction_digest(exact_trace2),
            "rayleigh_digest": fraction_digest(rayleigh),
            "trace_decimal": display(float(exact_trace), 16),
            "trace_g2_decimal": display(float(exact_trace2), 16),
            "rayleigh_decimal": display(float(rayleigh), 16),
        },
        "finite_audit": {
            "scales": len(SCALES),
            "rows": len(rows),
            "top_eigenvalue_rows": len(rows),
            "top_decrease_comparison_rows": len(comparisons),
            "top_decrease_strict": len(comparisons),
            "dual_solver_rows": len(rows),
            "residual_rows": len(rows),
            "near_degenerate_rows_relative_gap_lt_0_01": near,
            "relative_gap_min": display(min(gaps), 16),
            "relative_gap_max": display(max(gaps), 16),
            "finite_log2_slope_min": display(min(slopes), 16),
            "finite_log2_slope_max": display(max(slopes), 16),
            "fixed_power_credit": 0,
            "growing_top_eigenvalue_theorem": "OPEN",
        },
        "claim_firewall": {
            "TPC318_TOP_EIGENVALUE_AUDIT":
                "NUMERICALLY_CERTIFIED_FINITE_24_OF_24",
            "TPC318_TOP_EIGENVALUE_DECREASE":
                "NUMERICALLY_CERTIFIED_FINITE_16_OF_16",
            "TPC318_DUAL_SOLVER_AGREEMENT":
                "NUMERICALLY_CERTIFIED_FINITE_24_OF_24",
            "TPC318_RESIDUAL_AUDIT":
                "NUMERICALLY_CERTIFIED_FINITE_24_OF_24",
            "TPC318_NEAR_DEGENERACY":
                "NUMERICALLY_CERTIFIED_FINITE_CENSUS",
            "TPC318_NORMALIZED_TREND":
                "NUMERICAL_OBSERVATION_FINITE_ONLY",
            "TPC318_UNNORMALIZED_POWER": "OPEN",
            "TPC318_ARITHMETIC_CANCELLATION": "OPEN",
            "TPC318_ARITHMETIC_ADVANCE": "NO",
            "TPC318_FIXED_POWER_CREDIT": 0,
            "TPC318_FULL_GATE_B": "OPEN",
            "TPC318_TWIN_PRIME_RESULT": "NONE",
        },
        "round2_clue": ROUND2_CLUE,
        "rows": rows,
        "top_comparisons": comparisons,
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
    need(stored == build_document(), "certificate does not replay")
    print("TPC318_CERTIFICATE=PASS scales=3 rows=24 "
          "top_decreases=16 near_degenerate=" + str(
              stored["payload"]["finite_audit"][
                  "near_degenerate_rows_relative_gap_lt_0_01"]))


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
            print("TPC318_CERTIFICATE=WRITTEN")
        else:
            check_certificate()
    except (CheckFailure, OSError, json.JSONDecodeError, ValueError,
            np.linalg.LinAlgError) as error:
        print("TPC318_CERTIFICATE=FAIL " + str(error), file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
