import numpy as np

from trace_coherence import trace_jet_distance


def test_trace_jet_distance_is_a_seminorm_distance():
    first = np.asarray([3.0, 0.2, -0.1, 0.04])
    second = np.asarray([-7.0, 0.2, -0.1, 0.04])
    assert trace_jet_distance(first, second) == 0.0
    third = np.asarray([0.0, 0.3, -0.1, 0.04])
    assert abs(trace_jet_distance(first, third) - 0.05) < 1e-14


def test_radius_monotonicity():
    first = np.asarray([0.0, 0.2, 0.1])
    second = np.zeros(3)
    assert trace_jet_distance(first, second, radius=0.5) < trace_jet_distance(first, second)
