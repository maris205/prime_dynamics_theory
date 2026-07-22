from __future__ import annotations

import math

import pytest

from snapshot_packets import captured_energy_lower, prefix_counterexample, snapshot_transfer_bound


def test_snapshot_transfer_bound() -> None:
    assert snapshot_transfer_bound(2.0, 0.125) >= 0.25
    with pytest.raises(ValueError):
        snapshot_transfer_bound(-1.0, 1.0)


def test_captured_energy() -> None:
    assert captured_energy_lower(1e-3) <= 1.0 - 1e-6
    assert captured_energy_lower(1e-3) > 0.9999989


def test_prefix_counterexample() -> None:
    record = prefix_counterexample(20)
    assert record["prefix_selects_transient"] == 1.0
    assert record["terminal_missed_relative"] > 0.999999
    assert math.isfinite(record["terminal_missed_relative"])
