from __future__ import annotations

import math

import pytest

from projector_propagation import endpoint_tail_lipschitz_bound, local_gap_distance_bound, projector_secant_multiplier


def test_projector_bounds() -> None:
    assert endpoint_tail_lipschitz_bound(2.0, 0.25) >= 0.5
    assert local_gap_distance_bound(0.02, 0.5) >= math.sqrt(0.08)
    assert projector_secant_multiplier(0.2, 0.5) >= 2.5


def test_invalid_projector_bounds() -> None:
    with pytest.raises(ValueError):
        local_gap_distance_bound(1.0, 0.0)
    with pytest.raises(ValueError):
        projector_secant_multiplier(0.0, 1.0)
