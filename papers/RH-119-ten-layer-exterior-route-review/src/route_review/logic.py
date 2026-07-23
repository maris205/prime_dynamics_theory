"""AND/OR proof-graph closure and minimal missing requirement sets."""

from __future__ import annotations

from collections.abc import Iterable, Mapping, Sequence
from itertools import product


RuleMap = Mapping[str, Sequence[Sequence[str]]]


def proof_closure(proved: Iterable[str], rules: RuleMap) -> set[str]:
    """Return the monotone closure of an AND/OR rule system."""
    reached = set(proved)
    changed = True
    while changed:
        changed = False
        for output, alternatives in rules.items():
            if output in reached:
                continue
            if any(set(inputs) <= reached for inputs in alternatives):
                reached.add(output)
                changed = True
    return reached


def _minimal(sets: set[frozenset[str]]) -> set[frozenset[str]]:
    return {candidate for candidate in sets if not any(other < candidate for other in sets)}


def minimal_missing_sets(target: str, proved: Iterable[str], rules: RuleMap) -> list[frozenset[str]]:
    """Find inclusion-minimal primitive additions making ``target`` reachable."""
    known = set(proved)
    memo: dict[str, set[frozenset[str]]] = {}

    def requirements(node: str, stack: frozenset[str]) -> set[frozenset[str]]:
        if node in known:
            return {frozenset()}
        if node in stack:
            raise ValueError("proof rules must be acyclic")
        if node in memo:
            return memo[node]
        alternatives = rules.get(node)
        if not alternatives:
            result = {frozenset({node})}
        else:
            result: set[frozenset[str]] = set()
            for inputs in alternatives:
                pieces = [requirements(value, stack | {node}) for value in inputs]
                combined = {
                    frozenset().union(*selection)
                    for selection in product(*pieces)
                }
                result.update(combined)
            result = _minimal(result)
        memo[node] = result
        return result

    output = requirements(str(target), frozenset())
    return sorted(output, key=lambda value: (len(value), tuple(sorted(value))))


def each_addition_reaches(
    target: str,
    proved: Iterable[str],
    rules: RuleMap,
    additions: Iterable[str],
) -> dict[str, bool]:
    """Audit whether adding each individual primitive reaches the target."""
    base = set(proved)
    return {
        addition: target in proof_closure(base | {addition}, rules)
        for addition in additions
    }
