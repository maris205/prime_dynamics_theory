from __future__ import annotations

from itertools import product

import pytest

from constraint_transducers import (
    ALPHABET,
    Graph,
    Transducer,
    capacity,
    delta_coefficient,
    mobius_prefix,
    one_site,
    safe_transducer,
    simulate,
)
from experiments.build_result import (
    enumerate_small_certificates,
    rh366_graph,
    rh366_q3_switch,
    rh366_transducer,
    rh368_graph,
    rh368_transducer,
)


def _brute_capacity(values: tuple[int, ...], graph: Graph) -> dict[str, int]:
    """Enumerate all open paths, retaining the same start-anywhere contract."""

    scores: list[int] = []

    def extend(index: int, vertex: int, score: int) -> None:
        if index == len(values):
            scores.append(score)
            return
        for successor in graph.vertices:
            if (vertex, successor) in graph.edge_set:
                extend(
                    index + 1,
                    successor,
                    score + values[index] * graph.observable[successor],
                )

    for vertex in graph.vertices:
        extend(1, vertex, values[0] * graph.observable[vertex])
    maximum = max(scores)
    minimum = min(scores)
    return {
        "maximum": maximum,
        "minimum": minimum,
        "capacity": max(abs(maximum), abs(minimum)),
    }


def test_mobius_sieve_prefix_is_exact() -> None:
    assert mobius_prefix(12) == [1, -1, -1, 0, -1, 1, -1, 0, 0, 1, -1, 0]


def test_max_plus_capacity_matches_brute_force() -> None:
    graph = Graph(
        edges=((0, 0), (0, 1), (1, 1), (1, 2), (2, 0), (2, 2)),
        observable=(-2, 1, 0),
    )
    for values in (
        (1,),
        (1, -1),
        (1, -1, 0, 1),
        (-1, 0, 1, -1, 1),
    ):
        assert capacity(values, graph) == _brute_capacity(values, graph)


def test_capacity_rejects_empty_input() -> None:
    graph = Graph(edges=((0, 0),), observable=(1,))
    with pytest.raises(ValueError, match="nonempty"):
        capacity([], graph)


def test_three_frozen_transducers_are_safe_one_site_and_path_valid() -> None:
    instances = (
        (rh366_graph(), rh366_transducer()),
        (rh368_graph(), rh368_transducer()),
        (rh366_graph(), rh366_q3_switch()),
    )
    values = (-1, 0, 1, -1, 1, 0, 1, -1)
    for graph, transducer in instances:
        assert safe_transducer(transducer, graph)
        assert one_site(transducer, graph)
        vertices, _ = simulate(values, transducer, graph)
        assert all(edge in graph.edge_set for edge in zip(vertices, vertices[1:]))


def test_memory_dependent_observable_is_rejected() -> None:
    # The complete two-vertex graph makes safety independent of the label
    # choice; one_site must still reject the state-dependent observable.
    graph = Graph(
        edges=tuple(product((0, 1), repeat=2)),
        observable=(-1, 1),
    )
    transition = (
        ((0, 0, 0),),
        ((1, 1, 1),),
    )
    output = (
        ((0, 0, 0),),
        ((1, 1, 1),),
    )
    transducer = Transducer(1, transition, output)
    assert safe_transducer(transducer, graph)
    assert not one_site(transducer, graph)


def test_small_q2_enumeration_has_frozen_count() -> None:
    audit = enumerate_small_certificates(rh368_graph())
    assert audit == {
        "total_tables": 729,
        "safe_one_site_tables": 16,
        "max_abs_coefficient_of_pi^-2": "4",
    }


def test_known_density_placeholders() -> None:
    assert delta_coefficient(2, 1) == "4/pi^2"
    assert delta_coefficient(2, 0) == "2/pi^2"
    assert delta_coefficient(3, 1) == "9/(4*pi^2)"
    assert delta_coefficient(4, 1) == "2/pi^2"
