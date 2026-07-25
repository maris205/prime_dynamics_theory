from __future__ import annotations

import math

import pytest

from packet_transport import (
    cross_operator_radius,
    enriched_projector_radius,
    ideal_truncation_packet_gate,
    packet_transfer_radius,
    singular_direction_enclosure,
    spectral_packet_enclosure,
)


def test_rank_mismatch_is_unit_radius() -> None:
    result = packet_transfer_radius(0.2, 0.01, 4, 5)
    assert not result["rank_compatible"]
    assert result["transferred_radius"] == 1.0
    assert not result["informative"]


def test_equal_rank_transfer_uses_triangle_cap() -> None:
    assert packet_transfer_radius(0.2, 0.1, 4, 4)["transferred_radius"] == pytest.approx(0.3)
    assert packet_transfer_radius(0.8, 0.4, 4, 4)["transferred_radius"] == 1.0


def test_cross_and_enriched_bounds() -> None:
    assert cross_operator_radius(0.01, 2.0, 0.03) == pytest.approx(0.13)
    assert enriched_projector_radius(0.3, 0.4) == pytest.approx(0.7)
    assert enriched_projector_radius(0.8, 0.7) == 1.0


def test_singular_direction_gate_and_boundary() -> None:
    stable = singular_direction_enclosure([4.0, 2.0, 1.0], 2, 0.2)
    assert stable["stable"]
    assert stable["singular_gap"] == pytest.approx(1.0)
    assert stable["projector_radius"] == pytest.approx(0.25)
    assert not singular_direction_enclosure([4.0, 2.0, 1.0], 2, 0.5)["stable"]


def test_spectral_packet_gate_is_strict() -> None:
    assert spectral_packet_enclosure(1.0, 0.49)["stable"]
    assert not spectral_packet_enclosure(1.0, 0.5)["stable"]


def test_ideal_truncation_formula() -> None:
    result = ideal_truncation_packet_gate([4.0, 3.0, 2.0, 1.0, 0.1], 4)
    assert result["packet_gate"]
    assert 0.0 < result["tail_energy_fraction"] < 1.0
    assert math.isfinite(result["gap_ratio"])


def test_invalid_data_rejected() -> None:
    with pytest.raises(ValueError):
        packet_transfer_radius(-1.0, 0.0, 4, 4)
    with pytest.raises(ValueError):
        singular_direction_enclosure([1.0, 2.0], 1, 0.1)
