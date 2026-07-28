import numpy as np

from coefficient_anchor import (
    exponential_coefficients_from_trace,
    one_step_numerator_trace_coefficient,
    trace_log_jet,
    two_step_anchor_from_one_step,
)


def test_one_step_pole_correction_and_hardy_scaling():
    value = one_step_numerator_trace_coefficient(
        1.2, 2, 1.6, hardy_radius=0.8
    )
    expected = (1.2 - 2.0 + 2.0 / 1.6) / 0.8**2
    assert abs(value - expected) < 1.0e-14
    odd = one_step_numerator_trace_coefficient(
        0.3, 3, 1.6, hardy_radius=0.8
    )
    assert abs(odd - 0.3 / 0.8**3) < 1.0e-14


def test_symmetric_two_step_dictionary_and_exponential_recursion():
    orders = np.arange(2, 9)
    anchors = np.asarray([0.5, 0.3, 0.2, 0.1, 0.08, 0.04, 0.02])
    two_orders, two_values = two_step_anchor_from_one_step(orders, anchors)
    z = 0.17 + 0.03j
    assert abs(
        trace_log_jet(orders, anchors, z)
        + trace_log_jet(orders, anchors, -z)
        - trace_log_jet(two_orders, two_values, z * z)
    ) < 1.0e-14
    traces = np.zeros(5, dtype=complex)
    traces[2] = 0.5
    coefficients = exponential_coefficients_from_trace(traces, 4)
    assert abs(coefficients[2] + 0.25) < 1.0e-14
    assert abs(coefficients[4] - 0.03125) < 1.0e-14
