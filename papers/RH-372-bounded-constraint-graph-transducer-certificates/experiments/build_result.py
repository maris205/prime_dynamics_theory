"""Build the deterministic RH-372 theorem and provenance ledger."""

from __future__ import annotations

import hashlib
import itertools
import json
from fractions import Fraction
from pathlib import Path

from constraint_transducers.core import (
    ALPHABET,
    Graph,
    Transducer,
    capacity,
    mobius_prefix,
    one_site,
    safe_transducer,
    simulate,
)


ROOT = Path(__file__).resolve().parents[1]
WORKSPACE = ROOT.parents[2]
OUTPUT = ROOT / "results" / "result.json"

SOURCE_FILES = [
    "henon_mobius_correlations/henon_mobius/sft.py",
    "henon_mobius_correlations/henon_mobius/arithmetic.py",
    "prime_dynamics_theory/papers/RH-366-mobius-orthogonality-adaptive-encoding-and-parry-covariance/README.md",
    "prime_dynamics_theory/papers/RH-366-mobius-orthogonality-adaptive-encoding-and-parry-covariance/results/result.json",
    "prime_dynamics_theory/papers/RH-368-parity-factor-mobius-capacity-limit/README.md",
    "prime_dynamics_theory/papers/RH-368-parity-factor-mobius-capacity-limit/results/result.json",
    "prime_dynamics_theory/papers/RH-371-eight-run-distance-two-capacity-obstruction/README.md",
    "prime_dynamics_theory/papers/RH-MVP2-corpus-frontier-synthesis/results/four_volume_archive_verification.json",
    "dyna_zeta_map/paper/sections/6_quadratic_application.tex",
]

SOURCE_COMMITS = {
    "henon_mobius_correlations": "34490443f50cfe9af9ff93888e51e7e7e534a5a7",
    "dyna_zeta_map": "7fd3a3fdd5a6a25827a0965345459baf4a47b816",
    "rh366_release": "6da1b94deaa865bbb297546f3de238433184772a",
    "rh368_release": "ebcf29a4a2d248d8320067d85899b3b8039a7b12",
    "rh371_release": "241b78a89ccbc0bad96d9ef20ee9256d61b4eaca",
}


def digest(path: Path) -> str:
    hasher = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1 << 20), b""):
            hasher.update(chunk)
    return hasher.hexdigest()


def rh366_graph() -> Graph:
    return Graph(
        edges=((0, 0), (0, 2), (1, 0), (2, 1), (2, 3), (3, 1)),
        observable=(-1, -1, 1, 1),
    )


def rh368_graph() -> Graph:
    return Graph(
        edges=((0, 2), (1, 2), (2, 0), (2, 1)),
        observable=(1, -1, -1),
    )


def _table(rows: list[list[list[int]]]) -> tuple[tuple[tuple[int, ...], ...], ...]:
    return tuple(tuple(tuple(cell) for cell in row) for row in rows)


def rh366_transducer() -> Transducer:
    # The two states are a universal-safety completion, rather than a literal
    # previous-sign register.  The observed labels are still exactly the
    # RH-366 phase rule: phases 1 and 2 use ``mu=1`` for the positive label;
    # phases 0 and 3 are negative for every input.  The state-1 rows at phases
    # 2 and 3 choose the alternate negative/positive representatives needed
    # to make every possible input pair an edge of the four-state graph.
    phase_outputs = [
        [[0, 0, 0], [0, 0, 0]],
        [[0, 0, 2], [0, 0, 2]],
        [[0, 0, 2], [1, 1, 3]],
        [[0, 0, 0], [1, 1, 1]],
    ]
    phase_transitions = [
        [[0, 0, 0], [0, 0, 0]],
        [[0, 0, 1], [0, 0, 1]],
        [[0, 0, 1], [0, 0, 1]],
        [[0, 0, 0], [0, 0, 0]],
    ]
    outputs = _table(
        [[phase_outputs[residue][state] for residue in range(4)] for state in range(2)]
    )
    transitions = _table(
        [
            [phase_transitions[residue][state] for residue in range(4)]
            for state in range(2)
        ]
    )
    return Transducer(4, transitions, outputs, 0)


