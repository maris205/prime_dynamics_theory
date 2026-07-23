from __future__ import annotations

import math

import pytest

from prefix_transient import (
    block_tail_energy_squared_upper,
    crude_prefix_power,
    crude_prefix_upper,
    directional_prefix_power,
    full_hardy_upper,
)


def test_scalar_prefix_and_tail_bounds() -> None:
    crude = crude_prefix_upper(3.0, 4.0)
    assert crude >= 6.0
    tail2 = block_tail_energy_squared_upper(2.0, 0.1, 3.0)
    assert tail2 >= 12.0 * 0.01 / 0.99
    assert full_hardy_upper(1.5, tail2) >= math.sqrt(2.25 + tail2)


def test_power_bookkeeping() -> None:
    assert crude_prefix_power(0.5, 0.0) == pytest.approx(0.5)
    assert crude_prefix_power(0.5, -1.0) == pytest.approx(0.0)
    assert directional_prefix_power(0.0) == 0.0
    assert directional_prefix_power(0.2) == pytest.approx(0.1)


def test_validation() -> None:
    with pytest.raises(ValueError):
        block_tail_energy_squared_upper(1.0, 1.0, 1.0)
    with pytest.raises(ValueError):
        crude_prefix_upper(-1.0, 1.0)
