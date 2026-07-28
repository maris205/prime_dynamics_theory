import numpy as np

from shell_zonotope import (
    binary_subset_count,
    solve_binary_selection,
    solve_box_zonotope,
    weighted_distance,
)


def test_box_primal_dual_identity_on_scalar_example():
    difference = np.array([1.5])
    matrix = np.array([[1.0]])
    orders = np.array([2])
    result = solve_box_zonotope(difference, matrix, orders)
    assert abs(result["distance"] - 0.25) < 1e-12
    assert abs(result["primal_dual_gap"]) < 1e-12


def test_binary_and_subset_count():
    difference = np.array([1.1, 0.0])
    matrix = np.array([[1.0, 0.2], [0.0, 1.0]])
    orders = np.array([2, 3])
    result = solve_binary_selection(difference, matrix, orders)
    assert abs(result["distance"] - weighted_distance(difference - matrix @ np.array([1.0, 0.0]), orders)) < 1e-10
    assert binary_subset_count(np.array([2, 2, 1]), minimum_rank=3) == 4
