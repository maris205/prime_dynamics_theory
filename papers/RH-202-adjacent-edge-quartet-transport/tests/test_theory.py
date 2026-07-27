import numpy as np

from quartet_transport import (
    biorthogonal_eigenpacket,
    coefficient_error,
    haar_embedding,
    matched_assignment,
    principal_data,
)


def test_haar_embedding_and_principal_data():
    embedding = haar_embedding(8)
    assert np.linalg.norm(embedding.T @ embedding - np.eye(4)) < 1e-14
    data = principal_data(embedding[:, :2], embedding[:, :2])
    assert data["maximum_principal_sine"] < 1e-7


def test_matching_and_polynomial_are_permutation_invariant():
    values = np.array([0.5 + 0.2j, 0.5 - 0.2j, -0.3 + 0.4j, -0.3 - 0.4j])
    permuted = values[[2, 0, 3, 1]]
    assignment = matched_assignment(values, permuted)
    assert np.max(np.abs(values - permuted[assignment])) < 1e-14
    assert coefficient_error(values, permuted)["relative_l2_coefficient_error"] < 1e-14


def test_biorthogonal_packet_projector():
    rng = np.random.default_rng(202)
    right = rng.normal(size=(8, 3)) + 1j * rng.normal(size=(8, 3))
    left = rng.normal(size=(8, 3)) + 1j * rng.normal(size=(8, 3))
    vectors, duals, projector = biorthogonal_eigenpacket(right, left)
    assert np.linalg.norm(duals.conj().T @ vectors - np.eye(3)) < 1e-11
    assert np.linalg.norm(projector @ projector - projector) < 1e-10
