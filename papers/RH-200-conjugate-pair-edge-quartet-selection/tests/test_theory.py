import numpy as np

from edge_quartet import conjugate_closed, outer_edge_indices, radial_edge_gap


def test_conjugate_pair_and_edge_gap_helpers():
    values = np.array([0.7 + 0.2j, 0.7 - 0.2j, -0.4 + 0.1j, -0.4 - 0.1j, 0.1])
    assert conjugate_closed(values)
    assert outer_edge_indices(values, 4) == [0, 1, 2, 3]
    assert radial_edge_gap(values, 4) > 0.0
