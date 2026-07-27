import numpy as np

from finite_clock import clock_window_metrics, normalized_orbit, weighted_cycle


def test_weighted_cycle_power_is_scalar():
    norms = [1.0, 2.0, 3.0, 5.0, 7.0]
    cycle, weights = weighted_cycle(norms, 0, 4, wrap_phase=-1.0)
    expected = -float(np.prod(weights)) * np.eye(4)
    assert np.linalg.norm(np.linalg.matrix_power(cycle, 4) - expected, 2) < 1e-12


def test_exact_periodic_orbit_has_zero_clock_defects():
    operator = np.array([
        [0.0, 0.0, 0.0, 1.0],
        [1.0, 0.0, 0.0, 0.0],
        [0.0, 1.0, 0.0, 0.0],
        [0.0, 0.0, 1.0, 0.0],
    ])
    seed = np.array([[1.0], [0.0], [0.0], [0.0]])
    _, norms, units = normalized_orbit(operator, seed, 4)
    metrics = clock_window_metrics(operator, norms, units, 0, 4)
    assert metrics["marked_wrap_chord"] < 1e-12
    assert metrics["primal_relative_residual"] < 1e-12
    assert metrics["adjoint_relative_residual"] < 1e-12
    assert metrics["cycle_phase_rms_error"] < 1e-12
