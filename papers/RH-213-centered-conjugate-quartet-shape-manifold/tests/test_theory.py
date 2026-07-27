import numpy as np

from quartet_shape import (
    coefficient_manifold_residual,
    coordinates_from_roots,
    shape_coefficients,
    shape_roots,
)


def test_root_and_coefficient_formulas_agree():
    for u, eta in ((0.2, -0.4), (0.7, 0.1), (0.95, -0.8)):
        assert np.max(np.abs(np.poly(shape_roots(u, eta)) - shape_coefficients(u, eta))) < 1e-12


def test_coordinate_roundtrip_and_manifold_identity():
    u, eta = 0.43, -0.17
    recovered = coordinates_from_roots(shape_roots(u, eta))
    assert abs(recovered.u - u) < 1e-12
    assert abs(recovered.eta - eta) < 1e-12
    assert coefficient_manifold_residual(shape_coefficients(u, eta)) < 1e-12
