from __future__ import annotations

import numpy as np
import pytest

from weak_mode_quotient import adaptive_width, gap_weighted_tail_loss_bound, universal_omitted_block_bound


def ky_fan_sum(matrix: np.ndarray, rank: int) -> float:
    return float(np.linalg.eigvalsh((matrix + matrix.T) / 2.0)[-rank:].sum())


def test_adaptive_width() -> None:
    singular = [1.0, 0.2, 1e-4, 1e-10]
    assert adaptive_width(singular, 1e-8, minimum=2, maximum=4) == 3
    assert adaptive_width(singular, 1e-3, minimum=2, maximum=4) == 2
    with pytest.raises(ValueError):
        adaptive_width(singular, -1.0)


def test_gap_weighted_bound() -> None:
    a = np.diag([5.0, 4.0, 3.0])
    d = np.array([[1.0]])
    c = np.array([[0.1], [0.2], [0.05]])
    full = np.block([[a, c], [c.T, d]])
    rank = 2
    actual = ky_fan_sum(full, rank) - ky_fan_sum(a, rank)
    bound = gap_weighted_tail_loss_bound(np.linalg.norm(c, "fro"), 4.0, 1.0)
    assert 0.0 <= actual <= bound


def test_universal_bound() -> None:
    value = universal_omitted_block_bound(0.25, 0.5)
    assert value >= 1.0
    with pytest.raises(ValueError):
        universal_omitted_block_bound(-1.0, 0.0)
