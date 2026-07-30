import math

from counterloop import BETA, counterloop_moment


def test_pre_alias_moments_are_exact():
    for k in range(2, 12):
        for n in range(1, 2 * k):
            target = -2 * BETA**n if n % 2 == 0 else 0.0
            assert abs(counterloop_moment(k, n) - target) < 1e-14


def test_first_alias_is_order_two_k():
    k = 7
    moment = counterloop_moment(k, 2 * k).real
    target = -2 * BETA ** (2 * k)
    assert math.isclose(moment, 2 * (k - 1) * BETA ** (2 * k), rel_tol=1e-14)
    assert math.isclose(moment - target, 2 * k * BETA ** (2 * k), rel_tol=1e-14)
