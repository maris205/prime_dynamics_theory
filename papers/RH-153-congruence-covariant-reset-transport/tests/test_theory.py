import numpy as np
import pytest

from reset_congruence import correlated_base_lower, inverse_congruence_radius, normalized_base


def generalized_top(gram: np.ndarray, tail: np.ndarray) -> float:
    values, vectors = np.linalg.eigh(gram)
    inverse = vectors @ np.diag(values ** -0.5) @ vectors.T
    return float(np.linalg.eigvalsh(inverse @ tail @ inverse)[-1])


def test_normalized_base() -> None:
    assert normalized_base(1.0, 4.0) == 0.5
    assert correlated_base_lower(1.0, 4.0, 0.2) == 0.1


def test_congruence_ratio_invariance() -> None:
    gram = np.diag([4.0, 1.0])
    tail = np.array([[0.8, 0.1], [0.1, 0.2]])
    overlap = np.array([[0.7, 0.1], [0.0, 0.3]])
    inverse = np.linalg.inv(overlap)
    assert generalized_top(gram, tail) == pytest.approx(
        generalized_top(inverse.T @ gram @ inverse, inverse.T @ tail @ inverse)
    )


def test_sharp_base_example() -> None:
    gram = np.diag([9.0, 1.0])
    overlap = np.diag([0.2, 1.0])
    inverse = np.linalg.inv(overlap)
    pulled = inverse.T @ gram @ inverse
    actual = np.sqrt(np.linalg.eigvalsh(pulled)[0] / np.linalg.eigvalsh(pulled)[-1])
    assert actual == pytest.approx(correlated_base_lower(1.0, 9.0, 0.2))


def test_inverse_radius() -> None:
    result = inverse_congruence_radius(0.8, 0.1, 2.0, 0.01)
    assert result["stable"]
    assert result["overlap_lower"] == pytest.approx(0.7)
    assert result["radius"] > 0.01 / 0.7**2


def test_invalid() -> None:
    with pytest.raises(ValueError):
        normalized_base(2.0, 1.0)
