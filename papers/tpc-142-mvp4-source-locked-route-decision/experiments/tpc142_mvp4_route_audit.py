#!/usr/bin/env python3
"""Deterministic source-locked MVP4 route audit for TPC-142.

The script reads the frozen TPC-141 batch manifest.  Default mode writes
the derived MVP4 snapshot and audit JSON; ``--check`` performs no writes.
No arithmetic sum is evaluated.
"""

from __future__ import annotations

import argparse
import copy
import hashlib
import json
from fractions import Fraction
from pathlib import Path
from typing import Any


HERE = Path(__file__).resolve().parent
PAPER_DIR = HERE.parent
PAPERS_DIR = PAPER_DIR.parent
TPC141_DIR = (
    PAPERS_DIR / "tpc-141-source-locked-cut-arithmetic-integration"
)
TPC141_MANIFEST = (
    TPC141_DIR / "experiments" / "tpc141_batch_manifest.json"
)
TPC141_SCHEMA = (
    TPC141_DIR / "experiments" / "tpc141_batch_manifest.schema.json"
)
SCHEMA_PATH = HERE / "tpc142_mvp4_snapshot.schema.json"
SNAPSHOT_PATH = HERE / "tpc142_mvp4_snapshot.json"
AUDIT_PATH = HERE / "tpc142_mvp4_route_audit.json"

SNAPSHOT_SCHEMA = "tpc-142-mvp4-source-locked-snapshot-v1"
SOURCE_SCHEMA = "tpc-141-source-locked-batch-manifest-v1"
VALID_STATUSES = {
    "PROVED",
    "CONDITIONAL",
    "OPEN",
    "NOT_TESTABLE",
    "REFUTED",
}
ORDERED_VERDICTS = [
    "GO",
    "ARCHITECTURE_INFEASIBLE",
    "REROUTE",
    "STOP_ROUTE",
    "NOT_TESTABLE",
    "ARITHMETIC_FRONTIER",
    "OPEN",
]


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def sha256_file(path: Path) -> str:
    return sha256_bytes(path.read_bytes())


def canonical_json(payload: Any) -> str:
    return json.dumps(payload, indent=2, sort_keys=True) + "\n"


def parse_fraction(record: dict[str, int]) -> Fraction:
    denominator = record["denominator"]
    if denominator <= 0:
        raise ValueError("fraction denominator must be positive")
    return Fraction(record["numerator"], denominator)


def topo_order(graph: dict[str, tuple[str, ...]]) -> list[str]:
    indegree = {node: 0 for node in graph}
    children = {node: [] for node in graph}
    for node, parents in graph.items():
        for parent in parents:
            if parent not in graph:
                raise ValueError(f"unknown DAG parent {parent}")
            indegree[node] += 1
            children[parent].append(node)
    queue = sorted(node for node, degree in indegree.items() if degree == 0)
    order: list[str] = []
    while queue:
        node = queue.pop(0)
        order.append(node)
        for child in sorted(children[node]):
            indegree[child] -= 1
            if indegree[child] == 0:
                queue.append(child)
                queue.sort()
    if len(order) != len(graph):
        raise ValueError("cyclic snapshot DAG")
    return order


def validate_order(
    graph: dict[str, tuple[str, ...]],
    order: list[str],
) -> None:
    if len(order) != len(set(order)) or set(order) != set(graph):
        raise ValueError("declared topological order does not cover DAG")
    position = {node: index for index, node in enumerate(order)}
    for node, parents in graph.items():
        if any(position[parent] >= position[node] for parent in parents):
            raise ValueError("declared order is not topological")


def ancestor_closure(
    graph: dict[str, tuple[str, ...]],
    node_id: str,
) -> set[str]:
    """Return every direct or indirect parent of ``node_id``."""

    seen: set[str] = set()
    stack = list(graph[node_id])
    while stack:
        parent = stack.pop()
        if parent in seen:
            continue
        seen.add(parent)
        stack.extend(graph[parent])
    return seen


def load_source_manifest() -> tuple[dict[str, Any], str]:
    if not TPC141_MANIFEST.is_file():
        raise FileNotFoundError(
            "TPC-141 manifest is missing; run its audit in default mode first"
        )
    rendered = TPC141_MANIFEST.read_text(encoding="utf-8")
    manifest = json.loads(rendered)
    if canonical_json(manifest) != rendered:
        raise ValueError("TPC-141 manifest is not in canonical JSON form")
    return manifest, rendered


