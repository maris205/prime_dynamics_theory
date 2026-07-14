#!/usr/bin/env python3
"""Finite sharp-box diagnostic for the TPC-9 zero-Mellin identities.

This standard-library script is intentionally separate from the exact
certificate.  It uses floating logarithms and a nonsmooth box, so it is not
a verification of the analytic asymptotic theorem.
"""

from __future__ import annotations

import argparse
import json
import math
from pathlib import Path
from typing import List


APERY = 1.2020569031595942854
C2 = 52.5 * APERY / (math.pi**4)


def prime_list(limit: int) -> List[int]:
    sieve = bytearray(b"\x01") * (limit + 1)
    if limit >= 0:
        sieve[0] = 0
    if limit >= 1:
        sieve[1] = 0
    for p in range(2, math.isqrt(limit) + 1):
        if sieve[p]:
            sieve[p * p : limit + 1 : p] = b"\x00" * (((limit - p * p) // p) + 1)
    return [p for p in range(2, limit + 1) if sieve[p]]


def von_mangoldt_array(limit: int, primes: List[int]) -> List[float]:
    values = [0.0] * (limit + 1)
    for p in primes:
        power = p
        logp = math.log(p)
        while power <= limit:
            values[power] = logp
            if power > limit // p:
                break
            power *= p
    return values


def tau_array(limit: int) -> List[int]:
    values = [0] * (limit + 1)
    for d in range(1, limit + 1):
        for multiple in range(d, limit + 1, d):
            values[multiple] += 1
    return values


def small_coefficient(r0: int, r1: int, cutoff: int, mangoldt: List[float]) -> List[float]:
    values = [0.0] * (r1 - r0 + 1)
    for n in range(1, cutoff + 1):
        coefficient = mangoldt[n] - 1.0
        first = ((r0 + n - 1) // n) * n
        for r in range(first, r1 + 1, n):
            values[r - r0] += coefficient
    return values


def evaluate_scale(x: int, h: int, mangoldt: List[float], tau: List[int]) -> dict:
    r0, r1 = x + 1, 2 * x
    cutoff = math.isqrt(x)
    small = small_coefficient(r0, r1, cutoff, mangoldt)
    complete = 0.0
    small_sum = 0.0
    target_mass = 0.0
    for r in range(r0, r1 + 1):
        target = r + h
        target_lambda = mangoldt[target] if 0 <= target < len(mangoldt) else 0.0
        complete += (math.log(r) - tau[r]) * target_lambda
        small_sum += small[r - r0] * target_lambda
        target_mass += target_lambda
    large = complete - small_sum
    scale = x * math.log(x)
    return {
        "X": x,
        "D": cutoff,
        "complete_over_XlogX": complete / scale,
        "large_over_XlogX": large / scale,
        "small_over_XlogX": small_sum / scale,
        "target_mass_over_X": target_mass / x,
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--powers", default="14,16,18")
    parser.add_argument("--h", type=int, default=2)
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    powers = [int(value) for value in args.powers.split(",") if value]
    scales = [2**power for power in powers]
    limit = 2 * max(scales) + abs(args.h) + 10
    primes = prime_list(limit)
    mangoldt = von_mangoldt_array(limit, primes)
    tau = tau_array(2 * max(scales))
    payload = {
        "schema": "tpc9-zero-mellin-floating-diagnostic-v1",
        "sharp_box": "X < r <= 2X",
        "h": args.h,
        "C2": C2 if args.h == 2 else None,
        "predicted_complete_leading_ratio_for_h2": 1.0 - C2 if args.h == 2 else None,
        "predicted_sqrt_tail_leading_ratio_for_h2": 0.5 * (1.0 - C2)
        if args.h == 2
        else None,
        "cutoff_outside_proved_logarithmic_range": True,
        "leading_ratios_are_formal_asymptotic_comparisons": True,
        "rows": [evaluate_scale(x, args.h, mangoldt, tau) for x in scales],
        "scope": "Finite nonsmooth floating diagnostic; not a theorem verification.",
    }
    text = json.dumps(payload, indent=2, sort_keys=True) + "\n"
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(text, encoding="utf-8", newline="\n")
    else:
        print(text, end="")


if __name__ == "__main__":
    main()
