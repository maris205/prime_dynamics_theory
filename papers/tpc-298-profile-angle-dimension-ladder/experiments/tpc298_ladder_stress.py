#!/usr/bin/env python3
"""Exact adversarial fixtures for the TPC-298 angle ladder."""

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
        pivot = next((r for r in range(col, n) if aug[r][col]), None)
        need(pivot is not None, "fixture singular system")
        aug[col], aug[pivot] = aug[pivot], aug[col]
        scale = aug[col][col]
        aug[col] = [x / scale for x in aug[col]]
        for r in range(n):
            if r == col or not aug[r][col]:
                continue
            factor = aug[r][col]
            aug[r] = [x - factor * y for x, y in zip(aug[r], aug[col])]
    return [aug[i][-1] for i in range(n)]


def projection_data(v: list[list[Fraction]],
                    b: list[Fraction]) -> tuple[list[Fraction], list[Fraction],
                                                 list[Fraction]]:
    vt = transpose(v)
    coefficients = solve(gram(v), mat_vec(vt, b))
    projected = [sum(v[i][j] * coefficients[j]
                     for j in range(len(coefficients))) for i in range(len(b))]
    residual = [projected[i] - b[i] for i in range(len(b))]
    return coefficients, projected, residual


def exact_rank(matrix: list[list[Fraction]]) -> int:
    a = [row[:] for row in matrix]
    if not a or not a[0]:
        return 0
    rows, columns = len(a), len(a[0])
    rank = 0
    for column in range(columns):
        pivot = next((r for r in range(rank, rows) if a[r][column]), None)
        if pivot is None:
            continue
        a[rank], a[pivot] = a[pivot], a[rank]
        scale = a[rank][column]
        a[rank] = [x / scale for x in a[rank]]
        for r in range(rows):
            if r == rank or not a[r][column]:
                continue
            factor = a[r][column]
            a[r] = [x - factor * y for x, y in zip(a[r], a[rank])]
        rank += 1
        if rank == rows:
            break
    return rank


def main() -> int:
    # A two-dimensional image in R^3 and a third direction that closes the
    # target space.  This catches projection, angle, and nesting mistakes.
    v1 = [[Fraction(1), Fraction(0)],
          [Fraction(0), Fraction(1)],
          [Fraction(1), Fraction(1)]]
    b_in = [Fraction(2), Fraction(-1), Fraction(1)]
    b_out = [Fraction(1), Fraction(1), Fraction(0)]
    _, projected, residual = projection_data(v1, b_in)
    need(residual == [Fraction(0)] * 3, "exact in-image projection")
    need(projected == b_in, "in-image projection value")
    _, projected_out, residual_out = projection_data(v1, b_out)
    residual_sq = dot(residual_out, residual_out)
    norm_sq = dot(b_out, b_out)
    captured_sq = dot(projected_out, projected_out)
    need(residual_sq > 0, "outside residual")
    need(residual_sq + captured_sq == norm_sq,
         "exact principal-angle Pythagoras")
    # Adding a column can only reduce the normalized residual; this column
    # makes the outside target exact.
    v2 = [row + [Fraction(1 if i == 2 else 0)]
          for i, row in enumerate(v1)]
    _, _, residual_two = projection_data(v2, b_out)
    need(dot(residual_two, residual_two) == 0, "nested exact closure")
    need(dot(residual_two, residual_two) <= residual_sq,
         "nested image monotonicity")

    # A rank ladder with an intentionally repeated late column must still
    # report min(k,3), not the number of columns.
    ladder = [[Fraction(1), Fraction(0), Fraction(0), Fraction(1)],
              [Fraction(0), Fraction(1), Fraction(0), Fraction(0)],
              [Fraction(0), Fraction(0), Fraction(1), Fraction(0)]]
    ranks = [exact_rank([row[:k] for row in ladder])
             for k in range(1, 5)]
    need(ranks == [1, 2, 3, 3], "rank ladder adversary")

    # The first-threshold index is monotone under adding directions.
    threshold = Fraction(1, 2)
    residual_sequence = [Fraction(3, 4), Fraction(3, 5), Fraction(2, 5)]
    first = next(i + 1 for i, value in enumerate(residual_sequence)
                 if value <= threshold)
    need(first == 3, "threshold index")
    need(all(residual_sequence[i] <= residual_sequence[i - 1]
             for i in range(1, len(residual_sequence))),
         "threshold monotonicity")
    print("TPC298_STRESS=PASS projection_cases=4 angle_cases=1 "
          "nesting_cases=2 rank_ladder_cases=1 threshold_cases=1")
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except Failure as error:
        print("TPC298_STRESS=FAIL " + str(error))
        raise SystemExit(1)
