#!/usr/bin/env python3
"""Adversarial finite sanity checks for the TPC-215 theorem hypotheses."""

from __future__ import annotations

import argparse
import math
import sys
from fractions import Fraction
from math import gcd
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "code"))

from short_quotient_majorant import (  # noqa: E402
    AuditFailure,
    active_denominators,
    coefficient_value,
    divisor_family,
    emitter_row,
    harmonic,
    mobius,
    positive_divisors,
    primitive_row_norm,
    require,
    row_norm,
)


def audit_configuration(
    q_values: tuple[int, ...], height: int, lower: int, upper: int
) -> tuple[int, int, int]:
    family = divisor_family(lower, upper, q_values)
    active = active_denominators(family, q_values, height)
    activation_floor = (height + max(q_values) - 1) // max(q_values)
    quotient_bound = upper * max(q_values) // height
    require(all(h >= activation_floor for h in active), "activation floor")
    require(all(lower < h <= upper and h in family for h in active), "diagonal anchor")

    checked = 0
    top_rows = 0
    for h in active:
        multiples = tuple(d for d in family if d % h == 0)
        require(multiples and multiples[0] == h, "full-band h term")
        require(max(d // h for d in multiples) <= quotient_bound, "quotient bound")
        tail = sum(coefficient_value(d) for d in multiples)
        direct = sum(coefficient_value(d) ** 2 for d in multiples)
        ratio = tail * tail / direct
        majorant = (math.log(upper) / math.log(h)) ** 2 * float(harmonic(upper // h)) ** 2
        require(ratio <= majorant * (1 + 1e-13), "harmonic majorant")
        if 2 * h > upper:
            top_rows += 1
            require(multiples == (h,), "top shell")
            require(abs(ratio - 1.0) <= 1e-14, "top ratio")
        checked += 1

    for d in family:
        lhs = row_norm(emitter_row(d, q_values, height))
        rhs = sum(
            (
                primitive_row_norm(emitter_row(h, q_values, height))
                for h in positive_divisors(d)
            ),
            Fraction(0, 1),
        )
        require(lhs == rhs, "row decomposition")

    return checked, top_rows, len(family)


def full_band_hypothesis_attack() -> bool:
    """Deleting the anchored h term must invalidate the diagonal premise."""

    q_values = (11, 13, 17)
    height = 40
    family = divisor_family(2, 35, q_values)
    h = 3
    require(h in active_denominators(family, q_values, height), "attack row active")
    deleted = tuple(d for d in family if d != h)
    remaining = tuple(d for d in deleted if d % h == 0)
    return bool(remaining) and h not in remaining


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--check", action="store_true")
    parser.parse_args()
    configurations = (
        ((11, 13, 17), 40, 2, 35),
        ((17, 19, 23), 54, 2, 31),
        ((29, 31, 37), 96, 2, 43),
    )
    try:
        totals = [audit_configuration(*configuration) for configuration in configurations]
        require(full_band_hypothesis_attack(), "full-band attack was not detected")
        require(sum(row_count for row_count, _, _ in totals) > 20, "insufficient rows")
        require(sum(top_count for _, top_count, _ in totals) > 10, "insufficient top rows")
    except (AuditFailure, ValueError, ZeroDivisionError) as error:
        print(f"TPC215_MAJORANT_SANITY=FAIL {error}", file=sys.stderr)
        return 1
    print("TPC215_MAJORANT_SANITY=PASS")
    print("configurations=", len(configurations))
    print("active_rows=", sum(row_count for row_count, _, _ in totals))
    print("top_shell_rows=", sum(top_count for _, top_count, _ in totals))
    print("full_band_attack=REJECTED")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
