import math

from moment_packets import minimal_multiplicity, packet_power_sum, packet_radius


def test_packet_is_invisible_below_its_order():
    for power in range(1, 9):
        assert packet_power_sum(9, 4, 2.5, power) == 0.0


def test_packet_hits_the_selected_moment_exactly():
    assert packet_power_sum(7, 5, -3.25, 7) == -3.25


def test_higher_multiples_follow_the_exact_formula():
    assert math.isclose(packet_power_sum(3, 2, 6.0, 6), 6.0)


def test_minimal_multiplicity_enforces_radius_cap():
    multiplicity = minimal_multiplicity(10, 0.7**10, 0.5)
    assert packet_radius(10, multiplicity, 0.7**10) <= 0.5
