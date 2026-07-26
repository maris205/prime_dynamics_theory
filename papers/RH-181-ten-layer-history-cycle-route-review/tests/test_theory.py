import pytest

from history_cycle_frontier import current_frontiers, route_status


def current_statuses():
    return {
        "memory_to_history": "proved",
        "history_to_transfer": "open",
        "cycle_algebra": "proved",
        "cycle_calibration": "open",
        "cycle_to_transfer": "open",
        "physical_data": "open",
        "uniform_margins": "open",
        "shell_transport": "open",
    }


def test_two_open_branch_frontiers():
    statuses = current_statuses()
    frontiers = dict(current_frontiers(statuses))
    assert frontiers["reset_history"] == frozenset({"history_to_transfer", "physical_data", "uniform_margins", "shell_transport"})
    assert frontiers["finite_cycle"] == frozenset({"cycle_calibration", "cycle_to_transfer", "physical_data", "uniform_margins", "shell_transport"})
    assert route_status(statuses) == "open"


def test_rejected_reset_branch_leaves_cycle_branch():
    statuses = current_statuses()
    statuses["history_to_transfer"] = "no_go"
    assert [name for name, _ in current_frontiers(statuses)] == ["finite_cycle"]


def test_invalid_leaf_status():
    statuses = current_statuses()
    statuses["physical_data"] = "maybe"
    with pytest.raises(ValueError):
        current_frontiers(statuses)
