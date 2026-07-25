"""Dependency logic for the conditional prime-dynamics MVP roadmap."""

from __future__ import annotations

from collections.abc import Iterable, Mapping


ALLOWED_STATUSES = {"proved", "finite", "conditional", "open", "no_go"}


def antichain(families: Iterable[frozenset[str]]) -> tuple[frozenset[str], ...]:
    """Remove duplicate and nonminimal completion bundles."""

    unique = set(families)
    minimal = [family for family in unique if not any(other < family for other in unique)]
    return tuple(sorted(minimal, key=lambda family: (len(family), tuple(sorted(family)))))


def completion_bundles(formula: Mapping[str, object], statuses: Mapping[str, str]) -> tuple[frozenset[str], ...]:
    """Compute inclusion-minimal open-leaf bundles for an AND/OR formula.

    Proved leaves are free, finite and conditional leaves remain proof debt,
    and no-go leaves kill their branch.
    """

    if "gate" in formula:
        gate = str(formula["gate"])
        status = statuses[gate]
        if status not in ALLOWED_STATUSES:
            raise ValueError(f"unknown status: {status}")
        if status == "proved":
            return (frozenset(),)
        if status == "no_go":
            return ()
        return (frozenset({gate}),)

    operator = str(formula.get("op", ""))
    children = list(formula.get("children", []))
    if operator not in {"and", "or"} or not children:
        raise ValueError("formula nodes require a nonempty AND/OR child list")
    child_bundles = [completion_bundles(child, statuses) for child in children]
    if operator == "or":
        return antichain(bundle for bundles in child_bundles for bundle in bundles)
    product = (frozenset(),)
    for bundles in child_bundles:
        if not bundles:
            return ()
        product = antichain(left | right for left in product for right in bundles)
    return product


def implication_holds(active_gates: Iterable[str], required_gates: Iterable[str]) -> bool:
    return set(required_gates).issubset(set(active_gates))


def first_missing_gate(active_gates: Iterable[str], ordered_gates: Iterable[str]) -> str | None:
    active = set(active_gates)
    return next((gate for gate in ordered_gates if gate not in active), None)


def classify_claim(active_gates: Iterable[str], milestones: Mapping[str, Iterable[str]]) -> str:
    """Return the strongest milestone whose complete gate set is active."""

    active = set(active_gates)
    strongest = "foundation"
    for name, required in milestones.items():
        if set(required).issubset(active):
            strongest = name
    return strongest
