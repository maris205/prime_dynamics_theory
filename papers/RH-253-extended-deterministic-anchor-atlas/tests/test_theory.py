import numpy as np

from anchor_atlas import (
    finite_logarithmic_norm,
    hardy_scaled_anchor,
    log_linear_root_rate,
    ordinary_coefficients_from_traces,
)


def test_anchor_dictionary_matches_known_order_two_value():
    value = hardy_scaled_anchor(1.1801429862402304, 2, 1.6785735104283177)
    assert abs(value - 0.5143679864267854) < 1e-14


def test_finite_norm_and_root_rate():
    orders = np.asarray([2, 3, 4])
    coefficients = np.asarray([0.25, 0.125, 0.0625])
    assert abs(finite_logarithmic_norm(orders, coefficients) - (0.25 / 2 + 0.125 / 3 + 0.0625 / 4)) < 1e-15
    assert abs(log_linear_root_rate(orders, coefficients) - 0.5) < 1e-14


def test_trace_to_ordinary_coefficient_recursion():
    traces = np.zeros(5)
    traces[2] = 2.0
    traces[4] = 4.0
    ordinary = ordinary_coefficients_from_traces(traces)
    assert abs(ordinary[2] + 1.0) < 1e-15
    assert abs(ordinary[4] + 0.5) < 1e-15
