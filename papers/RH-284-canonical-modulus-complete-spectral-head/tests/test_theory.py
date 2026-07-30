import numpy as np

from spectral_head import complementary_radius, modulus_head, rank_bound


def test_strict_threshold_and_conjugate_completion():
    roots = np.asarray([0.7 + 0.2j, 0.7 - 0.2j, 0.5, 0.4])
    head, tail = modulus_head(roots, 0.5)
    assert head.size == 2
    assert tail.size == 2
    assert 0.5 in tail
    assert complementary_radius(roots, 0.5) == 0.5


def test_rank_bound():
    assert rank_bound(10.0, 0.5) == 40.0
