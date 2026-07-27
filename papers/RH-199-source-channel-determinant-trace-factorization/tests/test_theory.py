import numpy as np

from channel_determinant import (
    channel_transfer,
    feedback_determinant_ratio,
    modal_weighted_moments,
    power_traces,
    weighted_moments,
)


def test_feedback_determinant_and_moment_identities():
    K = np.diag([0.2 + 0.3j, 0.2 - 0.3j])
    b = np.ones(2)
    residues = np.array([0.4 + 0.1j, 0.4 - 0.1j])
    c = np.conj(residues)
    z = 1.3 + 0.4j
    transfer = channel_transfer(K, b, c, z)
    assert abs(feedback_determinant_ratio(K, b, c, z) - (1.0 - transfer)) < 1e-12
    assert np.allclose(weighted_moments(K, b, c, 6), modal_weighted_moments(np.diag(K), residues, 6))
    assert np.allclose(power_traces(K, 6), [np.sum(np.diag(K) ** power) for power in range(1, 7)])
