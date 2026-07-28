import numpy as np

from local_count_gate import contour_clearance, disk_count, tail_is_constant


def test_disk_count_and_clearance():
    roots = np.asarray([1.0, 2.0j, 3.0])
    assert disk_count(roots, 2.5) == 2
    assert abs(contour_clearance(roots, 2.5) - 0.5) < 1e-14


def test_tail_constancy_is_only_finite_diagnostic():
    assert tail_is_constant([1, 2, 3, 3, 3, 3], 4)
    assert not tail_is_constant([1, 2, 3, 3, 3, 4], 4)
