import numpy as np

from transverse_quenching import coefficient_jacobian, coefficient_map, transverse_difference, transverse_lipschitz_bound


def test_jacobian_against_centered_difference():
    u, eta, h = 0.63, -0.11, 1e-6
    numerical = (coefficient_map(u, eta + h) - coefficient_map(u, eta - h)) / (2 * h)
    assert np.linalg.norm(numerical - coefficient_jacobian(u, eta)[:, 1]) < 1e-8


def test_uniform_transverse_bound_and_quenching():
    assert transverse_difference(0.6, -0.8, 0.9) <= transverse_lipschitz_bound(0.6) * 1.7 + 1e-14
    assert transverse_lipschitz_bound(0.999) < transverse_lipschitz_bound(0.9)
