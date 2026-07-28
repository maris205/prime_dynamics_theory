import numpy as np

from absolute_majorant import cancellation_gain, root_rates, separate_absolute_majorant


def test_separate_majorant_dominates_residual():
    full = np.array([1.0, 2.0, 3.0], dtype=complex)
    majorant = separate_absolute_majorant(full, 0.5, -0.25, np.array([0.1, -0.1]))
    residual = full - np.array([0.5, 0.5**2, 0.5**3]) - np.array([-0.25, 0.25, -0.125]) - np.array([0.1 + -0.1, (0.1)**2 + (-0.1)**2, (0.1)**3 + (-0.1)**3])
    assert np.all(majorant >= np.abs(residual))
    assert np.all(root_rates(majorant) > 0.0)
    assert np.all(cancellation_gain(majorant, residual) >= 1.0)


def test_perron_sector_forces_superunit_root_rate():
    majorant = separate_absolute_majorant(np.zeros(12), 1.0 / 0.85, 0.0, np.zeros(0))
    assert np.all(majorant[1:] ** (1.0 / np.arange(2, 13)) >= 1.0 / 0.85)
