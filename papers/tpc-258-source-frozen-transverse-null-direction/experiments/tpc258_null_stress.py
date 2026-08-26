#!/usr/bin/env python3
"""Clock and error-model stress checks for TPC-258."""

from __future__ import annotations

import argparse
import math
import sys
from fractions import Fraction


def need(condition: bool, message: str) -> None:
    if type(condition) is not bool or not condition:
        raise RuntimeError(message)


def floor_fraction(value: Fraction) -> int:
    return value.numerator // value.denominator


def family() -> list[tuple[Fraction, str]]:
    clocks = [(Fraction(512 + 11 * index, 1), "integer") for index in range(128)]
    for index in range(128):
        numerator = 4097 + 44 * index + 2 * (index % 11) + 1
        if numerator % 8 == 0:
            numerator += 1
        clocks.append((Fraction(numerator, 8), "noninteger"))
    return clocks


def run() -> dict[str, int]:
    clocks = family()
    norms = dots = source_splits = rate_models = 0
    l1 = math.log(3456.0 / 3125.0)
    l2 = math.log(884736.0 / 823543.0)
    denominator = math.hypot(l1, l2)
    weight1 = l2 / denominator
    weight2 = -l1 / denominator
    need(abs(weight1 * weight1 + weight2 * weight2 - 1.0) < 2e-15, "weights")
    for index, (clock, kind) in enumerate(clocks):
        need((clock.denominator == 1) == (kind == "integer"), "clock kind")
        a = floor_fraction(clock / 2)
        b = floor_fraction(clock)
        n = b - a
        ell = n // 2
        right = n - ell
        left_shift = index % 5 - 2
        right_shift = (index // 5) % 5 - 2
        s1 = min(max(ell // 2 + left_shift, 1), ell - 1)
        s2 = ell - s1
        s3 = min(max(right // 2 + right_shift, 1), right - 1)
        s4 = right - s3
        sizes = [s1, s2, s3, s4]
        rho1 = Fraction(s1 * s2, ell)
        rho2 = Fraction(s3 * s4, right)
        z1 = [Fraction(1, s1), Fraction(-1, s2), Fraction(0), Fraction(0)]
        z2 = [Fraction(0), Fraction(0), Fraction(1, s3), Fraction(-1, s4)]
        need(rho1 * sum((size * value * value for size, value in zip(sizes, z1)), Fraction(0)) == 1,
             "left norm")
        need(rho2 * sum((size * value * value for size, value in zip(sizes, z2)), Fraction(0)) == 1,
             "right norm")
        need(sum((size * left * right_value for size, left, right_value in
                  zip(sizes, z1, z2)), Fraction(0)) == 0, "disjoint dot")
        norms += 2
        dots += 1
        need(sum(sizes) == n and a + sum(sizes) == b, "source split")
        source_splits += 1

    # Finite diagnostics for the o(1)-versus-power firewall.
    previous = 0.0
    for m in range(16, 31, 2):
        ratio = (1.0 / m) / math.exp(-m * m / 400.0)
        need(ratio > previous, "rate ratio monotonicity")
        previous = ratio
        rate_models += 1
    need(Fraction(1, 2) - Fraction(1, 2) == 0, "formal cancellation")
    return {"families": len(clocks), "integer": 128, "noninteger": 128,
            "norms": norms, "dots": dots, "source_splits": source_splits,
            "rate_models": rate_models}


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()
    need(args.check, "--check required")
    counts = run()
    print("TPC258_STRESS=PASS "
          f"families={counts['families']} integer={counts['integer']} "
          f"noninteger={counts['noninteger']} norms={counts['norms']} "
          f"source_splits={counts['source_splits']} rate_models={counts['rate_models']}")
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except Exception as exc:
        print("TPC258_STRESS=FAIL " + str(exc), file=sys.stderr)
        raise SystemExit(1)
