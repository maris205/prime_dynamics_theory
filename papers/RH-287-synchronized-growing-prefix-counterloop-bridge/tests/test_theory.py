from prefix_bridge import admissible_level, prefix_weight_upper


def test_admissible_level_grows_for_smaller_errors():
    coarse = admissible_level([1e-2 * n**2 for n in range(2, 60)])
    fine = admissible_level([1e-5 * n**2 for n in range(2, 60)])
    assert fine > coarse


def test_unweighted_error_can_have_large_weighted_cost():
    short = prefix_weight_upper(1e-3, 5, 1.4)
    long = prefix_weight_upper(1e-3, 30, 1.4)
    assert long > short > 0.0
