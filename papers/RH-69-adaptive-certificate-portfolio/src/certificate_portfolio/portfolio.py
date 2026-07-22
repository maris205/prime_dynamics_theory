"""Safe Pareto selection for upper/lower certificate portfolios."""

from __future__ import annotations

from dataclasses import dataclass
import math
from typing import Mapping, Sequence


@dataclass(frozen=True)
class Candidate:
    name: str
    upper: float
    costs: Mapping[str, float]
    evidence: str = "analytic"


@dataclass(frozen=True)
class TriageResult:
    status: str
    selected: Candidate | None
    lower_bound: float | None
    reason: str


def _validate(candidate: Candidate) -> None:
    if not candidate.name:
        raise ValueError("candidate name must be nonempty")
    if not math.isfinite(candidate.upper) or candidate.upper < 0.0:
        raise ValueError("candidate upper must be finite and nonnegative")
    if not candidate.costs:
        raise ValueError("candidate must have at least one cost")
    for key, value in candidate.costs.items():
        if not key or not math.isfinite(float(value)) or float(value) < 0.0:
            raise ValueError("costs must be named finite nonnegative values")


def dominates(left: Candidate, right: Candidate, *, tolerance: float = 1.0e-14) -> bool:
    """Return whether left weakly improves every ledger entry and one strictly."""

    _validate(left)
    _validate(right)
    if set(left.costs) != set(right.costs):
        raise ValueError("candidate cost keys must agree")
    entries_left = [left.upper, *(float(left.costs[key]) for key in sorted(left.costs))]
    entries_right = [right.upper, *(float(right.costs[key]) for key in sorted(right.costs))]
    weak = all(a <= b + tolerance for a, b in zip(entries_left, entries_right, strict=True))
    strict = any(a < b - tolerance for a, b in zip(entries_left, entries_right, strict=True))
    return weak and strict


def pareto_frontier(candidates: Sequence[Candidate]) -> list[Candidate]:
    """Remove safely dominated candidates."""

    values = list(candidates)
    if not values:
        return []
    for candidate in values:
        _validate(candidate)
    keys = set(values[0].costs)
    if any(set(candidate.costs) != keys for candidate in values):
        raise ValueError("all candidates must use the same cost keys")
    frontier = []
    for index, candidate in enumerate(values):
        if not any(
            dominates(other, candidate)
            for other_index, other in enumerate(values)
            if other_index != index
        ):
            frontier.append(candidate)
    return sorted(
        frontier,
        key=lambda item: (
            item.upper,
            *(float(item.costs[key]) for key in sorted(item.costs)),
            item.name,
        ),
    )


def select_feasible(
    candidates: Sequence[Candidate],
    upper_target: float,
    primary_cost: str,
    *,
    budgets: Mapping[str, float] | None = None,
) -> Candidate | None:
    """Select the least-primary-cost candidate meeting all upper budgets."""

    target = float(upper_target)
    if not math.isfinite(target) or target < 0.0:
        raise ValueError("upper target must be finite and nonnegative")
    budget_values = dict(budgets or {})
    feasible = []
    for candidate in pareto_frontier(candidates):
        if primary_cost not in candidate.costs:
            raise ValueError("primary cost is missing")
        if candidate.upper > target:
            continue
        if any(
            key not in candidate.costs
            or float(candidate.costs[key]) > float(value)
            for key, value in budget_values.items()
        ):
            continue
        feasible.append(candidate)
    if not feasible:
        return None
    return min(
        feasible,
        key=lambda item: (
            float(item.costs[primary_cost]),
            item.upper,
            sum(float(value) for value in item.costs.values()),
            item.name,
        ),
    )


def triage(
    candidates: Sequence[Candidate],
    upper_target: float,
    primary_cost: str,
    *,
    budgets: Mapping[str, float] | None = None,
    approximation_lower_bound: float | None = None,
    approximation_target: float | None = None,
) -> TriageResult:
    """Return green, red, or amber without conflating upper and lower claims."""

    selected = select_feasible(
        candidates,
        upper_target,
        primary_cost,
        budgets=budgets,
    )
    if selected is not None:
        return TriageResult(
            status="green",
            selected=selected,
            lower_bound=approximation_lower_bound,
            reason="a valid upper candidate meets every displayed budget",
        )
    if approximation_lower_bound is not None:
        if approximation_target is None:
            raise ValueError("a lower-bound target is required")
        if approximation_lower_bound > approximation_target:
            return TriageResult(
                status="red",
                selected=None,
                lower_bound=float(approximation_lower_bound),
                reason=(
                    "the certified projection lower bound excludes the "
                    "displayed approximation budget"
                ),
            )
    return TriageResult(
        status="amber",
        selected=None,
        lower_bound=approximation_lower_bound,
        reason="no upper closes and no displayed lower bound rules out the class",
    )
