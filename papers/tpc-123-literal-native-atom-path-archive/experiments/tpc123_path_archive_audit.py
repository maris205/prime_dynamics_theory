#!/usr/bin/env python3
"""Exact finite tests for the TPC-123 path-archive theorem."""

from __future__ import annotations

import argparse
import json
from fractions import Fraction
from pathlib import Path

Matrix = tuple[tuple[Fraction, ...], ...]


def matmul(left: Matrix, right: Matrix) -> Matrix:
    assert left and right and len(left[0]) == len(right)
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


def column_sums(matrix: Matrix) -> tuple[Fraction, ...]:
    return tuple(
        sum((matrix[i][j] for i in range(len(matrix))), Fraction(0))
        for j in range(len(matrix[0]))
    )


def row_times(row: tuple[Fraction, ...], matrix: Matrix) -> tuple[Fraction, ...]:
    assert len(row) == len(matrix)
    return tuple(
        sum((row[i] * matrix[i][j] for i in range(len(matrix))), Fraction(0))
        for j in range(len(matrix[0]))
    )


def row_add(*rows: tuple[Fraction, ...]) -> tuple[Fraction, ...]:
    return tuple(sum((row[j] for row in rows), Fraction(0)) for j in range(len(rows[0])))


def row_sub(left: tuple[Fraction, ...], right: tuple[Fraction, ...]) -> tuple[Fraction, ...]:
    return tuple(a - b for a, b in zip(left, right))


def apply(matrix: Matrix, vector: tuple[Fraction, ...]) -> tuple[Fraction, ...]:
    return tuple(
        sum((matrix[i][j] * vector[j] for j in range(len(vector))), Fraction(0))
        for i in range(len(matrix))
    )


def dot(row: tuple[Fraction, ...], vector: tuple[Fraction, ...]) -> Fraction:
    return sum((a * b for a, b in zip(row, vector)), Fraction(0))


def certificate() -> dict[str, object]:
    checks = 0

    # Stage 1: two native atoms split into three intermediate records.
    t1: Matrix = (
        (Fraction(1, 3), Fraction(0)),
        (Fraction(2, 3), Fraction(0)),
        (Fraction(0), Fraction(1)),
    )
    # Stage 2: the last intermediate record is split retained/soft.
    t2: Matrix = (
        (Fraction(1), Fraction(0), Fraction(0)),
        (Fraction(0), Fraction(0), Fraction(1, 2)),
        (Fraction(0), Fraction(1), Fraction(0)),
        (Fraction(0), Fraction(0), Fraction(1, 2)),
    )
    assert column_sums(t1) == (Fraction(1), Fraction(1))
    checks += 1
    assert column_sums(t2) == (Fraction(1), Fraction(1), Fraction(1))
    checks += 1

    composite = matmul(t2, t1)
    assert column_sums(composite) == (Fraction(1), Fraction(1))
    checks += 1
    expanded = tuple(
        tuple(
            sum(
                (t2[leaf][mid] * t1[mid][source] for mid in range(3)),
                Fraction(0),
            )
            for source in range(2)
        )
        for leaf in range(4)
    )
    assert expanded == composite
    checks += 1

    coefficient = (Fraction(6), Fraction(-5))
    native_scalar = sum(coefficient, Fraction(0))
    leaf_vector = apply(composite, coefficient)
    assert sum(leaf_vector, Fraction(0)) == native_scalar
    checks += 1

    retained_rows = (0, 1)
    soft_rows = (2, 3)
    retained = sum((leaf_vector[i] for i in retained_rows), Fraction(0))
    soft = sum((leaf_vector[i] for i in soft_rows), Fraction(0))
    assert retained + soft == native_scalar
    checks += 1

    # Exact two-stage defect telescope.
    bad_t2: Matrix = (
        (Fraction(1), Fraction(0), Fraction(0)),
        (Fraction(0), Fraction(0), Fraction(1, 2)),
        (Fraction(0), Fraction(1, 2), Fraction(0)),
        (Fraction(0), Fraction(0), Fraction(1, 2)),
    )
    bad_composite = matmul(bad_t2, t1)
    defect2 = row_sub(column_sums(bad_t2), (Fraction(1),) * 3)
    defect1 = row_sub(column_sums(t1), (Fraction(1),) * 2)
    telescoped = row_add(row_times(defect2, t1), defect1)
    total_defect = row_sub(column_sums(bad_composite), (Fraction(1),) * 2)
    assert telescoped == total_defect
    checks += 1
    assert total_defect != (Fraction(0), Fraction(0))
    checks += 1

    # A scalar coincidence on one vector is weaker than column conservation.
    camouflage: Matrix = (
        (Fraction(2), Fraction(0)),
        (Fraction(0), Fraction(0)),
    )
    ones = (Fraction(1), Fraction(1))
    assert sum(apply(camouflage, ones), Fraction(0)) == sum(ones, Fraction(0))
    checks += 1
    assert column_sums(camouflage) != (Fraction(1), Fraction(1))
    checks += 1

    # Nonconservative stages can cancel in the final product.
    expand: Matrix = (
        (Fraction(2), Fraction(0)),
        (Fraction(0), Fraction(1, 2)),
    )
    contract: Matrix = (
        (Fraction(1, 2), Fraction(0)),
        (Fraction(0), Fraction(2)),
    )
    identity = matmul(contract, expand)
    assert identity == (
        (Fraction(1), Fraction(0)),
        (Fraction(0), Fraction(1)),
    )
    checks += 1
    assert column_sums(expand) != (Fraction(1), Fraction(1))
    assert column_sums(contract) != (Fraction(1), Fraction(1))
    checks += 1

    # A wrong leaf shift tag is invisible to coefficient sums.
    native_shift = {"a0": 2, "a1": 2}
    leaf_sources = {"r0": "a0", "r1": "a1", "s0": "a0", "s1": "a1"}
    leaf_shift = {"r0": 2, "r1": 2, "s0": 2, "s1": 4}
    metadata_ok = all(
        leaf_shift[leaf] == native_shift[source]
        for leaf, source in leaf_sources.items()
    )
    assert not metadata_ok
    checks += 1

    return {
        "schema": "tpc123-literal-path-archive-audit-v1",
        "scope": "finite theorem regression only; not the growing TPC archive",
        "status": "PASS",
        "finite_regression_pass": True,
        "assertions_checked": checks,
        "exact_model": {
            "native_atoms": 2,
            "intermediate_records": 3,
            "final_leaves": 4,
            "path_expansion_verified": True,
            "stage_column_conservation": True,
            "composite_column_conservation": True,
            "retained_soft_scalar_reconnection": True,
            "defect_telescope_verified": True,
        },
        "counterexamples": {
            "one_vector_scalar_coincidence_is_not_column_conservation": True,
            "nonconservative_stage_defects_can_cancel": True,
            "coefficient_conservation_does_not_verify_shift_metadata": True,
        },
        "typed_fields_required": [
            "native_key",
            "fixed_h0",
            "physical_normalization",
            "branch_path",
            "retained_or_soft",
            "determinant_fiber_and_phase",
            "zero_mode_order_sign_weight_and_content",
        ],
        "route_verdict": {
            "finite_path_archive_theorem": "PROVED_L0",
            "literal_tpc15_attachment": "INTERFACE_L1",
            "complete_growing_stage_archive_present": False,
            "H8_archive_audit": "NOT_TESTABLE_FROM_CURRENT_ARTIFACTS",
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
