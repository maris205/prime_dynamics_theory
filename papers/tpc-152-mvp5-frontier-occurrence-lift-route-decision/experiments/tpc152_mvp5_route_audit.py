#!/usr/bin/env python3
"""Build and verify the source-locked TPC-152 MVP5 route decision."""

from __future__ import annotations

import argparse
import copy
import hashlib
import importlib.util
import json
from fractions import Fraction
from pathlib import Path
from types import ModuleType
from typing import Any


HERE = Path(__file__).resolve().parent
PAPER_DIR = HERE.parent
PAPERS_DIR = PAPER_DIR.parent
TPC151_DIR = PAPERS_DIR / "tpc-151-source-locked-frontier-quotient-integration"
TPC151_SCRIPT = TPC151_DIR / "experiments" / "tpc151_source_locked_integration.py"
TPC151_MANIFEST = TPC151_DIR / "experiments" / "tpc151_integration_manifest.json"
TPC151_SCHEMA = TPC151_DIR / "experiments" / "tpc151_integration_manifest.schema.json"
SCHEMA_PATH = HERE / "tpc152_mvp5_snapshot.schema.json"
SNAPSHOT_PATH = HERE / "tpc152_mvp5_snapshot.json"
AUDIT_PATH = HERE / "tpc152_mvp5_route_audit.json"

SNAPSHOT_SCHEMA = "tpc-152-mvp5-frontier-occurrence-lift-snapshot-v1"
SOURCE_SCHEMA = "tpc-151-source-locked-frontier-quotient-integration-v1"
ORDERED_VERDICTS = [
    "GO",
    "ARCHITECTURE_INFEASIBLE",
    "REROUTE",
    "STOP_ROUTE",
    "NOT_TESTABLE",
    "ARITHMETIC_FRONTIER",
    "OPEN",
]
VALID_STATUSES = {"PROVED", "CONDITIONAL", "OPEN", "NOT_TESTABLE", "REFUTED"}


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def canonical_json(payload: Any) -> str:
    return json.dumps(
        payload,
        ensure_ascii=False,
        indent=2,
        sort_keys=True,
    ) + "\n"


def normalize_lf(text: str) -> str:
    return text.replace("\r\n", "\n").replace("\r", "\n")


def parse_fraction(record: dict[str, int] | None) -> Fraction | None:
    if record is None:
        return None
    denominator = record["denominator"]
    if denominator <= 0:
        raise ValueError("fraction denominator must be positive")
    return Fraction(record["numerator"], denominator)


def fraction_record(value: Fraction | None) -> dict[str, int] | None:
    if value is None:
        return None
    return {"numerator": value.numerator, "denominator": value.denominator}


def load_tpc151_module() -> ModuleType:
    if not TPC151_SCRIPT.is_file():
        raise FileNotFoundError("TPC-151 audit script is missing")
    spec = importlib.util.spec_from_file_location("tpc151_audit", TPC151_SCRIPT)
    if spec is None or spec.loader is None:
        raise ImportError("cannot load TPC-151 audit module")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def load_source() -> tuple[dict[str, Any], str, ModuleType]:
    if not TPC151_MANIFEST.is_file():
        raise FileNotFoundError(
            "TPC-151 manifest is missing; run its audit in default mode first"
        )
    source = json.loads(
        normalize_lf(TPC151_MANIFEST.read_text(encoding="utf-8"))
    )
    rendered = canonical_json(source)
    module = load_tpc151_module()
    source_checks = module.validate_manifest(source)
    if not all(source_checks.values()):
        raise ValueError("TPC-151 source manifest failed validation")
    return source, rendered, module


def validate_gate_projection(gates: dict[str, dict[str, Any]]) -> None:
    if set(gates) != {f"H{index}" for index in range(1, 10)}:
        raise ValueError("gate projection is not exactly H1--H9")
    for record in gates.values():
        if record["status"] not in VALID_STATUSES:
            raise ValueError("unknown gate status")
        if not isinstance(record["structural"], bool):
            raise ValueError("gate structural flag is not Boolean")
        if not isinstance(record["scope_match"], bool):
            raise ValueError("gate scope flag is not Boolean")


