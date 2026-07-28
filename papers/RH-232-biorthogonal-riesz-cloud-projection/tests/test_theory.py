import numpy as np

from riesz_cloud import biorthogonal_projector_metrics, match_eigenvalues


def test_biorthogonal_projector_on_a_nonnormal_matrix():
    matrix = np.asarray([[0.7, 5.0], [0.0, 0.2]])
    right_values, right = np.linalg.eig(matrix)
    left_values, left = np.linalg.eig(matrix.T)
    indices, error = match_eigenvalues(left_values, right_values, conjugate_targets=True)
    metrics = biorthogonal_projector_metrics(right, left[:, indices])
    projector = right @ metrics["inverse_overlap"] @ left[:, indices].conj().T
    assert error < 1e-14
    assert np.linalg.norm(projector @ projector - projector) < 1e-12
    assert np.linalg.norm(matrix @ projector - projector @ matrix) < 1e-12


def test_matching_uses_distinct_indices():
    values = np.asarray([1.0, 0.5 + 0.2j, 0.5 - 0.2j])
    indices, error = match_eigenvalues(values, values[::-1])
    assert len(set(indices.tolist())) == 3
    assert error == 0.0