def recompute_first_missing(
    source: dict[str, Any],
) -> dict[str, Any] | None:
    nodes = {record["node_id"]: record for record in source["nodes"]}
    if len(nodes) != len(source["nodes"]):
        raise ValueError("duplicate source node id")
    graph = {
        node_id: tuple(parents)
        for node_id, parents in source["proof_dag"]["parents"].items()
    }
    if set(nodes) != set(graph):
        raise ValueError("source node table differs from source DAG")
    topo_order(graph)
    order = source["proof_dag"]["topological_order"]
    validate_order(graph, order)
    for node_id in order:
        record = nodes[node_id]
        if record["required_for_selected_route"] and (
            record["status"] == "NOT_TESTABLE"
            or not record.get("scope_match", True)
        ):
            return {
                "node_id": node_id,
                "gate": record["gate"],
                "status": record["status"],
                "program_level": record["program_level"],
                "required_artifact": record["required_artifact"],
            }
    return None


def validate_source_manifest(source: dict[str, Any]) -> dict[str, bool]:
    if source.get("schema") != SOURCE_SCHEMA:
        raise ValueError("unexpected TPC-141 manifest schema")
    if len(source.get("source_bundles", {})) != 8:
        raise ValueError("TPC-141 source bundle count is not eight")
    if source["snapshot"]["schema_sha256"] != sha256_file(TPC141_SCHEMA):
        raise ValueError("TPC-141 schema hash drift")
    if source["snapshot"].get("source_hash_semantics") != "INTEGRITY_ONLY":
        raise ValueError("TPC-141 assigned proof semantics to source hashes")
    if source["snapshot"].get(
        "restricted_positive_arithmetic_shadow"
    ) != "SMALL_POLYLOG_AFFINE_ALMOST_SCALE":
        raise ValueError("TPC-141 restricted positive shadow is absent")
    if source["snapshot"].get("exceptional_window_state") != (
        "GLOBAL_DENSITY_PROVED_LOCAL_ACTUAL_WINDOW_OPEN"
    ):
        raise ValueError("TPC-141 exceptional-window state is absent")
    for number in range(133, 141):
        bundle = source["source_bundles"].get(f"TPC-{number}")
        if bundle is None or len(bundle.get("bundle_sha256", "")) != 64:
            raise ValueError("TPC-141 source bundle is absent or unhashed")

    missing = recompute_first_missing(source)
    if missing != source["first_missing"]:
        raise ValueError("TPC-141 first-missing record is stale")
    if missing is None or missing["node_id"] != "H1.frontier_totalization":
        raise ValueError("unexpected TPC-141 first missing node")

    nodes = {record["node_id"]: record for record in source["nodes"]}
    graph = {
        node_id: tuple(parents)
        for node_id, parents in source["proof_dag"]["parents"].items()
    }
    h9_ancestors = ancestor_closure(graph, "H9.physical_registry")
    if any(
        nodes[ancestor]["gate"].split(".", 1)[0] in {"H2", "H3", "H4", "H5"}
        for ancestor in h9_ancestors
    ):
        raise ValueError("H9 has a direct or indirect arithmetic dependency")
    if source["endpoint_ledger"]["determinant_reserve_reusable"]:
        raise ValueError("determinant reserve was reused physically")
    if parse_fraction(source["endpoint_ledger"]["sigma_target"]) != Fraction(
        1, 400
    ):
        raise ValueError("TPC-141 endpoint threshold drift")
    if source["endpoint_ledger"]["state"] != "INCOMPLETE":
        raise ValueError("unexpected current endpoint state")
    if source["claim_boundary"]["positive_L2"]:
        raise ValueError("TPC-141 falsely claims positive L2")
    cut = source["cut_aware_bound"]
    expected_bound = (
        "|B| <= o(X)+|S_frontier|"
        "+X^(1-sigma_eligible+Lambda_eligible+o(1))"
    )
    if (
        cut["identity"] != "B=S_soft+S_eligible+S_frontier"
        or cut["soft"] != "o(X)"
        or cut["bound"] != expected_bound
        or not cut["frontier_explicit"]
        or cut.get("coverage") != "DECLARED_THREE_WAY_CUT_ONLY"
        or cut.get("full_carrier_totalized") is not False
    ):
        raise ValueError("TPC-141 cut scope or explicit frontier drifted")
    if source["gate_projection"]["H1"]["status"] != "NOT_TESTABLE":
        raise ValueError("cut completeness was promoted to full-carrier H1")
    boundary = source["claim_boundary"]
    if any(
        boundary[field]
        for field in (
            "source_hashes_prove_theorems",
            "cut_complete_is_full_carrier",
            "arithmetic_frontier",
            "positive_L2",
            "strict_endpoint",
            "endpoint_pass",
        )
    ):
        raise ValueError("TPC-141 contains an unsupported promotion")
    exports = {
        record["export_id"]: record for record in source["exports"]
    }
    restricted = exports.get("A139.small_polylog_affine_almost_scale")
    if (
        restricted is None
        or restricted["status"] != "PROVED"
        or restricted["program_level"] != "L1"
        or restricted["coverage"]
        != "RESTRICTED_ALMOST_SCALE_ARITHMETIC_SHADOW"
        or restricted["promotion_eligible"]
    ):
        raise ValueError("restricted positive shadow was promoted or mistyped")
    return {
        "source_schema": True,
        "source_bundles_hashed": True,
        "source_hashes_integrity_only": True,
        "restricted_positive_arithmetic_shadow_scoped": True,
        "global_density_not_promoted_to_terminal_window": True,
        "source_DAG_and_order": True,
        "source_first_missing": True,
        "H9_transitively_arithmetic_independent": True,
        "one_over_400_contract": True,
        "cut_complete_not_full_carrier": True,
        "frontier_explicit": True,
        "no_positive_L2_source": True,
    }


