import numpy as np

from pseudospectral_gap import triangular_projector_norm, triangular_spectral_projector


def test_fixed_gap_projector_growth():
    small = triangular_projector_norm(0.8, 0.5, 1.0)
    large = triangular_projector_norm(0.8, 0.5, 1.0e6)
    assert large > 1.0e5 * small


def test_triangular_projector_is_idempotent_and_reducing():
    matrix = np.asarray([[0.8, 7.0], [0.0, 0.5]])
    projector = triangular_spectral_projector(0.8, 0.5, 7.0)
    assert np.linalg.norm(projector @ projector - projector) < 1e-14
    assert np.linalg.norm(matrix @ projector - projector @ matrix) < 1e-14
