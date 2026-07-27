from directional_balance import directed_schur_feedback, scalar_gauge_balance, weighted_scalar_gauge_balance


def test_scalar_balance_is_optimal_and_product_invariant():
    result = scalar_gauge_balance(4.0, 1.0)
    assert result["optimal_gauge"] == 2.0
    assert result["balanced_left_coupling"] == 2.0
    assert result["balanced_right_coupling"] == 2.0
    assert result["directed_coupling_product"] == 4.0


def test_directed_schur_product():
    result = directed_schur_feedback(2.0, 3.0, 0.1, 0.2)
    assert abs(result["directed_schur_product"] - 0.12) < 1e-12
    assert result["schur_contraction"]


def test_weighted_scalar_balance():
    result = weighted_scalar_gauge_balance(4.0, 1.0, 1.0, 9.0)
    assert abs(result["optimal_gauge"] - 2.0 / 3.0) < 1e-12
    assert abs(result["weighted_left_coupling"] - 6.0) < 1e-12
    assert abs(result["weighted_right_coupling"] - 6.0) < 1e-12
