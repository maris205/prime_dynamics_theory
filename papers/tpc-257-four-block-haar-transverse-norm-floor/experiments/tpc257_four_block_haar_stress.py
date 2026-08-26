#!/usr/bin/env python3
"""Exact integer/noninteger stress families for TPC-257 geometry."""

from __future__ import annotations

import argparse
import sys
from fractions import Fraction


def need(condition: bool, message: str) -> None:
    if not condition:
        raise RuntimeError(message)


def floor_fraction(value: Fraction) -> int:
    return value.numerator // value.denominator


def clocks() -> list[tuple[Fraction, str]]:
    values: list[tuple[Fraction, str]] = []
    for index in range(96):
        values.append((Fraction(512 + 7 * index, 1), "integer"))
    for index in range(96):
        numerator = 4097 + 28 * index + 2 * (index % 6)
        values.append((Fraction(numerator, 8), "noninteger"))
    return values


def checked_family(clock: Fraction, family_index: int) -> tuple[int, int, int, int, int]:
    a = floor_fraction(clock / 2)
    b = floor_fraction(clock)
    n = b - a
    ell = n // 2
    right = n - ell
    need(ell > 8 and right > 8, "short stress clock")

    # Exercise several nearby balanced cuts, rather than only floor(length/2).
    left_shift = family_index % 3 - 1
    right_shift = (family_index // 3) % 3 - 1
    s1 = min(max(ell // 2 + left_shift, 1), ell - 1)
    s2 = ell - s1
    s3 = min(max(right // 2 + right_shift, 1), right - 1)
    s4 = right - s3
    sizes = [s1, s2, s3, s4]
    cursor = a + 1
    intervals: list[tuple[int, int]] = []
    for size in sizes:
        intervals.append((cursor, cursor + size - 1))
        cursor += size
    need(cursor == b + 1, "stress blocks fail to cover")

    specs = [
        (Fraction(ell * right, ell + right),
         [Fraction(1, ell), Fraction(1, ell), Fraction(-1, right), Fraction(-1, right)]),
        (Fraction(s1 * s2, s1 + s2),
         [Fraction(1, s1), Fraction(-1, s2), Fraction(0), Fraction(0)]),
        (Fraction(s3 * s4, s3 + s4),
         [Fraction(0), Fraction(0), Fraction(1, s3), Fraction(-1, s4)]),
    ]
    norms = dots = variations = 0
    for rho2, coeff in specs:
        norm = rho2 * sum((size * value * value for size, value in zip(sizes, coeff)), Fraction(0))
        need(norm == 1, "stress norm")
        variation_base = sum((abs(left - right) for left, right in
                              zip([Fraction(0)] + coeff, coeff + [Fraction(0)])), Fraction(0))
        need(rho2 * variation_base * variation_base == Fraction(4, 1) / rho2,
             "stress variation")
        norms += 1
        variations += 1
    for i in range(3):
        for j in range(i + 1, 3):
            dot = sum((size * left * right for size, left, right in
                       zip(sizes, specs[i][1], specs[j][1])), Fraction(0))
            need(dot == 0, "stress orthogonality")
            dots += 1

    layers = 0
    for lo, hi in intervals:
        length = hi - lo + 1
        for divisor in range(1, 33):
            count = hi // divisor - (lo - 1) // divisor
            need(abs(Fraction(count) - Fraction(length, divisor)) <= 1,
                 "stress divisor density")
            layers += 1

    # Outer endpoints and all three internal block boundaries.
    boundaries = [a, a + s1, a + ell, a + ell + s3, b]
    crossings = 0
    for shift in range(-80, 81):
        for boundary in boundaries:
            count = sum(1 for source in range(a + 1, b + 1)
                        if (source <= boundary) != (source + shift <= boundary))
            need(count <= abs(shift), "stress crossing")
            crossings += 1
    return norms, dots, variations, layers, crossings


def run() -> dict[str, int]:
    family_list = clocks()
    integer = sum(kind == "integer" for _, kind in family_list)
    noninteger = sum(kind == "noninteger" for _, kind in family_list)
    norms = dots = variations = layers = crossings = 0
    for index, (clock, kind) in enumerate(family_list):
        need((clock.denominator == 1) == (kind == "integer"), "clock class")
        a, b, c, d, e = checked_family(clock, index)
        norms += a
        dots += b
        variations += c
        layers += d
        crossings += e
    need(len(family_list) == 192, "family count")
    need(integer == 96 and noninteger == 96, "integer split")
    need(Fraction(133, 400) - Fraction(1, 2) == Fraction(-67, 400), "divisor exponent")
    need(Fraction(1, 3) + 2 * Fraction(21, 32) - Fraction(1, 2) == Fraction(55, 48),
         "boundary exponent")
    need(Fraction(2, 3) + Fraction(1, 2) == Fraction(56, 48), "main exponent")
    need(Fraction(56, 48) - Fraction(55, 48) == Fraction(1, 48), "gap")
    return {"families": len(family_list), "integer": integer, "noninteger": noninteger,
            "frame_norms": norms, "orthogonality": dots, "variation_checks": variations,
            "divisor_layers": layers, "boundary_crossings": crossings}


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()
    need(args.check, "--check is required")
    counts = run()
    print("TPC257_STRESS=PASS "
          f"families={counts['families']} integer={counts['integer']} "
          f"noninteger={counts['noninteger']} frame_norms={counts['frame_norms']} "
          f"orthogonality={counts['orthogonality']} divisor_layers={counts['divisor_layers']} "
          f"boundary_crossings={counts['boundary_crossings']}")
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except Exception as exc:
        print(f"TPC257_STRESS=FAIL {exc}", file=sys.stderr)
        raise SystemExit(1)
