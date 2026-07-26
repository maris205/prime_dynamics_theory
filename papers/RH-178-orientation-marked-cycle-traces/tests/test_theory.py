from directed_cycle_marks import ordinary_cycle_trace, reduced_marked_trace


def test_scalar_traces_do_not_see_orientation():
    for power in range(1, 20):
        assert abs(ordinary_cycle_trace(9, power, 1) - ordinary_cycle_trace(9, power, -1)) < 1e-14


def test_reduced_edge_marker_has_unit_orientation_gap():
    for length in (3, 5, 11):
        forward = reduced_marked_trace(length, 1, 1)
        reverse = reduced_marked_trace(length, 1, -1)
        assert abs(abs(forward - reverse) - 1.0) < 1e-14