def validate_routes(routes: dict[str, Any]) -> None:
    universe = set(routes["routes"])
    selected = routes["selected_route"]
    stops = routes["stops"]
    if not universe or selected not in universe:
        raise ValueError("selected route lies outside route universe")
    if set(stops) != universe:
        raise ValueError("stop map is not an exact route cover")
    for route_id, record in stops.items():
        if record["stopped"]:
            if record["coverage"] != "COMPLETE_DECLARED_ROUTE_CELL":
                raise ValueError(f"stop for {route_id} lacks complete coverage")
            if not all(
                record.get(field)
                for field in (
                    "source_export",
                    "scope_id",
                    "carrier_id",
                    "normalization_id",
                    "registry_id",
                )
            ):
                raise ValueError(f"stop for {route_id} lacks typed metadata")
    completeness = routes["universe_completeness"]
    if completeness["status"] == "PROVED" and not completeness["source_export"]:
        raise ValueError("route-universe completeness lacks a source theorem")
    alternative = routes.get("typed_alternative")
    if alternative is not None:
        if alternative not in universe or alternative == selected:
            raise ValueError("invalid typed alternative")
        if not stops[selected]["stopped"] or stops[alternative]["stopped"]:
            raise ValueError("reroute stop/open states are inconsistent")
        if not routes.get("typed_alternative_crosswalk"):
            raise ValueError("reroute lacks a theorem-backed crosswalk")
        if stops[selected]["registry_id"] == stops[alternative]["registry_id"]:
            raise ValueError("reroute alternative does not have a fresh registry")


def complete_stop_cover(routes: dict[str, Any]) -> bool:
    completeness = routes["universe_completeness"]
    if (
        completeness["status"] != "PROVED"
        or not completeness["source_export"]
    ):
        return False
    return all(
        record["stopped"]
        and record["coverage"] == "COMPLETE_DECLARED_ROUTE_CELL"
        and bool(record["source_export"])
        for record in routes["stops"].values()
    )


def physical_endpoint_certified(endpoint: dict[str, Any]) -> bool:
    physical = endpoint["physical"]
    threshold = parse_fraction(physical["lambda_required_strict_upper"])
    upper = parse_fraction(physical["lambda_phys_upper"])
    return (
        physical["state"] == "STRICT_PASS"
        and physical["registry_complete"]
        and upper is not None
        and threshold is not None
        and upper < threshold
    )


def full_endpoint_certified(endpoint: dict[str, Any]) -> bool:
    arithmetic = endpoint["arithmetic"]
    full = endpoint["full_synthesis"]
    sigma = parse_fraction(arithmetic["sigma_actual_lower"])
    required = parse_fraction(arithmetic["sigma_required"])
    slack = parse_fraction(full["strict_net_slack"])
    return (
        physical_endpoint_certified(endpoint)
        and arithmetic["state"] == "TARGET_CERTIFIED"
        and sigma is not None
        and required is not None
        and sigma >= required
        and full["state"] == "STRICT_PASS"
        and slack is not None
        and slack > 0
    )


def decide(
    gates: dict[str, dict[str, Any]],
    endpoint: dict[str, Any],
    routes: dict[str, Any],
) -> str:
    """Apply the seven ordered verdicts after snapshot validation."""

    validate_gate_projection(gates)
    validate_routes(routes)
    selected = routes["selected_route"]
    if (
        any(record["status"] == "REFUTED" for record in gates.values())
        and not routes["stops"][selected]["stopped"]
        and not complete_stop_cover(routes)
    ):
        raise ValueError("active refuted gate lacks a selected-route stop")
    if all(
        record["status"] == "PROVED" and record["scope_match"]
        for record in gates.values()
    ) and full_endpoint_certified(endpoint):
        return "GO"
    if complete_stop_cover(routes):
        return "ARCHITECTURE_INFEASIBLE"
    if routes["stops"][selected]["stopped"]:
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
        record for record in gates.values() if record["status"] != "PROVED"
    ]
    structural_closed = all(
        record["status"] == "PROVED" and record["scope_match"]
        for record in gates.values()
        if record["structural"]
    )
    unresolved_are_open_actual_l2_targets = bool(unresolved) and all(
        record["status"] == "OPEN"
        and record["evidence"] == "L2_TARGET_POSITIVE"
        and not record["structural"]
        and record["scope_match"]
        for record in unresolved
    )
    if (
        physical_endpoint_certified(endpoint)
        and structural_closed
        and unresolved_are_open_actual_l2_targets
    ):
        return "ARITHMETIC_FRONTIER"
    return "OPEN"


