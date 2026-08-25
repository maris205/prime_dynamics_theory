#!/usr/bin/env python3
"""Deterministic exact-rational stress for TPC-252 binary refinements."""

from __future__ import annotations

import argparse
import random
from fractions import Fraction


CASES = 192
Gaussian = tuple[Fraction, Fraction]
Vector = list[Gaussian]
Matrix = list[list[Gaussian]]
ZERO: Gaussian = (Fraction(0), Fraction(0))


def add_scalar(left: Gaussian, right: Gaussian) -> Gaussian:
    return (left[0] + right[0], left[1] + right[1])


def sub_scalar(left: Gaussian, right: Gaussian) -> Gaussian:
    return (left[0] - right[0], left[1] - right[1])


def mul(left: Gaussian, right: Gaussian) -> Gaussian:
    return (
        left[0] * right[0] - left[1] * right[1],
        left[0] * right[1] + left[1] * right[0],
    )


def conj(value: Gaussian) -> Gaussian:
    return (value[0], -value[1])


def vadd(*vectors: Vector) -> Vector:
    if not vectors:
        return []
    result: Vector = []
    for entries in zip(*vectors):
        total = ZERO
        for entry in entries:
            total = add_scalar(total, entry)
        result.append(total)
    return result


def vsub(left: Vector, right: Vector) -> Vector:
    return [sub_scalar(x, y) for x, y in zip(left, right)]


def scale(scalar: Gaussian, vector: Vector) -> Vector:
    return [mul(scalar, entry) for entry in vector]


def inner(left: Vector, right: Vector) -> Gaussian:
    total = ZERO
    for x, y in zip(left, right):
        total = add_scalar(total, mul(conj(x), y))
    return total


def norm2(vector: Vector) -> Fraction:
    value = inner(vector, vector)
    if value[1] != 0 or value[0] < 0:
        raise RuntimeError("invalid exact squared norm")
    return value[0]


def matvec(matrix: Matrix, vector: Vector) -> Vector:
    result: Vector = []
    for row in matrix:
        total = ZERO
        for coefficient, entry in zip(row, vector):
            total = add_scalar(total, mul(coefficient, entry))
        result.append(total)
    return result


def average_projection(vector: Vector, blocks: list[list[int]]) -> Vector:
    result = [ZERO for _ in vector]
    for block in blocks:
        total = ZERO
        for index in block:
            total = add_scalar(total, vector[index])
        mean = (total[0] / len(block), total[1] / len(block))
        for index in block:
            result[index] = mean
    return result


def residual(vector: Vector, blocks: list[list[int]]) -> Vector:
    return vsub(vector, average_projection(vector, blocks))


def restrict(vector: Vector, block: list[int]) -> Vector:
    return [vector[index] for index in block]


def rank_one(z: list[Fraction], vector: Vector) -> Vector:
    z_vector = [(entry, Fraction(0)) for entry in z]
    return scale(inner(z_vector, vector), z_vector)


def gram(vectors: list[Vector]) -> list[list[Gaussian]]:
    return [[inner(left, right) for right in vectors] for left in vectors]


def random_fraction(rng: random.Random) -> Fraction:
    return Fraction(rng.randint(-7, 7), rng.choice([1, 2, 3, 4, 5, 6, 7]))


def random_gaussian(rng: random.Random) -> Gaussian:
    return (random_fraction(rng), random_fraction(rng))


def check_partition(blocks: list[list[int]], dimension: int) -> None:
    if not blocks or any(not block for block in blocks):
        raise RuntimeError("empty partition or block")
    flat = [index for block in blocks for index in block]
    if sorted(flat) != list(range(dimension)) or len(set(flat)) != dimension:
        raise RuntimeError("partition is not disjoint and exhaustive")


def check_radius_monotonicity(
    w: Vector,
    g_vector: Vector,
    parent: list[int],
    child_one: list[int],
    child_two: list[int],
    z: list[Fraction],
    case_id: int,
) -> bool:
    old_w = residual(restrict(w, parent), [list(range(len(parent)))])
    old_g = residual(restrict(g_vector, parent), [list(range(len(parent)))])
    w_children = [
        residual(restrict(w, child), [list(range(len(child)))])
        for child in (child_one, child_two)
    ]
    g_children = [
        residual(restrict(g_vector, child), [list(range(len(child)))])
        for child in (child_one, child_two)
    ]
    z_vector = [(entry, Fraction(0)) for entry in z]
    alpha2 = norm2(rank_one(z, w))
    beta2 = norm2(rank_one(z, g_vector))
    x = [norm2(vector) for vector in w_children]
    y = [norm2(vector) for vector in g_children]
    old_x = norm2(old_w)
    old_y = norm2(old_g)
    if old_x != alpha2 + x[0] + x[1]:
        raise RuntimeError(f"case {case_id}: old w residual energy split failed")
    if old_y != beta2 + y[0] + y[1]:
        raise RuntimeError(f"case {case_id}: old g residual energy split failed")

    cross_budget = x[0] * y[1] + x[1] * y[0]
    cross_product = x[0] * x[1] * y[0] * y[1]
    if cross_budget < 0 or cross_budget * cross_budget < 4 * cross_product:
        raise RuntimeError(f"case {case_id}: exact two-child Cauchy audit failed")
    child_energy_product = (x[0] + x[1]) * (y[0] + y[1])
    old_energy_product = old_x * old_y
    if child_energy_product > old_energy_product:
        raise RuntimeError(f"case {case_id}: exact transverse radius monotonicity failed")
    return child_energy_product < old_energy_product or (
        cross_budget * cross_budget > 4 * cross_product
    )


