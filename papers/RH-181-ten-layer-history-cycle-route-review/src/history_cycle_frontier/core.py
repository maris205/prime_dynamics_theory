"""Architecture-relative AND/OR frontier calculations."""

from __future__ import annotations


BRANCHES = {
    "reset_history": (
        "memory_to_history",
        "history_to_transfer",
        "physical_data",
        "uniform_margins",
        "shell_transport",
    ),
    "finite_cycle": (
        "cycle_algebra",
        "cycle_calibration",
        "cycle_to_transfer",
        "physical_data",
        "uniform_margins",
        "shell_transport",
    ),
}


def _validate(statuses: dict[str, str]) -> None:
    required = {leaf for branch in BRANCHES.values() for leaf in branch}
    if set(statuses) != required:
        raise ValueError("statuses must contain exactly the route leaves")
    if any(value not in {"proved", "open", "no_go"} for value in statuses.values()):
        raise ValueError("leaf status must be proved, open, or no_go")


def current_frontiers(statuses: dict[str, str]) -> tuple[tuple[str, frozenset[str]], ...]:
    _validate(statuses)
    frontiers = []
    for name, leaves in BRANCHES.items():
        if any(statuses[leaf] == "no_go" for leaf in leaves):
            continue
        missing = frozenset(leaf for leaf in leaves if statuses[leaf] != "proved")
        frontiers.append((name, missing))
    return tuple(frontiers)


def route_status(statuses: dict[str, str]) -> str:
    frontiers = current_frontiers(statuses)
    if any(not missing for _, missing in frontiers):
        return "proved"
    if frontiers:
        return "open"
    return "all_branches_rejected"
