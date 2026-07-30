import math

from endpoint_obstruction import (
    BASE,
    endpoint_packet_coefficient,
    escaping_multiplicity,
    higher_endpoint_packet_coefficient,
    packet_mass_upper,
    packet_squared_mass,
    strict_radius_packet_coefficient,
)


def test_endpoint_coefficient_is_exactly_one():
    for order in (5, 10, 20):
        assert endpoint_packet_coefficient(order) == 1.0


def test_strict_radius_coefficient_decays():
    assert strict_radius_packet_coefficient(40, 1.41) < strict_radius_packet_coefficient(10, 1.41)


def test_packet_mass_is_bounded_by_rank_times_q_squared():
    order = 12
    multiplicity = escaping_multiplicity(order)
    upper = packet_mass_upper(order, multiplicity)
    assert upper == order * multiplicity * 0.25
    assert packet_squared_mass(order, multiplicity) <= upper


def test_higher_endpoint_coefficients_have_exact_multiplicity_decay():
    order = 20
    multiplicity = escaping_multiplicity(order)
    assert higher_endpoint_packet_coefficient(order, 1, multiplicity) == 1.0
    assert math.isclose(
        higher_endpoint_packet_coefficient(order, 2, multiplicity),
        1.0 / (2.0 * multiplicity),
    )


def test_packet_mass_has_the_claimed_logarithmic_clock():
    for order in (16, 32, 64):
        residual = abs(math.log(packet_squared_mass(order)) - order * math.log(BASE))
        assert residual <= 3.0 * math.log(order)
