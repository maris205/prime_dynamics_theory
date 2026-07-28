import numpy as np

from spectral_factor import det2_log_jet, det2_product, factorization_error


def test_det2_factorization_is_multiset_multiplicative():
    cloud = np.asarray([0.5 + 0.2j, 0.5 - 0.2j])
    complement = np.asarray([-0.1, 0.03j, -0.03j])
    assert factorization_error(cloud, complement, 0.7 + 0.1j) < 1e-14


def test_det2_log_jet_matches_small_variable_product():
    values = np.asarray([0.2, -0.1, 0.04j, -0.04j])
    z = 1e-3
    exact = np.log(det2_product(values, z))
    jet = det2_log_jet(values, z, 4)
    assert abs(exact - jet) < 1e-15
