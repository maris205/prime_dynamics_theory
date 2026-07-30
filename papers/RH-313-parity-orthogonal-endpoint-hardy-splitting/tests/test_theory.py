import math

from parity_hardy import parity_projection, singular_coefficient, split_energy


def test_singular_linear_term_is_cancelled():
    assert singular_coefficient(1) == 0.0
    assert singular_coefficient(3) == -1.0 / 3.0


def test_parity_projection_is_disjoint():
    values = [complex(index, -index) for index in range(8)]
    even = parity_projection(values, "even")
    odd = parity_projection(values, "odd")
    assert all(even[index] == 0 for index in range(1, 8, 2))
    assert all(odd[index] == 0 for index in range(0, 8, 2))


def test_energy_is_pythagorean():
    even, odd, total = split_energy([0.0, 1.0, 2.0, 3.0])
    assert math.isclose(total, even + odd)
