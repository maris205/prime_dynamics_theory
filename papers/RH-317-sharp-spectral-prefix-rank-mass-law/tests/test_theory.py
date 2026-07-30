import math

from rank_mass import (
    BASE,
    LOG_BASE,
    mass_lower_bound,
    normalized_divisor_feedback,
    proper_divisors,
    rank_lower_bound,
)


def test_growth_base_is_superunit():
    assert BASE > 1.0
    assert math.isclose(math.log(BASE), LOG_BASE)


def test_model_rank_lower_bound_has_exact_base():
    q_star = 0.7008752258547759
    first = rank_lower_bound(10, q_star**10)
    second = rank_lower_bound(11, q_star**11)
    assert math.isclose(second / first, BASE)


def test_mass_and_rank_lower_bounds_differ_by_q_squared():
    q_star = 0.7008752258547759
    rank = rank_lower_bound(12, q_star**12)
    mass = mass_lower_bound(12, q_star**12)
    assert math.isclose(mass / rank, 0.25)


def test_packet_feedback_uses_only_proper_divisors():
    for order in (8, 16, 32):
        assert all(divisor <= order // 2 for divisor in proper_divisors(order))
    assert normalized_divisor_feedback(32) < normalized_divisor_feedback(16)
