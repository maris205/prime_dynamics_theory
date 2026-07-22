"""Status-aware minimal completion bundles for monotone route formulas."""

from __future__ import annotations

from itertools import product
from typing import Iterable


def prune_antichain(bundles: Iterable[frozenset[str]]) -> tuple[frozenset[str], ...]:
    unique = sorted(set(bundles), key=lambda item: (len(item), tuple(sorted(item))))
    kept = []
    for bundle in unique:
        if not any(existing <= bundle for existing in kept):
            kept.append(bundle)
    return tuple(kept)


def minimal_completion_bundles(node: dict[str, object]) -> tuple[frozenset[str], ...]:
    kind = str(node["kind"])
    if kind == "leaf":
        status = str(node["status"])
        if status == "closed":
            return (frozenset(),)
        if status == "open":
            return (frozenset({str(node["name"])}),)
        if status == "red":
            return tuple()
        raise ValueError(f"unknown leaf status: {status}")
    children = [minimal_completion_bundles(child) for child in node["children"]]
    if kind == "or":
        return prune_antichain(bundle for family in children for bundle in family)
    if kind == "and":
        if any(not family for family in children):
            return tuple()
        return prune_antichain(frozenset().union(*choice) for choice in product(*children))
    raise ValueError(f"unknown node kind: {kind}")
