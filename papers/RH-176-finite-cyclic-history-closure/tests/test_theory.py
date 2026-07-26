import numpy as np

from cyclic_history import cycle_matrix, geometric_section, reduced_cycle_determinant


def test_cycle_and_geometric_determinant():
    cycle = cycle_matrix(7)
    assert np.linalg.norm(np.linalg.matrix_power(cycle, 7) - np.eye(7)) < 1e-14
    value = 0.3 + 0.2j
    assert abs(reduced_cycle_determinant(7, value) - geometric_section(6, value)) < 1e-13


def test_orientation_is_scalar_determinant_invisible():
    value = -0.4 + 0.1j
    assert abs(reduced_cycle_determinant(9, value) - reduced_cycle_determinant(9, value, direction=-1)) < 1e-13
