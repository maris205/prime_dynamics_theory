#!/usr/bin/env python3
"""Exact finite tests for TPC-125 shift intertwining and localization."""

from __future__ import annotations

import argparse
import json
from fractions import Fraction
from pathlib import Path

Vector = tuple[Fraction, ...]
Matrix = tuple[tuple[Fraction, ...], ...]


def transpose(matrix: Matrix) -> Matrix:
    return tuple(tuple(matrix[i][j] for i in range(len(matrix))) for j in range(len(matrix[0])))


def matmul(left: Matrix, right: Matrix) -> Matrix:
    return tuple(
        tuple(
            sum(
                (left[i][k] * right[k][j] for k in range(len(right))),
                Fraction(0),
            )
            for j in range(len(right[0]))
        )
        for i in range(len(left))
    )


def apply(matrix: Matrix, vector: Vector) -> Vector:
    return tuple(
        sum((matrix[i][j] * vector[j] for j in range(len(vector))), Fraction(0))
        for i in range(len(matrix))
    )


def add(left: Matrix, right: Matrix) -> Matrix:
    return tuple(
        tuple(left[i][j] + right[i][j] for j in range(len(left[0])))
        for i in range(len(left))
    )


def sub(left: Matrix, right: Matrix) -> Matrix:
    return tuple(
        tuple(left[i][j] - right[i][j] for j in range(len(left[0])))
        for i in range(len(left))
    )


def dot(left: Vector, right: Vector) -> Fraction:
    return sum((a * b for a, b in zip(left, right)), Fraction(0))


def certificate() -> dict[str, object]:
    checks = 0

    selector: Matrix = (
        (Fraction(1), Fraction(0), Fraction(0), Fraction(0)),
        (Fraction(0), Fraction(1), Fraction(0), Fraction(0)),
    )
    t1: Matrix = (
        (Fraction(2), Fraction(0), Fraction(0), Fraction(0)),
        (Fraction(0), Fraction(1), Fraction(0), Fraction(0)),
        (Fraction(0), Fraction(0), Fraction(3), Fraction(0)),
        (Fraction(0), Fraction(0), Fraction(0), Fraction(4)),
    )
    t1_fixed: Matrix = (
        (Fraction(2), Fraction(0)),
        (Fraction(0), Fraction(1)),
    )
    t2: Matrix = (
        (Fraction(1), Fraction(1), Fraction(0), Fraction(0)),
        (Fraction(0), Fraction(1), Fraction(0), Fraction(0)),
        (Fraction(0), Fraction(0), Fraction(2), Fraction(0)),
        (Fraction(0), Fraction(0), Fraction(0), Fraction(1)),
    )
    t2_fixed: Matrix = (
        (Fraction(1), Fraction(1)),
        (Fraction(0), Fraction(1)),
    )

    d1 = sub(matmul(selector, t1), matmul(t1_fixed, selector))
    d2 = sub(matmul(selector, t2), matmul(t2_fixed, selector))
    zero_2x4: Matrix = (
        (Fraction(0),) * 4,
        (Fraction(0),) * 4,
    )
    assert d1 == zero_2x4
    assert d2 == zero_2x4
    checks += 2

    full_defect = sub(
        matmul(selector, matmul(t2, t1)),
        matmul(matmul(t2_fixed, t1_fixed), selector),
    )
    telescoped = add(matmul(d2, t1), matmul(t2_fixed, d1))
    assert full_defect == telescoped == zero_2x4
    checks += 1

    # Introduce cross-shift leakage into the selected target rows.
    t2_bad: Matrix = (
        (Fraction(1), Fraction(1), Fraction(1), Fraction(0)),
        (Fraction(0), Fraction(1), Fraction(0), Fraction(0)),
        (Fraction(0), Fraction(0), Fraction(2), Fraction(0)),
        (Fraction(0), Fraction(0), Fraction(0), Fraction(1)),
    )
    d2_bad = sub(matmul(selector, t2_bad), matmul(t2_fixed, selector))
    bad_defect = sub(
        matmul(selector, matmul(t2_bad, t1)),
        matmul(matmul(t2_fixed, t1_fixed), selector),
    )
    bad_telescoped = add(matmul(d2_bad, t1), matmul(t2_fixed, d1))
    assert bad_defect == bad_telescoped
    checks += 1
    literal_coefficient: Vector = (
        Fraction(1),
        Fraction(-1),
        Fraction(2),
        Fraction(0),
    )
    assert apply(bad_defect, literal_coefficient) != (Fraction(0), Fraction(0))
    checks += 1

    # Finite localization: observe only the first profile coordinate.
    observation: Matrix = ((Fraction(1), Fraction(0)),)
    gram = matmul(transpose(observation), observation)
    assert gram == (
        (Fraction(1), Fraction(0)),
        (Fraction(0), Fraction(0)),
    )
    checks += 1
    b_good: Vector = (Fraction(1), Fraction(0))
    b_bad: Vector = (Fraction(0), Fraction(1))
    gram_dagger = gram
    k_good = dot(b_good, apply(gram_dagger, b_good))
    assert k_good == Fraction(1)
    checks += 1
    kernel_witness: Vector = (Fraction(0), Fraction(1))
    assert apply(observation, kernel_witness) == (Fraction(0),)
    assert dot(b_bad, kernel_witness) == Fraction(1)
    checks += 2

    sigma = Fraction(1, 100)
    lambda_loc = Fraction(1, 500)
    fixed_saving = sigma - lambda_loc
    assert fixed_saving == Fraction(1, 125)
    assert fixed_saving > 0
    checks += 2

    return {
        "schema": "tpc125-prescribed-shift-intertwining-audit-v1",
        "scope": "finite theorem regression only; not the growing fixed-shift archive",
        "status": "PASS",
        "finite_regression_pass": True,
        "assertions_checked": checks,
        "intertwining_model": {
            "full_dimension": 4,
            "fixed_shift_dimension": 2,
            "stagewise_commutation": True,
            "composite_telescope": True,
            "cross_shift_leakage_detected": True,
        },
        "localization_model": {
            "finite_range_case": True,
            "sharp_squared_cost": "1",
            "infinite_cost_kernel_witness": True,
            "example_average_saving": "1/100",
            "example_localization_amplitude_cost": "1/500",
            "example_fixed_shift_saving": "1/125",
        },
        "route_verdict": {
            "commutator_telescope": "PROVED_L0",
            "sharp_localization_identity": "PROVED_L0",
            "literal_archive_crosswalk": "CONDITIONAL_L1",
            "complete_shift_tagged_growing_archive_present": False,
            "H7_fixed_shift_audit": "NOT_TESTABLE_FROM_CURRENT_ARTIFACTS",
            "fixed_h0_L2_progress": False,
        },
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--write", action="store_true")
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()

    result = certificate()
    target = Path(__file__).with_suffix(".json")
    if args.write:
        target.write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
    if args.check:
        expected = json.loads(target.read_text(encoding="utf-8"))
        if result != expected:
            raise SystemExit("certificate mismatch")
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
