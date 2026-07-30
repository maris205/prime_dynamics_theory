import math

from parity_majorant import (
    bulk_leading_coefficient,
    growth_exponent,
    minimal_bridge_slope,
    parity_budget,
)


def test_fixed_order_sign_and_scale():
    assert bulk_leading_coefficient(2) > 0.0
    assert bulk_leading_coefficient(3) < 0.0


def test_minimal_clock_is_supercritical_for_parity_majorant():
    assert growth_exponent(minimal_bridge_slope()) > 0.0
    expected = minimal_bridge_slope() * math.log(1.4 / 0.85) - 0.5
    assert math.isclose(growth_exponent(minimal_bridge_slope()), expected)


def test_parity_budget_grows():
    assert parity_budget(1e-8) > parity_budget(1e-4)
