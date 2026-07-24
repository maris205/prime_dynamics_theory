import math
import numpy as np

from semidefinite_directional import floor_distortion, fp_supported_rank, support_restricted_rayleigh


def test_singular_support_and_kernel_obstruction():
    gram = np.diag([4.0, 1.0, 0.0])
    tail = np.diag([1.0, 0.25, 0.0])
    result = support_restricted_rayleigh(gram, tail, tolerance=1e-12)
    assert result["support_rank"] == 2
    assert result["kernel_compatible"]
    assert abs(result["full_space_gamma"] - 0.5) < 1e-12
    obstructed = support_restricted_rayleigh(gram, tail + np.diag([0.0, 0.0, 1e-3]), tolerance=1e-12)
    assert not obstructed["kernel_compatible"]
    assert math.isinf(obstructed["full_space_gamma"])


def test_fp_support_and_floor_distortion():
    action = np.diag([1.0, 1e-4, 1e-8, 1e-18])
    result = fp_supported_rank(action, multiplier=32.0)
    assert result["rank"] == 3
    distortion = floor_distortion(np.array([1e-20, 1e-8, 1.0]), 1e-12)
    assert distortion["floor_to_weakest_ratio"] == 1e8
