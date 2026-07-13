from __future__ import annotations

import numpy as np

from flat_trace_completion import (
    H_CRITICAL,
    LAMBDA_FIXED,
    R_FIXED,
    U_CRITICAL,
    audit_length,
    centered_component_zeta_series,
    component_critical_value_derivative,
    component_geometry,
    component_weighted_coefficients,
    component_weighted_traces,
    critical_orbit,
    critical_value_derivative,
    flat_periodic_trace,
    iterate_map,
    orbit_multiplier,
    periodic_points,
    physical_fixed_point_count,
    quadratic_map,
    smallest_positive_real_root,
    weighted_periodic_trace,
)


def direct_derivative(point: float, length: int) -> float:
    value = float(point)
    derivative = 1.0
    for _ in range(length):
        derivative *= -2.0 * U_CRITICAL * value
        value = float(quadratic_map(value))
    return abs(derivative)


def test_postcritical_orbit_and_exact_collet_eckmann_growth() -> None:
    expected = np.asarray((0.0, 1.0, -R_FIXED, R_FIXED, R_FIXED))
    assert np.max(np.abs(np.asarray(critical_orbit()) - expected)) < 5.0e-14
    for length in range(1, 9):
        assert abs(direct_derivative(1.0, length) - critical_value_derivative(length)) < (
            2.0e-11 * critical_value_derivative(length)
        )


def test_two_component_critical_data_and_growth() -> None:
    central = component_geometry("central")
    high = component_geometry("high")
    assert central["interval"] == (-R_FIXED, R_FIXED)
    assert high["interval"] == (R_FIXED, 1.0)
    assert abs(float(high["critical_point"]) - H_CRITICAL) < 1.0e-15
    assert abs(float(iterate_map(0.0, 2)) + R_FIXED) < 5.0e-14
    assert abs(float(iterate_map(H_CRITICAL, 2)) - 1.0) < 5.0e-14
    for length in range(1, 7):
        assert component_critical_value_derivative("central", length) > 1.0
        assert component_critical_value_derivative("high", length) > 1.0


def test_periodic_counts_and_residuals() -> None:
    for length in range(1, 13):
        points = periodic_points(length)
        assert len(points) == physical_fixed_point_count(length)
        assert max(abs(float(iterate_map(point, length)) - point) for point in points) < 2.0e-10


def test_component_weighted_traces_are_exactly_paired() -> None:
    for length in range(2, 13, 2):
        central, high = component_weighted_traces(length)
        assert abs(central - high) < 3.0e-11
        reconstructed = central + high - LAMBDA_FIXED ** (-length)
        assert abs(reconstructed - weighted_periodic_trace(length)) < 3.0e-11


def test_flat_weighted_comparison_bound() -> None:
    for length in range(2, 13):
        record = audit_length(length)
        if np.isfinite(record.elementary_comparison_bound):
            assert abs(record.flat_minus_weighted) <= record.elementary_comparison_bound


def test_odd_traces_are_explicit() -> None:
    for length in range(1, 14, 2):
        assert abs(weighted_periodic_trace(length) - LAMBDA_FIXED ** (-length)) < 2.0e-12
        expected_flat = 1.0 / (1.0 + LAMBDA_FIXED**length)
        assert abs(flat_periodic_trace(length) - expected_flat) < 3.0e-14


def test_centered_zeta_series_reconstructs_logarithmic_coefficients() -> None:
    weighted = component_weighted_coefficients(6)
    series = centered_component_zeta_series(weighted)
    # Numerically take the formal logarithm through degree six.
    remainder = series.copy()
    remainder[0] -= 1.0
    log_series = np.zeros_like(series)
    power = remainder.copy()
    for order in range(1, 7):
        log_series += ((-1) ** (order + 1) / order) * power
        power = np.convolve(power, remainder)[: series.size]
    expected = np.zeros_like(series)
    expected[1:] = (weighted - 1.0) / np.arange(1, 7)
    assert np.max(np.abs(log_series - expected)) < 2.0e-12


def test_first_centered_zeta_zero_moves_toward_lambda() -> None:
    weighted = component_weighted_coefficients(8)
    roots = []
    for degree in range(4, 9):
        series = centered_component_zeta_series(weighted[:degree])
        roots.append(smallest_positive_real_root(series))
    errors = np.abs(np.asarray(roots) - LAMBDA_FIXED)
    assert np.all(errors[1:] < errors[:-1])
    assert errors[-1] < 0.015
