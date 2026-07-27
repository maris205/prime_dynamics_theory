import numpy as np

from gauge_divisor import gauge_shape_parameters, raw_coefficients, raw_roots, route_coordinate


def test_gauge_shape_roundtrip():
    roots = raw_roots(0.07, 0.8, 0.61, -0.12)
    recovered = gauge_shape_parameters(roots)
    assert abs(recovered["center"] - 0.07) < 1e-12
    assert abs(recovered["radius"] - 0.8) < 1e-12
    assert abs(recovered["u"] - 0.61) < 1e-12
    assert abs(recovered["eta"] + 0.12) < 1e-12
    assert np.max(np.abs(np.poly(roots) - raw_coefficients(0.07, 0.8, 0.61, -0.12))) < 1e-12


def test_route_coordinate_requires_growing_divisor_next():
    statuses = {key: True for key in (
        "shape_manifold_exact", "gauge_reconstruction_exact", "simple_recurrence_rejected", "fixed_quartic_counting_rejected"
    )}
    statuses["rank_growing_divisor_constructed"] = False
    assert route_coordinate(statuses) == "finite_gauge_complete_shape_flow_open_rank_growing_divisor"