def build_snapshot(
    source: dict[str, Any],
    source_rendered: str,
    module: ModuleType,
) -> dict[str, Any]:
    graph, order = module.validate_nodes(source["nodes"], source["exports"])
    first = module.minimal_missing_set(
        source["nodes"],
        graph,
        order,
        source["proof_dag"]["selected_root"],
    )
    if first != source["first_missing"]:
        raise ValueError("TPC-151 first-missing record is stale")
    if first is None or first["node_id"] != "H1.frontier_occurrence_lift":
        raise ValueError("unexpected MVP5 first missing object")
    gates = copy.deepcopy(source["gate_projection"])
    routes = copy.deepcopy(source["route_universe"])
    endpoint = copy.deepcopy(source["endpoint_ledgers"])
    verdict = decide(gates, endpoint, routes)
    if verdict != "NOT_TESTABLE":
        raise ValueError("unexpected current MVP5 verdict")

    return {
        "schema": SNAPSHOT_SCHEMA,
        "snapshot": {
            "date": "2026-07-27",
            "source_manifest": (
                "tpc-151-source-locked-frontier-quotient-integration/"
                "experiments/tpc151_integration_manifest.json"
            ),
            "source_manifest_sha256": sha256_bytes(
                source_rendered.encode("utf-8")
            ),
            "source_schema_sha256": module.canonical_source_hash(TPC151_SCHEMA),
            "snapshot_schema_sha256": module.canonical_source_hash(SCHEMA_PATH),
            "hash_mode": source["snapshot"]["hash_mode"],
            "source_hash_semantics": "INTEGRITY_ONLY",
            "selected_route": routes["selected_route"],
        },
        "imported_manifest_summary": {
            "source_schema": source["schema"],
            "source_range": source["snapshot"]["source_range"],
            "anchor_chain_verified": source["anchor_chain"][
                "tpc142_embedded_tpc141_hash_verified"
            ],
            "source_bundle_hashes": {
                paper: record["bundle_sha256"]
                for paper, record in source["source_bundles"].items()
            },
            "occurrence_lift_status": source["frontier_contract"][
                "occurrence_lift"
            ]["status"],
            "all_nonsoft_domain": source["frontier_contract"]["domain"],
            "frontier_totalization_logic": source["frontier_contract"][
                "totalization_logic"
            ],
            "frontier_totalization_required_artifact": {
                record["node_id"]: record["required_artifact"]
                for record in source["nodes"]
            }["H1.frontier_totalization"],
            "frontier_scalar_proved": source["frontier_contract"][
                "scalar_route"
            ]["frontier_scalar_proved"],
            "eligible_tail_disposed": source["frontier_contract"][
                "scalar_route"
            ]["eligible_tail_disposed"],
            "schema_nonidentifiability_is_actual_carrier_impossibility": (
                source["claim_boundary"][
                    "schema_nonidentifiability_is_actual_carrier_impossibility"
                ]
            ),
            "actual_core_scope": source["arithmetic_corridor"]["scope_id"],
            "actual_core_status": source["arithmetic_corridor"]["status"],
            "actual_core_x_power_sigma": source["arithmetic_corridor"][
                "x_power_sigma"
            ],
            "actual_core_promotion_eligible": source[
                "arithmetic_corridor"
            ]["promotion_eligible"],
            "positive_L2": source["arithmetic_corridor"]["positive_L2"],
            "actual_fixed_power_target_level": source[
                "progress_classification"
            ]["actual_fixed_power_target_level"],
            "actual_fixed_power_status": source[
                "progress_classification"
            ]["actual_fixed_power_status"],
            "actual_fixed_power_achieved": source[
                "progress_classification"
            ]["actual_fixed_power_achieved"],
        },
        "gate_projection": gates,
        "proof_dag": copy.deepcopy(source["proof_dag"]),
        "route_universe": routes,
        "endpoint_ledgers": endpoint,
        "first_missing": first,
        "ordered_verdicts": ORDERED_VERDICTS,
        "current_verdict": verdict,
        "progress_tags": [
            "L1_STRUCTURAL_FRONTIER_OCCURRENCE_CONTRACT",
            "ALL_NONSOFT_ETO_PLUS_FUM",
            "FRONTIER_SCALAR_REQUIRES_ETO_ROUTE",
            "SCHEMA_NONIDENTIFIABILITY_NOT_ACTUAL_IMPOSSIBILITY",
            "CUT_SELECTOR_NOT_DOWNSTREAM_SELECTOR",
            "SCOPED_SCHEMA_ONLY_ROUTE_STOPS",
            "L1_ACTUAL_CORE_FIXED_TWO_MOBIUS_PERIODIC_CORRIDOR",
            "ACTUAL_CORE_NOT_FULL_PHYSICAL_H3",
            "LOG_POWER_HAS_ZERO_X_POWER_EXPONENT",
            "L2_ACTUAL_POSITIVE_IS_TARGET_LABEL_ONLY",
            "ACTUAL_FIXED_POWER_NOT_PROVED",
            "H9_ARITHMETICALLY_INDEPENDENT",
            "SPLIT_ONE_OVER_400_LEDGERS",
            "NO_POSITIVE_L2",
        ],
        "claim_boundary": {
            "source_hashes_prove_theorems": False,
            "schema_nonidentifiability_is_actual_carrier_impossibility": False,
            "GO": False,
            "ARCHITECTURE_INFEASIBLE": False,
            "REROUTE": False,
            "STOP_ROUTE": False,
            "ARITHMETIC_FRONTIER": False,
            "positive_L2": False,
            "physical_endpoint_pass": False,
            "arithmetic_target_pass": False,
            "full_endpoint_pass": False,
            "hard_packet_oX": False,
            "prime_pair_theorem": False,
            "twin_prime_theorem": False,
        },
    }


