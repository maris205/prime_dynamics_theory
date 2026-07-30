import math

from root_l1_clock import (
    critical_exponent,
    moment_error,
    padded_l1_cost,
    radial_pair_budget,
    transport_bound,
)


def test_padded_matching_controls_moments():
    left = [0.7 + 0.1j, 0.7 - 0.1j]
    right = [0.69 + 0.1j]
    cost = padded_l1_cost(left, right)
    cap = max(abs(value) for value in left + right)
    for order in (2, 3, 4):
        assert moment_error(left, right, order) <= order * cap ** (order - 1) * cost + 1e-14


def test_transport_bound_is_positive():
    assert transport_bound(0.01, 0.9, 1.4, 20) > 0.0


def test_radial_rate_threshold():
    slope = 1.0 / math.log(10.0 / 7.0)
    beta = 1.0 / (0.85 * math.sqrt(1.678573510428322))
    gamma = critical_exponent(slope, beta)
    assert radial_pair_budget(1e-8, gamma + 0.2, slope, beta) < radial_pair_budget(
        1e-4, gamma + 0.2, slope, beta
    )
