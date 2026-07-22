from __future__ import annotations

import pytest

from late_memory import memory_mass, relative_stack_bound, suffix_relative_bound


def test_memory_mass() -> None:
    mass = memory_mass(1.0 / 512.0, 20)
    assert 0.00195 < mass["past"] < 0.00196
    assert mass["past_fraction"] < 0.002


def test_relative_stack_bound() -> None:
    assert relative_stack_bound(3.0, 4.0) >= 5.0
    with pytest.raises(ValueError):
        relative_stack_bound(-1.0, 0.0)


def test_suffix_relative_bound() -> None:
    assert suffix_relative_bound(2.0, 3.0, 4.0, 0.1) >= 0.15
    with pytest.raises(ValueError):
        suffix_relative_bound(1.0, 1.0, 0.0, 0.1)
