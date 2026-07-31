import math

from paired_affine import (
    ALPHA,
    BETA,
    KAPPA_AFF,
    LAMBDA,
    S1,
    S2,
    U_C,
    collapsed_output_density,
    covariance_matrix,
    entrance_mean,
    entrance_variance,
    exact_endpoint_l1_tail,
    first_leg_density,
    folded_endpoint_density,
    halfline_density,
    intermediate_density,
    intermediate_positive_probability_at_zero,
    joint_l1_bound,
    mean_vector,
    normal_cdf,
    normal_survival,
    oriented_joint_density,
    output_density,
    output_negative_probability_at_zero,
    output_reference_ratio,
    output_tail_ratio_limit,
    second_leg_density,
)


def _simpson(function, lower, upper, intervals=16000):
    if intervals % 2:
        intervals += 1
    step = (upper - lower) / intervals
    total = function(lower) + function(upper)
    total += 4.0 * sum(function(lower + step * index) for index in range(1, intervals, 2))
    total += 2.0 * sum(function(lower + step * index) for index in range(2, intervals, 2))
    return total * step / 3.0


def test_repository_constants_and_signed_two_leg_collapse():
    assert math.isclose(ALPHA, 2.0 * U_C, rel_tol=1e-15)
    assert math.isclose(KAPPA_AFF, ALPHA * LAMBDA, rel_tol=1e-15)
    assert math.isclose(BETA * BETA, 1.0 + LAMBDA * LAMBDA, rel_tol=1e-15)
    assert math.isclose(S1 * S1, 1.0 + ALPHA * ALPHA, rel_tol=1e-15)
    assert math.isclose(S2 * S2, KAPPA_AFF * KAPPA_AFF + BETA * BETA, rel_tol=1e-15)
    entrance = 0.7
    output = 2.0
    direct = _simpson(
        lambda intermediate: first_leg_density(intermediate, entrance)
        * second_leg_density(output, intermediate),
        -16.0,
        16.0,
    )
    assert math.isclose(
        direct,
        collapsed_output_density(output, entrance),
        rel_tol=2e-11,
        abs_tol=2e-12,
    )


def test_explicit_marginals_match_convolution_and_normalize():
    ratio = 0.7
    for intermediate in (-4.0, -1.0, 1.5):
        direct = _simpson(
            lambda entrance: halfline_density(entrance, ratio)
            * first_leg_density(intermediate, entrance),
            0.0,
            12.0,
        )
        assert math.isclose(
            direct, intermediate_density(intermediate, ratio), rel_tol=3e-10, abs_tol=3e-12
        )
    for output in (-2.0, 3.0, 8.0):
        direct = _simpson(
            lambda entrance: halfline_density(entrance, ratio)
            * collapsed_output_density(output, entrance),
            0.0,
            12.0,
        )
        assert math.isclose(direct, output_density(output, ratio), rel_tol=3e-10, abs_tol=3e-12)
    assert math.isclose(
        _simpson(lambda value: intermediate_density(value, ratio), -32.0, 18.0),
        1.0,
        rel_tol=2e-10,
        abs_tol=2e-10,
    )
    assert math.isclose(
        _simpson(lambda value: output_density(value, ratio), -24.0, 44.0, 24000),
        1.0,
        rel_tol=2e-10,
        abs_tol=2e-10,
    )


def test_moment_and_covariance_formulas():
    ratio = 0.6
    means = mean_vector(ratio)
    covariance = covariance_matrix(ratio)
    intermediate_mean = _simpson(
        lambda value: value * intermediate_density(value, ratio), -32.0, 18.0
    )
    intermediate_second = _simpson(
        lambda value: value * value * intermediate_density(value, ratio), -32.0, 18.0
    )
    output_mean = _simpson(
        lambda value: value * output_density(value, ratio), -24.0, 44.0, 24000
    )
    output_second = _simpson(
        lambda value: value * value * output_density(value, ratio),
        -24.0,
        44.0,
        24000,
    )
    assert math.isclose(intermediate_mean, means[1], rel_tol=3e-10, abs_tol=3e-10)
    assert math.isclose(output_mean, means[2], rel_tol=3e-10, abs_tol=3e-10)
    assert math.isclose(
        intermediate_second - intermediate_mean * intermediate_mean,
        covariance[1][1],
        rel_tol=5e-10,
        abs_tol=5e-10,
    )
    assert math.isclose(
        output_second - output_mean * output_mean,
        covariance[2][2],
        rel_tol=5e-10,
        abs_tol=5e-10,
    )
    assert math.isclose(covariance[0][1], -ALPHA * entrance_variance(ratio))
    assert math.isclose(covariance[1][2], -LAMBDA * covariance[1][1])
    assert entrance_mean(ratio) > ratio


def test_joint_markov_transfer_and_exact_same_phase_tail():
    sigma = 0.2
    ratio = 0.8
    scale = 1.0 / sigma
    finite_part = _simpson(
        lambda entrance: abs(
            folded_endpoint_density(entrance, sigma, ratio)
            - halfline_density(entrance, ratio)
        ),
        0.0,
        scale,
    )
    limiting_tail = normal_survival(scale - ratio) / normal_cdf(ratio)
    assert math.isclose(
        finite_part + limiting_tail,
        exact_endpoint_l1_tail(sigma, ratio),
        rel_tol=2e-10,
        abs_tol=2e-10,
    )
    assert math.isclose(
        joint_l1_bound(sigma, ratio, ratio), exact_endpoint_l1_tail(sigma, ratio)
    )
    conditional_mass = _simpson(
        lambda intermediate: first_leg_density(intermediate, 0.5), -14.0, 14.0
    )
    assert math.isclose(conditional_mass, 1.0, rel_tol=2e-12, abs_tol=2e-12)
    joint_slice = oriented_joint_density(0.5, -1.0, 2.0, ratio)
    assert joint_slice > 0.0


def test_output_is_not_gaussian_and_both_orientations_survive():
    ratio = 0.5
    assert math.isclose(
        output_reference_ratio(30.0, ratio),
        output_tail_ratio_limit(ratio),
        rel_tol=1e-13,
    )
    assert output_tail_ratio_limit(ratio) > 1.0
    probability_u_positive = _simpson(
        lambda entrance: halfline_density(entrance, 0.0) * normal_cdf(-ALPHA * entrance),
        0.0,
        10.0,
    )
    probability_w_negative = _simpson(
        lambda entrance: halfline_density(entrance, 0.0)
        * normal_cdf(-KAPPA_AFF * entrance / BETA),
        0.0,
        10.0,
    )
    assert math.isclose(
        probability_u_positive,
        intermediate_positive_probability_at_zero(),
        rel_tol=3e-11,
        abs_tol=3e-12,
    )
    assert math.isclose(
        probability_w_negative,
        output_negative_probability_at_zero(),
        rel_tol=3e-11,
        abs_tol=3e-12,
    )
    assert 0.09 < probability_u_positive < 0.11
    assert 0.11 < probability_w_negative < 0.12
