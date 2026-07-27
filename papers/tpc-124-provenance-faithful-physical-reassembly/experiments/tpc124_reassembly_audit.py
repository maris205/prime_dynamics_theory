#!/usr/bin/env python3
"""Exact coordinate-model tests for the TPC-124 reassembly theorem."""

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


def add(left: Vector, right: Vector) -> Vector:
    return tuple(a + b for a, b in zip(left, right))


def sub(left: Vector, right: Vector) -> Vector:
    return tuple(a - b for a, b in zip(left, right))


def dot(left: Vector, right: Vector) -> Fraction:
    return sum((a * b for a, b in zip(left, right)), Fraction(0))


def certificate() -> dict[str, object]:
    checks = 0

    # C embeds two block coefficients as the first two native leaves.
    c_map: Matrix = (
        (Fraction(1), Fraction(0)),
        (Fraction(0), Fraction(1)),
        (Fraction(0), Fraction(0)),
    )
    c_dagger = transpose(c_map)
    z: Vector = (Fraction(2), Fraction(-1), Fraction(3))
    q_leaf = apply(c_dagger, z)
    r_leaf = sub(z, apply(c_map, q_leaf))
    assert q_leaf == (Fraction(2), Fraction(-1))
    assert r_leaf == (Fraction(0), Fraction(0), Fraction(3))
    checks += 2

    # Faithful physical realization: G=I, hence B=C.
    identity3: Matrix = (
        (Fraction(1), Fraction(0), Fraction(0)),
        (Fraction(0), Fraction(1), Fraction(0)),
        (Fraction(0), Fraction(0), Fraction(1)),
    )
    b_faithful = matmul(identity3, c_map)
    w_faithful = apply(identity3, z)
    q_phys = apply(transpose(b_faithful), w_faithful)
    r_phys = sub(w_faithful, apply(b_faithful, q_phys))
    assert r_phys == r_leaf
    checks += 1
    p_b_faithful = matmul(b_faithful, transpose(b_faithful))
    grouped_leaf_residual = apply(identity3, r_leaf)
    h_r_leaf_faithful = sub(
        grouped_leaf_residual,
        apply(p_b_faithful, grouped_leaf_residual),
    )
    assert h_r_leaf_faithful == r_phys
    checks += 1
    # Here ker(C^T)=span(e_3), so this normalized direction determines
    # the full restricted minimum modulus.
    faithful_gamma_squared = dot(h_r_leaf_faithful, h_r_leaf_faithful) / dot(
        r_leaf, r_leaf
    )
    assert faithful_gamma_squared == Fraction(1)
    checks += 1

    dual_leaf: Vector = (Fraction(0), Fraction(0), Fraction(1))
    assert apply(transpose(c_map), dual_leaf) == (Fraction(0), Fraction(0))
    assert dot(dual_leaf, z) == Fraction(3)
    checks += 2

    # A grouping can erase the third leaf. Physical cover then holds
    # although provenance cover fails.
    collapse: Matrix = (
        (Fraction(1), Fraction(0), Fraction(0)),
        (Fraction(0), Fraction(1), Fraction(0)),
    )
    b_collapsed = matmul(collapse, c_map)
    w_collapsed = apply(collapse, z)
    q_collapsed = apply(transpose(b_collapsed), w_collapsed)
    r_collapsed = sub(w_collapsed, apply(b_collapsed, q_collapsed))
    assert r_collapsed == (Fraction(0), Fraction(0))
    assert r_leaf != (Fraction(0), Fraction(0), Fraction(0))
    checks += 2
    p_b_collapsed = matmul(b_collapsed, transpose(b_collapsed))
    collapsed_grouped_residual = apply(collapse, r_leaf)
    h_r_leaf_collapsed = sub(
        collapsed_grouped_residual,
        apply(p_b_collapsed, collapsed_grouped_residual),
    )
    assert h_r_leaf_collapsed == r_collapsed
    checks += 1
    collapsed_gamma_squared = dot(h_r_leaf_collapsed, h_r_leaf_collapsed) / dot(
        r_leaf, r_leaf
    )
    assert collapsed_gamma_squared == Fraction(0)
    checks += 1

    # Exact scalar evaluator decomposition in the faithful model.
    evaluator: Vector = (Fraction(1), Fraction(2), Fraction(4))
    lhs = dot(evaluator, w_faithful)
    block_term = dot(apply(transpose(b_faithful), evaluator), q_phys)
    residual_term = dot(evaluator, r_phys)
    assert lhs == block_term + residual_term
    checks += 1

    gram_b = matmul(transpose(b_faithful), b_faithful)
    gram_crosswalk = matmul(
        matmul(transpose(c_map), matmul(transpose(identity3), identity3)),
        c_map,
    )
    assert gram_b == gram_crosswalk
    checks += 1

    # Distinct determinant and zero-mode dictionaries cannot be silently
    # identified. The two maps agree on one vector but not on every column.
    q_det: Matrix = (
        (Fraction(1), Fraction(0), Fraction(0)),
        (Fraction(0), Fraction(1), Fraction(1)),
    )
    q_zero: Matrix = (
        (Fraction(1), Fraction(0), Fraction(1)),
        (Fraction(0), Fraction(1), Fraction(0)),
    )
    test_vector: Vector = (Fraction(1), Fraction(2), Fraction(0))
    assert apply(q_det, test_vector) == apply(q_zero, test_vector)
    assert q_det != q_zero
    checks += 2

    return {
        "schema": "tpc124-provenance-physical-reassembly-audit-v1",
        "scope": "finite coordinate-model regression only; not the growing physical archive",
        "status": "PASS",
        "finite_regression_pass": True,
        "assertions_checked": checks,
        "exact_model": {
            "native_leaf_dimension": 3,
            "block_dimension": 2,
            "leaf_residual_nonzero": True,
            "faithful_physical_residual_matches_leaf_residual": True,
            "collapsed_physical_residual_zero": True,
            "scalar_reassembly_identity": True,
            "native_gram_crosswalk": True,
            "quotient_observability_faithful_and_zero_regimes": True,
        },
        "quotient_observability": {
            "residual_domain_dimension": 1,
            "residual_transfer_checked_in_both_models": True,
            "faithful_gamma_squared": str(faithful_gamma_squared),
            "collapsed_gamma_squared": str(collapsed_gamma_squared),
        },
        "counterexamples": {
            "physical_cover_does_not_imply_provenance_cover": True,
            "one_vector_agreement_does_not_identify_fiber_maps": True,
        },
        "route_verdict": {
            "dual_residual_theorem": "PROVED_L0",
            "literal_physical_crosswalk": "INTERFACE_L1",
            "actual_growing_G_C_z_B_archive_present": False,
            "H6_reassembly_audit": "NOT_TESTABLE_FROM_CURRENT_ARTIFACTS",
            "H8_provenance_reconnection_proved": False,
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
