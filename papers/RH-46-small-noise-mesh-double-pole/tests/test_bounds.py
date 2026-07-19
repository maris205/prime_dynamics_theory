from __future__ import annotations

import math

import numpy as np

from small_noise_two_step import (
    DETERMINISTIC_LAMBDA,
    bulk_square_mesh_power,
    edge_scaled_square_section,
    folded_gaussian_envelope,
    galerkin_resolution_ledger,
    gaussian_row_asymptotic_constant,
    ideal_cloud,
    ideal_square_section,
    normalizer_linear_lower,
    power_schedule_dimension,
    square_cloud_determinant,
    universal_squared_profile,
)


def test_normalizer_lower_is_uniform_and_positive() -> None:
    value = normalizer_linear_lower(0.03)
    assert 1.2533 < value < math.sqrt(math.pi / 2.0)


def test_uniform_envelope_dominates_validated_sigma_point() -> None:
    envelope = folded_gaussian_envelope(0.01)
    assert envelope.kernel_hilbert_schmidt_upper > 5.49855
    assert envelope.source_first_hilbert_schmidt_upper > 669.465
    assert envelope.target_first_hilbert_schmidt_upper > 382.571
    assert envelope.combined_first_hilbert_schmidt_upper > 1052.0


def test_envelope_has_exact_declared_scaling() -> None:
    first = folded_gaussian_envelope(0.01)
    second = folded_gaussian_envelope(0.0025)
    assert math.isclose(
        second.kernel_hilbert_schmidt_upper
        / first.kernel_hilbert_schmidt_upper,
        2.0,
        rel_tol=2.0e-15,
    )
    assert math.isclose(
        second.combined_first_hilbert_schmidt_upper
        / first.combined_first_hilbert_schmidt_upper,
        8.0,
        rel_tol=2.0e-15,
    )


def test_power_schedules_separate_hs_and_trace_thresholds() -> None:
    assert power_schedule_dimension(0.001, 1.0) == 655360
    assert power_schedule_dimension(0.001, 2.0) == 6553600
    critical = galerkin_resolution_ledger(
        0.001,
        power_schedule_dimension(0.001, 2.0),
        determinant_disk_radius=0.001,
    )
    finer = galerkin_resolution_ledger(
        0.0001,
        power_schedule_dimension(0.0001, 2.5),
        determinant_disk_radius=0.0001,
    )
    assert critical.galerkin_hilbert_schmidt_error_upper < 0.02
    assert finer.square_trace_norm_error_upper < 0.24


def test_conditional_bulk_power_formula() -> None:
    assert bulk_square_mesh_power(0.5, 1.5) == 2.0
    assert bulk_square_mesh_power(0.0, 2.25) == 2.75
    assert bulk_square_mesh_power(1.0, 1.0) == 2.5


def test_ideal_cloud_square_is_geometric_section_squared() -> None:
    for degree in (1, 2, 5, 9):
        cloud = ideal_cloud(degree)
        for w in (0.1, 0.5 + 0.1j, 1.0):
            actual = square_cloud_determinant(cloud, w)
            expected = ideal_square_section(degree, w)
            assert np.isclose(actual, expected, rtol=2.0e-13, atol=2.0e-13)


def test_edge_scaled_square_section_converges() -> None:
    s = 1.25
    target = universal_squared_profile(s)
    coarse = abs(edge_scaled_square_section(8, s) - target)
    fine = abs(edge_scaled_square_section(128, s) - target)
    assert fine < coarse / 10.0


def test_two_step_pole_location_and_gaussian_constant() -> None:
    assert 1.678 < DETERMINISTIC_LAMBDA < 1.679
    constant = gaussian_row_asymptotic_constant()
    assert 0.1084 < constant < 0.1085
