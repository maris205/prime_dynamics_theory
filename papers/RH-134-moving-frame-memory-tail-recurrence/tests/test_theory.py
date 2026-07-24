import numpy as np

from memory_tail_recurrence import envelope_ratio, memory_tail_update, moving_frame_tail_upper


def test_exact_tail_update_and_envelope_ratio():
    tail = np.diag([2.0, 1.0])
    snapshot = np.diag([1.0, 3.0])
    result = memory_tail_update(tail, snapshot, 0.25, 2)
    assert np.allclose(result, 0.25 * tail + 0.25**2 * snapshot)
    assert abs(envelope_ratio(0.25, 2, 1) - 1.25) < 1e-12


def test_moving_frame_young_bound_and_sharpness():
    old = np.diag([1.0, 2.0])
    birth = np.zeros((2, 2))
    result = moving_frame_tail_upper(old, 2.0, birth, np.eye(2), 0.5, 0.2, 3, 1.0)
    assert np.allclose(result["transported"], 0.4 * old)
    assert np.allclose(result["frame_forcing"], 0.2 * np.eye(2))
    assert result["raw_multiplicative_factor"] == 0.4
