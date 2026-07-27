import numpy as np

from biorthogonal_clock import adjoint, balanced_biorthogonal_frames, oblique_projector, operator_norm


def test_balanced_frames_and_optimal_norm_product():
    right = np.array([[1.0, 0.0], [0.0, 1.0], [0.0, 0.0]])
    left = np.array([[0.8, 0.0], [0.0, 0.6], [0.6, 0.8]])
    data = balanced_biorthogonal_frames(right, left)
    v = data["right_frame"]
    w = data["left_frame"]
    assert operator_norm(adjoint(w) @ v - np.eye(2)) < 1e-12
    assert abs(operator_norm(v) * operator_norm(w) - data["optimal_norm_product"]) < 1e-12
    projector = oblique_projector(v, w)
    assert operator_norm(projector @ projector - projector) < 1e-12


def test_nontransverse_subspaces_are_rejected():
    right = np.array([[1.0], [0.0]])
    left = np.array([[0.0], [1.0]])
    try:
        balanced_biorthogonal_frames(right, left)
    except ValueError:
        pass
    else:
        raise AssertionError("orthogonal subspaces should not admit biorthogonal frames")
