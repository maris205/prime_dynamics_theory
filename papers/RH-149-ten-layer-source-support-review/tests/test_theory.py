from __future__ import annotations

import itertools

import pytest

from route_review import composition_closed, missing_interfaces, priority_score


def test_only_all_three_interfaces_close_composition() -> None:
    closed = 0
    for values in itertools.product((False, True), repeat=3):
        state = dict(zip(("E-source", "E-update", "E-cocycle"), values))
        closed += composition_closed(state)
    assert closed == 1


def test_each_interface_is_individually_necessary() -> None:
    for omitted in ("E-source", "E-update", "E-cocycle"):
        state = {name: name != omitted for name in ("E-source", "E-update", "E-cocycle")}
        assert not composition_closed(state)
        assert missing_interfaces(state) == (omitted,)


def test_priority_score() -> None:
    assert priority_score(5, 5, 5) == 15
    with pytest.raises(ValueError):
        priority_score(6, 1, 1)

