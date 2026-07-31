import math

from physical_affine import (
    ALPHA,
    CANONICAL_ETA,
    CRITICAL_PARTITION,
    LAMBDA,
    R_FIXED,
    U_C,
    alias_scale_exponent,
    curvature_shift_l1,
    curved_gaussian_density,
    endpoint_branch_margin,
    entrance_second_moment,
    exact_curved_boundary_l1,
    exact_seed_l1_tail,
    finite_joint_l1_bound,
    folded_seed_density,
    gaussian_shift_l1,
    halfline_density,
    normal_cdf,
    normal_survival,
    output_coordinate_interval,
    physical_row_density,
    physical_row_normalizer,
    physical_joint_density,
    remainder_components,
    row_tangent_l1_bound,
    sharp_linear_coefficient,
    tangent_gaussian_density,
)


def _simpson(function, lower, upper, intervals=16000):
    if intervals % 2:
        intervals += 1
    step = (upper - lower) / intervals
    total = function(lower) + function(upper)
    total += 4.0 * sum(function(lower + step * index) for index in range(1, intervals, 2))
    total += 2.0 * sum(function(lower + step * index) for index in range(2, intervals, 2))
    return total * step / 3.0


def _numerical_row_l1(function, reference, lower, upper):
    inside = _simpson(lambda value: abs(function(value) - reference(value)), lower, upper)
    return inside


def test_constants_and_exact_physical_row_normalization():
    assert math.isclose(R_FIXED, U_C - 1.0, rel_tol=1e-15)
    assert math.isclose(LAMBDA, 2.0 * U_C * R_FIXED, rel_tol=1e-15)
    assert math.isclose(ALPHA, 2.0 * U_C, rel_tol=1e-15)
    assert 0.0 < CANONICAL_ETA < 1.0 - CRITICAL_PARTITION
    assert endpoint_branch_margin() > 0.25
    sigma = 0.08
    entrance = 0.6
    lower, upper = output_coordinate_interval(sigma)
    mass = _simpson(
        lambda output: physical_row_density(output, sigma, entrance), lower, upper
    )
    assert 0.0 < physical_row_normalizer(sigma, entrance) <= 1.0
    assert math.isclose(mass, 1.0, rel_tol=2e-10, abs_tol=2e-10)


def test_exact_curved_boundary_identity_and_tangent_bound():
    sigma = 0.10
    entrance = 0.2
    lower, upper = output_coordinate_interval(sigma)
    inside = _numerical_row_l1(
        lambda output: physical_row_density(output, sigma, entrance),
        lambda output: curved_gaussian_density(output, sigma, entrance),
        lower,
        upper,
    )
    parameter = ALPHA * entrance - U_C * sigma * entrance * entrance
    outside = normal_cdf(lower + parameter) + normal_survival(upper + parameter)
    numerical = inside + outside
    assert math.isclose(
        numerical,
        exact_curved_boundary_l1(sigma, entrance),
        rel_tol=2e-9,
        abs_tol=2e-12,
    )
    tangent_inside = _numerical_row_l1(
        lambda output: physical_row_density(output, sigma, entrance),
        lambda output: tangent_gaussian_density(output, entrance),
        lower,
        upper,
    )
    tangent_outside = normal_cdf(lower + ALPHA * entrance) + normal_survival(
        upper + ALPHA * entrance
    )
    assert tangent_inside + tangent_outside <= row_tangent_l1_bound(
        sigma, entrance
    ) + 3e-11


def test_gaussian_shift_formula_and_curvature_slope():
    displacement = 0.35
    numerical = _simpson(
        lambda value: abs(
            math.exp(-0.5 * value * value) / math.sqrt(2.0 * math.pi)
            - math.exp(-0.5 * (value - displacement) ** 2) / math.sqrt(2.0 * math.pi)
        ),
        -12.0,
        12.0,
    )
    assert math.isclose(numerical, gaussian_shift_l1(displacement), rel_tol=2e-10)
    sigma = 0.01
    entrance = 1.2
    expected = math.sqrt(2.0 / math.pi) * U_C * entrance * entrance
    assert math.isclose(
        curvature_shift_l1(sigma, entrance) / sigma,
        expected,
        rel_tol=3e-4,
    )


def test_sharp_phase_averaged_linear_coefficient():
    ratio = 0.5
    sigma = 0.005
    average = _simpson(
        lambda entrance: halfline_density(entrance, ratio)
        * curvature_shift_l1(sigma, entrance),
        0.0,
        14.0,
        24000,
    )
    assert math.isclose(
        average / sigma,
        sharp_linear_coefficient(ratio),
        rel_tol=2e-3,
    )
    assert sharp_linear_coefficient(ratio) > 0.0


def test_finite_seed_tail_and_explicit_joint_bound_components():
    sigma = 0.05
    ratio = 0.5
    scale = 1.0 / sigma
    seed_mass = _simpson(
        lambda entrance: folded_seed_density(entrance, sigma, ratio), 0.0, scale
    )
    assert math.isclose(seed_mass, 1.0, rel_tol=2e-10, abs_tol=2e-10)
    tail = normal_survival(scale - ratio) / normal_cdf(ratio)
    assert math.isclose(exact_seed_l1_tail(sigma, ratio), 2.0 * tail)
    components = remainder_components(sigma, ratio)
    assert components["curvature"] > 0.0
    assert all(value >= 0.0 for value in components.values())
    assert math.isclose(
        finite_joint_l1_bound(sigma, ratio, ratio), sum(components.values())
    )
    assert math.isclose(
        entrance_second_moment(0.0), 1.0, rel_tol=1e-15
    )


def test_physical_joint_density_respects_finite_seed_support():
    sigma = 0.05
    ratio = 0.5
    assert physical_joint_density(-0.1, 0.0, sigma, ratio) == 0.0
    assert physical_joint_density(1.0 / sigma + 0.1, 0.0, sigma, ratio) == 0.0
    assert physical_joint_density(0.5, 0.0, sigma, ratio) > 0.0


def test_first_alias_scale_exponent_is_strictly_sublinear():
    exponent = alias_scale_exponent()
    assert 0.64 < exponent < 0.66
    assert 1.0 - exponent > 0.3
