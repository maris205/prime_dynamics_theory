import numpy as np

from integer_selector import signed_lattice_size, solve_bounded_signed_integer


def test_unit_cap_integer_solver_finds_exact_signed_solution():
    matrix = np.asarray([[1.0, 0.0], [0.0, 1.0]])
    target = np.asarray([1.0, -1.0])
    result = solve_bounded_signed_integer(target, matrix, np.asarray([2, 3]), cap=1)
    assert result["distance"] < 1e-12
    np.testing.assert_array_equal(result["weights"], np.asarray([1, -1]))


def test_signed_lattice_size():
    assert signed_lattice_size(4, 1) == 81
    assert signed_lattice_size(3, 2) == 125
