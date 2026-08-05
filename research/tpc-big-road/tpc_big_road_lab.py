#!/usr/bin/env python3
"""Read-only exact/stress lab for the TPC big-road deletion cocycle.

The program writes JSON only to stdout.  It never mutates repository artifacts.
"""

from __future__ import annotations

import argparse
import json
import math
from fractions import Fraction
from typing import Iterable


def primes_up_to(limit: int) -> list[int]:
    if limit < 2:
        return []
    sieve = bytearray(b"\x01") * (limit + 1)
    sieve[0:2] = b"\x00\x00"
    for p in range(2, math.isqrt(limit) + 1):
        if sieve[p]:
            start = p * p
            sieve[start : limit + 1 : p] = b"\x00" * (
                (limit - start) // p + 1
            )
    return [n for n in range(2, limit + 1) if sieve[n]]


def primality_table(limit: int) -> bytearray:
    if limit < 1:
        return bytearray(limit + 1)
    sieve = bytearray(b"\x01") * (limit + 1)
    sieve[0] = 0
    if limit >= 1:
        sieve[1] = 0
    for p in range(2, math.isqrt(limit) + 1):
        if sieve[p]:
            start = p * p
            sieve[start : limit + 1 : p] = b"\x00" * (
                (limit - start) // p + 1
            )
    return sieve


def fraction_text(value: Fraction) -> str:
    return f"{value.numerator}/{value.denominator}"


def deletion_positions(lo: int, hi: int, p: int, residues: Iterable[int]) -> Iterable[int]:
    for residue in residues:
        first = lo + ((residue - lo) % p)
        for n in range(first, hi + 1, p):
            yield n - lo


def stage_profile(
    x_value: int,
    shift: int = 2,
    keep_stages: int = 12,
    include_exact_fraction: bool = False,
) -> dict[str, object]:
    if x_value < 4:
        raise ValueError("x must be at least 4")
    if shift <= 0:
        raise ValueError("shift must be positive")

    lo = x_value + 1
    hi = 2 * x_value
    length = hi - lo + 1
    cutoff = math.isqrt(hi + shift)
    primes = primes_up_to(cutoff)
    survivors = bytearray(b"\x01") * length

    count = length
    haar_mass = Fraction(1, 1)
    ratio: Fraction | None = Fraction(1, 1)
    telescope = Fraction(1, 1)
    telescope_applicable = True
    stages: list[dict[str, object]] = []

    for p in primes:
        residues = sorted({0, (-shift) % p})
        local_rank = len(residues)
        before = count
        deleted = 0
        for index in deletion_positions(lo, hi, p, residues):
            if survivors[index]:
                survivors[index] = 0
                deleted += 1

        count = before - deleted
        innovation = Fraction(deleted, 1) - Fraction(local_rank * before, p)
        next_mass = haar_mass * Fraction(p - local_rank, p)
        if count != before - deleted:
            raise AssertionError("stage deletion identity failed")

        if next_mass == 0:
            if count != 0:
                raise AssertionError("zero Haar mass must delete the entire interval")
            contribution: Fraction | None = None
            next_ratio: Fraction | None = None
            telescope_applicable = False
        else:
            if ratio is None:
                raise AssertionError("positive mass cannot follow a zero-mass stage")
            next_ratio = Fraction(count, 1) / (next_mass * length)
            contribution = -innovation / (next_mass * length)
            if next_ratio != ratio + contribution:
                raise AssertionError("normalized telescope step failed")

        if contribution is not None:
            telescope += contribution
        ratio = next_ratio
        haar_mass = next_mass
        stages.append(
            {
                "prime": p,
                "local_rank": local_rank,
                "before": before,
                "deleted": deleted,
                "after": count,
                "innovation": fraction_text(innovation),
                "ratio_contribution": None if contribution is None else float(contribution),
            }
        )
        if next_mass == 0:
            break

    if telescope_applicable and telescope != ratio:
        raise AssertionError("global normalized telescope failed")

    prime = primality_table(hi + shift)
    exact_pair_count = sum(1 for n in range(lo, hi + 1) if prime[n] and prime[n + shift])
    identity_ok = count == exact_pair_count

    ranked = sorted(
        (row for row in stages if row["ratio_contribution"] is not None),
        key=lambda row: abs(float(row["ratio_contribution"])),
        reverse=True,
    )
    euler_gamma = 0.5772156649015328606
    endpoint_heuristic = math.exp(2.0 * euler_gamma) / 4.0
    payload: dict[str, object] = {
        "X": x_value,
        "shift": shift,
        "interval": [lo, hi],
        "cutoff": cutoff,
        "prime_stages": len(primes),
        "survivor_count": count,
        "prime_pair_count": exact_pair_count,
        "primality_identity": identity_ok,
        "haar_mass_float": float(haar_mass),
        "haar_mass_fraction_digits": {
            "numerator": len(str(haar_mass.numerator)),
            "denominator": len(str(haar_mass.denominator)),
        },
        "haar_main": float(haar_mass * length),
        "physical_to_haar_ratio": None if ratio is None else float(ratio),
        "endpoint_heuristic_e2gamma_over_4": endpoint_heuristic,
        "telescope_exact": (not telescope_applicable) or telescope == ratio,
        "normalized_telescope_applicable": telescope_applicable,
        "largest_stage_contributions": ranked[:keep_stages],
    }
    if include_exact_fraction:
        payload["haar_mass_exact"] = fraction_text(haar_mass)
    return payload


def run_checks() -> dict[str, object]:
    cases: list[dict[str, object]] = []
    for shift in (1, 2, 4, 6):
        for x_value in (40, 100, 1000, 10_000):
            result = stage_profile(x_value, shift, keep_stages=0)
            if not result["primality_identity"]:
                raise AssertionError(f"primality identity failed for X={x_value}, h={shift}")
            if not result["telescope_exact"]:
                raise AssertionError(f"telescope failed for X={x_value}, h={shift}")
            cases.append(
                {
                    "X": x_value,
                    "shift": shift,
                    "count": result["survivor_count"],
                    "ratio": result["physical_to_haar_ratio"],
                }
            )

    odd_control = stage_profile(1000, 1, keep_stages=0)
    if odd_control["survivor_count"] != 0:
        raise AssertionError("odd-shift parity control should have no pairs in this interval")

    return {
        "status": "PASS",
        "checks": [
            "exact stage deletion",
            "exact normalized innovation telescope",
            "critical-cutoff survivor/primality identity",
            "local-rank handling for p dividing the shift",
            "odd-shift parity control",
        ],
        "case_count": len(cases),
        "cases": cases,
    }


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    mode = parser.add_mutually_exclusive_group()
    mode.add_argument("--check", action="store_true", help="run exact self-checks (default)")
    mode.add_argument("--stress", action="store_true", help="print finite-scale stage profiles")
    parser.add_argument("--x", type=int, nargs="+", default=[10_000, 100_000, 1_000_000])
    parser.add_argument("--shift", type=int, default=2)
    parser.add_argument("--keep-stages", type=int, default=12)
    parser.add_argument(
        "--exact-fractions",
        action="store_true",
        help="include potentially very long exact Haar fractions in stress output",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    if args.stress:
        payload = {
            "status": "FINITE_DIAGNOSTIC_NOT_THEOREM",
            "profiles": [
                stage_profile(x, args.shift, args.keep_stages, args.exact_fractions)
                for x in args.x
            ],
        }
    else:
        payload = run_checks()
    print(json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
