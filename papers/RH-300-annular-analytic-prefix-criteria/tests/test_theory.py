import math

from annular_criteria import endpoint_hardy_example, hardy_bound, hinfty_bound


def test_annular_constants():
    ratio = 1.4 / 1.41
    assert math.isclose(hinfty_bound(1.0), ratio**2 / (1.0 - ratio))
    assert math.isclose(
        hardy_bound(1.0), ratio**2 / math.sqrt(1.0 - ratio**2)
    )


def test_bounds_scale_linearly():
    assert math.isclose(hinfty_bound(0.1), 0.1 * hinfty_bound(1.0))
    assert math.isclose(hardy_bound(0.1), 0.1 * hardy_bound(1.0))


def test_endpoint_counterexample():
    h2_small, l1_fixed = endpoint_hardy_example(10_000)
    assert h2_small == 0.01
    assert l1_fixed == 1.0
