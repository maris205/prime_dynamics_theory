from __future__ import annotations

import pytest

from rayleigh_injection import geometric_injection_bound, injection_convolution, one_step_tail_bound


def test_one_step() -> None:
    assert one_step_tail_bound(0.1, 0.5, 0.2) >= 0.2
    with pytest.raises(ValueError):
        one_step_tail_bound(-1.0, 0.5, 0.0)


def test_convolution() -> None:
    bound = injection_convolution(1.0, 0.5, [0.0, 0.0, 0.0])
    assert 0.125 <= bound < 0.126


def test_geometric_injection() -> None:
    bound = geometric_injection_bound(0.0, 0.25, 1.0, 0.5, 4)
    assert 0.0 < bound < 0.2
