from annular_reduction import annular_exponents, tail_bounds


def test_fixed_annulus_exponents_are_positive():
    noisy, target = annular_exponents(1.41)
    assert noisy > 0.39
    assert target > 0.04


def test_both_tail_norms_decay():
    for hardy in (False, True):
        old = sum(tail_bounds(1e-4, 1.41, hardy=hardy))
        new = sum(tail_bounds(1e-8, 1.41, hardy=hardy))
        assert new < old
