#!/usr/bin/env python3
"""Exact rational checks for the TPC-110 determinant-binning SVD."""

from __future__ import annotations

import argparse
import json
from fractions import Fraction
from pathlib import Path


def projection(fibers: list[list[int]], size: int) -> list[list[Fraction]]:
    p = [[Fraction(0) for _ in range(size)] for _ in range(size)]
    for fiber in fibers:
        m = len(fiber)
        for i in fiber:
            for j in fiber:
                p[i][j] = Fraction(1, m)
    return p


def matmul(a: list[list[Fraction]], b: list[list[Fraction]]) -> list[list[Fraction]]:
    return [
        [sum(a[i][k] * b[k][j] for k in range(len(b))) for j in range(len(b[0]))]
        for i in range(len(a))
    ]


def apply(a: list[list[Fraction]], v: list[Fraction]) -> list[Fraction]:
    return [sum(row[j] * v[j] for j in range(len(v))) for row in a]


def certificate() -> dict:
    partitions = [
        [[0], [1], [2], [3]],
        [[0, 1], [2, 3]],
        [[0, 1, 2], [3, 4], [5]],
        [[0, 1, 2, 3, 4]],
    ]
    checks = 0
    kernel_dimensions = []
    for fibers in partitions:
        size = sum(len(f) for f in fibers)
        p = projection(fibers, size)
        assert matmul(p, p) == p
        checks += 1
        assert all(p[i][j] == p[j][i] for i in range(size) for j in range(size))
        checks += 1
        kernel_dimensions.append(size - len(fibers))
        checks += 1

        for fiber in fibers:
            if len(fiber) >= 2:
                v = [Fraction(0) for _ in range(size)]
                v[fiber[0]] = Fraction(1)
                v[fiber[1]] = Fraction(-1)
                assert apply(p, v) == [Fraction(0) for _ in range(size)]
                checks += 1

    q = Fraction(267, 400)
    j = Fraction(133, 400)
    assert q + j == 1
    checks += 1
    assert q - 2 * j == Fraction(1, 400)
    checks += 1

    return {
        "schema": "tpc110-post-bin-energy-audit-v1",
        "status": "PASS",
        "partitions_tested": len(partitions),
        "kernel_dimensions": kernel_dimensions,
        "assertions_checked": checks,
        "endpoint_identities": {
            "q_plus_j": str(q + j),
            "q_minus_2j": str(q - 2 * j),
        },
        "claim_boundary": {
            "exact_binning_svd": True,
            "natural_scale_energy_lower_bound": False,
            "zero_mode_estimate": False,
            "fixed_h0_L2_progress": False,
        },
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--check", action="store_true")
    parser.add_argument("--write", action="store_true")
    args = parser.parse_args()
    result = certificate()
    target = Path(__file__).with_suffix(".json")
    if args.write:
        target.write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
    if args.check:
        expected = json.loads(target.read_text(encoding="utf-8"))
        if result != expected:
            raise SystemExit("certificate mismatch")
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
