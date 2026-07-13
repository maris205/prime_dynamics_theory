import numpy as np

from gaussian_response.operator import (
    FixedSupportGaussianFamily,
    dense_gaussian_matrices,
)


def infinity_norm(matrix):
    return np.max(np.sum(np.abs(matrix), axis=1))


def test_dense_reference_has_exact_stochastic_derivative_sums():
    kernel, first, second = dense_gaussian_matrices(d=73, sigma=0.061, u=1.5437)
    np.testing.assert_allclose(np.sum(kernel, axis=1), 1.0, atol=2.0e-15)
    np.testing.assert_allclose(np.sum(first, axis=1), 0.0, atol=2.0e-13)
    np.testing.assert_allclose(np.sum(second, axis=1), 0.0, atol=2.0e-11)


def test_sparse_full_support_matches_dense_reference():
    d = 61
    sigma = 0.073
    u = 1.519
    expected = dense_gaussian_matrices(d=d, sigma=sigma, u=u)
    family = FixedSupportGaussianFamily(d=d, sigma=sigma, u_ref=u, cutoff=None)
    actual = family.matrices(u)
    for sparse_matrix, dense_matrix in zip(actual, expected):
        np.testing.assert_allclose(sparse_matrix.toarray(), dense_matrix, rtol=2e-14, atol=2e-14)


def test_analytic_derivatives_match_fixed_support_finite_differences():
    d = 91
    sigma = 0.052
    u = 1.5437
    first_step = 5.0e-6
    second_step = 5.0e-4
    family = FixedSupportGaussianFamily(
        d=d,
        sigma=sigma,
        u_ref=u,
        cutoff=6.0,
        parameter_radius=2.0 * second_step,
    )
    kernel, first, second = (matrix.toarray() for matrix in family.matrices(u))
    first_plus = family.matrix(u + first_step).toarray()
    first_minus = family.matrix(u - first_step).toarray()
    finite_first = (first_plus - first_minus) / (2.0 * first_step)
    second_plus = family.matrix(u + second_step).toarray()
    second_minus = family.matrix(u - second_step).toarray()
    second_plus_two = family.matrix(u + 2.0 * second_step).toarray()
    second_minus_two = family.matrix(u - 2.0 * second_step).toarray()
    finite_second = (
        -second_plus_two
        + 16.0 * second_plus
        - 30.0 * kernel
        + 16.0 * second_minus
        - second_minus_two
    ) / (12.0 * second_step * second_step)
    assert infinity_norm(first - finite_first) < 2.0e-7
    assert infinity_norm(second - finite_second) < 1.0e-6


def test_truncation_l1_error_is_twice_omitted_mass():
    d = 121
    sigma = 0.055
    u = 1.5437
    full = dense_gaussian_matrices(d=d, sigma=sigma, u=u)[0]
    family = FixedSupportGaussianFamily(d=d, sigma=sigma, u_ref=u, cutoff=3.25)
    truncated = family.matrix(u).toarray()

    for i in range(d):
        retained_mass = np.sum(full[i, family._lo[i] : family._hi[i]])
        omitted_mass = 1.0 - retained_mass
        row_error = np.sum(np.abs(full[i] - truncated[i]))
        np.testing.assert_allclose(row_error, 2.0 * omitted_mass, atol=3.0e-15)


def test_declared_parameter_padding_covers_interval():
    family = FixedSupportGaussianFamily(
        d=100,
        sigma=0.01,
        u_ref=1.54,
        cutoff=6.0,
        parameter_radius=0.03,
    )
    assert family.support_covers(1.51)
    assert family.support_covers(1.57)
    assert not family.support_covers(1.58)
