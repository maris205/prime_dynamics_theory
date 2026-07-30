import math

from prefix_rate import (
    critical_exponent,
    minimal_bridge_slope,
    saturated_budget,
    weighted_geometric_sum,
)


def test_weighted_sum_asymptotic():
    for cut in (80, 160):
        ratio = (
            weighted_geometric_sum(cut)
            * cut
            * (1.4 - 1.0)
            / 1.4**cut
        )
        assert abs(ratio - 1.0) < 0.05


def test_target_critical_exponent():
    expected = math.log(1.4) / math.log(10.0 / 7.0)
    assert math.isclose(critical_exponent(minimal_bridge_slope()), expected)


def test_three_rate_regimes():
    beta_star = critical_exponent(minimal_bridge_slope())
    assert saturated_budget(1e-10, beta_star) < saturated_budget(1e-5, beta_star)
    assert saturated_budget(1e-10, 1.1) < saturated_budget(1e-5, 1.1)
    assert saturated_budget(1e-10, 0.8) > saturated_budget(1e-5, 0.8)
