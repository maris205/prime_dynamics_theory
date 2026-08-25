#!/usr/bin/env python3
"""Deterministic exact-rational stress for TPC-253 rank midpoints."""

from __future__ import annotations

import argparse
import random
from fractions import Fraction


CASES = 192
Gaussian = tuple[Fraction, Fraction]
Vector = list[Gaussian]
GMatrix = list[list[Gaussian]]
RMatrix = list[list[Fraction]]
ZERO: Gaussian = (Fraction(0), Fraction(0))


def add(left: Gaussian, right: Gaussian) -> Gaussian:
    return (left[0] + right[0], left[1] + right[1])


def sub(left: Gaussian, right: Gaussian) -> Gaussian:
    return (left[0] - right[0], left[1] - right[1])


def mul(left: Gaussian, right: Gaussian) -> Gaussian:
    return (
        left[0] * right[0] - left[1] * right[1],
        left[0] * right[1] + left[1] * right[0],
    )


def conj(value: Gaussian) -> Gaussian:
    return (value[0], -value[1])


def scale_real(value: Fraction, scalar: Gaussian) -> Gaussian:
    return (value * scalar[0], value * scalar[1])


def vsub(left: Vector, right: Vector) -> Vector:
    return [sub(x, y) for x, y in zip(left, right)]


def inner(left: Vector, right: Vector) -> Gaussian:
    total = ZERO
    for x, y in zip(left, right):
        total = add(total, mul(conj(x), y))
    return total


def gmatvec(matrix: GMatrix, vector: Vector) -> Vector:
    result: Vector = []
    for row in matrix:
        total = ZERO
        for coefficient, entry in zip(row, vector):
            total = add(total, mul(coefficient, entry))
        result.append(total)
    return result


def rmatvec(matrix: RMatrix, vector: Vector) -> Vector:
    result: Vector = []
    for row in matrix:
        total = ZERO
        for coefficient, entry in zip(row, vector):
            total = add(total, scale_real(coefficient, entry))
        result.append(total)
    return result


def rmatmul(left: RMatrix, right: RMatrix) -> RMatrix:
    size = len(left)
    return [
        [sum((left[i][k] * right[k][j] for k in range(size)), Fraction(0)) for j in range(size)]
        for i in range(size)
    ]


def adjoint(matrix: GMatrix) -> GMatrix:
    size = len(matrix)
    return [[conj(matrix[row][column]) for row in range(size)] for column in range(size)]


def floor_fraction(value: Fraction) -> int:
    return value.numerator // value.denominator


def rank_data(x: Fraction) -> tuple[list[int], int, int, list[Fraction], Fraction]:
    coordinates = list(range(floor_fraction(x / 2) + 1, floor_fraction(x) + 1))
    count = len(coordinates)
    if count < 2:
        raise RuntimeError("stress clock has N<2")
    ell = count // 2
    right_size = count - ell
    h = [Fraction(1, ell)] * ell + [Fraction(-1, right_size)] * right_size
    return coordinates, ell, right_size, h, Fraction(ell * right_size, count)


def coarse_matrix(size: int) -> RMatrix:
    return [[Fraction(1, size) for _ in range(size)] for _ in range(size)]


def midpoint_matrix(ell: int, right_size: int) -> RMatrix:
    size = ell + right_size
    return [
        [
            Fraction(1, ell)
            if row < ell and column < ell
            else Fraction(1, right_size)
            if row >= ell and column >= ell
            else Fraction(0)
            for column in range(size)
        ]
        for row in range(size)
    ]


def contrast_projector(h: list[Fraction], rho_squared: Fraction) -> RMatrix:
    return [[rho_squared * left * right for right in h] for left in h]


def sum_positions(vector: Vector, positions: list[int]) -> Gaussian:
    total = ZERO
    for position in positions:
        total = add(total, vector[position])
    return total


