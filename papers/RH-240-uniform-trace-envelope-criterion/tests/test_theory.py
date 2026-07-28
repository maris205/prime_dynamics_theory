import numpy as np

from trace_envelope import finite_log_majorant, geometric_log_bound, observed_unit_amplitude_rate


def test_geometric_log_bound_dominates_finite_sum():
    orders = np.arange(2, 20)
    moments = 0.4**orders
    finite = finite_log_majorant(orders, moments)
    assert finite <= geometric_log_bound(1.0, 0.4, 1.0)
    assert abs(observed_unit_amplitude_rate(orders, moments) - 0.4) < 1e-14
