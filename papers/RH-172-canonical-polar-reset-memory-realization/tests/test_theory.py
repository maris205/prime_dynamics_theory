import numpy as np
import pytest

from history_realization import (
    memory_gram,
    normalized_history_factor,
    polar_realization,
    spectral_formula_realization,
    subspace_distance,
    top_packet,
)


def test_history_factor_is_the_memory_gram():
    rng = np.random.default_rng(4)
    states = [rng.normal(size=(7, 5)) for _ in range(4)]
    factor = normalized_history_factor(states)
    assert np.linalg.norm(factor.T @ factor - memory_gram(states), 2) < 1e-14


def test_polar_packet_is_an_isometry():
    rng = np.random.default_rng(5)
    states = [rng.normal(size=(8, 6)) for _ in range(3)]
    factor = normalized_history_factor(states)
    values, packet = top_packet(memory_gram(states), 3)
    realized, positive = polar_realization(factor, packet)
    direct = spectral_formula_realization(factor, packet, values)
    assert np.linalg.norm(realized.T @ realized - np.eye(3), 2) < 1e-13
    assert np.linalg.norm(factor @ packet - realized @ positive, 2) < 1e-13
    assert subspace_distance(realized, np.linalg.qr(direct)[0]) < 1e-7


def test_rank_deficient_packet_is_rejected():
    factor = np.diag([1.0, 0.0])
    with pytest.raises(ValueError):
        polar_realization(factor, np.eye(2))
