from __future__ import annotations

import numpy as np

from long_cycle import (
    LAMBDA_FIXED,
    R_FIXED,
    U_CRITICAL,
    boundary_periodic_point,
    bulk_trace_from_spectrum,
    critical_orbit,
    deterministic_flat_trace,
    exact_bulk_det2,
    folded_gaussian_matrix,
    iterate_map,
    markov_matrix,
    orbit_multiplier,
    periodic_points,
    physical_fixed_point_count,
    regularized_determinant_from_traces,
    resolve_spectrum,
    symbolic_closed_path_count,
    trace_from_spectrum,
)


def test_algebraic_parameter_orbit_and_markov_spectrum() -> None:
    polynomial = U_CRITICAL**3 - 2.0 * U_CRITICAL**2 + 2.0 * U_CRITICAL - 2.0
    assert abs(polynomial) < 2.0e-14
    assert np.max(
        np.abs(np.asarray(critical_orbit()) - np.asarray((0.0, 1.0, -R_FIXED, R_FIXED, R_FIXED)))
    ) < 5.0e-14
    values = np.sort(np.linalg.eigvals(markov_matrix()).real)
    assert np.max(np.abs(values - np.asarray((-np.sqrt(2.0), 0.0, np.sqrt(2.0))))) < 2.0e-14


def test_exact_symbolic_and_physical_counts() -> None:
    for length in range(1, 13):
        symbolic_expected = 0 if length % 2 else 2 ** (length // 2 + 1)
        assert symbolic_closed_path_count(length) == symbolic_expected
        points = periodic_points(length)
        assert len(points) == physical_fixed_point_count(length)
        assert len(points) == (1 if length % 2 else symbolic_expected - 1)
        assert max(abs(float(iterate_map(point, length)) - point) for point in points) < 2.0e-10


def test_odd_flat_trace_is_exactly_the_fixed_boundary_orbit() -> None:
    for length in range(1, 14, 2):
        assert periodic_points(length) == (R_FIXED,)
        expected = 1.0 / (1.0 + LAMBDA_FIXED**length)
        assert abs(deterministic_flat_trace(length) - expected) < 3.0e-14
        assert abs(orbit_multiplier(R_FIXED, length) + LAMBDA_FIXED**length) < 1.0e-11 * (
            1.0 + LAMBDA_FIXED**length
        )


def test_boundary_cycle_has_lambda_to_minus_length_clearance() -> None:
    lengths = np.arange(8, 22, 2)
    clearances = np.asarray([1.0 - boundary_periodic_point(int(length)) for length in lengths])
    scaled = clearances * LAMBDA_FIXED**lengths
    assert np.all((scaled > 0.38) & (scaled < 0.47))
    slope = np.polyfit(lengths, np.log(clearances), 1)[0]
    assert abs(slope + np.log(LAMBDA_FIXED)) < 0.025


def test_folded_matrix_is_markov_and_spectrum_resolves() -> None:
    matrix = folded_gaussian_matrix(96, 0.06)
    assert np.min(matrix) >= 0.0
    assert np.max(np.abs(np.sum(matrix, axis=1) - 1.0)) < 3.0e-15
    spectrum = resolve_spectrum(matrix)
    assert abs(spectrum.perron - 1.0) < 2.0e-13
    assert spectrum.parity.real < -0.8
    assert abs(spectrum.parity.imag) < 1.0e-12
    assert spectrum.bulk_radius < abs(spectrum.parity)


def test_spectral_trace_and_parity_bulk_decomposition() -> None:
    matrix = folded_gaussian_matrix(72, 0.07)
    spectrum = resolve_spectrum(matrix)
    for length in range(2, 7):
        spectral = trace_from_spectrum(spectrum, length)
        direct = np.trace(np.linalg.matrix_power(matrix, length))
        resolved = spectrum.perron**length + spectrum.parity**length + bulk_trace_from_spectrum(
            spectrum, length
        )
        assert abs(spectral - direct) < 2.0e-11
        assert abs(spectral - resolved) < 2.0e-13


def test_bulk_det2_trace_series_matches_eigenvalue_product() -> None:
    spectrum = resolve_spectrum(folded_gaussian_matrix(80, 0.065))
    traces = {length: bulk_trace_from_spectrum(spectrum, length) for length in range(2, 101)}
    z = 0.7
    from_traces = regularized_determinant_from_traces(traces, z, maximum_length=100)
    from_product = exact_bulk_det2(spectrum, z)
    assert abs(from_traces - from_product) < 2.0e-11


def test_fixed_noise_long_trace_returns_to_one() -> None:
    spectrum = resolve_spectrum(folded_gaussian_matrix(96, 0.08))
    assert abs(trace_from_spectrum(spectrum, 300) - 1.0) < 5.0e-8
