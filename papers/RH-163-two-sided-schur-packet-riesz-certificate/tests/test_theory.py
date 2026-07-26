import math

import numpy as np
import pytest

from schur_packet import scalar_block_norm, schur_certificate


def test_scalar_block_norm_matches_numpy():
    matrix = np.array([[1.2, 3.0], [0.4, -2.0]])
    assert scalar_block_norm(*matrix.ravel()) == pytest.approx(np.linalg.norm(matrix, 2))


def test_imbalanced_product_passes_when_symmetric_gate_fails():
    result = schur_certificate(1.0, 1.0, 1.0, 10.0, 0.01)
    assert result["rank_certified"]
    assert result["feedback_product"] == pytest.approx(0.1)
    assert result["symmetric_neumann_product"] == 10.0


def test_triangular_feedback_is_zero():
    result = schur_certificate(2.0 * math.pi, 2.0, 3.0, 1000.0, 0.0)
    assert result["rank_certified"]
    assert result["feedback_product"] == 0.0


def test_invalid_and_failed_gate():
    assert not schur_certificate(1.0, 2.0, 2.0, 1.0, 1.0)["rank_certified"]
    with pytest.raises(ValueError):
        schur_certificate(-1.0, 1.0, 1.0, 1.0, 1.0)
