import numpy as np

from shape_prediction import fit_clock, prediction_metrics


def test_power_gap_model_recovers_synthetic_law():
    sigma = np.asarray([0.02, 0.01, 0.005, 0.0025])
    u = 1.0 - 0.8 * sigma**0.3
    fit = fit_clock("power_gap", sigma, u)
    assert np.max(np.abs(fit.predict(sigma) - u)) < 1e-12


def test_prediction_metrics_are_zero_on_identity():
    values = np.asarray([0.2, 0.4, 0.7])
    assert prediction_metrics(values, values)["maximum_absolute_error"] == 0.0
