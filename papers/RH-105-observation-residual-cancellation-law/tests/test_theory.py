from __future__ import annotations

import math

import pytest

from observation_cancellation import (
    block_observability_factor,
    full_observability_factor,
    matched_scale_factors,
    nonnegative_cancellation_power,
    signed_cancellation_power,
    weighted_residual_upper,
)


def test_observability_and_weighted_bounds() -> None:
    omega = block_observability_factor(4.0, 0.5)
    assert omega >= math.sqrt(4.0 / 0.75)
    assert full_observability_factor(9.0) >= 3.0
    assert weighted_residual_upper(omega, 0.25) >= omega * 0.25


def test_signed_cancellation_power() -> None:
    assert signed_cancellation_power(0.5, 0.75) == pytest.approx(-0.25)
    assert nonnegative_cancellation_power(0.5, 0.75) == 0.0
    assert nonnegative_cancellation_power(0.5, 0.25) == pytest.approx(0.25)


def test_matched_scale_identity() -> None:
    left, right = matched_scale_factors(0.01, 20.0, 5.0e-4)
    assert left >= 2.0
    assert right >= 5.0e-3
    assert left * right >= 20.0 * 5.0e-4


def test_validation() -> None:
    with pytest.raises(ValueError):
        block_observability_factor(1.0, 1.0)
    with pytest.raises(ValueError):
        matched_scale_factors(0.0, 1.0, 1.0)
    with pytest.raises(ValueError):
        full_observability_factor(-1.0)
