import numpy as np

from quartic_flow import coefficient_comparison, monic_coefficients, newton_traces


def test_newton_traces_recover_power_sums_beyond_degree():
    roots = np.array([0.2 + 0.4j, 0.2 - 0.4j, -0.3 + 0.5j, -0.3 - 0.5j])
    coefficients = monic_coefficients(roots)
    traces = newton_traces(coefficients, 9)
    direct = np.array([np.sum(roots**power) for power in range(1, 10)])
    assert np.max(np.abs(traces - direct)) < 1e-12


def test_coefficients_are_permutation_invariant():
    roots = np.array([1, 2, 3, 4], dtype=complex)
    assert coefficient_comparison(roots, roots[[2, 0, 3, 1]])["relative_l2_error"] < 1e-14


def test_constant_term_is_determinant():
    roots = np.array([1j, -1j, 2j, -2j])
    assert abs(monic_coefficients(roots)[-1] - np.prod(roots)) < 1e-14
