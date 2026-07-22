import pytest

from certificate_portfolio import (
    Candidate,
    dominates,
    pareto_frontier,
    select_feasible,
    triage,
)


def candidates():
    return [
        Candidate("fast_loose", 1.2, {"horizon": 8.0}),
        Candidate("middle", 1.01, {"horizon": 16.0}),
        Candidate("slow_tight", 1.001, {"horizon": 32.0}),
        Candidate("dominated", 1.3, {"horizon": 40.0}),
    ]


def test_pareto_pruning_removes_only_dominated_candidate() -> None:
    frontier = pareto_frontier(candidates())
    assert {candidate.name for candidate in frontier} == {
        "fast_loose",
        "middle",
        "slow_tight",
    }
    assert dominates(candidates()[0], candidates()[3])


def test_selector_finds_least_cost_feasible_upper() -> None:
    selected = select_feasible(candidates(), 1.02, "horizon")
    assert selected is not None
    assert selected.name == "middle"


def test_triage_green_red_and_amber() -> None:
    green = triage(candidates(), 1.02, "horizon")
    assert green.status == "green"
    red = triage(
        [Candidate("miss", 1.0, {"depth": 8.0})],
        0.1,
        "depth",
        approximation_lower_bound=0.9,
        approximation_target=0.1,
    )
    assert red.status == "red"
    amber = triage(
        [Candidate("miss", 1.0, {"depth": 8.0})],
        0.1,
        "depth",
    )
    assert amber.status == "amber"


@pytest.mark.parametrize(
    "call",
    [
        lambda: pareto_frontier(
            [Candidate("x", -1.0, {"cost": 1.0})]
        ),
        lambda: dominates(
            Candidate("x", 1.0, {"a": 1.0}),
            Candidate("y", 1.0, {"b": 1.0}),
        ),
        lambda: select_feasible(candidates(), -1.0, "horizon"),
        lambda: triage(
            [],
            1.0,
            "cost",
            approximation_lower_bound=1.0,
        ),
    ],
)
def test_invalid_inputs_are_rejected(call) -> None:
    with pytest.raises(ValueError):
        call()
