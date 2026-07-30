import math

from clock_separation import (
    clearance_exponent,
    localization_slope,
    tail_decay_exponent,
    tail_slope,
)


def test_clock_intervals_are_disjoint():
    assert tail_slope() > localization_slope()
    assert math.isclose(tail_slope(), 1.0 / math.log(10.0 / 7.0))


def test_localization_clock_fails_tail_bound():
    assert tail_decay_exponent(localization_slope()) < 0.0
    assert clearance_exponent(tail_slope()) > 0.0
