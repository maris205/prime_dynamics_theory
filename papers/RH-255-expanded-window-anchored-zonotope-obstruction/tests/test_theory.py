import numpy as np

from expanded_reachability import (
    best_prefix_distance,
    shell_power_matrix,
    single_coefficient_box_gap,
)


def test_shell_power_matrix_preserves_conjugate_reality():
    shells = [np.asarray([0.5 + 0.2j, 0.5 - 0.2j]), np.asarray([-0.1])]
    matrix = shell_power_matrix(shells, np.asarray([2, 3]))
    assert np.max(np.abs(matrix.imag)) < 1e-15


def test_best_prefix_and_single_coordinate_gap():
    difference = np.asarray([1.0, 0.0])
    matrix = np.asarray([[0.4, 0.5], [0.0, 0.0]])
    result = best_prefix_distance(difference, matrix, np.asarray([2, 3]), np.asarray([2, 2]))
    assert result["rank"] == 4
    gap = single_coefficient_box_gap(difference, matrix, np.asarray([2, 3]))
    assert abs(gap["weighted_gap"] - 0.05) < 1e-15
    assert gap["order"] == 2
