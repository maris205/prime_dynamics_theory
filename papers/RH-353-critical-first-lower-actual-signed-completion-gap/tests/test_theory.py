from fractions import Fraction

import pytest

from boundary_completion_gap import (
    FIXTURE_LAMBDA,
    LAMBDA_LOWER,
    LAMBDA_UPPER,
    Q,
    R,
    R_H,
    boundary_completion,
    finite_rows,
    minimax_certificate,
    rate_certificate,
    weighted_supply_bound,
)


def test_physical_constant_interval_and_fixture_are_strict():
    assert LAMBDA_LOWER == Fraction(28, 17)
    assert LAMBDA_UPPER == Fraction(17, 10)
    assert LAMBDA_LOWER < FIXTURE_LAMBDA < LAMBDA_UPPER
    assert R_H == Fraction(17, 20)
    assert Q == Fraction(1, 2)
    assert R == Fraction(7, 5)


def test_two_order_rate_certificate_is_subunit():
    data = rate_certificate()
    assert data["rho_noisy"] == R_H**2 * FIXTURE_LAMBDA**3 / 4
    assert data["rho_target"] == 1 / FIXTURE_LAMBDA
    assert data["rho_max"] == data["rho_noisy"]
    assert data["normalized_rates_subunit"] is True


def test_global_rate_certificates_are_exact():
    data = rate_certificate()
    assert data["rho_noisy_upper"] == Fraction(1_419_857, 1_600_000)
    assert data["rho_noisy_upper"] < 1
    assert data["rho_target_upper"] == Fraction(17, 28)
    assert data["rho_target_upper"] < 1


@pytest.mark.parametrize(
    "gamma",
    [Fraction(1), FIXTURE_LAMBDA, Fraction(15, 8), Fraction(2)],
)
def test_phase_free_gap_is_exact_for_every_fixture(gamma):
    data = boundary_completion(gamma)
    assert data["gap_identity_exact"] is True
    assert data["phase_free_gap"] == 2 - FIXTURE_LAMBDA
    assert data["finite_formula_only"] is True


def test_critical_and_lower_formulas_use_one_phase_scalar():
    gamma = Fraction(7, 4)
    data = boundary_completion(gamma)
    assert data["critical_Z"] == 2 - gamma
    assert data["first_lower_Z"] == 1 - gamma / FIXTURE_LAMBDA


def test_exact_minimax_optimizer_and_opposite_errors():
    data = minimax_certificate()
    assert data["optimizer_gamma"] == Fraction(15, 8)
    assert data["minimax_value"] == Fraction(1, 8)
    assert data["critical_at_optimizer"] == Fraction(1, 8)
    assert data["first_lower_at_optimizer"] == Fraction(-1, 8)
    assert data["opposite_equal_errors"] is True


def test_global_gap_and_minimax_certificates_are_strict():
    data = minimax_certificate()
    assert data["global_lower_certificate"] == Fraction(1, 9)
    assert data["strictly_above_global_certificate"] is True
    assert data["gap_lower_certificate"] == Fraction(3, 10)
    assert data["strict_gap_certificate"] is True


def test_weighted_triangle_bound_recovers_minimax_lower_bound():
    data = minimax_certificate()
    bound = weighted_supply_bound(
        data["critical_at_optimizer"], data["first_lower_at_optimizer"]
    )
    assert bound["triangle_bound_exact"] is True
    assert bound["gap"] == 2 - FIXTURE_LAMBDA
    assert bound["implied_lower_bound"] == data["minimax_value"]


def test_finite_rows_preserve_input_count_and_scope():
    rows = finite_rows((1, Fraction(3, 2), 2))
    assert len(rows) == 3
    assert all(row["gap_identity_exact"] for row in rows)
    assert all(row["finite_formula_only"] for row in rows)


@pytest.mark.parametrize("bad_lambda", [LAMBDA_LOWER, LAMBDA_UPPER, 1, 2])
def test_lambda_domain_fails_closed(bad_lambda):
    with pytest.raises(ValueError):
        rate_certificate(bad_lambda)
    with pytest.raises(ValueError):
        boundary_completion(1, bad_lambda)


@pytest.mark.parametrize("bad_gamma", [0, -1, Fraction(-1, 3)])
def test_phase_scalar_must_be_positive(bad_gamma):
    with pytest.raises(ValueError):
        boundary_completion(bad_gamma)


def test_empty_fixture_family_fails_closed():
    with pytest.raises(ValueError):
        finite_rows(())


def test_boolean_inputs_are_not_integer_coerced():
    with pytest.raises(TypeError):
        rate_certificate(True)
    with pytest.raises(TypeError):
        boundary_completion(True)
    with pytest.raises(TypeError):
        weighted_supply_bound(True, 0)
