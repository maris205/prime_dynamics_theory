from __future__ import annotations

from hundred_layer_review import minimal_completion_bundles, prune_antichain


def leaf(name: str, status: str): return {"kind": "leaf", "name": name, "status": status}


def test_minimal_bundles() -> None:
    formula = {"kind": "and", "children": [leaf("closed", "closed"), {"kind": "or", "children": [leaf("a", "open"), {"kind": "and", "children": [leaf("b", "open"), leaf("c", "open")]}]}]}
    bundles = minimal_completion_bundles(formula)
    assert frozenset({"a"}) in bundles
    assert frozenset({"b", "c"}) in bundles


def test_red_branch_and_antichain() -> None:
    formula = {"kind": "or", "children": [leaf("dead", "red"), leaf("live", "open")]}
    assert minimal_completion_bundles(formula) == (frozenset({"live"}),)
    assert prune_antichain([frozenset({"a"}), frozenset({"a", "b"})]) == (frozenset({"a"}),)
