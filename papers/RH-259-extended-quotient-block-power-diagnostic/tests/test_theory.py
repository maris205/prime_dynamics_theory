import numpy as np

from quotient_stability import block_root_rate, power_norm_profile


def test_nonnormal_block_can_contract_after_one_step():
    matrix = np.asarray([[0.5, 2.0], [0.0, 0.5]])
    profile = power_norm_profile(matrix, 12)
    assert profile["operator_norms"][0] > 1.0
    assert profile["first_contractive_depth"] is not None
    assert profile["operator_norms"][-1] < 1.0


def test_block_root_rate():
    assert abs(block_root_rate(0.25, 2) - 0.5) < 1e-15
