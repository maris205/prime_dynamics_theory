from __future__ import annotations

import numpy as np

from cycle_spectrum.invariants import (
    centered_trace_derivatives,
    centered_trace_moments,
    cycle_affinity,
    cycle_affinity_from_kernel,
    exact_dobrushin_coefficient,
)
from cycle_spectrum.operators import (
    fold_matrix,
    gaussian_markov_family,
    nonperron_spectrum,
)


def test_normalization_folding_and_nonzero_spectrum() -> None:
    _, matrix, derivative = gaussian_markov_family(80, 1.5436890127, 0.12)
    folded = fold_matrix(matrix)
    assert np.max(np.abs(matrix.sum(axis=1) - 1.0)) < 2.0e-15
    assert np.max(np.abs(derivative.sum(axis=1))) < 2.0e-13
    assert np.max(np.abs(folded.sum(axis=1) - 1.0)) < 2.0e-15

    full_nonzero = nonperron_spectrum(matrix)
    full_nonzero = full_nonzero[np.abs(full_nonzero) > 1.0e-6]
    folded_nonperron = nonperron_spectrum(folded)
    folded_nonperron = folded_nonperron[np.abs(folded_nonperron) > 1.0e-6]
    for value in folded_nonperron:
        assert np.min(np.abs(full_nonzero - value)) < 2.0e-9
    assert len(full_nonzero) == len(folded_nonperron)


def test_exact_cycle_affinity() -> None:
    parameters = (-0.71, 0.13, 0.82, 1.47, 0.19)
    direct = cycle_affinity_from_kernel(*parameters)
    closed = cycle_affinity(*parameters)
    assert abs(direct - closed) < 2.0e-13


def test_exact_dobrushin_against_endpoint_quadrature() -> None:
    u = 1.3
    sigma = 0.45
    result = exact_dobrushin_coefficient(u, sigma)
    y = np.linspace(-1.0, 1.0, 200_001)
    means = (result["lower_mean"], result["upper_mean"])
    rows = []
    for mean in means:
        weight = np.exp(-0.5 * ((y - mean) / sigma) ** 2)
        rows.append(weight / np.trapezoid(weight, y))
    quadrature_tv = 0.5 * np.trapezoid(np.abs(rows[0] - rows[1]), y)
    assert abs(quadrature_tv - result["delta"]) < 2.0e-10


def test_centered_trace_identity_and_derivative() -> None:
    d = 96
    u = 1.52
    sigma = 0.11
    _, matrix, derivative = gaussian_markov_family(d, u, sigma)
    folded = fold_matrix(matrix)
    folded_derivative = fold_matrix(derivative)
    orders = (2, 3, 4, 5)
    moments = centered_trace_moments(folded, orders)
    eigenvalues = nonperron_spectrum(folded)
    for n in orders:
        assert abs(moments[n] - np.sum(eigenvalues**n)) < 2.0e-10

    analytic = centered_trace_derivatives(folded, folded_derivative, orders)
    epsilon = 2.0e-6
    plus = fold_matrix(gaussian_markov_family(d, u + epsilon, sigma)[1])
    minus = fold_matrix(gaussian_markov_family(d, u - epsilon, sigma)[1])
    plus_moments = centered_trace_moments(plus, orders)
    minus_moments = centered_trace_moments(minus, orders)
    for n in orders:
        finite_difference = (plus_moments[n] - minus_moments[n]) / (2.0 * epsilon)
        assert abs(finite_difference - analytic[n]) < 2.0e-6
