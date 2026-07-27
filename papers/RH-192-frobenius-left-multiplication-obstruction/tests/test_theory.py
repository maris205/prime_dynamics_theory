import numpy as np

from frobenius_obstruction import (
    characteristic_power,
    complement_count,
    complement_free_compatible,
    left_multiply,
    resolvent_norm_identity,
    riesz_rank,
    vectorized_left_operator,
)


def test_vectorized_left_action_and_determinant_power():
    A = np.array([[1.0, 2.0], [-0.5, 0.25]])
    X = np.arange(6.0).reshape(2, 3, order="F")
    L = vectorized_left_operator(A, 3)
    assert np.allclose(L @ X.reshape(-1, order="F"), left_multiply(A, X).reshape(-1, order="F"))
    z = 2.3 + 0.4j
    base = np.linalg.det(z * np.eye(2) - A)
    assert np.allclose(np.linalg.det(z * np.eye(6) - L), characteristic_power(base, 3))


def test_rank_count_and_resolvent_identities():
    assert riesz_rank(2, 7) == 14
    assert complement_count(1, 1, 64) == 63
    assert not complement_free_compatible(4, 64)
    assert complement_free_compatible(64, 64)
    base, ambient = resolvent_norm_identity(np.diag([0.2, -0.4]), 1.1 + 0.2j)
    assert abs(base - ambient) < 1e-12
