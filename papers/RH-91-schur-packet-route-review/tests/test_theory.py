from __future__ import annotations

import pytest

from route_review import bootstrap_relative_bound, minimal_completion_bundles, updates_for_tolerance


def test_bootstrap_updates() -> None:
    assert updates_for_tolerance(1.0 / 512.0, 0.24, 1e-6) == 20
    assert bootstrap_relative_bound(1.0 / 512.0, 0.24, 20) < 1e-6
    assert bootstrap_relative_bound(1.0 / 512.0, 0.24, 19) > 1e-6


def test_completion_bundles() -> None:
    bundles = minimal_completion_bundles([{"L"}, {"S", "R", "O"}], {"P", "C", "U"})
    assert bundles == [["C", "L", "P", "U"], ["C", "O", "P", "R", "S", "U"]]


def test_invalid_bootstrap() -> None:
    with pytest.raises(ValueError):
        bootstrap_relative_bound(0.0, 1.0, 2)
