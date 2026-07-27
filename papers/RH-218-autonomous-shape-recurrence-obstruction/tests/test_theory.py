import numpy as np

from shape_recurrence import (
    evaluate_polynomial_shape_map,
    fit_affine_shape_map,
    lagrange_autonomous_map,
)


def test_affine_shape_map_recovers_affine_data():
    current = np.asarray([[0.1, -0.2], [0.3, 0.1], [0.7, -0.1], [0.9, 0.2]])
    matrix = np.asarray([[0.8, 0.1], [-0.2, 0.5]])
    offset = np.asarray([0.1, -0.03])
    following = current @ matrix.T + offset
    fit = fit_affine_shape_map(current, following)
    assert np.max(np.abs(fit(current) - following)) < 1e-12


def test_finite_orbit_has_polynomial_autonomous_map():
    states = np.asarray([[0.1, 0.0], [0.2, -0.1], [0.4, 0.05], [0.7, -0.2]])
    coefficients = lagrange_autonomous_map(states)
    assert np.max(np.abs(evaluate_polynomial_shape_map(coefficients, states[:-1]) - states[1:])) < 1e-12
