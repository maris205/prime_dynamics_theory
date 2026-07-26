import numpy as np

from double_cycle_cloud import cloud_factor, double_cycle_determinant, double_cycle_eigenvalues, double_cycle_trace


def test_double_cycle_is_exact_cloud_factor():
    degree = 7
    parameter = 0.4 + 0.2j
    assert abs(double_cycle_determinant(degree, parameter) - cloud_factor(degree, parameter)) < 1e-12


def test_trace_ledger():
    degree = 5
    eigenvalues = double_cycle_eigenvalues(degree)
    for power in range(1, 13):
        assert abs(np.sum(eigenvalues ** power) - double_cycle_trace(degree, power)) < 1e-12
