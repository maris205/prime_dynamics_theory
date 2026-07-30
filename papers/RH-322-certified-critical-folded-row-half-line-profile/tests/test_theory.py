import math

from folded_halfline import (
    compact_mills_l1_bound,
    direct_density,
    direct_mean,
    direct_normalizer,
    direct_second_moment,
    direct_wasserstein_tail,
    exact_l1_tail,
    exact_tv_tail,
    folded_density,
    folded_normalizer,
    halfline_density,
    limit_l1_distance,
    limit_mean,
    limit_moments,
    limit_second_moment,
    limit_variance,
    reflected_lobe_mass,
)


def _simpson(function, lower, upper, intervals=12000):
    if intervals % 2:
        intervals += 1
    step = (upper - lower) / intervals
    total = function(lower) + function(upper)
    total += 4.0 * sum(function(lower + step * index) for index in range(1, intervals, 2))
    total += 2.0 * sum(function(lower + step * index) for index in range(2, intervals, 2))
    return total * step / 3.0


def test_folded_normalizer_splits_into_two_lobes():
    sigma = 0.2
    ratio = 0.8
    assert math.isclose(
        folded_normalizer(sigma, ratio),
        direct_normalizer(sigma, ratio) + reflected_lobe_mass(sigma, ratio),
        rel_tol=1e-14,
        abs_tol=1e-15,
    )


def test_physical_folded_density_is_normalized_and_has_exact_tv_tail():
    sigma = 0.2
    ratio = 0.8
    scale = 1.0 / sigma
    mass = _simpson(lambda value: folded_density(value, sigma, ratio), 0.0, scale)
    assert math.isclose(mass, 1.0, rel_tol=2e-10, abs_tol=2e-10)
    for index in range(101):
        value = scale * index / 100.0
        assert folded_density(value, sigma, ratio) >= halfline_density(value, ratio)
    assert math.isclose(exact_l1_tail(sigma, ratio), 2.0 * exact_tv_tail(sigma, ratio))


def test_direct_finite_moments_and_wasserstein_identity():
    sigma = 0.2
    ratio = 0.7
    scale = 1.0 / sigma
    mean = _simpson(lambda value: value * direct_density(value, sigma, ratio), 0.0, scale)
    second = _simpson(
        lambda value: value * value * direct_density(value, sigma, ratio),
        0.0,
        scale,
    )
    assert math.isclose(mean, direct_mean(sigma, ratio), rel_tol=2e-10, abs_tol=2e-10)
    assert math.isclose(
        second,
        direct_second_moment(sigma, ratio),
        rel_tol=2e-10,
        abs_tol=2e-10,
    )
    assert math.isclose(
        limit_mean(ratio) - direct_mean(sigma, ratio),
        direct_wasserstein_tail(sigma, ratio),
        rel_tol=1e-13,
        abs_tol=1e-15,
    )


def test_limit_moments_and_phase_separation():
    moments = limit_moments(0.0, 4)
    assert math.isclose(moments[1], math.sqrt(2.0 / math.pi), rel_tol=1e-14)
    assert math.isclose(moments[2], 1.0, rel_tol=1e-14)
    assert math.isclose(limit_second_moment(0.0), 1.0, rel_tol=1e-14)
    assert math.isclose(limit_variance(0.0), 1.0 - 2.0 / math.pi, rel_tol=1e-14)
    separation = limit_l1_distance(0.0, 1.0)
    assert 0.5 < separation < 0.6
    assert math.isclose(separation, limit_l1_distance(1.0, 0.0), rel_tol=1e-14)


def test_mills_bound_controls_the_exact_tail():
    sigma = 0.125
    ratio = 1.0
    bound = compact_mills_l1_bound(
        sigma,
        ratio,
        minimum_ratio=0.0,
        maximum_ratio=1.5,
    )
    assert exact_l1_tail(sigma, ratio) <= bound
