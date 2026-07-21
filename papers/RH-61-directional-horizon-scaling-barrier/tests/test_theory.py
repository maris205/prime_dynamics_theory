import math

import pytest

from horizon_scaling import (
    geometric_tail_envelope,
    log_power_fit,
    minimum_geometric_horizon,
    observed_horizon,
    slow_mode_horizon_lower_bound,
)


def test_geometric_envelope_and_minimum_horizon() -> None:
    tails = (2.0, 1.0)
    rates = (0.5, 0.25)
    assert geometric_tail_envelope(tails, rates, 0) == pytest.approx(3.0)
    assert geometric_tail_envelope(tails, rates, 2) == pytest.approx(0.5625)
    horizon = minimum_geometric_horizon(tails, rates, 0.6)
    assert horizon == 2
    assert geometric_tail_envelope(tails, rates, horizon) <= 0.6
    assert geometric_tail_envelope(tails, rates, horizon - 1) > 0.6


def test_slow_mode_bound_is_the_integer_threshold() -> None:
    q = 0.8
    amplitude = 1.0
    tolerance = 0.1
    horizon = slow_mode_horizon_lower_bound(q, amplitude, tolerance)
    assert horizon == math.ceil(math.log(10.0) / -math.log(q))
    assert amplitude * q**horizon <= tolerance
    assert amplitude * q ** max(0, horizon - 1) > tolerance


def test_observed_horizon_and_power_fit() -> None:
    assert observed_horizon({"0": 2.0, "4": 1.2, "8": 1.01}, 1.0, 0.02) == 8
    assert observed_horizon({0: 2.0, 4: 1.2}, 1.0, 0.02) is None
    fit = log_power_fit((1.0, 0.5, 0.25), (2.0, 4.0, 8.0))
    assert fit["power"] == pytest.approx(-1.0)
    assert fit["growth_exponent"] == pytest.approx(1.0)
    assert fit["maximum_log_residual"] < 1.0e-12


@pytest.mark.parametrize(
    "call",
    [
        lambda: geometric_tail_envelope((1.0,), (1.0,), 0),
        lambda: geometric_tail_envelope((1.0,), (0.5,), -1),
        lambda: minimum_geometric_horizon((1.0,), (0.5,), 0.0),
        lambda: slow_mode_horizon_lower_bound(0.0, 1.0, 0.1),
        lambda: observed_horizon({0: 1.0}, 1.0, -0.1),
        lambda: log_power_fit((1.0,), (1.0,)),
    ],
)
def test_invalid_inputs_are_rejected(call) -> None:
    with pytest.raises(ValueError):
        call()
