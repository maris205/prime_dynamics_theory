import numpy as np

from riesz_channels import (
    cross_channel_gram,
    normalized_eigenprojector,
    residue_normalized_frames,
    source_observation_channel,
)


def test_projector_channels_are_cross_diagonal_and_biorthogonal():
    A = np.array([[0.3, 1.0], [0.0, -0.4]], dtype=complex)
    values, right = np.linalg.eig(A)
    left_values, left_raw = np.linalg.eig(A.conj().T)
    source = np.array([[1.0, 0.2], [0.3, 0.7]], dtype=complex)
    observation = np.array([[0.4, 0.8], [-0.2, 0.5]], dtype=complex)
    projectors = []
    for index, value in enumerate(values):
        left_index = int(np.argmin(abs(left_values - np.conj(value))))
        projectors.append(normalized_eigenprojector(right[:, index], left_raw[:, left_index]))
    channels = [source_observation_channel(projector, source, observation) for projector in projectors]
    rights = [item["right_state"] for item in channels]
    lefts = [item["left_state"] for item in channels]
    residues = np.array([item["residue"] for item in channels])
    assert np.allclose(cross_channel_gram(rights, lefts), np.diag(residues), atol=1e-12)
    V, W = residue_normalized_frames(rights, lefts, residues)
    assert np.allclose(W.conj().T @ V, np.eye(2), atol=1e-12)
