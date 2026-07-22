import numpy as np
import pytest

from depth_barrier import (
    arc_phases,
    jittered_ring_phases,
    projection_audit,
    required_depth,
    uniform_ring_phases,
)


def test_exact_ring_is_orthogonal_until_target_enters_space() -> None:
    phases = uniform_ring_phases(32)
    for depth in (1, 4, 8, 16):
        record = projection_audit(phases, 16, depth)
        assert record.projection_error == pytest.approx(1.0, abs=1.0e-12)
        assert record.spectral_lower_bound > 1.0 - 1.0e-12
    assert projection_audit(phases, 16, 17).projection_error < 1.0e-12


def test_exact_ring_required_depth_is_horizon_plus_one() -> None:
    assert required_depth(uniform_ring_phases(64), 32, 0.1) == 33


def test_clustered_single_phase_has_depth_one() -> None:
    phases = arc_phases(64, 0.0)
    assert required_depth(phases, 32, 0.1) == 1


def test_spectral_lower_bound_is_valid_for_jittered_ring() -> None:
    phases = jittered_ring_phases(64, 0.5)
    record = projection_audit(phases, 32, 32)
    assert record.projection_error + 1.0e-12 >= record.spectral_lower_bound
    assert record.projection_error > 0.98


@pytest.mark.parametrize(
    "call",
    [
        lambda: uniform_ring_phases(0),
        lambda: arc_phases(4, -1.0),
        lambda: projection_audit(np.zeros(4), 2, 4),
        lambda: required_depth(np.zeros(4), 2, 1.0),
        lambda: jittered_ring_phases(4, -0.1),
    ],
)
def test_invalid_inputs_are_rejected(call) -> None:
    with pytest.raises(ValueError):
        call()