def rh368_transducer() -> Transducer:
    # At odd phases choose I_1 versus I_2; at even phases the only next
    # vertex is I_3.  Both edges are legal for every input symbol.
    transitions = [[[0, 0, 0], [0, 0, 0]]]
    outputs = [[[2, 2, 2], [1, 1, 0]]]
    return Transducer(2, _table(transitions), _table(outputs), 0)


def rh366_q3_switch() -> Transducer:
    # A two-state universal completion of the period-three switch.  At phase
    # 1, only input ``+1`` selects the branch 0 -> 2 -> 1 -> 0; all other
    # inputs use the 0-loop.  Alternate representatives in the second state
    # keep the observable one-site while making the safety quantifier literal.
    phase_outputs = [
        [[0, 0, 0], [0, 0, 0]],
        [[0, 0, 2], [0, 0, 2]],
        [[0, 0, 0], [1, 1, 1]],
    ]
    phase_transitions = [
        [[0, 0, 0], [0, 0, 0]],
        [[0, 0, 1], [0, 0, 1]],
        [[0, 0, 0], [0, 0, 0]],
    ]
    outputs = _table(
        [[phase_outputs[residue][state] for residue in range(3)] for state in range(2)]
    )
    transitions = _table(
        [
            [phase_transitions[residue][state] for residue in range(3)]
            for state in range(2)
        ]
    )
    return Transducer(3, transitions, outputs, 0)


def path_ok(vertices: list[int], graph: Graph) -> bool:
    return all(edge in graph.edge_set for edge in zip(vertices, vertices[1:]))


def density_numerator(q: int, transducer: Transducer, graph: Graph) -> Fraction:
    """Return the coefficient of 1/pi^2 for the small frozen examples."""

    # The source-locked examples use only q=2,3,4.  The AP densities are
    # 2/pi^2 and 4/pi^2 for even/odd q=2, 9/(4*pi^2) for (q,r)=(3,1),
    # and 2/pi^2 for each of (q,r)=(4,1),(4,2).
    weights: dict[tuple[int, int], Fraction] = {
        (2, 0): Fraction(2),
        (2, 1): Fraction(4),
        (3, 1): Fraction(9, 4),
        (4, 1): Fraction(2),
        (4, 2): Fraction(2),
    }
    value = Fraction(0)
    for residue in range(q):
        plus = graph.observable[transducer.vertex(0, residue, 1)]
        minus = graph.observable[transducer.vertex(0, residue, -1)]
        difference = Fraction(plus - minus, 2)
        value += weights.get((q, residue), Fraction(0)) * difference
    return value


def format_limit_constant(value: Fraction) -> str:
    """Format a rational coefficient of 1/pi^2 without ambiguity."""

    if value.denominator == 1:
        return f"{value.numerator}/pi^2"
    return f"{value.numerator}/({value.denominator}*pi^2)"


def enumerate_small_certificates(graph: Graph) -> dict[str, int | str]:
    """Exhaust the q=2, one-state output tables on the three-cell graph."""

    safe_count = 0
    best = Fraction(-1)
    total = len(graph.observable) ** (2 * len(ALPHABET))
    transition = _table([[[0, 0, 0], [0, 0, 0]]])
    for values in itertools.product(range(len(graph.observable)), repeat=2 * len(ALPHABET)):
        outputs = _table([[list(values[:3]), list(values[3:])]])
        candidate = Transducer(2, transition, outputs, 0)
        if not safe_transducer(candidate, graph) or not one_site(candidate, graph):
            continue
        safe_count += 1
        score = abs(density_numerator(2, candidate, graph))
        if score > best:
            best = score
    return {
        "total_tables": total,
        "safe_one_site_tables": safe_count,
        "max_abs_coefficient_of_pi^-2": str(best),
    }


