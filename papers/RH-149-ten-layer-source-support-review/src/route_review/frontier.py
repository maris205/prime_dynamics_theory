from __future__ import annotations

from collections.abc import Mapping


INTERFACES = ("E-source", "E-update", "E-cocycle")


def missing_interfaces(state: Mapping[str, bool]) -> tuple[str, ...]:
    return tuple(name for name in INTERFACES if not bool(state.get(name, False)))


def composition_closed(state: Mapping[str, bool]) -> bool:
    return not missing_interfaces(state)


def priority_score(tractability: int, falsification_value: int, dependency_leverage: int) -> int:
    values = (tractability, falsification_value, dependency_leverage)
    if any(not isinstance(value, int) or value < 0 or value > 5 for value in values):
        raise ValueError("priority components must be integer scores in [0,5]")
    return sum(values)