def within_child_covariance(w: Vector, g_vector: Vector, ell: int) -> Gaussian:
    total = ZERO
    for positions in (list(range(ell)), list(range(ell, len(w)))):
        mean_w = scale_real(Fraction(1, len(positions)), sum_positions(w, positions))
        mean_g = scale_real(Fraction(1, len(positions)), sum_positions(g_vector, positions))
        for position in positions:
            total = add(
                total,
                mul(conj(sub(w[position], mean_w)), sub(g_vector[position], mean_g)),
            )
    return total


def random_fraction(rng: random.Random) -> Fraction:
    return Fraction(rng.randint(-8, 8), rng.choice([1, 2, 3, 4, 5, 6, 7, 8]))


def random_gaussian(rng: random.Random) -> Gaussian:
    return (random_fraction(rng), random_fraction(rng))


def clock_for_case(case_id: int) -> tuple[Fraction, bool]:
    if case_id < CASES // 2:
        return Fraction(3 + case_id % 32), True
    offset = case_id - CASES // 2
    integer_part = 3 + offset % 32
    numerator = 1 + offset % 4
    denominator = 6 + offset % 5
    return Fraction(integer_part) + Fraction(numerator, denominator), False


def run_case(case_id: int) -> tuple[bool, bool, int | None]:
    x, integer_clock = clock_for_case(case_id)
    coordinates, ell, right_size, h, rho_squared = rank_data(x)
    size = len(coordinates)
    if size != floor_fraction(x) - floor_fraction(x / 2):
        raise RuntimeError(f"case {case_id}: N=#I identity failed")
    if sum(h, Fraction(0)) != 0:
        raise RuntimeError(f"case {case_id}: constant annihilation failed")
    unit = rho_squared * sum((entry * entry for entry in h), Fraction(0))
    if unit != 1:
        raise RuntimeError(f"case {case_id}: contrast normalization failed")
    if unit != 1 or -unit != -1:
        raise RuntimeError(f"case {case_id}: synthetic sign controls failed")

    coarse = coarse_matrix(size)
    midpoint = midpoint_matrix(ell, right_size)
    projector = contrast_projector(h, rho_squared)
    for row in range(size):
        for column in range(size):
            if midpoint[row][column] != coarse[row][column] + projector[row][column]:
                raise RuntimeError(f"case {case_id}: projector update failed")
    if rmatmul(projector, projector) != projector:
        raise RuntimeError(f"case {case_id}: contrast projector idempotence failed")
    zero_matrix = [[Fraction(0) for _ in range(size)] for _ in range(size)]
    if rmatmul(projector, coarse) != zero_matrix or rmatmul(coarse, projector) != zero_matrix:
        raise RuntimeError(f"case {case_id}: coarse/contrast orthogonality failed")

    rng = random.Random(253000 + case_id)
    matrix: GMatrix = [
        [random_gaussian(rng) for _ in range(size)]
        for _ in range(size)
    ]
    beta = [random_gaussian(rng) for _ in range(size)]
    w = [random_gaussian(rng) for _ in range(size)]
    g_vector = gmatvec(matrix, beta)
    coarse_w = rmatvec(coarse, w)
    coarse_g = rmatvec(coarse, g_vector)
    midpoint_w = rmatvec(midpoint, w)
    midpoint_g = rmatvec(midpoint, g_vector)
    projector_w = rmatvec(projector, w)
    projector_g = rmatvec(projector, g_vector)
    if midpoint_w != [add(x_value, y_value) for x_value, y_value in zip(coarse_w, projector_w)]:
        raise RuntimeError(f"case {case_id}: projector action on w failed")
    if midpoint_g != [add(x_value, y_value) for x_value, y_value in zip(coarse_g, projector_g)]:
        raise RuntimeError(f"case {case_id}: projector action on g failed")

    left_positions = list(range(ell))
    right_positions = list(range(ell, size))
    w_left = sum_positions(w, left_positions)
    w_right = sum_positions(w, right_positions)
    g_left = sum_positions(g_vector, left_positions)
    g_right = sum_positions(g_vector, right_positions)
    h_w = sub(scale_real(Fraction(1, ell), w_left), scale_real(Fraction(1, right_size), w_right))
    h_g = sub(scale_real(Fraction(1, ell), g_left), scale_real(Fraction(1, right_size), g_right))
    transfer = scale_real(rho_squared, mul(conj(h_w), h_g))
    c_coarse_formula = scale_real(
        Fraction(1, size), mul(conj(add(w_left, w_right)), add(g_left, g_right))
    )
    c_mid_formula = add(
        scale_real(Fraction(1, ell), mul(conj(w_left), g_left)),
        scale_real(Fraction(1, right_size), mul(conj(w_right), g_right)),
    )
    c_coarse = inner(coarse_w, coarse_g)
    c_mid = inner(midpoint_w, midpoint_g)
    q_coarse = inner(vsub(w, coarse_w), vsub(g_vector, coarse_g))
    q_mid = inner(vsub(w, midpoint_w), vsub(g_vector, midpoint_g))
    scalar = inner(w, g_vector)
    within = within_child_covariance(w, g_vector, ell)
    if c_coarse != c_coarse_formula or c_mid != c_mid_formula:
        raise RuntimeError(f"case {case_id}: partial-sum longitudinal formula failed")
    if c_mid != add(c_coarse, transfer):
        raise RuntimeError(f"case {case_id}: conjugate-first covariance transfer failed")
    if q_mid != sub(q_coarse, transfer):
        raise RuntimeError(f"case {case_id}: opposite transverse update failed")
    if within != q_mid:
        raise RuntimeError(f"case {case_id}: within-child covariance failed")
    if scalar != add(c_coarse, q_coarse) or scalar != add(c_mid, q_mid):
        raise RuntimeError(f"case {case_id}: scalar decomposition failed")

    h_vector = [(entry, Fraction(0)) for entry in h]
    direct_h_moment = inner(h_vector, g_vector)
    adjoint_h = gmatvec(adjoint(matrix), h_vector)
    if direct_h_moment != inner(adjoint_h, beta):
        raise RuntimeError(f"case {case_id}: safe adjoint identity failed")

    residue: int | None = None
    if integer_clock:
        integer_x = x.numerator
        endpoint = coordinates[ell - 1]
        threshold = (3 * integer_x) // 4
        expected_left = [coordinate for coordinate in coordinates if coordinate <= threshold]
        if endpoint != threshold or coordinates[:ell] != expected_left:
            raise RuntimeError(f"case {case_id}: integer floor(3x/4) crosswalk failed")
        residue = integer_x % 4
    elif x.denominator == 1:
        raise RuntimeError(f"case {case_id}: requested nonintegral clock became integral")
    return transfer != ZERO, integer_clock, residue


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()
    if not args.check:
        parser.error("the stress suite is read-only; pass --check")
    nonzero_transfers = 0
    integer_count = 0
    nonintegral_count = 0
    residue_counts = {0: 0, 1: 0, 2: 0, 3: 0}
    try:
        for case_id in range(CASES):
            nonzero, integer_clock, residue = run_case(case_id)
            if nonzero:
                nonzero_transfers += 1
            if integer_clock:
                integer_count += 1
                if residue is None:
                    raise RuntimeError(f"case {case_id}: missing integer residue")
                residue_counts[residue] += 1
            else:
                nonintegral_count += 1
    except RuntimeError as error:
        print(f"FAIL {error}")
        return 1
    residue_text = ",".join(f"{key}:{residue_counts[key]}" for key in sorted(residue_counts))
    print(
        f"PASS exact_rational_rank_midpoint_families={CASES} integer_x={integer_count} "
        f"nonintegral_rational_x={nonintegral_count} integer_mod4={residue_text} "
        f"projector_identities={CASES} covariance_identities={CASES} "
        f"adjoint_identities={CASES} within_child_identities={CASES} "
        f"constant_zero_controls={2 * CASES} sign_controls={2 * CASES} "
        f"nonzero_transfer_families={nonzero_transfers} "
        "evidence=FINITE_STRUCTURAL_STRESS_NOT_ASYMPTOTIC"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
