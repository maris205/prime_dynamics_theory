import numpy as np

from resonance_cloud import (
    cloud_gauge,
    conjugacy_error,
    conjugate_shells,
    reciprocal_zeros,
    select_shell_complete_cloud,
)


def test_shell_completion_repairs_split_pair():
    values = np.asarray([0.8 + 0.2j, 0.8 - 0.2j, -0.5, 0.3 + 0.4j, 0.3 - 0.4j])
    shells = conjugate_shells(values)
    cloud, selected = select_shell_complete_cloud(shells, 4)
    assert cloud.size == 5
    assert len(selected) == 3
    assert conjugacy_error(cloud) == 0.0


def test_unmatched_candidate_boundary_is_discarded():
    values = np.asarray([0.8 + 0.2j, 0.8 - 0.2j, 0.3 + 0.4j])
    shells = conjugate_shells(values)
    assert sum(shell.size for shell in shells) == 2


def test_global_gauge_and_reciprocal_identity():
    values = np.asarray([0.7 + 0.2j, 0.7 - 0.2j, -0.4 + 0.1j, -0.4 - 0.1j])
    gauge = cloud_gauge(values)
    normalized = np.asarray(gauge["normalized"])
    assert abs(np.mean(normalized)) < 1e-14
    assert abs(np.mean(np.abs(normalized) ** 2) - 1.0) < 1e-14
    assert np.allclose(reciprocal_zeros(values) * values, 1.0)
