from fractions import Fraction

import numpy as np
import pytest

from folded_assembly import (
    compressed_assembly_defect,
    exact_stochastic_repair,
    full_sparse_row_l1,
    induced_two_norm_bound,
)


def test_full_sparse_l1_identity() -> None:
    weights = np.asarray([2.0, 3.0, 0.5])
    full = weights / np.sum(weights)
    sparse = np.asarray([2.0, 3.0, 0.0]) / 5.0
    assert np.linalg.norm(full - sparse, 1) == pytest.approx(
        full_sparse_row_l1(0.5, 5.5)
    )


def test_exact_stochastic_repair() -> None:
    row = np.asarray([0.1, 0.2, 0.6999999999999998])
    pivot, correction, repaired = exact_stochastic_repair(row)
    assert pivot == 2
    assert sum(repaired, Fraction(0, 1)) == 1
    assert repaired[pivot] - Fraction.from_float(float(row[pivot])) == correction
    assert all(value > 0 for value in repaired)


def test_compressed_defect_formula() -> None:
    result = compressed_assembly_defect(1.0e-8, 2.0e-16, 1.4, 1.0)
    assert result.compressed_two_norm_defect_upper >= 1.0e-8
    assert result.compressed_two_norm_defect_upper < 1.0000001e-8
    assert induced_two_norm_bound(4.0, 9.0) == pytest.approx(6.0)


@pytest.mark.parametrize(
    "call",
    [
        lambda: full_sparse_row_l1(-1.0, 1.0),
        lambda: full_sparse_row_l1(2.0, 1.0),
        lambda: induced_two_norm_bound(-1.0, 1.0),
        lambda: exact_stochastic_repair(np.asarray([1.0, -0.1])),
    ],
)
def test_invalid_inputs_are_rejected(call) -> None:
    with pytest.raises(ValueError):
        call()
