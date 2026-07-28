import numpy as np

from trace_hs import nilpotent_shift


def test_nilpotent_shift_separates_hs_mass_from_trace_powers():
    shift = nilpotent_shift(64)
    assert np.sum(shift**2) == 63.0
    for order in range(1, 8):
        assert np.trace(np.linalg.matrix_power(shift, order)) == 0.0
    assert np.linalg.det(np.eye(64) - 0.7 * shift) == 1.0
