#!/usr/bin/env python3
"""Exact stress family for the TPC-259 projection and residual firewall."""

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


def clocks() -> list[tuple[Fraction, str]]:
    answer = [(Fraction(512 + 17 * i, 1), "integer") for i in range(256)]
    for i in range(256):
        numerator = 4097 + 37 * i + 2 * (i % 13) + 1
        if numerator % 8 == 0:
            numerator += 1
        answer.append((Fraction(numerator, 8), "noninteger"))
    return answer


def split(clock: Fraction, index: int) -> list[int]:
    a = floor_fraction(clock / 2)
    b = floor_fraction(clock)
    total = b - a
    ell = total // 2
    right = total - ell
    left_shift = index % 9 - 4
    right_shift = (index // 9) % 9 - 4
    first = min(max(ell // 2 + left_shift, 1), ell - 1)
    third = min(max(right // 2 + right_shift, 1), right - 1)
    return [first, ell - first, third, right - third]


def check_frame(sizes: list[int]) -> None:
    ell = sizes[0] + sizes[1]
    right = sizes[2] + sizes[3]
    total = ell + right
    vectors = [
        (Fraction(ell * right, total),
         [Fraction(1, ell), Fraction(1, ell),
          Fraction(-1, right), Fraction(-1, right)]),
        (Fraction(sizes[0] * sizes[1], ell),
         [Fraction(1, sizes[0]), Fraction(-1, sizes[1]), Fraction(0), Fraction(0)]),
        (Fraction(sizes[2] * sizes[3], right),
         [Fraction(0), Fraction(0), Fraction(1, sizes[2]), Fraction(-1, sizes[3])]),
    ]
    for rho2, vector in vectors:
        value = rho2 * sum((size * coefficient * coefficient
                            for size, coefficient in zip(sizes, vector)),
                           Fraction(0))
        need(value == 1, "frame norm")
    for i in range(3):
        for j in range(i + 1, 3):
            value = sum((size * left * right_value
                         for size, left, right_value
                         in zip(sizes, vectors[i][1], vectors[j][1])),
                        Fraction(0))
            need(value == 0, "frame dot")


def projection_identity(index: int) -> None:
    # The vectors and output are deliberately varied; all arithmetic is exact.
    z = [Fraction(1), Fraction(0)]
    w = [Fraction(index % 7 - 3), Fraction((index % 11) - 5)]
    output = [Fraction(2 * (index % 5) - 3), Fraction(3 - (index % 13))]
    coefficient = sum((z[i] * w[i] for i in range(2)), Fraction(0))
    residual = [w[i] - coefficient * z[i] for i in range(2)]
    left = sum((w[i] * output[i] for i in range(2)), Fraction(0))
    right = coefficient * sum((z[i] * output[i] for i in range(2)), Fraction(0))
    right += sum((residual[i] * output[i] for i in range(2)), Fraction(0))
    need(left == right and residual[0] == 0, "projection identity")


def residual_witness(index: int) -> None:
    lam = Fraction((index % 17) + 1, 3)
    if index % 2:
        lam = -lam
    z = [Fraction(1), Fraction(0)]
    w = [Fraction(0), Fraction(1)]
    output = [Fraction(0), lam]
    need(sum(z[i] * w[i] for i in range(2)) == 0, "null witness")
    need(sum(w[i] * output[i] for i in range(2)) == lam, "full witness")
    need(sum(z[i] * output[i] for i in range(2)) == 0, "diagonal witness")


def run() -> dict[str, int]:
    family = clocks()
    norms = dots = source_splits = projections = witnesses = 0
    for index, (clock, kind) in enumerate(family):
        need((clock.denominator == 1) == (kind == "integer"), "clock class")
        sizes = split(clock, index)
        need(all(size > 0 for size in sizes), "positive split")
        need(sum(sizes) == floor_fraction(clock) - floor_fraction(clock / 2),
             "source split")
        check_frame(sizes)
        norms += 3
        dots += 3
        source_splits += 1
        projection_identity(index)
        projections += 1
        residual_witness(index)
        witnesses += 1

    l1 = math.log(3456.0 / 3125.0)
    l2 = math.log(884736.0 / 823543.0)
    length = math.hypot(l1, l2)
    need(abs((l2 / length) ** 2 + (-l1 / length) ** 2 - 1.0) < 2e-15,
         "null weights")
    previous = 0.0
    rate_models = 0
    for m in range(16, 42, 2):
        ratio = (1.0 / m) / math.exp(-m * m / 400.0)
        need(ratio > previous, "rate diagnostic")
        previous = ratio
        rate_models += 1
    need(Fraction(1, 2) + Fraction(55, 48) == Fraction(79, 48),
         "residual exponent")
    need(Fraction(5, 3) - Fraction(79, 48) == Fraction(1, 48),
         "gap")
    return {"families": len(family), "integer": 256, "noninteger": 256,
            "norms": norms, "dots": dots, "source_splits": source_splits,
            "projections": projections, "witnesses": witnesses,
            "rate_models": rate_models}


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()
    need(args.check, "--check required")
    counts = run()
    print("TPC259_STRESS=PASS "
          f"families={counts['families']} integer={counts['integer']} "
          f"noninteger={counts['noninteger']} norms={counts['norms']} "
          f"dots={counts['dots']} projections={counts['projections']} "
          f"witnesses={counts['witnesses']} rate_models={counts['rate_models']}")
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except Exception as exc:
        print("TPC259_STRESS=FAIL " + str(exc), file=sys.stderr)
        raise SystemExit(1)
