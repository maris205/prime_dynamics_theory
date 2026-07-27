import numpy as np

from residue_cocycle import diagonal_multipliers, optimal_common_scalar


def test_diagonal_cocycle_is_exact_and_composes():
    first = np.array([1 + 2j, 1 - 2j])
    second = np.array([0.4 + 0.3j, 0.4 - 0.3j])
    third = np.array([0.2 - 0.1j, 0.2 + 0.1j])
    one = diagonal_multipliers(first, second)
    two = diagonal_multipliers(second, third)
    assert np.linalg.norm(one * first - second) < 1e-14
    assert np.linalg.norm(two * one - diagonal_multipliers(first, third)) < 1e-14


def test_optimal_common_scalar():
    coarse = np.array([1.0, 2.0, 3.0])
    fine = 2j * coarse
    result = optimal_common_scalar(coarse, fine)
    assert abs(result["scalar"] - 2j) < 1e-14
    assert result["relative_residual"] < 1e-14


def test_branch_dependent_scaling_has_positive_scalar_residual():
    coarse = np.ones(2)
    fine = np.array([1.0, -1.0])
    assert optimal_common_scalar(coarse, fine)["relative_residual"] > 0.99
