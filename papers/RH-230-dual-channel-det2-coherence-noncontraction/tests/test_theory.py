import numpy as np

from det2_coherence import det2_log, grid_sup_log_difference, strict_tail_contraction


def test_det2_log_is_permutation_invariant():
    values = np.asarray([0.2, -0.1, 0.3j, -0.3j])
    assert det2_log(values, 0.7) == det2_log(values[::-1], 0.7)
    assert grid_sup_log_difference(values, values[::-1], np.asarray([0.5, 1.0j])) < 1e-14


def test_strict_tail_contraction():
    assert strict_tail_contraction([4.0, 3.0, 2.0, 1.0], 4)
    assert not strict_tail_contraction([4.0, 3.0, 2.0, 2.5], 4)
