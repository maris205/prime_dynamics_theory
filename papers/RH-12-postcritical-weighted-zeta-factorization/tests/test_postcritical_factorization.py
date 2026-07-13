from __future__ import annotations

import numpy as np

from postcritical_zeta import (
    LAMBDA_FIXED,
    R_FIXED,
    U_CRITICAL,
    centered_zeta_series,
    component_weighted_trace,
    component_weighted_trace_mp,
    deflated_zeta_series,
    lift_derivative,
    lift_map,
    lift_trace_audit,
    multiprecision_constants,
    postcritical_model,
    postcritical_remainder,
    quadratic_component_map,
)


def test_algebraic_constants_and_component_endpoints() -> None:
    u = U_CRITICAL
    polynomial = u**3 - 2 * u**2 + 2 * u - 2
    assert abs(polynomial) < np.longdouble("2e-18")
    assert abs(quadratic_component_map(-R_FIXED) - R_FIXED) < np.longdouble(
        "2e-18"
    )
    assert abs(quadratic_component_map(0) + R_FIXED) < np.longdouble("2e-18")
    assert abs(quadratic_component_map(R_FIXED) - R_FIXED) < np.longdouble(
        "2e-18"
    )


def test_lift_degree_symmetry_and_expansion() -> None:
    two_pi = 2.0 * np.pi
    points = np.linspace(0.0, two_pi, 101)
    images = lift_map(points, unwrapped=True)
    assert np.all(np.diff(images) > 0.0)
    assert abs(float(lift_map(two_pi, unwrapped=True) - lift_map(0.0, unwrapped=True)) - 4.0 * np.pi) < 2.0e-13
    assert np.max(np.abs(lift_map(points + np.pi) - lift_map(points))) < 3.0e-13
    derivative = lift_derivative(points)
    assert np.min(derivative) >= float(LAMBDA_FIXED) - 3.0e-14
    assert abs(float(lift_derivative(0.0)) - float(LAMBDA_FIXED)) < 3.0e-14
    assert abs(float(lift_derivative(np.pi)) - float(LAMBDA_FIXED)) < 3.0e-14


def test_component_traces_against_reference_values() -> None:
    expected = [
        0.8147325332053104247069447,
        0.7910151092089199977144063,
        0.8387046384007948011233650,
        0.8912308808183144502291804,
    ]
    for length, reference in enumerate(expected, start=1):
        audit = component_weighted_trace(length)
        assert audit.fixed_point_count == 2**length
        assert abs(float(audit.weighted_trace) - reference) < 2.0e-15
        assert audit.maximum_inverse_residual < np.longdouble("2e-17")


def test_exact_lift_trace_reconstruction() -> None:
    for length in range(1, 6):
        lift = lift_trace_audit(length)
        direct = component_weighted_trace(length)
        assert lift.fixed_count == 2**length - 1
        assert lift.twisted_fixed_count == 2**length + 1
        assert (
            abs(lift.reconstructed_component_trace - float(direct.weighted_trace))
            < 8.0e-14
        )


def test_multiprecision_independent_check() -> None:
    constants = multiprecision_constants(60)
    assert abs(float(constants.u) - float(U_CRITICAL)) < 2.0e-16
    assert abs(float(constants.lam) - float(LAMBDA_FIXED)) < 2.0e-16
    for length in range(1, 4):
        multiprecision = component_weighted_trace_mp(length, decimal_places=60)
        long_double = component_weighted_trace(length).weighted_trace
        assert abs(float(multiprecision) - float(long_double)) < 2.0e-15


def test_postcritical_deflation_formal_algebra() -> None:
    length = np.arange(1, 9, dtype=np.int64)
    model = postcritical_model(length)
    assert np.max(np.abs(postcritical_remainder(model))) < np.longdouble("2e-18")
    deflated = deflated_zeta_series(model)
    assert abs(deflated[0] - 1.0) < 2.0e-15
    assert np.max(np.abs(deflated[1:])) < 2.0e-15

    centered = centered_zeta_series(model)
    lam = float(LAMBDA_FIXED)
    numerator = np.asarray([1.0, -1.0 / lam])
    denominator_inverse = (1.0 / lam**2) ** np.arange(model.size + 1)
    expected = np.convolve(numerator, denominator_inverse)[: model.size + 1]
    assert np.max(np.abs(centered.real - expected)) < 3.0e-15
    assert np.max(np.abs(centered.imag)) < 3.0e-15
