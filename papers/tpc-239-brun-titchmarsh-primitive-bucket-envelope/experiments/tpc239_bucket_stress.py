#!/usr/bin/env python3
"""Finite stress tests for physical rows, AP censuses, and factor 16."""

from __future__ import annotations

import argparse
import json
import math
from fractions import Fraction
from math import gcd, isqrt
from typing import Any


class StressFailure(RuntimeError):
    """Fail-closed stress error."""


def demand(condition: bool, message: str) -> None:
    if type(condition) is not bool:
        raise StressFailure("stress condition is not a strict bool")
    if not condition:
        raise StressFailure(message)


def strict_int(value: object, name: str) -> int:
    demand(type(value) is int, f"{name} must be an exact int")
    return value


def primality(value: int) -> bool:
    strict_int(value, "prime candidate")
    if value < 2:
        return False
    for divisor in range(2, isqrt(value) + 1):
        if value % divisor == 0:
            return False
    return True


def totient(modulus: int) -> int:
    strict_int(modulus, "modulus")
    demand(modulus >= 1, "modulus must be positive")
    return sum(gcd(residue, modulus) == 1 for residue in range(modulus))


def shell(Q: int) -> list[int]:
    strict_int(Q, "Q")
    return [prime for prime in range(Q + 1, 2 * Q + 1) if primality(prime)]


def physical_matches(Q: int, H: int, h: int, a: int, primes: list[int]) -> list[int]:
    matched: list[int] = []
    for prime in primes:
        cutoff = (h * prime) // H
        multipliers = [value for value in range(-cutoff, cutoff + 1) if value]
        residues = [(value * pow(prime, -1, h)) % h for value in multipliers]
        demand(len(residues) == len(set(residues)), "row injectivity stress")
        if a in residues:
            matched.append(prime)
    return matched


def ap_rows(Q: int, H: int, h: int, a: int, primes: list[int]) -> list[dict[str, Any]]:
    maximum = (2 * h * Q) // H
    inverse = pow(a, -1, h)
    output: list[dict[str, Any]] = []
    for multiplier in range(-maximum, maximum + 1):
        if multiplier == 0 or gcd(multiplier, h) != 1:
            continue
        prime_class = (inverse * multiplier) % h
        demand(gcd(prime_class, h) == 1, "nonreduced stress class")
        row_primes = [prime for prime in primes if prime % h == prime_class]
        output.append(
            {
                "b": prime_class,
                "count": len(row_primes),
                "m": multiplier,
                "primes": row_primes,
            }
        )
    return output


def decimal(value: float) -> str:
    demand(type(value) is float and math.isfinite(value), "invalid stress real")
    return format(value, ".12f")


def stress_fixture(Q: int, H: int, h: int) -> dict[str, Any]:
    strict_int(Q, "Q")
    strict_int(H, "H")
    strict_int(h, "h")
    demand(Q >= 2, "Q too small")
    demand(4 * Q < H, "strict 4Q < H stress premise")
    demand(2 <= h < Q, "stress requires 2 <= h < Q")
    primes = shell(Q)
    demand(bool(primes), "stress shell is empty")
    phi = totient(h)
    logarithm = math.log(2.0 * Q / h)
    demand(logarithm > 0.0, "stress logarithm")
    class_rhs = 4.0 * Q / (phi * logarithm)
    factor_rhs = 16.0 * Q * Q / H * (h / phi) / logarithm
    maximum = (2 * h * Q) // H
    multipliers = [
        value
        for value in range(-maximum, maximum + 1)
        if value != 0 and gcd(value, h) == 1
    ]
    demand(len(multipliers) <= 2 * maximum, "stress multiplier count")
    demand(
        Fraction(2 * maximum, 1) <= Fraction(4 * h * Q, H),
        "stress 2M_h bound",
    )

    maximum_actual = 0
    maximum_census = 0
    minimum_factor_margin = math.inf
    strict_cutoff_buckets = 0
    active_buckets = 0
    total_actual_rows = 0
    total_ap_pairs = 0
    for residue in range(h):
        if gcd(residue, h) != 1:
            continue
        actual_primes = physical_matches(Q, H, h, residue, primes)
        rows = ap_rows(Q, H, h, residue, primes)
        census = sum(row["count"] for row in rows)
        for row in rows:
            demand(
                row["count"] <= class_rhs + 1.0e-12,
                "stress AP class exceeds real BT bound",
            )
        demand(len(actual_primes) <= census, "stress actual exceeds AP census")
        demand(census <= len(multipliers) * class_rhs + 1.0e-12, "row-sum stress")
        demand(census <= factor_rhs + 1.0e-12, "factor-16 stress")
        if len(actual_primes) < census:
            strict_cutoff_buckets += 1
        if actual_primes:
            active_buckets += 1
        maximum_actual = max(maximum_actual, len(actual_primes))
        maximum_census = max(maximum_census, census)
        minimum_factor_margin = min(minimum_factor_margin, factor_rhs - census)
        total_actual_rows += len(actual_primes)
        total_ap_pairs += census

    return {
        "H": H,
        "M_h": maximum,
        "Q": Q,
        "active_primitive_buckets": active_buckets,
        "ap_class_bt_rhs_approx": decimal(class_rhs),
        "factor_16_rhs_approx": decimal(factor_rhs),
        "h": h,
        "max_actual_R": maximum_actual,
        "max_ap_census": maximum_census,
        "minimum_factor_16_margin_approx": decimal(minimum_factor_margin),
        "phi_h": phi,
        "shell_prime_count": len(primes),
        "strict_dropped_cutoff_buckets": strict_cutoff_buckets,
        "total_actual_row_incidences": total_actual_rows,
        "total_ap_pairs": total_ap_pairs,
    }


def stress() -> dict[str, Any]:
    parameter_grid = [
        (11, 100, 7),
        (17, 220, 13),
        (29, 700, 23),
        (43, 1500, 35),
        (101, 8830, 82),
    ]
    fixtures = [stress_fixture(Q, H, h) for Q, H, h in parameter_grid]
    demand(any(row["strict_dropped_cutoff_buckets"] for row in fixtures), "no cutoff test")
    demand(max(row["max_actual_R"] for row in fixtures) == 3, "triple collision changed")

    h_one_primes = shell(101)
    h_one_cutoffs = [prime // 8830 for prime in h_one_primes]
    demand(2 * 101 < 8830, "h=1 premise")
    demand(all(cutoff == 0 for cutoff in h_one_cutoffs), "h=1 stress row")
    return {
        "TPC239_BUCKET_STRESS": "PASS",
        "classification": "NUMERICAL_FINITE_ILLUSTRATION_ONLY",
        "fixtures": fixtures,
        "h_one_empty_row_checked": True,
        "max_actual_R_across_grid": max(row["max_actual_R"] for row in fixtures),
        "max_ap_census_across_grid": max(row["max_ap_census"] for row in fixtures),
        "parameter_sets": len(fixtures),
        "primitive_buckets_checked": sum(row["phi_h"] for row in fixtures),
        "strict_dropped_cutoff_buckets": sum(
            row["strict_dropped_cutoff_buckets"] for row in fixtures
        ),
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--check", action="store_true", required=True)
    parser.parse_args()
    print(
        json.dumps(
            stress(),
            ensure_ascii=True,
            separators=(",", ":"),
            sort_keys=True,
        )
    )
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except StressFailure as error:
        raise SystemExit(f"TPC239_BUCKET_STRESS=FAIL: {error}")
