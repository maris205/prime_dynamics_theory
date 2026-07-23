from __future__ import annotations

import math

import pytest

from quotient_law import (
    gap_weighted_loss,
    quotient_decay_exponent,
    quotient_growth_power,
    stopped_allowance,
    total_debit_upper,
    total_price_fits,
)


def test_gap_price_and_total_debit() -> None:
    price = gap_weighted_loss(2.0, 4.0)
    assert price >= 1.0
    total = total_debit_upper(3, 2.0, 2.0, 4.0)
    assert total >= 6.0
    assert total_price_fits(total, 6.1)


def test_power_ledger() -> None:
    assert quotient_decay_exponent(1.25, 1.0, 0.0) == pytest.approx(1.5)
    assert quotient_growth_power(1.25, 1.0, 0.0) == 0.0
    assert quotient_growth_power(0.5, 1.0, 0.0) == pytest.approx(0.0)
    assert quotient_growth_power(0.5, 1.0, 0.25) == pytest.approx(0.25)


def test_stopped_allowance() -> None:
    allowance = stopped_allowance(1.01, 10.0, 9.0, 0.5)
    assert allowance == pytest.approx(0.55)


def test_validation() -> None:
    with pytest.raises(ValueError):
        gap_weighted_loss(1.0, 0.0)
    with pytest.raises(ValueError):
        stopped_allowance(1.0, 1.0, 1.0, 0.5)
    with pytest.raises(ValueError):
        total_debit_upper(-1, 1.0, 1.0, 1.0)
