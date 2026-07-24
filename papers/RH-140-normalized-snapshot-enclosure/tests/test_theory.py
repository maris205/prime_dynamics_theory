import math

import numpy as np
import pytest

from snapshot_enclosure import normalized_snapshot, sharp_witness, snapshot_bounds, svd_split_bounds


def distances(first, second):
    difference = normalized_snapshot(first) - normalized_snapshot(second)
    values = np.linalg.eigvalsh(difference)
    return max(abs(values[0]), abs(values[-1])), np.linalg.norm(difference, "fro"), np.sum(abs(values))


@pytest.mark.parametrize("delta", [0.0, 0.1, 0.5, 0.9, 0.999])
def test_sharp_witness_attains_all_constants(delta):
    source, approximant = sharp_witness(delta)
    error = np.linalg.norm(source - approximant, "fro")
    bounds = snapshot_bounds(error, np.linalg.norm(source, "fro"), np.linalg.norm(approximant, "fro"))
    operator, frobenius, trace = distances(source, approximant)
    assert operator == pytest.approx(bounds["operator_radius"], abs=2e-13)
    assert frobenius == pytest.approx(bounds["frobenius_radius"], abs=2e-13)
    assert trace == pytest.approx(bounds["trace_radius"], abs=2e-13)


def test_orthogonal_svd_split_has_quadratic_trace_distance():
    source = np.diag([3.0, 2.0, 1.0])
    approximant = np.diag([3.0, 2.0, 0.0])
    q = np.linalg.norm(source - approximant, "fro") / np.linalg.norm(source, "fro")
    operator, frobenius, trace = distances(source, approximant)
    bounds = svd_split_bounds(q)
    assert operator <= bounds["operator_radius"] + 1e-14
    assert frobenius <= bounds["frobenius_radius"] + 1e-14
    assert trace == pytest.approx(bounds["trace_radius"], abs=1e-14)


def test_normalization_rejects_zero_and_bad_radius():
    with pytest.raises(ValueError):
        normalized_snapshot(np.zeros((2, 2)))
    with pytest.raises(ValueError):
        snapshot_bounds(-1.0, 1.0)
    with pytest.raises(ValueError):
        svd_split_bounds(1.1)

