import math

from weighted_diagonal import certified_budget, level_tolerance, weighted_sum


def test_level_budget_is_exact():
    for level in (2, 5, 10, 40):
        assert math.isclose(certified_budget(level), 1.0 / level)


def test_tolerance_decreases():
    assert level_tolerance(20) < level_tolerance(10)
    assert weighted_sum(20) > weighted_sum(10)
