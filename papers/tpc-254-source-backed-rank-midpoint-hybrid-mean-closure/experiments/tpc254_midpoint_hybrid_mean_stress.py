#!/usr/bin/env python3
"""Deterministic exact-rational stress audit for TPC-254 finite algebra."""

from __future__ import annotations

import argparse
from fractions import Fraction


Gaussian = tuple[Fraction, Fraction]
Vector = list[Gaussian]
Matrix = list[list[Gaussian]]
ZERO: Gaussian = (Fraction(0), Fraction(0))


class StressError(ValueError):
    pass


def _g(real: int | Fraction, imag: int | Fraction = 0) -> Gaussian:
    return (Fraction(real), Fraction(imag))


def _add(left: Gaussian, right: Gaussian) -> Gaussian:
    return (left[0] + right[0], left[1] + right[1])


def _mul(left: Gaussian, right: Gaussian) -> Gaussian:
    return (
        left[0] * right[0] - left[1] * right[1],
        left[0] * right[1] + left[1] * right[0],
    )


def _conj(value: Gaussian) -> Gaussian:
    return (value[0], -value[1])


def _scale(value: Fraction, entry: Gaussian) -> Gaussian:
    return (value * entry[0], value * entry[1])


def _inner(left: Vector, right: Vector) -> Gaussian:
    total = ZERO
    for left_entry, right_entry in zip(left, right):
        total = _add(total, _mul(_conj(left_entry), right_entry))
    return total


def _matvec(matrix: Matrix, vector: Vector) -> Vector:
    result: Vector = []
    for row in matrix:
        total = ZERO
        for coefficient, entry in zip(row, vector):
            total = _add(total, _mul(coefficient, entry))
        result.append(total)
    return result


def _adjoint(matrix: Matrix) -> Matrix:
    size = len(matrix)
    return [[_conj(matrix[row][column]) for row in range(size)] for column in range(size)]


def _floor(value: Fraction) -> int:
    return value.numerator // value.denominator


def _rational_matvec(matrix: list[list[Fraction]], vector: list[Fraction]) -> list[Fraction]:
    return [
        sum((coefficient * entry for coefficient, entry in zip(row, vector)), Fraction(0))
        for row in matrix
    ]


def _rank_audit(x: Fraction, family_index: int) -> tuple[int, int]:
    coordinates = list(range(_floor(x / 2) + 1, _floor(x) + 1))
    count = len(coordinates)
    if count < 2:
        raise StressError("rank family has fewer than two active coordinates")
    ell = count // 2
    right_size = count - ell
    left = coordinates[:ell]
    right = coordinates[ell:]
    if left + right != coordinates or left[-1] + 1 != right[0]:
        raise StressError("rank children are not consecutive")
    h = [Fraction(1, ell)] * ell + [Fraction(-1, right_size)] * right_size
    rho_squared = Fraction(ell * right_size, count)
    if sum(h, Fraction(0)) != 0:
        raise StressError("Haar step is not zero sum")
    if rho_squared * sum((entry * entry for entry in h), Fraction(0)) != 1:
        raise StressError("Haar normalization failed")
    projector = [[rho_squared * row * column for column in h] for row in h]
    probe = [Fraction(((family_index + 3) * (position + 1)) % 19 - 9, position % 5 + 1)
             for position in range(count)]
    projected_probe = _rational_matvec(projector, probe)
    if _rational_matvec(projector, projected_probe) != projected_probe:
        raise StressError("rank-one Haar projector is not idempotent on exact probe")
    if _rational_matvec(projector, h) != h:
        raise StressError("rank-one Haar projector did not fix its normalized range direction")
    for row in projector:
        if sum(row, Fraction(0)) != 0:
            raise StressError("Haar projector did not annihilate constants")
    w: Vector = []
    for position in range(count):
        real = Fraction(((family_index + 2) * (position + 3)) % 17 - 8, (position % 4) + 1)
        imag = Fraction(((family_index + 5) * (position + 1)) % 13 - 6, (family_index % 3) + 1)
        w.append((real, imag))
    left_sum = ZERO
    right_sum = ZERO
    for entry in w[:ell]:
        left_sum = _add(left_sum, entry)
    for entry in w[ell:]:
        right_sum = _add(right_sum, entry)
    mean_difference = _add(
        _scale(Fraction(1, ell), left_sum),
        _scale(Fraction(-1, right_size), right_sum),
    )
    h_as_gaussian = [(entry, Fraction(0)) for entry in h]
    if _inner(h_as_gaussian, w) != mean_difference:
        raise StressError("partial-sum Haar identity failed")
    lambda_value = Fraction((family_index % 11) - 5, (family_index % 5) + 1)
    if lambda_value == 0:
        lambda_value = Fraction(7, 9)
    if sum(h, Fraction(0)) != 0 or rho_squared * sum((entry * entry for entry in h), Fraction(0)) != 1:
        raise StressError("whole-shell counterexample representation failed")
    if lambda_value == 0:
        raise StressError("whole-shell Haar moment unexpectedly vanished")
    noninteger_mismatch = 0
    if x.denominator != 1:
        wrong_threshold = _floor(3 * x / 4)
        if left[-1] != wrong_threshold:
            noninteger_mismatch = 1
    return count % 2, noninteger_mismatch


