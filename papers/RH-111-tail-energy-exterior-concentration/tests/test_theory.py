from __future__ import annotations

import math
import numpy as np
import pytest

from exterior_concentration import concentration_upper_bound, normalized_trace_lower_bound, spectral_concentration


def test_concentration_range() -> None:
    for rank in range(4, 9):
        for _ in range(20):
            singular = np.sort(np.random.default_rng(rank).random(rank))[::-1] + 0.1
            value = spectral_concentration(singular)
            assert 1.0 - 1e-12 <= value <= math.comb(rank, 4) + 1e-12


def test_tail_energy_bound_contains_actual_concentration() -> None:
    rng = np.random.default_rng(111)
    for _ in range(40):
        recent = rng.normal(size=(12, 6))
        error = rng.normal(size=(12, 6))
        error *= 1e-3 / np.linalg.norm(error, 2)
        shat = np.linalg.svd(recent, compute_uv=False)
        full = np.linalg.svd(recent + error, compute_uv=False)
        bound = concentration_upper_bound(shat, 1e-3)
        assert spectral_concentration(full) <= bound["upper"] + 2e-10
        refined = normalized_trace_lower_bound(shat, 1e-3)
        assert refined["refined_lower"] <= np.prod(full[:4]) / full[0] ** 4 + 2e-12


def test_rank_four_is_exact() -> None:
    singular = [4.0, 3.0, 2.0, 1.0]
    assert spectral_concentration(singular) == pytest.approx(1.0)
    bound = concentration_upper_bound(singular, 0.0)
    assert bound["upper"] == pytest.approx(1.0)


def test_validation() -> None:
    with pytest.raises(ValueError):
        spectral_concentration([1.0, 0.5, 0.2])
    with pytest.raises(ValueError):
        concentration_upper_bound([1.0, 0.5, 0.2, 0.1], -1.0)
