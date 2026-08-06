"""Finite constraint-graph dynamic programming and safe transducers.

The implementation is deliberately integer-only.  The asymptotic theorem in
the manuscript supplies the squarefree-density constants; this module checks
the finite graph and transducer contracts exactly.
"""

from __future__ import annotations

from dataclasses import dataclass
from itertools import product
from typing import Iterable

ALPHABET: tuple[int, ...] = (-1, 0, 1)
_SYMBOL_INDEX = {value: index for index, value in enumerate(ALPHABET)}


@dataclass(frozen=True)
class Graph:
    """A finite directed graph with an integer vertex observable."""

    edges: tuple[tuple[int, int], ...]
    observable: tuple[int, ...]

    def __post_init__(self) -> None:
        size = len(self.observable)
        if size == 0:
            raise ValueError("a graph needs at least one vertex")
        if any(u < 0 or v < 0 or u >= size or v >= size for u, v in self.edges):
            raise ValueError("edge endpoint outside the vertex set")
        if not self.edges:
            raise ValueError("a graph needs at least one edge")

    @property
    def vertices(self) -> tuple[int, ...]:
        return tuple(range(len(self.observable)))

    @property
    def incoming(self) -> tuple[tuple[int, ...], ...]:
        rows: list[list[int]] = [[] for _ in self.vertices]
        for u, v in self.edges:
            rows[v].append(u)
        return tuple(tuple(row) for row in rows)

    @property
    def edge_set(self) -> frozenset[tuple[int, int]]:
        return frozenset(self.edges)


@dataclass(frozen=True)
class Transducer:
    """A q-clock deterministic finite-memory output transducer.

    ``transition[s][r][a]`` is the next internal state and
    ``output[s][r][a]`` is a graph vertex.  Residues are represented by
    ``n mod q`` for the one-indexed arithmetic input.
    """

    q: int
    transition: tuple[tuple[tuple[int, ...], ...], ...]
    output: tuple[tuple[tuple[int, ...], ...], ...]
    initial_state: int = 0

    def __post_init__(self) -> None:
        if self.q < 1:
            raise ValueError("q must be positive")
        if len(self.transition) == 0 or len(self.transition) != len(self.output):
            raise ValueError("transition/output state dimensions disagree")
        states = len(self.transition)
        for table in (self.transition, self.output):
            if any(len(row) != self.q for row in table):
                raise ValueError("clock dimension mismatch")
            if any(len(cell) != len(ALPHABET) for row in table for cell in row):
                raise ValueError("alphabet dimension mismatch")
        if not 0 <= self.initial_state < states:
            raise ValueError("invalid initial state")
        if any(
            next_state < 0 or next_state >= states
            for row in self.transition
            for cell in row
            for next_state in cell
        ):
            raise ValueError("transition points outside state set")

    @property
    def state_count(self) -> int:
        return len(self.transition)

    def next_state(self, state: int, residue: int, symbol: int) -> int:
        return self.transition[state][residue % self.q][_SYMBOL_INDEX[symbol]]

    def vertex(self, state: int, residue: int, symbol: int) -> int:
        return self.output[state][residue % self.q][_SYMBOL_INDEX[symbol]]


def mobius_prefix(limit: int) -> list[int]:
    """Return ``[mu(1), ..., mu(limit)]`` by a linear sieve."""

    if limit < 0:
        raise ValueError("limit must be nonnegative")
    mu = [0] * (limit + 1)
    composite = [False] * (limit + 1)
    primes: list[int] = []
    if limit >= 1:
        mu[1] = 1
    for n in range(2, limit + 1):
        if not composite[n]:
            primes.append(n)
            mu[n] = -1
        for prime in primes:
            multiple = n * prime
            if multiple > limit:
                break
            composite[multiple] = True
            if n % prime == 0:
                mu[multiple] = 0
                break
            mu[multiple] = -mu[n]
    return mu[1:]


def capacity(values: Iterable[int], graph: Graph) -> dict[str, object]:
    """Compute open-path max/min scores and the absolute capacity exactly."""

    data = tuple(int(value) for value in values)
    if not data:
        raise ValueError("values must be nonempty")
    incoming = graph.incoming
    max_prev = {v: data[0] * graph.observable[v] for v in graph.vertices}
    min_prev = dict(max_prev)
    for value in data[1:]:
        max_next: dict[int, int] = {}
        min_next: dict[int, int] = {}
        for vertex in graph.vertices:
            predecessors = incoming[vertex]
            if not predecessors:
                continue
            max_next[vertex] = value * graph.observable[vertex] + max(
                max_prev[u] for u in predecessors
            )
            min_next[vertex] = value * graph.observable[vertex] + min(
                min_prev[u] for u in predecessors
            )
        max_prev, min_prev = max_next, min_next
    maximum = max(max_prev.values())
    minimum = min(min_prev.values())
    return {
        "maximum": maximum,
        "minimum": minimum,
        "capacity": max(abs(maximum), abs(minimum)),
    }


def safe_transducer(transducer: Transducer, graph: Graph) -> bool:
    """Check graph safety for every state, phase, and consecutive input pair."""

    edges = graph.edge_set
    for state, residue, symbol, next_symbol in product(
        range(transducer.state_count),
        range(transducer.q),
        ALPHABET,
        ALPHABET,
    ):
        current = transducer.vertex(state, residue, symbol)
        next_state = transducer.next_state(state, residue, symbol)
        following = transducer.vertex(next_state, residue + 1, next_symbol)
        if (current, following) not in edges:
            return False
    return True


def one_site(transducer: Transducer, graph: Graph) -> bool:
    """Check that the observed label depends only on phase and input."""

    labels: dict[tuple[int, int], int] = {}
    for residue in range(transducer.q):
        for symbol in ALPHABET:
            observed = graph.observable[transducer.vertex(0, residue, symbol)]
            labels[(residue, symbol)] = observed
            for state in range(1, transducer.state_count):
                if graph.observable[transducer.vertex(state, residue, symbol)] != observed:
                    return False
    return True


def simulate(values: Iterable[int], transducer: Transducer, graph: Graph) -> tuple[list[int], int]:
    """Return output vertices and the exact arithmetic correlation score."""

    data = tuple(int(value) for value in values)
    state = transducer.initial_state
    vertices: list[int] = []
    score = 0
    for index, value in enumerate(data, start=1):
        residue = index % transducer.q
        vertex = transducer.vertex(state, residue, value)
        vertices.append(vertex)
        state = transducer.next_state(state, residue, value)
        score += value * graph.observable[vertex]
    return vertices, score


def delta_coefficient(q: int, residue: int) -> str:
    """Human-readable exact density placeholder used in result ledgers."""

    if q == 2 and residue % 2 == 1:
        return "4/pi^2"
    if q == 2 and residue % 2 == 0:
        return "2/pi^2"
    if q == 3 and residue % 3 == 1:
        return "9/(4*pi^2)"
    if q == 4 and residue % 4 in (1, 2):
        return "2/pi^2"
    return "delta_{%d,%d}" % (q, residue % q)


def graph_digest(graph: Graph) -> str:
    """Stable compact representation for result files."""

    return "V=%s;E=%s;obs=%s" % (
        len(graph.observable),
        ",".join("%d>%d" % edge for edge in graph.edges),
        ",".join(map(str, graph.observable)),
    )
