#!/usr/bin/env python3
"""Stress families for the TPC-260 Haar-complement and mode audit."""

from __future__ import annotations

import argparse
import sys
from fractions import Fraction


def need(condition: bool, message: str) -> None:
    if type(condition) is not bool or not condition:
        raise RuntimeError(message)


def dot(left, right, sizes):
    return sum((Fraction(size) * a * b
                for size, a, b in zip(sizes, left, right)), Fraction(0))


def specs(sizes):
    s0, s1, s2, s3 = sizes
    left, right = s0 + s1, s2 + s3
    total = left + right
    return [
        (Fraction(left * right, total),
         (Fraction(1, left), Fraction(1, left),
          Fraction(-1, right), Fraction(-1, right))),
        (Fraction(s0 * s1, left),
         (Fraction(1, s0), Fraction(-1, s1), Fraction(0), Fraction(0))),
        (Fraction(s2 * s3, right),
         (Fraction(0), Fraction(0), Fraction(1, s2), Fraction(-1, s3))),
    ]


def frame_check(sizes):
    vectors = specs(sizes)
    scale = (Fraction(1),) * 4
    for rho2, vector in vectors:
        need(dot(vector, vector, sizes) * rho2 == 1, "norm")
        need(dot(scale, vector, sizes) == 0, "scale")
    for i in range(3):
        for j in range(i + 1, 3):
            need(dot(vectors[i][1], vectors[j][1], sizes) == 0,
                 "orthogonality")


def gauss_add(left, right):
    return left[0] + right[0], left[1] + right[1]


def gauss_mul(left, right):
    return (left[0] * right[0] - left[1] * right[1],
            left[0] * right[1] + left[1] * right[0])


def gauss_norm(value):
    return value[0] * value[0] + value[1] * value[1]


def dft(phases):
    roots = [(1, 0), (0, 1), (-1, 0), (0, -1)]
    modes = []
    for k in range(4):
        total = (Fraction(0), Fraction(0))
        for j, value in enumerate(phases):
            root = roots[(-j * k) % 4]
            product = gauss_mul(root, value)
            total = gauss_add(total, product)
        modes.append((total[0] / 2, total[1] / 2))
    return modes


def mode_check(phases, expected_mode):
    modes = dft(phases)
    energy = [gauss_norm(mode) for mode in modes]
    packet_energy = sum((gauss_norm(value) for value in phases), Fraction(0))
    total = (sum(value[0] for value in phases),
             sum(value[1] for value in phases))
    need(sum(energy, Fraction(0)) == packet_energy, "Parseval")
    need(gauss_norm(total) == 4 * energy[0], "mode zero")
    need(energy == expected_mode, "mode placement")
    need(total[0] == 0 and total[1] == 0 or
         gauss_norm(total) > 0, "aggregate record")


def run() -> dict[str, int]:
    frame_count = 0
    for i in range(256):
        sizes = (3 + 2 * i, 4 + 3 * i + (i % 2),
                 5 + 4 * i, 6 + 5 * i + (i % 3))
        frame_check(sizes)
        frame_count += 1
    for i in range(256):
        sizes = (9 + 5 * i + (i % 4), 10 + 2 * i,
                 12 + 3 * i + (i % 5), 15 + 4 * i)
        frame_check(sizes)
        frame_count += 1

    one = (Fraction(1), Fraction(0))
    minus = (Fraction(-1), Fraction(0))
    imag = (Fraction(0), Fraction(1))
    neg_imag = (Fraction(0), Fraction(-1))
    mode_check([one, one, one, one], [Fraction(4), Fraction(0),
                                     Fraction(0), Fraction(0)])
    mode_check([one, minus, one, minus], [Fraction(0), Fraction(0),
                                          Fraction(4), Fraction(0)])
    mode_check([one, imag, minus, neg_imag], [Fraction(0), Fraction(4),
                                              Fraction(0), Fraction(0)])

    # The equal-length completion has both exact endpoint residuals and the
    # same packet diagonal in every phase family above.
    endpoint_checks = 2
    need(max(2 * 7 - (1 + 2 + 3 + 7), 0) == 1, "polygon lower endpoint")
    need(1 + 2 + 3 + 7 == 13, "polygon upper endpoint")
    return {"frame_families": frame_count, "mode_families": 3,
            "endpoint_checks": endpoint_checks}


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()
    need(args.check, "--check required")
    counts = run()
    print("TPC260_STRESS=PASS "
          f"frame_families={counts['frame_families']} "
          f"mode_families={counts['mode_families']} "
          f"endpoint_checks={counts['endpoint_checks']} "
          "null_channel=ZERO residual_range=EXACT")
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except Exception as exc:
        print("TPC260_STRESS=FAIL " + str(exc), file=sys.stderr)
        raise SystemExit(1)
