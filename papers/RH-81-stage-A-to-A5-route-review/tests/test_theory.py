from __future__ import annotations

from route_frontier import all_of, any_of, leaf, minimal_completion_sets


def normalized(formula):
    return {frozenset(item) for item in minimal_completion_sets(formula)}


def test_closed_leaf_needs_nothing() -> None:
    assert normalized(leaf("done", closed=True)) == {frozenset()}


def test_open_leaf_is_singleton() -> None:
    assert normalized(leaf("gate", closed=False)) == {frozenset({"gate"})}


def test_and_or_stage_formula() -> None:
    finite = leaf("finite", closed=True)
    full = leaf("full_block", closed=False)
    rank = leaf("effective_rank", closed=False)
    stage = all_of(finite, any_of(full, rank))
    assert normalized(stage) == {
        frozenset({"full_block"}),
        frozenset({"effective_rank"}),
    }


def test_a5_bundles() -> None:
    stage = any_of(
        leaf("full_block", closed=False),
        leaf("effective_rank", closed=False),
    )
    target = all_of(
        stage,
        leaf("moving_cloud_algebra", closed=True),
        leaf("cloud_projection", closed=False),
        leaf("cloud_coefficients", closed=False),
        leaf("complement_trace_limit", closed=False),
    )
    assert normalized(target) == {
        frozenset({"full_block", "cloud_projection", "cloud_coefficients", "complement_trace_limit"}),
        frozenset({"effective_rank", "cloud_projection", "cloud_coefficients", "complement_trace_limit"}),
    }


def test_superset_pruning() -> None:
    a = leaf("a", closed=False)
    b = leaf("b", closed=False)
    assert normalized(any_of(a, all_of(a, b))) == {frozenset({"a"})}

