import math

import pytest

from shrinking_annulus import (
    critical_gap_constant,
    critical_tail_scale,
    logarithmic_gap,
    minimal_slope,
    radius_is_certified,
    shrinking_radius,
)


def test_critical_constant_is_reciprocal_slope():
    assert math.isclose(critical_gap_constant() * minimal_slope(), 1.0)


def test_subcritical_and_supercritical_scales():
    critical = critical_gap_constant()
    sigma = 1e-80
    assert critical_tail_scale(sigma, 0.5 * critical) < 1.0
    assert math.isclose(critical_tail_scale(sigma, critical), 1.0)
    assert critical_tail_scale(sigma, 1.5 * critical) > 1.0


def test_gap_shrinks():
    assert logarithmic_gap(1e-80, 0.1) < logarithmic_gap(1e-20, 0.1)


def test_reported_supercritical_radius_remains_certified():
    coefficient = 1.5 * critical_gap_constant()
    assert radius_is_certified(1e-80, coefficient)
    assert shrinking_radius(1e-80, coefficient) > 1.4


def test_tail_scale_validates_inputs():
    with pytest.raises(ValueError):
        critical_tail_scale(2.0, 0.1)
