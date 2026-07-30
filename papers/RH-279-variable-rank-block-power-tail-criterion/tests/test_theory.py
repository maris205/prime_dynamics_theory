from variable_block import block_tail_bound, trace_power_bound


def test_block_formula():
    assert trace_power_bound(10, 4, 2, 0.5, 1.0) == 1.0


def test_tail_decreases_with_block_depth():
    assert block_tail_bound(16, 0.8, 1.0, 0.7**16, 1.1) < block_tail_bound(4, 0.8, 1.0, 0.7**4, 1.1)
