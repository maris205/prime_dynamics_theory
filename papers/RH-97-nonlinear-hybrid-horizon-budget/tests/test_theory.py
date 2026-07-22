from __future__ import annotations

import pytest

from hybrid_horizon_budget import absolute_horizon_budget, hybrid_contributions, signed_horizon_shift


def test_hybrid_telescoping() -> None:
    values = [2.0, 2.5, 2.25, 3.0]
    contributions = hybrid_contributions(values)
    assert contributions == (0.5, -0.25, 0.75)
    assert abs(sum(contributions) - signed_horizon_shift(values)) < 1e-15
    assert absolute_horizon_budget(contributions) >= 1.5


def test_invalid_hybrid_data() -> None:
    with pytest.raises(ValueError):
        hybrid_contributions([1.0])
    with pytest.raises(ValueError):
        absolute_horizon_budget([])
