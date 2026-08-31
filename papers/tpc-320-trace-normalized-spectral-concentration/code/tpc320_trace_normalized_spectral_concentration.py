#!/usr/bin/env python3
"""TPC-320: scale-invariant spectral concentration audit.

This project keeps the literal prime-shell operator of TPC-318/319 fixed and
changes only the readout.  Instead of dividing a Ky Fan mass by the number of
source columns, we divide by the trace of the same Gram matrix.  For a
positive-semidefinite Gram matrix G with descending eigenvalues lambda_j, the
core quantities are

    C_k(G) = (lambda_1+...+lambda_k) / tr(G),
    r_st(G) = tr(G) / lambda_1,
    r_part(G) = tr(G)^2 / tr(G^2).

The first quantity is a cumulative mass of the trace-normalized spectral
measure.  All three quantities are exactly invariant under multiplication of
G by a positive scalar.  The finite comparisons below are numerical
certificates for the declared panel only; they do not assert a uniform law in
X, nor do they reassemble the prime-shell signs into a twin-prime estimate.
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
    from scipy.linalg import eigh
except ImportError as error:  # pragma: no cover - environment failure path
    raise SystemExit("TPC320 requires numpy and scipy: " + str(error))

if hasattr(sys, "set_int_max_str_digits"):
    sys.set_int_max_str_digits(0)

PROJECT = Path(__file__).resolve().parents[1]
ROOT = PROJECT.parents[1]
RESULT = PROJECT / "results/tpc320_certificate.json"
PARENT_CERT = ROOT / (
    "papers/tpc-319-kyfan-cluster-normalization-firewall/results/"
    "tpc319_certificate.json")
PARENT_CERT_SHA256 = (
    "3bd20dfa30870b3e163861a6f712354d50e712f3a61ac1080939327a2da6d4f7")

SCHEMA = "TPC320_TRACE_NORMALIZED_SPECTRAL_CONCENTRATION_V1"
STATUS = (
    "NUMERICALLY_CERTIFIED_FINITE_TRACE_NORMALIZED_SPECTRAL_CONCENTRATION_"
    "AUDIT")
ROUND2_CLUE = (
    "AUDIT_SPECTRAL_PROFILE_STABILITY_ACROSS_SHELLS_OR_TEST_SIGNED_"
    "PROJECTOR_REASSEMBLY_BEFORE_ANY_ARITHMETIC_POWER_CLAIM")

HEIGHT = 66
SCALES = (640, 1280, 2560)
Q_ANCHORS = (24, 36, 54, 80)
EXPONENTS = (1, 2)
K_VALUES = (1, 2, 4, 8, 16)
MAX_K = max(K_VALUES)
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


def display(value: float, digits: int = 14) -> str:
    return format(float(value), f".{digits}g")


def as_float(value: str) -> float:
    return float(value)


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
    """Exact finite anchor shared with the preceding spectral projects."""
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
    rayleigh = gram[0][0]
    need(trace > 0 and trace2 > 0 and rayleigh > 0,
         "positive exact anchor")
    return trace, trace2, rayleigh


def gram_matrix(scale: int, q0: int, exponent: int,
                reverse_shell: bool = False) -> np.ndarray:
    """Rebuild the literal source Gram matrix in a chosen shell order."""
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


def spectral_paths(gram: np.ndarray) -> dict[str, Any]:
    """Obtain top eigenvalues and full spectral summaries by two paths."""
    n = gram.shape[0]
    values, vectors = eigh(gram, subset_by_index=[n - (MAX_K + 1), n - 1],
                           check_finite=False, driver="evr")
    scipy_top = np.asarray(values[::-1], dtype=np.float64)
    numpy_full = np.asarray(np.linalg.eigvalsh(gram), dtype=np.float64)
    numpy_top = numpy_full[-(MAX_K + 1):][::-1]
    vector = np.asarray(vectors[:, -1], dtype=np.float64)
    residual = float(np.linalg.norm(gram @ vector -
                                    scipy_top[0] * vector))
    trace_direct = float(np.trace(gram))
    trace_eigen = float(np.sum(numpy_full, dtype=np.float64))
    trace2_direct = float(np.sum(gram * gram, dtype=np.float64))
    trace2_eigen = float(np.sum(numpy_full * numpy_full, dtype=np.float64))
    need(len(scipy_top) == MAX_K + 1 and
         len(numpy_top) == MAX_K + 1 and
         scipy_top[0] > 0 and numpy_top[0] > 0 and
         numpy_full[-1] >= 0 and trace_direct > 0 and
         trace_eigen > 0 and trace2_direct > 0 and trace2_eigen > 0 and
         math.isfinite(residual), "positive spectral paths")
    return {
        "scipy": scipy_top,
        "numpy_top": numpy_top,
        "numpy_full": numpy_full,
        "residual": residual,
        "trace_direct": trace_direct,
        "trace_eigen": trace_eigen,
        "trace2_direct": trace2_direct,
        "trace2_eigen": trace2_eigen,
    }


def top_sum_guard(records: list[dict[str, Any]], n: int,
                  shell_size: int, k: int) -> dict[str, Any]:
    estimates = []
    for record in records:
        estimates.append(float(np.sum(record["scipy"][:k], dtype=np.float64)))
        estimates.append(float(np.sum(record["numpy_top"][:k], dtype=np.float64)))
    low_estimate = min(estimates)
    high_estimate = max(estimates)
    center = sum(estimates) / len(estimates)
    spread = high_estimate - low_estimate
    residual_guard = max(float(record["residual"]) for record in records)
    entry_guard = gram_entry_guard(n, shell_size)
    # Weyl gives one spectral-norm error per eigenvalue; a top-k sum costs k.
    matrix_spectral_guard = 2.0 * n * entry_guard
    round_guard = 256.0 * (2.0 ** -53) * max(1.0, abs(center))
    absolute_guard = k * (matrix_spectral_guard + residual_guard +
                          round_guard) + spread
    low = max(0.0, low_estimate - absolute_guard)
    high = high_estimate + absolute_guard
    need(low <= center <= high, "top-sum interval containment")
    return {
        "low": low,
        "high": high,
        "center": center,
        "spread": spread,
        "entry_guard": entry_guard,
        "spectral_guard": matrix_spectral_guard,
        "absolute_guard": absolute_guard,
        "residual": residual_guard,
    }


def trace_guard(records: list[dict[str, Any]], n: int,
                shell_size: int) -> dict[str, Any]:
    estimates = []
    squares = []
    for record in records:
        estimates.extend((float(record["trace_direct"]),
                          float(record["trace_eigen"])))
        squares.extend((float(record["trace2_direct"]),
                        float(record["trace2_eigen"])))
    low = min(estimates)
    high = max(estimates)
    center = sum(estimates) / len(estimates)
    spread = high - low
    square_low = min(squares)
    square_high = max(squares)
    square_center = sum(squares) / len(squares)
    square_spread = square_high - square_low
    entry_guard = gram_entry_guard(n, shell_size)
    unit = 2.0 ** -53
    # The trace is a sum of n diagonal entries.  The extra factor is an
    # outward finite guard for the two arithmetic paths and their reductions.
    round_guard = 256.0 * unit * max(1.0, abs(center))
    absolute_guard = 2.0 * n * entry_guard + round_guard + spread
    trace_low = max(0.0, low - absolute_guard)
    trace_high = high + absolute_guard
    # The Frobenius-square quantity is used as an observation; retain its two
    # path spread explicitly, without promoting it to a theorem.
    square_round_guard = 256.0 * unit * max(1.0, abs(square_center))
    square_guard = square_spread + square_round_guard
    square_out_low = max(0.0, square_low - square_guard)
    square_out_high = square_high + square_guard
    need(trace_low > 0 and trace_low <= center <= trace_high,
         "trace interval containment")
    need(square_out_low > 0 and
         square_out_low <= square_center <= square_out_high,
         "trace-square interval containment")
    return {
        "trace_low": trace_low,
        "trace_high": trace_high,
        "trace_center": center,
        "trace_spread": spread,
        "trace_guard": absolute_guard,
        "trace2_low": square_out_low,
        "trace2_high": square_out_high,
        "trace2_center": square_center,
        "trace2_spread": square_spread,
        "trace2_guard": square_guard,
    }


def safe_entropy(eigenvalues: np.ndarray, n: int) -> float:
    positive = np.maximum(np.asarray(eigenvalues, dtype=np.float64), 0.0)
    total = float(np.sum(positive, dtype=np.float64))
    need(total > 0, "entropy trace")
    probabilities = positive / total
    nonzero = probabilities[probabilities > 0]
    entropy = -float(np.sum(nonzero * np.log(nonzero), dtype=np.float64))
    return entropy / math.log(n)


def build_row(scale: int, q0: int, exponent: int) -> dict[str, Any]:
    lo, hi, n = source_interval(scale)
    shell = shell_for(q0)
    forward = spectral_paths(gram_matrix(scale, q0, exponent, False))
    reverse = spectral_paths(gram_matrix(scale, q0, exponent, True))
    records = [forward, reverse]
    trace = trace_guard(records, n, len(shell))
    concentration = {}
    top = forward["scipy"]
    for k in K_VALUES:
        top_guard = top_sum_guard(records, n, len(shell), k)
        c_low = top_guard["low"] / trace["trace_high"]
        c_high = top_guard["high"] / trace["trace_low"]
        estimate_mass = float(np.sum(top[:k], dtype=np.float64))
        estimate_c = estimate_mass / trace["trace_center"]
        edge_gap = float(1.0 - top[k] / top[k - 1])
        need(0 <= c_low <= estimate_c <= c_high and 0 <= edge_gap < 1,
             "concentration interval")
        concentration[str(k)] = {
            "trace_normalized_interval": [display(c_low), display(c_high)],
            "trace_normalized_estimate": display(estimate_c, 16),
            "ky_fan_mass_estimate": display(estimate_mass, 16),
            "edge_gap": display(edge_gap, 16),
            "top_mass_fraction": display(estimate_c, 16),
            "entrywise_gram_guard": display(top_guard["entry_guard"], 16),
            "spectral_guard_unnormalized": display(
                top_guard["spectral_guard"], 16),
            "absolute_guard_unnormalized": display(
                top_guard["absolute_guard"], 16),
            "trace_guard": display(trace["trace_guard"], 16),
            "model": (
                "binary64 dual solver plus finite Weyl quotient guard; "
                "trace-normalized Ky Fan mass"),
        }
    trace_estimate = trace["trace_center"]
    lambda1 = float(top[0])
    trace2_estimate = trace["trace2_center"]
    stable_rank = trace_estimate / lambda1
    participation = trace_estimate * trace_estimate / trace2_estimate
    # Full-spectrum entropy is intentionally a diagnostic rather than a trend
    # certificate: it is retained to expose the absence of a universal scalar
    # concentration law.
    entropy = sum(safe_entropy(record["numpy_full"], n)
                  for record in records) / len(records)
    need(stable_rank >= 1 and participation >= 1 and 0 < entropy <= 1,
         "scale-invariant metrics")
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
        "top_spectrum": {
            "scipy_forward": [display(value, 16)
                               for value in forward["scipy"]],
            "scipy_reverse": [display(value, 16)
                               for value in reverse["scipy"]],
            "numpy_forward": [display(value, 16)
                               for value in forward["numpy_top"]],
            "numpy_reverse": [display(value, 16)
                               for value in reverse["numpy_top"]],
            "residual_forward": display(forward["residual"], 16),
            "residual_reverse": display(reverse["residual"], 16),
        },
        "trace_summary": {
            "trace_estimate": display(trace_estimate, 16),
            "trace_interval": [display(trace["trace_low"]),
                                display(trace["trace_high"])],
            "trace2_estimate": display(trace2_estimate, 16),
            "trace2_interval": [display(trace["trace2_low"]),
                                 display(trace["trace2_high"])],
            "trace_spread": display(trace["trace_spread"], 16),
            "trace2_spread": display(trace["trace2_spread"], 16),
        },
        "concentration": concentration,
        "scale_invariant_metrics": {
            "stable_rank": display(stable_rank, 16),
            "participation_rank": display(participation, 16),
            "normalized_entropy": display(entropy, 16),
        },
        "finite_identity": (
            "C_k=sum_{j<=k} lambda_j/tr(G); invariant under G -> cG for c>0"),
    }


def interval(row: dict[str, Any], k: int) -> tuple[float, float]:
    raw = row["concentration"][str(k)]["trace_normalized_interval"]
    need(isinstance(raw, list) and len(raw) == 2, "concentration interval")
    low, high = as_float(raw[0]), as_float(raw[1])
    need(0 <= low <= high <= 1.0, "concentration interval order")
    return low, high


def estimate(row: dict[str, Any], k: int) -> float:
    return as_float(row["concentration"][str(k)][
        "trace_normalized_estimate"])


def build_comparison(low: dict[str, Any], high: dict[str, Any],
                     k: int) -> dict[str, Any]:
    need(low["Q"] == high["Q"] and
         low["kernel_exponent"] == high["kernel_exponent"] and
         low["scale"] < high["scale"], "comparison pairing")
    low_interval = interval(low, k)
    high_interval = interval(high, k)
    need(high_interval[1] < low_interval[0],
         "trace-normalized concentration not separated")
    low_value = estimate(low, k)
    high_value = estimate(high, k)
    ratio = high_value / low_value
    need(0 < ratio < 1, "concentration ratio")
    return {
        "Q": low["Q"],
        "kernel_exponent": low["kernel_exponent"],
        "k": k,
        "lower_scale": low["scale"],
        "upper_scale": high["scale"],
        "quantity": "C_k=F_k/tr(G)",
        "direction": "strict_decrease",
        "lower_interval": [display(low_interval[0]),
                            display(low_interval[1])],
        "upper_interval": [display(high_interval[0]),
                            display(high_interval[1])],
        "lower_estimate": display(low_value, 16),
        "upper_estimate": display(high_value, 16),
        "ratio": display(ratio, 16),
        "log2_slope": display(math.log2(ratio), 16),
        "strict_separation": True,
        "scale_invariant_readout": True,
    }


def build_payload() -> dict[str, Any]:
    need(PARENT_CERT.is_file() and digest(PARENT_CERT.read_bytes()) ==
         PARENT_CERT_SHA256, "TPC-319 parent certificate lock")
    rows = [build_row(scale, q0, exponent)
            for scale in SCALES for q0 in Q_ANCHORS for exponent in EXPONENTS]
    need(len(rows) == 24, "row census")
    indexed = {(row["scale"], row["Q"], row["kernel_exponent"]): row
               for row in rows}
    need(len(indexed) == 24, "unique row census")
    comparisons = []
    for q0 in Q_ANCHORS:
        for exponent in EXPONENTS:
            for k in K_VALUES:
                for lower, upper in zip(SCALES, SCALES[1:]):
                    comparisons.append(build_comparison(
                        indexed[(lower, q0, exponent)],
                        indexed[(upper, q0, exponent)], k))
    need(len(comparisons) == 80, "comparison census")
    exact_trace, exact_trace2, rayleigh = exact_small_audit()
    gaps = {str(k): [as_float(row["concentration"][str(k)]["edge_gap"])
                     for row in rows] for k in K_VALUES}
    stable = [as_float(row["scale_invariant_metrics"]["stable_rank"])
              for row in rows]
    participation = [as_float(
        row["scale_invariant_metrics"]["participation_rank"])
        for row in rows]
    entropy = [as_float(row["scale_invariant_metrics"]["normalized_entropy"])
               for row in rows]
    ratios = [as_float(item["ratio"]) for item in comparisons]
    slopes = [as_float(item["log2_slope"]) for item in comparisons]
    metric_index = {(row["Q"], row["kernel_exponent"]): row
                    for row in rows}
    stable_growth = []
    participation_growth = []
    for q0 in Q_ANCHORS:
        for exponent in EXPONENTS:
            for lower, upper in zip(SCALES, SCALES[1:]):
                left = indexed[(lower, q0, exponent)]
                right = indexed[(upper, q0, exponent)]
                stable_growth.append(
                    as_float(right["scale_invariant_metrics"]["stable_rank"]) /
                    as_float(left["scale_invariant_metrics"]["stable_rank"]))
                participation_growth.append(
                    as_float(right["scale_invariant_metrics"][
                        "participation_rank"]) /
                    as_float(left["scale_invariant_metrics"][
                        "participation_rank"]))
    need(all(value > 1 for value in stable_growth) and
         all(value > 1 for value in participation_growth),
         "metric growth observations")
    # The entropy list is intentionally checked only for being nonconstant;
    # this is the adversarial control that prevents a universal scalar claim.
    need(max(entropy) - min(entropy) > 1.0e-6, "entropy variation")
    return {
        "schema": SCHEMA,
        "parent_lock": {
            "project": "TPC-319 Ky Fan cluster normalization firewall",
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
            "concentration_k_values": list(K_VALUES),
            "shell_rule": "S_Q={p prime: Q<p<=2Q}",
            "domain": "ell^2(I_X)",
            "codomain": "ell^2(S_Q x I_X)",
            "matrix_entry": (
                "1_{t!=u,p not_divides ut} p H^(2s)/(H^2+(u-t)^2)^s "
                "(1_{u==t mod p}-1/(p-1))"),
            "spectral_method": (
                "SciPy symmetric top-17 eigensolver plus NumPy full eigvalsh "
                "on forward and reverse shell accumulations"),
            "trace_normalization": (
                "C_k=F_k/tr(G), p_j=lambda_j/tr(G), independent of global "
                "positive scalar"),
            "error_model": (
                "safe |K|<=160, dual-path solver spread, residual, and finite "
                "Weyl quotient guard; numerical only"),
        },
        "exact_small_audit": {
            "interval": list(SMALL_INTERVAL),
            "prime": SMALL_PRIME,
            "kernel_exponent": SMALL_EXPONENT,
            "trace_digest": hashlib.sha256(
                f"{exact_trace.numerator}/{exact_trace.denominator}\n".encode(
                    "ascii")).hexdigest(),
            "trace_g2_digest": hashlib.sha256(
                f"{exact_trace2.numerator}/{exact_trace2.denominator}\n".encode(
                    "ascii")).hexdigest(),
            "rayleigh_digest": hashlib.sha256(
                f"{rayleigh.numerator}/{rayleigh.denominator}\n".encode(
                    "ascii")).hexdigest(),
            "trace_decimal": display(float(exact_trace), 16),
            "trace_g2_decimal": display(float(exact_trace2), 16),
            "rayleigh_decimal": display(float(rayleigh), 16),
        },
        "finite_audit": {
            "scales": len(SCALES),
            "rows": len(rows),
            "concentration_k_values": list(K_VALUES),
            "concentration_intervals": len(rows) * len(K_VALUES),
            "comparisons": len(comparisons),
            "concentration_decrease_strict": len(comparisons),
            "stable_rank_rows": len(stable),
            "stable_rank_growth_observation": len(stable_growth),
            "participation_rank_rows": len(participation),
            "participation_rank_growth_observation": len(participation_growth),
            "entropy_control": "MIXED_FINITE_PANEL",
            "edge_gap_counts_lt_0_01": {
                key: sum(value < NEAR_GAP_THRESHOLD for value in values)
                for key, values in gaps.items()},
            "edge_gap_min": {key: display(min(values), 16)
                             for key, values in gaps.items()},
            "edge_gap_max": {key: display(max(values), 16)
                             for key, values in gaps.items()},
            "trace_normalized_top_share_min": display(
                min(as_float(row["concentration"]["1"][
                    "trace_normalized_estimate"]) for row in rows), 16),
            "trace_normalized_top_share_max": display(
                max(as_float(row["concentration"]["1"][
                    "trace_normalized_estimate"]) for row in rows), 16),
            "stable_rank_min": display(min(stable), 16),
            "stable_rank_max": display(max(stable), 16),
            "participation_rank_min": display(min(participation), 16),
            "participation_rank_max": display(max(participation), 16),
            "normalized_entropy_min": display(min(entropy), 16),
            "normalized_entropy_max": display(max(entropy), 16),
            "concentration_ratio_min": display(min(ratios), 16),
            "concentration_ratio_max": display(max(ratios), 16),
            "log2_slope_min": display(min(slopes), 16),
            "log2_slope_max": display(max(slopes), 16),
            "stable_rank_ratio_min": display(min(stable_growth), 16),
            "stable_rank_ratio_max": display(max(stable_growth), 16),
            "participation_rank_ratio_min": display(min(participation_growth),
                                                      16),
            "participation_rank_ratio_max": display(max(participation_growth),
                                                      16),
            "fixed_power_credit": 0,
            "uniform_concentration_law": "OPEN",
        },
        "claim_firewall": {
            "TPC320_CONCENTRATION_AUDIT":
                "NUMERICALLY_CERTIFIED_FINITE_24_ROWS_5_K",
            "TPC320_CONCENTRATION_DECREASES":
                "NUMERICALLY_CERTIFIED_FINITE_80_OF_80",
            "TPC320_SCALE_INVARIANCE": "PROVED_EXACT_FINITE",
            "TPC320_STABLE_RANK_GROWTH":
                "NUMERICAL_OBSERVATION_FINITE_16_OF_16",
            "TPC320_PARTICIPATION_GROWTH":
                "NUMERICAL_OBSERVATION_FINITE_16_OF_16",
            "TPC320_ENTROPY_CONTROL": "NUMERICAL_OBSERVATION_MIXED",
            "TPC320_ARITHMETIC_ADVANCE": "NO",
            "TPC320_FIXED_POWER_CREDIT": 0,
            "TPC320_FULL_GATE_B": "OPEN",
            "TPC320_TWIN_PRIME_RESULT": "NONE",
        },
        "round2_clue": ROUND2_CLUE,
        "rows": rows,
        "comparisons": comparisons,
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
    print("TPC320_CERTIFICATE=PASS rows=24 k_values=5 comparisons=80 "
          "concentration_decreases=80 stable_rank_growth=16 "
          "participation_growth=16")


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
            print("TPC320_CERTIFICATE=WRITTEN")
        else:
            check_certificate()
    except (CheckFailure, OSError, json.JSONDecodeError, ValueError,
            np.linalg.LinAlgError) as error:
        print("TPC320_CERTIFICATE=FAIL " + str(error), file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
