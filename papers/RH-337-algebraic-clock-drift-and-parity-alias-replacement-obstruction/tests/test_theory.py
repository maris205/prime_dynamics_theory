from fractions import Fraction

import pytest

from clock_drift import (
    C_M_HAT,
    C_STAR_HAT,
    LAMBDA_HAT,
    R_H,
    clock_diagnostics,
    exact_clock_certificate,
    lambda_polynomial,
    model_alias_packet,
    model_packet_audit,
    model_packet_scale,
    model_parity_packet,
    parity_binomial_bounds,
)


F = Fraction


def test_exact_polynomial_residual_certifies_Lambda_hat_above_physical_root():
    certificate = exact_clock_certificate()
    residual = certificate["polynomial_at_Lambda_hat"]
    assert lambda_polynomial(F(1)) == -11
    assert lambda_polynomial(F(2)) == 8
    assert residual == F(
        5765081705833725291502719395827,
        1953125000000000000000000000000000000000000000,
    )
    assert residual > 0
    assert F(1) < LAMBDA_HAT < F(2)
    assert certificate["Lambda_hat_greater_than_lambda"] is True
    assert certificate["R_over_r_H_squared"] == F(784, 289)
    assert certificate["R_over_r_H_squared_greater_than_two"] is True
    assert certificate["beta_R_greater_than_one_from_lambda_less_than_two"] is True


def test_hatted_constants_remain_exact_model_definitions():
    assert LAMBDA_HAT == F(2098216888035403, 1250000000000000)
    assert C_M_HAT == F(9731714526004839, 5000000000000000)
    assert C_STAR_HAT == F(26314633984227, 250000000000000)
    assert R_H == F(17, 20)


def test_exact_hatted_packets_obey_the_binomial_bounds():
    for k in (2, 3, 4, 6, 8):
        lower, upper = parity_binomial_bounds(k)
        parity = model_parity_packet(k)
        assert lower <= parity <= upper
        assert model_alias_packet(k) > 0
        assert model_packet_scale(k) > 0
    with pytest.raises(ValueError):
        model_parity_packet(1)
    with pytest.raises(ValueError):
        model_alias_packet(1)


def test_finite_audit_reproduces_common_hatted_scale_exactly():
    for k in (2, 3, 4, 6):
        audit = model_packet_audit(k)
        assert audit["parity"] == model_parity_packet(k)
        assert audit["alias"] == model_alias_packet(k)
        assert audit["common_model_scale"] == model_packet_scale(k)
        assert audit["parity_lower_bound"] <= audit["parity"]
        assert audit["parity"] <= audit["parity_upper_bound"]


def test_decimal_diagnostics_have_the_strict_signs_locked_exactly_elsewhere():
    diagnostics = clock_diagnostics()
    assert diagnostics["Lambda_hat_minus_lambda"] > 0
    assert diagnostics["physical_phase_slope"] < 0
    assert diagnostics["one_phase_unit_k"] > 6_000_000_000_000_000
    assert diagnostics["log_lambda_over_Lambda_hat"] < 0
