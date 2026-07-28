from head_tail_gluing import determinant_difference_bound, logarithmic_gluing_error


def test_logarithmic_gluing_adds_independent_budgets():
    assert abs(logarithmic_gluing_error(0.1, 0.2, 0.3) - 0.6) < 1e-12
    assert abs(determinant_difference_bound(0.6, 0.0) - 0.6) < 1e-12


def test_exponential_conversion_is_monotone():
    assert determinant_difference_bound(0.1, 1.0) > determinant_difference_bound(0.1, 0.0)
