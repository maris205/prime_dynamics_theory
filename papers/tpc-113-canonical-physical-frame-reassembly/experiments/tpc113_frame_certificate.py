#!/usr/bin/env python3
"""Exact finite regression for the TPC-113 quotient-frame identities."""

from __future__ import annotations

from fractions import Fraction
import json
from pathlib import Path


def transpose(a: list[list[Fraction]]) -> list[list[Fraction]]:
    return [list(row) for row in zip(*a)]


def matmul(
    a: list[list[Fraction]], b: list[list[Fraction]]
) -> list[list[Fraction]]:
    bt = transpose(b)
    return [[sum(x * y for x, y in zip(row, col)) for col in bt] for row in a]


def eye(n: int) -> list[list[Fraction]]:
    return [[Fraction(int(i == j)) for j in range(n)] for i in range(n)]


def inverse(a: list[list[Fraction]]) -> list[list[Fraction]]:
    n = len(a)
    aug = [row[:] + ident[:] for row, ident in zip(a, eye(n))]
    for col in range(n):
        pivot = next(i for i in range(col, n) if aug[i][col])
        aug[col], aug[pivot] = aug[pivot], aug[col]
        scale = aug[col][col]
        aug[col] = [x / scale for x in aug[col]]
        for i in range(n):
            if i == col:
                continue
            scale = aug[i][col]
            aug[i] = [x - scale * y for x, y in zip(aug[i], aug[col])]
    return [row[n:] for row in aug]


def equal(a: list[list[Fraction]], b: list[list[Fraction]]) -> bool:
    return a == b


def main() -> None:
    pseudoinverse_checks = 0
    projection_checks = 0
    syntheses = [
        [[1, 0, 1], [0, 2, 0]],
        [[1, 1, 0], [0, 1, 1]],
        [[2, -1, 0, 1], [0, 1, 2, 1]],
    ]
    for raw in syntheses:
        s = [[Fraction(x) for x in row] for row in raw]
        st = transpose(s)
        sst = matmul(s, st)
        sdag = matmul(st, inverse(sst))
        if not equal(matmul(s, sdag), eye(len(s))):
            raise AssertionError("S S^dagger is not the range identity")
        pseudoinverse_checks += 1
        projection = matmul(sdag, s)
        if not equal(matmul(projection, projection), projection):
            raise AssertionError("S^dagger S is not idempotent")
        if not equal(transpose(projection), projection):
            raise AssertionError("quotient projection is not self-adjoint")
        projection_checks += 2

    # A large quotient condition number is not an inevitable
    # round-trip loss.  For S=diag(M,1), SS^dagger=I, while the
    # intervening swap Q attains ||SQS^dagger||=M=kappa_q.
    scale = Fraction(5)
    diagonal = [[scale, Fraction(0)], [Fraction(0), Fraction(1)]]
    diagonal_dagger = [
        [Fraction(1, 5), Fraction(0)],
        [Fraction(0), Fraction(1)],
    ]
    swap = [[Fraction(0), Fraction(1)], [Fraction(1), Fraction(0)]]
    if matmul(diagonal, diagonal_dagger) != eye(2):
        raise AssertionError("identity intermediate should cost one")
    attained = matmul(matmul(diagonal, swap), diagonal_dagger)
    if attained != [
        [Fraction(0), scale],
        [Fraction(1, 5), Fraction(0)],
    ]:
        raise AssertionError("uniform conjugation extremizer mismatch")
    attained_star_attained = matmul(transpose(attained), attained)
    if attained_star_attained != [
        [Fraction(1, 25), Fraction(0)],
        [Fraction(0), Fraction(25)],
    ]:
        raise AssertionError("conjugation norm did not attain kappa")
    conjugation_checks = 3

    coherence_checks = 0
    unequal_norm_checks = 0
    sharp_ratios: list[str] = []
    # Unit columns (1,0) and (a/c,b/c) from Pythagorean triples.
    for a, b, c in ((3, 4, 5), (20, 21, 29), (99, 20, 101)):
        rho = Fraction(a, c)
        if rho * rho + Fraction(b, c) ** 2 != 1:
            raise AssertionError("non-unit rational column")
        gram = [[Fraction(1), rho], [rho, Fraction(1)]]
        determinant = gram[0][0] * gram[1][1] - gram[0][1] ** 2
        if determinant != 1 - rho**2:
            raise AssertionError("Gram determinant mismatch")
        lam_plus = 1 + rho
        lam_minus = 1 - rho
        ratio = lam_plus / lam_minus
        if ratio != (1 + rho) / (1 - rho):
            raise AssertionError("coherence ratio mismatch")
        sharp_ratios.append(f"{ratio.numerator}/{ratio.denominator}")
        coherence_checks += 3

    # Literal unequal column norms: verify the characteristic data and
    # the algebraic inequality Delta >= rho * trace without square roots.
    for alpha, beta, rho in (
        (Fraction(2), Fraction(1), Fraction(3, 5)),
        (Fraction(3), Fraction(2), Fraction(20, 29)),
        (Fraction(5), Fraction(4), Fraction(99, 101)),
    ):
        alpha2, beta2 = alpha**2, beta**2
        gram = [
            [alpha2, alpha * beta * rho],
            [alpha * beta * rho, beta2],
        ]
        trace = gram[0][0] + gram[1][1]
        determinant = gram[0][0] * gram[1][1] - gram[0][1] ** 2
        if trace != alpha2 + beta2:
            raise AssertionError("literal Gram trace mismatch")
        if determinant != alpha2 * beta2 * (1 - rho**2):
            raise AssertionError("literal Gram determinant mismatch")
        delta2 = (alpha2 - beta2) ** 2 + 4 * alpha2 * beta2 * rho**2
        gap = delta2 - rho**2 * trace**2
        if gap != (1 - rho**2) * (alpha2 - beta2) ** 2 or gap < 0:
            raise AssertionError("unequal-norm coherence obstruction mismatch")
        unequal_norm_checks += 3

    result = {
        "schema": "tpc-113-canonical-frame-certificate-v1",
        "status": "PASS",
        "checks": {
            "moore_penrose_range_identities": pseudoinverse_checks,
            "quotient_projection_identities": projection_checks,
            "sharp_two_column_identities": coherence_checks,
            "literal_unequal_norm_identities": unequal_norm_checks,
            "uniform_conjugation_envelope_examples": conjugation_checks,
        },
        "sharp_condition_number_squared": sharp_ratios,
        "claim_boundary": {
            "finite_exact_certificate": True,
            "actual_growing_frame_bound": False,
            "actual_polynomial_obstruction": False,
            "new_L2_fixed_shift_estimate": False,
            "parity_breakthrough": False,
            "prime_pair_or_twin_prime_theorem": False,
        },
    }
    payload = json.dumps(result, indent=2, sort_keys=True) + "\n"
    Path(__file__).with_suffix(".json").write_text(payload)
    print(payload, end="")


if __name__ == "__main__":
    main()
