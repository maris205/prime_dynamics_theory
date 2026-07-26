import math

import pytest

from mesh_resolvent import circle_covering_radius, sampled_resolvent_envelope, sampled_schur_gate


def test_circle_covering_radius():
    assert circle_covering_radius(2.0, 4) == pytest.approx(4.0 * math.sin(math.pi / 8.0))


def test_uniform_and_local_envelopes():
    uniform = sampled_resolvent_envelope([2.0, 3.0], 0.1)
    assert uniform["mesh_certified"]
    assert uniform["continuous_resolvent_upper"] == pytest.approx(3.0 / 0.7)
    local = sampled_resolvent_envelope([2.0, 3.0], [0.1, 0.05])
    assert local["continuous_resolvent_upper"] == pytest.approx(3.0 / 0.85)


def test_failed_mesh_and_schur_gate():
    assert not sampled_resolvent_envelope([5.0], 0.2)["mesh_certified"]
    result = sampled_schur_gate([1.0] * 8, [2.0] * 8, 0.01, 0.1, 0.1)
    assert result["rank_certified"]


def test_invalid():
    with pytest.raises(ValueError):
        sampled_resolvent_envelope([], 0.1)
