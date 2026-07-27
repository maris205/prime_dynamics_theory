#!/usr/bin/env python3
"""Deterministic manifest, verdict, and first-missing audit for TPC-MVP3."""

from __future__ import annotations

import argparse
import hashlib
import json
from dataclasses import asdict, dataclass
from pathlib import Path


PROVED = "PROVED"
CONDITIONAL = "CONDITIONAL"
OPEN = "OPEN"
NOT_TESTABLE = "NOT_TESTABLE"
REFUTED = "REFUTED"
VALID_STATUSES = {PROVED, CONDITIONAL, OPEN, NOT_TESTABLE, REFUTED}

HERE = Path(__file__).resolve().parent
PAPERS = HERE.parents[1]
TPC_DIRS = {
    number: next(PAPERS.glob(f"tpc-{number}-*"))
    for number in range(123, 133)
}


@dataclass(frozen=True)
class Node:
    node_id: str
    gate: str
    status: str
    evidence: str
    required_artifact: str
    structural: bool
    scope: str
    carrier_hash: str
    scope_match: bool = True


@dataclass(frozen=True)
class StopRecord:
    stopped: bool
    carrier: str
    scope: str
    source: str


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def topo_order(graph: dict[str, tuple[str, ...]]) -> list[str]:
    indegree = {node: 0 for node in graph}
    children = {node: [] for node in graph}
    for node, parents in graph.items():
        for parent in parents:
            if parent not in graph:
                raise ValueError(f"unknown parent {parent}")
            indegree[node] += 1
            children[parent].append(node)
    queue = sorted(node for node, degree in indegree.items() if degree == 0)
    out: list[str] = []
    while queue:
        node = queue.pop(0)
        out.append(node)
        for child in sorted(children[node]):
            indegree[child] -= 1
            if indegree[child] == 0:
                queue.append(child)
                queue.sort()
    if len(out) != len(graph):
        raise ValueError("cyclic snapshot DAG")
    return out


def validate_order(
    graph: dict[str, tuple[str, ...]],
    order: list[str],
) -> None:
    if set(order) != set(graph) or len(order) != len(set(order)):
        raise ValueError("topological order does not exactly cover the DAG")
    position = {node: index for index, node in enumerate(order)}
    for node, parents in graph.items():
        if any(position[parent] >= position[node] for parent in parents):
            raise ValueError("declared order is not topological")


def first_missing(
    nodes: list[Node],
    graph: dict[str, tuple[str, ...]],
    order: list[str],
) -> Node | None:
    validate_order(graph, order)
    by_id = {node.node_id: node for node in nodes}
    if set(by_id) != set(graph):
        raise ValueError("node table does not exactly cover the DAG")
    for node_id in order:
        node = by_id[node_id]
        if node.status == NOT_TESTABLE:
            return node
    return None


def stop_cover_valid(
    route_universe: set[str],
    route_stops: dict[str, StopRecord],
) -> bool:
    if set(route_stops) != route_universe or not route_universe:
        return False
    return all(
        record.stopped
        and bool(record.carrier)
        and bool(record.scope)
        and bool(record.source)
        for record in route_stops.values()
    )


def endpoint_certified(endpoint: dict[str, object]) -> bool:
    return (
        endpoint.get("proved") is True
        and endpoint.get("strict_slack") is True
        and bool(endpoint.get("source"))
        and bool(endpoint.get("route_cell"))
    )


