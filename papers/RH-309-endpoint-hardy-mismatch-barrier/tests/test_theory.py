import math

from endpoint_hardy import (
    complement_endpoint_product,
    endpoint_h2_lower_bound,
    endpoint_odd_cutoff,
    endpoint_conversion_constant,
    model_target_hardy_tail_bounds,
    normalized_logarithmic_scale,
)


def test_endpoint_is_inside_complement_disk():
    assert complement_endpoint_product() < 1.0


def test_endpoint_conversion_constant():
    assert math.isclose(endpoint_conversion_constant(), 4.992111068649647)


def test_logarithmic_barrier_and_model_tail_decay():
    assert normalized_logarithmic_scale(1e12) < normalized_logarithmic_scale(1e6)
    assert model_target_hardy_tail_bounds(200)[1] < model_target_hardy_tail_bounds(100)[1]


def test_cutoff_forces_the_endpoint_tail_gap():
    mass = 1e12
    order = endpoint_odd_cutoff(mass)
    assert order % 2 == 1
    assert mass * 0.5 ** (order - 2) <= 0.25 * (1.0 / (0.85 * 1.678573510428322)) ** order
    assert endpoint_h2_lower_bound(mass) == (order, 1.0 / math.sqrt(32.0 * order))
