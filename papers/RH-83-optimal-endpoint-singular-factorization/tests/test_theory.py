from __future__ import annotations

import pytest

from singular_factor import optimal_factor_constant, optimal_rank_residual


def test_factor_constant() -> None:
    assert optimal_factor_constant([4.0, 2.0], [8.0, 3.0], 2) == pytest.approx(2.0 / 3.0)


def test_rank_residual() -> None:
    assert optimal_rank_residual([4.0, 3.0, 2.0], 1) == pytest.approx((13.0) ** 0.5)


def test_zero_rank_factor() -> None:
    assert optimal_factor_constant([1.0], [1.0], 0) == 0.0


@pytest.mark.parametrize("rank", [-1, 3])
def test_bad_rank(rank: int) -> None:
    with pytest.raises(ValueError):
        optimal_factor_constant([1.0, 0.5], [1.0, 0.5], rank)