def validate_snapshot(
    nodes: list[Node],
    route_universe: set[str],
    route_stops: dict[str, StopRecord],
    selected_route: str,
    typed_alternative: str | None,
) -> None:
    if len({node.node_id for node in nodes}) != len(nodes):
        raise ValueError("duplicate node id")
    if any(node.status not in VALID_STATUSES for node in nodes):
        raise ValueError("unknown node status")
    if selected_route not in route_universe:
        raise ValueError("selected route is outside the declared universe")
    if not set(route_stops) <= route_universe:
        raise ValueError("stop map contains an undeclared route")
    for route, record in route_stops.items():
        if record.stopped and (
            not record.carrier or not record.scope or not record.source
        ):
            raise ValueError(f"stop record for {route} lacks proof metadata")
    if typed_alternative is not None:
        if typed_alternative not in route_universe:
            raise ValueError("typed alternative is outside route universe")
        if typed_alternative == selected_route:
            raise ValueError("selected route cannot be its own alternative")
        if not route_stops.get(
            selected_route,
            StopRecord(False, "", "", ""),
        ).stopped:
            raise ValueError("reroute declared without a selected-route stop")
        if route_stops.get(
            typed_alternative,
            StopRecord(False, "", "", ""),
        ).stopped:
            raise ValueError("typed alternative is already stopped")


def decide(
    nodes: list[Node],
    *,
    endpoint: dict[str, object],
    route_universe: set[str],
    route_stops: dict[str, StopRecord],
    selected_route: str,
    typed_alternative: str | None,
) -> str:
    """Return one ordered exhaustive outcome after manifest validation."""

    validate_snapshot(
        nodes,
        route_universe,
        route_stops,
        selected_route,
        typed_alternative,
    )
    endpoint_ok = endpoint_certified(endpoint)
    if all(node.status == PROVED and node.scope_match for node in nodes) and endpoint_ok:
        return "GO"

    if stop_cover_valid(route_universe, route_stops):
        return "ARCHITECTURE_INFEASIBLE"

    selected_stopped = route_stops.get(
        selected_route,
        StopRecord(False, "", "", ""),
    ).stopped
    if selected_stopped:
        if typed_alternative is not None:
            return "REROUTE"
        return "STOP_ROUTE"

    if any(node.status == NOT_TESTABLE or not node.scope_match for node in nodes):
        return "NOT_TESTABLE"

    unresolved = [node for node in nodes if node.status != PROVED]
    structural_closed = all(
        node.status == PROVED and node.scope_match
        for node in nodes
        if node.structural
    )
    all_unresolved_are_open_positive_l2 = bool(unresolved) and all(
        node.status == OPEN
        and node.evidence == "L2_TARGET_POSITIVE"
        and not node.structural
        and node.scope_match
        for node in unresolved
    )
    if endpoint_ok and structural_closed and all_unresolved_are_open_positive_l2:
        return "ARITHMETIC_FRONTIER"

    return "OPEN"


def snapshot_graph() -> dict[str, tuple[str, ...]]:
    return {
        "H1.archive": (),
        "H2.resonance": ("H1.archive",),
        "H3.generic": ("H1.archive",),
        "H4.tail": ("H1.archive",),
        "H5.det_zero": ("H1.archive",),
        "H6.cover": ("H1.archive",),
        "H7.fixed_h0": ("H1.archive",),
        "H8.reconnection": (
            "H1.archive",
            "H6.cover",
            "H7.fixed_h0",
        ),
        "H9.endpoint": (
            "H2.resonance",
            "H3.generic",
            "H4.tail",
            "H5.det_zero",
            "H6.cover",
            "H7.fixed_h0",
            "H8.reconnection",
        ),
    }


