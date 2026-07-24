import numpy as np
import pytest

from factorized_packet import factorized_gap_lower, hybrid_packet_gate, projector_radius


def test_factorized_gap_is_exact_for_orthogonal_factors():
    left = np.diag([3.0, 2.0, 1.0])
    right = np.eye(3)
    assert factorized_gap_lower(left, right) == pytest.approx(1.0 / 14.0)


def test_factorized_gap_is_a_lower_bound_for_general_factors():
    rng = np.random.default_rng(142)
    left = rng.normal(size=(8, 3))
    right = rng.normal(size=(3, 7))
    product = left @ right
    gram = product.T @ product / np.sum(product * product)
    nonzero = np.linalg.eigvalsh(gram)[-3:]
    assert factorized_gap_lower(left, right) <= nonzero[0] * (1 + 1e-12)


def test_hybrid_rescues_a_failed_frobenius_gate():
    result = hybrid_packet_gate(1.0, 0.6, 0.4)
    assert result["method"] == "interval_eigen"
    assert result["certified"]
    assert result["projector_radius"] == pytest.approx(2.0 / 3.0)
    assert projector_radius(1.0, 0.5) is None


def test_invalid_factorization_is_rejected():
    with pytest.raises(ValueError):
        factorized_gap_lower(np.ones((2, 2)), np.ones((3, 2)))
    with pytest.raises(ValueError):
        hybrid_packet_gate(-1.0, 0.1)

