import numpy as np

from orthogonal_quotient import (
    ordered_schur_quotient,
    riesz_projection_norm_2x2,
    selected_quotient_trace_partition,
)


def test_upper_triangular_selected_quotient_trace_identity():
    matrix = np.array([
        [2.0, 100.0, -30.0],
        [0.0, 0.5, 4.0],
        [0.0, 0.0, 0.25],
    ], dtype=complex)
    result = ordered_schur_quotient(matrix, 1.0)
    assert result["selected_dimension"] == 1
    partition = selected_quotient_trace_partition(
        result["triangular"], result["selected_dimension"], 8
    )
    np.testing.assert_allclose(partition["partition_error"], 0.0, atol=1e-10)
    expected = np.array([0.5**n + 0.25**n for n in range(1, 9)])
    np.testing.assert_allclose(partition["quotient"], expected, atol=1e-10)


def test_riesz_projection_can_blow_up_while_orthogonal_quotient_is_fixed():
    assert riesz_projection_norm_2x2(2.0, 0.5, 0.0) == 1.0
    assert riesz_projection_norm_2x2(2.0, 0.5, 1.0e6) > 6.0e5
