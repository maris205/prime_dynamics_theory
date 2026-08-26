#!/usr/bin/env python3
"""Rational stress grid for the finite reduced-residue fiber."""

from __future__ import annotations

import argparse
from fractions import Fraction


def need(condition: bool, message: str) -> None:
    if type(condition) is not bool or not condition:
        raise RuntimeError(message)


def matrix(q: int):
    m = q - 1
    return tuple(tuple((Fraction(1) if i == j else Fraction(0))
                       - Fraction(1, m) for j in range(m))
                 for i in range(m))


def apply(c, v):
    return tuple(sum((a * b for a, b in zip(row, v)), Fraction(0))
                 for row in c)


def run_grid() -> int:
    primes = (3, 5, 7, 11, 13, 17, 19, 23)
    cases = 0
    for q in primes:
        c = matrix(q)
        m = q - 1
        square = tuple(tuple(sum((c[i][k] * c[k][j] for k in range(m)),
                                 Fraction(0)) for j in range(m))
                       for i in range(m))
        need(square == c, "idempotence")
        for seed in range(1, 10):
            v = tuple(Fraction((seed + 2 * i) ** 2 - 3 * seed)
                      for i in range(m))
            cv = apply(c, v)
            form = sum((a * b for a, b in zip(v, cv)), Fraction(0))
            pair_form = sum(((v[i] - v[j]) ** 2 for i in range(m)
                             for j in range(i + 1, m)), Fraction(0)) / m
            need(form == pair_form and form >= 0, "PSD identity")
            cases += 1
    return cases


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()
    need(args.check, "--check required")
    cases = run_grid()
    print("TPC262_FIBER_STRESS=PASS "
          f"cases={cases} primes=8 exact_projection=YES psd=YES")
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except Exception as exc:
        print("TPC262_FIBER_STRESS=FAIL " + str(exc))
        raise SystemExit(1)
