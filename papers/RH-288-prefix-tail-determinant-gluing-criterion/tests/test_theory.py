import math

from determinant_gluing import gluing_relative_error, weighted_prefix


def test_gluing_bound():
    assert math.isclose(gluing_relative_error(0.1, 0.2, 0.3), math.expm1(0.6))


def test_weighted_prefix_uses_order_weights():
    value = weighted_prefix([1.0, 1.0], 2.0, first_order=2)
    assert math.isclose(value, 2.0**2 / 2 + 2.0**3 / 3)
