import math

from bridge_clock import complement_tail_bound, critical_slope, target_tail_bound


def test_critical_slope():
    assert math.isclose(critical_slope(), 1.0 / math.log(10.0 / 7.0))


def test_critical_tail_bounds_decay():
    assert complement_tail_bound(1e-8) < complement_tail_bound(1e-4)
    assert target_tail_bound(1e-8) < target_tail_bound(1e-4)


def test_critical_complement_bound_is_logarithmic():
    sigma = 1e-8
    m = math.ceil(critical_slope() * math.log(1.0 / sigma))
    assert complement_tail_bound(sigma) <= 40.0 / (3.0 * m)