def normalize_gates(
    gates: dict[str, dict[str, Any]],
) -> dict[str, dict[str, Any]]:
    expected = {f"H{index}" for index in range(1, 10)}
    if set(gates) != expected:
        raise ValueError("gate projection is not exactly H1--H9")
    normalized: dict[str, dict[str, Any]] = {}
    for gate, record in gates.items():
        if record["status"] not in VALID_STATUSES:
            raise ValueError("unknown gate status")
        normalized[gate] = dict(record)
        normalized[gate].setdefault("scope_match", True)
    return normalized


def stop_cover_valid(routes: dict[str, Any]) -> bool:
    universe = set(routes["routes"])
    stops = routes["stops"]
    if not universe or set(stops) != universe:
        return False
    return all(
        record["stopped"]
        and bool(record["source_export"])
        and bool(record["scope_id"])
        and bool(record["carrier_id"])
        for record in stops.values()
    )


def validate_routes(routes: dict[str, Any]) -> None:
    universe = set(routes["routes"])
    selected = routes["selected_route"]
    stops = routes["stops"]
    if not universe or selected not in universe:
        raise ValueError("selected route is outside route universe")
    if set(stops) != universe:
        raise ValueError("stop map does not exactly cover route universe")
    for route, record in stops.items():
        if record["stopped"] and (
            not record["source_export"]
            or not record["scope_id"]
            or not record["carrier_id"]
        ):
            raise ValueError(f"stop record for {route} lacks metadata")
    alternative = routes.get("typed_alternative")
    if alternative is not None:
        if alternative not in universe or alternative == selected:
            raise ValueError("invalid typed alternative")
        if not stops[selected]["stopped"]:
            raise ValueError("reroute lacks selected-route stop")
        if stops[alternative]["stopped"]:
            raise ValueError("typed alternative is already stopped")


def endpoint_certified(endpoint: dict[str, Any]) -> bool:
    return (
        endpoint.get("state") == "STRICT_PASS"
        and endpoint.get("strict_slack") is not None
        and endpoint.get("lambda_phys_upper") is not None
    )


