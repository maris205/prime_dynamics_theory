import math

from spectral_tail import logarithmic_tail_bound, root_rate_limit, trace_power_bound


def test_certified_root_rate_is_strict():
    assert root_rate_limit() == 0.7 * math.exp(0.25)
    assert root_rate_limit() < 1.0


def test_tail_bound_decays_and_trace_envelope_is_geometric():
    values = [logarithmic_tail_bound(s) for s in (1e-2, 1e-4, 1e-8)]
    assert values[0] > values[1] > values[2] > 0.0
    sigma = 1e-3
    assert trace_power_bound(5, sigma) == 0.5 * trace_power_bound(4, sigma)
