"""Monotone four-leaf dependency logic for RH-171."""

from __future__ import annotations

from collections.abc import Mapping


LEAVES = ("X_phys", "D_phys", "K_phys", "H_phys")
ALLOWED = {"proved", "conditional", "finite", "open", "no_go"}


def physical_r_frontier(statuses: Mapping[str, str]) -> tuple[frozenset[str], ...]:
    missing: set[str] = set()
    for leaf in LEAVES:
        status = statuses[leaf]
        if status not in ALLOWED:
            raise ValueError(f"unknown status for {leaf}: {status}")
        if status == "no_go":
            return ()
        if status != "proved":
            missing.add(leaf)
    return (frozenset(missing),)


def physical_r_status(statuses: Mapping[str, str]) -> str:
    frontier = physical_r_frontier(statuses)
    if not frontier:
        return "branch_rejected"
    if frontier == (frozenset(),):
        return "proved"
    return "open"
