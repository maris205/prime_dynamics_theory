from __future__ import annotations

import numpy as np
from scipy.linalg import eigvals

from parity_boundary import (
    R_FIXED,
    U_CRITICAL,
    boundary_eigen_equation_residual,
    component_density,
    parity_boundary_profile,
    peripheral_spectrum,
    sparse_folded_gaussian_matrix,
    square_root_gap_constant,
)


def dense_folded_matrix(dimension: int, sigma: float) -> np.ndarray:
    grid = (np.arange(dimension, dtype=np.float64) + 0.5) / dimension
    means = 1.0 - U_CRITICAL * grid * grid
    destination = grid[None, :]
    log_positive = -0.5 * ((destination - means[:, None]) / sigma) ** 2
    log_negative = -0.5 * ((-destination - means[:, None]) / sigma) ** 2
    log_weights = np.logaddexp(log_positive, log_negative)
    log_weights -= np.max(log_weights, axis=1, keepdims=True)
    weights = np.exp(log_weights)
    return weights / np.sum(weights, axis=1, keepdims=True)


def test_sparse_operator_matches_dense_midpoint_spectrum() -> None:
    dimension = 128
    sigma = 0.05
    sparse = sparse_folded_gaussian_matrix(dimension, sigma)
    assert np.max(np.abs(np.asarray(sparse.sum(axis=1)).ravel() - 1.0)) < 5.0e-15
    sparse_data = peripheral_spectrum(sparse)
    dense_values = eigvals(dense_folded_matrix(dimension, sigma))
    dense_parity = dense_values[np.argmin(dense_values.real)]
    assert abs(sparse_data.perron - 1.0) < 2.0e-12
    assert abs(sparse_data.parity - dense_parity) < 3.0e-12


def test_component_density_value_is_taylor_stable() -> None:
    low = component_density(degree=80)
    high = component_density(degree=140)
    assert abs(low.eigenvalue - 1.0) < 5.0e-13
    assert abs(high.eigenvalue - 1.0) < 5.0e-13
    assert abs(low.interval_density_at_zero - high.interval_density_at_zero) < 2.0e-14
    assert abs(high.interval_density_at_zero - 0.562641254486572) < 3.0e-14
    assert R_FIXED < 0.7


def test_error_function_profile_solves_local_eigen_equation() -> None:
    for xi in (-4.0, -1.5, 0.0, 0.75, 3.0):
        assert abs(boundary_eigen_equation_residual(xi)) < 2.0e-11
    values = parity_boundary_profile(np.asarray([-20.0, 0.0, 20.0]))
    assert values[0] > 0.999999
    assert abs(values[1]) < 1.0e-15
    assert values[2] < -0.999999


def test_square_root_constant_reproduces_nested_integral() -> None:
    result = square_root_gap_constant()
    assert result.rho_c > 0.0
    assert result.kappa > 0.0
    assert result.endpoint_rate > 0.0
    assert result.quadrature_error < 2.0e-9
    assert abs(result.value - 0.105258535936908) < 3.0e-11


def test_small_noise_gap_is_in_square_root_crossover() -> None:
    sigma = 0.004
    matrix = sparse_folded_gaussian_matrix(2048, sigma)
    data = peripheral_spectrum(matrix, eigenvalue_count=4)
    assert -1.0 < data.parity.real < -0.98
    assert abs(data.parity.imag) < 1.0e-10
    scaled = data.parity_gap / np.sqrt(sigma)
    assert 0.10 < scaled < 0.14
