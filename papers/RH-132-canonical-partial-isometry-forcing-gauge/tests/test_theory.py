import numpy as np

from partial_isometry_gauge import canonical_partial_isometry, minimal_trace_forcing


def test_principal_angle_transport():
    source = np.eye(3)[:, :2]
    theta = 0.3
    target = np.array([[1.0, 0.0], [0.0, np.cos(theta)], [0.0, np.sin(theta)]])
    result = canonical_partial_isometry(source, target)
    assert result["overlap_rank"] == 2
    assert np.allclose(np.sort(result["principal_cosines"]), [np.cos(theta), 1.0])
    assert result["initial_defect"] < 1e-12
    assert result["final_defect"] < 1e-12


def test_positive_part_is_trace_minimal_and_dominates():
    target = np.diag([3.0, 0.5])
    transported = np.diag([1.0, 1.0])
    result = minimal_trace_forcing(target, transported, 1.0, final_projector=np.diag([1.0, 0.0]))
    assert np.allclose(result["forcing"], np.diag([2.0, 0.0]))
    assert abs(result["trace_cost"] - 2.0) < 1e-12
    assert result["minimum_slack_eigenvalue"] >= -1e-12
    assert abs(result["unmatched_target_trace_lower"] - 0.5) < 1e-12
