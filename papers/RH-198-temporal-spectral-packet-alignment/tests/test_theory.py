import numpy as np

from packet_alignment import endpoint_is_minimum, graph_tangent, log_linear_decay


def test_graph_tangent_matches_principal_angle():
    theta = 0.3
    exact = np.array([[1.0], [0.0]])
    approximate = np.array([[np.cos(theta)], [np.sin(theta)]])
    data = graph_tangent(exact, approximate)
    assert abs(data["maximum_tangent"] - np.tan(theta)) < 1e-12
    assert abs(data["maximum_sine"] - np.sin(theta)) < 1e-12


def test_log_decay_fit_and_endpoint():
    indices = [2, 3, 4, 5]
    values = [0.5 * 0.8**index for index in indices]
    data = log_linear_decay(indices, values)
    assert abs(data["per_step_ratio"] - 0.8) < 1e-12
    assert data["r_squared"] > 0.999999
    assert endpoint_is_minimum(values)
