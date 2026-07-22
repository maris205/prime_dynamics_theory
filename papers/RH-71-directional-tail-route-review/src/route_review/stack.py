"""Composable certificate stacks and open dependency frontiers."""

from __future__ import annotations

from dataclasses import dataclass
from functools import lru_cache
from typing import Mapping, Sequence


@dataclass(frozen=True)
class TerminalBracket:
    """A certified finite-prefix lower and full frozen upper."""

    finite_lower: float
    full_upper: float

    def __post_init__(self) -> None:
        if self.finite_lower <= 0.0:
            raise ValueError("finite lower must be positive")
        if self.full_upper < self.finite_lower:
            raise ValueError("full upper cannot be below the finite lower")

    def bridge_slack(self, relative_tolerance: float) -> float:
        """Sufficient upstream H2-difference budget for a relative target."""

        tolerance = float(relative_tolerance)
        if tolerance < 0.0:
            raise ValueError("relative tolerance must be nonnegative")
        return (1.0 + tolerance) * self.finite_lower - self.full_upper

    def relative_bridge_slack(self, relative_tolerance: float) -> float:
        return self.bridge_slack(relative_tolerance) / self.finite_lower


@dataclass(frozen=True)
class Candidate:
    """One terminal upper with a coordinatewise nonnegative cost vector."""

    name: str
    upper: float
    costs: tuple[float, ...]

    def __post_init__(self) -> None:
        if self.upper < 0.0:
            raise ValueError("upper must be nonnegative")
        if any(cost < 0.0 for cost in self.costs):
            raise ValueError("costs must be nonnegative")


def stacked_energy_upper(frozen_upper: float, bridge_upper: float) -> float:
    """Compose a frozen H2 upper and an H2 transfer-difference upper."""

    frozen = float(frozen_upper)
    bridge = float(bridge_upper)
    if frozen < 0.0 or bridge < 0.0:
        raise ValueError("certificate uppers must be nonnegative")
    return frozen + bridge


def _dominates(left: Candidate, right: Candidate) -> bool:
    if len(left.costs) != len(right.costs):
        raise ValueError("candidate cost dimensions differ")
    weak = left.upper <= right.upper and all(
        a <= b for a, b in zip(left.costs, right.costs, strict=True)
    )
    strict = left.upper < right.upper or any(
        a < b for a, b in zip(left.costs, right.costs, strict=True)
    )
    return weak and strict


def pareto_frontier(candidates: Sequence[Candidate]) -> tuple[Candidate, ...]:
    """Return candidates not dominated in upper-and-cost coordinates."""

    values = tuple(candidates)
    return tuple(
        candidate
        for index, candidate in enumerate(values)
        if not any(
            _dominates(other, candidate)
            for other_index, other in enumerate(values)
            if other_index != index
        )
    )


def common_bridge_frontier(
    candidates: Sequence[Candidate], bridge_upper: float
) -> tuple[Candidate, ...]:
    """Add one common bridge upper; the Pareto names must be unchanged."""

    bridge = float(bridge_upper)
    if bridge < 0.0:
        raise ValueError("bridge upper must be nonnegative")
    shifted = tuple(
        Candidate(candidate.name, candidate.upper + bridge, candidate.costs)
        for candidate in candidates
    )
    return pareto_frontier(shifted)


def first_open_frontier(
    target: str,
    dependencies: Mapping[str, Sequence[str]],
    closed: set[str] | frozenset[str],
) -> frozenset[str]:
    """Return the first unresolved prerequisite antichain for one target.

    A node closes monotonically once all of its prerequisites are closed.
    If a nonclosed node has no unresolved prerequisite, that node itself is
    the current frontier. Cycles are rejected.
    """

    closed_nodes = frozenset(closed)
    visiting: set[str] = set()

    @lru_cache(maxsize=None)
    def visit(node: str) -> frozenset[str]:
        if node in closed_nodes:
            return frozenset()
        if node in visiting:
            raise ValueError("dependency graph contains a cycle")
        visiting.add(node)
        prerequisites = tuple(dependencies.get(node, ()))
        unresolved: set[str] = set()
        for prerequisite in prerequisites:
            unresolved.update(visit(prerequisite))
        visiting.remove(node)
        if unresolved:
            return frozenset(unresolved)
        return frozenset((node,))

    return visit(str(target))
