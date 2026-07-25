#!/usr/bin/env python3
"""Exact finite regression for the TPC-95 native-key identities.

The script uses integer row slopes, primitive positive orbit points,
and integer real weights.  All checked equalities and inequalities are
therefore exact.  This is a finite regression, not an asymptotic
arithmetic proof.
"""

from __future__ import annotations

from collections import defaultdict
from dataclasses import dataclass
from math import gcd
import json


@dataclass(frozen=True)
class Node:
    h: int
    m_left: int
    m_right: int
    j: int
    x: int
    y: int
    content: int
    nu: int
    weight: int


def make_nodes(h: int, row_max: int = 19, orbit_max: int = 11) -> list[Node]:
    nodes: list[Node] = []
    for m_left in range(1, row_max + 1):
        for m_right in range(1, row_max + 1):
            if m_left == m_right or gcd(m_left * m_right, h) != 1:
                continue
            for j in range(1, orbit_max + 1):
                if gcd(j, h) != 1:
                    continue
                x = m_left * j + h
                y = m_right * j + h
                content = gcd(x, y)
                difference = m_left - m_right
                assert difference % content == 0
                nu = difference // content
                raw_weight = (3 * m_left + 5 * m_right + 7 * j + h) % 11 - 5
                weight = raw_weight if raw_weight else 1
                nodes.append(
                    Node(
                        h=h,
                        m_left=m_left,
                        m_right=m_right,
                        j=j,
                        x=x,
                        y=y,
                        content=content,
                        nu=nu,
                        weight=weight,
                    )
                )
    return nodes


def group_stats(nodes: list[Node], side: str) -> dict[tuple[int, int], tuple[int, int, int]]:
    weights: dict[tuple[int, int], list[int]] = defaultdict(list)
    for node in nodes:
        target = node.x if side == "L" else node.y
        weights[(node.nu, target)].append(node.weight)
    return {
        key: (len(values), sum(values), sum(value * value for value in values))
        for key, values in weights.items()
    }


def run_packet(h: int) -> dict[str, int]:
    nodes = make_nodes(h)

    composite: dict[tuple[int, int, int], Node] = {}
    for node in nodes:
        key = (node.nu, node.x, node.y)
        # The archive is already at canonical-parent level: repeated records
        # are provenance failures even when all displayed fields agree.
        assert key not in composite
        composite[key] = node
        assert node.x != node.y

    left = group_stats(nodes, "L")
    right = group_stats(nodes, "R")

    c_ll = sum(total * total - energy for _, total, energy in left.values())
    c_rr = sum(total * total - energy for _, total, energy in right.values())
    common_keys = set(left) | set(right)
    c_lr = 2 * sum(
        left.get(key, (0, 0, 0))[1] * right.get(key, (0, 0, 0))[1]
        for key in common_keys
    )
    compressed_target = c_ll + c_rr + c_lr

    neighbors: list[set[int]] = [set() for _ in nodes]
    explicit_target = 0
    shared_edges = 0
    for index, node in enumerate(nodes):
        for other_index in range(index + 1, len(nodes)):
            other = nodes[other_index]
            if node.nu != other.nu:
                continue
            equalities = (
                int(node.x == other.x)
                + int(node.x == other.y)
                + int(node.y == other.x)
                + int(node.y == other.y)
            )
            assert equalities <= 1
            if equalities:
                neighbors[index].add(other_index)
                neighbors[other_index].add(index)
                explicit_target += 2 * node.weight * other.weight
                shared_edges += 1
    assert compressed_target == explicit_target

    for index, node in enumerate(nodes):
        degree_formula = (
            left.get((node.nu, node.x), (0, 0, 0))[0]
            + right.get((node.nu, node.x), (0, 0, 0))[0]
            + left.get((node.nu, node.y), (0, 0, 0))[0]
            + right.get((node.nu, node.y), (0, 0, 0))[0]
            - 2
        )
        assert degree_formula == len(neighbors[index])

    fiber_weights: dict[int, list[int]] = defaultdict(list)
    for node in nodes:
        fiber_weights[node.nu].append(node.weight)

    determinant_energy = 0
    dominance_energy = 0
    triplet_energy = 0
    for values in fiber_weights.values():
        determinant_energy += sum(values) ** 2
        raw_mass = sum(abs(value) for value in values)
        largest = max(abs(value) for value in values)
        defect = max(2 * largest - raw_mass, 0)
        dominance_energy += defect * defect
        triplet_energy += sum(value * value for value in values)

    assert determinant_energy >= dominance_energy
    equal_coherence = determinant_energy - triplet_energy
    max_degree = max((len(group) for group in neighbors), default=0)
    assert abs(explicit_target) <= max_degree * triplet_energy

    return {
        "h": h,
        "nodes": len(nodes),
        "fibers": len(fiber_weights),
        "composite_keys": len(composite),
        "shared_target_edges": shared_edges,
        "max_target_degree": max_degree,
        "triplet_energy": triplet_energy,
        "determinant_energy": determinant_energy,
        "dominance_energy": dominance_energy,
        "equal_coherence": equal_coherence,
        "compressed_target_coherence": compressed_target,
    }


def main() -> None:
    summaries = [run_packet(h) for h in (1, 2, 3, 5, 6)]
    output = {
        "description": (
            "Exact finite regression for canonical composite uniqueness, "
            "single shared-target rigidity, compressed target coherence, "
            "exact degrees, and dominance energy; not an asymptotic theorem"
        ),
        "all_checks_passed": True,
        "packets": summaries,
    }
    print(json.dumps(output, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
