import numpy as np

from quartic_normalization import (
    centered_rms_normalize,
    determinant_radius_normalize,
    monic_coefficients,
)


def sample_quartet():
    return np.asarray([0.2 + 0.7j, 0.2 - 0.7j, -0.1 + 0.4j, -0.1 - 0.4j])


def test_centered_rms_normalization_fixes_two_gauges():
    normalized = centered_rms_normalize(sample_quartet())
    assert abs(np.mean(normalized.roots)) < 1e-14
    assert abs(np.mean(np.abs(normalized.roots) ** 2) - 1.0) < 1e-14


def test_determinant_radius_has_unit_constant_modulus():
    normalized = determinant_radius_normalize(sample_quartet())
    assert abs(abs(monic_coefficients(normalized.roots)[-1]) - 1.0) < 1e-14
