#!/usr/bin/env python3
"""Adversarial finite tests for the signed max-cut claims in TPC-293.

No TPC certificate or producer is read.  Every signed graph on 3--6 vertices
is enumerated, every coefficient-sign assignment (modulo global reversal) is
checked, and the all-positive complete-graph formula is tested independently.
The test is deliberately finite and makes no statement about growing prime
shells or the weighted Gram objective.
"""

from __future__ import annotations

import itertools
import sys


class Failure(RuntimeError):
    pass


def need(condition: bool, message: str) -> None:
    if type(condition) is not bool or not condition:
        raise Failure(message)


def edges(m: int) -> list[tuple[int, int]]:
    return [(i, j) for i in range(m) for j in range(i + 1, m)]


def graph_signs(m: int, mask: int) -> list[int]:
    return [1 if (mask >> index) & 1 else -1
            for index in range(len(edges(m)))]


def favorable(m: int, signed_edges: list[int], labels: tuple[int, ...]) -> int:
    return sum(labels[i] * labels[j] * edge == -1
               for edge, (i, j) in zip(signed_edges, edges(m)))


def optimum(m: int, signed_edges: list[int]) -> int:
    return max(favorable(m, signed_edges, (1,) + tail)
               for tail in itertools.product((-1, 1), repeat=m - 1))


def switched(m: int, signed_edges: list[int], switch: tuple[int, ...]
             ) -> list[int]:
    return [edge * switch[i] * switch[j]
            for edge, (i, j) in zip(signed_edges, edges(m))]


def triangle_parity_ok(m: int, signed_edges: list[int]) -> int:
    edge_map = {(i, j): value for value, (i, j) in
                zip(signed_edges, edges(m))}
    checked = 0
    for i, j, k in itertools.combinations(range(m), 3):
        product = (edge_map[(i, j)] * edge_map[(i, k)] *
                   edge_map[(j, k)])
        # A triangle can satisfy all three cancellation equations precisely
        # for odd negative-edge parity.  Check this by direct enumeration.
        actual = any(
            labels[i] * labels[j] * edge_map[(i, j)] == -1 and
            labels[i] * labels[k] * edge_map[(i, k)] == -1 and
            labels[j] * labels[k] * edge_map[(j, k)] == -1
            for labels in itertools.product((-1, 1), repeat=m))
        need(actual == (product == -1), "triangle parity")
        checked += 1
    return checked


def main() -> int:
    graph_cases = 0
    label_cases = 0
    switch_cases = 0
    triangle_cases = 0
    for m in range(3, 7):
        edge_count = len(edges(m))
        for mask in range(1 << edge_count):
            signed = graph_signs(m, mask)
            best = optimum(m, signed)
            need(0 <= best <= edge_count, "max-cut range")
            # Reversing every coefficient sign leaves every edge decision
            # unchanged; fixing label[0]=+1 loses no optimum.
            full_best = max(favorable(
                m, signed, labels)
                for labels in itertools.product((-1, 1), repeat=m))
            need(best == full_best, "global sign quotient")
            need(edge_count - best >= 0, "frustration nonnegative")
            # Switching a signed graph is a relabeling, so its optimum is
            # invariant.  Exercise a deterministic switch on every graph.
            switch = tuple(1 if ((vertex + mask) % 3) else -1
                           for vertex in range(m))
            need(optimum(m, switched(m, signed, switch)) == best,
                 "switching invariance")
            triangle_cases += triangle_parity_ok(m, signed)
            graph_cases += 1
            label_cases += 2 ** (m - 1)
            switch_cases += 1

    # Independent direct checks of the complete-graph max-cut theorem.
    all_positive_cases = 0
    for m in range(3, 13):
        signed = [1] * len(edges(m))
        need(optimum(m, signed) == (m * m) // 4,
             "all-positive complete graph formula")
        all_positive_cases += 1

    need(graph_cases == 33864, "unexpected exhaustive graph count")
    need(all_positive_cases == 10, "theorem stress count")
    print("TPC293_STRESS=PASS graphs={} labels={} switches={} "
          "triangles={} all_positive_m=3..12".format(
              graph_cases, label_cases, switch_cases, triangle_cases))
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except (Failure, ValueError, TypeError) as error:
        print("TPC293_STRESS=FAIL " + str(error), file=sys.stderr)
        raise SystemExit(1)
