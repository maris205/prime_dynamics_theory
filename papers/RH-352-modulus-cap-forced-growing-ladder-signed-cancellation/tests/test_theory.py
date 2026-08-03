from fractions import Fraction

import pytest

from modulus_cap_cancellation import (
    FIXTURE_LAMBDA,
    LAMBDA_LOWER,
    LAMBDA_UPPER,
    Q,
    R,
    R_H,
    coordinate_caps,
    finite_identity_witness,
    rate_certificate,
    window_caps,
)


def test_physical_constant_interval_and_fixture_are_strict():
    assert LAMBDA_LOWER == Fraction(28, 17)
    assert LAMBDA_UPPER == Fraction(17, 10)
    assert LAMBDA_LOWER < FIXTURE_LAMBDA < LAMBDA_UPPER
    assert R_H == Fraction(17, 20)
    assert Q == Fraction(1, 2)
    assert R == Fraction(7, 5)


def test_exact_x_and_weight_dominance_identity():
    data = rate_certificate()
    assert data["x_lambda"] == Fraction(784, 289)
    assert data["x_lambda"] > 2
    assert data["x"] > 1


def test_normalized_rate_formulas_are_exact_and_subunit():
    data = rate_certificate()
    assert data["rho_noisy"] == R_H**2 * FIXTURE_LAMBDA**3 / 4
    assert data["rho_target"] == 1 / FIXTURE_LAMBDA
    assert data["rho_max"] == data["rho_noisy"]
    assert data["normalized_rates_subunit"] is True


def test_global_strict_rational_rate_certificates():
    data = rate_certificate()
    assert data["rho_noisy_upper"] == Fraction(1_419_857, 1_600_000)
    assert data["rho_noisy_upper"] < 1
    assert data["rho_target_upper"] == Fraction(17, 28)
    assert data["rho_target_upper"] < 1


def test_raw_noisy_barrier_is_strictly_superunit():
    data = rate_certificate()
    assert data["raw_noisy_lower"] == Fraction(9_604, 7_225)
    assert data["raw_noisy_lower"] > 1
    assert data["raw_noisy_root"] > data["raw_noisy_lower"]
    assert data["raw_target_root"] < 1


def test_scale_conversion_is_exact():
    data = rate_certificate()
    assert data["scale_conversion_exact"] is True
    assert data["x"] * data["rho_noisy"] == data["raw_noisy_root"]


def test_coordinate_caps_reproduce_source_formulas():
    k, j = 20, 4
    m = k - j
    data = coordinate_caps(k, j)
    b_noisy = Q**2 * R_H**2 * FIXTURE_LAMBDA
    assert data["normalized_noisy_cap"] == (
        Fraction(2, m) * FIXTURE_LAMBDA ** (2 * k) * b_noisy**m
    )
    assert data["normalized_target_cap"] == (
        Fraction(24, m) * FIXTURE_LAMBDA ** (-m)
    )
    assert data["normalized_direct_cap"] == (
        data["normalized_noisy_cap"] + data["normalized_target_cap"]
    )


def test_coordinate_raw_and_normalized_caps_convert_exactly():
    data = coordinate_caps(32, 7)
    assert data["noisy_scale_conversion_exact"] is True
    assert data["target_scale_conversion_exact"] is True
    assert data["finite_fixture_only"] is True


def test_growing_window_fixture_has_expected_coordinate_count():
    data = window_caps(64, 8)
    assert data["coordinate_count"] == 7
    assert data["max_normalized_coordinate_j"] == 8
    assert data["max_raw_noisy_coordinate_j"] == 8
    assert data["all_scale_conversions_exact"] is True


def test_finite_identity_witness_locks_Y_equals_S_minus_P_plus_p():
    witness = finite_identity_witness(
        (8, 5, 3),
        (8, 3, 1),
        (Fraction(1, 64), Fraction(-1, 81), Fraction(1, 125)),
    )
    assert witness["direct_identity_exact"] is True
    assert witness["tracking_error_equals_direct_exact"] is True
    assert witness["tracking_error"] == witness["direct"]
    assert witness["physical_trace_observation"] is False


@pytest.mark.parametrize("bad_lambda", [Fraction(28, 17), Fraction(17, 10), 1, 2])
def test_lambda_range_fails_closed(bad_lambda):
    with pytest.raises(ValueError):
        rate_certificate(bad_lambda)


@pytest.mark.parametrize(
    "args",
    [
        (4, 2),
        (10, 1),
        (10, 10),
    ],
)
def test_coordinate_domain_fails_closed(args):
    with pytest.raises(ValueError):
        coordinate_caps(*args)


def test_window_domain_and_ledger_lengths_fail_closed():
    with pytest.raises(ValueError):
        window_caps(20, 2)
    with pytest.raises(ValueError):
        window_caps(20, 20)
    with pytest.raises(ValueError):
        finite_identity_witness((1, 2), (1,), (0, 0))


def test_boolean_inputs_are_not_silently_integer_coerced():
    with pytest.raises(TypeError):
        coordinate_caps(True, 2)
    with pytest.raises(TypeError):
        coordinate_caps(10, False)
    with pytest.raises(TypeError):
        window_caps(10, True)
