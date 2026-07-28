import numpy as np

from cloud_tightness import (
    centered_rms_normalize,
    empirical_tail_mass,
    second_moment_tail_bound,
    tightness_radius,
)


def test_centered_rms_identities():
    normalized, _, _ = centered_rms_normalize(np.asarray([1 + 2j, 1 - 2j, -2 + 1j, -2 - 1j]))
    assert abs(np.mean(normalized)) < 1e-14
    assert abs(np.mean(np.abs(normalized) ** 2) - 1.0) < 1e-14


def test_markov_tail_certificate():
    values = np.asarray([0.0, 0.0, np.sqrt(2.0), -np.sqrt(2.0)])
    assert empirical_tail_mass(values, 1.0) <= second_moment_tail_bound(1.0)
    assert abs(tightness_radius(0.25) - 2.0) < 1e-14
