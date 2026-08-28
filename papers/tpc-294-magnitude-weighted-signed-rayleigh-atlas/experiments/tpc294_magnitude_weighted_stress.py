#!/usr/bin/env python3
"""Adversarial exact tests for the TPC-294 weighted sign layer."""

from __future__ import annotations

import itertools
import sys
from fractions import Fraction


class Failure(RuntimeError):
    pass


def need(condition: bool, message: str) -> None:
    if type(condition) is not bool or not condition:
        raise Failure(message)


def gray_extrema(matrix: list[list[int]]) -> dict[str, object]:
    m = len(matrix)
    labels = [1] * m
    fields = [sum(matrix[i][j] for j in range(m) if j != i)
              for i in range(m)]
    value = sum(matrix[i][j] for i in range(m) for j in range(m))
    minimum = maximum = value
    minimum_label = maximum_label = tuple(labels)
    minimum_count = maximum_count = 1
    previous = 0
    for code in range(1, 1 << (m - 1)):
        current = code ^ (code >> 1)
        changed = current ^ previous
        vertex = changed.bit_length()
        old = labels[vertex]
        value -= 4 * old * fields[vertex]
        labels[vertex] = -old
        for other in range(m):
            if other != vertex:
                fields[other] -= 2 * old * matrix[other][vertex]
        previous = current
        candidate = tuple(labels)
        if value < minimum:
            minimum, minimum_label, minimum_count = value, candidate, 1
        elif value == minimum:
            minimum_count += 1
            minimum_label = min(minimum_label, candidate)
        if value > maximum:
            maximum, maximum_label, maximum_count = value, candidate, 1
        elif value == maximum:
            maximum_count += 1
            maximum_label = max(maximum_label, candidate)
    return {"minimum": minimum, "maximum": maximum,
            "minimum_label": minimum_label, "maximum_label": maximum_label,
            "minimum_count": minimum_count, "maximum_count": maximum_count}


def brute(matrix: list[list[int]]) -> dict[str, object]:
    values = []
    for tail in itertools.product((-1, 1), repeat=len(matrix) - 1):
        labels = (1,) + tail
        value = sum(labels[i] * labels[j] * matrix[i][j]
                    for i in range(len(matrix)) for j in range(len(matrix)))
        values.append((value, labels))
    low = min(value for value, _ in values)
    high = max(value for value, _ in values)
    return {"minimum": low, "maximum": high,
            "minimum_label": min(label for value, label in values
                                  if value == low),
            "maximum_label": max(label for value, label in values
                                  if value == high),
            "minimum_count": sum(value == low for value, _ in values),
            "maximum_count": sum(value == high for value, _ in values)}


def deterministic_matrix(m: int, seed: int) -> list[list[int]]:
    state = seed
    matrix = [[0] * m for _ in range(m)]
    for i in range(m):
        matrix[i][i] = 1 + ((seed + 3 * i) % 7)
        for j in range(i):
            state = (1664525 * state + 1013904223) % (2 ** 32)
            value = int(state % 19) - 9
            if value == 0:
                value = 1 if (i + j + seed) % 2 else -1
            matrix[i][j] = matrix[j][i] = value
    return matrix


def gram_matrix(m: int, seed: int) -> list[list[int]]:
    vectors = []
    state = seed
    for i in range(m):
        row = []
        for _ in range(4):
            state = (1103515245 * state + 12345) % (2 ** 31)
            row.append(int(state % 13) - 6)
        vectors.append(row)
    return [[sum(vectors[i][k] * vectors[j][k] for k in range(4))
             for j in range(m)] for i in range(m)]


def quotient(matrix: list[list[int]], labels: tuple[int, ...]) -> Fraction:
    trace = sum(matrix[i][i] for i in range(len(matrix)))
    need(trace > 0, "positive trace")
    return Fraction(sum(labels[i] * labels[j] * matrix[i][j]
                        for i in range(len(matrix))
                        for j in range(len(matrix))), trace)


def main() -> int:
    matrix_cases = 0
    for m in range(2, 9):
        for seed in range(1, 13):
            matrix = deterministic_matrix(m, seed)
            need(gray_extrema(matrix) == brute(matrix),
                 "Gray/brute mismatch m={} seed={}".format(m, seed))
            matrix_cases += 1

    psd_cases = 0
    for m in range(2, 9):
        for seed in range(7):
            matrix = gram_matrix(m, 17 + seed)
            for tail in itertools.product((-1, 1), repeat=m - 1):
                labels = (1,) + tail
                need(quotient(matrix, labels) >= 0,
                     "Gram quotient negativity")
            psd_cases += 1

    for m in range(3, 13):
        best = max(r * (m - r) for r in range(m + 1))
        need(best == m * m // 4, "all-positive max-cut formula")

    print("TPC294_STRESS=PASS gray_cases={} psd_cases={} "
          "all_positive_m=3..12".format(matrix_cases, psd_cases))
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except Failure as error:
        print("TPC294_STRESS=FAIL " + str(error), file=sys.stderr)
        raise SystemExit(1)
