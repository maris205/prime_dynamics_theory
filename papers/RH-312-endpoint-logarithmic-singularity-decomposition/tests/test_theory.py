import math

from endpoint_singularity import (
    even_endpoint_normalized_anchor,
    odd_normalized_anchor,
    regularity_radius_lower_bound,
)


def test_remainder_is_analytic_past_unit_circle():
    assert regularity_radius_lower_bound() > 1.0


def test_odd_anchor_approaches_one_exponentially():
    first = abs(odd_normalized_anchor(7) - 1.0)
    second = abs(odd_normalized_anchor(15) - 1.0)
    assert second < first


def test_even_endpoint_term_approaches_one():
    assert math.isclose(even_endpoint_normalized_anchor(60), 1.0, rel_tol=1e-12)
