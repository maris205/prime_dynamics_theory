import numpy as np

from block_envelope import (
    block_trace_bound,
    geometric_envelope_constant,
    logarithmic_tail_bound,
)


def test_block_trace_bound_for_diagonal_example():
    matrix = np.diag([0.5, 0.25])
    m = 2
    eta = np.linalg.norm(np.linalg.matrix_power(matrix, m), 2)
    trace_norm = np.linalg.norm(np.linalg.matrix_power(matrix, m), ord="nuc")
    remainders = [1.0, np.linalg.norm(matrix, 2)]
    for order in range(2, 9):
        actual = abs(np.trace(np.linalg.matrix_power(matrix, order)))
        assert actual <= block_trace_bound(trace_norm, eta, remainders, m, order) + 1e-15


def test_geometric_and_tail_constants_are_valid():
    result = geometric_envelope_constant(0.4, 0.25, [1.0, 2.0], 2)
    assert result["q"] == 0.5
    for order in range(2, 20):
        assert block_trace_bound(0.4, 0.25, [1.0, 2.0], 2, order) <= (
            result["M"] * result["q"] ** order + 1e-15
        )
    assert logarithmic_tail_bound(0.4, 0.25, [1.0, 2.0], 2, 1.0) > 0.0
