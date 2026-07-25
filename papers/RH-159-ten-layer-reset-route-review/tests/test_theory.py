import numpy as np
import pytest

from reset_route_review import classify_route, directional_to_native_lower, first_unresolved_gate


def test_positive_block_directional_to_native_inequality() -> None:
    rng = np.random.default_rng(159)
    factor = rng.normal(size=(9, 7))
    matrix = factor @ factor.T
    native = matrix[:4, :4]
    cross = matrix[4:, :4]
    complement = matrix[4:, 4:]
    complement_upper = float(np.linalg.norm(complement, 2))
    native_eigenvalues = np.linalg.eigvalsh(native)[::-1]
    cross_singular = np.linalg.svd(cross, compute_uv=False)
    for index in range(4):
        lower = directional_to_native_lower(float(cross_singular[index]), complement_upper)
        assert native_eigenvalues[index] >= lower * (1.0 - 1e-12)


def test_native_does_not_imply_cross_rank() -> None:
    native = np.diag([4.0, 3.0, 2.0, 1.0])
    complement = np.diag([0.5, 0.25, 0.1, 0.05])
    matrix = np.block([[native, np.zeros((4, 4))], [np.zeros((4, 4)), complement]])
    projector = np.diag([1.0] * 4 + [0.0] * 4)
    cross = (np.eye(8) - projector) @ matrix @ projector
    assert np.linalg.eigvalsh(native)[0] > 0.0
    assert np.linalg.norm(cross) == 0.0


def test_typed_route_classification() -> None:
    assert classify_route(["certified", "certified"]) == "finite_closed"
    assert classify_route(["certified", "open"]) == "open"
    assert classify_route(["certified", "obstruction", "open"]) == "rejected"
    assert first_unresolved_gate([("one", "certified"), ("two", "open")]) == "two"
    assert first_unresolved_gate([("one", "certified")]) is None


def test_invalid_route_data() -> None:
    with pytest.raises(ValueError):
        directional_to_native_lower(1.0, 0.0)
    with pytest.raises(ValueError):
        classify_route([])
    with pytest.raises(ValueError):
        classify_route(["optional"])
