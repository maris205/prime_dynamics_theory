#!/usr/bin/env python3
"""Exact small fixtures for the TPC-299 budget frontier."""

from __future__ import annotations

from fractions import Fraction
from math import isclose, sqrt


class Failure(RuntimeError):
    pass


def need(condition: bool, message: str) -> None:
    if type(condition) is not bool or not condition:
        raise Failure(message)


def norm_sq(values: list[float]) -> float:
    return sum(value * value for value in values)


def ridge(v: list[list[float]], m: list[list[float]],
          b: list[float], lam: float) -> tuple[list[float], float, float]:
    # This fixture only uses diagonal normal matrices, so the explicit solve
    # keeps the adversarial cases transparent.
    columns = len(m)
    gram = [[sum(v[i][j] * v[i][k] for i in range(len(v)))
             for k in range(columns)] for j in range(columns)]
    rhs = [sum(v[i][j] * b[i] for i in range(len(v)))
           for j in range(columns)]
    a = [[gram[i][j] + lam * m[i][j] for j in range(columns)]
         for i in range(columns)]
    # Gauss-Jordan solve.
    aug = [a[i] + [rhs[i]] for i in range(columns)]
    for col in range(columns):
        pivot = next(r for r in range(col, columns)
                     if abs(aug[r][col]) > 1e-14)
        aug[col], aug[pivot] = aug[pivot], aug[col]
        scale = aug[col][col]
        aug[col] = [x / scale for x in aug[col]]
        for r in range(columns):
            if r == col:
                continue
            factor = aug[r][col]
            aug[r] = [x - factor * y for x, y in zip(aug[r], aug[col])]
    c = [aug[i][-1] for i in range(columns)]
    residual = [sum(v[i][j] * c[j] for j in range(columns)) - b[i]
                for i in range(len(v))]
    source = sum(c[i] * m[i][j] * c[j]
                 for i in range(columns) for j in range(columns))
    return c, norm_sq(residual), source


def main() -> int:
    # One-dimensional exact budget: V=1, M=4, b=1, residual radius=1/2.
    # The feasible endpoint is c=1/2, source budget is exactly 1.
    c, residual, source = ridge([[1.0]], [[4.0]], [1.0], 0.25)
    need(isclose(c[0], 0.5, rel_tol=0, abs_tol=1e-12),
         "one-dimensional ridge coefficient")
    need(isclose(residual, 0.25, rel_tol=0, abs_tol=1e-12),
         "one-dimensional boundary residual")
    need(isclose(source, 1.0, rel_tol=0, abs_tol=1e-12),
         "one-dimensional exact budget")

    # Nested image spaces: adding the second coordinate strictly lowers the
    # minimum budget at the same radius.
    v1 = [[1.0], [0.0]]
    v2 = [[1.0, 0.0], [0.0, 1.0]]
    b = [1.0, 1.0]
    radius_sq = 1.0
    _, r1, s1 = ridge(v1, [[1.0]], b, 0.0)
    # For the full image, the minimum-norm point on the radius circle is
    # (1-1/sqrt(2))b.
    scale = 1.0 - 1.0 / sqrt(2.0)
    s2 = 2.0 * scale * scale
    r2 = 2.0 * (scale - 1.0) ** 2
    need(isclose(r1, radius_sq, rel_tol=0, abs_tol=1e-12),
         "nested first residual")
    need(isclose(r2, radius_sq, rel_tol=0, abs_tol=1e-12),
         "nested second residual")
    need(s2 < s1 and isclose(s1, 1.0, rel_tol=0, abs_tol=1e-12),
         "nested budget monotonicity")

    # An out-of-image target is infeasible below its projection distance.
    _, impossible_residual, _ = ridge(v1, [[1.0]], b, 0.0)
    need(impossible_residual > Fraction(1, 4),
         "infeasible tolerance fixture")

    # Zero budget gives the zero source and residual ||b|| exactly.
    _, zero_residual, zero_source = ridge([[2.0]], [[3.0]], [1.0], 1e15)
    need(zero_source < 1e-20 and isclose(zero_residual, 1.0,
                                        rel_tol=0, abs_tol=1e-9),
         "zero-budget limit")
    print("TPC299_STRESS=PASS exact_budget=1 nested_budget_drop=1 "
          "infeasible_case=1 zero_budget_limit=1")
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except Failure as error:
        print("TPC299_STRESS=FAIL " + str(error))
        raise SystemExit(1)
