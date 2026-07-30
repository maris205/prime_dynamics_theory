import math

from alias_ledger import (
    alias_count,
    alias_growth_exponent,
    alias_order_slope,
    alias_weight,
    beta_limit,
    minimal_bridge_slope,
)


def test_alias_ordering_and_counts():
    assert alias_order_slope(1) < minimal_bridge_slope() < alias_order_slope(2)
    assert alias_order_slope(2) < 4.0 < alias_order_slope(3)
    assert alias_count(minimal_bridge_slope()) == 1
    assert alias_count(4.0) == 2
    assert alias_count(100.0) == math.ceil(100.0 * math.log(1.678573510428322)) - 1
    for alias_index in (1, 13, 26, 52):
        assert alias_count(alias_order_slope(alias_index)) == alias_index - 1


def test_aliases_amplify():
    assert beta_limit() * 1.4 > 1.0
    assert math.isclose(alias_growth_exponent(2), 2 * alias_growth_exponent(1))
    assert alias_weight(12, 2) > alias_weight(12, 1)
