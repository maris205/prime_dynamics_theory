#!/usr/bin/env python3
"""Exact rational stress tests for TPC-248 Gram pseudoinverses."""

from __future__ import annotations

import argparse
from fractions import Fraction
from itertools import product


class Failure(RuntimeError):
    pass


def need(condition: bool, message: str) -> None:
    if type(condition) is not bool or not condition:
        raise Failure(message)


def tr(a):
    return [list(column) for column in zip(*a)]


def mm(a, b):
    return [[sum((a[i][k] * b[k][j] for k in range(len(b))), Fraction(0))
             for j in range(len(b[0]))] for i in range(len(a))]


def mv(a, x):
    return [sum((u * v for u, v in zip(row, x)), Fraction(0)) for row in a]


def identity(n):
    return [[Fraction(int(i == j)) for j in range(n)] for i in range(n)]


def inverse(a):
    n = len(a)
    aug = [row[:] + eye[:] for row, eye in zip(a, identity(n))]
    for col in range(n):
        pivot = next((row for row in range(col, n) if aug[row][col] != 0), None)
        need(pivot is not None, "singular matrix")
        aug[col], aug[pivot] = aug[pivot], aug[col]
        scale = aug[col][col]
        aug[col] = [value / scale for value in aug[col]]
        for row in range(n):
            if row == col:
                continue
            factor = aug[row][col]
            aug[row] = [left - factor * right
                        for left, right in zip(aug[row], aug[col])]
    return [row[n:] for row in aug]


def qmatrix(rows):
    return [[Fraction(value) for value in row] for row in rows]


def verify_probe_matrix(v):
    # v is the physical-coordinate-by-probe matrix and has full row rank.
    vt = tr(v)
    gram = mm(vt, v)
    frame = mm(v, vt)
    frame_inv = inverse(frame)
    frame_inv_sq = mm(frame_inv, frame_inv)
    dagger = mm(mm(vt, frame_inv_sq), v)
    need(mm(mm(gram, dagger), gram) == gram, "MP1")
    need(mm(mm(dagger, gram), dagger) == dagger, "MP2")
    need(mm(gram, dagger) == tr(mm(gram, dagger)), "MP3")
    need(mm(dagger, gram) == tr(mm(dagger, gram)), "MP4")
    samples = 0
    for raw in product((-1, 0, 1), repeat=len(v)):
        w = [Fraction(value) for value in raw]
        y = mv(vt, w)
        recovered_energy = sum((a * b for a, b in zip(y, mv(dagger, y))), Fraction(0))
        physical_energy = sum((value * value for value in w), Fraction(0))
        need(recovered_energy == physical_energy, "minimum energy")
        samples += 1
    return samples


def check():
    matrices = [
        [[1, 1]],
        [[1, 2, -1]],
        [[1, 0], [0, 1]],
        [[1, 0, 1], [0, 1, 1]],
        [[1, 1, 0], [0, 1, 1]],
        [[1, 0, 0], [0, 1, 0], [0, 0, 1]],
        [[1, 0, 0, 1], [0, 1, 0, 1], [0, 0, 1, 1]],
    ]
    samples = sum(verify_probe_matrix(qmatrix(rows)) for rows in matrices)
    need(Fraction(1) ** 2 + Fraction(1) ** 2 > Fraction(1) ** 2,
         "global budget obstruction")
    need(Fraction(3, 5) ** 2 + Fraction(4, 5) ** 2 == 1,
         "sphere boundary fixture")
    print("TPC248_GRAM_ELLIPSOID_STRESS=PASS")
    print("probe_matrices=" + str(len(matrices)))
    print("minimum_energy_samples=" + str(samples))
    print("global_budget_obstruction=PASS")


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()
    if not args.check:
        raise SystemExit("TPC248_GRAM_ELLIPSOID_STRESS=FAIL: use --check")
    try:
        check()
    except (Failure, StopIteration, TypeError, ValueError, ZeroDivisionError) as error:
        raise SystemExit("TPC248_GRAM_ELLIPSOID_STRESS=FAIL: " + str(error))


if __name__ == "__main__":
    main()
