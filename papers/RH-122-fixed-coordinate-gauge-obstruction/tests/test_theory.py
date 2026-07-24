import numpy as np
import pytest

from fixed_coordinate_obstruction import fixed_coordinate_constants, swap_obstruction_family


def test_swap_formula() -> None:
    for epsilon in (0.5, 0.1, 1e-4, 1e-9):
        row = swap_obstruction_family(epsilon, 0.3)
        assert row["gram_lower_factor"] == pytest.approx(epsilon)
        assert row["tail_upper_factor"] == pytest.approx(1.0 / epsilon)
        assert row["fixed_transfer_factor"] == pytest.approx(1.0 / epsilon)
        assert row["source_gamma"] == pytest.approx(row["target_gamma"])


def test_identity_constants_are_sharp() -> None:
    g = np.diag([1.0, 2.0, 4.0, 8.0])
    gp = np.diag([0.5, 3.0, 5.0, 10.0])
    d = np.diag([2.0, 3.0, 6.0, 9.0])
    dp = np.diag([4.0, 1.0, 7.0, 20.0])
    row = fixed_coordinate_constants(g, d, gp, dp)
    assert np.linalg.eigvalsh(gp - row["gram_lower_factor"] * g)[0] >= -1e-12
    assert np.linalg.eigvalsh(row["tail_upper_factor"] * d - dp)[0] >= -1e-12


def test_validation() -> None:
    with pytest.raises(ValueError):
        swap_obstruction_family(0.0)

