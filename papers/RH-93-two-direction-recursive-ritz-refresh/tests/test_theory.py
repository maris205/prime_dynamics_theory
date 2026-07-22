from __future__ import annotations

import math

import numpy as np
import pytest

from two_direction_refresh import (
    block_budget_product,
    block_geometric_mean,
    cross_energy_fraction,
    generalized_frame_trace,
    ky_fan_gain,
    recursive_tail_bound,
    trial_frame_form,
)


def test_block_helpers() -> None:
    factors = (0.3, 0.2, 0.1, 0.2)
    assert block_budget_product(factors) >= math.prod(factors)
    assert block_geometric_mean(factors) >= math.prod(factors) ** 0.25
    assert recursive_tail_bound(2.0, factors) >= 2.0 * math.prod(factors)


def test_cross_energy_fraction() -> None:
    singular = (4.0, 3.0, 1.0)
    assert cross_energy_fraction(singular, 2) <= 25.0 / 26.0
    assert cross_energy_fraction(singular, 2) > 0.96
    with pytest.raises(ValueError):
        cross_energy_fraction(singular, 0)


def test_ky_fan_gain_identity() -> None:
    matrix = np.diag([5.0, 4.0, 1.5, 0.5])
    bottom = np.linalg.eigvalsh(matrix)[:2]
    gain = ky_fan_gain(3.0, bottom)
    assert abs(gain - 1.0) < 1e-12


def test_generalized_frame_certificate() -> None:
    matrix = np.diag([5.0, 4.0, 1.0, 0.25])
    frame = np.array([[0.0, 0.0], [0.0, 0.0], [2.0, 0.0], [0.0, 3.0]])
    assert abs(generalized_frame_trace(matrix, frame) - 1.25) < 1e-12
    assert trial_frame_form(matrix, frame, 2.0, 0.5) < 0.0
