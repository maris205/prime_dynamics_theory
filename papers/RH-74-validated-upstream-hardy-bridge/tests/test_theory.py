import math

import pytest

from upstream_bridge import (
    normalized_matrix_difference_upper,
    robust_block_bridge,
    volterra_power_defects,
)


def test_normalized_difference_vanishes() -> None:
    assert normalized_matrix_difference_upper(2.0, 0.0) == 0.0


def test_normalized_difference_bound() -> None:
    assert normalized_matrix_difference_upper(2.0, 0.1) > 0.1


def test_volterra_is_exact_for_scalar_reference_zero() -> None:
    result = volterra_power_defects([1.0, 0.0, 0.0, 0.0], 0.2)
    assert result[1] >= 0.2
    assert result[2] >= 0.04
    assert result[3] >= 0.008


def test_robust_bridge_closes_scalar_contraction() -> None:
    powers = [0.5**k for k in range(9)]
    ledger = robust_block_bridge(
        reference_power_bounds=powers,
        reference_state_prefix_bounds=[1.0, 0.5],
        reference_source_norm=1.0,
        reference_observation_norm=1.0,
        operator_error=1.0e-4,
        source_error=2.0e-4,
        observation_error=3.0e-4,
        block_horizon=2,
        block_multiple=4,
    )
    assert ledger.block_contraction_certified
    assert math.isfinite(ledger.bridge_energy_upper)
    assert ledger.bridge_energy_upper > 0.0


@pytest.mark.parametrize(
    "call",
    [
        lambda: normalized_matrix_difference_upper(1.0, 1.0),
        lambda: volterra_power_defects([], 0.1),
        lambda: robust_block_bridge(
            reference_power_bounds=[1.0, 2.0, 4.0],
            reference_state_prefix_bounds=[1.0],
            reference_source_norm=1.0,
            reference_observation_norm=1.0,
            operator_error=0.1,
            source_error=0.0,
            observation_error=0.0,
            block_horizon=1,
            block_multiple=2,
        ),
    ],
)
def test_invalid_ledgers_fail(call) -> None:
    with pytest.raises(ValueError):
        call()
