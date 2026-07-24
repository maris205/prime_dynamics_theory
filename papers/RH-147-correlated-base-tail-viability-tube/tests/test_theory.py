from __future__ import annotations

import math

from correlated_tube import cocycle_lower, support, support_factor, tube_base_requirement, tube_multiplier


def test_tube_boundary_is_exact() -> None:
    beta = 2e-5
    y = 0.36
    required = tube_base_requirement(beta, y)
    assert math.isclose(support(y, required), beta, rel_tol=1e-13)
    assert support(y, 0.99 * required) < beta


def test_superunit_tail_has_empty_positive_slice() -> None:
    assert support_factor(1.0) == 0.0
    assert support_factor(4.0) == 0.0
    assert math.isinf(tube_base_requirement(1e-8, 1.0))


def test_cocycle_keeps_positive_recoveries() -> None:
    floor, path = cocycle_lower(0.2, [0.5, 4.0, 0.5, 2.0])
    assert math.isclose(floor, 0.1)
    assert math.isclose(path[-1], 0.4)


def test_sharp_transition_multiplier() -> None:
    y0, y1, a0, ratio = 0.04, 0.01, 0.3, 0.8
    multiplier = tube_multiplier(y0, y1, ratio)
    assert math.isclose(support(y1, ratio * a0), multiplier * support(y0, a0), rel_tol=1e-13)


def test_negative_log_drift_is_sharp_obstruction() -> None:
    floor, path = cocycle_lower(1.0, [0.5] * 20)
    assert floor == path[-1]
    assert path[-1] < 1e-5
