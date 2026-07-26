import numpy as np

from history_cocycle import (
    apply_history_cocycle,
    apply_history_cocycle_adjoint,
    cocycle_extreme_singular_values,
    history_cocycle_matrix,
)


def test_matrix_action_and_adjoint():
    rng = np.random.default_rng(9)
    operator = rng.normal(size=(4, 4))
    values = rng.normal(size=(12, 2))
    target = rng.normal(size=(16, 2))
    matrix = history_cocycle_matrix(operator, 3, 0.7)
    assert np.linalg.norm(matrix @ values - apply_history_cocycle(values, operator, 0.7)) < 1e-13
    assert np.linalg.norm(matrix.T @ target - apply_history_cocycle_adjoint(target, operator, 0.7)) < 1e-13


def test_extreme_singular_values():
    operator = np.diag([0.2, 1.4])
    matrix = history_cocycle_matrix(operator, 4, 0.8)
    observed = np.linalg.svd(matrix, compute_uv=False)
    largest, smallest = cocycle_extreme_singular_values(operator, 4, 0.8)
    assert abs(observed[0] - largest) < 1e-14
    assert abs(observed[-1] - smallest) < 1e-14
