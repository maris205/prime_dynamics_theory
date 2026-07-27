import numpy as np
import pytest

from branch_correspondence import branch_matching_data, conjugate_representatives, synchronize_branches


def test_conjugate_representatives_and_unique_matching():
    coarse = np.array([-0.4 + 0.7j, -0.4 - 0.7j, 0.3 + 0.6j, 0.3 - 0.6j])
    fine = np.array([-0.45 - 0.68j, 0.35 + 0.57j, -0.45 + 0.68j, 0.35 - 0.57j])
    representatives = conjugate_representatives(coarse)
    assert np.all(representatives.real == np.sort(representatives.real))
    data = branch_matching_data(coarse, fine)
    assert data["real_order_assignment_unique"]
    assert data["assignment_cost_margin"] > 0.0


def test_channel_synchronization():
    first = np.array([-0.4 + 0.7j, -0.4 - 0.7j, 0.3 + 0.6j, 0.3 - 0.6j])
    second = first + np.array([0.001j, -0.001j, 0.002, 0.002])
    data = synchronize_branches(first, second)
    assert data["maximum_branch_mismatch"] <= 0.0021


def test_real_mode_is_rejected():
    with pytest.raises(ValueError):
        conjugate_representatives(np.array([0.2, -0.3, 0.4j, -0.4j]))
