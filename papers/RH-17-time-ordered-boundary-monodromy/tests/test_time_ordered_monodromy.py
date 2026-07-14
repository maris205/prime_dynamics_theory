from __future__ import annotations

import csv
from pathlib import Path
import sys

import mpmath as mp
import numpy as np

from time_ordered_monodromy import (
    balancing_condition_number,
    balancing_diagonal,
    bipartite_lift,
    boundary_cycle,
    critical_constants,
    edge_deflated_determinant,
    eigenvalue_condition_number,
    endpoint_dictionary_gap,
    geometric_section,
    ideal_reciprocal_cloud,
    two_step_map,
    weighted_cycle_matrix,
)


ROOT = Path(__file__).resolve().parents[1]
PAPERS = ROOT.parent


def test_boundary_orbit_is_in_exact_two_step_time_order() -> None:
    cycle = boundary_cycle(8, 100)
    for index, point in enumerate(cycle.orbit):
        image = two_step_map(point, decimal_digits=100)
        target = cycle.orbit[(index + 1) % cycle.component_period]
        assert abs(image - target) < mp.mpf("1e-75")
    assert abs(cycle.multiplier * cycle.inverse_branch_derivative - 1) < mp.mpf(
        "1e-70"
    )


def test_cross_cycle_endpoint_dictionary_is_not_forward_invariant() -> None:
    constants = critical_constants(100)
    assert endpoint_dictionary_gap(100) > mp.mpf("0.09")
    p_two = boundary_cycle(1, 100).point
    for period in range(2, 10):
        image = two_step_map(boundary_cycle(period, 100).point)
        assert image < constants.first_interior_point
        assert p_two - image > endpoint_dictionary_gap(100)


def test_boundary_multiplier_has_lambda_to_k_growth() -> None:
    constants = critical_constants(120)
    cycle_60 = boundary_cycle(60, 120)
    cycle_80 = boundary_cycle(80, 120)
    assert cycle_60.multiplier < 0
    assert abs(cycle_80.scaled_multiplier - cycle_60.scaled_multiplier) < mp.mpf(
        "2e-13"
    )
    assert abs(cycle_80.scaled_multiplier - mp.mpf("1.94634290520097")) < mp.mpf(
        "3e-14"
    )
    assert abs(cycle_80.inverse_jacobian_radius - 1 / constants.lambda_fixed) < 0.006


def test_weighted_cycle_is_diagonally_similar_to_constant_cycle() -> None:
    cycle = boundary_cycle(8, 100)
    weighted = weighted_cycle_matrix(cycle)
    diagonal = balancing_diagonal(cycle)
    balanced = np.diag(1.0 / diagonal) @ weighted @ np.diag(diagonal)
    rho = float(cycle.inverse_jacobian_radius)
    expected = np.zeros_like(weighted)
    columns = np.arange(cycle.component_period)
    expected[(columns + 1) % cycle.component_period, columns] = rho
    assert np.max(np.abs(balanced - expected)) < 2.0e-13
    assert np.max(
        np.abs(
            np.linalg.matrix_power(weighted, cycle.component_period)
            - rho**cycle.component_period * np.eye(cycle.component_period)
        )
    ) < 3.0e-13


def test_bipartite_edge_deflation_is_exact_geometric_section() -> None:
    cycle = boundary_cycle(6, 100)
    lifted = bipartite_lift(cycle)
    for z in (0.2, 0.4 + 0.15j, -0.3 + 0.2j):
        direct = np.linalg.det(np.eye(lifted.shape[0]) - z * lifted)
        rho = float(cycle.inverse_jacobian_radius)
        quotient = direct / (1.0 - rho * z * z)
        exact = edge_deflated_determinant(cycle, z)
        assert abs(quotient - exact) < 2.0e-12

    q = np.asarray((0.1, 0.5 + 0.2j, 1.0), dtype=np.complex128)
    assert np.max(
        np.abs(geometric_section(5, q) * (1 - q) - (1 - q**6))
    ) < 2.0e-15


def test_reciprocal_cloud_has_exact_root_of_unity_phases() -> None:
    cycle = boundary_cycle(8, 100)
    cloud = ideal_reciprocal_cloud(cycle)
    assert cloud.size == 14
    roots = 1.0 / cloud
    values = edge_deflated_determinant(cycle, roots)
    assert np.max(np.abs(values)) < 2.0e-12


def test_balancing_and_eigenvalue_conditioning_are_nonuniform() -> None:
    constants = critical_constants(110)
    for period in (20, 30, 40):
        cycle = boundary_cycle(period, 110)
        scaled = balancing_condition_number(cycle) / float(
            constants.lambda_fixed**period
        )
        assert 0.39 < scaled < 0.44
        assert eigenvalue_condition_number(cycle) >= (
            balancing_condition_number(cycle) / period
        )


def test_finite_cycle_radius_improves_archived_cloud_prediction() -> None:
    cloud_path = (
        PAPERS
        / "RH-15-parity-extracted-bulk-scattering"
        / "results"
        / "cloud_summary.csv"
    )
    rank_source = (
        PAPERS
        / "RH-16-endpoint-gaussian-resolution-rank"
        / "src"
    )
    sys.path.insert(0, str(rank_source))
    from endpoint_rank import (  # pylint: disable=import-outside-toplevel
        HALF_ENERGY_THRESHOLD,
        boundary_clearances,
        threshold_rank,
    )

    with cloud_path.open(encoding="utf-8") as handle:
        cloud_rows = list(csv.DictReader(handle))
    clearances = boundary_clearances(70)
    target = float(critical_constants(100).lambda_fixed ** (-mp.mpf("0.5")))
    for row in cloud_rows:
        sigma = float(row["sigma"])
        hellinger_degree = threshold_rank(
            clearances,
            sigma,
            threshold=HALF_ENERGY_THRESHOLD,
            power=0.5,
        )
        linear_degree = threshold_rank(
            clearances,
            sigma,
            threshold=HALF_ENERGY_THRESHOLD,
            power=1.0,
        )
        cloud_degree = int(row["effective_cloud_degree"])
        observed = float(row["cloud_radial_mean"])
        for degree in (hellinger_degree, linear_degree, cloud_degree):
            predicted = float(boundary_cycle(degree + 1, 100).one_step_radius)
            assert abs(observed - predicted) < abs(observed - target)
