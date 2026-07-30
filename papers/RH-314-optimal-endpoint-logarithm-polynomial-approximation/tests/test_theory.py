import math

from endpoint_approximation import best_log_error, logarithmic_tail_energy, tail_energy_bounds


def test_tail_is_between_integral_bounds():
    for degree in (3, 10, 100):
        lower, upper = tail_energy_bounds(degree)
        value = logarithmic_tail_energy(degree)
        assert lower <= value <= upper


def test_scaled_error_tends_to_one():
    assert abs(best_log_error(2000) * math.sqrt(2000) - 1.0) < 5e-4


def test_error_is_strictly_decreasing():
    assert best_log_error(64) < best_log_error(16)
