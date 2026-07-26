import pytest

from midgap_contour import centered_circle_certificate


def test_midgap_formula():
    result = centered_circle_certificate(1.0, 5.0, 0.5, 0.5)
    assert result["midpoint_radius"] == 3.0
    assert result["feedback_product"] == pytest.approx(0.0625)
    assert result["rank_certified"]


def test_sharp_gap_contact():
    result = centered_circle_certificate(1.0, 3.0, 1.0, 1.0)
    assert result["feedback_product"] == 1.0
    assert not result["rank_certified"]


def test_imbalanced_couplings_use_product():
    result = centered_circle_certificate(0.0, 4.0, 100.0, 0.01)
    assert result["rank_certified"]
    assert result["feedback_product"] == pytest.approx(0.25)


def test_invalid():
    with pytest.raises(ValueError):
        centered_circle_certificate(2.0, 1.0, 0.1, 0.1)
