from __future__ import annotations

import pytest

from tail_majorization import ky_fan_tail, tail_transfer_bound


def test_ky_fan_tail() -> None:
    assert ky_fan_tail([4.0, 3.0, 2.0], 1) == pytest.approx(13.0**0.5)


def test_tail_transfer() -> None:
    assert tail_transfer_bound(0.1, 2.0, 0.03) == pytest.approx(0.23)


def test_bad_rank() -> None:
    with pytest.raises(ValueError):
        ky_fan_tail([1.0], 2)

