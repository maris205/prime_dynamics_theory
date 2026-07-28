import numpy as np

from adaptive_jet import trace_jet_distance, trace_jet_norm, triangle_tolerance_bound


def test_triangle_tolerance_bound():
    first = np.asarray([0.0, 0.02, 0.01])
    second = np.asarray([0.0, -0.01, 0.005])
    assert trace_jet_distance(first, second) <= trace_jet_norm(first) + trace_jet_norm(second)
    assert abs(triangle_tolerance_bound(0.2, 0.1) - 0.3) < 1e-15
