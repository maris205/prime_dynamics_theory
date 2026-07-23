from __future__ import annotations

import pytest

from quotient_support import (
    coarse_support_price_upper,
    finite_support_reduction,
    fourth_cross_ratio,
    local_quotient_price,
    support_margin,
    weak_mode_event,
)


def test_support_selector() -> None:
    singular = [1.0, 0.4, 0.2, 1.0e-5]
    assert fourth_cross_ratio(singular) == pytest.approx(1.0e-5)
    assert weak_mode_event(singular, 1.0e-4)
    assert not weak_mode_event(singular, 1.0e-6)
    assert support_margin(1.0e-5, 1.0e-4) == pytest.approx(0.1)


def test_price_reduction() -> None:
    price = local_quotient_price(2.0, 4.0)
    assert price >= 1.0
    total = coarse_support_price_upper(5, 0.5, 2.0)
    assert total >= 5.0
    assert finite_support_reduction([2, 1, 0, 0], 2)
    assert not finite_support_reduction([2, 1, 1, 0], 2)


def test_validation() -> None:
    with pytest.raises(ValueError):
        fourth_cross_ratio([1.0, 0.5, 0.2])
    with pytest.raises(ValueError):
        weak_mode_event([0.0, 0.5, 0.2, 0.1], 1.0e-4)
    with pytest.raises(ValueError):
        local_quotient_price(1.0, 0.0)
