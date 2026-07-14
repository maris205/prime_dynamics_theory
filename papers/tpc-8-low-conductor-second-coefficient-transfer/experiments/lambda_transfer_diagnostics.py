#!/usr/bin/env python3
"""Optional floating diagnostics for the TPC-8 transfer theorem.

This script is deliberately separate from ``exact_transfer_certificate.py``.
It uses NumPy and floating logarithms to inspect finite von Mangoldt rows; its
output is not an exact certificate and does not verify the non-explicit
logarithmic range in Bombieri--Vinogradov.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import math
from fractions import Fraction
from pathlib import Path
from typing import Iterable, Mapping

import numpy as np

from exact_transfer_certificate import (
    canonical_hash,
    euler_phi,
    quadratic_mode,
    squarefree_divisors,
    squarefree_primes,
    transfer_residue_sum,
    units,
)


def von_mangoldt_array(limit: int) -> tuple[np.ndarray, np.ndarray]:
    if limit < 2:
        raise ValueError("the sieve limit must be at least two")
    is_prime = np.ones(limit + 1, dtype=np.bool_)
    is_prime[:2] = False
    for prime in range(2, math.isqrt(limit) + 1):
        if is_prime[prime]:
            is_prime[prime * prime : limit + 1 : prime] = False
    primes = np.flatnonzero(is_prime).astype(np.int64)
    values = np.zeros(limit + 1, dtype=np.float64)
    for prime64 in primes:
        prime = int(prime64)
        power = prime
        log_prime = math.log(prime)
        while power <= limit:
            values[power] = log_prime
            if power > limit // prime:
                break
            power *= prime
    return values, primes


def first_progression_value(lower_exclusive: int, residue: int, modulus: int) -> int:
    first_allowed = lower_exclusive + 1
    return first_allowed + (residue - first_allowed) % modulus


def direct_lambda_row(
    m: int,
    n_values: np.ndarray,
    h: int,
    beta_values: np.ndarray,
    von_mangoldt: np.ndarray,
) -> float:
    return float(np.dot(beta_values, von_mangoldt[m * n_values + h]))


def progression_lambda_row(
    m: int,
    n_scale: int,
    modulus: int,
    h: int,
    beta: Mapping[int, int],
    von_mangoldt: np.ndarray,
) -> float:
    lower = m * n_scale + h
    upper = 2 * m * n_scale + h
    progression_modulus = m * modulus
    total = 0.0
    for residue, coefficient in beta.items():
        target_residue = (m * residue + h) % progression_modulus
        first = first_progression_value(lower, target_residue, progression_modulus)
        targets = np.arange(first, upper + 1, progression_modulus, dtype=np.int64)
        total += coefficient * float(np.sum(von_mangoldt[targets]))
    return total


def fraction_record(value: Fraction) -> dict[str, int]:
    return {"numerator": value.numerator, "denominator": value.denominator}


def run_diagnostics(
    m_scale: int,
    n_scale: int,
    modulus: int,
    h: int,
    conductors: Iterable[int],
) -> dict[str, object]:
    if m_scale < 2 or n_scale < 100:
        raise ValueError("use M>=2 and N>=100")
    if modulus % 2 == 0 or math.gcd(modulus, h) != 1:
        raise ValueError("use an odd squarefree modulus coprime to h")
    if (m_scale + 1) * (n_scale + 1) + h < 1:
        raise ValueError("the selected scales and shift must keep every target positive")
    primes_q = squarefree_primes(modulus)
    valid_conductors = set(squarefree_divisors(primes_q))
    conductors = tuple(int(value) for value in conductors)
    if any(value not in valid_conductors for value in conductors):
        raise ValueError("each mode conductor must be a squarefree divisor of q")

    x = m_scale * n_scale
    limit = 4 * x + abs(h) + 2
    von_mangoldt, primes = von_mangoldt_array(limit)
    n_values = np.arange(n_scale + 1, 2 * n_scale + 1, dtype=np.int64)
    m_values = [
        m
        for m in range(m_scale + 1, 2 * m_scale + 1)
        if math.gcd(m, modulus * h) == 1
    ]
    if not m_values:
        raise ValueError("the selected M interval contains no eligible rows")

    mode_records = []
    maximum_crosscheck_error = 0.0
    for conductor in conductors:
        beta = quadratic_mode(modulus, conductor)
        lookup = np.zeros(modulus, dtype=np.float64)
        for residue, coefficient in beta.items():
            lookup[residue] = coefficient
        beta_values = lookup[n_values % modulus]

        actual_rows = []
        main_rows = []
        row_errors = []
        crosscheck_errors = []
        exact_main_records = []
        for m in m_values:
            direct = direct_lambda_row(
                m, n_values, h, beta_values, von_mangoldt
            )
            progression = progression_lambda_row(
                m, n_scale, modulus, h, beta, von_mangoldt
            )
            crosscheck = abs(direct - progression)
            maximum_crosscheck_error = max(maximum_crosscheck_error, crosscheck)
            residue_sum = transfer_residue_sum(beta, m, modulus, h)
            exact_main = Fraction(
                m * n_scale * residue_sum, euler_phi(m * modulus)
            )
            main = float(exact_main)
            actual_rows.append(direct)
            main_rows.append(main)
            row_errors.append(direct - main)
            crosscheck_errors.append(crosscheck)
            exact_main_records.append(fraction_record(exact_main))

        errors = np.asarray(row_errors, dtype=np.float64)
        normalized_lambda_m_weight = np.asarray(
            [von_mangoldt[m] / math.log(2 * m_scale) for m in m_values]
        )
        mode_records.append(
            {
                "exact_conductor": conductor,
                "eligible_rows": len(m_values),
                "l1_row_error_over_X": float(np.sum(np.abs(errors)) / x),
                "rms_row_error_over_N": float(
                    np.sqrt(np.mean(errors**2)) / n_scale
                ),
                "max_row_error_over_N": float(np.max(np.abs(errors)) / n_scale),
                "signed_row_error_over_X": float(np.sum(errors) / x),
                "lambda_M_weighted_error_over_X": float(
                    np.dot(normalized_lambda_m_weight, errors) / x
                ),
                "total_abs_main_over_X": float(
                    np.sum(np.abs(main_rows)) / x
                ),
                "max_direct_AP_crosscheck_error": float(max(crosscheck_errors)),
                "exact_main_rows_sha256": hashlib.sha256(
                    json.dumps(
                        exact_main_records, sort_keys=True, separators=(",", ":")
                    ).encode("utf-8")
                ).hexdigest().upper(),
            }
        )

    payload: dict[str, object] = {
        "schema": "tpc8-floating-lambda-transfer-diagnostic-v1",
        "parameters": {
            "M": m_scale,
            "N": n_scale,
            "X_equals_MN": x,
            "q": modulus,
            "q_primes": list(primes_q),
            "h": h,
            "conductors": list(conductors),
            "target_sieve_limit": limit,
            "eligible_rows": len(m_values),
            "raw_level_ratio_2Mq_over_sqrt_X": float(
                2 * m_scale * modulus / math.sqrt(x)
            ),
        },
        "array_checks": {
            "prime_count_to_limit": int(len(primes)),
            "lambda_2": float(von_mangoldt[2]),
            "lambda_4": float(von_mangoldt[4]),
            "lambda_6": float(von_mangoldt[6]),
        },
        "modes": mode_records,
        "max_direct_AP_crosscheck_error": maximum_crosscheck_error,
        "interpretation_boundary": (
            "This NumPy calculation uses floating logarithms. It is a finite "
            "indexing and scale diagnostic only; it does not instantiate the "
            "non-explicit logarithmic Bombieri--Vinogradov cutoff or prove an "
            "asymptotic estimate."
        ),
    }
    return {**payload, "canonical_payload_sha256": canonical_hash(payload)}


def render_diagnostic(payload: Mapping[str, object]) -> bytes:
    return (json.dumps(payload, indent=2, sort_keys=True) + "\n").encode("utf-8")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--m", type=int, default=32)
    parser.add_argument("--n", type=int, default=524_288)
    parser.add_argument("--q", type=int, default=35)
    parser.add_argument("--h", type=int, default=2)
    parser.add_argument("--conductors", default="1,5,7,35")
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    conductors = [int(value) for value in args.conductors.split(",")]
    payload = run_diagnostics(args.m, args.n, args.q, args.h, conductors)
    rendered = render_diagnostic(payload)
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_bytes(rendered)
    else:
        print(rendered.decode("utf-8"), end="")


if __name__ == "__main__":
    main()
