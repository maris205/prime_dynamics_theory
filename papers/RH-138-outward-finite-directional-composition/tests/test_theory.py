import numpy as np

from outward_directional import directional_lower, outward_base_lower, outward_two_residual_certificate


def test_two_residual_certificate_on_exact_diagonal_data():
    gram = np.diag([1.0, 2.0])
    tail = np.diag([0.1, 0.2])
    target_gram = np.diag([1.5, 3.0])
    forcing = np.diag([0.05, 0.1])
    raw = 0.5
    target_tail = raw * tail + forcing
    source_bound = 0.1
    target_bound = (raw * source_bound * 2.0 + 0.1) / 3.0
    result = outward_two_residual_certificate(
        gram, tail, target_gram, target_tail, forcing, np.eye(2), raw,
        source_bound, target_bound, 0.0, 0.0, 0.0, 0.0, 0.0,
    )
    assert result["both_certified"]


def test_outward_guards_reject_insufficient_rounding_slack():
    gram = np.eye(2)
    tail = 0.1 * np.eye(2)
    result = outward_two_residual_certificate(
        gram, tail, gram, tail, np.zeros((2, 2)), np.eye(2), 1.0,
        0.1, 0.1, 1e-6, 1e-6, 1e-6, 1e-6, 1e-6,
    )
    assert not result["both_certified"]


def test_base_and_directional_lower():
    gram = np.diag([1.0, 4.0])
    base = outward_base_lower(gram, 0.0)
    assert abs(base - 0.5) < 1e-12
    assert abs(directional_lower(0.25, base) - 0.5**5) < 1e-12
    assert outward_base_lower(gram, 1.0) == 0.0
