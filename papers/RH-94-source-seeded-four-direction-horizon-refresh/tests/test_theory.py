from __future__ import annotations

import numpy as np
import pytest

from source_seeded_refresh import (
    cross_energy_fraction,
    normalized_source_gram,
    orthogonality_defect,
    projector_distance,
    source_right_packet,
    top_gram_packet,
)


def test_source_seed_equivalence() -> None:
    source = np.array([[3.0, 0.0, 0.0], [0.0, 2.0, 0.0], [0.0, 0.0, 1.0]])
    svd_packet = source_right_packet(source, 2)
    gram_packet = top_gram_packet(normalized_source_gram(source), 2)
    assert projector_distance(svd_packet, gram_packet) < 1e-12
    assert orthogonality_defect(svd_packet) < 1e-12


def test_normalized_source_gram() -> None:
    source = np.arange(1.0, 13.0).reshape(4, 3)
    gram = normalized_source_gram(source)
    assert abs(np.trace(gram) - 1.0) < 1e-12
    assert np.linalg.eigvalsh(gram)[0] > -1e-12
    with pytest.raises(ValueError):
        normalized_source_gram(np.zeros((2, 2)))


def test_cross_energy_fraction() -> None:
    singular = np.array([4.0, 3.0, 2.0, 1.0])
    assert cross_energy_fraction(singular, 3) > 0.96
    with pytest.raises(ValueError):
        cross_energy_fraction(singular, 0)
