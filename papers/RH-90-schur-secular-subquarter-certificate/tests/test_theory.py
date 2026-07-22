from __future__ import annotations

import pytest

from schur_certificate import corrected_contraction_bound, required_gain, schur_trial_form


def test_required_gain() -> None:
    assert required_gain(1.0, 2.0, 0.25) == 0.5
    assert required_gain(0.4, 2.0, 0.25) == 0.0


def test_trial_form() -> None:
    assert schur_trial_form(1.0, 1.0, 0.5) < 0.0
    with pytest.raises(ValueError):
        schur_trial_form(1.0, 1.0, -1.0)


def test_corrected_contraction() -> None:
    assert corrected_contraction_bound(1.0, 0.6, 2.0) >= 0.2
