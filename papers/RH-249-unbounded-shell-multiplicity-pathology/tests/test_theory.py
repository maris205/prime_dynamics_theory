import numpy as np

from cone_reachability import (
    minimum_weight_cap_for_tolerance,
    solve_bounded_nonnegative,
    solve_nonnegative_cone,
)


def test_cone_primal_dual_and_minimum_cap():
    difference = np.array([2.0])
    matrix = np.array([[0.5]])
    orders = np.array([2])
    cone = solve_nonnegative_cone(difference, matrix, orders)
    assert cone["distance"] < 1e-12
    assert abs(cone["primal_dual_gap"]) < 1e-12
    cap = minimum_weight_cap_for_tolerance(difference, matrix, orders, tolerance=0.0)
    assert cap["feasible"] is True
    assert abs(cap["minimum_cap"] - 4.0) < 1e-10
    bounded = solve_bounded_nonnegative(difference, matrix, orders, upper_weight=3.0)
    assert abs(bounded["distance"] - 0.25) < 1e-12
