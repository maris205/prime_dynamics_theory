import numpy as np

from physical_matching import (
    contour_count,
    nearest_unique_matching,
    normalize_left_eigenvector,
    source_observation_mode,
    subspace_gap,
    trace_power_errors,
)


def test_matching_mode_residue_and_alignment():
    A = np.array([[0.4, 1.0], [0.0, -0.2]], dtype=complex)
    values, vectors = np.linalg.eig(A)
    left_values, left_vectors = np.linalg.eig(A.conj().T)
    order = [int(np.argmin(abs(left_values - np.conj(value)))) for value in values]
    S = np.array([[1.0, 0.2], [0.3, 1.0]], dtype=complex)
    O = np.array([[0.5, -0.2], [0.7, 0.4]], dtype=complex)
    packet = values + np.array([1e-5, -2e-5])
    matching = nearest_unique_matching(packet, values)
    assert set(matching) == {0, 1}
    for index in matching:
        left = normalize_left_eigenvector(vectors[:, index], left_vectors[:, order[index]])
        assert abs(np.vdot(left, vectors[:, index]) - 1.0) < 1e-12
        mode = source_observation_mode(vectors[:, index], left, S, O)
        assert abs(np.vdot(mode["left_state"], mode["right_state"]) - mode["residue"]) < 1e-12
    assert contour_count(values, values[0], 0.05) == 1
    assert subspace_gap(np.eye(3)[:, :2], np.eye(3)[:, :2])["maximum_principal_sine"] < 1e-12


def test_trace_power_identity_for_exact_diagonal_packet():
    values = np.array([0.2 + 0.3j, 0.2 - 0.3j])
    records = trace_power_errors(np.diag(values), values, 6)
    assert max(item["absolute_error"] for item in records) < 1e-14
