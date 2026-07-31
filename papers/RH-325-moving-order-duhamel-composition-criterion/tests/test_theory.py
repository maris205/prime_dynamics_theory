import math

from moving_duhamel import (
    ALIAS_EXPONENT,
    PACKET_CONDITIONING_LOWER_EXPONENT,
    LAMBDA,
    QUARTER_POWER_SLACK,
    STABILITY_GROWTH_THRESHOLD,
    TRACE_RADIUS,
    alias_clock,
    alias_scale,
    cyclic_trace_counterexample,
    endpoint_composition_l1,
    moving_order_budget,
    operator_duhamel_bound,
    operator_duhamel_terms,
    phase_transport_counterexample,
    retained_path_duhamel_bound,
    retained_path_duhamel_terms,
    retained_path_l1,
    stability_power,
)


def test_alias_constants_and_sharp_stability_window():
    assert math.isclose(
        ALIAS_EXPONENT,
        math.log(TRACE_RADIUS) / math.log(LAMBDA),
        rel_tol=1e-15,
    )
    assert 0.649 < ALIAS_EXPONENT < 0.650
    assert math.isclose(
        STABILITY_GROWTH_THRESHOLD,
        1.0 - ALIAS_EXPONENT,
        rel_tol=1e-15,
    )
    assert 0.350 < STABILITY_GROWTH_THRESHOLD < 0.351
    assert math.isclose(
        QUARTER_POWER_SLACK,
        STABILITY_GROWTH_THRESHOLD - PACKET_CONDITIONING_LOWER_EXPONENT,
        rel_tol=1e-15,
    )
    assert 0.100 < QUARTER_POWER_SLACK < 0.101


def test_retained_path_duhamel_bound_and_endpoint_contraction():
    initial = (0.6, 0.4)
    physical = (
        ((0.9, 0.1), (0.2, 0.8)),
        ((0.7, 0.3), (0.1, 0.9)),
        ((0.8, 0.2), (0.4, 0.6)),
    )
    affine = (
        ((0.85, 0.15), (0.25, 0.75)),
        ((0.72, 0.28), (0.08, 0.92)),
        ((0.78, 0.22), (0.43, 0.57)),
    )
    terms = retained_path_duhamel_terms(initial, physical, affine)
    bound = retained_path_duhamel_bound(initial, physical, affine)
    path_error = retained_path_l1(initial, physical, affine)
    endpoint_error = endpoint_composition_l1(initial, physical, affine)
    assert len(terms) == 3
    assert math.isclose(bound, sum(terms), rel_tol=1e-15)
    assert endpoint_error <= path_error + 1e-15
    assert path_error <= bound + 1e-15


def test_seed_error_is_added_before_kernel_telescope():
    physical_initial = (0.55, 0.45)
    affine_initial = (0.5, 0.5)
    physical = (((0.8, 0.2), (0.1, 0.9)),)
    affine = (((0.75, 0.25), (0.15, 0.85)),)
    bound = retained_path_duhamel_bound(
        physical_initial,
        physical,
        affine,
        affine_initial=affine_initial,
    )
    path_error = retained_path_l1(
        physical_initial,
        physical,
        affine,
        affine_initial=affine_initial,
    )
    assert path_error <= bound + 1e-15
    assert bound >= 0.1


def test_phase_transport_same_seed_counterexample_is_maximal():
    data = phase_transport_counterexample()
    assert data["local_seed_error"] == 0.0
    assert data["transported_row_error"] == 2.0
    assert data["composed_endpoint_error"] == 2.0


def test_cyclic_markov_trace_counterexample_has_fixed_trace_gap():
    for dimension in (4, 16, 64, 256):
        data = cyclic_trace_counterexample(dimension)
        assert math.isclose(data["max_row_l1"], 2.0 / dimension)
        assert math.isclose(data["uniform_retained_path_l1"], 2.0 / dimension)
        assert data["uniform_endpoint_l1"] == 0.0
        assert math.isclose(data["trace_gap"], 1.0)
        assert math.isclose(data["trace_to_row_ratio"], dimension / 2.0)


def test_operator_duhamel_terms_keep_prefix_suffix_norms():
    physical_norms = (1.2, 0.8, 1.5)
    affine_norms = (0.9, 1.1, 0.7)
    errors = (0.01, 0.02, 0.03)
    terms = operator_duhamel_terms(
        physical_norms,
        affine_norms,
        errors,
        observation_norm=4.0,
    )
    expected = (
        4.0 * 0.8 * 1.5 * 0.01,
        4.0 * 1.5 * 0.02 * 0.9,
        4.0 * 0.03 * 0.9 * 1.1,
    )
    assert all(math.isclose(value, target) for value, target in zip(terms, expected))
    assert math.isclose(
        operator_duhamel_bound(
            physical_norms,
            affine_norms,
            errors,
            observation_norm=4.0,
        ),
        sum(expected),
    )


def test_moving_order_budget_has_the_predicted_power_transition():
    sigma = 1e-10
    clock = alias_clock(sigma)
    assert math.isclose(alias_scale(sigma), sigma**ALIAS_EXPONENT, rel_tol=2e-15)
    assert clock > 20.0
    subcritical = moving_order_budget(sigma, growth_exponent=0.25)
    critical = moving_order_budget(
        sigma, growth_exponent=STABILITY_GROWTH_THRESHOLD
    )
    supercritical = moving_order_budget(sigma, growth_exponent=0.4)
    assert stability_power(0.25) > 0.1
    assert math.isclose(
        stability_power(STABILITY_GROWTH_THRESHOLD), 0.0, abs_tol=1e-15
    )
    assert stability_power(0.4) < 0.0
    assert subcritical["normalized_ratio"] < critical["normalized_ratio"]
    assert critical["normalized_ratio"] < supercritical["normalized_ratio"]
