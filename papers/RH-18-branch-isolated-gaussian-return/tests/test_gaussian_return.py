from __future__ import annotations

from pathlib import Path
import sys

import numpy as np
from scipy.integrate import quad
from scipy.special import ndtr

from gaussian_return import (
    affine_critical_profile,
    bipartite_root_ring,
    block_cyclic_matrix,
    conditioned_critical_profile,
    critical_branch_midpoint,
    effective_noise_scales,
    fixed_boundary_width,
    packet_masks,
    periodic_packet_tube,
    positive_midpoints,
    principal_return_eigenpair,
    return_product,
    root_ring,
    sparse_folded_gaussian_matrix,
    unconditioned_critical_profile,
)


ROOT = Path(__file__).resolve().parents[1]
PAPERS = ROOT.parent
sys.path.insert(
    0, str(PAPERS / "RH-17-time-ordered-boundary-monodromy" / "src")
)

from time_ordered_monodromy import boundary_cycle, critical_constants  # noqa: E402


def cycle_packet_data(period: int):
    constants = critical_constants(110)
    cycle = boundary_cycle(period, 120)
    points = np.asarray([float(value) for value in cycle.orbit])
    multipliers = np.abs(
        np.asarray([float(value) for value in cycle.two_step_derivatives])
    )
    noise = effective_noise_scales(points, float(constants.u))
    return constants, cycle, points, multipliers, noise, periodic_packet_tube(
        multipliers, noise
    )


def test_periodic_riccati_tube_has_exact_multiplier_product() -> None:
    _, cycle, _, multipliers, noise, tube = cycle_packet_data(8)
    residual = (
        multipliers**2 * tube.widths**2
        - np.roll(tube.widths**2, -1)
        - noise**2
    )
    assert np.max(np.abs(residual)) < 3.0e-12
    assert tube.recurrence_residual < 3.0e-12
    assert abs(np.prod(tube.coefficients) - 1.0 / abs(float(cycle.multiplier))) < 2.0e-14
    assert abs(tube.spectral_radius - float(cycle.inverse_jacobian_radius)) < 2.0e-14
    assert np.min(tube.coefficients) > 0.0
    assert np.max(tube.coefficients) < 1.0


def test_affine_gaussian_channel_formula_is_exact() -> None:
    _, _, _, multipliers, noise, tube = cycle_packet_data(6)
    index = 3
    target_width = tube.widths[(index + 1) % tube.widths.size]
    source_width = tube.widths[index]
    coefficient = tube.coefficients[index]
    multiplier = multipliers[index]
    beta = noise[index]
    for source in (-1.2, -0.3, 0.0, 0.8):
        direct = quad(
            lambda z: np.exp(
                -0.5 * (multiplier * source + beta * z) ** 2 / target_width**2
            )
            * np.exp(-0.5 * z * z)
            / np.sqrt(2.0 * np.pi),
            -10.0,
            10.0,
            epsabs=2.0e-13,
        )[0]
        expected = coefficient * np.exp(-0.5 * source**2 / source_width**2)
        assert abs(direct - expected) < 3.0e-12


def test_packet_widths_recover_the_half_cycle_conditioning_exponent() -> None:
    constants, _, _, _, _, tube_40 = cycle_packet_data(40)
    _, _, _, _, _, tube_80 = cycle_packet_data(80)
    lambda_fixed = float(constants.lambda_fixed)
    exponent_40 = np.log(tube_40.balancing_condition) / (
        40.0 * np.log(lambda_fixed)
    )
    exponent_80 = np.log(tube_80.balancing_condition) / (
        80.0 * np.log(lambda_fixed)
    )
    assert 0.47 < exponent_40 < 0.53
    assert 0.48 < exponent_80 < 0.52
    assert tube_80.balancing_condition > tube_40.balancing_condition**1.8
    assert tube_80.recurrence_residual < 8.0e-15


def test_endpoint_and_critical_width_asymptotics() -> None:
    constants, _, _, _, _, tube = cycle_packet_data(80)
    _, endpoint_limit = fixed_boundary_width(
        float(constants.lambda_fixed), float(constants.u)
    )
    assert abs(tube.widths[0] - endpoint_limit) < 3.0e-7
    scaled_final = tube.widths[-1] / float(constants.lambda_fixed**80)
    assert abs(scaled_final - 0.2570) < 8.0e-4


