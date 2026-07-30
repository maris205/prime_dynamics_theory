import math

from critical_alias import (
    absolute_matching_exponent,
    alias_growth_exponent,
    first_alias_clearance_exponent,
    localization_slope,
    minimal_clearance_exponent,
    parity_alias_exponent,
)


def test_alias_and_parity_exponents_coincide():
    assert math.isclose(alias_growth_exponent(), parity_alias_exponent())


def test_first_alias_is_exactly_clearance_critical():
    assert math.isclose(first_alias_clearance_exponent(), 0.0, abs_tol=1e-15)
    assert math.isclose(alias_growth_exponent(), 0.46340694451700304)


def test_first_alias_is_localization_clock():
    assert math.isclose(localization_slope(), 1.9307094191869356)


def test_matching_and_clearance_exponents():
    assert math.isclose(absolute_matching_exponent(), 0.6496301165394711)
    assert minimal_clearance_exponent() > 0.45