def decide(
    gates: dict[str, dict[str, Any]],
    endpoint: dict[str, Any],
    routes: dict[str, Any],
) -> str:
    """Apply the seven ordered valid-snapshot verdicts."""

    gates = normalize_gates(gates)
    validate_routes(routes)
    endpoint_ok = endpoint_certified(endpoint)

    if all(
        record["status"] == "PROVED" and record["scope_match"]
        for record in gates.values()
    ) and endpoint_ok:
        return "GO"

    if stop_cover_valid(routes):
        return "ARCHITECTURE_INFEASIBLE"

    selected = routes["selected_route"]
    selected_stopped = routes["stops"][selected]["stopped"]
    if selected_stopped:
        if routes.get("typed_alternative") is not None:
            return "REROUTE"
        return "STOP_ROUTE"

    if any(
        record["status"] == "NOT_TESTABLE"
        or not record["scope_match"]
        for record in gates.values()
    ):
        return "NOT_TESTABLE"

    unresolved = [
        record for record in gates.values()
        if record["status"] != "PROVED"
    ]
    structural_closed = all(
        record["status"] == "PROVED" and record["scope_match"]
        for record in gates.values()
        if record["structural"]
    )
    unresolved_are_open_positive_l2 = bool(unresolved) and all(
        record["status"] == "OPEN"
        and record["evidence"] == "L2_TARGET_POSITIVE"
        and not record["structural"]
        and record["scope_match"]
        for record in unresolved
    )
    if (
        endpoint_ok
        and structural_closed
        and unresolved_are_open_positive_l2
    ):
        return "ARITHMETIC_FRONTIER"
    return "OPEN"


def build_snapshot(
    source: dict[str, Any],
    source_rendered: str,
) -> dict[str, Any]:
    source_checks = validate_source_manifest(source)
    gates = normalize_gates(source["gate_projection"])
    routes = copy.deepcopy(source["route_universe"])
    endpoint = copy.deepcopy(source["endpoint_ledger"])
    verdict = decide(gates, endpoint, routes)
    if verdict != "NOT_TESTABLE":
        raise ValueError("unexpected current MVP4 verdict")
    first_missing = recompute_first_missing(source)
    if first_missing is None:
        raise ValueError("current snapshot has no first-missing record")

    return {
        "schema": SNAPSHOT_SCHEMA,
        "snapshot": {
            "date": "2026-07-27",
            "source_manifest": (
                "tpc-141-source-locked-cut-arithmetic-integration/"
                "experiments/tpc141_batch_manifest.json"
            ),
            "source_manifest_sha256": sha256_bytes(
                source_rendered.encode("utf-8")
            ),
            "source_schema_sha256": sha256_file(TPC141_SCHEMA),
            "snapshot_schema_sha256": sha256_file(SCHEMA_PATH),
            "selected_route": routes["selected_route"],
        },
        "imported_manifest_summary": {
            "source_schema": source["schema"],
            "source_range": source["snapshot"]["source_range"],
            "source_bundle_hashes": {
                paper: bundle["bundle_sha256"]
                for paper, bundle in source["source_bundles"].items()
            },
            "source_validation": source_checks,
            "integration_state": "ASSEMBLED_WITH_GAPS",
            "source_hash_semantics": source["snapshot"][
                "source_hash_semantics"
            ],
            "restricted_positive_arithmetic_shadow": source["snapshot"][
                "restricted_positive_arithmetic_shadow"
            ],
            "exceptional_window_state": source["snapshot"][
                "exceptional_window_state"
            ],
            "frontier_explicit": source["cut_aware_bound"][
                "frontier_explicit"
            ],
            "full_carrier_totalized": source["cut_aware_bound"][
                "full_carrier_totalized"
            ],
        },
        "gate_projection": gates,
        "proof_dag": copy.deepcopy(source["proof_dag"]),
        "endpoint": endpoint,
        "route_universe": routes,
        "first_missing": first_missing,
        "ordered_verdicts": ORDERED_VERDICTS,
        "current_verdict": verdict,
        "progress_tags": [
            "STRUCTURAL_L1_NATIVE_CUT",
            "CUT_COMPLETE_ONLY_NOT_FULL_CARRIER",
            "SCOPED_NEGATIVE_ELIGIBLE_ONLY",
            "SCOPED_NEGATIVE_SHIFT1_REPARAMETERIZATION",
            "FIXED_LOG_ARITHMETIC_SHADOW",
            "RESTRICTED_SMALL_POLYLOG_ALMOST_SCALE_SHADOW",
            "GLOBAL_TO_TERMINAL_WINDOW_DENSITY_FIREWALL",
            "LOCAL_ACTUAL_EXCEPTIONAL_WINDOW_OPEN",
            "CONDITIONAL_RAW_POWER_LEDGER",
        ],
        "claim_boundary": {
            "source_hashes_prove_theorems": False,
            "cut_complete_is_full_carrier": False,
            "GO": False,
            "ARITHMETIC_FRONTIER": False,
            "ARCHITECTURE_INFEASIBLE": False,
            "positive_L2": False,
            "strict_endpoint": False,
            "endpoint_pass": False,
            "hard_packet_oX": False,
            "prime_pair_theorem": False,
            "twin_prime_theorem": False,
        },
    }


