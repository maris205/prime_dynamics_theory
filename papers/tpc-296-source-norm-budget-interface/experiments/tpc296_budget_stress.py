#!/usr/bin/env python3
"""Exact adversarial fixtures for the TPC-296 source-budget identities."""

from __future__ import annotations

import sys
from fractions import Fraction


class Failure(RuntimeError):
    pass


def need(condition: bool, message: str) -> None:
    if type(condition) is not bool or not condition:
        raise Failure(message)


def deterministic_columns(n: int, m: int, seed: int) -> list[list[Fraction]]:
    state = seed
    columns = []
    for _column in range(m):
        values = []
        for _row in range(n):
            state = (1664525 * state + 1013904223) % (2 ** 32)
            numerator = int(state % 19) - 9
            denominator = 1 + ((state >> 9) % 7)
            values.append(Fraction(numerator, denominator))
        columns.append(values)
    return columns


def gram(columns: list[list[Fraction]]) -> list[list[Fraction]]:
    return [[sum(columns[i][u] * columns[j][u]
                 for u in range(len(columns[0])))
             for j in range(len(columns))] for i in range(len(columns))]


def rank(matrix: list[list[Fraction]]) -> int:
    if not matrix:
        return 0
    a = [row[:] for row in matrix]
    rows, columns = len(a), len(a[0])
    result = 0
    for column in range(columns):
        pivot = next((r for r in range(result, rows) if a[r][column]), None)
        if pivot is None:
            continue
        a[result], a[pivot] = a[pivot], a[result]
        value = a[result][column]
        a[result] = [x / value for x in a[result]]
        for r in range(rows):
            if r == result or not a[r][column]:
                continue
            value = a[r][column]
            a[r] = [x - value * y for x, y in zip(a[r], a[result])]
        result += 1
        if result == rows:
            break
    return result


def solve(matrix: list[list[Fraction]], target: list[Fraction]) -> list[Fraction]:
    n = len(matrix)
    a = [matrix[i][:] + [target[i]] for i in range(n)]
    for column in range(n):
        pivot = next((r for r in range(column, n) if a[r][column]), None)
        need(pivot is not None, "singular solve")
        a[column], a[pivot] = a[pivot], a[column]
        value = a[column][column]
        a[column] = [x / value for x in a[column]]
        for r in range(n):
            if r == column or not a[r][column]:
                continue
            value = a[r][column]
            a[r] = [x - value * y for x, y in zip(a[r], a[column])]
    return [a[i][-1] for i in range(n)]


def dot(left: list[Fraction], right: list[Fraction]) -> Fraction:
    return sum(x * y for x, y in zip(left, right))


def matrix_vector(matrix: list[list[Fraction]], vector: list[Fraction]
                  ) -> list[Fraction]:
    return [dot(row, vector) for row in matrix]


def source_witness(columns: list[list[Fraction]], target: list[Fraction]
                   ) -> tuple[Fraction, Fraction, Fraction]:
    G = gram(columns)
    coefficients = solve(G, target)
    h = [sum(columns[j][u] * coefficients[j]
             for j in range(len(columns))) for u in range(len(columns[0]))]
    recovered = [sum(h[u] * columns[j][u] for u in range(len(h)))
                 for j in range(len(columns))]
    need(recovered == target, "exact witness")
    cost = dot(target, coefficients)
    need(dot(h, h) == cost, "least-norm identity")
    energy = dot(target, matrix_vector(G, target))
    target_norm = dot(target, target)
    trade = cost * energy
    need(trade >= target_norm * target_norm, "source-energy tradeoff")
    return cost, energy, trade


def main() -> int:
    full_cases = 0
    target_cases = 0
    profile_cases = 0
    for m in range(1, 7):
        columns = deterministic_columns(m + 4, m, 31 + m)
        G = gram(columns)
        need(rank(G) == m, "constructed full-rank Gram")
        targets = (
            [Fraction(1 if i % 2 == 0 else -1) for i in range(m)],
            [Fraction(1) for _ in range(m)],
        )
        for target in targets:
            cost, _energy, _trade = source_witness(columns, target)
            need(cost > 0 and cost <= cost and not (cost <= cost / 2),
                 "budget threshold order")
            target_cases += 1

        beta = [Fraction((3 * i + 1) % 7 - 3, 1 + i % 3)
                for i in range(m + 4)]
        native = [sum(beta[u] * columns[j][u] for u in range(len(beta)))
                  for j in range(m)]
        if dot(native, native):
            target = targets[0]
            alpha = dot(native, target) / dot(native, native)
            residual = [alpha * value - target[i]
                        for i, value in enumerate(native)]
            residual_squared = dot(residual, residual)
            formula = (dot(target, target) -
                       dot(native, target) ** 2 / dot(native, native))
            need(residual_squared == formula and residual_squared >= 0,
                 "one-ray projection formula")
            profile_cases += 1
        full_cases += 1

    singular_cases = 0
    for m in range(2, 7):
        base = deterministic_columns(m + 3, m - 1, 83 + m)
        columns = base + [base[0][:]]
        G = gram(columns)
        need(rank(G) == m - 1, "constructed singular Gram")
        target = [Fraction(0) for _ in range(m)]
        target[-1] = Fraction(1)
        augmented = [G[i][:] + [target[i]] for i in range(m)]
        need(rank(augmented) > rank(G), "singular unattainable target")
        singular_cases += 1

    print("TPC296_STRESS=PASS full_rank_cases={} target_cases={} "
          "profile_cases={} singular_cases={}".format(
              full_cases, target_cases, profile_cases, singular_cases))
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except Failure as error:
        print("TPC296_STRESS=FAIL " + str(error), file=sys.stderr)
        raise SystemExit(1)
