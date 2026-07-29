import numpy as np

from signed_monodromy import (
    integer_lattice_distance,
    minimum_norm_signed_fit,
    monodromy_defect,
    weighted_moment_distance,
)


def test_minimum_norm_signed_fit_solves_full_row_rank_system():
    matrix = np.asarray([[1.0, 0.0, 1.0], [0.0, 1.0, 1.0]])
    target = np.asarray([1.0, -1.0])
    result = minimum_norm_signed_fit(matrix, target)
    assert result["rank"] == 2
    assert weighted_moment_distance(result["residual"], np.asarray([2, 3])) < 1e-14


def test_integer_weights_have_trivial_monodromy():
    weights = np.asarray([-2.0, 0.0, 3.0, 0.5])
    defects = monodromy_defect(weights)
    assert np.max(defects[:3]) < 1e-14
    assert abs(defects[3] - 2.0) < 1e-14
    distances = integer_lattice_distance(weights)
    assert np.max(distances[:3]) == 0.0
    assert distances[3] == 0.5