def test_conditioned_critical_profile_matches_its_defining_integral() -> None:
    u = float(critical_constants(100).u)
    clearance = 1.3
    width = 0.41
    for coordinate in (-0.7, -0.1, 0.2, 0.6):
        a_value = (np.sqrt(clearance) - 2.0 * u * coordinate) ** 2
        b_value = clearance - a_value
        direct = quad(
            lambda z: np.exp(-0.5 * (b_value + z) ** 2 / width**2)
            * np.exp(-0.5 * z * z)
            / np.sqrt(2.0 * np.pi),
            -12.0,
            a_value,
            epsabs=2.0e-13,
        )[0] / ndtr(a_value)
        exact = conditioned_critical_profile(
            coordinate, clearance, width, u
        )
        assert abs(direct - exact) < 3.0e-12


def test_critical_profile_has_two_symbolic_lobes() -> None:
    u = float(critical_constants(100).u)
    clearance = 0.9
    width = 0.4
    midpoint = critical_branch_midpoint(clearance, u)
    offsets = np.linspace(-0.8, 0.8, 41)
    left = conditioned_critical_profile(midpoint + offsets, clearance, width, u)
    right = conditioned_critical_profile(midpoint - offsets, clearance, width, u)
    assert np.max(np.abs(left - right)) < 2.0e-15
    assert affine_critical_profile(0.4, clearance, width, u) != left[30]
    assert unconditioned_critical_profile(0.4, clearance, width, u) > 0.0


def test_block_cyclic_spectrum_is_generated_by_return_roots() -> None:
    channels = [
        np.asarray(((0.8, 0.1), (0.2, 0.5))),
        np.asarray(((0.7, -0.2), (0.1, 0.9))),
        np.asarray(((0.6, 0.3), (-0.1, 0.75))),
    ]
    block = block_cyclic_matrix(channels)
    returned = return_product(channels)
    expected = np.concatenate([root_ring(value, 3) for value in np.linalg.eigvals(returned)])
    observed = np.linalg.eigvals(block)
    for value in expected:
        assert np.min(np.abs(observed - value)) < 2.0e-12
    lifted = np.concatenate(
        [bipartite_root_ring(value, 3) for value in np.linalg.eigvals(returned)]
    )
    assert lifted.size == 12


def test_sparse_folded_operator_and_local_edge_smoke() -> None:
    constants, cycle, points, multipliers, noise, tube = cycle_packet_data(3)
    sigma = 1.0e-2
    dimension = 2048
    grid = positive_midpoints(dimension)
    matrix = sparse_folded_gaussian_matrix(
        dimension, sigma, u=float(constants.u)
    )
    assert np.max(np.abs(np.asarray(matrix.sum(axis=1)).ravel() - 1.0)) < 8.0e-15
    masks = packet_masks(
        grid,
        points,
        sigma * tube.widths,
        window_multiple=6.0,
        critical_partition=float(constants.first_interior_point),
    )
    initial = np.exp(
        -0.5 * ((grid - points[0]) / (sigma * tube.widths[0])) ** 2
    )
    pair = principal_return_eigenpair(matrix, masks, initial, iterations=10)
    radius = pair.eigenvalue ** (1.0 / (2.0 * cycle.component_period))
    assert abs(radius - 0.7407671) < 4.0e-4
    assert pair.residual < 2.0e-7


def test_conditioned_profile_matches_small_noise_folded_channel() -> None:
    constants, cycle, points, _, _, tube = cycle_packet_data(3)
    sigma = 1.0e-2
    dimension = 2048
    grid = positive_midpoints(dimension)
    matrix = sparse_folded_gaussian_matrix(
        dimension, sigma, u=float(constants.u)
    )
    endpoint = np.exp(
        -0.5 * ((grid - points[0]) / (sigma * tube.widths[0])) ** 2
    )
    observed = matrix @ (matrix @ endpoint)
    coordinate = (grid - points[-1]) / np.sqrt(sigma)
    clearance = float(cycle.clearance) / sigma
    exact = conditioned_critical_profile(
        coordinate, clearance, tube.widths[0], float(constants.u)
    )
    mask = (
        np.abs(grid - points[-1]) < 6.0 * sigma * tube.widths[-1]
    ) & (grid < float(constants.first_interior_point))
    relative = np.linalg.norm(observed[mask] - exact[mask]) / np.linalg.norm(
        observed[mask]
    )
    assert relative < 0.055
