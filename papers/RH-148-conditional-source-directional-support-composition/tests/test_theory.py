from __future__ import annotations

import math

import pytest

from source_support import branch_is_stable, compose_support_floor, projector_radius, support_value


def test_gap_gate_and_projector_radius() -> None:
    assert math.isclose(projector_radius(0.1, 0.5), 0.25)
    with pytest.raises(ValueError):
        projector_radius(0.1, 0.2)


def test_branch_gate_is_strict() -> None:
    assert branch_is_stable(0.09, 0.1)
    assert not branch_is_stable(0.1, 0.1)


def test_support_floor_keeps_positive_cocycle_recovery() -> None:
    floor, drawdown = compose_support_floor(0.2, [math.log(0.5), math.log(4.0), math.log(0.5)])
    assert math.isclose(floor, 0.1)
    assert math.isclose(drawdown, math.log(2.0))
    assert math.isclose(support_value(0.0, 0.1), 0.1)


def test_cocycle_omission_witness_collapses() -> None:
    floor, _ = compose_support_floor(1.0, [math.log(0.5)] * 80)
    assert floor < 1e-20

