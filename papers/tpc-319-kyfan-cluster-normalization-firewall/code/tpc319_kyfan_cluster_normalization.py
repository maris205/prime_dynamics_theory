#!/usr/bin/env python3
"""TPC-319: finite Ky Fan cluster and normalization audit.

The matrix is intentionally rebuilt from the literal prime-shell convention used
by TPC-318.  This release replaces the single top eigenvalue by the Ky Fan mass
F_k=sum_{j<=k} lambda_j and records both F_k and F_k/N.  The result is finite
and numerical; the exact normalization-flip identity is kept separate from the
numerical observations.
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
    raise SystemExit("TPC319 requires numpy and scipy: " + str(error))

if hasattr(sys, "set_int_max_str_digits"):
    sys.set_int_max_str_digits(0)

PROJECT = Path(__file__).resolve().parents[1]
ROOT = PROJECT.parents[1]
RESULT = PROJECT / "results/tpc319_certificate.json"
PARENT_CERT = ROOT / (
    "papers/tpc-318-top-eigenvalue-prime-shell-audit/results/"
    "tpc318_certificate.json")
PARENT_CERT_SHA256 = (
    "2465c91d3dcc5edb24bd1cdc8d5cd0748ddfa28efa7e352c2edbffcee2229ffa")

SCHEMA = "TPC319_KY_FAN_CLUSTER_NORMALIZATION_FIREWALL_V1"
STATUS = "NUMERICALLY_CERTIFIED_FINITE_KY_FAN_CLUSTER_NORMALIZATION_AUDIT"
ROUND2_CLUE = (
    "AUDIT_A_SCALE_INVARIANT_SPECTRAL_MEASURE_OR_PROVE_A_SOURCE_"
    "NORMALIZATION_LAW_BEFORE_ANY_POWER_CLAIM")

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
    """Exact trace powers and one positive coordinate Rayleigh witness."""
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
    """Return top 17 eigenvalues and a residual from two symmetric paths."""
    n = gram.shape[0]
    values, vectors = eigh(gram, subset_by_index=[n - (MAX_K + 1), n - 1],
                           check_finite=False, driver="evr")
    scipy_values = np.asarray(values[::-1], dtype=np.float64)
    numpy_values = np.asarray(np.linalg.eigvalsh(gram)[-(MAX_K + 1):][::-1],
                              dtype=np.float64)
    vector = np.asarray(vectors[:, -1], dtype=np.float64)
    residual = float(np.linalg.norm(gram @ vector -
                                    scipy_values[0] * vector))
    need(len(scipy_values) == MAX_K + 1 and
         len(numpy_values) == MAX_K + 1 and
         scipy_values[0] > 0 and numpy_values[0] > 0 and
         scipy_values[-1] >= 0 and numpy_values[-1] >= 0 and
         math.isfinite(residual), "positive top spectrum")
    return {
        "scipy": [float(value) for value in scipy_values],
        "numpy": [float(value) for value in numpy_values],
        "residual": residual,
    }


def cluster_interval(records: list[dict[str, Any]], n: int,
                     shell_size: int, k: int) -> dict[str, Any]:
    estimates = []
    for record in records:
        estimates.append(sum(record["scipy"][:k]))
        estimates.append(sum(record["numpy"][:k]))
    low_estimate = min(estimates)
    high_estimate = max(estimates)
    center = sum(estimates) / len(estimates)
    spread = high_estimate - low_estimate
    residual_guard = max(float(record["residual"]) for record in records)
    entry_guard = gram_entry_guard(n, shell_size)
    # Weyl gives one spectral-norm error per eigenvalue; the Ky Fan sum costs k.
    matrix_spectral_guard = 2.0 * n * entry_guard
    round_guard = 256.0 * (2.0 ** -53) * max(1.0, abs(center))
    absolute_guard = k * (matrix_spectral_guard + residual_guard +
                          round_guard) + spread
    low = max(0.0, low_estimate - absolute_guard)
    high = high_estimate + absolute_guard
    normalized_low = low / n
    normalized_high = high / n
    pad = max(1.0e-9 * max(1.0, abs(center / n)),
              16.0 * spread / n, 1.0e-10)
    normalized_low = max(0.0, normalized_low - pad)
    normalized_high += pad
    need(normalized_low <= center / n <= normalized_high,
         "cluster normalized interval containment")
    need(low <= center <= high, "cluster unnormalized interval containment")
    return {
        "normalized_interval": [display(normalized_low),
                                 display(normalized_high)],
        "unnormalized_interval": [display(low), display(high)],
        "normalized_estimate": display(center / n, 16),
        "unnormalized_estimate": display(center, 16),
        "solver_spread_unnormalized": display(spread, 16),
        "largest_residual": display(residual_guard, 16),
        "entrywise_gram_guard": display(entry_guard, 16),
        "spectral_guard_unnormalized": display(matrix_spectral_guard, 16),
        "absolute_guard_unnormalized": display(absolute_guard, 16),
        "uniform_entry_bound": display(A_ENTRY_BOUND, 16),
        "error_multiplier": display(ERROR_MULTIPLIER, 16),
        "model": "binary64 dual solver plus finite Weyl guard, Ky Fan factor k",
    }


def build_row(scale: int, q0: int, exponent: int) -> dict[str, Any]:
    lo, hi, n = source_interval(scale)
    shell = shell_for(q0)
    forward = top_spectrum(gram_matrix(scale, q0, exponent, False))
    reverse = top_spectrum(gram_matrix(scale, q0, exponent, True))
    intervals = {}
    for k in K_VALUES:
        interval = cluster_interval([forward, reverse], n, len(shell), k)
        top = forward["scipy"]
        edge_gap = 1.0 - top[k] / top[k - 1]
        mass = sum(top[:k])
        effective_rank = mass * mass / sum(value * value for value in top[:k])
        need(0 <= edge_gap < 1 and effective_rank >= 1,
             "cluster metrics")
        interval.update({
            "edge_gap": display(edge_gap, 16),
            "mass_to_top": display(mass / top[0], 16),
            "effective_rank": display(effective_rank, 16),
            "dual_sum_relative_discrepancy": display(
                max(abs(sum(record[path][:k]) - mass)
                    for record in [forward, reverse]
                    for path in ("scipy", "numpy")) / max(1.0, mass), 16),
        })
        intervals[str(k)] = interval
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
            "scipy_forward": [display(value, 16) for value in forward["scipy"]],
            "scipy_reverse": [display(value, 16) for value in reverse["scipy"]],
            "numpy_forward": [display(value, 16) for value in forward["numpy"]],
            "numpy_reverse": [display(value, 16) for value in reverse["numpy"]],
            "residual_forward": display(forward["residual"], 16),
            "residual_reverse": display(reverse["residual"], 16),
        },
        "ky_fan": intervals,
        "finite_identity": (
            "F_k(G)=sum_{j<=k} lambda_j(G) is the rank-k Ky Fan maximum"),
    }


def interval(row: dict[str, Any], k: int, normalized: bool) -> tuple[float, float]:
    key = "normalized_interval" if normalized else "unnormalized_interval"
    raw = row["ky_fan"][str(k)][key]
    need(isinstance(raw, list) and len(raw) == 2, "cluster interval")
    low, high = as_float(raw[0]), as_float(raw[1])
    need(0 <= low <= high, "cluster interval order")
    return low, high


def estimate(row: dict[str, Any], k: int, normalized: bool) -> float:
    return as_float(row["ky_fan"][str(k)][
        "normalized_estimate" if normalized else "unnormalized_estimate"])


def build_comparison(low: dict[str, Any], high: dict[str, Any], k: int) -> dict[str, Any]:
    need(low["Q"] == high["Q"] and
         low["kernel_exponent"] == high["kernel_exponent"] and
         low["scale"] < high["scale"], "comparison pairing")
    low_n = interval(low, k, True)
    high_n = interval(high, k, True)
    low_u = interval(low, k, False)
    high_u = interval(high, k, False)
    need(high_n[1] < low_n[0], "normalized decrease not separated")
    need(high_u[0] > low_u[1], "unnormalized increase not separated")
    low_norm = estimate(low, k, True)
    high_norm = estimate(high, k, True)
    low_unnorm = estimate(low, k, False)
    high_unnorm = estimate(high, k, False)
    unnorm_ratio = high_unnorm / low_unnorm
    need(1.0 < unnorm_ratio < 2.0, "normalization flip regime")
    return {
        "Q": low["Q"],
        "kernel_exponent": low["kernel_exponent"],
        "k": k,
        "lower_scale": low["scale"],
        "upper_scale": high["scale"],
        "normalized_quantity": "F_k/N",
        "unnormalized_quantity": "F_k",
        "normalized_direction": "decrease",
        "unnormalized_direction": "increase",
        "normalized_lower_interval": [display(low_n[0]), display(low_n[1])],
        "normalized_upper_interval": [display(high_n[0]), display(high_n[1])],
        "unnormalized_lower_interval": [display(low_u[0]), display(low_u[1])],
        "unnormalized_upper_interval": [display(high_u[0]), display(high_u[1])],
        "normalized_ratio": display(high_norm / low_norm, 16),
        "unnormalized_ratio": display(unnorm_ratio, 16),
        "normalized_log2_slope": display(math.log2(high_norm / low_norm), 16),
        "unnormalized_log2_slope": display(math.log2(unnorm_ratio), 16),
        "strict_normalized_separation": True,
        "strict_unnormalized_separation": True,
        "finite_normalization_identity": "normalized_ratio=unnormalized_ratio/2",
    }


def build_payload() -> dict[str, Any]:
    need(PARENT_CERT.is_file() and digest(PARENT_CERT.read_bytes()) ==
         PARENT_CERT_SHA256, "TPC-318 parent certificate lock")
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
    gaps = {str(k): [as_float(row["ky_fan"][str(k)]["edge_gap"])
                     for row in rows] for k in K_VALUES}
    effective = {str(k): [as_float(row["ky_fan"][str(k)]["effective_rank"])
                          for row in rows] for k in K_VALUES}
    normalized_slopes = [as_float(item["normalized_log2_slope"])
                         for item in comparisons]
    unnormalized_slopes = [as_float(item["unnormalized_log2_slope"])
                           for item in comparisons]
    return {
        "schema": SCHEMA,
        "parent_lock": {
            "project": "TPC-318 finite top-eigenvalue audit",
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
            "cluster_sizes": list(K_VALUES),
            "shell_rule": "S_Q={p prime: Q<p<=2Q}",
            "domain": "ell^2(I_X)",
            "codomain": "ell^2(S_Q x I_X)",
            "matrix_entry": (
                "1_{t!=u,p not_divides ut} p H^(2s)/(H^2+(u-t)^2)^s "
                "(1_{u==t mod p}-1/(p-1))"),
            "spectral_method": (
                "SciPy symmetric top-17 eigensolver plus NumPy full eigvalsh "
                "on forward and reverse shell accumulations"),
            "normalization": "F_k divided by source count N",
            "error_model": (
                "safe |K|<=160, dual-path solver spread, residual, and finite "
                "Weyl guard; Ky Fan spectral term multiplied by k; numerical only"),
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
            "cluster_sizes": list(K_VALUES),
            "cluster_intervals": len(rows) * len(K_VALUES),
            "comparisons": len(comparisons),
            "normalized_decrease_strict": len(comparisons),
            "unnormalized_increase_strict": len(comparisons),
            "normalization_flip_transitions": len(comparisons),
            "edge_gap_counts_lt_0_01": {
                key: sum(value < NEAR_GAP_THRESHOLD for value in values)
                for key, values in gaps.items()},
            "edge_gap_min": {key: display(min(values), 16)
                             for key, values in gaps.items()},
            "edge_gap_max": {key: display(max(values), 16)
                             for key, values in gaps.items()},
            "effective_rank_min": {key: display(min(values), 16)
                                    for key, values in effective.items()},
            "effective_rank_max": {key: display(max(values), 16)
                                    for key, values in effective.items()},
            "normalized_log2_slope_min": display(min(normalized_slopes), 16),
            "normalized_log2_slope_max": display(max(normalized_slopes), 16),
            "unnormalized_log2_slope_min": display(min(unnormalized_slopes), 16),
            "unnormalized_log2_slope_max": display(max(unnormalized_slopes), 16),
            "fixed_power_credit": 0,
            "uniform_normalization_law": "OPEN",
        },
        "claim_firewall": {
            "TPC319_KY_FAN_AUDIT": "NUMERICALLY_CERTIFIED_FINITE_24_ROWS_5_K",
            "TPC319_NORMALIZED_DECREASES":
                "NUMERICALLY_CERTIFIED_FINITE_80_OF_80",
            "TPC319_UNNORMALIZED_INCREASES":
                "NUMERICALLY_CERTIFIED_FINITE_80_OF_80",
            "TPC319_NORMALIZATION_FLIP":
                "PROVED_EXACT_FINITE_IDENTITY_PLUS_NUMERICALLY_CERTIFIED_FINITE_80",
            "TPC319_CLUSTER_GAP_CENSUS": "NUMERICAL_OBSERVATION_FINITE",
            "TPC319_EFFECTIVE_RANK": "NUMERICAL_OBSERVATION_FINITE",
            "TPC319_ARITHMETIC_ADVANCE": "NO",
            "TPC319_FIXED_POWER_CREDIT": 0,
            "TPC319_FULL_GATE_B": "OPEN",
            "TPC319_TWIN_PRIME_RESULT": "NONE",
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
    print("TPC319_CERTIFICATE=PASS rows=24 k_values=5 comparisons=80 "
          "normalized_decreases=80 unnormalized_increases=80")


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
            print("TPC319_CERTIFICATE=WRITTEN")
        else:
            check_certificate()
    except (CheckFailure, OSError, json.JSONDecodeError, ValueError,
            np.linalg.LinAlgError) as error:
        print("TPC319_CERTIFICATE=FAIL " + str(error), file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
