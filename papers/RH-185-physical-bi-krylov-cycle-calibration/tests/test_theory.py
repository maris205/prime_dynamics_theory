import numpy as np

from bi_krylov_calibration import bi_krylov_window_metrics


def test_exact_normal_cycle_has_zero_bi_ritz_residuals():
    operator = np.array([[0.0, -1.0], [1.0, 0.0]])
    right = np.eye(2)
    left = np.eye(2)

    def builder(x, y):
        return {
            "right_frame": x,
            "left_frame": y,
            "minimum_cross_singular_value": 1.0,
        }

    result = bi_krylov_window_metrics(
        operator,
        right,
        left,
        (2, 1),
        target_radius=1.0,
        wrap_phase=-1.0,
        balanced_builder=builder,
    )
    assert result["right_relative_residual"] < 1e-12
    assert result["left_relative_residual"] < 1e-12
    assert result["biorthogonality_defect"] < 1e-12


def test_phase_grid_error_detects_exact_twisted_roots():
    operator = np.array([[0.0, -2.0], [0.5, 0.0]])
    right = np.eye(2)
    left = np.eye(2)

    def builder(x, y):
        return {"right_frame": x, "left_frame": y, "minimum_cross_singular_value": 1.0}

    result = bi_krylov_window_metrics(operator, right, left, (2, 1), target_radius=1.0, wrap_phase=-1.0, balanced_builder=builder)
    assert result["compressed_cycle_phase_rms_error"] < 1e-12
