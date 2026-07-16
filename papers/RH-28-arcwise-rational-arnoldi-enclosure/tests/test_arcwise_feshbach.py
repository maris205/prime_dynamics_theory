from __future__ import annotations

import csv
from fractions import Fraction
from pathlib import Path

import numpy as np

from arcwise_feshbach import (
    bisect_circular_arc_disc,
    circular_arc_discs,
    coordinate_extension_sum,
    enclose_coordinate_increment,
    enclose_shifted_coordinates,
    family_inverse_norm_upper,
    positive_fixed_point_upper,
)
from outward_residuals import ComponentwiseBall


ROOT = Path(__file__).resolve().parents[1]


def test_positive_fixed_point_upper_contains_direct_solution() -> None:
    majorant = np.array([[0.08, 0.03], [0.02, 0.06]], dtype=float)
    source = np.array([1.0, 0.4], dtype=float)
    upper, contraction, iterations = positive_fixed_point_upper(
        majorant, source
    )
    direct = np.linalg.solve(np.eye(2) - majorant, source)
    assert contraction < 1.0
    assert iterations >= 1
    assert np.all(np.asarray(direct) <= upper)


def test_nested_hessenberg_increment_contains_sampled_solutions() -> None:
    hessenberg = np.array(
        [
            [0.12 + 0.03j, -0.07j, 0.04, 0.0, 0.0],
            [0.18, 0.22 - 0.02j, 0.05j, -0.03, 0.0],
            [0.0, 0.16 - 0.01j, -0.11, 0.06j, 0.02],
            [0.0, 0.0, 0.14, 0.08 + 0.01j, -0.04j],
            [0.0, 0.0, 0.0, 0.11, -0.05],
        ],
        dtype=np.complex128,
    )
    center = 1.7 + 0.4j
    radius = 0.02
    base_depth = 2
    rhs = np.zeros(base_depth, dtype=np.complex128)
    rhs[0] = 1.0
    base = enclose_shifted_coordinates(
        hessenberg[:base_depth, :base_depth], rhs, center, radius
    )
    increment = enclose_coordinate_increment(
        hessenberg, base, center, radius, base_depth=base_depth
    )
    deep = coordinate_extension_sum(base, increment)
    for angle in np.linspace(0.0, 2.0 * np.pi, 17)[:-1]:
        zeta = center + radius * np.exp(1.0j * angle)
        deep_rhs = np.zeros(hessenberg.shape[0], dtype=np.complex128)
        deep_rhs[0] = 1.0
        exact_deep = np.linalg.solve(zeta * np.eye(5) - hessenberg, deep_rhs)
        exact_base = np.linalg.solve(
            zeta * np.eye(base_depth)
            - hessenberg[:base_depth, :base_depth],
            rhs,
        )
        exact_increment = exact_deep.copy()
        exact_increment[:base_depth] -= exact_base
        increment_bound = np.abs(increment.center) + increment.radius
        deep_bound = np.abs(deep.center) + deep.radius
        assert np.max(np.abs(exact_increment) - increment_bound) <= 2.0e-12
        assert np.max(np.abs(exact_deep) - deep_bound) <= 2.0e-12


def test_rational_arc_children_cover_parent_endpoints() -> None:
    contour_center = -0.3 + 0.2j
    contour_radius = 0.7
    parent = circular_arc_discs(contour_center, contour_radius, 16)[3]
    left, right = bisect_circular_arc_disc(
        parent, contour_center, contour_radius, first_index=100
    )
    assert left.start_numerator == 2 * parent.start_numerator
    assert left.end_numerator == right.start_numerator
    assert right.end_numerator == 2 * parent.end_numerator
    assert left.turn_denominator == right.turn_denominator
    for child in (left, right):
        denominator = child.turn_denominator
        for numerator in (child.start_numerator, child.end_numerator):
            point = contour_center + contour_radius * np.exp(
                2.0j * np.pi * numerator / denominator
            )
            assert abs(point - child.center) <= child.radius * (1.0 + 1.0e-12)


def test_projected_family_neumann_bound_is_valid_for_a_simple_ball() -> None:
    center = np.array(
        [[2.0 + 0.1j, 0.03], [-0.02j, 1.7 - 0.05j]],
        dtype=np.complex128,
    )
    radius = np.full(center.shape, 2.0e-6, dtype=float)
    upper, product, defect = family_inverse_norm_upper(
        ComponentwiseBall(center, radius)
    )
    assert product < 1.0
    assert defect < 1.0e-10
    rng = np.random.default_rng(20260715)
    for _ in range(20):
        perturbation = (
            rng.normal(size=center.shape)
            + 1.0j * rng.normal(size=center.shape)
        )
        perturbation *= 1.0e-6 / np.linalg.norm(perturbation)
        assert np.linalg.norm(np.linalg.inv(center + perturbation), 2) <= upper


def test_archived_adaptive_covers_are_exact_partitions() -> None:
    summary_path = ROOT / "results" / "arcwise_scale_summary.csv"
    arc_path = ROOT / "results" / "arcwise_contour_arcs.csv"
    with summary_path.open(encoding="utf-8") as handle:
        summaries = list(csv.DictReader(handle))
    with arc_path.open(encoding="utf-8") as handle:
        arcs = list(csv.DictReader(handle))
    assert len(summaries) == 7
    for summary in summaries:
        sigma = float(summary["sigma"])
        selected = sorted(
            [row for row in arcs if float(row["sigma"]) == sigma],
            key=lambda row: int(row["arc"]),
        )
        cursor = Fraction(0, 1)
        for row in selected:
            start = Fraction(
                int(row["start_numerator"]), int(row["turn_denominator"])
            )
            end = Fraction(
                int(row["end_numerator"]), int(row["turn_denominator"])
            )
            assert start == cursor
            assert end > start
            assert float(row["correction_ratio_upper"]) < 1.0
            cursor = end
        assert cursor == Fraction(1, 1)
        assert len(selected) == int(summary["accepted_arc_count"])
        assert max(
            float(row["correction_ratio_upper"]) for row in selected
        ) == float(summary["maximum_correction_ratio_upper"])
