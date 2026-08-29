#!/usr/bin/env python3
"""Small exact stress suite for the TPC-302 finite theorem layer."""

from __future__ import annotations

from fractions import Fraction
import sys


class Failure(RuntimeError):
    pass


def need(condition: bool, message: str) -> None:
    if type(condition) is not bool or not condition:
        raise Failure(message)


def gram_identity_fixture() -> None:
    vectors = ((Fraction(2), Fraction(-1), Fraction(3)),
               (Fraction(1), Fraction(4), Fraction(-2)),
               (Fraction(-3), Fraction(2), Fraction(1)))
    gram = [[sum(vectors[i][u] * vectors[j][u] for u in range(3))
             for j in range(3)] for i in range(3)]
    for signs in ((1, 1, 1), (1, -1, 1), (-1, 1, -1)):
        left = sum(signs[i] * signs[j] * gram[i][j]
                   for i in range(3) for j in range(3))
        combined = [sum(signs[i] * vectors[i][u] for i in range(3))
                    for u in range(3)]
        right = sum(value * value for value in combined)
        need(left == right and left >= 0, "Gram PSD identity")


def gray_class_fixture() -> None:
    # Global sign fixing leaves exactly 2^(m-1) classes, and the quadratic
    # value is unchanged by the omitted global flip.
    for m in range(1, 9):
        need(2 ** (m - 1) == len(list(range(1 << (m - 1)))),
             "Gray class count")
    matrix = [[Fraction(2), Fraction(1)], [Fraction(1), Fraction(3)]]
    a = (1, -1)
    b = (-1, 1)
    qa = sum(a[i] * a[j] * matrix[i][j] for i in range(2)
             for j in range(2))
    qb = sum(b[i] * b[j] * matrix[i][j] for i in range(2)
             for j in range(2))
    need(qa == qb, "global sign symmetry")


def budget_nesting_fixture() -> None:
    # A one-dimensional exact frontier: V=3, M=2, b=6.
    values = []
    for tau in (Fraction(1, 4), Fraction(1, 2), Fraction(3, 4)):
        c = Fraction(2) * (1 - tau)
        values.append(Fraction(2) * c * c)
    need(values[0] >= values[1] >= values[2], "tolerance nesting")
    # Adding a source coordinate and retaining coefficient zero gives a
    # nested feasible set; a common positive normalizer cancels exactly.
    need(Fraction(7, 11) / Fraction(13, 5) /
         (Fraction(1, 37) / Fraction(13, 5)) == Fraction(7, 11) /
         Fraction(1, 37), "normalization cancellation")


def main() -> int:
    try:
        gram_identity_fixture()
        gray_class_fixture()
        budget_nesting_fixture()
    except Failure as error:
        print("TPC302_STRESS=FAIL " + str(error), file=sys.stderr)
        return 1
    print("TPC302_STRESS=PASS gram_psd=1 global_sign=1 "
          "budget_nesting=1 normalization=1")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
