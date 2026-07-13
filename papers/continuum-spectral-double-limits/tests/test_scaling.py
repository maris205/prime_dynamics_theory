import numpy as np

from continuum_limits.sampling import representative_gaussian_row, sampling_diagnostics
from continuum_limits.windows import response_windows


def test_representative_row_is_stochastic_and_positive():
    centers, probabilities = representative_gaussian_row(
        257, sigma=0.05, u=1.5437, source=0.8
    )
    assert centers.shape == probabilities.shape == (257,)
    assert np.all(probabilities > 0.0)
    np.testing.assert_allclose(np.sum(probabilities), 1.0, atol=2.0e-15)


def test_multinomial_observable_rms_matches_exact_variance():
    centers, probabilities = representative_gaussian_row(
        64, sigma=0.08, u=1.5437, source=0.75
    )
    observable = np.cos(np.pi * centers)
    result = sampling_diagnostics(
        probabilities,
        observable,
        source_count=200_000,
        repetitions=2000,
        rng=np.random.default_rng(12345),
    )
    ratio = result["observable_rms_error"] / result["observable_exact_rms"]
    assert 0.93 < ratio < 1.07
    assert result["mean_l1_error"] < result["l1_upper_bound"]


def test_strong_window_is_stricter_than_weak_window():
    horizons = np.array([1.0e8, 1.0e12, 1.0e16])
    windows = response_windows(horizons, p=2.0)
    assert np.all(windows["strong_upper"] < windows["weak_upper"])
    assert np.all(windows["deterministic_lower"] < windows["strong_upper"])