def current_snapshot_nodes(hashes: dict[str, str]) -> list[Node]:
    scope = "fixed-h0=2|physical-normalization=nu_X"
    return [
        Node(
            "H1.archive", "H1", NOT_TESTABLE, "L1_TARGET",
            "complete actual-carrier native path archive", True,
            scope, hashes["TPC-123"],
        ),
        Node(
            "H2.resonance", "H2", OPEN, "L2_TARGET_POSITIVE",
            "literal growing resonance ledgers or signed replacement", False,
            scope, hashes["TPC-120"],
        ),
        Node(
            "H3.generic", "H3", OPEN, "L2_TARGET_POSITIVE",
            (
                "uniform actual Fejer four-Liouville estimate with "
                "participation, masks, phases, weights, origins, and prefixes"
            ),
            False, scope, hashes["TPC-130"],
        ),
        Node(
            "H4.tail", "H4", OPEN, "L2_TARGET_POSITIVE",
            "complete original-scale physical tail estimate", False,
            scope, hashes["TPC-120"],
        ),
        Node(
            "H5.det_zero", "H5", NOT_TESTABLE, "L2_TARGET_POSITIVE",
            "actual compatible lambda_D and eta_Z certificates", False,
            scope, hashes["TPC-121-122"],
        ),
        Node(
            "H6.cover", "H6", NOT_TESTABLE, "L1_TARGET",
            "actual growing physical B,w cover or residual certificate", True,
            scope, hashes["TPC-124"],
        ),
        Node(
            "H7.fixed_h0", "H7", NOT_TESTABLE, "L1_TARGET",
            "complete shift-tagged archive or subcritical localization", True,
            scope, hashes["TPC-125"],
        ),
        Node(
            "H8.reconnection", "H8", NOT_TESTABLE, "L1_TARGET",
            "complete exact hard-packet intertwining", True,
            scope, hashes["TPC-123"],
        ),
        Node(
            "H9.endpoint", "H9", NOT_TESTABLE, "L1_TARGET",
            "complete occurrence registry and strict endpoint certificate", True,
            scope, hashes["TPC-131"],
        ),
    ]


def scenario_nodes(
    statuses: list[tuple[str, str, bool]],
) -> list[Node]:
    return [
        Node(
            f"N{index}",
            f"G{index}",
            status,
            evidence,
            f"artifact-{index}",
            structural,
            "scope",
            f"hash-{index}",
        )
        for index, (status, evidence, structural) in enumerate(statuses)
    ]


def route_records(
    records: dict[str, bool],
) -> dict[str, StopRecord]:
    return {
        route: StopRecord(
            stopped=stopped,
            carrier=f"carrier-{route}",
            scope="scope",
            source=f"theorem-{route}" if stopped else "",
        )
        for route, stopped in records.items()
    }


