#!/usr/bin/env python3
"""Stress grid for the exact rank-three frame identities."""

from __future__ import annotations

import argparse
from fractions import Fraction


def need(condition: bool, message: str) -> None:
    if type(condition) is not bool or not condition:
        raise RuntimeError(message)


def floor_fraction(value: Fraction) -> int:
    return value.numerator // value.denominator


def run_grid() -> tuple[int, int]:
    clocks = [Fraction(73 + 11 * i, 1) for i in range(32)]
    clocks += [Fraction(401 + 13 * i, 3) for i in range(32)]
    frame_cases = 0
    variation_cases = 0
    for clock in clocks:
        a = floor_fraction(clock / 2)
        b = floor_fraction(clock)
        n = b - a
        ell = n // 2
        right = n - ell
        sizes = [ell // 2, ell - ell // 2, right // 2,
                 right - right // 2]
        need(min(sizes) > 0, "empty block")
        specs = [
            (Fraction(ell * right, n),
             [Fraction(1, ell), Fraction(1, ell),
              Fraction(-1, right), Fraction(-1, right)]),
            (Fraction(sizes[0] * sizes[1], sizes[0] + sizes[1]),
             [Fraction(1, sizes[0]), Fraction(-1, sizes[1]),
              Fraction(0), Fraction(0)]),
            (Fraction(sizes[2] * sizes[3], sizes[2] + sizes[3]),
             [Fraction(0), Fraction(0), Fraction(1, sizes[2]),
              Fraction(-1, sizes[3])]),
        ]
        for rho2, coeff in specs:
            norm = rho2 * sum((s * c * c for s, c in zip(sizes, coeff)),
                              Fraction(0))
            need(norm == 1, "norm")
            jumps = [Fraction(0)] + coeff + [Fraction(0)]
            variation = sum((abs(jumps[j + 1] - jumps[j])
                             for j in range(len(jumps) - 1)), Fraction(0))
            need(rho2 * variation * variation == Fraction(4, 1) / rho2,
                 "variation")
            frame_cases += 1
            variation_cases += 1
        for i in range(3):
            for j in range(i + 1, 3):
                left = specs[i][1]
                right_coeff = specs[j][1]
                dot = sum((s * u * v for s, u, v in
                           zip(sizes, left, right_coeff)), Fraction(0))
                need(dot == 0, "orthogonality")
                frame_cases += 1
    return len(clocks), frame_cases + variation_cases


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()
    need(args.check, "--check required")
    clocks, checks = run_grid()
    w_exp = Fraction(1, 2)
    g_exp = Fraction(7, 6)
    need(w_exp + g_exp == Fraction(5, 3), "channel exponent")
    need(Fraction(5, 3) - Fraction(1997, 1200) == Fraction(1, 400),
         "endpoint gap")
    print("TPC263_RANK_THREE_STRESS=PASS "
          f"clocks={clocks} exact_checks={checks} "
          "rank=3 exponent=5/3 log_power=M+3 residual=OPEN")
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except Exception as exc:
        print("TPC263_RANK_THREE_STRESS=FAIL " + str(exc))
        raise SystemExit(1)
