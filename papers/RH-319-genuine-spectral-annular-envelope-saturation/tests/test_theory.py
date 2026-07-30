import math

from spectral_saturation import annular_kappa, annular_mass_scale


def test_kappa_decreases_toward_endpoint():
    assert annular_kappa(1.42) < annular_kappa(1.41) < annular_kappa(1.4)


def test_archived_radius_value_is_reproduced():
    assert math.isclose(annular_kappa(1.41), 0.03504570526096135)


def test_mass_scale_decays():
    assert annular_mass_scale(1e12, 1.41) < annular_mass_scale(1e6, 1.41)
