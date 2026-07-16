from __future__ import annotations

import csv
import json
from pathlib import Path

import numpy as np

from deflated_resolvent import (
    NormInterval,
    arb_vector_norm_interval,
    arc_center_threshold_lower,
    candidate_arc_inverse,
    lifted_full_inverse_upper,
    lifted_inverse_budget_lower,
    normalized_residual_bounds,
)


def test_exact_singular_lift_bounds_inverse() -> None:
    singular = 0.01
    matrix = np.diag([singular, 0.2, 0.5]).astype(np.complex128)
    right = np.array([1.0, 0.0, 0.0], dtype=np.complex128)
    left = right.copy()
    lifted = matrix + (1.0 - singular) * np.outer(left, right.conj())
    lifted_inverse = np.linalg.norm(np.linalg.inv(lifted), 2)
    evaluation = lifted_full_inverse_upper(
        lifted_inverse,
        singular,
        0.0,
        0.0,
    )
    assert evaluation.admissible
    assert evaluation.full_inverse_upper >= np.linalg.norm(np.linalg.inv(matrix), 2)
    assert evaluation.denominator_lower > 0.0


def test_approximate_triplet_bound_dominates_direct_inverse() -> None:
    rng = np.random.default_rng(20260716)
    left_unitary, _ = np.linalg.qr(
        rng.standard_normal((5, 5)) + 1.0j * rng.standard_normal((5, 5))
    )
    right_unitary, _ = np.linalg.qr(
        rng.standard_normal((5, 5)) + 1.0j * rng.standard_normal((5, 5))
    )
    values = np.array([0.018, 0.21, 0.43, 0.77, 1.1])
    matrix = left_unitary @ np.diag(values) @ right_unitary.conj().T
    left = left_unitary[:, 0].copy()
    right = right_unitary[:, 0].copy()
    perturbation = 2.0e-5 * right_unitary[:, 1]
    right = right + perturbation
    right /= np.linalg.norm(right)
    singular = float(np.linalg.norm(matrix @ right))
    left = matrix @ right / singular
    right_residual = np.linalg.norm(matrix @ right - singular * left)
    left_residual = np.linalg.norm(matrix.conj().T @ left - singular * right)
    lifted = matrix + (1.0 - singular) * np.outer(left, right.conj())
    lifted_inverse = np.linalg.norm(np.linalg.inv(lifted), 2)
    evaluation = lifted_full_inverse_upper(
        lifted_inverse,
        singular,
        right_residual,
        left_residual,
    )
    assert evaluation.admissible
    assert evaluation.full_inverse_upper >= np.linalg.norm(np.linalg.inv(matrix), 2)


def test_arc_transport_threshold_is_sufficient() -> None:
    arc_budget = 1.1e5
    radius = 1.37e-6
    center_budget = arc_center_threshold_lower(arc_budget, radius)
    transported = candidate_arc_inverse(center_budget, radius)
    assert center_budget < arc_budget
    assert transported <= arc_budget * (1.0 + 2.0e-15)


def test_lifted_budget_bisection_is_downward() -> None:
    target = 9.5e4
    singular = 5.8e-5
    right_residual = 2.0e-9
    left_residual = 3.0e-9
    budget = lifted_inverse_budget_lower(
        target,
        singular,
        right_residual,
        left_residual,
    )
    assert budget > 0.0
    assert lifted_full_inverse_upper(
        budget,
        singular,
        right_residual,
        left_residual,
    ).full_inverse_upper < target
    assert lifted_full_inverse_upper(
        budget * (1.0 + 1.0e-8),
        singular,
        right_residual,
        left_residual,
    ).full_inverse_upper >= target


def test_normalization_and_arb_norm_intervals() -> None:
    vector = np.array([0.3 + 0.4j, -0.5 + 0.1j, 0.2 - 0.7j])
    interval = arb_vector_norm_interval(vector)
    direct = float(np.linalg.norm(vector))
    assert interval.lower <= direct <= interval.upper
    bounds = normalized_residual_bounds(
        1.0e-10,
        2.0e-10,
        interval,
        NormInterval(interval.lower * (1.0 - 1.0e-12), interval.upper),
        0.02,
    )
    assert bounds.right >= 1.0e-10 / interval.upper
    assert bounds.left >= 2.0e-10 / interval.upper
    assert bounds.norm_mismatch > 0.0


def test_archived_seven_scale_summary() -> None:
    root = Path(__file__).resolve().parents[1]
    with (root / "results" / "deflated_scale_summary.csv").open(
        encoding="utf-8"
    ) as handle:
        rows = list(csv.DictReader(handle))
    assert [float(row["sigma"]) for row in rows] == [
        1.0e-2,
        4.0e-3,
        2.0e-3,
        1.0e-3,
        5.0e-4,
        2.0e-4,
        1.0e-4,
    ]
    assert all(
        float(row["lifted_inverse_budget_lower"])
        > float(row["lifted_bulk_inverse_candidate"])
        for row in rows
    )
    assert min(float(row["lifted_bulk_budget_margin"]) for row in rows) > 95.0


def test_archived_numerical_range_witness() -> None:
    root = Path(__file__).resolve().parents[1]
    data = json.loads(
        (root / "results" / "certified_numerical_range_witness.json").read_text(
            encoding="utf-8"
        )
    )
    assert data["strict_origin_in_convex_hull_certified"] == 1
    assert data["minimum_weight_lower"] > 0.048