def audit() -> dict[str, object]:
    content_hashes = {
        f"TPC-{number}": sha256(TPC_DIRS[number] / "main.tex")
        for number in range(123, 133)
    }
    # Existing prerequisite papers are frozen by their source hashes too.
    content_hashes["TPC-120"] = sha256(
        next(PAPERS.glob("tpc-120-*")) / "main.tex"
    )
    content_hashes["TPC-121-122"] = hashlib.sha256(
        (
            sha256(next(PAPERS.glob("tpc-121-*")) / "main.tex")
            + sha256(next(PAPERS.glob("tpc-122-*")) / "main.tex")
        ).encode("ascii")
    ).hexdigest()

    graph = snapshot_graph()
    order = topo_order(graph)
    snapshot = current_snapshot_nodes(content_hashes)
    missing = first_missing(snapshot, graph, order)

    route_universe = {
        "signed_native",
        "positive_resonance",
        "coherent_prime_square",
    }
    current_stops = route_records(
        {
            "signed_native": False,
            "positive_resonance": True,
            "coherent_prime_square": True,
        }
    )
    incomplete_endpoint = {
        "proved": False,
        "strict_slack": False,
        "source": "",
        "route_cell": "signed_native",
    }
    current_verdict = decide(
        snapshot,
        endpoint=incomplete_endpoint,
        route_universe=route_universe,
        route_stops=current_stops,
        selected_route="signed_native",
        typed_alternative=None,
    )

    endpoint_pass = {
        "proved": True,
        "strict_slack": True,
        "source": "endpoint theorem",
        "route_cell": "r1",
    }
    endpoint_fail = {
        "proved": False,
        "strict_slack": False,
        "source": "",
        "route_cell": "r1",
    }
    all_proved = scenario_nodes([(PROVED, "L1", True)] * 3)
    open_l2 = scenario_nodes(
        [
            (PROVED, "L1", True),
            (PROVED, "L1", True),
            (OPEN, "L2_TARGET_POSITIVE", False),
        ]
    )
    ordinary_open = scenario_nodes(
        [
            (PROVED, "L1", True),
            (OPEN, "L1_TARGET", True),
            (OPEN, "L2_TARGET_POSITIVE", False),
        ]
    )
    missing_nodes = scenario_nodes(
        [
            (NOT_TESTABLE, "L1_TARGET", True),
            (OPEN, "L2_TARGET_POSITIVE", False),
        ]
    )
    stopped_nodes = scenario_nodes(
        [
            (REFUTED, "L2_NEGATIVE", False),
            (OPEN, "L2_TARGET_POSITIVE", False),
        ]
    )
    universe_two = {"r1", "r2"}
    no_stops_two = route_records({"r1": False, "r2": False})
    all_stopped_two = route_records({"r1": True, "r2": True})

    scenarios = {
        "GO": decide(
            all_proved,
            endpoint=endpoint_pass,
            route_universe=universe_two,
            route_stops=no_stops_two,
            selected_route="r1",
            typed_alternative=None,
        ),
        "ARCHITECTURE_INFEASIBLE": decide(
            ordinary_open,
            endpoint=endpoint_fail,
            route_universe=universe_two,
            route_stops=all_stopped_two,
            selected_route="r1",
            typed_alternative=None,
        ),
        "REROUTE": decide(
            stopped_nodes,
            endpoint=endpoint_fail,
            route_universe=universe_two,
            route_stops=route_records({"r1": True, "r2": False}),
            selected_route="r1",
            typed_alternative="r2",
        ),
        "STOP_ROUTE": decide(
            stopped_nodes,
            endpoint=endpoint_fail,
            route_universe=universe_two,
            route_stops=route_records({"r1": True, "r2": False}),
            selected_route="r1",
            typed_alternative=None,
        ),
        "NOT_TESTABLE": decide(
            missing_nodes,
            endpoint=endpoint_fail,
            route_universe=universe_two,
            route_stops=no_stops_two,
            selected_route="r1",
            typed_alternative=None,
        ),
        "ARITHMETIC_FRONTIER": decide(
            open_l2,
            endpoint=endpoint_pass,
            route_universe=universe_two,
            route_stops=no_stops_two,
            selected_route="r1",
            typed_alternative=None,
        ),
        "OPEN": decide(
            ordinary_open,
            endpoint=endpoint_fail,
            route_universe=universe_two,
            route_stops=no_stops_two,
            selected_route="r1",
            typed_alternative=None,
        ),
    }
    outcomes_reachable = all(key == value for key, value in scenarios.items())

    conditional_frontier_rejected = (
        decide(
            scenario_nodes(
                [
                    (PROVED, "L1", True),
                    (CONDITIONAL, "L2_TARGET_POSITIVE", False),
                ]
            ),
            endpoint=endpoint_pass,
            route_universe=universe_two,
            route_stops=no_stops_two,
            selected_route="r1",
            typed_alternative=None,
        )
        != "ARITHMETIC_FRONTIER"
    )
    refuted_frontier_rejected = (
        decide(
            scenario_nodes(
                [
                    (PROVED, "L1", True),
                    (REFUTED, "L2_NEGATIVE", False),
                    (OPEN, "L2_TARGET_POSITIVE", False),
                ]
            ),
            endpoint=endpoint_pass,
            route_universe=universe_two,
            route_stops=no_stops_two,
            selected_route="r1",
            typed_alternative=None,
        )
        != "ARITHMETIC_FRONTIER"
    )
    incomplete_cover_rejected = not stop_cover_valid(
        universe_two,
        {"r1": all_stopped_two["r1"]},
    )
    contradictory_manifest_rejected = False
    try:
        decide(
            stopped_nodes,
            endpoint=endpoint_fail,
            route_universe=universe_two,
            route_stops=route_records({"r1": False, "r2": False}),
            selected_route="r1",
            typed_alternative="r2",
        )
    except ValueError:
        contradictory_manifest_rejected = True

    no_positive_l2 = all(
        node.status != PROVED or node.evidence != "L2_POSITIVE"
        for node in snapshot
    )
    first_missing_ok = (
        missing is not None
        and missing.node_id == "H1.archive"
        and current_verdict == "NOT_TESTABLE"
    )
    manifest_complete = all(
        [
            bool(content_hashes),
            bool(route_universe),
            "signed_native" in route_universe,
            set(graph) == {node.node_id for node in snapshot},
            bool(order),
            set(current_stops) == route_universe,
            "route_cell" in incomplete_endpoint,
        ]
    )

    status = all(
        [
            outcomes_reachable,
            conditional_frontier_rejected,
            refuted_frontier_rejected,
            incomplete_cover_rejected,
            contradictory_manifest_rejected,
            no_positive_l2,
            first_missing_ok,
            manifest_complete,
        ]
    )

    return {
        "schema": "tpc-132-mvp3-route-decision-v2",
        "snapshot_manifest": {
            "date": "2026-07-27",
            "content_hashes": content_hashes,
            "route_universe": sorted(route_universe),
            "selected_route": "signed_native",
            "dag_edges": {
                node: list(parents) for node, parents in graph.items()
            },
            "topological_order": order,
            "occurrence_registry": {
                "status": "INCOMPLETE",
                "required_artifact": (
                    "complete theorem-backed occurrence registry"
                ),
            },
            "endpoint": incomplete_endpoint,
        },
        "status": "PASS" if status else "FAIL",
        "current_verdict": current_verdict,
        "first_missing": None
        if missing is None
        else {
            "node_id": missing.node_id,
            "gate": missing.gate,
            "status": missing.status,
            "evidence": missing.evidence,
            "required_artifact": missing.required_artifact,
        },
        "checks": {
            "seven_ordered_outcomes_reachable": outcomes_reachable,
            "conditional_frontier_rejected": conditional_frontier_rejected,
            "refuted_frontier_rejected": refuted_frontier_rejected,
            "incomplete_route_cover_rejected": incomplete_cover_rejected,
            "contradictory_manifest_rejected": contradictory_manifest_rejected,
            "no_positive_L2_in_snapshot": no_positive_l2,
            "dag_checked_first_missing": first_missing_ok,
            "snapshot_manifest_fields_present": manifest_complete,
        },
        "scenario_regression": scenarios,
        "gate_status": {
            node.gate: {
                key: value
                for key, value in asdict(node).items()
                if key != "carrier_hash"
            }
            | {"carrier_hash": node.carrier_hash}
            for node in snapshot
        },
        "route_stops": {
            route: asdict(record)
            for route, record in current_stops.items()
        },
        "claim_boundary": {
            "GO": False,
            "ARITHMETIC_FRONTIER": False,
            "ARCHITECTURE_INFEASIBLE": False,
            "fixed_h0_L2_saving": False,
            "prime_pair_theorem": False,
            "twin_prime_theorem": False,
        },
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--check",
        action="store_true",
        help="compare with the committed JSON instead of rewriting it",
    )
    args = parser.parse_args()
    payload = audit()
    out = Path(__file__).with_suffix(".json")
    rendered = json.dumps(payload, indent=2, sort_keys=True) + "\n"
    if args.check:
        if not out.exists() or out.read_text(encoding="utf-8") != rendered:
            raise SystemExit("certificate mismatch")
    else:
        out.write_text(rendered, encoding="utf-8")
    print(rendered, end="")
    if payload["status"] != "PASS":
        raise SystemExit(1)


if __name__ == "__main__":
    main()
