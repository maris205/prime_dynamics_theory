import numpy as np

from polynomial_selector import (
    interpolation_coefficients,
    nodal_idempotence_error,
    polynomial_values,
    selected_power_traces,
)


def test_complex_polynomial_coordinates_still_realize_binary_mask():
    roots = np.asarray([0.4 + 0.3j, 0.4 - 0.3j, -0.2 + 0j])
    mask = np.asarray([1.0, 1.0, 0.0])
    coefficients = interpolation_coefficients(roots, mask)
    np.testing.assert_allclose(polynomial_values(coefficients, roots), mask, atol=1e-12)
    assert nodal_idempotence_error(coefficients, roots) < 1e-12
    assert np.max(np.abs(coefficients.imag)) < 1e-12


def test_selected_power_trace_is_masked_spectral_sum():
    roots = np.asarray([0.5, -0.25])
    mask = np.asarray([1.0, 0.0])
    traces = selected_power_traces(roots, mask, np.asarray([2, 3]))
    np.testing.assert_allclose(traces, np.asarray([0.25, 0.125]))
