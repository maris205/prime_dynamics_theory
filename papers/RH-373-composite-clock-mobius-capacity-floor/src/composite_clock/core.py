"""Integer and rational checks for the RH-373 phase-selector theorem.

The mathematical statement uses only the RH-366 distance-two sign rule and
squarefree densities in arithmetic progressions.  This module keeps the
finite certificate exact: no floating point values are used for the selector,
the density coefficients, or the universal-safety audit.
"""

from __future__ import annotations

from fractions import Fraction
from itertools import product

Q = 180
ALPHABET = (-1, 0, 1)
STATE_ORDER = ((-1, -1), (-1, 1), (1, -1), (1, 1))
OBSERVABLE = (-1, -1, 1, 1)
EDGES = ((0, 0), (0, 2), (1, 0), (2, 1), (2, 3), (3, 1))
EDGE_SET = frozenset(EDGES)

# The even part is all nonzero squarefree phases in the class 2 (mod 4).
I_EVEN = tuple(r for r in range(Q) if r % 4 == 2 and r % 9 != 0)

# An exact weighted-independent-set witness on the odd phase cycle.  The
# list is intentionally explicit so the theorem can be replayed without a
# hidden optimizer or a numerical fit.
I_ODD = (
    3, 7, 11, 15, 19, 23, 29, 33, 37, 41, 47, 51, 57, 61, 65, 69,
    73, 77, 83, 87, 91, 97, 101, 105, 109, 113, 119, 123, 127, 131,
    137, 141, 147, 151, 155, 159, 163, 167, 173, 177,
)

I = frozenset(I_EVEN + I_ODD)


def mobius_prefix(limit: int) -> list[int]:
    """Return ``mu(1),...,mu(limit)`` using an exact linear sieve."""

    if limit < 1:
        raise ValueError("limit must be positive")
    mu = [0] * (limit + 1)
    composite = [False] * (limit + 1)
    primes: list[int] = []
    mu[1] = 1
    for value in range(2, limit + 1):
        if not composite[value]:
            primes.append(value)
            mu[value] = -1
        for prime in primes:
            multiple = value * prime
            if multiple > limit:
                break
            composite[multiple] = True
            if value % prime == 0:
                mu[multiple] = 0
                break
            mu[multiple] = -mu[value]
    return mu[1:]


def density_coefficient(residue: int) -> Fraction:
    """Return ``pi^2 * delta_(180,residue)`` exactly.

    For q=180=2^2*3^2*5, a squarefree integer in a residue class is
    impossible when 4|r or 9|r.  The remaining local factor at the prime 5
    is 1 or 4/5, giving the two rational coefficients below.
    """

    r = residue % Q
    if r % 4 == 0 or r % 9 == 0:
        return Fraction(0)
    return Fraction(1, 24) if r % 5 == 0 else Fraction(5, 96)


def selector_values(mu: list[int]) -> list[int]:
    """Return the phase selector epsilon_n for a Mobius prefix."""

    values: list[int] = []
    for index, value in enumerate(mu, start=1):
        values.append(1 if index % Q in I and value == 1 else -1)
    return values


def selector_score(mu: list[int]) -> int:
    """Return the exact finite correlation sum ``sum mu(n) epsilon_n``."""

    return sum(value * sign for value, sign in zip(mu, selector_values(mu)))


def path_capacity(values: list[int]) -> int:
    """Return the RH-366 open distance-two capacity by two path DPs."""

    def path_mwis(weights: list[int]) -> int:
        skip = 0
        take = 0
        for weight in weights:
            skip, take = max(skip, take), skip + weight
        return max(skip, take)

    odd = values[0::2]
    even = values[1::2]
    plus = path_mwis(odd) + path_mwis(even)
    minus = path_mwis([-value for value in odd]) + path_mwis([-value for value in even])
    total = sum(values)
    maximum = -total + 2 * plus
    minimum = -total - 2 * minus
    return max(abs(maximum), abs(minimum))


def pair_vertex(current: int, previous: int) -> int:
    """Encode (current, previous) in the frozen RH-366 state order."""

    try:
        return STATE_ORDER.index((current, previous))
    except ValueError as exc:
        raise ValueError("pair signs must be +/-1") from exc


