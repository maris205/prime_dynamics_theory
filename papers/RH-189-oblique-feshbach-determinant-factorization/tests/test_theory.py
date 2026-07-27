import numpy as np

from oblique_feshbach import block_coordinates, feshbach_determinant_identity


def test_feshbach_identity_on_diagonal_matrix():
    operator = np.diag([1.0, 2.0, 4.0])
    right = np.array([[1.0], [0.0], [0.0]])
    left = right.copy()
    blocks = block_coordinates(operator, right, left)
    result = feshbach_determinant_identity(3.0, operator, blocks)
    assert result["relative_error"] < 1e-12


def test_oblique_coordinates_have_the_declared_blocks():
    operator = np.array([[1.0, 2.0], [0.0, 3.0]])
    right = np.array([[1.0], [0.0]])
    left = np.array([[1.0], [-0.5]])
    left = left / (left.T @ right)[0, 0]
    blocks = block_coordinates(operator, right, left)
    similarity = blocks["coordinate_inverse"] @ operator @ blocks["coordinate_matrix"]
    assembled = np.block([[blocks["K"], blocks["B"]], [blocks["C"], blocks["D"]]])
    assert np.linalg.norm(similarity - assembled, 2) < 1e-12
