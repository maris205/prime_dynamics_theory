import math
import numpy as np

from relative_affine_tail import optimize_fixed_floor, relative_affine_coefficients


def test_relative_coefficients_and_sharp_scalar_case():
    source = np.diag([2.0, 1.0])
    target = np.diag([1.0, 0.5])
    forcing = np.diag([0.1, 0.2])
    result = relative_affine_coefficients(source, target, np.eye(2), 0.25, forcing)
    assert abs(result["metric_factor"] - 2.0) < 1e-12
    assert abs(result["rho"] - 0.5) < 1e-12
    assert abs(result["q"] - 0.4) < 1e-12


def test_optimization_and_metric_gap_obstruction():
    result = optimize_fixed_floor(0.1, 0.02, 0.05)
    assert result["contractive_feasible"]
    assert result["rho"] < 1.0
    assert result["fixed_floor"] < 1.0
    assert not optimize_fixed_floor(1.1, 0.0, 0.0)["contractive_feasible"]
    epsilon = 1e-8
    gram = np.diag([1.0, epsilon**2])
    forcing = np.diag([0.0, epsilon])
    coefficients = relative_affine_coefficients(np.eye(2), gram, np.eye(2), 0.0, forcing)
    assert np.linalg.norm(forcing, 2) == epsilon
    assert coefficients["q"] > 1e7
