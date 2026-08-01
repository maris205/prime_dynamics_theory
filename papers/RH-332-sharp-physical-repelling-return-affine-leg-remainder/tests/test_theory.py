import math

from repelling_return import (
    ALPHA,
    CRITICAL_PARTITION,
    CURVATURE_L1_SLOPE,
    LAMBDA,
    R_FIXED,
    U_C,
    composite_simpson,
    critical_partition_obstruction_lower_bound,
    critical_partition_source,
    curved_second_density,
    exact_curvature_shift_l1,
    exact_curved_boundary_l1,
    fixed_row_linear_coefficient,
    gaussian_shift_l1,
    limiting_intermediate_density,
    normal_cdf,
    normal_survival,
    physical_row_normalizer_at_x,
    physical_second_row_density,
    physical_tangent_triangle_bounds,
    repelling_displacement,
    sector_curvature_proxy,
    sector_intermediate_second_moment,
    state_interval,
    tangent_second_density,
    total_intermediate_second_moment,
    total_transported_linear_coefficient,
)


def _numerical_l1(function, reference, lower, upper, intervals=26000):
    return composite_simpson(
        lambda value: abs(function(value) - reference(value)),
        lower,
        upper,
        intervals,
    )


def test_constants_and_exact_repelling_expansion():
    assert math.isclose(R_FIXED, U_C - 1.0, rel_tol=1e-15)
    assert math.isclose(LAMBDA, 2.0 * U_C * R_FIXED, rel_tol=1e-15)
    assert math.isclose(ALPHA, 2.0 * U_C, rel_tol=1e-15)
    sigma = 0.07
    source = -0.8
    exact_image = 1.0 - U_C * (R_FIXED + sigma * source) ** 2
    expanded = R_FIXED - sigma * repelling_displacement(sigma, source)
    assert math.isclose(exact_image, expanded, rel_tol=1e-14, abs_tol=1e-14)


def test_exact_physical_second_row_normalization():
    sigma = 0.09
    source = 0.6
    lower, upper = state_interval(sigma)
    mass = composite_simpson(
        lambda output: physical_second_row_density(output, sigma, source),
        lower,
        upper,
        30000,
    )
    normalizer = physical_row_normalizer_at_x(
        sigma, R_FIXED + sigma * source
    )
    assert 0.0 < normalizer <= 1.0
    assert math.isclose(mass, 1.0, rel_tol=3e-10, abs_tol=3e-10)


def test_exact_physical_to_curved_boundary_identity():
    sigma = 0.10
    source = -0.75
    lower, upper = state_interval(sigma)
    inside = _numerical_l1(
        lambda output: physical_second_row_density(output, sigma, source),
        lambda output: curved_second_density(output, sigma, source),
        lower,
        upper,
    )
    displacement = repelling_displacement(sigma, source)
    outside = normal_cdf(lower + displacement) + normal_survival(
        upper + displacement
    )
    assert math.isclose(
        inside + outside,
        exact_curved_boundary_l1(sigma, source),
        rel_tol=3e-9,
        abs_tol=3e-11,
    )


def test_exact_curved_to_tangent_shift_identity():
    sigma = 0.08
    source = 1.1
    numerical = _numerical_l1(
        lambda output: curved_second_density(output, sigma, source),
        lambda output: tangent_second_density(output, source),
        -14.0,
        14.0,
    )
    assert math.isclose(
        numerical,
        exact_curvature_shift_l1(sigma, source),
        rel_tol=5e-8,
        abs_tol=5e-9,
    )
    assert math.isclose(
        exact_curvature_shift_l1(sigma, source),
        gaussian_shift_l1(U_C * sigma * source * source),
    )


def test_physical_to_tangent_row_obeys_triangle_interval():
    sigma = 0.08
    source = -0.5
    lower, upper = state_interval(sigma)
    numerical = _numerical_l1(
        lambda output: physical_second_row_density(output, sigma, source),
        lambda output: tangent_second_density(output, source),
        lower,
        upper,
        30000,
    )
    numerical += normal_cdf(lower + LAMBDA * source)
    numerical += normal_survival(upper + LAMBDA * source)
    lower_bound, upper_bound = physical_tangent_triangle_bounds(sigma, source)
    assert lower_bound - 4e-10 <= numerical <= upper_bound + 4e-10


def test_fixed_row_sharp_coefficient_and_zero_source_exception():
    source = 1.2
    sigma = 0.001
    assert math.isclose(
        exact_curvature_shift_l1(sigma, source) / sigma,
        fixed_row_linear_coefficient(source),
        rel_tol=4e-6,
    )
    assert fixed_row_linear_coefficient(0.0) == 0.0
    assert fixed_row_linear_coefficient(source) > 0.0


def test_limiting_intermediate_density_and_sector_moments():
    phase = 0.5
    mass = composite_simpson(
        lambda source: limiting_intermediate_density(source, phase),
        -24.0,
        24.0,
        30000,
    )
    negative = sector_intermediate_second_moment(phase, positive=False)
    positive = sector_intermediate_second_moment(phase, positive=True)
    assert math.isclose(mass, 1.0, rel_tol=2e-11, abs_tol=2e-11)
    assert negative > 0.0
    assert positive > 0.0
    assert math.isclose(
        negative + positive,
        total_intermediate_second_moment(phase),
        rel_tol=3e-9,
        abs_tol=3e-9,
    )


def test_sector_curvature_proxies_converge_to_sharp_coefficients():
    phase = 0.0
    sigma = 0.0025
    for positive in (False, True):
        proxy = sector_curvature_proxy(sigma, phase, positive=positive)
        target = CURVATURE_L1_SLOPE * sector_intermediate_second_moment(
            phase, positive=positive
        )
        assert math.isclose(proxy / sigma, target, rel_tol=3e-3)
    assert total_transported_linear_coefficient(phase) > 0.0


def test_critical_partition_gives_global_uniformity_obstruction():
    values = [
        critical_partition_obstruction_lower_bound(sigma)
        for sigma in (0.08, 0.04, 0.02)
    ]
    assert R_FIXED < CRITICAL_PARTITION < 1.0
    assert critical_partition_source(0.04) > 0.0
    assert values[0] < values[1] < values[2]
    assert values[2] > 0.98