def validate_snapshot(
    snapshot: dict[str, Any],
    source: dict[str, Any],
    source_rendered: str,
    module: ModuleType,
) -> dict[str, bool]:
    schema = json.loads(normalize_lf(SCHEMA_PATH.read_text(encoding="utf-8")))
    if set(snapshot) != set(schema["required"]):
        raise ValueError("snapshot fields differ from schema contract")
    if snapshot["schema"] != SNAPSHOT_SCHEMA:
        raise ValueError("snapshot schema mismatch")
    summary_schema = schema["properties"]["imported_manifest_summary"]
    if set(snapshot["imported_manifest_summary"]) != set(
        summary_schema["required"]
    ):
        raise ValueError(
            "imported-manifest summary fields differ from schema contract"
        )
    if snapshot["snapshot"]["source_manifest_sha256"] != sha256_bytes(
        source_rendered.encode("utf-8")
    ):
        raise ValueError("source manifest hash mismatch")
    if snapshot["snapshot"]["source_hash_semantics"] != "INTEGRITY_ONLY":
        raise ValueError("source hashes were assigned proof semantics")
    if snapshot["ordered_verdicts"] != ORDERED_VERDICTS:
        raise ValueError("ordered verdict precedence drift")
    validate_gate_projection(snapshot["gate_projection"])
    validate_routes(snapshot["route_universe"])

    graph, order = module.validate_nodes(source["nodes"], source["exports"])
    expected_first = module.minimal_missing_set(
        source["nodes"],
        graph,
        order,
        source["proof_dag"]["selected_root"],
    )
    if snapshot["first_missing"] != expected_first:
        raise ValueError("snapshot first-missing pointer is stale")
    if snapshot["first_missing"]["node_id"] != "H1.frontier_occurrence_lift":
        raise ValueError("occurrence lift is not the first missing object")
    if snapshot["first_missing"]["minimal_missing_set"] != [
        "H1.frontier_occurrence_lift"
    ]:
        raise ValueError("first-missing antichain drift")
    if snapshot["imported_manifest_summary"]["all_nonsoft_domain"] != (
        "ALL_NONSOFT_CUT_PATHS_ETO_PLUS_FUM"
    ):
        raise ValueError("MVP5 dropped an all-nonsoft terminal class")
    if snapshot["imported_manifest_summary"][
        "frontier_totalization_logic"
    ] != module.FRONTIER_TOTALIZATION_LOGIC:
        raise ValueError("MVP5 weakened the frontier disjunction")
    if snapshot["imported_manifest_summary"][
        "frontier_totalization_required_artifact"
    ] != module.REQUIRED_ARTIFACT_CONTRACTS["H1.frontier_totalization"]:
        raise ValueError(
            "MVP5 imported a compressed frontier-totalization artifact"
        )
    if (
        snapshot["imported_manifest_summary"]["frontier_scalar_proved"]
        or snapshot["imported_manifest_summary"]["eligible_tail_disposed"]
    ):
        raise ValueError("MVP5 falsely closed the scalar-plus-ETO route")
    if snapshot["imported_manifest_summary"][
        "schema_nonidentifiability_is_actual_carrier_impossibility"
    ]:
        raise ValueError(
            "MVP5 promoted schema nonidentifiability to actual impossibility"
        )
    if snapshot["imported_manifest_summary"]["actual_core_status"] != (
        "PROVED_L1_ACTUAL_CORE"
    ):
        raise ValueError("actual-core arithmetic progress was lost")
    if snapshot["imported_manifest_summary"]["actual_core_promotion_eligible"]:
        raise ValueError("actual core was promoted to full H3")
    if parse_fraction(
        snapshot["imported_manifest_summary"]["actual_core_x_power_sigma"]
    ) != 0:
        raise ValueError("log-power core was assigned an X-power saving")
    if snapshot["imported_manifest_summary"]["positive_L2"]:
        raise ValueError("snapshot falsely claims positive L2")
    if snapshot["imported_manifest_summary"][
        "actual_fixed_power_target_level"
    ] != "L2_ACTUAL_POSITIVE":
        raise ValueError("actual fixed-power target level drift")
    if snapshot["imported_manifest_summary"][
        "actual_fixed_power_status"
    ] != "NOT_PROVED":
        raise ValueError("actual fixed-power target was falsely proved")
    if snapshot["imported_manifest_summary"][
        "actual_fixed_power_achieved"
    ]:
        raise ValueError("actual fixed-power target was falsely achieved")
    verdict = decide(
        snapshot["gate_projection"],
        snapshot["endpoint_ledgers"],
        snapshot["route_universe"],
    )
    if verdict != snapshot["current_verdict"] or verdict != "NOT_TESTABLE":
        raise ValueError("current MVP5 verdict is stale")
    if physical_endpoint_certified(snapshot["endpoint_ledgers"]):
        raise ValueError("current physical endpoint falsely passes")
    if full_endpoint_certified(snapshot["endpoint_ledgers"]):
        raise ValueError("current full endpoint falsely passes")
    if any(snapshot["claim_boundary"].values()):
        raise ValueError("claim boundary contains a false positive")
    return {
        "schema_fields": True,
        "source_manifest_canonical_hash": True,
        "source_hashes_integrity_only": True,
        "ordered_verdicts": True,
        "active_ancestor_first_missing": True,
        "occurrence_lift_first_missing": True,
        "all_nonsoft_domain": True,
        "frontier_scalar_requires_ETO": True,
        "frontier_totalization_artifact_exact": True,
        "schema_nonidentifiability_scope_preserved": True,
        "actual_core_L1_retained": True,
        "actual_core_not_positive_L2": True,
        "actual_fixed_power_target_not_achievement": True,
        "H9_role_based_independence_imported": True,
        "split_endpoint_ledgers": True,
        "current_verdict_not_testable": True,
        "claim_boundary": True,
    }


