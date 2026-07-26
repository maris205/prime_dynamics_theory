import pytest

from riesz_shells import finite_partial_cloud, rank_change_norm_floor, shell_tail_bound


def test_rank_change_floor():
    assert rank_change_norm_floor(3, 4) == 1.0
    assert rank_change_norm_floor(3, 3) == 0.0


def test_shell_tail():
    result = shell_tail_bound([0.25, 0.125, 0.0625], start=1)
    assert result["tail_upper"] == pytest.approx(0.1875)
    assert result["all_step_transports_stable"]


def test_partial_cloud_rank():
    assert finite_partial_cloud([2, 2, 1])["partial_cloud_rank"] == 5


def test_invalid():
    with pytest.raises(ValueError):
        rank_change_norm_floor(-1, 2)
