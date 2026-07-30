import math

from block_clock import critical_slope, decay_exponent, root_rate_limit, saturation_lower


def test_critical_slope_and_root_rate_boundary():
    critical = critical_slope(1.0, 0.5, 1.4)
    assert math.isclose(critical, 1.0 / math.log(10.0 / 7.0))
    assert math.isclose(root_rate_limit(1.0, critical, 0.5, 1.4), 1.0)
    assert decay_exponent(1.0, 4.0, 0.5, 1.4) > 0.0


def test_subcritical_saturation_grows():
    coarse = saturation_lower(1e-4, 1.0, 2.0, 0.5, 1.4)
    fine = saturation_lower(1e-8, 1.0, 2.0, 0.5, 1.4)
    assert fine > coarse > 0.0