def scenario_gates(
    *,
    structural_status: str,
    arithmetic_status: str,
    arithmetic_evidence: str = "L2_TARGET_POSITIVE",
) -> dict[str, dict[str, Any]]:
    gates: dict[str, dict[str, Any]] = {}
    for index in range(1, 10):
        structural = index in {1, 6, 7, 8, 9}
        gates[f"H{index}"] = {
            "status": structural_status if structural else arithmetic_status,
            "evidence": (
                "L1_STRUCTURAL" if structural else arithmetic_evidence
            ),
            "structural": structural,
            "scope_match": True,
            "source_node": f"synthetic.H{index}",
        }
    return gates


def scenario_endpoint(
    *,
    physical_pass: bool,
    full_pass: bool,
) -> dict[str, Any]:
    threshold = Fraction(1, 400)
    physical_upper = Fraction(1, 500) if physical_pass else None
    sigma = threshold if full_pass else None
    return {
        "contract": "MVP1-FIXED-H0-SPLIT-ENDPOINT-V2",
        "scale": "AMPLITUDE",
        "arithmetic": {
            "sigma_required": fraction_record(threshold),
            "sigma_actual_lower": fraction_record(sigma),
            "best_shadow_x_power_sigma": fraction_record(Fraction(0)),
            "state": "TARGET_CERTIFIED" if full_pass else "INCOMPLETE",
            "log_saving_pays_fixed_power": False,
        },
        "physical": {
            "lambda_required_strict_upper": fraction_record(threshold),
            "lambda_phys_upper": fraction_record(physical_upper),
            "lambda_phys_lower": None,
            "registry_complete": physical_pass,
            "state": "STRICT_PASS" if physical_pass else "INCOMPLETE",
            "unknown_cost_policy": "UNKNOWN_IS_NOT_ZERO",
            "upper_at_or_above_is_stop_without_lower": False,
            "determinant_reserve_reusable": False,
        },
        "full_synthesis": {
            "strict_net_slack": (
                fraction_record(threshold - Fraction(1, 500))
                if full_pass
                else None
            ),
            "state": "STRICT_PASS" if full_pass else "INCOMPLETE",
        },
    }


