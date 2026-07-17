"""Exact rational bookkeeping for adaptive contour-atlas gaps."""

from __future__ import annotations

from dataclasses import dataclass
from fractions import Fraction
import math
from typing import Iterable, Mapping


@dataclass(frozen=True)
class CircularGapComponent:
    """One connected unresolved component in unwrapped turn coordinates."""

    start_turn: Fraction
    end_turn: Fraction
    leaf_count: int
    parent_arcs: tuple[int, ...]

    @property
    def length_turns(self) -> Fraction:
        return self.end_turn - self.start_turn

    @property
    def midpoint_turn(self) -> Fraction:
        return ((self.start_turn + self.end_turn) / 2) % 1


def _interval(record: Mapping[str, object]) -> tuple[Fraction, Fraction, int]:
    denominator = int(record["turn_denominator"])
    start = Fraction(int(record["start_numerator"]), denominator)
    end = Fraction(int(record["end_numerator"]), denominator)
    if not (Fraction(0) <= start < end <= Fraction(1)):
        raise ValueError("refined contour leaves must lie in one normalized turn")
    return start, end, int(record["parent_arc"])


def merge_circular_gap_components(
    records: Iterable[Mapping[str, object]],
) -> list[CircularGapComponent]:
    """Merge exactly adjacent rational leaves, including the turn seam."""

    intervals = sorted((_interval(record) for record in records), key=lambda row: row[0])
    if not intervals:
        return []
    groups: list[dict[str, object]] = []
    for start, end, parent in intervals:
        if groups and start == groups[-1]["end"]:
            groups[-1]["end"] = end
            groups[-1]["leaf_count"] = int(groups[-1]["leaf_count"]) + 1
            groups[-1]["parents"].add(parent)
        else:
            groups.append(
                {
                    "start": start,
                    "end": end,
                    "leaf_count": 1,
                    "parents": {parent},
                }
            )
    if (
        len(groups) > 1
        and groups[0]["start"] == 0
        and groups[-1]["end"] == 1
    ):
        seam = {
            "start": groups[-1]["start"],
            "end": Fraction(1) + groups[0]["end"],
            "leaf_count": int(groups[-1]["leaf_count"])
            + int(groups[0]["leaf_count"]),
            "parents": set(groups[-1]["parents"]) | set(groups[0]["parents"]),
        }
        groups = [seam, *groups[1:-1]]
    components = [
        CircularGapComponent(
            start_turn=group["start"],
            end_turn=group["end"],
            leaf_count=int(group["leaf_count"]),
            parent_arcs=tuple(sorted(int(value) for value in group["parents"])),
        )
        for group in groups
    ]
    return sorted(components, key=lambda component: float(component.midpoint_turn))


def turn_center_id(turn: Fraction) -> str:
    """Return a deterministic filename-safe identifier for a rational turn."""

    reduced = Fraction(turn) % 1
    return f"turn_{reduced.numerator:08d}_of_{reduced.denominator:08d}"


def contour_point(center: complex, radius: float, turn: Fraction) -> complex:
    """Evaluate a rational turn on a stored floating circular contour."""

    angle = 2.0 * math.pi * float(Fraction(turn) % 1)
    return complex(center) + float(radius) * complex(math.cos(angle), math.sin(angle))
