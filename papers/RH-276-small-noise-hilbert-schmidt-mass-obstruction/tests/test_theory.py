from hs_mass import ASYMPTOTIC_CONSTANT, explicit_lower_constant, hs_squared


def test_explicit_lower_constant_is_positive():
    assert 0.069 < explicit_lower_constant() < 0.071


def test_scaled_hs_mass_approaches_limit():
    coarse = 0.01 * hs_squared(0.01)
    fine = 0.001 * hs_squared(0.001)
    assert abs(fine - ASYMPTOTIC_CONSTANT) < abs(coarse - ASYMPTOTIC_CONSTANT)
    assert fine / ASYMPTOTIC_CONSTANT < 1.03
