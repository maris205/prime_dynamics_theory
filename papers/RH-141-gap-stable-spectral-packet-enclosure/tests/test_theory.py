import numpy as np
import pytest

from spectral_packet import aligned_frame_radius, projector_enclosure, top_projector


def test_gap_enclosure_on_rotating_two_by_two_example():
    gap = 1.0
    approximate = np.diag([0.5, -0.5])
    perturbation = np.array([[0.0, 0.1], [0.1, 0.0]])
    exact = approximate + perturbation
    actual = np.linalg.norm(top_projector(exact, 1) - top_projector(approximate, 1), 2)
    result = projector_enclosure(gap, np.linalg.norm(perturbation, 2))
    assert result["stable"]
    assert actual <= result["projector_radius"]
    assert result["frame_radius"] == pytest.approx(aligned_frame_radius(result["projector_radius"]))


def test_two_radius_threshold_allows_swap_and_degeneracy():
    approximate = np.diag([0.5, -0.5])
    at_wall = approximate + np.diag([-0.5, 0.5])
    beyond = approximate + np.diag([-0.6, 0.6])
    assert np.linalg.eigvalsh(at_wall)[0] == pytest.approx(np.linalg.eigvalsh(at_wall)[1])
    assert np.linalg.norm(top_projector(beyond, 1) - top_projector(approximate, 1), 2) == pytest.approx(1.0)
    assert not projector_enclosure(1.0, 0.5)["stable"]
    assert not projector_enclosure(1.0, 0.6)["stable"]


def test_bad_inputs_are_rejected():
    with pytest.raises(ValueError):
        projector_enclosure(-1.0, 0.1)
    with pytest.raises(ValueError):
        aligned_frame_radius(1.1)
    with pytest.raises(ValueError):
        top_projector(np.eye(2), 2)

