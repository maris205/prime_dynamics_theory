#!/usr/bin/env python3
"""Finite-scale diagnostics for the TPC-7 defect and periodic energy.

The computations are exploratory.  They verify exact finite identities up to
floating-point roundoff and record shift quantiles for several artificial
power cutoffs D=X^theta.  They do not implement the unspecified, non-optimized
logarithmic constant in the Bombieri--Vinogradov cutoff.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import math
from pathlib import Path
from typing import Iterable

import numpy as np


def arithmetic_arrays(limit: int) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    """Return mu, Lambda, and the primes up to limit."""
    if limit < 2:
        raise ValueError("limit must be at least 2")

    is_prime = np.ones(limit + 1, dtype=np.bool_)
    is_prime[:2] = False
    for p in range(2, math.isqrt(limit) + 1):
        if is_prime[p]:
            is_prime[p * p : limit + 1 : p] = False
    primes = np.flatnonzero(is_prime).astype(np.int64)

    mu = np.ones(limit + 1, dtype=np.int8)
    mu[0] = 0
    for p64 in primes:
        p = int(p64)
        mu[p : limit + 1 : p] *= -1
        square = p * p
        if square <= limit:
            mu[square : limit + 1 : square] = 0

    von_mangoldt = np.zeros(limit + 1, dtype=np.float64)
    for p64 in primes:
        p = int(p64)
        log_p = math.log(p)
        power = p
        while power <= limit:
            von_mangoldt[power] = log_p
            if power > limit // p:
                break
            power *= p

    return mu, von_mangoldt, primes


def truncated_source_weight(
    mu: np.ndarray, x: int, cutoff: int, total_length: int
) -> np.ndarray:
    """Compute a_D(n) on X<n<=2X and zero-extend to total_length."""
    if cutoff < 1 or cutoff >= len(mu):
        raise ValueError("cutoff outside the Mobius array")
    result = np.zeros(total_length, dtype=np.float64)
    lower = x + 1
    upper = 2 * x
    for d in range(2, cutoff + 1):
        mu_d = int(mu[d])
        if mu_d == 0:
            continue
        start = ((lower + d - 1) // d) * d
        result[start : upper + 1 : d] += -mu_d * math.log(d)
    return result


def next_power_of_two(value: int) -> int:
    return 1 << (value - 1).bit_length()


def all_shift_correlations(
    source: np.ndarray, target: np.ndarray, max_shift: int
) -> np.ndarray:
    """Return sum_n source[n] target[n+h] for 1<=h<=max_shift."""
    if source.shape != target.shape:
        raise ValueError("source and target must have the same shape")
    length = len(source)
    nfft = next_power_of_two(2 * length - 1)
    source_reversed = source[::-1]
    transform = np.fft.rfft(target, nfft) * np.fft.rfft(source_reversed, nfft)
    convolution = np.fft.irfft(transform, nfft)
    indices = length - 1 + np.arange(1, max_shift + 1)
    return convolution[indices]


def quantile_summary(values: np.ndarray, x: int) -> dict[str, float]:
    normalized = np.abs(values) / float(x)
    return {
        "count": int(len(values)),
        "median_abs_over_X": float(np.quantile(normalized, 0.50)),
        "q90_abs_over_X": float(np.quantile(normalized, 0.90)),
        "q99_abs_over_X": float(np.quantile(normalized, 0.99)),
        "max_abs_over_X": float(np.max(normalized)),
        "rms_over_X": float(np.sqrt(np.mean(normalized**2))),
        "fraction_abs_over_0.05X": float(np.mean(normalized > 0.05)),
    }


def euler_phi(value: int) -> int:
    result = value
    n = value
    p = 2
    while p * p <= n:
        if n % p == 0:
            while n % p == 0:
                n //= p
            result -= result // p
        p += 1 if p == 2 else 2
    if n > 1:
        result -= result // n
    return result


def periodic_projection_energy(values: np.ndarray, start: int, q: int) -> float:
    indices = np.arange(start, start + len(values), dtype=np.int64)
    residues = indices % q
    counts = np.bincount(residues, minlength=q).astype(np.float64)
    sums = np.bincount(residues, weights=values, minlength=q)
    nonempty = counts > 0
    return float(np.sum((sums[nonempty] ** 2) / counts[nonempty]))


def direct_correlation(source: np.ndarray, target: np.ndarray, shift: int) -> float:
    return float(np.dot(source[:-shift], target[shift:]))


def run_diagnostics(
    x: int,
    max_shift: int,
    cutoff_exponents: Iterable[float],
    moduli: Iterable[int],
) -> dict:
    if x < 100 or max_shift < 2:
        raise ValueError("use x>=100 and max_shift>=2")
    cutoff_exponents = tuple(float(theta) for theta in cutoff_exponents)
    moduli = tuple(int(q) for q in moduli)
    total_length = 2 * x + max_shift + 2
    mu, von_mangoldt, primes = arithmetic_arrays(total_length - 1)

    source_lambda = np.zeros(total_length, dtype=np.float64)
    source_lambda[x + 1 : 2 * x + 1] = von_mangoldt[x + 1 : 2 * x + 1]
    full_corr = all_shift_correlations(source_lambda, von_mangoldt, max_shift)

    shift_records: list[dict] = []
    validation_shifts = sorted(
        h for h in {2, 3, 5, 11, max_shift // 2, max_shift} if 1 <= h <= max_shift
    )
    for theta in cutoff_exponents:
        cutoff = max(2, min(2 * x, int(round(x**theta))))
        short_weight = truncated_source_weight(mu, x, cutoff, total_length)
        defect = source_lambda - short_weight
        tail_corr = all_shift_correlations(defect, von_mangoldt, max_shift)
        short_corr = all_shift_correlations(short_weight, von_mangoldt, max_shift)

        identity_error = float(np.max(np.abs(full_corr - short_corr - tail_corr)))
        direct_error = 0.0
        for h in validation_shifts:
            direct = direct_correlation(defect, von_mangoldt, h)
            direct_error = max(direct_error, abs(direct - tail_corr[h - 1]))

        shift_records.append(
            {
                "theta": float(theta),
                "D": int(cutoff),
                "all_shifts": quantile_summary(tail_corr, x),
                "even_shifts": quantile_summary(tail_corr[1::2], x),
                "odd_shifts": quantile_summary(tail_corr[0::2], x),
                "max_fft_split_identity_error": identity_error,
                "max_fft_direct_identity_error": float(direct_error),
            }
        )

    fluctuation = von_mangoldt[x + 1 : 2 * x + 1] - 1.0
    total_energy = float(np.dot(fluctuation, fluctuation))
    energy_records = []
    for q in moduli:
        if q < 1 or q > x:
            continue
        projected = periodic_projection_energy(fluctuation, x + 1, q)
        phi_q = euler_phi(q)
        energy_records.append(
            {
                "q": int(q),
                "phi_q": int(phi_q),
                "q_over_phi_q": float(q / phi_q),
                "projected_energy": projected,
                "total_energy": total_energy,
                "captured_ratio": float(projected / total_energy),
                "scaled_ratio_times_log_X": float(
                    projected / total_energy * math.log(x)
                ),
            }
        )

    scale_records = []
    for scale in sorted({max(100, x // 8), x // 4, x // 2, x}):
        scale_fluctuation = von_mangoldt[scale + 1 : 2 * scale + 1] - 1.0
        scale_total = float(np.dot(scale_fluctuation, scale_fluctuation))
        for q in moduli:
            if q < 1 or q > scale:
                continue
            projected = periodic_projection_energy(scale_fluctuation, scale + 1, q)
            scale_records.append(
                {
                    "N": int(scale),
                    "q": int(q),
                    "captured_ratio": float(projected / scale_total),
                }
            )

    payload = {
        "description": "TPC-7 finite-scale shift-defect and periodic-energy diagnostics",
        "parameters": {
            "X": int(x),
            "H": int(max_shift),
            "sigma": float(8 / 33),
            "H_over_X_to_sigma": float(max_shift / (x ** (8 / 33))),
            "cutoff_exponents": list(cutoff_exponents),
            "moduli": list(moduli),
        },
        "array_checks": {
            "prime_count_to_limit": int(len(primes)),
            "mu_1_to_10": [int(v) for v in mu[1:11]],
            "lambda_2": float(von_mangoldt[2]),
            "lambda_4": float(von_mangoldt[4]),
            "lambda_6": float(von_mangoldt[6]),
        },
        "shift_defect": shift_records,
        "periodic_energy": energy_records,
        "periodic_energy_by_scale": scale_records,
        "interpretation_boundary": (
            "Power cutoffs are finite-scale diagnostics, not a numerical "
            "realization of the theoretical cutoff X^(1/2)/log^B X; no "
            "asymptotic theorem is inferred from these values."
        ),
    }
    return payload


def canonical_hash(payload: dict) -> str:
    encoded = json.dumps(payload, sort_keys=True, separators=(",", ":")).encode()
    return hashlib.sha256(encoded).hexdigest().upper()


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--x", type=int, default=262_144)
    parser.add_argument("--max-shift", type=int, default=32_768)
    parser.add_argument("--cutoff-exponents", default="0.25,0.35,0.45")
    parser.add_argument("--moduli", default="2,6,30,210,2310")
    parser.add_argument(
        "--output", type=Path, default=Path("data/defect-shift-certificate.json")
    )
    args = parser.parse_args()

    exponents = [float(item) for item in args.cutoff_exponents.split(",")]
    moduli = [int(item) for item in args.moduli.split(",")]
    payload = run_diagnostics(args.x, args.max_shift, exponents, moduli)
    payload["canonical_payload_sha256"] = canonical_hash(payload)

    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n")
    print(json.dumps(payload, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
