import math

from finite_radius import moment_bias_constant, root_l1_bias_limit


def test_bias_constants():
    beta = 0.9
    constant = 2.0
    assert math.isclose(root_l1_bias_limit(beta, constant), beta * math.log(2.0))
    assert math.isclose(moment_bias_constant(4, beta, constant), 4 * beta**4 * math.log(2.0))


def test_zero_bias_when_multiplier_constant_is_one():
    assert root_l1_bias_limit(0.9, 1.0) == 0.0
    assert moment_bias_constant(2, 0.9, 1.0) == 0.0