def run_case(case_id: int) -> bool:
    rng = random.Random(252000 + case_id)
    dimension = 8
    permutation = list(range(dimension))
    rng.shuffle(permutation)
    coarse = [permutation[:4], permutation[4:]]
    split_index = case_id % 2
    parent = coarse[split_index]
    child_one = parent[:2]
    child_two = parent[2:]
    refined = [list(block) for block in coarse]
    refined[split_index:split_index + 1] = [child_one, child_two]
    check_partition(coarse, dimension)
    check_partition(refined, dimension)

    z = [Fraction(0) for _ in range(dimension)]
    for index in child_one:
        z[index] = Fraction(1, 2)
    for index in child_two:
        z[index] = Fraction(-1, 2)
    z_vector = [(entry, Fraction(0)) for entry in z]
    if norm2(z_vector) != 1 or sum(z[index] for index in parent) != 0:
        raise RuntimeError(f"case {case_id}: normalized contrast construction failed")

    matrix: Matrix = [
        [random_gaussian(rng) for _ in range(dimension)]
        for _ in range(dimension)
    ]
    beta = [random_gaussian(rng) for _ in range(dimension)]
    w = [random_gaussian(rng) for _ in range(dimension)]
    g_vector = matvec(matrix, beta)

    mw = average_projection(w, coarse)
    mg = average_projection(g_vector, coarse)
    mpw = average_projection(w, refined)
    mpg = average_projection(g_vector, refined)
    if vadd(mw, rank_one(z, w)) != mpw:
        raise RuntimeError(f"case {case_id}: M refinement update failed for w")
    if vadd(mg, rank_one(z, g_vector)) != mpg:
        raise RuntimeError(f"case {case_id}: M refinement update failed for g")

    moment_w = inner(z_vector, w)
    moment_g = inner(z_vector, g_vector)
    delta = mul(conj(moment_w), moment_g)
    c_coarse = inner(mw, mg)
    c_refined = inner(mpw, mpg)
    q_coarse = inner(residual(w, coarse), residual(g_vector, coarse))
    q_refined = inner(residual(w, refined), residual(g_vector, refined))
    scalar = inner(w, g_vector)
    if c_refined != add_scalar(c_coarse, delta):
        raise RuntimeError(f"case {case_id}: C_long update failed")
    if q_refined != sub_scalar(q_coarse, delta):
        raise RuntimeError(f"case {case_id}: Q_trans update failed")
    if scalar != add_scalar(c_coarse, q_coarse) or scalar != add_scalar(c_refined, q_refined):
        raise RuntimeError(f"case {case_id}: scalar decomposition failed")

    probes = [w, g_vector, matrix[case_id % dimension]]
    coarse_residuals = [residual(probe, coarse) for probe in probes]
    refined_residuals = [residual(probe, refined) for probe in probes]
    coarse_gram = gram(coarse_residuals)
    refined_gram = gram(refined_residuals)
    moments = [inner(z_vector, probe) for probe in probes]
    for i in range(len(probes)):
        for j in range(len(probes)):
            expected = sub_scalar(coarse_gram[i][j], mul(conj(moments[i]), moments[j]))
            if refined_gram[i][j] != expected:
                raise RuntimeError(f"case {case_id}: fixed-family Gram update failed")

    strict_radius_drop = check_radius_monotonicity(
        w, g_vector, parent, child_one, child_two, z, case_id
    )

    singleton = [[index] for index in range(dimension)]
    if average_projection(w, singleton) != w or average_projection(g_vector, singleton) != g_vector:
        raise RuntimeError(f"case {case_id}: singleton projection is not identity")
    if residual(w, singleton) != [ZERO] * dimension or residual(g_vector, singleton) != [ZERO] * dimension:
        raise RuntimeError(f"case {case_id}: singleton transverse vectors did not vanish")
    if inner(average_projection(w, singleton), average_projection(g_vector, singleton)) != scalar:
        raise RuntimeError(f"case {case_id}: singleton C_long does not equal C_x")
    return strict_radius_drop


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()
    if not args.check:
        parser.error("the stress suite is read-only; pass --check")
    strict_count = 0
    try:
        for case_id in range(CASES):
            if run_case(case_id):
                strict_count += 1
    except RuntimeError as error:
        print(f"FAIL {error}")
        return 1
    print(
        f"PASS exact_gaussian_rational_refinement_families={CASES} "
        f"strict_radius_drop_families={strict_count} fixed_probe_gram_families={CASES} "
        f"singleton_collapses={CASES} optimization_sensitive_assertions=0 "
        "evidence=FINITE_STRUCTURAL_STRESS_NOT_ASYMPTOTIC"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
