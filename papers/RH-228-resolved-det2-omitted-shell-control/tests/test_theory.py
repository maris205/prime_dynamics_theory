import numpy as np

from det2_tail import det2_log, det2_log_tail_bound


def test_regularized_log_starts_at_second_order():
    values = np.asarray([0.2, -0.1])
    z = 1e-5
    assert abs(det2_log(values, z)) < 1e-10


def test_log_tail_bound():
    values = np.asarray([0.2 + 0.1j, 0.2 - 0.1j, -0.1])
    bound = det2_log_tail_bound(values, 1.0)["log_tail_upper"]
    for angle in np.linspace(0.0, 2.0 * np.pi, 24, endpoint=False):
        assert abs(det2_log(values, np.exp(1j * angle))) <= bound + 1e-14
