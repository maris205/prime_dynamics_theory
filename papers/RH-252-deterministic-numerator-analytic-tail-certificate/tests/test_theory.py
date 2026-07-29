import math

import pytest

from deterministic_tail import (
    cauchy_tail_factor,
    logarithmic_target_tail_bound,
    multiplicative_tail_error,
    scaled_zero_free_radius,
)


def test_scaled_zero_free_radius_exceeds_unit_disk():
    radius = scaled_zero_free_radius(0.85, 1.6785735104283177)
    assert abs(radius - 1.42678748386407) < 1e-14
    assert radius > 1.0


def test_cauchy_tail_factor_is_geometric_series():
    factor = cauchy_tail_factor(1.0, 1.2, 13)
    expected = (1.0 / 1.2) ** 13 / (1.0 - 1.0 / 1.2)
    assert abs(factor - expected) < 1e-14
    assert abs(logarithmic_target_tail_bound(2.5, 1.0, 1.2, 13) - 2.5 * expected) < 1e-14


def test_exponential_conversion_and_domain_checks():
    assert abs(multiplicative_tail_error(0.1) - math.expm1(0.1)) < 1e-15
    with pytest.raises(ValueError):
        cauchy_tail_factor(1.0, 1.0, 13)
    with pytest.raises(ValueError):
        logarithmic_target_tail_bound(-1.0, 1.0, 1.2, 13)
