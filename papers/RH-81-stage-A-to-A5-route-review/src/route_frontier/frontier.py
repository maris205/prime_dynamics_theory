"""Compute minimal open-gate bundles in a monotone dependency formula."""

from __future__ import annotations

from dataclasses import dataclass
from itertools import product
from typing import Iterable


@dataclass(frozen=True)
class Formula:
    kind: str
    name: str | None = None
    closed: bool = False
    children: tuple["Formula", ...] = ()


def leaf(name: str, *, closed: bool) -> Formula:
    if not name:
        raise ValueError("leaf name must be nonempty")
    return Formula(kind="leaf", name=name, closed=bool(closed))


def all_of(*children: Formula) -> Formula:
    if not children:
        raise ValueError("all_of requires at least one child")
    return Formula(kind="all", children=tuple(children))


def any_of(*children: Formula) -> Formula:
    if not children:
        raise ValueError("any_of requires at least one child")
    return Formula(kind="any", children=tuple(children))


def _minimal(family: Iterable[frozenset[str]]) -> tuple[frozenset[str], ...]:
    unique = sorted(set(family), key=lambda item: (len(item), sorted(item)))
    kept: list[frozenset[str]] = []
    for candidate in unique:
        if not any(existing <= candidate for existing in kept):
            kept.append(candidate)
    return tuple(kept)


def minimal_completion_sets(formula: Formula) -> tuple[frozenset[str], ...]:
    """Return inclusion-minimal open leaves whose closure makes formula true."""
    if formula.kind == "leaf":
        if formula.name is None:
            raise ValueError("leaf missing name")
        return (frozenset(),) if formula.closed else (frozenset({formula.name}),)
    child_families = [minimal_completion_sets(child) for child in formula.children]
    if formula.kind == "any":
        return _minimal(item for family in child_families for item in family)
    if formula.kind == "all":
        unions = (
            frozenset().union(*choice)
            for choice in product(*child_families)
        )
        return _minimal(unions)
    raise ValueError(f"unknown formula kind: {formula.kind}")