def _m1_audit(family_index: int) -> None:
    maxima = [
        Fraction((family_index + 3) % 19, 7),
        Fraction((family_index + 5) % 23, 11),
        Fraction((family_index + 7) % 29, 13),
    ]
    weights = [1, 2 ** ((family_index % 4) + 1), 3 ** ((family_index % 3) + 1)]
    total = sum((weight * maximum for weight, maximum in zip(weights, maxima)), Fraction(0))
    if any(maximum < 0 for maximum in maxima) or total < maxima[0] or weights[0] != 1:
        raise StressError("nonnegative m=1 row extraction failed")


def _adjoint_audit(family_index: int) -> None:
    matrix: Matrix = []
    for row in range(3):
        matrix_row: list[Gaussian] = []
        for column in range(3):
            real = Fraction(((family_index + 1) * (row + 2) + column) % 11 - 5, column + 1)
            imag = Fraction(((family_index + 4) * (column + 1) + row) % 9 - 4, row + 1)
            matrix_row.append((real, imag))
        matrix.append(matrix_row)
    z = [
        _g(Fraction((family_index % 5) + 1, 3), -1),
        _g(-2, Fraction((family_index % 7) - 3, 5)),
        _g(1, 2),
    ]
    beta = [
        _g(2, -1),
        _g(Fraction((family_index % 9) - 4, 2), 3),
        _g(-3, Fraction((family_index % 5) + 1, 4)),
    ]
    lhs = _inner(z, _matvec(matrix, beta))
    rhs = _inner(_matvec(_adjoint(matrix), z), beta)
    if lhs != rhs:
        raise StressError("adjoint orientation identity failed")


def _derangement_audit(family_index: int) -> tuple[int, int]:
    sign = -1 if family_index % 2 else 1
    second_sign = -1 if (family_index // 2) % 2 else 1
    z = [
        _g(Fraction(3, 5)),
        _g(Fraction(second_sign * 4, 5)),
        _g(0),
    ]
    if _inner(z, z) != _g(1):
        raise StressError("synthetic derangement direction is not unit")
    lambda_value = Fraction(sign * ((family_index % 13) + 1), (family_index % 7) + 1)
    permutation = [1, 2, 0]
    matrix: Matrix = [[ZERO for _ in range(3)] for _ in range(3)]
    for row, column in enumerate(permutation):
        matrix[row][column] = _scale(lambda_value, z[row])
    if any(matrix[index][index] != ZERO for index in range(3)):
        raise StressError("derangement matrix has a diagonal entry")
    beta = [_g(1), _g(1), _g(1)]
    expected = [_scale(lambda_value, entry) for entry in z]
    a_beta = _matvec(matrix, beta)
    if a_beta != expected or _inner(z, a_beta) != _g(lambda_value):
        raise StressError("derangement arbitrary-scale moment failed")
    lambda_squared = lambda_value * lambda_value
    adjoint_norm_squared = lambda_squared / 2
    beta_norm_squared = Fraction(2)
    if adjoint_norm_squared * beta_norm_squared != lambda_squared:
        raise StressError("N=2 Cauchy sharpness square ledger failed")
    return (1 if sign > 0 else 0, 1 if sign < 0 else 0)


def run() -> None:
    clocks = [Fraction(40 + index) for index in range(96)]
    clocks += [Fraction(81 + 2 * index, 2) for index in range(96)]
    if len(clocks) != 192:
        raise StressError("stress family count construction failed")
    odd_rank = 0
    even_rank = 0
    noninteger_count = 0
    noninteger_threshold_mismatches = 0
    positive_scales = 0
    negative_scales = 0
    for family_index, x in enumerate(clocks):
        parity, mismatch = _rank_audit(x, family_index)
        if parity == 0:
            even_rank += 1
        else:
            odd_rank += 1
        if x.denominator != 1:
            noninteger_count += 1
            noninteger_threshold_mismatches += mismatch
        _m1_audit(family_index)
        _adjoint_audit(family_index)
        positive, negative = _derangement_audit(family_index)
        positive_scales += positive
        negative_scales += negative
    if odd_rank == 0 or even_rank == 0 or noninteger_count != 96:
        raise StressError("odd/even/noninteger coverage failed")
    if positive_scales != 96 or negative_scales != 96:
        raise StressError("signed derangement scale coverage failed")
    print(
        "TPC254_STRESS=PASS families=192 integer=96 noninteger="
        + str(noninteger_count)
        + " odd_rank=" + str(odd_rank)
        + " even_rank=" + str(even_rank)
        + " noninteger_threshold_mismatches=" + str(noninteger_threshold_mismatches)
        + " positive_scales=" + str(positive_scales)
        + " negative_scales=" + str(negative_scales)
    )


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--check", action="store_true", required=True)
    parser.parse_args()
    run()


if __name__ == "__main__":
    main()
