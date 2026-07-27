import numpy as np

from canonical_packet import balanced_packet, exact_packet_metrics


def test_balanced_exact_packet_on_diagonal_matrix_states():
    A = np.diag([0.2 + 0.3j, 0.2 - 0.3j, -0.4, 0.7])
    S = np.eye(4, 2, dtype=complex)
    right = np.column_stack([
        np.outer(np.eye(4)[:, index], np.array([1.0, 0.2])).reshape(-1)
        for index in (0, 1)
    ])
    left = np.column_stack([
        np.outer(np.eye(4)[:, index], np.array([0.7, -0.1])).reshape(-1)
        for index in (0, 1)
    ])
    packet = balanced_packet(right, left)
    metrics = exact_packet_metrics(A, packet["right_frame"], packet["left_frame"], S.shape)
    assert metrics["biorthogonality_defect"] < 1e-12
    assert metrics["right_residual_norm"] < 1e-12
    assert metrics["left_residual_norm"] < 1e-12
    assert np.allclose(sorted(np.linalg.eigvals(metrics["compressed"]), key=lambda z: z.imag), sorted(np.diag(A)[:2], key=lambda z: z.imag))
