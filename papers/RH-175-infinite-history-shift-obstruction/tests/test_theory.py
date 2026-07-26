import numpy as np

from history_shift import shift_resolvent_vector_lower_bound, unilateral_shift_truncation


def test_nilpotent_shift_and_resolvent_vector():
    length = 8
    weight = 0.2
    point = 0.1
    shift = unilateral_shift_truncation(length)
    assert np.linalg.matrix_power(shift, length).max() == 0.0
    vector = np.eye(length)[:, 0]
    observed = np.linalg.norm(np.linalg.solve(point * np.eye(length) - weight * shift, vector))
    assert abs(observed - shift_resolvent_vector_lower_bound(length, weight, point)) < 1e-10
