import numpy as np

from gaussian_response.schedules import power_weighted_schedule_means


def test_unanchored_weighted_means_have_common_leading_scale():
    kappa = 0.031
    p = 2.0
    c = 10.0
    exponents = (0.0, 1.0, 3.0)
    spreads = []
    for T in (20_000, 500_000):
        means = power_weighted_schedule_means(T, exponents, kappa=kappa, p=p, c=c)
        scaled = np.array(list(means.values())) * np.log(T + c) ** p / kappa
        assert np.all(scaled > 1.0)
        assert np.all(np.diff(scaled) < 0.0)
        spreads.append(np.max(scaled) - np.min(scaled))
    assert spreads[1] < spreads[0]


def test_anchored_power_weights_approach_logarithmic_age_moments():
    exponents = (0.0, 1.0, 3.0)
    kappa = 0.02
    p = 2.0
    c = 10.0
    targets = 1.0 / (np.array(exponents) + 1.0)
    errors = []
    for T in (20_000, 500_000):
        means = power_weighted_schedule_means(
            T, exponents, kappa=kappa, p=p, c=c, anchored=True
        )
        log_scale = np.log(T + c)
        scaled = (
            np.array([means[a] for a in exponents])
            * log_scale ** (p + 1.0)
            / (p * kappa)
        )
        errors.append(np.max(np.abs(scaled - targets)))
    assert errors[1] < errors[0]
