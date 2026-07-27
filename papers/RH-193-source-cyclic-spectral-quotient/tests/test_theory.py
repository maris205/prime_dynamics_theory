import numpy as np

from source_cyclic import (
    moment_sequence,
    reduced_moment_sequence,
    source_cyclic_arnoldi,
    synthesis_inclusion_defect,
)


def test_diagonal_source_cyclic_restriction_preserves_moments():
    A = np.diag([0.2, -0.4, 0.7])
    S = np.array([[1.0, 0.2], [0.5, 1.0], [0.7, -0.3]])
    O = np.array([[0.4, -0.1], [1.2, 0.3], [-0.2, 0.8]])
    data = source_cyclic_arnoldi(A, S)
    assert data["closed"]
    assert data["dimension"] == 3
    full = moment_sequence(A, S, O, 8)
    reduced = reduced_moment_sequence(data["basis"], data["reduced_operator"], data["source_coordinate"], O, 8)
    assert np.allclose(full, reduced, atol=1e-12)


def test_temporal_synthesis_is_inside_cyclic_space():
    A = np.array([[0.2, 1.0], [0.0, -0.3]])
    S = np.array([[1.0, 0.0], [0.2, 1.0]])
    data = source_cyclic_arnoldi(A, S)
    synthesis = np.column_stack([S.reshape(-1), (A @ S).reshape(-1)])
    assert synthesis_inclusion_defect(data["basis"], synthesis) < 1e-12