def validate_snapshot(
    snapshot: dict[str, Any],
    source_rendered: str,
) -> dict[str, bool]:
    schema = json.loads(SCHEMA_PATH.read_text(encoding="utf-8"))
    required = set(schema["required"])
    if set(snapshot) != required:
        raise ValueError("snapshot fields differ from schema contract")
    if snapshot["schema"] != SNAPSHOT_SCHEMA:
        raise ValueError("snapshot schema name mismatch")
    if schema["properties"]["schema"]["const"] != SNAPSHOT_SCHEMA:
        raise ValueError("JSON schema and generator schema differ")
    if snapshot["snapshot"]["source_manifest_sha256"] != sha256_bytes(
        source_rendered.encode("utf-8")
    ):
        raise ValueError("source manifest hash mismatch")
    source = json.loads(source_rendered)
    if (
        snapshot["imported_manifest_summary"].get("source_hash_semantics")
        != "INTEGRITY_ONLY"
    ):
        raise ValueError("snapshot assigned proof semantics to source hashes")
    if snapshot["imported_manifest_summary"].get(
        "restricted_positive_arithmetic_shadow"
    ) != "SMALL_POLYLOG_AFFINE_ALMOST_SCALE":
        raise ValueError("snapshot lost the restricted positive shadow")
    if snapshot["imported_manifest_summary"].get(
        "exceptional_window_state"
    ) != "GLOBAL_DENSITY_PROVED_LOCAL_ACTUAL_WINDOW_OPEN":
        raise ValueError("snapshot promoted global density to a local window")
    if snapshot["imported_manifest_summary"].get(
        "full_carrier_totalized"
    ) is not False:
        raise ValueError("snapshot promoted a complete cut to a full carrier")
    gates = normalize_gates(snapshot["gate_projection"])
    validate_routes(snapshot["route_universe"])

    graph = {
        node: tuple(parents)
        for node, parents in snapshot["proof_dag"]["parents"].items()
    }
    topo_order(graph)
    validate_order(graph, snapshot["proof_dag"]["topological_order"])
    source_nodes = {
        record["node_id"]: record for record in source["nodes"]
    }
    h9_ancestors = ancestor_closure(graph, "H9.physical_registry")
    if any(
        source_nodes[ancestor]["gate"].split(".", 1)[0]
        in {"H2", "H3", "H4", "H5"}
        for ancestor in h9_ancestors
    ):
        raise ValueError("H9 is directly or indirectly arithmetic-dependent")
    expected_missing = recompute_first_missing(source)
    if snapshot["first_missing"] != expected_missing:
        raise ValueError("snapshot first-missing record is stale")
    if snapshot["first_missing"]["node_id"] != "H1.frontier_totalization":
        raise ValueError("snapshot first missing node drift")
    if snapshot["ordered_verdicts"] != ORDERED_VERDICTS:
        raise ValueError("verdict order drift")
    verdict = decide(
        gates,
        snapshot["endpoint"],
        snapshot["route_universe"],
    )
    if verdict != snapshot["current_verdict"]:
        raise ValueError("snapshot verdict is stale")
    if verdict != "NOT_TESTABLE":
        raise ValueError("unexpected current verdict")
    if endpoint_certified(snapshot["endpoint"]):
        raise ValueError("current snapshot falsely passes the endpoint")
    if any(snapshot["claim_boundary"].values()):
        raise ValueError("claim boundary contains a false positive")
    return {
        "snapshot_schema_fields": True,
        "source_manifest_hash_locked": True,
        "source_hash_integrity_semantics": True,
        "restricted_positive_arithmetic_shadow_scoped": True,
        "global_density_not_promoted_to_terminal_window": True,
        "gate_projection_exact": True,
        "proof_DAG_and_order_valid": True,
        "H9_transitively_arithmetic_independent": True,
        "cut_complete_not_full_carrier": True,
        "first_missing_frontier_totalization": True,
        "seven_verdict_order_fixed": True,
        "current_verdict_not_testable": True,
        "current_endpoint_not_passed": True,
        "claim_boundary_negative": True,
    }


