#!/usr/bin/env python3
"""Deterministic exact stress families for the TPC-256 bookkeeping."""

from __future__ import annotations

import argparse
import sys
from fractions import Fraction


PRIMES = (3, 5, 7, 11, 13, 17, 19, 23, 29, 31)


def require(condition: bool, message: str) -> None:
    if not condition:
        raise RuntimeError(message)


def floor_fraction(value: Fraction) -> int:
    return value.numerator // value.denominator


def count_multiples(lo: int, hi: int, divisor: int) -> int:
    return hi // divisor - (lo - 1) // divisor


def unit_value(prime: int, t: int, u: int) -> Fraction:
    if u % prime == 0:
        return Fraction(0, 1)
    return Fraction(int(u % prime == t % prime), 1) - Fraction(1, prime - 1)


def clocks() -> list[tuple[Fraction, str]]:
    values: list[tuple[Fraction, str]] = []
    for index in range(96):
        values.append((Fraction(512 + 7 * index, 1), "integer"))
    for index in range(96):
        numerator = 4097 + 28 * index + 2 * (index % 6)
        values.append((Fraction(numerator, 8), "noninteger"))
    return values


def run_stress() -> dict[str, int]:
    families = clocks()
    integer = 0
    noninteger = 0
    rank_identities = 0
    divisor_layers = 0
    unit_periods = 0
    unit_mask_terms = 0
    hard_boundary_checks = 0
    child_boundary_checks = 0
    separate_zero_modes = 0

    for family_index, (clock, kind) in enumerate(families):
        integer += int(kind == "integer")
        noninteger += int(kind == "noninteger")
        require((clock.denominator == 1) == (kind == "integer"), "clock classification failed")

        a = floor_fraction(clock / 2)
        b = floor_fraction(clock)
        n = b - a
        ell = n // 2
        right = n - ell
        midpoint = a + ell
        require(ell > 0 and right > 0, "empty rank child")
        rho_squared = Fraction(ell * right, n)
        require(rho_squared * (Fraction(1, ell) + Fraction(1, right)) == 1, "Haar normalization")
        require(rho_squared / (ell * ell) <= 1 / rho_squared, "left Haar height")
        require(rho_squared / (right * right) <= 1 / rho_squared, "right Haar height")
        require((Fraction(1, ell) + Fraction(1, right)) ** 2 * rho_squared == 1 / rho_squared, "jump height")
        rank_identities += 1

        for divisor in range(1, 33):
            left_count = count_multiples(a + 1, midpoint, divisor)
            right_count = count_multiples(midpoint + 1, b, divisor)
            left_error = Fraction(left_count, 1) - Fraction(ell, divisor)
            right_error = Fraction(right_count, 1) - Fraction(right, divisor)
            require(abs(left_error) <= 1, "left divisor discrepancy")
            require(abs(right_error) <= 1, "right divisor discrepancy")
            contrast = Fraction(left_count, ell) - Fraction(right_count, right)
            require(abs(contrast) <= Fraction(1, ell) + Fraction(1, right), "layerwise cancellation")
            divisor_layers += 1

        prime = PRIMES[family_index % len(PRIMES)]
        t = a + 1
        while t % prime == 0:
            t += 1
        require(t <= b, "input-unit fixture missing")

        c_sum = Fraction(0, 1)
        d_sum = Fraction(0, 1)
        v_sum = Fraction(0, 1)
        for u in range(prime):
            c_value = Fraction(int(u % prime == t % prime), 1) - Fraction(1, prime - 1)
            d_value = Fraction(int(u % prime == 0), prime - 1)
            v_value = unit_value(prime, t, u)
            require(c_value + d_value == v_value, "output-unit recombination")
            c_sum += c_value
            d_sum += d_value
            v_sum += v_value
        require(c_sum == -Fraction(1, prime - 1), "centered-bracket zero mode")
        require(d_sum == Fraction(1, prime - 1), "output-unit zero mode")
        require(v_sum == 0, "combined unit row mean")
        separate_zero_modes += 2
        unit_periods += 1

        for h in range(-4 * prime, 4 * prime + 1):
            value = unit_value(prime, t, t + h)
            pointwise_bound = Fraction(int(h % prime == 0), 1) + Fraction(2, prime)
            require(abs(value) <= pointwise_bound, "combined unit-mask majorant")
            unit_mask_terms += 1

        for h in range(-80, 81):
            hard_count = 0
            jump_count = 0
            for source in range(a + 1, b + 1):
                target = source + h
                hard_count += int(not (a < target <= b))
                jump_count += int(
                    a < target <= b
                    and ((source <= midpoint) != (target <= midpoint))
                )
            require(hard_count <= abs(h), "hard-window cardinality")
            require(jump_count <= abs(h), "child-jump cardinality")
            hard_boundary_checks += 1
            child_boundary_checks += 1

    require(len(families) == 192, "family count")
    require(integer == 96 and noninteger == 96, "clock split")
    require(Fraction(2, 3) + Fraction(1, 2) == Fraction(56, 48), "main exponent")
    require(Fraction(1, 3) + 2 * Fraction(21, 32) - Fraction(1, 2) == Fraction(55, 48), "boundary exponent")
    require(Fraction(56, 48) - Fraction(55, 48) == Fraction(1, 48), "boundary gap")
    require(Fraction(133, 400) - Fraction(1, 2) == Fraction(-67, 400), "divisor exponent")

    return {
        "child_boundary_checks": child_boundary_checks,
        "divisor_layers": divisor_layers,
        "families": len(families),
        "hard_boundary_checks": hard_boundary_checks,
        "integer": integer,
        "noninteger": noninteger,
        "rank_identities": rank_identities,
        "separate_zero_modes": separate_zero_modes,
        "unit_mask_terms": unit_mask_terms,
        "unit_periods": unit_periods,
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()
    require(args.check, "--check is required")
    counts = run_stress()
    print(
        "TPC256_STRESS=PASS "
        f"families={counts['families']} integer={counts['integer']} "
        f"noninteger={counts['noninteger']} rank_identities={counts['rank_identities']} "
        f"divisor_layers={counts['divisor_layers']} unit_mask_terms={counts['unit_mask_terms']} "
        f"hard_boundary_checks={counts['hard_boundary_checks']} "
        f"child_boundary_checks={counts['child_boundary_checks']}"
    )
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except Exception as exc:
        print(f"TPC256_STRESS=FAIL {exc}", file=sys.stderr)
        raise SystemExit(1)
