from __future__ import annotations

import pytest

from predictor_corrector import contraction_factor, global_rayleigh_upper, predictor_coefficient


def test_predictor() -> None:
    assert predictor_coefficient(0.5, 0.25) >= 0.75
    with pytest.raises(ValueError):
        predictor_coefficient(-1.0, 0.25)


def test_contraction() -> None:
    assert contraction_factor(0.5, 0.5, 0.25) >= 0.375
    with pytest.raises(ValueError):
        contraction_factor(1.1, 0.5, 0.25)


def test_global_rayleigh() -> None:
    assert global_rayleigh_upper(2.0, 4.0) >= 1.0