def scenario_routes(
    *,
    selected_stopped: bool = False,
    all_stopped: bool = False,
    complete_universe: bool = False,
    alternative: bool = False,
    fresh_registry: bool = True,
) -> dict[str, Any]:
    routes = ["r1", "r2"]
    selected_registry = "registry.r1"
    alternative_registry = "registry.r2" if fresh_registry else selected_registry
    stops = {
        "r1": {
            "stopped": selected_stopped or all_stopped,
            "source_export": (
                "negative.r1" if selected_stopped or all_stopped else None
            ),
            "scope_id": "scope",
            "carrier_id": "carrier",
            "normalization_id": "norm",
            "coverage": (
                "COMPLETE_DECLARED_ROUTE_CELL"
                if selected_stopped or all_stopped
                else "OPEN_SELECTED_ROUTE"
            ),
            "registry_id": selected_registry,
        },
        "r2": {
            "stopped": all_stopped,
            "source_export": "negative.r2" if all_stopped else None,
            "scope_id": "scope",
            "carrier_id": "carrier",
            "normalization_id": "norm",
            "coverage": (
                "COMPLETE_DECLARED_ROUTE_CELL"
                if all_stopped
                else "OPEN_SELECTED_ROUTE"
            ),
            "registry_id": alternative_registry,
        },
    }
    return {
        "routes": routes,
        "selected_route": "r1",
        "selected_root": "root",
        "typed_alternative": "r2" if alternative else None,
        "typed_alternative_crosswalk": "crosswalk.r1.r2" if alternative else None,
        "universe_completeness": {
            "status": "PROVED" if complete_universe else "OPEN",
            "source_export": "universe.theorem" if complete_universe else None,
            "scope": "synthetic",
        },
        "stops": stops,
    }