def transducer_tables() -> tuple[
    tuple[tuple[tuple[int, ...], ...], ...],
    tuple[tuple[tuple[int, ...], ...], ...],
]:
    """Build the two-state q=180 universal-safety completion.

    State 0 is M and state 1 is P.  The phase-dependent representative for P
    has previous sign + exactly when the preceding phase is in I.  This makes
    every table row safe, including states that are not reached from the
    chosen initial state.
    """

    transitions: list[list[list[int]]] = []
    outputs: list[list[list[int]]] = []
    for state in range(2):
        transition_row: list[list[int]] = []
        output_row: list[list[int]] = []
        for residue in range(Q):
            previous = 1 if state == 1 and (residue - 1) % Q in I else -1
            transition_cell: list[int] = []
            output_cell: list[int] = []
            for symbol in ALPHABET:
                current = 1 if residue in I and symbol == 1 else -1
                output_cell.append(pair_vertex(current, previous))
                transition_cell.append(1 if current == 1 else 0)
            transition_row.append(transition_cell)
            output_row.append(output_cell)
        transitions.append(transition_row)
        outputs.append(output_row)
    return (
        tuple(tuple(tuple(cell) for cell in row) for row in transitions),
        tuple(tuple(tuple(cell) for cell in row) for row in outputs),
    )


def safe_transducer() -> bool:
    """Check all 2*180*3^2 universal edge constraints."""

    transitions, outputs = transducer_tables()
    for state, residue, symbol, next_symbol in product(
        range(2), range(Q), ALPHABET, ALPHABET
    ):
        current = outputs[state][residue][ALPHABET.index(symbol)]
        next_state = transitions[state][residue][ALPHABET.index(symbol)]
        following = outputs[next_state][(residue + 1) % Q][ALPHABET.index(next_symbol)]
        if (current, following) not in EDGE_SET:
            return False
    return True


def one_site() -> bool:
    """Check that the graph observable is the phase/input selector."""

    transitions, outputs = transducer_tables()
    del transitions
    for residue in range(Q):
        for symbol in ALPHABET:
            index = ALPHABET.index(symbol)
            expected = 1 if residue in I and symbol == 1 else -1
            for state in range(2):
                if OBSERVABLE[outputs[state][residue][index]] != expected:
                    return False
    return True


def simulate_transducer(mu: list[int]) -> tuple[list[int], int]:
    """Simulate the certified transducer and return vertices and score."""

    transitions, outputs = transducer_tables()
    state = 0
    vertices: list[int] = []
    score = 0
    for residue, value in enumerate(mu, start=1):
        index = ALPHABET.index(value)
        vertex = outputs[state][residue % Q][index]
        vertices.append(vertex)
        score += value * OBSERVABLE[vertex]
        state = transitions[state][residue % Q][index]
    return vertices, score


def path_ok(vertices: list[int]) -> bool:
    return all(edge in EDGE_SET for edge in zip(vertices, vertices[1:]))


def capacity_witness(mu: list[int]) -> dict[str, int | bool]:
    """Return finite witness rows used by the result ledger."""

    selector = selector_score(mu)
    vertices, transducer_score = simulate_transducer(mu)
    return {
        "N": len(mu),
        "selector_score": selector,
        "transducer_score": transducer_score,
        "same_score": selector == transducer_score,
        "path_ok": path_ok(vertices),
        "capacity": path_capacity(mu),
        "capacity_witness": abs(selector) <= path_capacity(mu),
    }


def verify_certificate() -> dict[str, object]:
    """Run the complete finite certificate and return exact summary rows."""

    conflicts = sorted(r for r in I if (r + 2) % Q in I)
    counts = {
        "selected": len(I),
        "weight_5_over_96": sum(density_coefficient(r) == Fraction(5, 96) for r in I),
        "weight_1_over_24": sum(density_coefficient(r) == Fraction(1, 24) for r in I),
        "weight_zero": sum(density_coefficient(r) == 0 for r in I),
    }
    numerator = (
        counts["weight_5_over_96"] * 5
        + counts["weight_1_over_24"] * 4
    )
    mu = mobius_prefix(1 << 16)
    endpoint = capacity_witness(mu)
    prefix_rows = 0
    for limit in range(1, 2049):
        row = capacity_witness(mu[:limit])
        if not (row["same_score"] and row["path_ok"] and row["capacity_witness"]):
            raise AssertionError(f"finite witness failed at N={limit}")
        prefix_rows += 1
    return {
        "q": Q,
        "conflicts": conflicts,
        "counts": counts,
        "density_numerator_over_96_pi2": numerator,
        "universal_rows": 2 * Q * len(ALPHABET) ** 2,
        "density_constant": "97/(24*pi^2)",
        "safe_transducer": safe_transducer(),
        "one_site": one_site(),
        "endpoint": endpoint,
        "prefix_witness_rows": prefix_rows,
        "all_pass": (
            not conflicts
            and counts["selected"] == 80
            and counts["weight_5_over_96"] == 68
            and counts["weight_1_over_24"] == 12
            and counts["weight_zero"] == 0
            and numerator == 388
            and safe_transducer()
            and one_site()
            and endpoint["same_score"]
            and endpoint["path_ok"]
            and endpoint["capacity_witness"]
        ),
    }
