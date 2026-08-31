#!/usr/bin/env python3
"""TPC-321: cross-shell stability of the trace-normalized spectrum.

The literal deleted-diagonal centered prime-shell operator is kept fixed.  If
G_{X,Q,s} is its positive-semidefinite Gram matrix and

    p(G) = (lambda_1/tr(G), ..., lambda_N/tr(G)),

with the eigenvalues in decreasing order, this project compares p(G) for
adjacent prime shells Q -> Q'.  The comparison is deliberately made in rank
space: total variation is the l1 distance between the ordered mass vectors,
and the Lorenz/Ky-Fan discrepancy is the maximum difference of their
partial sums.  These are finite profile diagnostics, not a claim about an
infinite limiting spectral measure or about arithmetic cancellation.
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
    raise SystemExit("TPC321 requires numpy and scipy: " + str(error))

if hasattr(sys, "set_int_max_str_digits"):
    sys.set_int_max_str_digits(0)

PROJECT = Path(__file__).resolve().parents[1]
ROOT = PROJECT.parents[1]
RESULT = PROJECT / "results/tpc321_certificate.json"
PARENT_CERT = ROOT / (
    "papers/tpc-320-trace-normalized-spectral-concentration/results/"
    "tpc320_certificate.json")
PARENT_CERT_SHA256 = (
    "e8f272423fc14a1d5396549ced921eb66aeae28fbfc978e141230f1d1b0e6230")

SCHEMA = "TPC321_CROSS_SHELL_PROFILE_STABILITY_V1"
STATUS = "NUMERICALLY_CERTIFIED_FINITE_CROSS_SHELL_PROFILE_SEPARATION_AUDIT"
ROUND2_CLUE = (
    "TEST_SIGNED_PROJECTOR_REASSEMBLY_OR_PROVE_A_UNIFORM_SHELL_PROFILE_"
    "BOUND_BEFORE_ANY_ARITHMETIC_POWER_CLAIM")

HEIGHT = 66
SCALES = (640, 1280, 2560)
Q_ANCHORS = (24, 36, 54, 80)
EXPONENTS = (1, 2)
PROFILE_PATHS = ("numpy_forward", "numpy_reverse", "scipy_forward")
SIGN_TOL = 1.0e-8
NUMERICAL_GUARD = 1.0e-12
TV_THRESHOLD = 0.03
KS_THRESHOLD = 0.02
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


def display(value: float, digits: int = 14) -> str:
    return format(float(value), f".{digits}g")


def primes_up_to(limit: int) -> list[int]:
    sieve = bytearray(b"\x01") * (limit + 1)
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
    centered = Fraction(1) if (u - t) % prime == 0 else Fraction(0)
    centered -= Fraction(1, prime - 1)
    kernel = Fraction(HEIGHT ** (2 * exponent),
                      (HEIGHT * HEIGHT + (u - t) ** 2) ** exponent)
    return prime * kernel * centered


def exact_small_audit() -> tuple[Fraction, Fraction, Fraction]:
    values = list(range(*[SMALL_INTERVAL[0], SMALL_INTERVAL[1] + 1]))
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
    """Rebuild the literal prime-shell Gram matrix."""
    lo, hi, _ = source_interval(scale)
    values = np.arange(lo, hi + 1, dtype=np.int64)
    differences = values[:, None] - values[None, :]
    dd = differences.astype(np.float64)
    height = float(HEIGHT)
    kernel = (height ** (2 * exponent) /
              (height * height + dd * dd) ** exponent)
    gram = np.zeros((len(values), len(values)), dtype=np.float64)
    shell = shell_for(q0)
    if reverse_shell:
        shell = list(reversed(shell))
    for prime in shell:
        valid = ((differences != 0) &
                 (values[:, None] % prime != 0) &
                 (values[None, :] % prime != 0))
        centered = ((differences % prime == 0).astype(np.float64) -
                    1.0 / (prime - 1))
        block = prime * kernel * centered * valid
        gram += block.T @ block
    return (gram + gram.T) / 2.0


def normalize_spectrum(values: np.ndarray) -> np.ndarray:
    ordered = np.asarray(values, dtype=np.float64)[::-1]
    need(bool(np.all(np.isfinite(ordered))), "finite spectrum")
    clipped = np.maximum(ordered, 0.0)
    total = float(np.sum(clipped, dtype=np.float64))
    need(total > 0 and math.isfinite(total), "positive spectral trace")
    profile = clipped / total
    need(bool(np.all(np.isfinite(profile))) and
         math.isclose(float(np.sum(profile, dtype=np.float64)), 1.0,
                      rel_tol=2.0e-14, abs_tol=2.0e-14),
         "normalized profile")
    return profile


def spectral_paths(gram: np.ndarray) -> dict[str, np.ndarray]:
    """Use two eigensolvers while retaining both shell accumulation orders."""
    scipy_values = eigh(gram, eigvals_only=True, check_finite=False,
                        driver="evr")
    numpy_values = np.linalg.eigvalsh(gram)
    scipy_profile = normalize_spectrum(scipy_values)
    numpy_profile = normalize_spectrum(numpy_values)
    need(float(scipy_profile[0]) > 0 and float(numpy_profile[0]) > 0,
         "positive top spectral mass")
    return {"scipy": scipy_profile, "numpy": numpy_profile}


def profile_digest(profile: np.ndarray) -> str:
    rounded = np.round(np.asarray(profile, dtype=np.float64), 14)
    return hashlib.sha256(rounded.astype("<f8", copy=False).tobytes()).hexdigest()


def profile_metrics(left: np.ndarray, right: np.ndarray) -> dict[str, Any]:
    need(len(left) == len(right) and len(left) > 1,
         "profile dimensions")
    delta = np.cumsum(left - right, dtype=np.float64)
    interior = delta[:-1]
    tv = 0.5 * float(np.sum(np.abs(left - right), dtype=np.float64))
    ks = float(np.max(np.abs(interior)))
    integrated = float(np.mean(np.abs(interior)))
    minimum = float(np.min(interior))
    maximum = float(np.max(interior))
    need(0 <= tv <= 1 and 0 <= ks <= 1 and 0 <= integrated <= 1 and
         math.isfinite(minimum) and math.isfinite(maximum),
         "profile metric range")
    if minimum >= -SIGN_TOL and maximum > SIGN_TOL:
        classification = "P_MAJORIZES_Q"
    elif maximum <= SIGN_TOL and minimum < -SIGN_TOL:
        classification = "Q_MAJORIZES_P"
    elif minimum < -SIGN_TOL and maximum > SIGN_TOL:
        classification = "MIXED"
    else:
        classification = "UNRESOLVED"
    return {
        "tv": tv,
        "lorenz_ks": ks,
        "integrated_lorenz": integrated,
        "min_cumulative_delta": minimum,
        "max_cumulative_delta": maximum,
        "majorization": classification,
    }


def metric_interval(values: list[float]) -> tuple[float, float]:
    low = max(0.0, min(values) - NUMERICAL_GUARD)
    high = min(1.0, max(values) + NUMERICAL_GUARD)
    need(low <= min(values) <= max(values) <= high,
         "outward metric interval")
    return low, high


def path_map(paths: dict[str, dict[str, np.ndarray]]) -> dict[str, np.ndarray]:
    return {
        "numpy_forward": paths["forward"]["numpy"],
        "numpy_reverse": paths["reverse"]["numpy"],
        "scipy_forward": paths["forward"]["scipy"],
    }


def build_row(scale: int, q0: int, exponent: int) -> tuple[
        dict[str, Any], dict[str, np.ndarray]]:
    lo, hi, n = source_interval(scale)
    shell = shell_for(q0)
    forward = spectral_paths(gram_matrix(scale, q0, exponent, False))
    reverse = spectral_paths(gram_matrix(scale, q0, exponent, True))
    profiles = path_map({"forward": forward, "reverse": reverse})
    self_metrics = [profile_metrics(profiles["numpy_forward"], profile)
                    for profile in profiles.values()]
    path_l1 = [value["tv"] for value in self_metrics]
    path_ks = [value["lorenz_ks"] for value in self_metrics]
    path_integrated = [value["integrated_lorenz"] for value in self_metrics]
    need(max(path_l1) < 1.0e-7 and max(path_ks) < 1.0e-7,
         "dual-path profile agreement")
    numpy_forward = profiles["numpy_forward"]
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
        "profile_dimension": n,
        "profile_digests": {
            name: profile_digest(profile) for name, profile in profiles.items()
        },
        "top_share": display(float(numpy_forward[0]), 16),
        "path_agreement": {
            "l1_max": display(max(path_l1), 16),
            "lorenz_ks_max": display(max(path_ks), 16),
            "integrated_lorenz_max": display(max(path_integrated), 16),
        },
        "trace_normalization": (
            "p_j=lambda_j/tr(G), descending rank profile; positive-scalar "
            "invariant"),
        "model": "literal centered prime-shell Gram; binary64 eigensolvers",
    }, profiles


def build_comparison(lower: dict[str, np.ndarray],
                     upper: dict[str, np.ndarray], scale: int, q0: int,
                     exponent: int) -> dict[str, Any]:
    path_pairs = [(lower[left], upper[right])
                  for left in PROFILE_PATHS for right in PROFILE_PATHS]
    metrics = [profile_metrics(left, right) for left, right in path_pairs]
    estimate = profile_metrics(lower["numpy_forward"],
                               upper["numpy_forward"])
    classifications = sorted({item["majorization"] for item in metrics})
    need(classifications == [estimate["majorization"]],
         "path majorization classification disagreement")
    tv_interval = metric_interval([item["tv"] for item in metrics])
    ks_interval = metric_interval([item["lorenz_ks"] for item in metrics])
    integrated_interval = metric_interval(
        [item["integrated_lorenz"] for item in metrics])
    need(tv_interval[0] > TV_THRESHOLD and ks_interval[0] > KS_THRESHOLD,
         "profile separation threshold")
    return {
        "scale": scale,
        "lower_Q": q0,
        "upper_Q": Q_ANCHORS[Q_ANCHORS.index(q0) + 1],
        "kernel_exponent": exponent,
        "quantity": "ordered trace-normalized spectral profile",
        "tv_interval": [display(tv_interval[0], 16),
                         display(tv_interval[1], 16)],
        "tv_estimate": display(estimate["tv"], 16),
        "lorenz_ks_interval": [display(ks_interval[0], 16),
                               display(ks_interval[1], 16)],
        "lorenz_ks_estimate": display(estimate["lorenz_ks"], 16),
        "integrated_lorenz_interval": [display(integrated_interval[0], 16),
                                        display(integrated_interval[1], 16)],
        "integrated_lorenz_estimate": display(
            estimate["integrated_lorenz"], 16),
        "min_cumulative_delta": display(estimate["min_cumulative_delta"], 16),
        "max_cumulative_delta": display(estimate["max_cumulative_delta"], 16),
        "majorization": estimate["majorization"],
        "path_majorization_consensus": classifications,
        "strict_profile_separation": True,
        "scale_invariant_readout": True,
        "finite_numerical_guard": display(NUMERICAL_GUARD, 16),
    }


def build_payload() -> dict[str, Any]:
    need(PARENT_CERT.is_file() and digest(PARENT_CERT.read_bytes()) ==
         PARENT_CERT_SHA256, "TPC-320 parent certificate lock")
    rows: list[dict[str, Any]] = []
    cache: dict[tuple[int, int, int], dict[str, np.ndarray]] = {}
    for scale in SCALES:
        for q0 in Q_ANCHORS:
            for exponent in EXPONENTS:
                row, profiles = build_row(scale, q0, exponent)
                rows.append(row)
                cache[(scale, q0, exponent)] = profiles
    need(len(rows) == 24 and len(cache) == 24, "row census")

    comparisons = []
    for scale in SCALES:
        for exponent in EXPONENTS:
            for lower_q, upper_q in zip(Q_ANCHORS, Q_ANCHORS[1:]):
                comparisons.append(build_comparison(
                    cache[(scale, lower_q, exponent)],
                    cache[(scale, upper_q, exponent)], scale, lower_q,
                    exponent))
    need(len(comparisons) == 18, "comparison census")

    tv_lows = [float(item["tv_interval"][0]) for item in comparisons]
    ks_lows = [float(item["lorenz_ks_interval"][0]) for item in comparisons]
    integrated = [float(item["integrated_lorenz_estimate"])
                  for item in comparisons]
    classes = [item["majorization"] for item in comparisons]
    class_counts = {name: classes.count(name)
                    for name in ("P_MAJORIZES_Q", "Q_MAJORIZES_P", "MIXED")}
    need(all(item["strict_profile_separation"] for item in comparisons) and
         min(tv_lows) > TV_THRESHOLD and min(ks_lows) > KS_THRESHOLD,
         "finite profile separation audit")
    need(class_counts == {"P_MAJORIZES_Q": 3, "Q_MAJORIZES_P": 2,
                          "MIXED": 13}, "majorization census")

    exact_trace, exact_trace2, rayleigh = exact_small_audit()
    return {
        "schema": SCHEMA,
        "parent_lock": {
            "project": "TPC-320 scale-invariant spectral concentration",
            "certificate_sha256": PARENT_CERT_SHA256,
        },
        "protocol": {
            "source_scales": list(SCALES),
            "height": HEIGHT,
            "Q_anchors": list(Q_ANCHORS),
            "kernel_exponents": list(EXPONENTS),
            "domain": "ell^2(I_X)",
            "codomain": "ell^2(S_Q x I_X)",
            "profile": "p_j=lambda_j/tr(G), descending",
            "comparison_axis": "adjacent Q shells at fixed X and exponent",
            "profile_paths": list(PROFILE_PATHS),
            "distance_thresholds": {
                "tv_lower": TV_THRESHOLD,
                "lorenz_ks_lower": KS_THRESHOLD,
            },
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
            "adjacent_Q_pairs": len(Q_ANCHORS) - 1,
            "comparisons": len(comparisons),
            "profile_separation_strict": len(comparisons),
            "tv_lower_threshold": display(TV_THRESHOLD, 16),
            "lorenz_ks_lower_threshold": display(KS_THRESHOLD, 16),
            "tv_lower_min": display(min(tv_lows), 16),
            "lorenz_ks_lower_min": display(min(ks_lows), 16),
            "integrated_lorenz_min": display(min(integrated), 16),
            "integrated_lorenz_max": display(max(integrated), 16),
            "majorization_counts": class_counts,
            "uniform_shell_profile": "REFUTED_FINITE_PANEL",
            "uniform_majorization_direction": "REFUTED_FINITE_PANEL",
            "fixed_power_credit": 0,
        },
        "claim_firewall": {
            "TPC321_PROFILE_SEPARATION":
                "NUMERICALLY_CERTIFIED_FINITE_18_OF_18",
            "TPC321_TV_SEPARATION":
                "NUMERICALLY_CERTIFIED_FINITE_ALL_GT_0_03",
            "TPC321_LORENZ_KS_SEPARATION":
                "NUMERICALLY_CERTIFIED_FINITE_ALL_GT_0_02",
            "TPC321_MAJORISATION_PATTERN":
                "NUMERICAL_OBSERVATION_3_FORWARD_2_REVERSE_13_MIXED",
            "TPC321_UNIFORM_SHELL_PROFILE": "REFUTED_FINITE_PANEL",
            "TPC321_UNIFORM_MAJORISATION": "REFUTED_FINITE_PANEL",
            "TPC321_ARITHMETIC_ADVANCE": "NO",
            "TPC321_FIXED_POWER_CREDIT": 0,
            "TPC321_FULL_GATE_B": "OPEN",
            "TPC321_TWIN_PRIME_RESULT": "NONE",
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
    print("TPC321_CERTIFICATE=PASS rows=24 comparisons=18 "
          "profile_separation=18 tv_gt_003=18 ks_gt_002=18 "
          "majorization=3/2/13")


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
            print("TPC321_CERTIFICATE=WRITTEN")
        else:
            check_certificate()
    except (CheckFailure, OSError, json.JSONDecodeError, ValueError,
            np.linalg.LinAlgError) as error:
        print("TPC321_CERTIFICATE=FAIL " + str(error), file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
