import numpy as np

from procrustes_shell import optimal_shell_map, procrustes_residual_from_cosines


def test_identical_embedded_packet_has_zero_cost():
    embedding = np.eye(7, 4)
    coarse = np.eye(4, 2)
    fine = embedding @ coarse
    result = optimal_shell_map(coarse, fine, embedding)
    assert result["optimal_frobenius_residual"] < 1e-7
    transport = result["transport"]
    assert np.linalg.norm(transport @ coarse - fine) < 1e-12


def test_partial_isometry_projectors():
    rng = np.random.default_rng(5)
    coarse = np.linalg.qr(rng.normal(size=(6, 3)), mode="reduced")[0]
    fine = np.linalg.qr(rng.normal(size=(9, 3)), mode="reduced")[0]
    embedding = np.linalg.qr(rng.normal(size=(9, 6)), mode="reduced")[0]
    result = optimal_shell_map(coarse, fine, embedding)
    transport = result["transport"]
    assert np.linalg.norm(transport.conj().T @ transport - coarse @ coarse.T) < 1e-12
    assert np.linalg.norm(transport @ transport.conj().T - fine @ fine.T) < 1e-12


def test_residual_formula():
    data = procrustes_residual_from_cosines(np.array([1.0, 0.5]))
    assert abs(data["optimal_frobenius_residual"] - 1.0) < 1e-14
