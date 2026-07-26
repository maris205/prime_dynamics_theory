import math

import pytest

from riesz_transport import projector_step_bound, transport_chain


def test_step_bound():
    result = projector_step_bound(2.0 * math.pi, 2.0, 3.0, 0.01)
    assert result["projector_step_upper"] == pytest.approx(0.06)
    assert result["stable_range_transport"]


def test_failed_transport():
    result = projector_step_bound(2.0 * math.pi, 10.0, 10.0, 0.02)
    assert not result["stable_range_transport"]


def test_chain():
    result = transport_chain([0.2, 0.1, 0.05])
    assert result["all_local_transports_stable"]
    assert result["telescoping_upper"] == pytest.approx(0.35)


def test_invalid():
    with pytest.raises(ValueError):
        projector_step_bound(1.0, 1.0, 1.0, -1.0)
