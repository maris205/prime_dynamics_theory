import numpy as np

from anchored_prefix import (
    anchored_log_jet_distance,
    disjoint_ball_margin,
    extracted_moments,
    scan_anchored_prefixes,
)


def test_anchor_distance_and_triangle_ball_margin():
    target = np.array([1.0, 0.0], dtype=complex)
    residual = np.array([0.0, 0.0, 0.0], dtype=complex)
    assert anchored_log_jet_distance(residual, target) == 0.5
    assert disjoint_ball_margin(0.5, 0.1) == 0.3


def test_extracted_moments_and_prefix_scan():
    full = np.array([0.0, 4.0, 8.0], dtype=complex)
    roots = np.array([1.0, -1.0], dtype=complex)
    moments = extracted_moments(full, 0.0, 0.0, roots)
    np.testing.assert_allclose(moments, [0.0, 2.0, 8.0])

    shells = [np.array([1.0, -1.0]), np.array([0.5, -0.5])]
    result = scan_anchored_prefixes(
        shells,
        full,
        0.0,
        0.0,
        np.array([2.0, 8.0]),
        tolerance=1e-12,
        minimum_rank=2,
    )
    assert result["selected"] is not None
    assert np.asarray(result["selected"]["cloud"]).size == 2


def test_equal_radius_balls_are_disjoint_when_anchor_exceeds_twice_tolerance():
    assert disjoint_ball_margin(0.49450543569144195, 0.04) > 0.0
    assert disjoint_ball_margin(0.49450543569144195, 0.04) == (
        0.49450543569144195 - 0.08
    )
