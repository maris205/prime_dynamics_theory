import math

import numpy as np
import pytest

from balanced_coupling import balance_data, similarity_certificate


def test_balance_optimum():
    data = balance_data(9.0, 1.0)
    assert data["optimal_scale"] == pytest.approx(1.0 / 3.0)
    assert data["balanced_coupling_infimum"] == 3.0
    assert data["similarity_condition"] == 3.0


def test_offdiagonal_norm_identity():
    rng = np.random.default_rng(164)
    b = rng.normal(size=(3, 4))
    c = rng.normal(size=(4, 3))
    t = 0.7
    zero3 = np.zeros((3, 3))
    zero4 = np.zeros((4, 4))
    e = np.block([[zero3, t * b], [c / t, zero4]])
    expected = max(t * np.linalg.norm(b, 2), np.linalg.norm(c, 2) / t)
    assert np.linalg.norm(e, 2) == pytest.approx(expected)


def test_certificate_and_triangular_case():
    result = similarity_certificate(1.0, 0.5, 4.0, 0.01)
    assert result["rank_certified"]
    assert result["balanced_neumann_product"] == pytest.approx(0.1)
    triangular = similarity_certificate(2.0 * math.pi, 3.0, 10.0, 0.0)
    assert triangular["rank_certified"]
    assert not triangular["graph_certified"]


def test_invalid():
    with pytest.raises(ValueError):
        balance_data(-1.0, 1.0)
