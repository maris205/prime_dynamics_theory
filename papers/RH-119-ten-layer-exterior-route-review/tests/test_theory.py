from __future__ import annotations

import pytest

from route_review import each_addition_reaches, minimal_missing_sets, proof_closure


def test_and_or_closure() -> None:
    rules = {"target": [("a", "b"), ("c",)]}
    assert "target" not in proof_closure({"a"}, rules)
    assert "target" in proof_closure({"a", "b"}, rules)
    assert "target" in proof_closure({"c"}, rules)


def test_minimal_missing_sets_form_antichain() -> None:
    rules = {
        "target": [("theorem", "p1"), ("theorem", "p2"), ("theorem", "p3")],
        "validated": [("target", "outward")],
    }
    missing = minimal_missing_sets("target", {"theorem"}, rules)
    assert missing == [frozenset({"p1"}), frozenset({"p2"}), frozenset({"p3"})]
    validated = minimal_missing_sets("validated", {"theorem"}, rules)
    assert set(validated) == {
        frozenset({"outward", "p1"}),
        frozenset({"outward", "p2"}),
        frozenset({"outward", "p3"}),
    }


def test_each_packet_completes_conditional_graph() -> None:
    rules = {"target": [("theorem", "p1"), ("theorem", "p2")]}
    assert each_addition_reaches("target", {"theorem"}, rules, ["p1", "p2"]) == {"p1": True, "p2": True}


def test_cycle_is_rejected() -> None:
    rules = {"a": [("b",)], "b": [("a",)]}
    with pytest.raises(ValueError):
        minimal_missing_sets("a", set(), rules)