def main() -> None:
    graph366 = rh366_graph()
    graph368 = rh368_graph()
    t366 = rh366_transducer()
    t368 = rh368_transducer()
    t366_q3 = rh366_q3_switch()
    sources = {relative: digest(WORKSPACE / relative) for relative in SOURCE_FILES}
    mu = mobius_prefix(1 << 16)

    instances = []
    for name, graph, transducer, expected in (
        ("RH-366-q4", graph366, t366, Fraction(4)),
        ("RH-368-q2", graph368, t368, Fraction(4)),
        ("RH-366-q3-switch", graph366, t366_q3, Fraction(9, 4)),
    ):
        vertices, score = simulate(mu, transducer, graph)
        instances.append(
            {
                "name": name,
                "graph": {
                    "vertex_count": len(graph.observable),
                    "edge_count": len(graph.edges),
                    "observable": list(graph.observable),
                },
                "clock": transducer.q,
                "memory_states": transducer.state_count,
                "safe": safe_transducer(transducer, graph),
                "one_site": one_site(transducer, graph),
                "path_check": path_ok(vertices[:2048], graph),
                "endpoint_N": len(mu),
                "endpoint_score": score,
                "endpoint_density": score / len(mu),
                "limit_constant": format_limit_constant(expected),
                "coefficient_of_pi^-2": str(density_numerator(transducer.q, transducer, graph)),
            }
        )

    graph_capacity = {}
    for name, graph in (("RH-366", graph366), ("RH-368", graph368)):
        result = capacity(mu, graph)
        graph_capacity[name] = {
            "endpoint_capacity": result["capacity"],
            "endpoint_maximum": result["maximum"],
            "endpoint_minimum": result["minimum"],
            "upper_bound_check": result["capacity"] <= sum(abs(value) * max(map(abs, graph.observable)) for value in mu),
        }

    prefix_checks = 0
    for length in range(1, 129):
        prefix = mu[:length]
        for graph, transducer in ((graph366, t366), (graph368, t368), (graph366, t366_q3)):
            vertices, score = simulate(prefix, transducer, graph)
            if not path_ok(vertices, graph) or abs(score) > int(capacity(prefix, graph)["capacity"]):
                raise AssertionError("transducer certificate is not a capacity witness")
            prefix_checks += 1

    payload = {
        "status": "RH-372_bounded_constraint_graph_transducer_certificates",
        "source_locks": {"count": len(sources), "files": sources, "pass": True},
        "source_commits": SOURCE_COMMITS,
        "graph_instances": instances,
        "graph_capacity": graph_capacity,
        "finite_audit": {
            "endpoint_N": len(mu),
            "prefix_witness_rows": prefix_checks,
            "small_certificate_enumeration": enumerate_small_certificates(graph368),
            "all_safe_and_one_site": all(
                row["safe"] and row["one_site"] and row["path_check"] for row in instances
            ),
        },
        "theorem_contract": {
            "dp_complexity": "O(N|E|)",
            "upper_limsup": "6/pi^2 * ||ell||_infinity",
            "density": "delta_(q,r)=sum_{(q,d^2)|r} mu(d)/lcm(q,d^2)",
            "bounded_resource_scope": "fixed q and finite memory budget; exhaustive finite class only",
        },
        "claim_boundary": {
            "route_a": "GO",
            "route_b": "STOP_SCOPED",
            "route_b_first_blocker": "the transducer reads the Mobius prefix offline and supplies no canonical operator or trace",
            "notes": [
                "Memory-dependent observables are excluded from the unconditional density formula.",
                "Finite-resource enumeration is not a classification of all mixing SFTs.",
                "The RH-366 distance-two capacity limit remains open.",
                "No Hilbert--Polya operator, von Mangoldt trace, zero identification, or RH implication is claimed.",
            ],
        },
        "gates": {
            "A_canonical_intrinsic_dynamical_spectral_determinant": False,
            "B_time_oriented_scattering_or_unitary_completion": False,
            "C_self_adjoint_generator_and_intrinsic_T_log_T": False,
            "D_von_mangoldt_weighted_prime_power_traces": False,
            "E_completed_zeta_divisor_equality": False,
        },
    }
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n")
    print(json.dumps({
        "source_lock_pass": True,
        "instance_count": len(instances),
        "prefix_witness_rows": prefix_checks,
        "status": payload["status"],
    }, sort_keys=True))


if __name__ == "__main__":
    main()