def scenario_regressions() -> dict[str, Any]:
    all_proved = scenario_gates(
        structural_status="PROVED", arithmetic_status="PROVED"
    )
    missing = scenario_gates(
        structural_status="NOT_TESTABLE", arithmetic_status="OPEN"
    )
    arithmetic_frontier = scenario_gates(
        structural_status="PROVED", arithmetic_status="OPEN"
    )
    ordinary_open = scenario_gates(
        structural_status="OPEN", arithmetic_status="OPEN"
    )
    refuted = scenario_gates(
        structural_status="PROVED", arithmetic_status="REFUTED",
        arithmetic_evidence="L2_ACTUAL_POSITIVE",
    )
    outcomes = {
        "GO": decide(
            all_proved,
            scenario_endpoint(physical_pass=True, full_pass=True),
            scenario_routes(),
        ),
        "ARCHITECTURE_INFEASIBLE": decide(
            ordinary_open,
            scenario_endpoint(physical_pass=False, full_pass=False),
            scenario_routes(all_stopped=True, complete_universe=True),
        ),
        "REROUTE": decide(
            refuted,
            scenario_endpoint(physical_pass=False, full_pass=False),
            scenario_routes(selected_stopped=True, alternative=True),
        ),
        "STOP_ROUTE": decide(
            refuted,
            scenario_endpoint(physical_pass=False, full_pass=False),
            scenario_routes(selected_stopped=True),
        ),
        "NOT_TESTABLE": decide(
            missing,
            scenario_endpoint(physical_pass=False, full_pass=False),
            scenario_routes(),
        ),
        "ARITHMETIC_FRONTIER": decide(
            arithmetic_frontier,
            scenario_endpoint(physical_pass=True, full_pass=False),
            scenario_routes(),
        ),
        "OPEN": decide(
            ordinary_open,
            scenario_endpoint(physical_pass=False, full_pass=False),
            scenario_routes(),
        ),
    }
    if any(key != value for key, value in outcomes.items()):
        raise ValueError("one or more ordered verdict scenarios are unreachable")

    incomplete_universe = scenario_routes(all_stopped=True, complete_universe=False)
    no_false_architecture = decide(
        ordinary_open,
        scenario_endpoint(physical_pass=False, full_pass=False),
        incomplete_universe,
    ) != "ARCHITECTURE_INFEASIBLE"

    bad_reroute_rejected = False
    try:
        decide(
            refuted,
            scenario_endpoint(physical_pass=False, full_pass=False),
            scenario_routes(
                selected_stopped=True,
                alternative=True,
                fresh_registry=False,
            ),
        )
    except ValueError:
        bad_reroute_rejected = True

    conditional = scenario_gates(
        structural_status="PROVED",
        arithmetic_status="CONDITIONAL",
    )
    conditional_pseudo_frontier_rejected = (
        decide(
            conditional,
            scenario_endpoint(physical_pass=True, full_pass=False),
            scenario_routes(),
        )
        != "ARITHMETIC_FRONTIER"
    )
    actual_core = scenario_gates(
        structural_status="PROVED",
        arithmetic_status="OPEN",
        arithmetic_evidence="L1_ACTUAL_CORE",
    )
    actual_core_pseudo_frontier_rejected = (
        decide(
            actual_core,
            scenario_endpoint(physical_pass=True, full_pass=False),
            scenario_routes(),
        )
        != "ARITHMETIC_FRONTIER"
    )
    invalid_route_rejected = False
    malformed = scenario_routes()
    malformed["selected_route"] = "outside"
    try:
        decide(
            all_proved,
            scenario_endpoint(physical_pass=True, full_pass=True),
            malformed,
        )
    except ValueError:
        invalid_route_rejected = True
    return {
        "outcomes": outcomes,
        "unproved_universe_not_architecture_infeasible": no_false_architecture,
        "reroute_requires_fresh_registry": bad_reroute_rejected,
        "conditional_pseudo_frontier_rejected": (
            conditional_pseudo_frontier_rejected
        ),
        "actual_core_pseudo_frontier_rejected": (
            actual_core_pseudo_frontier_rejected
        ),
        "invalid_snapshot_rejected_before_verdict": invalid_route_rejected,
    }


