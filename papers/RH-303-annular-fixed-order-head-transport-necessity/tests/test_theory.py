import math

from head_necessity import coefficient_error, head_transport_bound


def test_coefficient_bound():
    assert math.isclose(coefficient_error(2.0, 2.0, 3), 0.75)


def test_head_bound_adds_all_typed_errors():
    value = head_transport_bound(0.1, 0.2, 0.3, 2.0, 2)
    assert math.isclose(value, 0.45)
