from __future__ import annotations

import math

import pytest

from half_log_rank import (
    clock_rank,
    excess_rank_tail_bound,
    factorized_tail_bound,
    half_log_clock,
)


def test_clock_dyadic_increment() -> None:
    first = half_log_clock(0.08)
    second = half_log_clock(0.04)
    assert second > first
    assert second - first == pytest.approx(math.log(2.0) / (2.0 * math.log(1.6785735104283224)))


@pytest.mark.parametrize("sigma,rank", [(0.16, 4), (0.08, 5), (0.04, 6), (0.02, 6), (0.01, 7)])
def test_archived_clock_ranks(sigma: float, rank: int) -> None:
    assert clock_rank(sigma, offset=2) == rank


def test_excess_tail_is_geometric() -> None:
    first = excess_rank_tail_bound(3, ratio_upper=0.4, quadratic_energy_constant=2.0)
    second = excess_rank_tail_bound(4, ratio_upper=0.4, quadratic_energy_constant=2.0)
    assert second == pytest.approx(0.4 * first)


def test_factorized_tail() -> None:
    value = factorized_tail_bound(1e-3, 2.0, 3.0, 4e-4)
    assert value >= 0.0064


@pytest.mark.parametrize("sigma", [0.0, 1.0, -0.1])
def test_bad_clock_inputs(sigma: float) -> None:
    with pytest.raises(ValueError):
        half_log_clock(sigma)

