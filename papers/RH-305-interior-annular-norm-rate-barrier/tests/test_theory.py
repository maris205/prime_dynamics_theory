import math

import pytest

from annular_rate import (
    Q_STAR,
    coefficient_norm_lower_bound,
    forced_odd_order,
    odd_anchor,
    rate_ceiling,
)


def test_rho_1p41_rate_ceiling():
    assert math.isclose(rate_ceiling(1.41), 0.035045705260961034)


def test_ceiling_decreases_toward_endpoint():
    assert rate_ceiling(1.405) > rate_ceiling(1.41) > rate_ceiling(1.42)


def test_lower_bound_decreases_with_mass():
    assert coefficient_norm_lower_bound(1e8, 1.41) < coefficient_norm_lower_bound(
        1e4, 1.41
    )


def test_forced_order_really_forces_half_anchor_mismatch():
    mass = 1e12
    order = forced_odd_order(mass)
    assert order % 2 == 1
    assert mass * 0.5 ** (order - 2) <= 0.5 * odd_anchor(order)
    assert math.isclose(
        coefficient_norm_lower_bound(mass, 1.41),
        0.5 * odd_anchor(order) * 1.41**order / order,
    )


def test_small_mass_lower_bound_stays_finite_and_annulus_is_strict():
    assert coefficient_norm_lower_bound(1e-100, 1.41) < 1.0
    with pytest.raises(ValueError):
        rate_ceiling(1.4)
    with pytest.raises(ValueError):
        rate_ceiling(1.0 / Q_STAR)
