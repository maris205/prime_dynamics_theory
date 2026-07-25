import pytest

from mvp_roadmap import antichain, classify_claim, completion_bundles, first_missing_gate, implication_holds


def test_antichain_removes_supersets() -> None:
    result = antichain([
        frozenset({"A"}),
        frozenset({"A", "B"}),
        frozenset({"C"}),
        frozenset({"A"}),
    ])
    assert result == (frozenset({"A"}), frozenset({"C"}))


def test_and_or_completion_frontier() -> None:
    formula = {
        "op": "and",
        "children": [
            {"gate": "F"},
            {"op": "or", "children": [{"gate": "A_native"}, {"gate": "A_lagged"}]},
            {"gate": "B"},
        ],
    }
    statuses = {"F": "proved", "A_native": "conditional", "A_lagged": "open", "B": "open"}
    assert completion_bundles(formula, statuses) == (
        frozenset({"A_lagged", "B"}),
        frozenset({"A_native", "B"}),
    )


def test_no_go_kills_only_its_or_branch() -> None:
    formula = {"op": "or", "children": [{"gate": "bad"}, {"gate": "live"}]}
    assert completion_bundles(formula, {"bad": "no_go", "live": "open"}) == (frozenset({"live"}),)


def test_claim_ladder_and_missing_gate() -> None:
    milestones = {
        "determinant": ["F", "A"],
        "scattering": ["F", "A", "B"],
        "self_adjoint": ["F", "A", "B", "C"],
    }
    assert classify_claim(["F"], milestones) == "foundation"
    assert classify_claim(["F", "A", "B"], milestones) == "scattering"
    assert first_missing_gate(["F", "A"], ["F", "A", "B", "C"]) == "B"
    assert implication_holds(["F", "A", "B"], ["F", "A"])
    assert not implication_holds(["F", "B"], ["F", "A"])


def test_invalid_formula_or_status() -> None:
    with pytest.raises(ValueError):
        completion_bundles({"op": "and", "children": []}, {})
    with pytest.raises(ValueError):
        completion_bundles({"gate": "X"}, {"X": "guessed"})
