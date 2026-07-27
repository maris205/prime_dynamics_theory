import numpy as np

from shape_clock import monotone_clock_summary, piecewise_linear_clock


def test_monotone_clock_and_interpolant():
    sigma = np.asarray([0.04, 0.02, 0.01])
    u = np.asarray([0.1, 0.3, 0.6])
    summary = monotone_clock_summary(sigma, u)
    assert summary["strictly_increasing"]
    t = np.log(1.0 / sigma[::-1])[::-1]
    # Explicitly sort t for the interpolation contract.
    t = np.sort(np.log(1.0 / sigma))
    values = u[np.argsort(np.log(1.0 / sigma))]
    assert np.allclose(piecewise_linear_clock(t, values, t), values)
