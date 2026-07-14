from __future__ import annotations

import numpy as np

from validated_gap import (
    LAMBDA_FIXED,
    certify_reduced_gap,
    leading_eigenvalues,
    reduced_beta_one_matrix,
    sector_matrices,
    taylor_ingredients,
)


def test_taylor_ingredients_are_stable_and_positive() -> None:
    ingredients = taylor_ingredients(40, 0.7)
    assert np.all(ingredients.inverse_square > 0.0)
    assert np.all(ingredients.beta_one_weight > 0.0)
    assert np.all(ingredients.beta_two_odd_weight > 0.0)
    assert abs(np.sum(ingredients.inverse_square) - 0.3622233962) < 2.0e-9


def test_floating_spectra_match_fredholm_diagnostics() -> None:
    degree = 80
    reduced = reduced_beta_one_matrix(degree, 0.7)
    _, odd_second = sector_matrices(degree, 0.7)
    leading_one = leading_eigenvalues(reduced, 1)[0]
    leading_two = leading_eigenvalues(odd_second, 1)[0]
    assert abs(leading_one.imag) < 1.0e-13
    assert abs(leading_two.imag) < 1.0e-13
    assert abs(leading_one.real - 0.20788029772254) < 2.0e-13
    assert abs(leading_two.real - 0.15252823980512) < 2.0e-13


def test_taylor_traces_match_circle_flat_traces() -> None:
    expected_one = [
        0.23849119781623518,
        0.04394054638900302,
        0.009002525937583883,
        0.0018679794144809136,
    ]
    expected_two = [
        0.1829255670361356,
        0.023976300252288668,
        0.0035670780045273798,
        0.0005417428719470957,
    ]
    reduced = reduced_beta_one_matrix(100, 0.7)
    _, odd_second = sector_matrices(100, 0.7)
    power_one = np.eye(reduced.shape[0])
    power_two = np.eye(odd_second.shape[0])
    for index in range(4):
        power_one = power_one @ reduced
        power_two = power_two @ odd_second
        assert abs(np.trace(power_one) - expected_one[index]) < 3.0e-12
        assert abs(np.trace(power_two) - expected_two[index]) < 3.0e-12


def test_arb_certificate_closes_both_gaps() -> None:
    result = certify_reduced_gap(
        decimal_precision=70,
        dimension=50,
        tail_degree=100,
    )
    assert result.beta_one_certified
    assert result.beta_two_certified
    assert result.beta_one_cube_bound < result.lam**-6
    assert result.beta_two_square_bound < result.lam**-4
    assert result.beta_one_radius_bound < result.lam**-2
    assert result.beta_two_radius_bound < result.lam**-2
    assert result.beta_one_radius_bound < 1 / 3
    assert result.beta_two_radius_bound < 1 / 3
    assert abs(float(result.target_radius.lower()) - LAMBDA_FIXED**-2) < 2.0e-16