def sample_gate(
    status: str,
    evidence: str,
    structural: bool,
    scope_match: bool = True,
) -> dict[str, Any]:
    return {
        "status": status,
        "evidence": evidence,
        "structural": structural,
        "scope_match": scope_match,
        "source_node": "sample",
    }


def scenario_gates(
    records: list[tuple[str, str, bool]],
) -> dict[str, dict[str, Any]]:
    if len(records) > 9:
        raise ValueError("too many scenario gate records")
    padded = list(records)
    while len(padded) < 9:
        padded.append(("PROVED", "L1", True))
    return {
        f"H{index + 1}": sample_gate(*record)
        for index, record in enumerate(padded)
    }


def scenario_routes(
    *,
    stopped_r1: bool = False,
    stopped_r2: bool = False,
    alternative: str | None = None,
) -> dict[str, Any]:
    return {
        "routes": ["r1", "r2"],
        "selected_route": "r1",
        "typed_alternative": alternative,
        "stops": {
            "r1": {
                "stopped": stopped_r1,
                "source_export": "theorem-r1" if stopped_r1 else None,
                "scope_id": "scope",
                "carrier_id": "carrier-r1",
            },
            "r2": {
                "stopped": stopped_r2,
                "source_export": "theorem-r2" if stopped_r2 else None,
                "scope_id": "scope",
                "carrier_id": "carrier-r2",
            },
        },
    }


def endpoint_sample(state: str) -> dict[str, Any]:
    if state == "STRICT_PASS":
        return {
            "state": state,
            "strict_slack": {"numerator": 1, "denominator": 2000},
            "lambda_phys_upper": {"numerator": 1, "denominator": 500},
        }
    return {
        "state": state,
        "strict_slack": None,
        "lambda_phys_upper": (
            None if state == "INCOMPLETE"
            else {"numerator": 1, "denominator": 300}
        ),
    }


