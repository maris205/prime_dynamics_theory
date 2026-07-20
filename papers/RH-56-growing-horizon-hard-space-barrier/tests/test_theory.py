import math

import numpy as np
import pytest

from hardy_barrier import (
    critical_strong_rate,
    overlap_hardy_upper,
    strong_space_ledger,
)


def test_two_sided_two_power_ledger_requires_r_to_the_eighth() -> None:
    radius = 0.85
    threshold = critical_strong_rate(radius, 2.0, 0.25)
    assert threshold == pytest.approx(radius**8)
    assert threshold == pytest.approx(0.27249052503906246)


def test_single_side_exponent_is_optimized_horizon_cost() -> None:
    result = strong_space_ledger(0.85, 0.4, 1.5)
    assert result.horizon_coefficient == pytest.approx(
        1.5 / math.log(1.0 / 0.4)
    )
    assert result.energy_power == pytest.approx(
        1.5 * math.log(1.0 / 0.85) / math.log(1.0 / 0.4)
    )


def test_common_edge_rate_exceeds_quarter_power_budget() -> None:
    edge = 1.678573510428322 ** -0.5
    left = strong_space_ledger(0.85, edge, 1.0)
    right = strong_space_ledger(0.85, edge, 1.0)
    assert left.energy_power + right.energy_power > 1.25
    assert left.energy_power + right.energy_power > 0.25


def test_overlap_bound_dominates_exact_diagonal_normal_response() -> None:
    eigenvalues = np.asarray((0.71, -0.43, 0.21j), dtype=np.complex128)
    source = np.asarray((0.8, -0.3, 0.5), dtype=np.complex128)
    observation = np.asarray((0.6, 1.2, -0.7), dtype=np.complex128)
    radius = 0.85
    exact_squared = 0.0
    state = source.copy()
    for power in range(1000):
        exact_squared += abs(np.dot(observation, state)) ** 2 / radius ** (
            2 * power
        )
        state = eigenvalues * state
    weights = np.abs(observation * source)
    bound = overlap_hardy_upper(np.abs(eigenvalues), weights, radius)
    assert math.sqrt(exact_squared) <= bound.energy_upper * (1.0 + 1.0e-12)


def test_overlap_inputs_are_checked() -> None:
    with pytest.raises(ValueError):
        overlap_hardy_upper([0.9], [1.0], 0.85)
    with pytest.raises(ValueError):
        critical_strong_rate(0.85, 3.0, 0.0)
