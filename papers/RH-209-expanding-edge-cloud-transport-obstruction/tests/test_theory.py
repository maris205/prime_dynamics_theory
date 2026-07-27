import numpy as np

from edge_cloud_transport import cloud_transport_data, ordered_edge_indices


def test_edge_indices_follow_modulus():
    values = np.array([0.1, -0.9, 0.4j, 0.7])
    assert set(ordered_edge_indices(values, 2)) == {1, 3}


def test_identical_embedded_cloud_has_zero_angle():
    embedding = np.eye(7, 4)
    coarse = np.eye(4, 3)
    data = cloud_transport_data(coarse, embedding @ coarse, embedding)
    assert data["maximum_principal_sine"] < 1e-7


def test_nesting_does_not_force_angle_monotonicity():
    embedding = np.eye(4)
    coarse_one = np.eye(4)[:, :1]
    fine_one = np.eye(4)[:, :1]
    coarse_two = np.eye(4)[:, :2]
    fine_two = np.column_stack([np.eye(4)[:, 0], np.eye(4)[:, 2]])
    first = cloud_transport_data(coarse_one, fine_one, embedding)
    second = cloud_transport_data(coarse_two, fine_two, embedding)
    assert first["maximum_principal_sine"] < 1e-7
    assert second["maximum_principal_sine"] > 0.99
