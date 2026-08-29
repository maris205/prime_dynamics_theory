#!/usr/bin/env python3
"""Exact adversarial fixtures for the TPC-297 projection interface."""

from __future__ import annotations

from fractions import Fraction


class Failure(RuntimeError):
    pass


def need(condition: bool, message: str) -> None:
    if type(condition) is not bool or not condition:
        raise Failure(message)


def dot(a: list[Fraction], b: list[Fraction]) -> Fraction:
    return sum((x * y for x, y in zip(a, b)), Fraction(0))


def transpose(a: list[list[Fraction]]) -> list[list[Fraction]]:
    return [list(column) for column in zip(*a)]


def mat_vec(a: list[list[Fraction]], x: list[Fraction]) -> list[Fraction]:
    return [dot(row, x) for row in a]


def gram(a: list[list[Fraction]]) -> list[list[Fraction]]:
    at = transpose(a)
    return [[dot(at[i], at[j]) for j in range(len(at))]
            for i in range(len(at))]


def solve(a: list[list[Fraction]], b: list[Fraction]) -> list[Fraction]:
    n = len(a)
    aug = [a[i][:] + [b[i]] for i in range(n)]
    for col in range(n):
        pivot = next(r for r in range(col, n) if aug[r][col])
        aug[col], aug[pivot] = aug[pivot], aug[col]
        scale = aug[col][col]
        aug[col] = [x / scale for x in aug[col]]
        for r in range(n):
            if r == col or not aug[r][col]:
                continue
            factor = aug[r][col]
            aug[r] = [x - factor * y for x, y in zip(aug[r], aug[col])]
    return [aug[i][-1] for i in range(n)]


def projection_residual(v: list[list[Fraction]], b: list[Fraction]) -> Fraction:
    # Full-column-rank normal equations on a small exact fixture.
    vt = transpose(v)
    coefficients = solve(gram(v), mat_vec(vt, b))
    residual = [sum(v[i][j] * coefficients[j]
                   for j in range(len(coefficients))) - b[i]
                for i in range(len(b))]
    return dot(residual, residual)


def main() -> int:
    # A two-dimensional image in R^3 and a third profile that changes nothing.
    v = [[Fraction(1), Fraction(0)],
         [Fraction(0), Fraction(1)],
         [Fraction(1), Fraction(1)]]
    b = [Fraction(2), Fraction(-1), Fraction(1)]
    residual = projection_residual(v, b)
    need(residual == 0, "exact in-image projection")
    outside = [Fraction(1), Fraction(1), Fraction(0)]
    residual_outside = projection_residual(v, outside)
    need(residual_outside > 0, "outside residual")
    # Adding a column can only reduce the residual; here it makes the target exact.
    v2 = [row + [Fraction(1 if i == 2 else 0)] for i, row in enumerate(v)]
    need(projection_residual(v2, outside) <= residual_outside,
         "nested image monotonicity")
    print("TPC297_STRESS=PASS projection_cases=3 nesting_cases=1")
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except Failure as error:
        print("TPC297_STRESS=FAIL " + str(error))
        raise SystemExit(1)
