import numpy as np

from riesz_transport import (
    channel_transport_decomposition,
    contour_projector_bound,
    resolvent_intertwining,
)


def test_resolvent_intertwining_identity():
    coarse = np.diag([0.2, -0.3])
    fine = np.diag([0.21, -0.28, 0.1])
    embedding = np.eye(3, 2)
    result = resolvent_intertwining(fine, coarse, embedding, 2.0 + 0.1j)
    assert result["absolute_identity_residual"] < 1e-13


def test_channel_transport_decomposition():
    rng = np.random.default_rng(3)
    pf = rng.normal(size=(5, 5))
    pc = rng.normal(size=(3, 3))
    sf = rng.normal(size=(5, 6))
    sc = rng.normal(size=(3, 4))
    row = np.linalg.qr(rng.normal(size=(5, 3)), mode="reduced")[0]
    column = np.linalg.qr(rng.normal(size=(6, 4)), mode="reduced")[0]
    result = channel_transport_decomposition(pf, pc, sf, sc, row, column)
    assert result["absolute_identity_residual"] < 1e-12
    assert np.linalg.norm(result["left"], "fro") <= result["triangle_upper_bound"] + 1e-12


def test_contour_bound_formula():
    assert abs(contour_projector_bound(2 * np.pi, 3.0, 4.0, 0.5) - 6.0) < 1e-14
