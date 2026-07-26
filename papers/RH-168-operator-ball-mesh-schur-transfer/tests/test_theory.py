import pytest

from operator_ball_transfer import inverse_defect_bound, robust_resolvent_envelope, robust_schur_gate


def test_inverse_defect_bound():
    assert inverse_defect_bound(2.0, 0.2)["exact_inverse_upper"] == pytest.approx(2.5)
    assert not inverse_defect_bound(2.0, 1.0)["inverse_certified"]


def test_joint_mesh_operator_radius():
    result = robust_resolvent_envelope([2.0, 3.0], 0.05, 0.02)
    assert result["transfer_certified"]
    assert result["exact_continuous_resolvent_upper"] == pytest.approx(3.0 / 0.79)


def test_robust_schur_gate():
    result = robust_schur_gate([1.0] * 8, [1.5] * 8, 0.01, 0.01, 0.01, 0.1, 0.2, 0.02)
    assert result["rank_certified"]
    assert result["complement_to_packet_upper"] == pytest.approx(0.12)


def test_failed_transfer_and_invalid():
    assert not robust_resolvent_envelope([5.0], 0.1, 0.1)["transfer_certified"]
    with pytest.raises(ValueError):
        inverse_defect_bound(-1.0, 0.0)
