from __future__ import annotations

import numpy as np

from small_noise_cycles.action import (
    cycle_action,
    cycle_action_gradient,
    cycle_residual,
    residual_jacobian,
)
from small_noise_cycles.deterministic import (
    cycle_orbits,
    directed_orbit_trace,
    periodic_orbit_trace,
)
from small_noise_cycles.operators import (
    autonomous_cycle_traces,
    directed_matrix_trace,
    folded_gaussian_matrix,
)


U_CRITICAL = 1.543689012692


def test_critical_fixed_point_audit() -> None:
    three = cycle_orbits((U_CRITICAL,) * 3, grid_size=80_001)
    six = cycle_orbits((U_CRITICAL,) * 6, grid_size=120_001)
    assert len(three) == 1
    assert len(six) == 15
    assert abs(sum(record.weight for record in three) - 0.1745333538263) < 2.0e-11
    assert abs(sum(record.weight for record in six) - 1.62214108872) < 2.0e-9
    assert min(record.boundary_clearance for record in six) > 0.017
    assert min(abs(1.0 - record.multiplier) for record in six) > 8.0


def test_residual_jacobian_determinant_identity() -> None:
    parameters = (1.42, 1.42, 1.54, 1.54, 1.66, 1.66)
    for record in cycle_orbits(parameters, grid_size=100_001):
        jacobian = residual_jacobian(record.points, parameters)
        assert abs(abs(np.linalg.det(jacobian)) - abs(1.0 - record.multiplier)) < 2.0e-8
        assert np.max(np.abs(cycle_residual(record.points, parameters))) < 2.0e-10
        assert cycle_action(record.points, parameters) < 2.0e-20


def test_cycle_action_gradient() -> None:
    parameters = np.array((1.41, 1.53, 1.64))
    points = np.array((-0.37, 0.82, -0.11))
    step = 1.0e-6
    numerical = np.empty(3)
    for index in range(3):
        perturbation = np.zeros(3)
        perturbation[index] = step
        numerical[index] = (
            cycle_action(points + perturbation, parameters)
            - cycle_action(points - perturbation, parameters)
        ) / (2.0 * step)
    assert np.max(np.abs(numerical - cycle_action_gradient(points, parameters))) < 2.0e-9


def test_deterministic_trace_is_cyclic_and_directed() -> None:
    a, b, c = 1.42, 1.54, 1.66
    first = periodic_orbit_trace((a, b, c), grid_size=80_001)
    second = periodic_orbit_trace((b, c, a), grid_size=80_001)
    third = periodic_orbit_trace((c, a, b), grid_size=80_001)
    assert abs(first - second) < 2.0e-11
    assert abs(first - third) < 2.0e-11
    directed = directed_orbit_trace(a, b, c, grid_size=80_001)
    reversed_directed = directed_orbit_trace(a, c, b, grid_size=80_001)
    assert abs(directed) > 1.0e-6
    assert abs(directed + reversed_directed) < 2.0e-11


def test_folded_matrix_trace_moves_toward_orbit_trace() -> None:
    target_three = periodic_orbit_trace((U_CRITICAL,) * 3, grid_size=80_001)
    coarse = folded_gaussian_matrix(220, U_CRITICAL, 0.08)
    fine = folded_gaussian_matrix(520, U_CRITICAL, 0.035)
    coarse_three, _ = autonomous_cycle_traces(coarse)
    fine_three, _ = autonomous_cycle_traces(fine)
    assert abs(fine_three - target_three) < abs(coarse_three - target_three)
    assert abs(fine_three - target_three) < 2.0e-3


def test_finite_matrix_directed_antisymmetry() -> None:
    a = folded_gaussian_matrix(180, 1.42, 0.055)
    b = folded_gaussian_matrix(180, 1.54, 0.055)
    c = folded_gaussian_matrix(180, 1.66, 0.055)
    directed = directed_matrix_trace(a, b, c)
    reversed_directed = directed_matrix_trace(a, c, b)
    assert abs(directed + reversed_directed) < 2.0e-12
    assert abs(directed) > 1.0e-5
