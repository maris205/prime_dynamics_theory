from __future__ import annotations

import pytest

from power_ledger import (
    identification_sigma_power,
    quarter_power_margin,
    rh49_full_range_green,
    side_hardy_power,
    stress_mesh_decay_power,
    two_side_hardy_power,
    zero_power_overheads,
)


def test_max_plus_side_power() -> None:
    power = side_hardy_power(
        normalization=0.0,
        upstream_bridge=0.02,
        finite_prefix=0.10,
        reduced_future=0.04,
        observability=0.08,
        packet_residual=0.03,
    )
    assert power == pytest.approx(0.11)
    cancellation = side_hardy_power(
        normalization=0.0,
        upstream_bridge=-1.0,
        finite_prefix=0.0,
        reduced_future=0.0,
        observability=0.5,
        packet_residual=-0.5,
    )
    assert cancellation == pytest.approx(0.0)


def test_two_side_quarter_budget_and_mesh() -> None:
    total = two_side_hardy_power(0.12, 0.13)
    assert total == pytest.approx(0.25)
    assert rh49_full_range_green(total)
    assert quarter_power_margin(total) == pytest.approx(0.0)
    assert stress_mesh_decay_power(total) == pytest.approx(0.5)
    assert identification_sigma_power(total, 2.0) == pytest.approx(0.5)


def test_zero_power_overheads_and_validation() -> None:
    assert zero_power_overheads(
        logarithmic_rank=True,
        fixed_memory_depth=True,
        fixed_endpoint_gate=True,
        normalized_source=True,
    )
    assert not zero_power_overheads(
        logarithmic_rank=False,
        fixed_memory_depth=True,
        fixed_endpoint_gate=True,
        normalized_source=True,
    )
    with pytest.raises(ValueError):
        side_hardy_power(
            normalization=float("nan"),
            upstream_bridge=0.0,
            finite_prefix=0.0,
            reduced_future=0.0,
            observability=0.0,
            packet_residual=0.0,
        )