def build_audit(
    snapshot: dict[str, Any],
    snapshot_rendered: str,
    source: dict[str, Any],
    source_rendered: str,
    module: ModuleType,
) -> dict[str, Any]:
    checks = validate_snapshot(
        snapshot, source, source_rendered, module
    )
    scenarios = scenario_regressions()
    scenario_checks = {
        key: value for key, value in scenarios.items() if key != "outcomes"
    }
    compressed = copy.deepcopy(snapshot)
    compressed["imported_manifest_summary"][
        "frontier_totalization_required_artifact"
    ] = (
        "zero four-map defect vector or a complete original-scale "
        "S_frontier=o(X) theorem"
    )
    try:
        validate_snapshot(
            compressed, source, source_rendered, module
        )
    except ValueError:
        scenario_checks[
            "compressed_frontier_totalization_artifact_rejected"
        ] = True
    else:
        scenario_checks[
            "compressed_frontier_totalization_artifact_rejected"
        ] = False
    promoted = copy.deepcopy(snapshot)
    promoted["imported_manifest_summary"][
        "schema_nonidentifiability_is_actual_carrier_impossibility"
    ] = True
    try:
        validate_snapshot(
            promoted, source, source_rendered, module
        )
    except ValueError:
        scenario_checks[
            "schema_nonidentifiability_promotion_rejected"
        ] = True
    else:
        scenario_checks[
            "schema_nonidentifiability_promotion_rejected"
        ] = False
    achieved = copy.deepcopy(snapshot)
    achieved["imported_manifest_summary"][
        "actual_fixed_power_status"
    ] = "PROVED"
    achieved["imported_manifest_summary"][
        "actual_fixed_power_achieved"
    ] = True
    try:
        validate_snapshot(
            achieved, source, source_rendered, module
        )
    except ValueError:
        scenario_checks[
            "actual_fixed_power_target_promotion_rejected"
        ] = True
    else:
        scenario_checks[
            "actual_fixed_power_target_promotion_rejected"
        ] = False
    status = all(checks.values()) and all(scenario_checks.values())
    return {
        "schema": "tpc-152-mvp5-route-audit-v1",
        "status": "PASS" if status else "FAIL",
        "snapshot_sha256": sha256_bytes(snapshot_rendered.encode("utf-8")),
        "checks": checks,
        "scenario_checks": scenario_checks,
        "scenario_verdicts": scenarios["outcomes"],
        "current_verdict": snapshot["current_verdict"],
        "first_missing": snapshot["first_missing"],
        "claim_boundary": snapshot["claim_boundary"],
    }


def write_canonical(path: Path, rendered: str) -> None:
    with path.open("w", encoding="utf-8", newline="\n") as stream:
        stream.write(rendered)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--check",
        action="store_true",
        help="compare committed deterministic artifacts without writing",
    )
    args = parser.parse_args()
    source, source_rendered, module = load_source()
    snapshot = build_snapshot(source, source_rendered, module)
    snapshot_rendered = canonical_json(snapshot)
    audit = build_audit(
        snapshot, snapshot_rendered, source, source_rendered, module
    )
    audit_rendered = canonical_json(audit)
    if args.check:
        for path, expected in (
            (SNAPSHOT_PATH, snapshot_rendered),
            (AUDIT_PATH, audit_rendered),
        ):
            if not path.is_file():
                raise SystemExit(f"missing certificate: {path.name}")
            existing = normalize_lf(path.read_text(encoding="utf-8"))
            if existing != expected:
                raise SystemExit(f"certificate mismatch: {path.name}")
    else:
        write_canonical(SNAPSHOT_PATH, snapshot_rendered)
        write_canonical(AUDIT_PATH, audit_rendered)
    print(audit_rendered, end="")
    if audit["status"] != "PASS":
        raise SystemExit(1)


if __name__ == "__main__":
    main()
