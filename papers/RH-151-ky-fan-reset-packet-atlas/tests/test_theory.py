from __future__ import annotations

import math

import pytest

from reset_packet import branch_free_energy_step, direct_packet_enclosure, ky_fan_projector_bound


def test_ky_fan_angle_bound() -> None:
    result = ky_fan_projector_bound(0.01, 0.04)
    assert result["operator_radius"] == pytest.approx(0.5)
    assert result["frobenius_radius"] == pytest.approx(math.sqrt(0.5))
    assert result["informative"]


def test_ky_fan_zero_gap_is_vacuous() -> None:
    result = ky_fan_projector_bound(0.0, 0.0)
    assert result["operator_radius"] == 1.0
    assert not result["informative"]


def test_branch_free_step() -> None:
    value = branch_free_energy_step(0.01, 0.04, 0.002, 0.1)
    assert value == pytest.approx(0.012 + math.sqrt(0.5) * 0.1)


def test_direct_reset_gate_is_strict() -> None:
    assert direct_packet_enclosure(1.0, 0.49)["stable"]
    assert not direct_packet_enclosure(1.0, 0.5)["stable"]


def test_invalid_input() -> None:
    with pytest.raises(ValueError):
        ky_fan_projector_bound(-1.0, 1.0)
