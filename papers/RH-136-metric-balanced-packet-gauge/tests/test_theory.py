import numpy as np

from metric_balanced_gauge import metric_inflation, metric_optimal_alignment, polar_blend, polar_frame_alignment


def test_metric_minimax_alignment():
    source = np.diag([1.0, 4.0])
    target = np.diag([2.0, 2.0])
    result = metric_optimal_alignment(source, target)
    assert abs(result["minimum_metric_factor"] - 2.0) < 1e-12
    orthogonal = result["target_to_source"]
    values = np.linalg.eigvalsh(np.linalg.solve(target, orthogonal.T @ source @ orthogonal))
    assert max(values) <= 2.0 + 1e-12
    assert abs(metric_inflation(source, target, orthogonal) - 2.0) < 1e-12


def test_ordered_eigenframe_value_is_a_lower_bound_for_random_gauges():
    rng = np.random.default_rng(136)
    source = np.diag([0.4, 1.2, 3.0, 7.5])
    target = np.diag([0.7, 1.6, 2.2, 9.0])
    optimum = metric_optimal_alignment(source, target)["minimum_metric_factor"]
    for _ in range(128):
        candidate, _ = np.linalg.qr(rng.normal(size=(4, 4)))
        assert metric_inflation(source, target, candidate) >= optimum - 1e-11


def test_metric_optimum_exists_in_both_orthogonal_components():
    source = np.diag([0.4, 1.2, 3.0, 7.5])
    target = np.diag([0.7, 1.6, 2.2, 9.0])
    result = metric_optimal_alignment(source, target)
    first = result["target_to_source"]
    reflection = first @ np.diag([-1.0, 1.0, 1.0, 1.0])
    assert np.sign(np.linalg.det(first)) != np.sign(np.linalg.det(reflection))
    assert abs(metric_inflation(source, target, first) - result["minimum_metric_factor"]) < 1e-12
    assert abs(metric_inflation(source, target, reflection) - result["minimum_metric_factor"]) < 1e-12


def test_polar_frame_and_blend_are_orthogonal():
    source = np.eye(3)[:, :2]
    target = np.array([[1.0, 0.0], [0.0, 0.8], [0.0, 0.6]])
    polar = polar_frame_alignment(source, target)
    assert np.linalg.norm(polar.T @ polar - np.eye(2), 2) < 1e-12
    other = np.array([[0.0, 1.0], [-1.0, 0.0]])
    blend = polar_blend(polar, other, 0.3)
    assert np.linalg.norm(blend.T @ blend - np.eye(2), 2) < 1e-12
