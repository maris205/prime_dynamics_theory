#!/usr/bin/env python3
"""Small exact adversarial tests for the TPC-292 triangle claims.

This test intentionally does not read the TPC-292 certificate.  It generates
deterministic integer-vector Gram matrices, enumerates every coefficient-sign
assignment, and checks both the triangle parity rule and the Schur residual
identity directly over ``Fraction``.  It is a sanity check for the algebra,
not evidence for an asymptotic prime theorem.
"""

from __future__ import annotations

import itertools
import sys
from fractions import Fraction

if hasattr(sys, "set_int_max_str_digits"):
    sys.set_int_max_str_digits(0)


class Failure(RuntimeError):
    pass


def need(condition: bool, message: str) -> None:
    if type(condition) is not bool or not condition:
        raise Failure(message)


def dot(left: tuple[int, ...], right: tuple[int, ...]) -> int:
    return sum(a * b for a, b in zip(left, right))


def determinant3(matrix: list[list[Fraction]]) -> Fraction:
    a, b, c = matrix[0]
    d, e, f = matrix[1]
    g, h, i = matrix[2]
    return a * (e * i - f * h) - b * (d * i - f * g) + c * (d * h - e * g)


def gram(vectors: list[tuple[int, ...]]) -> list[list[Fraction]]:
    return [[Fraction(dot(left, right)) for right in vectors]
            for left in vectors]


def sign(value: Fraction) -> int:
    return 1 if value > 0 else -1 if value < 0 else 0


def parity_prediction(sub: list[list[Fraction]]) -> bool:
    edges = (sign(sub[0][1]), sign(sub[0][2]), sign(sub[1][2]))
    need(all(edge != 0 for edge in edges), "stress vector has zero edge")
    return edges[0] * edges[1] * edges[2] == -1


def brute_force_anti_alignment(sub: list[list[Fraction]]) -> bool:
    edges = ((0, 1, sub[0][1]), (0, 2, sub[0][2]),
             (1, 2, sub[1][2]))
    for signs in itertools.product((-1, 1), repeat=3):
        if all(signs[i] * signs[j] * sign(edge) == -1
               for i, j, edge in edges):
            return True
    return False


def check_schur(sub: list[list[Fraction]]) -> None:
    for target in range(3):
        others = [index for index in range(3) if index != target]
        j, k = others
        d_i, d_j, d_k = sub[target][target], sub[j][j], sub[k][k]
        cross_jk = sub[j][k]
        minor = d_j * d_k - cross_jk * cross_jk
        need(minor > 0, "stress pair minor is not positive")
        alpha = (sub[target][j] * d_k - sub[target][k] * cross_jk) / minor
        beta = (sub[target][k] * d_j - sub[target][j] * cross_jk) / minor
        # The coefficient identity is checked using the Gram quadratic form.
        residual_direct = (d_i - 2 * alpha * sub[target][j]
                           - 2 * beta * sub[target][k]
                           + alpha * alpha * d_j + beta * beta * d_k
                           + 2 * alpha * beta * cross_jk) / d_i
        determinant = determinant3(sub)
        residual_schur = determinant / (d_i * minor)
        need(residual_direct == residual_schur, "Schur residual mismatch")
        need(residual_schur >= 0, "Gram residual is negative")


def main() -> int:
    # The vectors are fixed, small, and chosen to contain both positive and
    # negative edges while avoiding zero inner products.  Every triple is
    # checked; the duplicated-looking families test scale/sign robustness.
    bases = (
        (2, 1, 0, 0, 0), (1, -2, 1, 0, 0), (-1, 1, 2, 0, 0),
        (1, 1, -1, 2, 0), (-2, 1, 1, 1, 0), (1, -1, 2, 1, 1),
        (3, 1, 0, 1, -1), (-1, 2, 1, -1, 2), (2, -3, 1, 1, 1),
    )
    vectors: list[tuple[int, ...]] = []
    for scale in (1, 2, 3, 5):
        for index, vector in enumerate(bases):
            # A sign flip changes edge signs but preserves the Gram geometry;
            # include it to exercise both parity classes.
            multiplier = scale if index % 2 == 0 else -scale
            vectors.append(tuple(multiplier * value for value in vector))

    gram_cases = 0
    anti_cases = 0
    frustrated_cases = 0
    sign_assignments = 0
    schur_checks = 0
    full_gram = gram(vectors)
    for indices in itertools.combinations(range(len(vectors)), 3):
        sub = [[full_gram[i][j] for j in indices] for i in indices]
        edges = (sub[0][1], sub[0][2], sub[1][2])
        if any(value == 0 for value in edges):
            continue
        if any(sub[i][i] * sub[j][j] - sub[i][j] * sub[i][j] <= 0
               for i, j in ((0, 1), (0, 2), (1, 2))):
            # Proportional vectors have a singular two-vector projection
            # problem; they are outside the nondegenerate Schur test.
            continue
        predicted = parity_prediction(sub)
        actual = brute_force_anti_alignment(sub)
        need(predicted == actual, "triangle parity counterexample")
        if actual:
            anti_cases += 1
        else:
            frustrated_cases += 1
        for _ in itertools.product((-1, 1), repeat=3):
            sign_assignments += 1
        check_schur(sub)
        schur_checks += 3
        gram_cases += 1

    need(gram_cases > 100, "stress corpus unexpectedly small")
    need(anti_cases > 0 and frustrated_cases > 0,
         "stress corpus lacks both parity classes")
    print("TPC292_STRESS=PASS gram_cases={} anti_alignable={} "
          "frustrated={} sign_assignments={} schur_checks={}".format(
              gram_cases, anti_cases, frustrated_cases, sign_assignments,
              schur_checks))
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except (Failure, ValueError, TypeError) as error:
        print("TPC292_STRESS=FAIL " + str(error), file=sys.stderr)
        raise SystemExit(1)