def scenario_regressions() -> dict[str, Any]:
    all_proved = scenario_gates([("PROVED", "L1", True)])
    ordinary_open = scenario_gates(
        [
            ("PROVED", "L1", True),
            ("OPEN", "L1_TARGET", True),
            ("OPEN", "L2_TARGET_POSITIVE", False),
        ]
    )
    missing = scenario_gates(
        [
            ("NOT_TESTABLE", "L1_TARGET", True),
            ("OPEN", "L2_TARGET_POSITIVE", False),
        ]
    )
    arithmetic_frontier = scenario_gates(
        [
            ("PROVED", "L1", True),
            ("OPEN", "L2_TARGET_POSITIVE", False),
        ]
    )
    refuted = scenario_gates(
        [
            ("REFUTED", "L2_NEGATIVE", False),
            ("OPEN", "L2_TARGET_POSITIVE", False),
        ]
    )

    scenarios = {
        "GO": decide(
            all_proved,
            endpoint_sample("STRICT_PASS"),
            scenario_routes(),
        ),
        "ARCHITECTURE_INFEASIBLE": decide(
            ordinary_open,
            endpoint_sample("INCOMPLETE"),
            scenario_routes(stopped_r1=True, stopped_r2=True),
        ),
        "REROUTE": decide(
            refuted,
            endpoint_sample("INCOMPLETE"),
            scenario_routes(stopped_r1=True, alternative="r2"),
        ),
        "STOP_ROUTE": decide(
            refuted,
            endpoint_sample("INCOMPLETE"),
            scenario_routes(stopped_r1=True),
        ),
        "NOT_TESTABLE": decide(
            missing,
            endpoint_sample("INCOMPLETE"),
            scenario_routes(),
        ),
        "ARITHMETIC_FRONTIER": decide(
            arithmetic_frontier,
            endpoint_sample("STRICT_PASS"),
            scenario_routes(),
        ),
        "OPEN": decide(
            ordinary_open,
            endpoint_sample("NO_PASS_CERTIFICATE"),
            scenario_routes(),
        ),
    }
    if any(key != value for key, value in scenarios.items()):
        raise ValueError("one or more verdict scenarios are unreachable")

    invalid_snapshot_rejected = False
    invalid_routes = scenario_routes()
    invalid_routes["selected_route"] = "outside"
    try:
        decide(all_proved, endpoint_sample("STRICT_PASS"), invalid_routes)
    except ValueError:
        invalid_snapshot_rejected = True

    conditional_frontier = scenario_gates(
        [
            ("PROVED", "L1", True),
            ("CONDITIONAL", "L2_TARGET_POSITIVE", False),
        ]
    )
    conditional_frontier_rejected = (
        decide(
            conditional_frontier,
            endpoint_sample("STRICT_PASS"),
            scenario_routes(),
        )
        != "ARITHMETIC_FRONTIER"
    )

    frozen_frontier = scenario_gates(
        [
            ("PROVED", "L1", True),
            ("OPEN", "FROZEN_LOG_SHADOW", False),
        ]
    )
    frozen_frontier_rejected = (
        decide(
            frozen_frontier,
            endpoint_sample("STRICT_PASS"),
            scenario_routes(),
        )
        != "ARITHMETIC_FRONTIER"
    )

    refuted_frontier_rejected = (
        decide(
            refuted,
            endpoint_sample("STRICT_PASS"),
            scenario_routes(),
        )
        != "ARITHMETIC_FRONTIER"
    )

    incomplete_cover = scenario_routes(stopped_r1=True)
    incomplete_route_cover_rejected = not stop_cover_valid(incomplete_cover)

    upper_failure_is_not_stop = (
        decide(
            all_proved,
            endpoint_sample("NO_PASS_CERTIFICATE"),
            scenario_routes(),
        )
        == "OPEN"
    )

    return {
        "outcomes": scenarios,
        "invalid_snapshot_rejected": invalid_snapshot_rejected,
        "conditional_frontier_rejected": conditional_frontier_rejected,
        "frozen_frontier_rejected": frozen_frontier_rejected,
        "refuted_frontier_rejected": refuted_frontier_rejected,
        "incomplete_route_cover_rejected": incomplete_route_cover_rejected,
        "upper_failure_is_not_stop": upper_failure_is_not_stop,
    }


def build_audit(
    snapshot: dict[str, Any],
    snapshot_rendered: str,
    source_rendered: str,
) -> dict[str, Any]:
    checks = validate_snapshot(snapshot, source_rendered)
    scenarios = scenario_regressions()
    scenario_checks = {
        key: value
        for key, value in scenarios.items()
        if key != "outcomes"
    }
    status = all(checks.values()) and all(scenario_checks.values())
    return {
        "schema": "tpc-142-mvp4-route-audit-v1",
        "status": "PASS" if status else "FAIL",
        "snapshot_sha256": sha256_bytes(
            snapshot_rendered.encode("utf-8")
        ),
        "checks": checks,
        "scenario_checks": scenario_checks,
        "scenario_verdicts": scenarios["outcomes"],
        "current_verdict": snapshot["current_verdict"],
        "first_missing": snapshot["first_missing"],
        "claim_boundary": snapshot["claim_boundary"],
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--check",
        action="store_true",
        help="compare both committed JSON artifacts without writing",
    )
    args = parser.parse_args()

    source, source_rendered = load_source_manifest()
    snapshot = build_snapshot(source, source_rendered)
    snapshot_rendered = canonical_json(snapshot)
    audit = build_audit(snapshot, snapshot_rendered, source_rendered)
    audit_rendered = canonical_json(audit)

    if args.check:
        expected = {
            SNAPSHOT_PATH: snapshot_rendered,
            AUDIT_PATH: audit_rendered,
        }
        for path, rendered in expected.items():
            if not path.is_file() or path.read_text(encoding="utf-8") != rendered:
                raise SystemExit(f"certificate mismatch: {path.name}")
    else:
        SNAPSHOT_PATH.write_text(snapshot_rendered, encoding="utf-8")
        AUDIT_PATH.write_text(audit_rendered, encoding="utf-8")

    print(audit_rendered, end="")
    if audit["status"] != "PASS":
        raise SystemExit(1)


if __name__ == "__main__":
    main()
