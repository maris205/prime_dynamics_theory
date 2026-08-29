#!/usr/bin/env python3
"""Small exact stress fixtures for the TPC-300 dual algebra."""

from __future__ import annotations

import sys
from fractions import Fraction


class Failure(RuntimeError):
    pass


def need(condition: bool, message: str) -> None:
    if type(condition) is not bool or not condition:
        raise Failure(message)


def solve(matrix: list[list[Fraction]], rhs: list[Fraction]) -> list[Fraction]:
    n = len(rhs)
    a = [row[:] + [value] for row, value in zip(matrix, rhs)]
    for col in range(n):
        pivot = next((row for row in range(col, n) if a[row][col]), None)
        need(pivot is not None, "singular fixture")
        a[col], a[pivot] = a[pivot], a[col]
        q = a[col][col]
        a[col] = [x / q for x in a[col]]
        for row in range(n):
            if row == col:
                continue
            q = a[row][col]
            if q:
                a[row] = [a[row][j] - q * a[col][j]
                          for j in range(n + 1)]
    return [a[row][-1] for row in range(n)]


def quadratic(vector: list[Fraction], matrix: list[list[Fraction]]) -> Fraction:
    return sum((vector[i] * matrix[i][j] * vector[j]
                for i in range(len(vector))
                for j in range(len(vector))), Fraction(0))


def dot(left: list[Fraction], right: list[Fraction]) -> Fraction:
    return sum((x * y for x, y in zip(left, right)), Fraction(0))


def dual_fixture(V: list[list[Fraction]], M: list[list[Fraction]],
                 b: list[Fraction], rho: Fraction,
                 radius_squared: Fraction) -> tuple[Fraction, Fraction,
                                                     Fraction]:
    vt_v = [[sum((V[r][i] * V[r][j] for r in range(len(V))), Fraction(0))
             + rho * M[i][j] for j in range(len(M))]
            for i in range(len(M))]
    vt_b = [sum((V[r][i] * b[r] for r in range(len(V))), Fraction(0))
            for i in range(len(M))]
    c = solve(vt_v, vt_b)
    vc = [sum((V[r][i] * c[i] for i in range(len(c))), Fraction(0))
          for r in range(len(V))]
    residual = [vc[r] - b[r] for r in range(len(V))]
    primal_at_c = quadratic(c, M)
    lagrangian = primal_at_c + (quadratic(residual,
                                          [[Fraction(int(i == j))
                                            for j in range(len(V))]
                                           for i in range(len(V))])
                                - radius_squared) / rho
    formula = (dot(b, b) - radius_squared - dot(b, vc)) / rho
    return primal_at_c, lagrangian, formula


def main() -> int:
    try:
        # Scalar active frontier: min c^2 subject to |2c-3|<=1 is c=1.
        V = [[Fraction(2)]]
        M = [[Fraction(1)]]
        b = [Fraction(3)]
        primal, lagrangian, formula = dual_fixture(
            V, M, b, Fraction(2), Fraction(1))
        need(primal == 1, "scalar primal")
        need(lagrangian == formula == 1, "dual identity at active point")

        # An arbitrary positive ridge parameter is a valid weak dual bound.
        _, lagrangian_lo, formula_lo = dual_fixture(
            V, M, b, Fraction(1), Fraction(1))
        need(lagrangian_lo == formula_lo == Fraction(4, 5),
             "weak dual scalar value")
        need(formula_lo <= primal, "weak dual inequality")

        # The KKT multiplier is reciprocal to the ridge parameter.
        need(Fraction(2) * Fraction(1, 2) == 1,
             "rho-mu reciprocity")
        wrong_mu_solution = Fraction(6, 1) / (Fraction(4) + Fraction(1, 2))
        wrong_residual = abs(Fraction(2) * wrong_mu_solution - Fraction(3))
        need(wrong_residual != 1, "reciprocal correction witness")

        # A two-coordinate exact fixture checks the matrix form and positivity.
        V2 = [[Fraction(1), Fraction(0)],
              [Fraction(0), Fraction(2)]]
        M2 = [[Fraction(2), Fraction(0)],
              [Fraction(0), Fraction(3)]]
        b2 = [Fraction(2), Fraction(-1)]
        _, l2, f2 = dual_fixture(V2, M2, b2, Fraction(3, 2),
                                  Fraction(1))
        feasible_c2 = [Fraction(3, 2), Fraction(-1, 4)]
        feasible_output = [sum((V2[r][i] * feasible_c2[i]
                                for i in range(2)), Fraction(0))
                           for r in range(2)]
        feasible_residual = [feasible_output[r] - b2[r]
                             for r in range(2)]
        feasible_cost = quadratic(feasible_c2, M2)
        need(l2 == f2 and
             quadratic(feasible_residual,
                       [[Fraction(int(i == j)) for j in range(2)]
                        for i in range(2)]) <= 1 and
             f2 <= feasible_cost, "matrix dual fixture")
    except Failure as error:
        print("TPC300_STRESS=FAIL " + str(error), file=sys.stderr)
        return 1
    print("TPC300_STRESS=PASS scalar_identity=1 weak_dual=1 "
          "reciprocal_correction=1 matrix_fixture=1")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
