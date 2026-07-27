import numpy as np
import pytest

from transport_certification import eigenpair_condition, isolation_budget, transport_residual


def test_normal_eigenpair_condition_is_one():
    assert abs(eigenpair_condition(np.array([1.0, 0.0]), np.array([1.0, 0.0])) - 1.0) < 1e-14


def test_isolation_budget_and_transport_residual():
    assert abs(isolation_budget(0.01, 2.0, 0.2) - 0.2) < 1e-14
    coarse = np.diag([0.2, 0.1])
    fine = np.diag([0.2, 0.1, -0.3])
    embedding = np.eye(3, 2)
    assert transport_residual(fine, embedding, np.array([1.0, 0.0]), 0.2) < 1e-14


def test_zero_pairing_is_rejected():
    with pytest.raises(ValueError):
        eigenpair_condition(np.array([1.0, 0.0]), np.array([0.0, 1.0]))
