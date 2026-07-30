import math

from mass_demand import (
    mass_exponent,
    mass_saturation_slope,
    minimal_slope,
    necessary_mass,
)


def test_minimal_mass_exponent():
    assert math.isclose(mass_exponent(), 0.9468615163684616)
    assert 0.0 < 1.0 - mass_exponent() < 0.06


def test_saturation_clock_is_later():
    assert minimal_slope() < mass_saturation_slope()


def test_mass_demand_grows_with_order():
    assert necessary_mass(19) > necessary_mass(9)
