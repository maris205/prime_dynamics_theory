import math

import mpmath as mp
import pytest

from raw_affine_escape import (
    C_B_REPRODUCTION,
    LAMBDA,
    TRACE_RADIUS,
    U_C,
    boundary_cycle,
    critical_constants,
    expanded_prefix_variance,
    finite_unhalved_l1_lower_bound,
    first_innovation_standard_deviation,
    first_innovation_standard_deviation_via_multiplier,
    forward_prefix_variance,
    forward_variance_step,
    gaussian_maximum_interval_mass,
    natural_clock_sigma,
    natural_target_scale,
    normal_cdf,
    phase_clearance,
    phase_l1_lower_bound,
    phase_propagated_scale,
    raw_prefix_expansion_coefficients,
    reproduction_C_s,
    two_step_map,
)


def test_rh17_cycle_order_sign_and_k_two_k_clock():
    cycle = boundary_cycle(8, 110)
    assert cycle.component_period == 8
    assert cycle.physical_period == 16
    assert len(cycle.orbit) == 8
    for index, point in enumerate(cycle.orbit):
        target = cycle.orbit[(index + 1) % cycle.component_period]
        assert mp.almosteq(two_step_map(point, 110), target, rel_eps=mp.mpf("1e-85"))
    assert cycle.signed_slopes[0] < 0
    assert all(slope > 0 for slope in cycle.signed_slopes[1:])


def test_exact_forward_expansion_and_first_innovation_product_identity():
    for component_period in (4, 8, 12, 16, 20, 24):
        cycle = boundary_cycle(component_period, 110)
        entrance, innovations = raw_prefix_expansion_coefficients(cycle)
        assert len(innovations) == component_period - 1
        assert entrance < 0
        direct = first_innovation_standard_deviation(cycle)
        quotient = first_innovation_standard_deviation_via_multiplier(cycle)
        with mp.workdps(110):
            assert mp.almosteq(direct, quotient, rel_eps=mp.mpf("1e-90"))


def test_first_innovation_scale_converges_toward_reproduction_C_s():
    constants = critical_constants(110)
    scaled = []
    for component_period in (4, 8, 12, 16, 20, 24):
        cycle = boundary_cycle(component_period, 110)
        scaled.append(
            float(
                first_innovation_standard_deviation(cycle)
                / constants.lambda_fixed ** (2 * component_period)
            )
        )
    errors = [abs(value - reproduction_C_s()) for value in scaled]
    assert all(left > right for left, right in zip(errors, errors[1:]))
    assert math.isclose(scaled[-1], reproduction_C_s(), rel_tol=3e-6)


def test_forward_variance_has_plus_noise_and_matches_expansion():
    assert forward_variance_step(3, -2, 5) == 17
    cycle = boundary_cycle(9, 100)
    recurrence = forward_prefix_variance(cycle, mp.mpf("1.25"))
    expansion = expanded_prefix_variance(cycle, mp.mpf("1.25"))
    with mp.workdps(100):
        assert mp.almosteq(recurrence, expansion, rel_eps=mp.mpf("1e-75"))


def test_gaussian_maximum_interval_mass_is_centered_and_uniform_in_mean():
    length = 2.3
    standard_deviation = 1.7
    exact = gaussian_maximum_interval_mass(length, standard_deviation)
    centered = 2 * normal_cdf(length / (2 * standard_deviation)) - 1
    displaced = normal_cdf((4 + length) / standard_deviation) - normal_cdf(
        4 / standard_deviation
    )
    assert math.isclose(exact, centered, rel_tol=1e-15)
    assert displaced < exact


def test_unhalved_support_bound_has_the_required_factor_four():
    sigma = 0.02
    propagated_sd = 30.0
    expected = 2.0 * (
        1.0
        - gaussian_maximum_interval_mass(1 / sigma, propagated_sd)
    )
    assert math.isclose(
        finite_unhalved_l1_lower_bound(sigma, propagated_sd),
        expected,
        rel_tol=2e-15,
    )
    assert 0 < expected < 2


def test_fixed_phase_relation_and_positive_compact_phase_floor():
    for eta in (-0.5, 0.0, 0.5):
        d = phase_clearance(eta)
        c_eta = phase_propagated_scale(eta)
        assert d > 0 and c_eta > 0 and phase_l1_lower_bound(eta) > 0
        assert math.isclose(
            c_eta, reproduction_C_s() * C_B_REPRODUCTION / d, rel_tol=2e-15
        )
    compact_floor = phase_l1_lower_bound(-0.5)
    assert compact_floor > 0
    assert all(
        phase_l1_lower_bound(eta) >= compact_floor
        for eta in (-0.5, -0.25, 0.0, 0.25, 0.5)
    )


def test_natural_clock_finite_bounds_tend_to_phase_limit_while_targets_vanish():
    eta = 0.0
    finite_bounds = []
    for component_period in (8, 12, 16, 20, 24):
        sigma = natural_clock_sigma(component_period, eta)
        cycle = boundary_cycle(component_period, 110)
        finite_bounds.append(
            finite_unhalved_l1_lower_bound(
                sigma, float(first_innovation_standard_deviation(cycle))
            )
        )
    assert math.isclose(finite_bounds[-1], phase_l1_lower_bound(eta), rel_tol=4e-5)
    assert natural_clock_sigma(24, eta) * 24 < natural_clock_sigma(8, eta) * 8
    assert natural_target_scale(24) < natural_target_scale(8)
    assert 1 < TRACE_RADIUS < LAMBDA


def test_invalid_parameters_fail_closed():
    with pytest.raises(ValueError):
        boundary_cycle(1)
    with pytest.raises(ValueError):
        gaussian_maximum_interval_mass(-1, 1)
    with pytest.raises(ValueError):
        finite_unhalved_l1_lower_bound(0, 1)
    with pytest.raises(ValueError):
        forward_variance_step(-1, 2, 1)
    assert 1 < U_C < 2
