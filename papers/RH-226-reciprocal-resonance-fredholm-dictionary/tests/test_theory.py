import numpy as np

from fredholm_dictionary import (
    fredholm_product,
    reciprocal_polynomial_identity_error,
    reciprocal_zeros,
)


def test_reciprocal_polynomial_identity():
    values = np.asarray([0.5, -0.25, 0.2 + 0.1j, 0.2 - 0.1j])
    assert reciprocal_polynomial_identity_error(values, 0.7 + 0.2j) < 1e-14


def test_fredholm_zeros_are_reciprocals():
    values = np.asarray([0.5, -0.25, 0.2 + 0.1j, 0.2 - 0.1j])
    assert max(abs(fredholm_product(values, zero)) for zero in reciprocal_zeros(values)) < 1e-14
