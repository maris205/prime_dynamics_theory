#!/usr/bin/env python3
"""Adversarial finite tests for the TPC-295 source-correlation theorem."""

from __future__ import annotations

import itertools
import sys
from fractions import Fraction


class Failure(RuntimeError):
    pass


def need(condition: bool, message: str) -> None:
    if type(condition) is not bool or not condition:
        raise Failure(message)


def exact_rank(matrix: list[list[Fraction]]) -> int:
    a = [row[:] for row in matrix]
    rows, cols = len(a), len(a[0]) if a else 0
    rank = 0
    for column in range(cols):
        pivot = next((r for r in range(rank, rows) if a[r][column]), None)
        if pivot is None:
            continue
        a[rank], a[pivot] = a[pivot], a[rank]
        q = a[rank][column]
        a[rank] = [v / q for v in a[rank]]
        for r in range(rows):
            if r == rank or not a[r][column]:
                continue
            q = a[r][column]
            a[r] = [x - q * y for x, y in zip(a[r], a[rank])]
        rank += 1
        if rank == rows:
            break
    return rank


def gram(columns: list[list[Fraction]]) -> list[list[Fraction]]:
    return [[sum(columns[i][u] * columns[j][u]
                 for u in range(len(columns[0])))
             for j in range(len(columns))] for i in range(len(columns))]


def solve_square(matrix: list[list[Fraction]], target: list[Fraction]) -> list[Fraction]:
    n = len(matrix)
    a = [matrix[i][:] + [target[i]] for i in range(n)]
    for column in range(n):
        pivot = next((r for r in range(column, n) if a[r][column]), None)
        need(pivot is not None, "singular solve")
        a[column], a[pivot] = a[pivot], a[column]
        q = a[column][column]
        a[column] = [v / q for v in a[column]]
        for r in range(n):
            if r == column or not a[r][column]:
                continue
            q = a[r][column]
            a[r] = [x - q * y for x, y in zip(a[r], a[column])]
    return [a[i][-1] for i in range(n)]


def witness(columns: list[list[Fraction]], target: list[Fraction]) -> None:
    g = gram(columns)
    coefficients = solve_square(g, target)
    h = [sum(columns[j][u] * coefficients[j]
             for j in range(len(columns))) for u in range(len(columns[0]))]
    correlations = [sum(h[u] * columns[j][u]
                        for u in range(len(h))) for j in range(len(columns))]
    need(correlations == target, "explicit witness identity")


def deterministic_columns(n: int, m: int, seed: int) -> list[list[Fraction]]:
    state = seed
    columns = []
    for j in range(m):
        column = []
        for i in range(n):
            state = (1103515245 * state + 12345) % (2 ** 31)
            numerator = int(state % 17) - 8
            denominator = 1 + ((state >> 8) % 5)
            column.append(Fraction(numerator, denominator))
        columns.append(column)
    return columns


def modular_rank(matrix: list[list[Fraction]], modulus: int) -> int:
    def residue(value: Fraction) -> int:
        den = value.denominator % modulus
        need(den != 0, "test denominator")
        return value.numerator % modulus * pow(den, modulus - 2, modulus) % modulus
    a = [[residue(v) for v in row] for row in matrix]
    rows, cols = len(a), len(a[0]) if a else 0
    rank = 0
    for c in range(cols):
        pivot = next((r for r in range(rank, rows) if a[r][c]), None)
        if pivot is None:
            continue
        a[rank], a[pivot] = a[pivot], a[rank]
        inv = pow(a[rank][c], modulus - 2, modulus)
        a[rank] = [v * inv % modulus for v in a[rank]]
        for r in range(rank + 1, rows):
            factor = a[r][c]
            a[r] = [(x - factor * y) % modulus
                    for x, y in zip(a[r], a[rank])]
        rank += 1
    return rank


def main() -> int:
    full_cases = 0
    for m in range(1, 8):
        columns = deterministic_columns(m + 3, m, 19 + m)
        g = gram(columns)
        need(exact_rank(columns) == m and exact_rank(g) == m,
             "constructed full rank")
        need(modular_rank(g, 1000000007) == m and
             modular_rank(g, 998244353) == m, "modular rank agreement")
        for target in ([Fraction(1 if i == 0 else -1) for i in range(m)],
                       [Fraction(1) for _ in range(m)]):
            witness(columns, target)
        full_cases += 1

    singular_cases = 0
    for m in range(2, 8):
        base = deterministic_columns(m + 2, m - 1, 71 + m)
        columns = base + [base[0][:]]
        g = gram(columns)
        need(exact_rank(columns) == m - 1 and exact_rank(g) == m - 1,
             "constructed singular case")
        singular_cases += 1

    # A rank-deficient correlation map cannot hit every target: its image has
    # dimension at most m-1.  The duplicated-column cases above are the
    # concrete counterexample to the full-rank implication's converse.
    need(singular_cases == 6, "singular census")
    print("TPC295_STRESS=PASS full_rank_cases={} singular_cases={} "
          "targets=2_per_full_case moduli=2".format(full_cases,
                                                    singular_cases))
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except Failure as error:
        print("TPC295_STRESS=FAIL " + str(error), file=sys.stderr)
        raise SystemExit(1)
