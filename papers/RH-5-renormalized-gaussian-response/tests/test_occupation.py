import numpy as np
import scipy.sparse as sp

from gaussian_response.occupation import occupation_weighted_average, row_normalize_csr


def test_csr_normalization_uses_row_indices_not_column_indices():
    matrix = sp.csr_matrix(
        np.array(
            [
                [1.0, 2.0, 0.0],
                [0.0, 3.0, 1.0],
                [4.0, 0.0, 1.0],
            ]
        )
    )
    normalized = row_normalize_csr(matrix).toarray()
    np.testing.assert_allclose(np.sum(normalized, axis=1), 1.0)
    np.testing.assert_allclose(normalized[0], [1.0 / 3.0, 2.0 / 3.0, 0.0])
    np.testing.assert_allclose(normalized[1], [0.0, 3.0 / 4.0, 1.0 / 4.0])


def test_occupation_weighting_matches_exact_flow_definition():
    kernels = np.array(
        [
            [[0.8, 0.2], [0.1, 0.9]],
            [[0.6, 0.4], [0.3, 0.7]],
            [[0.5, 0.5], [0.4, 0.6]],
        ]
    )
    occupations = np.array([[0.9, 0.1], [0.5, 0.5], [0.2, 0.8]])
    actual = occupation_weighted_average(kernels, occupations)

    numerator = sum(np.diag(nu) @ kernel for nu, kernel in zip(occupations, kernels))
    denominator = np.sum(occupations, axis=0)
    expected = numerator / denominator[:, None]
    np.testing.assert_allclose(actual, expected)
    np.testing.assert_allclose(np.sum(actual, axis=1), 1.0)


def test_occupation_bias_is_exact_rowwise_covariance():
    rng = np.random.default_rng(20260713)
    raw = rng.random((17, 4, 4))
    kernels = raw / np.sum(raw, axis=2, keepdims=True)
    occupations = rng.random((17, 4))

    weighted = occupation_weighted_average(kernels, occupations)
    unweighted = np.mean(kernels, axis=0)
    mean_occupation = np.mean(occupations, axis=0)
    covariance = np.mean(
        (occupations - mean_occupation)[..., None]
        * (kernels - unweighted[None, ...]),
        axis=0,
    )
    np.testing.assert_allclose(weighted - unweighted, covariance / mean_occupation[:, None])
