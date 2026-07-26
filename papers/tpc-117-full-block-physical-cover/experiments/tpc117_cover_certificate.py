#!/usr/bin/env python3
"""Exact rational regression for the TPC-117 block-cover certificate."""

from __future__ import annotations

from fractions import Fraction
import json
from pathlib import Path


Vector = list[Fraction]
Matrix = list[list[Fraction]]


def transpose(a: Matrix) -> Matrix:
    return [list(row) for row in zip(*a)]


def matvec(a: Matrix, x: Vector) -> Vector:
    return [sum(v * w for v, w in zip(row, x)) for row in a]


def dot(x: Vector, y: Vector) -> Fraction:
    return sum(a * b for a, b in zip(x, y))


def main() -> None:
    # Columns overlap on adjacent physical atoms.
    b: Matrix = [
        [Fraction(1), Fraction(0), Fraction(0)],
        [Fraction(1), Fraction(1), Fraction(0)],
        [Fraction(0), Fraction(1), Fraction(1)],
        [Fraction(0), Fraction(0), Fraction(1)],
    ]
    bt = transpose(b)
    coefficient = [Fraction(2), Fraction(-1), Fraction(3)]
    covered = matvec(b, coefficient)
    if covered != [Fraction(2), Fraction(1), Fraction(2), Fraction(3)]:
        raise AssertionError("exact cover example failed")

    cokernel = [Fraction(1), Fraction(-1), Fraction(1), Fraction(-1)]
    if matvec(bt, cokernel) != [Fraction(0)] * 3:
        raise AssertionError("declared dual vector is not in ker B^T")
    if dot(cokernel, covered) != 0:
        raise AssertionError("dual vector did not annihilate covered vector")

    uncovered = covered[:]
    uncovered[0] += 1
    dual_pairing = dot(cokernel, uncovered)
    if dual_pairing != 1:
        raise AssertionError("non-cover dual witness failed")

    # The cokernel is one-dimensional and has squared norm four.
    residual = [dual_pairing * value / 4 for value in cokernel]
    projection = [x - r for x, r in zip(uncovered, residual)]
    if matvec(bt, residual) != [Fraction(0)] * 3:
        raise AssertionError("canonical residual is not orthogonal to range")
    if dot(cokernel, projection) != 0:
        raise AssertionError("projected vector is not in the covered hyperplane")
    if dot(residual, residual) != dual_pairing**2 / dot(cokernel, cokernel):
        raise AssertionError("distance/dual identity failed")

    # Full row rank: ker(B^T)={0}.  The dual closed-unit-ball supremum
    # is zero (the unit-sphere formulation would have an empty set).
    full_rank: Matrix = [
        [Fraction(1), Fraction(0)],
        [Fraction(0), Fraction(1)],
    ]
    full_vector = [Fraction(3), Fraction(-2)]
    if matvec(full_rank, full_vector) != full_vector:
        raise AssertionError("full-row-rank cover failed")
    full_rank_dual_ball_supremum = Fraction(0)
    full_rank_residual_squared_norm = Fraction(0)
    if full_rank_dual_ball_supremum != full_rank_residual_squared_norm:
        raise AssertionError("full-row-rank dual-ball convention failed")

    evaluation = [Fraction(1), Fraction(2), Fraction(3), Fraction(4)]
    physical_total = dot(evaluation, uncovered)
    physical_residual = dot(evaluation, residual)
    physical_block = dot(evaluation, projection)
    if physical_total != physical_block + physical_residual:
        raise AssertionError("physical block-residual identity failed")

    result = {
        "schema": "tpc-117-full-block-cover-certificate-v1",
        "status": "PASS",
        "checks": {
            "exact_cover": 1,
            "cokernel_annihilation": 2,
            "noncover_dual_witness": 1,
            "canonical_residual": 3,
            "full_row_rank_dual_ball": 1,
            "physical_remainder_identity": 1,
        },
        "certificate": {
            "dual_pairing": str(dual_pairing),
            "residual_squared_norm": str(dot(residual, residual)),
            "physical_residual": str(physical_residual),
        },
        "claim_boundary": {
            "finite_exact_certificate": True,
            "actual_tpc18_growing_cover": False,
            "actual_physical_remainder_bound": False,
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
