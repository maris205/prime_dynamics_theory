import numpy as np
import pytest

from bi_ritz_graph import directional_graph_certificate


def test_residual_identities():
    rng = np.random.default_rng(166)
    a = rng.normal(size=(8, 8))
    v, _ = np.linalg.qr(rng.normal(size=(8, 3)))
    p = v @ v.T
    q = np.eye(8) - p
    h = v.T @ a @ v
    right = a @ v - v @ h
    left = a.T @ v - v @ h.T
    assert np.linalg.norm(right, 2) == pytest.approx(np.linalg.norm(q @ a @ p, 2))
    assert np.linalg.norm(left, 2) == pytest.approx(np.linalg.norm(p @ a @ q, 2))


def test_directional_asymmetry():
    result = directional_graph_certificate(1.0, 1.0, 1.0, 10.0, 0.001)
    assert result["rank_certified"]
    assert result["primal_graph_slope_upper"] < result["dual_graph_slope_upper"]


def test_zero_right_residual_gives_zero_primal_slope():
    result = directional_graph_certificate(2.0, 2.0, 3.0, 100.0, 0.0)
    assert result["rank_certified"]
    assert result["primal_graph_slope_upper"] == 0.0


def test_failed_gate_and_invalid_data():
    assert not directional_graph_certificate(1.0, 2.0, 2.0, 1.0, 1.0)["rank_certified"]
    with pytest.raises(ValueError):
        directional_graph_certificate(1.0, 1.0, 1.0, -1.0, 1.0)
