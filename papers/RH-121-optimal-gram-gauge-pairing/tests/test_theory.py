from __future__ import annotations

import numpy as np
import pytest

from optimal_gram_gauge import normalized_tail_spectrum, optimal_exact_gram_gauge


def spd(rng: np.random.Generator) -> np.ndarray:
    x = rng.normal(size=(4, 4))
    return x.T @ x + 0.3 * np.eye(4)


def random_gram_gauge(g: np.ndarray, gp: np.ndarray, rng: np.random.Generator) -> np.ndarray:
    vg, ug = np.linalg.eigh(g)
    vgp, ugp = np.linalg.eigh(gp)
    inv = (ug * vg**-0.5) @ ug.T
    rootp = (ugp * vgp**0.5) @ ugp.T
    q, _ = np.linalg.qr(rng.normal(size=(4, 4)))
    return inv @ q @ rootp


def tail_factor(dp: np.ndarray, transported: np.ndarray) -> float:
    values, vectors = np.linalg.eigh(transported)
    inverse = (vectors * values**-0.5) @ vectors.T
    return float(np.linalg.eigvalsh(inverse @ dp @ inverse)[-1])


def test_exact_alignment_and_optimality() -> None:
    rng = np.random.default_rng(121)
    for _ in range(20):
        g, d, gp, dp = spd(rng), spd(rng), spd(rng), spd(rng)
        result = optimal_exact_gram_gauge(g, d, gp, dp)
        s = result["gauge"]
        assert np.linalg.norm(s.T @ g @ s - gp, 2) < 2e-10
        for _ in range(30):
            trial = random_gram_gauge(g, gp, rng)
            assert result["optimal_tail_factor"] <= tail_factor(dp, trial.T @ d @ trial) + 2e-9


def test_diagonal_matching_formula() -> None:
    g = np.eye(4)
    gp = np.eye(4)
    d = np.diag([1.0, 2.0, 4.0, 8.0])
    dp = np.diag([3.0, 5.0, 9.0, 12.0])
    result = optimal_exact_gram_gauge(g, d, gp, dp)
    assert result["optimal_tail_factor"] == pytest.approx(max(3.0, 2.5, 2.25, 1.5))
    assert normalized_tail_spectrum(g, d).tolist() == pytest.approx([1.0, 2.0, 4.0, 8.0])


def test_validation() -> None:
    with pytest.raises(ValueError):
        optimal_exact_gram_gauge(np.eye(4), np.diag([0.0, 1.0, 1.0, 1.0]), np.eye(4), np.eye(4))

