import numpy as np

from frobenius_tail import det2_log_tail_upper, eigenvalue_squared_tail_budget


def test_eigenvalue_tail_budget_subtracts_selected_mass():
    selected = np.asarray([1.0, -0.5, 0.2j])
    assert abs(eigenvalue_squared_tail_budget(3.0, selected) - 1.71) < 1e-14


def test_det2_tail_upper_is_finite_inside_reciprocal_radius():
    assert abs(det2_log_tail_upper(2.0, 0.25, 1.0) - 4.0 / 3.0) < 1e-14
