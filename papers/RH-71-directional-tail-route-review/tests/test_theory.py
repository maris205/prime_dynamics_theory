import pytest

from route_review import (
    Candidate,
    TerminalBracket,
    common_bridge_frontier,
    first_open_frontier,
    pareto_frontier,
    stacked_energy_upper,
)


def test_bridge_slack_and_stack() -> None:
    bracket = TerminalBracket(finite_lower=2.0, full_upper=2.01)
    assert bracket.bridge_slack(0.01) == pytest.approx(0.01)
    assert bracket.relative_bridge_slack(0.01) == pytest.approx(0.005)
    assert stacked_energy_upper(2.01, 0.01) == pytest.approx(2.02)


def test_common_bridge_preserves_pareto_names() -> None:
    candidates = (
        Candidate("fast", 1.2, (2.0, 1.0)),
        Candidate("sharp", 1.0, (4.0, 1.0)),
        Candidate("dominated", 1.3, (5.0, 2.0)),
    )
    original = {candidate.name for candidate in pareto_frontier(candidates)}
    shifted = {
        candidate.name for candidate in common_bridge_frontier(candidates, 0.3)
    }
    assert original == shifted == {"fast", "sharp"}


def test_first_open_frontier_separates_finite_and_uniform_gates() -> None:
    dependencies = {
        "bridge_instance": ("bridge_theorem", "upstream_interval_triple"),
        "finite_scale": ("terminal_frozen_upper", "bridge_instance"),
        "stage_A1": ("finite_scale", "uniform_family_scaling"),
    }
    closed = {"bridge_theorem", "terminal_frozen_upper"}
    assert first_open_frontier("finite_scale", dependencies, closed) == {
        "upstream_interval_triple"
    }
    assert first_open_frontier("stage_A1", dependencies, closed) == {
        "upstream_interval_triple",
        "uniform_family_scaling",
    }


@pytest.mark.parametrize(
    "call",
    [
        lambda: TerminalBracket(0.0, 1.0),
        lambda: TerminalBracket(1.0, 0.5),
        lambda: stacked_energy_upper(-1.0, 0.0),
        lambda: Candidate("bad", 1.0, (-1.0,)),
    ],
)
def test_invalid_inputs_are_rejected(call) -> None:
    with pytest.raises(ValueError):
        call()
