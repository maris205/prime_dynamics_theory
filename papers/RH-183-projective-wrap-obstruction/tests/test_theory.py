import numpy as np

from wrap_obstruction import (
    best_scalar_wrap_residual,
    optimal_wrap_phase,
    phase_optimized_chord,
    projective_return_distance,
)


def test_phase_and_scalar_optima():
    seed = np.array([1.0, 0.0])
    endpoint = np.array([-0.8, 0.6])
    assert optimal_wrap_phase(seed, endpoint) == -1.0
    assert abs(phase_optimized_chord(seed, endpoint) - np.sqrt(0.4)) < 1e-12
    assert abs(projective_return_distance(seed, endpoint) - 0.6) < 1e-12
    result = best_scalar_wrap_residual(seed, endpoint, 2.0)
    assert abs(result["minimum_residual"] - 1.2) < 1e-12


def test_orthogonal_endpoint_is_unrepairable_by_phase():
    seed = np.array([1.0, 0.0])
    endpoint = np.array([0.0, 1.0])
    assert abs(phase_optimized_chord(seed, endpoint) - np.sqrt(2.0)) < 1e-12
    assert projective_return_distance(seed, endpoint) == 1.0
