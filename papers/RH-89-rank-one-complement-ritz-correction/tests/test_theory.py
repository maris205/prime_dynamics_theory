from __future__ import annotations

import pytest

from ritz_correction import correction_fraction, corrected_tail, residual_energy


def test_residual_energy() -> None:
    assert residual_energy(10.0, 7.0) >= 3.0


def test_corrected_tail() -> None:
    assert corrected_tail(5.0, 2.0) >= 3.0
    with pytest.raises(ValueError):
        corrected_tail(1.0, 2.0)


def test_correction_fraction() -> None:
    value = correction_fraction(10.0, 4.0, 2.0)
    assert 0.74 < value <= 0.75
