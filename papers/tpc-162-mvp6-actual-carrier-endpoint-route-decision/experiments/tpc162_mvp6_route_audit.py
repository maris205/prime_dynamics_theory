#!/usr/bin/env python3
"""Build and verify the source-locked TPC-162 MVP6 route decision."""

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
REPO_DIR = PAPERS_DIR.parent

TPC161_DIR = PAPERS_DIR / "tpc-161-source-locked-occurrence-return-integration"
TPC161_SCRIPT = TPC161_DIR / "experiments" / "tpc161_source_locked_integration.py"
TPC161_MANIFEST = (
    TPC161_DIR / "experiments" / "tpc161_occurrence_return_manifest.json"
)
TPC161_MANIFEST_SCHEMA = (
    TPC161_DIR / "experiments" / "tpc161_occurrence_return_manifest.schema.json"
)
TPC161_AUDIT = (
    TPC161_DIR / "experiments" / "tpc161_occurrence_return_audit.json"
)
TPC161_AUDIT_SCHEMA = (
    TPC161_DIR / "experiments" / "tpc161_occurrence_return_audit.schema.json"
)

TPC156_DIR = PAPERS_DIR / "tpc-156-h1-occurrence-crosswalk-route-decision"
TPC156_DECISION = (
    TPC156_DIR / "experiments" / "tpc156_h1_occurrence_decision.json"
)
TPC160_DIR = PAPERS_DIR / "tpc-160-exceptional-variation-abel-return"
TPC160_AUDIT = TPC160_DIR / "experiments" / "tpc160_abel_return_audit.json"

SNAPSHOT_SCHEMA = (
    PAPER_DIR / "schemas" / "tpc162-mvp6-snapshot-v1.schema.json"
)
AUDIT_SCHEMA = (
    PAPER_DIR / "schemas" / "tpc162-mvp6-route-audit-v1.schema.json"
)
SNAPSHOT_PATH = HERE / "tpc162_mvp6_snapshot.json"
AUDIT_PATH = HERE / "tpc162_mvp6_route_audit.json"
ROUTE_UNIVERSE_FIXTURE = (
    HERE / "fixtures" / "tpc162_route_universe_complete_fixture.json"
)
ROUTE_CROSSWALK_FIXTURE = (
    HERE / "fixtures" / "tpc162_r1_r2_crosswalk_fixture.json"
)

HASH_MODE = "CANONICAL_UTF8_LF_V2"
HASH_SEMANTICS = "INTEGRITY_ONLY"
SOURCE_LOCKED = "SOURCE_LOCKED"
SYNTHETIC_REACHABILITY = "SYNTHETIC_REACHABILITY"
SNAPSHOT_SCHEMA_ID = "tpc-162-mvp6-actual-carrier-endpoint-route-snapshot-v1"
AUDIT_SCHEMA_ID = "tpc-162-mvp6-route-audit-v1"
FIRST_MISSING = "H1.theorem_backed_occurrence_provenance_crosswalk"
SELECTED_ROUTE = "occurrence_augmented_map"
ORDERED_VERDICTS = [
    "GO",
    "ARCHITECTURE_INFEASIBLE",
    "REROUTE",
    "STOP_ROUTE",
    "NOT_TESTABLE",
    "ARITHMETIC_FRONTIER",
    "OPEN",
]
VALID_NODE_STATUSES = {
    "PROVED",
    "CONDITIONAL",
    "OPEN",
    "NOT_TESTABLE",
    "REFUTED",
}
TOP_LEVEL_SNAPSHOT_FIELDS = {
    "schema",
    "snapshot",
    "source_locks",
    "imported_state",
    "route_universe",
    "gate_projection",
    "typed_frontiers",
    "endpoint_ledger_v3",
    "next_forced_objects",
    "ordered_valid_verdicts",
    "current_verdict",
    "progress_classification",
    "claim_boundary",
}


def normalize_lf(text: str) -> str:
    return text.replace("\r\n", "\n").replace("\r", "\n")


def canonical_json(payload: Any) -> str:
    return json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True) + "\n"


def canonical_bytes(path: Path) -> bytes:
    text = normalize_lf(path.read_text(encoding="utf-8"))
    if path.suffix == ".json":
        text = canonical_json(json.loads(text))
    elif not text.endswith("\n"):
        text += "\n"
    return text.encode("utf-8")


def canonical_hash(path: Path) -> str:
    return hashlib.sha256(canonical_bytes(path)).hexdigest()


def rendered_hash(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def load_json(path: Path) -> dict[str, Any]:
    if not path.is_file():
        raise FileNotFoundError(f"missing source artifact: {path}")
    payload = json.loads(normalize_lf(path.read_text(encoding="utf-8")))
    if not isinstance(payload, dict):
        raise ValueError(f"source artifact is not an object: {path}")
    return payload


def assert_strict_schema_shape(schema: Any) -> None:
    if isinstance(schema, dict):
        if (
            schema.get("type") == "object"
            and schema.get("additionalProperties") is False
        ):
            properties = schema.get("properties")
            required = schema.get("required")
            if not isinstance(properties, dict) or not isinstance(required, list):
                raise ValueError("strict object schema lacks fields")
            if set(properties) != set(required):
                raise ValueError(
                    "strict object schema does not require exactly its properties"
                )
        for value in schema.values():
            assert_strict_schema_shape(value)
    elif isinstance(schema, list):
        for value in schema:
            assert_strict_schema_shape(value)


def repo_relative(path: Path) -> str:
    return path.relative_to(REPO_DIR).as_posix()


def source_lock(source_id: str, path: Path) -> dict[str, str]:
    return {
        "source_id": source_id,
        "path": repo_relative(path),
        "canonical_utf8_lf_sha256": canonical_hash(path),
        "hash_semantics": HASH_SEMANTICS,
    }


def source_record(path: Path) -> dict[str, Any]:
    payload = load_json(path)
    required = {
        "schema",
        "source_id",
        "evidence_kind",
        "claim_type",
        "scope_id",
        "from_route",
        "to_route",
        "statement",
        "proof_semantics",
    }
    if set(payload) != required:
        raise ValueError(f"classifier source fields drift: {path}")
    return {
        **payload,
        "path": repo_relative(path),
        "canonical_utf8_lf_sha256": canonical_hash(path),
    }


def locked_tpc156_stop_record() -> dict[str, Any]:
    return {
        "schema": "tpc-162-source-locked-route-claim-v1",
        "source_id": (
            "TPC156.H1.current_artifacts_only_canonical_actual_lift"
        ),
        "evidence_kind": "SOURCE_LOCKED_ROUTE_RESULT",
        "claim_type": "ROUTE_CELL_STOP",
        "scope_id": "CURRENT_ARTIFACTS_ONLY",
        "from_route": "current_schema_only_canonical_lift",
        "to_route": None,
        "statement": (
            "TPC-156 stops only the actual lift derived from current "
            "archive fields."
        ),
        "proof_semantics": "SCOPED_SOURCE_RESULT",
        "path": repo_relative(TPC156_DECISION),
        "canonical_utf8_lf_sha256": canonical_hash(TPC156_DECISION),
    }


def synthetic_stop_record(route_id: str) -> dict[str, Any]:
    return {
        "schema": "tpc-162-synthetic-route-stop-assumption-v1",
        "source_id": f"fixture.synthetic.stop.{route_id}",
        "evidence_kind": "SYNTHETIC_SCENARIO_ASSUMPTION",
        "claim_type": "ROUTE_CELL_STOP",
        "scope_id": "scope.actual",
        "from_route": route_id,
        "to_route": None,
        "statement": (
            "Assume this synthetic route cell is exactly stopped solely "
            "for classifier reachability testing."
        ),
        "proof_semantics": "NONE_SYNTHETIC_REACHABILITY_ONLY",
        "path": None,
        "canonical_utf8_lf_sha256": None,
    }


def validate_source_records(
    records: dict[str, Any],
    evidence_mode: str,
) -> None:
    if evidence_mode not in {SOURCE_LOCKED, SYNTHETIC_REACHABILITY}:
        raise ValueError("classifier evidence mode is invalid")
    if not isinstance(records, dict):
        raise ValueError("classifier source registry is not an object")
    expected_fields = {
        "schema",
        "source_id",
        "evidence_kind",
        "claim_type",
        "scope_id",
        "from_route",
        "to_route",
        "statement",
        "proof_semantics",
        "path",
        "canonical_utf8_lf_sha256",
    }
    for source_id, record in records.items():
        if not isinstance(source_id, str) or not source_id:
            raise ValueError("classifier source id is empty")
        if not isinstance(record, dict) or set(record) != expected_fields:
            raise ValueError(f"classifier source fields drift: {source_id}")
        if record["source_id"] != source_id:
            raise ValueError(f"classifier source key drift: {source_id}")
        kind = record["evidence_kind"]
        semantics = record["proof_semantics"]
        if evidence_mode == SOURCE_LOCKED:
            if kind == "SOURCE_LOCKED_ROUTE_RESULT":
                if (
                    record != locked_tpc156_stop_record()
                ):
                    raise ValueError(
                        f"source-locked route result drift: {source_id}"
                    )
                decision = load_json(TPC156_DECISION)
                route = decision.get("routes", {}).get(
                    "current_archive_only_actual_lift", {}
                )
                if (
                    not route.get("stopped")
                    or record["claim_type"] != "ROUTE_CELL_STOP"
                    or record["scope_id"] != "CURRENT_ARTIFACTS_ONLY"
                    or record["from_route"]
                    != "current_schema_only_canonical_lift"
                    or record["to_route"] is not None
                ):
                    raise ValueError(
                        "TPC-156 scoped-stop evidence does not match"
                    )
                continue
            if (
                kind != "THEOREM_SOURCE"
                or semantics != "PROVED_SOURCE_CLAIM"
            ):
                raise ValueError(
                    f"classifier source kind is incompatible with mode: {source_id}"
                )
        else:
            if kind == "SYNTHETIC_SCENARIO_ASSUMPTION":
                if (
                    semantics != "NONE_SYNTHETIC_REACHABILITY_ONLY"
                    or record["schema"]
                    != "tpc-162-synthetic-route-stop-assumption-v1"
                    or record["claim_type"] != "ROUTE_CELL_STOP"
                    or record["path"] is not None
                    or record["canonical_utf8_lf_sha256"] is not None
                    or not isinstance(record["from_route"], str)
                    or record
                    != synthetic_stop_record(record["from_route"])
                ):
                    raise ValueError(
                        f"synthetic route-stop assumption drift: {source_id}"
                    )
                continue
            if (
                kind != "SYNTHETIC_PREDICATE_FIXTURE"
                or semantics != "NONE_SYNTHETIC_REACHABILITY_ONLY"
            ):
                raise ValueError(
                    f"classifier source kind is incompatible with mode: {source_id}"
                )
        raw_path = record["path"]
        if not isinstance(raw_path, str) or not raw_path:
            raise ValueError(f"classifier source path is missing: {source_id}")
        path = (REPO_DIR / raw_path).resolve()
        try:
            path.relative_to(REPO_DIR.resolve())
        except ValueError as exc:
            raise ValueError(
                f"classifier source escapes repository: {source_id}"
            ) from exc
        if not path.is_file():
            raise ValueError(f"classifier source file is missing: {source_id}")
        if record["canonical_utf8_lf_sha256"] != canonical_hash(path):
            raise ValueError(f"classifier source hash drift: {source_id}")
        payload = load_json(path)
        if {
            key: record[key]
            for key in expected_fields
            if key not in {"path", "canonical_utf8_lf_sha256"}
        } != payload:
            raise ValueError(f"classifier source payload drift: {source_id}")


def parse_fraction(record: dict[str, int] | None) -> Fraction | None:
    if record is None:
        return None
    if set(record) != {"numerator", "denominator"}:
        raise ValueError("fraction record has unexpected fields")
    denominator = record["denominator"]
    if not isinstance(denominator, int) or denominator <= 0:
        raise ValueError("fraction denominator must be a positive integer")
    numerator = record["numerator"]
    if not isinstance(numerator, int):
        raise ValueError("fraction numerator must be an integer")
    return Fraction(numerator, denominator)


def fraction_record(value: Fraction | None) -> dict[str, int] | None:
    if value is None:
        return None
    return {"numerator": value.numerator, "denominator": value.denominator}


def first_missing_id(value: Any) -> str:
    if isinstance(value, str):
        return value
    if isinstance(value, dict):
        for key in (
            "node_id",
            "canonical_selected_representative",
            "first_missing",
        ):
            candidate = value.get(key)
            if isinstance(candidate, str):
                return candidate
    raise ValueError("cannot extract first-missing node identifier")


def status_is_pass(value: Any) -> bool:
    if value == "PASS":
        return True
    if isinstance(value, dict):
        return value.get("status") == "PASS"
    return False


def validate_gate_projection(gates: dict[str, dict[str, Any]]) -> None:
    if set(gates) != {f"H{index}" for index in range(1, 10)}:
        raise ValueError("gate projection is not exactly H1--H9")
    required = {"status", "evidence", "structural", "scope_match", "source_node"}
    for gate_id, record in gates.items():
        if set(record) != required:
            raise ValueError(f"{gate_id} gate fields drift")
        if record["status"] not in VALID_NODE_STATUSES:
            raise ValueError(f"{gate_id} has an invalid status")
        if not isinstance(record["structural"], bool):
            raise ValueError(f"{gate_id} structural flag is not Boolean")
        if not isinstance(record["scope_match"], bool):
            raise ValueError(f"{gate_id} scope flag is not Boolean")


def validate_routes(routes: dict[str, Any], evidence_mode: str) -> None:
    required = {
        "routes",
        "selected_route",
        "selected_root",
        "typed_alternative",
        "typed_alternative_crosswalk",
        "universe_completeness",
        "route_evidence_registry",
        "records",
    }
    if set(routes) != required:
        raise ValueError("route-universe fields drift")
    universe = routes["routes"]
    if not isinstance(universe, list) or len(universe) != len(set(universe)):
        raise ValueError("route universe is not a unique ordered list")
    if not universe or routes["selected_route"] not in universe:
        raise ValueError("selected route lies outside route universe")
    source_records = routes["route_evidence_registry"]
    validate_source_records(source_records, evidence_mode)
    referenced_sources: set[str] = set()
    if set(routes["records"]) != set(universe):
        raise ValueError("route records are not an exact universe cover")
    record_fields = {
        "selected",
        "stopped",
        "state",
        "source_export",
        "scope_id",
        "carrier_id",
        "normalization_id",
        "registry_id",
        "coverage",
    }
    for route_id, record in routes["records"].items():
        if set(record) != record_fields:
            raise ValueError(f"route fields drift for {route_id}")
        if record["selected"] != (route_id == routes["selected_route"]):
            raise ValueError(f"selected flag drift for {route_id}")
        if not all(
            isinstance(record[field], str) and record[field]
            for field in (
                "scope_id",
                "carrier_id",
                "normalization_id",
                "registry_id",
            )
        ):
            raise ValueError(f"route {route_id} lacks typed metadata")
        if record["stopped"]:
            source_id = record["source_export"]
            if not isinstance(source_id, str) or source_id not in source_records:
                raise ValueError(
                    f"route {route_id} stop lacks a registered source"
                )
            source = source_records[source_id]
            if (
                source["claim_type"] != "ROUTE_CELL_STOP"
                or source["scope_id"] != record["scope_id"]
                or source["from_route"] != route_id
                or source["to_route"] is not None
            ):
                raise ValueError(
                    f"route {route_id} stop source has the wrong claim"
                )
            referenced_sources.add(source_id)
            if record["coverage"] != "COMPLETE_DECLARED_ROUTE_CELL":
                raise ValueError(f"route {route_id} stop lacks exact coverage")
            if record["state"] != "STOP_SCOPED":
                raise ValueError(f"route {route_id} stop has wrong state")
        else:
            if record["source_export"] is not None:
                raise ValueError(f"open route {route_id} carries stop evidence")
            if record["state"] not in {"OPEN_NOT_TESTABLE", "OPEN"}:
                raise ValueError(f"open route {route_id} has wrong state")
    completeness = routes["universe_completeness"]
    if set(completeness) != {"status", "source_export", "scope"}:
        raise ValueError("route-universe completeness fields drift")
    if completeness["status"] not in {"PROVED", "NOT_PROVED"}:
        raise ValueError("route-universe completeness status is invalid")
    if completeness["status"] == "PROVED":
        source_id = completeness["source_export"]
        if not isinstance(source_id, str) or source_id not in source_records:
            raise ValueError(
                "complete route universe lacks a registered source"
            )
        source = source_records[source_id]
        if (
            source["claim_type"] != "ROUTE_UNIVERSE_COMPLETENESS"
            or source["scope_id"] != completeness["scope"]
            or source["from_route"] is not None
            or source["to_route"] is not None
        ):
            raise ValueError("route-universe source has the wrong claim")
        referenced_sources.add(source_id)
    elif completeness["source_export"] is not None:
        raise ValueError("unproved route universe carries a source export")
    alternative = routes["typed_alternative"]
    crosswalk = routes["typed_alternative_crosswalk"]
    if alternative is None:
        if crosswalk is not None:
            raise ValueError("crosswalk exists without a typed alternative")
    else:
        selected = routes["selected_route"]
        if alternative not in universe or alternative == selected:
            raise ValueError("typed alternative is invalid")
        if not routes["records"][selected]["stopped"]:
            raise ValueError("reroute alternative exists before selected stop")
        if routes["records"][alternative]["stopped"]:
            raise ValueError("reroute alternative is stopped")
        if not isinstance(crosswalk, str) or crosswalk not in source_records:
            raise ValueError("reroute lacks a registered typed crosswalk")
        source = source_records[crosswalk]
        if (
            source["claim_type"] != "ROUTE_CROSSWALK"
            or source["scope_id"]
            != routes["records"][selected]["scope_id"]
            or source["from_route"] != selected
            or source["to_route"] != alternative
        ):
            raise ValueError("reroute crosswalk has the wrong typed claim")
        referenced_sources.add(crosswalk)
        if (
            routes["records"][selected]["registry_id"]
            == routes["records"][alternative]["registry_id"]
        ):
            raise ValueError(
                "reroute alternative does not have a fresh registry"
            )
    if set(source_records) != referenced_sources:
        raise ValueError("classifier source registry has unused records")


def validate_frontiers(frontiers: dict[str, Any]) -> None:
    required = {
        "minimal_not_testable_antichain",
        "parent_ready_open_frontier",
        "selection_rule",
        "frontiers_are_type_disjoint",
    }
    if set(frontiers) != required:
        raise ValueError("typed-frontier fields drift")
    blockers = frontiers["minimal_not_testable_antichain"]
    open_nodes = frontiers["parent_ready_open_frontier"]
    blocker_fields = {
        "node_id",
        "status",
        "role",
        "scope_match",
        "transitive_ancestor_node_ids",
    }
    open_fields = {
        "node_id",
        "status",
        "role",
        "scope_match",
        "all_active_parents_proved",
        "target_level",
    }
    for record in blockers:
        if set(record) != blocker_fields:
            raise ValueError("typed blocker fields drift")
        if record["status"] not in VALID_NODE_STATUSES:
            raise ValueError("minimal blocker has an invalid status")
        if not isinstance(record["scope_match"], bool):
            raise ValueError("minimal blocker has a non-Boolean scope flag")
        if not (
            record["status"] == "NOT_TESTABLE"
            or not record["scope_match"]
        ):
            raise ValueError("minimal blocker has wrong type")
        if not isinstance(record["transitive_ancestor_node_ids"], list):
            raise ValueError("minimal blocker ancestry is not a list")
        ancestors = record["transitive_ancestor_node_ids"]
        if (
            any(not isinstance(item, str) or not item for item in ancestors)
            or len(ancestors) != len(set(ancestors))
            or record["node_id"] in ancestors
        ):
            raise ValueError("minimal blocker ancestry is malformed")
    blocker_ids = [record["node_id"] for record in blockers]
    if len(blocker_ids) != len(set(blocker_ids)):
        raise ValueError("duplicate minimal blocker")
    for record in blockers:
        if set(record["transitive_ancestor_node_ids"]) & set(blocker_ids):
            raise ValueError("blocker set is not an antichain")
    for record in open_nodes:
        if set(record) != open_fields:
            raise ValueError("parent-ready open fields drift")
        if (
            record["status"] != "OPEN"
            or not record["scope_match"]
            or not record["all_active_parents_proved"]
        ):
            raise ValueError("parent-ready open frontier has wrong type")
    open_ids = [record["node_id"] for record in open_nodes]
    if len(open_ids) != len(set(open_ids)):
        raise ValueError("duplicate parent-ready open node")
    disjoint = set(blocker_ids).isdisjoint(open_ids)
    if not disjoint or not frontiers["frontiers_are_type_disjoint"]:
        raise ValueError("typed frontiers were merged")


def validate_endpoint(endpoint: dict[str, Any]) -> None:
    required = {
        "contract",
        "scale",
        "source_nonduplicating_ledger",
        "literal_audit",
        "arithmetic",
        "physical",
        "full_synthesis",
    }
    if set(endpoint) != required:
        raise ValueError("endpoint-V3 fields drift")
    if endpoint["contract"] != "MVP6-FIXED-H0-ENDPOINT-V3":
        raise ValueError("endpoint-V3 contract mismatch")
    if endpoint["scale"] != "AMPLITUDE":
        raise ValueError("endpoint-V3 scale mismatch")
    validate_source_endpoint_ledger(
        endpoint["source_nonduplicating_ledger"]
    )
    literal_fields = {
        "literal_physical_coefficients",
        "fixed_physical_h0",
        "physical_atomic_normalization",
        "canonical_or_minimal_representation",
        "actual_active_support",
        "strict_one_over_400_budget",
    }
    if set(endpoint["literal_audit"]) != literal_fields:
        raise ValueError("literal endpoint audit fields drift")
    allowed_literal = {"PROVED", "NOT_TESTABLE", "OPEN", "STRICT_PASS"}
    if any(value not in allowed_literal for value in endpoint["literal_audit"].values()):
        raise ValueError("invalid literal endpoint status")
    arithmetic = endpoint["arithmetic"]
    if set(arithmetic) != {
        "strongest_export",
        "achieved_level",
        "scope_id",
        "fixed_h0",
        "log_saving",
        "deterministic_all_prefix",
        "sigma_required",
        "sigma_actual_fixed_X_lower",
        "state",
    }:
        raise ValueError("arithmetic endpoint fields drift")
    if arithmetic["fixed_h0"] != 2:
        raise ValueError("arithmetic endpoint lost fixed h0=2")
    parse_fraction(arithmetic["sigma_required"])
    parse_fraction(arithmetic["sigma_actual_fixed_X_lower"])
    physical = endpoint["physical"]
    if set(physical) != {
        "lambda_required_strict_upper",
        "lambda_phys_upper",
        "registry_complete",
        "unknown_cost_policy",
        "state",
    }:
        raise ValueError("physical endpoint fields drift")
    parse_fraction(physical["lambda_required_strict_upper"])
    parse_fraction(physical["lambda_phys_upper"])
    full = endpoint["full_synthesis"]
    if set(full) != {"strict_net_slack", "scope_compatible", "state"}:
        raise ValueError("full endpoint fields drift")
    parse_fraction(full["strict_net_slack"])
    if physical["state"] == "STRICT_PASS":
        literal_pass = all(
            value in {"PROVED", "STRICT_PASS"}
            for value in endpoint["literal_audit"].values()
        )
        threshold = parse_fraction(physical["lambda_required_strict_upper"])
        upper = parse_fraction(physical["lambda_phys_upper"])
        if (
            not literal_pass
            or not physical["registry_complete"]
            or threshold is None
            or upper is None
            or upper >= threshold
        ):
            raise ValueError("physical endpoint pass is internally inconsistent")
    if full["state"] == "STRICT_PASS":
        sigma = parse_fraction(arithmetic["sigma_actual_fixed_X_lower"])
        required_sigma = parse_fraction(arithmetic["sigma_required"])
        slack = parse_fraction(full["strict_net_slack"])
        if (
            physical["state"] != "STRICT_PASS"
            or arithmetic["state"] != "TARGET_CERTIFIED"
            or not arithmetic["deterministic_all_prefix"]
            or sigma is None
            or required_sigma is None
            or sigma < required_sigma
            or not full["scope_compatible"]
            or slack is None
            or slack <= 0
        ):
            raise ValueError("full endpoint pass is internally inconsistent")


def validate_source_endpoint_ledger(ledger: dict[str, Any]) -> None:
    required = {
        "charge_registry",
        "contract",
        "invariants",
        "ledgers",
        "scale",
        "target",
    }
    if set(ledger) != required:
        raise ValueError("source endpoint-V3 fields drift")
    if ledger["contract"] != "MVP1_FIXED_H0_NON_DUPLICATING_ENDPOINT_V3":
        raise ValueError("source endpoint-V3 contract drift")
    if ledger["scale"] != "AMPLITUDE":
        raise ValueError("source endpoint-V3 scale drift")
    invariants = ledger["invariants"]
    required_invariants = {
        "each_charge_has_exactly_one_owner",
        "full_synthesis_references_not_recharges",
        "log_power_not_converted_to_X_power",
        "no_charge_id_repeated",
        "physical_loss_registry_complete",
    }
    if set(invariants) != required_invariants:
        raise ValueError("source endpoint-V3 invariant fields drift")
    if not all(
        invariants[key]
        for key in required_invariants
        if key != "physical_loss_registry_complete"
    ):
        raise ValueError("source endpoint-V3 invariant failed")
    charges = ledger["charge_registry"]
    charge_ids = [item["charge_id"] for item in charges]
    if len(charge_ids) != len(set(charge_ids)):
        raise ValueError("source endpoint-V3 has duplicate charge ids")
    owners = {
        item["charge_id"]: item["owner_ledger"] for item in charges
    }
    used: list[str] = []
    for ledger_id in ("arithmetic", "physical"):
        for charge_id in ledger["ledgers"][ledger_id]["charge_ids"]:
            if owners.get(charge_id) != ledger_id:
                raise ValueError("source endpoint-V3 charge owner drift")
            used.append(charge_id)
    if sorted(used) != sorted(charge_ids):
        raise ValueError("source endpoint-V3 charge coverage drift")
    if ledger["ledgers"]["full_synthesis"]["charge_ids"]:
        raise ValueError("source full synthesis recharged child costs")
    arithmetic = ledger["ledgers"]["arithmetic"]
    physical = ledger["ledgers"]["physical"]
    full = ledger["ledgers"]["full_synthesis"]
    sigma = parse_fraction(arithmetic["fixed_X_sigma"])
    target = parse_fraction(ledger["target"]["fixed_X_sigma_required"])
    upper = parse_fraction(physical["fixed_X_lambda_upper"])
    lower = parse_fraction(physical["fixed_X_lambda_lower"])
    slack = parse_fraction(full["net_fixed_X_slack"])
    if target != Fraction(1, 400):
        raise ValueError("source endpoint target drift")
    paid = ledger["target"]["one_over_400_paid"]
    if invariants["physical_loss_registry_complete"] != physical[
        "registry_complete"
    ]:
        raise ValueError("source physical-registry invariant drift")
    if arithmetic["state"] == "TARGET_CERTIFIED":
        if sigma is None or target is None or sigma < target or not paid:
            raise ValueError("source arithmetic pass is inconsistent")
    elif paid:
        raise ValueError("source endpoint target paid without certification")
    if physical["state"] == "STRICT_PASS":
        if (
            not physical["registry_complete"]
            or upper is None
            or target is None
            or upper >= target
        ):
            raise ValueError("source physical pass is inconsistent")
    if full["state"] == "STRICT_PASS":
        if (
            arithmetic["state"] != "TARGET_CERTIFIED"
            or physical["state"] != "STRICT_PASS"
            or slack is None
            or slack <= 0
        ):
            raise ValueError("source full pass is inconsistent")
    if lower is not None and upper is not None and lower > upper:
        raise ValueError("source physical interval is reversed")


def complete_stop_cover(routes: dict[str, Any]) -> bool:
    completeness = routes["universe_completeness"]
    return (
        completeness["status"] == "PROVED"
        and bool(completeness["source_export"])
        and all(
            record["stopped"]
            and record["coverage"] == "COMPLETE_DECLARED_ROUTE_CELL"
            and bool(record["source_export"])
            for record in routes["records"].values()
        )
    )


def physical_endpoint_certified(endpoint: dict[str, Any]) -> bool:
    literal = endpoint["literal_audit"]
    physical = endpoint["physical"]
    threshold = parse_fraction(physical["lambda_required_strict_upper"])
    upper = parse_fraction(physical["lambda_phys_upper"])
    literal_pass = all(
        value in {"PROVED", "STRICT_PASS"} for value in literal.values()
    )
    return (
        literal_pass
        and physical["state"] == "STRICT_PASS"
        and physical["registry_complete"]
        and threshold is not None
        and upper is not None
        and upper < threshold
    )


def full_endpoint_certified(endpoint: dict[str, Any]) -> bool:
    arithmetic = endpoint["arithmetic"]
    full = endpoint["full_synthesis"]
    sigma = parse_fraction(arithmetic["sigma_actual_fixed_X_lower"])
    required = parse_fraction(arithmetic["sigma_required"])
    slack = parse_fraction(full["strict_net_slack"])
    return (
        physical_endpoint_certified(endpoint)
        and arithmetic["state"] == "TARGET_CERTIFIED"
        and arithmetic["deterministic_all_prefix"]
        and sigma is not None
        and required is not None
        and sigma >= required
        and full["scope_compatible"]
        and full["state"] == "STRICT_PASS"
        and slack is not None
        and slack > 0
    )


def validate_classifier_state(state: dict[str, Any]) -> None:
    required = {
        "evidence_mode",
        "gates",
        "typed_frontiers",
        "routes",
        "endpoint_ledger_v3",
    }
    if set(state) != required:
        raise ValueError("classifier state fields drift")
    validate_gate_projection(state["gates"])
    validate_frontiers(state["typed_frontiers"])
    validate_routes(state["routes"], state["evidence_mode"])
    validate_endpoint(state["endpoint_ledger_v3"])


def decide_valid(state: dict[str, Any]) -> str:
    validate_classifier_state(state)
    gates = state["gates"]
    frontiers = state["typed_frontiers"]
    routes = state["routes"]
    endpoint = state["endpoint_ledger_v3"]
    selected = routes["selected_route"]
    if all(
        record["status"] == "PROVED" and record["scope_match"]
        for record in gates.values()
    ) and full_endpoint_certified(endpoint):
        return "GO"
    if complete_stop_cover(routes):
        return "ARCHITECTURE_INFEASIBLE"
    if routes["records"][selected]["stopped"]:
        if routes["typed_alternative"] is not None:
            return "REROUTE"
        return "STOP_ROUTE"
    if (
        frontiers["minimal_not_testable_antichain"]
        or any(
            record["status"] == "NOT_TESTABLE" or not record["scope_match"]
            for record in gates.values()
        )
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
    pure_positive_l2_frontier = bool(unresolved) and all(
        record["status"] == "OPEN"
        and record["scope_match"]
        and not record["structural"]
        and record["evidence"] == "L2_ACTUAL_POSITIVE_TARGET"
        for record in unresolved
    )
    if (
        structural_closed
        and physical_endpoint_certified(endpoint)
        and pure_positive_l2_frontier
    ):
        return "ARITHMETIC_FRONTIER"
    return "OPEN"


def classify(state: dict[str, Any]) -> str:
    try:
        return decide_valid(state)
    except (KeyError, TypeError, ValueError):
        return "INVALID"


def current_routes() -> dict[str, Any]:
    return {
        "routes": [
            "current_schema_only_canonical_lift",
            "occurrence_augmented_map",
            "scalar_plus_ETO",
            "direct_additive_twist_core",
            "bad_endpoint_pointwise_core",
        ],
        "selected_route": SELECTED_ROUTE,
        "selected_root": "ROOT.selected_map_synthesis",
        "typed_alternative": None,
        "typed_alternative_crosswalk": None,
        "universe_completeness": {
            "status": "NOT_PROVED",
            "source_export": None,
            "scope": "actual_fixed_h0_physical_carrier",
        },
        "route_evidence_registry": {
            (
                "TPC156.H1.current_artifacts_only_canonical_actual_lift"
            ): locked_tpc156_stop_record()
        },
        "records": {
            "current_schema_only_canonical_lift": {
                "selected": False,
                "stopped": True,
                "state": "STOP_SCOPED",
                "source_export": (
                    "TPC156.H1.current_artifacts_only_canonical_actual_lift"
                ),
                "scope_id": "CURRENT_ARTIFACTS_ONLY",
                "carrier_id": "maximal_formal_schema_completion_class",
                "normalization_id": "cut_shadow_column_conservation",
                "registry_id": "registry.current_archive",
                "coverage": "COMPLETE_DECLARED_ROUTE_CELL",
            },
            "occurrence_augmented_map": {
                "selected": True,
                "stopped": False,
                "state": "OPEN_NOT_TESTABLE",
                "source_export": None,
                "scope_id": "ACTUAL_OCCURRENCE_AUGMENTED_CARRIER",
                "carrier_id": "all_nonsoft_ETO_plus_FUM_occurrences",
                "normalization_id": "physical_atomic_fixed_h0",
                "registry_id": "registry.production_occurrence",
                "coverage": "OPEN_SELECTED_ROUTE",
            },
            "scalar_plus_ETO": {
                "selected": False,
                "stopped": False,
                "state": "OPEN_NOT_TESTABLE",
                "source_export": None,
                "scope_id": "ORIGINAL_SCALE_FUM_PLUS_ETO",
                "carrier_id": "all_nonsoft_ETO_plus_FUM_cut_paths",
                "normalization_id": "original_scale_scalar",
                "registry_id": "registry.scalar_plus_ETO",
                "coverage": "OPEN_ALTERNATIVE_ROUTE",
            },
            "direct_additive_twist_core": {
                "selected": False,
                "stopped": False,
                "state": "OPEN",
                "source_export": None,
                "scope_id": "ACTUAL_PERIODIC_CORE_ONLY",
                "carrier_id": "determinant_two_two_mobius_periodic_core",
                "normalization_id": "q_over_N",
                "registry_id": "registry.direct_additive_twist_core",
                "coverage": "OPEN_ALTERNATIVE_ROUTE",
            },
            "bad_endpoint_pointwise_core": {
                "selected": False,
                "stopped": False,
                "state": "OPEN",
                "source_export": None,
                "scope_id": "ACTUAL_PREFIX_CORE_ONLY",
                "carrier_id": "determinant_two_two_mobius_periodic_core",
                "normalization_id": "q_over_T",
                "registry_id": "registry.bad_endpoint_pointwise_core",
                "coverage": "OPEN_ALTERNATIVE_ROUTE",
            },
        },
    }


def current_gates() -> dict[str, dict[str, Any]]:
    records: dict[str, dict[str, Any]] = {}
    statuses = {
        "H1": ("NOT_TESTABLE", True, FIRST_MISSING, "L1_STRUCTURAL_TARGET"),
        "H2": ("NOT_TESTABLE", False, "H2.literal_weight_and_phase_return", "L2_ACTUAL_POSITIVE_TARGET"),
        "H3": ("NOT_TESTABLE", False, "A160.production_literal_weight", "L2_ACTUAL_POSITIVE_TARGET"),
        "H4": ("NOT_TESTABLE", False, "H4.endpoint_return", "L2_ACTUAL_POSITIVE_TARGET"),
        "H5": ("NOT_TESTABLE", False, "H5.actual_determinant_zero_pair", "L2_ACTUAL_POSITIVE_TARGET"),
        "H6": ("NOT_TESTABLE", True, "H6.actual_physical_cover", "L1_STRUCTURAL_TARGET"),
        "H7": ("NOT_TESTABLE", True, "H7.downstream_fixed_h0_totality", "L1_STRUCTURAL_TARGET"),
        "H8": ("NOT_TESTABLE", True, "H8.hard_packet_reconnection", "L1_STRUCTURAL_TARGET"),
        "H9": ("NOT_TESTABLE", True, "H9.independent_physical_registry", "L1_STRUCTURAL_TARGET"),
    }
    for gate_id, (status, structural, source_node, evidence) in statuses.items():
        records[gate_id] = {
            "status": status,
            "evidence": evidence,
            "structural": structural,
            "scope_match": True,
            "source_node": source_node,
        }
    return records


def current_frontiers(
    source_blockers: list[dict[str, Any]],
    source_parent_ready: list[dict[str, Any]],
) -> dict[str, Any]:
    return {
        "minimal_not_testable_antichain": copy.deepcopy(source_blockers),
        "parent_ready_open_frontier": copy.deepcopy(source_parent_ready),
        "selection_rule": (
            "active selected-route ancestors; minimal NOT_TESTABLE "
            "antichain is separate from status-OPEN nodes whose active "
            "parents are all PROVED"
        ),
        "frontiers_are_type_disjoint": True,
    }


def fixture_source_endpoint_v3() -> dict[str, Any]:
    return {
        "charge_registry": [
            {
                "charge_id": "ARITH.correlation_log_saving",
                "owner_ledger": "arithmetic",
                "quantity_kind": "LOG_AMPLITUDE_SAVING",
                "state": "PROVED",
                "value": "(log X)^(-kappa_0+o(1))",
            },
            {
                "charge_id": "ARITH.dyadic_shadow",
                "owner_ledger": "arithmetic",
                "quantity_kind": "LOG_EXCEPTIONAL_MEASURE",
                "state": "PROVED",
                "value": "(log X)^(-kappa_0+o(1))",
            },
            {
                "charge_id": "PHYS.good_variation",
                "owner_ledger": "physical",
                "quantity_kind": "LOG_AMPLITUDE_COST",
                "state": "NOT_TESTABLE",
                "value": None,
            },
            {
                "charge_id": "PHYS.bad_variation",
                "owner_ledger": "physical",
                "quantity_kind": "ATOMIC_ENDPOINT_COST",
                "state": "NOT_TESTABLE",
                "value": None,
            },
            {
                "charge_id": "PHYS.phase_return",
                "owner_ledger": "physical",
                "quantity_kind": "PHASE_RETURN_COST",
                "state": "NOT_TESTABLE",
                "value": None,
            },
            {
                "charge_id": "PHYS.four_sign_reconnection",
                "owner_ledger": "physical",
                "quantity_kind": "RECONNECTION_COST",
                "state": "NOT_TESTABLE",
                "value": None,
            },
        ],
        "contract": "MVP1_FIXED_H0_NON_DUPLICATING_ENDPOINT_V3",
        "invariants": {
            "each_charge_has_exactly_one_owner": True,
            "full_synthesis_references_not_recharges": True,
            "log_power_not_converted_to_X_power": True,
            "no_charge_id_repeated": True,
            "physical_loss_registry_complete": False,
        },
        "ledgers": {
            "arithmetic": {
                "charge_ids": [
                    "ARITH.correlation_log_saving",
                    "ARITH.dyadic_shadow",
                ],
                "fixed_X_sigma": fraction_record(Fraction(0)),
                "state": "INCOMPLETE",
            },
            "full_synthesis": {
                "charge_ids": [],
                "input_ledgers": ["arithmetic", "physical"],
                "net_fixed_X_slack": None,
                "state": "INCOMPLETE",
            },
            "physical": {
                "charge_ids": [
                    "PHYS.good_variation",
                    "PHYS.bad_variation",
                    "PHYS.phase_return",
                    "PHYS.four_sign_reconnection",
                ],
                "fixed_X_lambda_lower": None,
                "fixed_X_lambda_upper": None,
                "registry_complete": False,
                "state": "NOT_TESTABLE",
                "unknown_cost_policy": "UNKNOWN_IS_NOT_ZERO",
            },
        },
        "scale": "AMPLITUDE",
        "target": {
            "fixed_X_sigma_required": fraction_record(Fraction(1, 400)),
            "one_over_400_paid": False,
        },
    }


def current_endpoint_v3(
    source_ledger: dict[str, Any] | None = None,
) -> dict[str, Any]:
    threshold = Fraction(1, 400)
    return {
        "contract": "MVP6-FIXED-H0-ENDPOINT-V3",
        "scale": "AMPLITUDE",
        "source_nonduplicating_ledger": copy.deepcopy(
            source_ledger
            if source_ledger is not None
            else fixture_source_endpoint_v3()
        ),
        "literal_audit": {
            "literal_physical_coefficients": "NOT_TESTABLE",
            "fixed_physical_h0": "PROVED",
            "physical_atomic_normalization": "NOT_TESTABLE",
            "canonical_or_minimal_representation": "NOT_TESTABLE",
            "actual_active_support": "NOT_TESTABLE",
            "strict_one_over_400_budget": "NOT_TESTABLE",
        },
        "arithmetic": {
            "strongest_export": "A159.almost_endpoint_prefix",
            "achieved_level": "L1_ACTUAL_PREFIX_ALMOST_ENDPOINT",
            "scope_id": "determinant_two_two_mobius_periodic_core",
            "fixed_h0": 2,
            "log_saving": True,
            "deterministic_all_prefix": False,
            "sigma_required": fraction_record(threshold),
            "sigma_actual_fixed_X_lower": fraction_record(Fraction(0)),
            "state": "LOG_ALMOST_ENDPOINT_ONLY",
        },
        "physical": {
            "lambda_required_strict_upper": fraction_record(threshold),
            "lambda_phys_upper": None,
            "registry_complete": False,
            "unknown_cost_policy": "UNKNOWN_IS_NOT_ZERO",
            "state": "INCOMPLETE",
        },
        "full_synthesis": {
            "strict_net_slack": None,
            "scope_compatible": False,
            "state": "INCOMPLETE",
        },
    }


def source_parent_ready_records(
    source: dict[str, Any],
) -> list[dict[str, Any]]:
    raw = source.get("parent_ready_open_frontiers", [])
    if not isinstance(raw, list):
        raise ValueError("TPC-161 parent-ready open frontier is not a list")
    node_lookup = {
        item["node_id"]: item for item in source.get("nodes", [])
    }
    records: list[dict[str, Any]] = []
    for item in raw:
        if not isinstance(item, dict):
            raise ValueError("TPC-161 parent-ready open item is malformed")
        node_id = first_missing_id(item)
        node = node_lookup.get(node_id)
        if node is None:
            raise ValueError("TPC-161 parent-ready node is absent from DAG")
        if (
            item.get("status") != "OPEN"
            or not item.get("parents_all_proved")
            or item.get("artifact_readiness") != "READY"
            or node.get("role") != "ARITHMETIC_TARGET"
            or node.get("status") != "OPEN"
        ):
            raise ValueError("TPC-161 parent-ready node has wrong type")
        records.append(
            {
                "node_id": node_id,
                "status": "OPEN",
                "role": node["role"],
                "scope_match": True,
                "all_active_parents_proved": True,
                "target_level": node["program_level"],
            }
        )
    if not records:
        raise ValueError("TPC-161 parent-ready OPEN frontier is empty")
    return sorted(records, key=lambda record: record["node_id"])


def transitive_ancestor_ids(
    node_id: str,
    node_lookup: dict[str, dict[str, Any]],
) -> list[str]:
    memo: dict[str, set[str]] = {}
    visiting: set[str] = set()

    def visit(current: str) -> set[str]:
        if current in memo:
            return memo[current]
        if current in visiting:
            raise ValueError("TPC-161 source DAG contains a cycle")
        node = node_lookup.get(current)
        if node is None:
            raise ValueError(f"TPC-161 source DAG lacks node {current}")
        parents = node.get("parents")
        if not isinstance(parents, list) or any(
            not isinstance(parent, str) for parent in parents
        ):
            raise ValueError(f"TPC-161 source DAG parents drift at {current}")
        visiting.add(current)
        result: set[str] = set()
        for parent in parents:
            if parent not in node_lookup:
                raise ValueError(
                    f"TPC-161 source DAG lacks parent {parent}"
                )
            result.add(parent)
            result.update(visit(parent))
        visiting.remove(current)
        memo[current] = result
        return result

    return sorted(visit(node_id))


def source_selected_blocker_records(
    source: dict[str, Any],
) -> list[dict[str, Any]]:
    node_lookup = {
        item["node_id"]: item for item in source.get("nodes", [])
    }
    antichain_lookup = {
        item["route_id"]: item
        for item in source.get("minimal_not_testable_antichains", [])
    }
    selected = antichain_lookup.get("ROOT.selected_map_synthesis")
    if selected is None:
        raise ValueError("TPC-161 selected-root antichain is missing")
    blocker_ids = selected.get("minimal_not_testable_nodes")
    if not isinstance(blocker_ids, list) or not blocker_ids:
        raise ValueError("TPC-161 selected-root antichain is malformed")
    if blocker_ids[0] != FIRST_MISSING:
        raise ValueError("TPC-161 selected first missing pointer drift")
    records: list[dict[str, Any]] = []
    for node_id in blocker_ids:
        node = node_lookup.get(node_id)
        if node is None:
            raise ValueError("TPC-161 blocker is absent from DAG")
        if (
            node.get("status") != "NOT_TESTABLE"
            or node.get("artifact_readiness") != "MISSING"
        ):
            raise ValueError("TPC-161 blocker has wrong type")
        records.append(
            {
                "node_id": node_id,
                "status": "NOT_TESTABLE",
                "role": node["role"],
                "scope_match": True,
                "transitive_ancestor_node_ids": transitive_ancestor_ids(
                    node_id, node_lookup
                ),
            }
        )
    return records


def validate_upstreams(
    manifest: dict[str, Any],
    audit: dict[str, Any],
    tpc156: dict[str, Any],
    tpc160: dict[str, Any],
) -> dict[str, Any]:
    if not status_is_pass(audit):
        raise ValueError("TPC-161 audit is not PASS")
    if manifest.get("current_verdict") != "NOT_TESTABLE":
        raise ValueError("TPC-161 verdict drift")
    if first_missing_id(manifest.get("first_missing")) != FIRST_MISSING:
        raise ValueError("TPC-161 first-missing pointer drift")
    if manifest.get("snapshot", {}).get("selected_route") != SELECTED_ROUTE:
        raise ValueError("TPC-161 selected route drift")
    routes161 = manifest.get("routes")
    if not isinstance(routes161, list):
        raise ValueError("TPC-161 route universe is malformed")
    route_state161 = {
        item["route_id"]: (item["state"], item["stopped"], item["selected"])
        for item in routes161
    }
    expected_route_state = {
        "current_schema_only_canonical_lift": (
            "STOP_SCOPED",
            True,
            False,
        ),
        "occurrence_augmented_map": (
            "OPEN_NOT_TESTABLE",
            False,
            True,
        ),
        "scalar_plus_ETO": ("OPEN_NOT_TESTABLE", False, False),
        "direct_additive_twist_core": (
            "OPEN_PARENT_READY",
            False,
            False,
        ),
        "bad_endpoint_pointwise_core": (
            "OPEN_PARENT_READY",
            False,
            False,
        ),
    }
    if route_state161 != expected_route_state:
        raise ValueError("TPC-161 route state drift")
    progress161 = manifest.get("progress_classification", {})
    if progress161.get("strongest_arithmetic_export") != (
        "A159.almost_endpoint_prefix"
    ):
        raise ValueError("TPC-161 strongest arithmetic export drift")
    if progress161.get("strongest_arithmetic_level") != (
        "L1_ACTUAL_PREFIX_ALMOST_ENDPOINT"
    ):
        raise ValueError("TPC-161 strongest arithmetic level drift")
    if progress161.get("new_positive_L2"):
        raise ValueError("TPC-161 was promoted to positive L2")
    source_endpoint = manifest.get("endpoint_ledger_v3", {})
    if source_endpoint.get("contract") != (
        "MVP1_FIXED_H0_NON_DUPLICATING_ENDPOINT_V3"
    ):
        raise ValueError("TPC-161 endpoint-V3 contract drift")
    if source_endpoint.get("target", {}).get("one_over_400_paid"):
        raise ValueError("TPC-161 endpoint was falsely paid")
    if tpc156.get("current_verdict") != "NOT_TESTABLE":
        raise ValueError("TPC-156 verdict drift")
    if tpc156.get("first_missing_selected_route") != FIRST_MISSING:
        raise ValueError("TPC-156 structural anchor drift")
    routes156 = tpc156.get("routes", {})
    if routes156.get("selected_route") != SELECTED_ROUTE:
        raise ValueError("TPC-156 selected route drift")
    if not routes156.get("current_archive_only_actual_lift", {}).get("stopped"):
        raise ValueError("TPC-156 scoped stop was lost")
    if routes156.get("occurrence_augmented_map", {}).get("stopped"):
        raise ValueError("TPC-156 augmented route was globally stopped")
    if routes156.get("scalar_plus_ETO", {}).get("stopped"):
        raise ValueError("TPC-156 scalar-plus-ETO route was globally stopped")
    if tpc160.get("status") != "PASS":
        raise ValueError("TPC-160 audit is not PASS")
    theorem160 = tpc160.get("theorem", {})
    if theorem160.get("export_id") != "A160.exceptional_variation_abel_return":
        raise ValueError("TPC-160 export drift")
    if theorem160.get("status") != (
        "PROVED_L1_ACTUAL_WEIGHTED_ALMOST_ENDPOINT_INTERFACE"
    ):
        raise ValueError("TPC-160 interface level drift")
    if tpc160.get("production_status", {}).get("actual_literal_weight") != (
        "NOT_TESTABLE"
    ):
        raise ValueError("TPC-160 literal-weight status drift")
    if tpc160.get("claim_boundary", {}).get("positive_fixed_X_power"):
        raise ValueError("TPC-160 was promoted to positive fixed-X power")
    imports = manifest.get("imports", [])
    if not any(
        isinstance(item, dict)
        and item.get("paper") == "TPC-159"
        and item.get("source_export_id")
        == "A159.dyadic_shadow_almost_endpoint_prefix"
        for item in imports
    ):
        raise ValueError("TPC-161 does not expose a TPC-159 import")
    return {
        "source_schema": manifest.get("schema"),
        "source_status": audit.get("status"),
        "source_verdict": manifest["current_verdict"],
        "source_first_missing": first_missing_id(manifest["first_missing"]),
    }


def build_snapshot() -> dict[str, Any]:
    manifest = load_json(TPC161_MANIFEST)
    audit = load_json(TPC161_AUDIT)
    tpc156 = load_json(TPC156_DECISION)
    tpc160 = load_json(TPC160_AUDIT)
    anchors = validate_upstreams(manifest, audit, tpc156, tpc160)
    source_parent_ready = source_parent_ready_records(manifest)
    source_blockers = source_selected_blocker_records(manifest)
    routes = current_routes()
    gates = current_gates()
    frontiers = current_frontiers(source_blockers, source_parent_ready)
    endpoint = current_endpoint_v3(manifest["endpoint_ledger_v3"])
    state = {
        "evidence_mode": SOURCE_LOCKED,
        "gates": gates,
        "typed_frontiers": frontiers,
        "routes": routes,
        "endpoint_ledger_v3": endpoint,
    }
    verdict = decide_valid(state)
    if verdict != "NOT_TESTABLE":
        raise ValueError("unexpected current MVP6 verdict")

    locks = [
        source_lock("TPC161.integration_script", TPC161_SCRIPT),
        source_lock("TPC161.manifest_schema", TPC161_MANIFEST_SCHEMA),
        source_lock("TPC161.manifest", TPC161_MANIFEST),
        source_lock("TPC161.audit_schema", TPC161_AUDIT_SCHEMA),
        source_lock("TPC161.audit", TPC161_AUDIT),
        source_lock("TPC156.decision", TPC156_DECISION),
        source_lock("TPC160.audit", TPC160_AUDIT),
        source_lock(
            "TPC162.synthetic_route_universe_fixture",
            ROUTE_UNIVERSE_FIXTURE,
        ),
        source_lock(
            "TPC162.synthetic_route_crosswalk_fixture",
            ROUTE_CROSSWALK_FIXTURE,
        ),
    ]
    return {
        "schema": SNAPSHOT_SCHEMA_ID,
        "snapshot": {
            "date": "2026-07-28",
            "source_manifest": repo_relative(TPC161_MANIFEST),
            "source_manifest_sha256": canonical_hash(TPC161_MANIFEST),
            "snapshot_schema_sha256": canonical_hash(SNAPSHOT_SCHEMA),
            "hash_mode": HASH_MODE,
            "hash_semantics": HASH_SEMANTICS,
            "classifier_evidence_mode": SOURCE_LOCKED,
            "selected_route": SELECTED_ROUTE,
        },
        "source_locks": locks,
        "imported_state": {
            "tpc161_schema": anchors["source_schema"],
            "tpc161_status": anchors["source_status"],
            "tpc161_verdict": anchors["source_verdict"],
            "selected_route": SELECTED_ROUTE,
            "first_missing": anchors["source_first_missing"],
            "selected_root_minimal_not_testable_nodes": [
                record["node_id"] for record in source_blockers
            ],
            "structural_shadow_level": "PROVED_L1_STRUCTURAL",
            "current_artifacts_only_stop_scope": "CURRENT_ARTIFACTS_ONLY",
            "occurrence_augmented_map_globally_stopped": False,
            "scalar_plus_ETO_globally_stopped": False,
            "route_universe_complete": False,
            "strongest_arithmetic_export": (
                "A159.almost_endpoint_prefix"
            ),
            "strongest_arithmetic_level": (
                "PROVED_L1_ACTUAL_PREFIX_ALMOST_ENDPOINT"
            ),
            "strongest_arithmetic_scope": (
                "determinant_two_two_mobius_periodic_core"
            ),
            "fixed_h0": 2,
            "deterministic_all_prefix": False,
            "positive_fixed_X_power": False,
            "weighted_interface_export": (
                "A160.exceptional_variation_abel_return"
            ),
            "weighted_interface_level": (
                "PROVED_L1_ACTUAL_WEIGHTED_ALMOST_ENDPOINT_INTERFACE"
            ),
            "production_literal_weight": "NOT_TESTABLE",
        },
        "route_universe": routes,
        "gate_projection": gates,
        "typed_frontiers": frontiers,
        "endpoint_ledger_v3": endpoint,
        "next_forced_objects": {
            "structural": [
                FIRST_MISSING,
                "H1.frontier_occurrence_lift",
                "H1.nine_literal_defects_and_occurrence_registry",
            ],
            "arithmetic_physical_return": [
                "H9.literal_weight_registry",
                "H9.phase_cell_registry",
                "H9.endpoint_registry",
                "H9.normalization_registry",
                "A160.small_bad_variation_or_pointwise_bad_endpoint_theorem",
                "H3.positive_fixed_X_power_upgrade",
            ],
        },
        "ordered_valid_verdicts": ORDERED_VERDICTS,
        "current_verdict": verdict,
        "progress_classification": {
            "structural_achieved_level": "L1_STRUCTURAL",
            "actual_arithmetic_achieved_level": (
                "L1_ACTUAL_PREFIX_ALMOST_ENDPOINT"
            ),
            "actual_weighted_interface_level": (
                "L1_ACTUAL_WEIGHTED_ALMOST_ENDPOINT_INTERFACE"
            ),
            "actual_fixed_power_target_level": "L2_ACTUAL_POSITIVE",
            "actual_fixed_power_status": "NOT_PROVED",
            "actual_fixed_power_achieved": False,
            "new_positive_L2": False,
        },
        "claim_boundary": {
            "source_hashes_prove_theorems": False,
            "current_artifacts_stop_is_actual_carrier_impossibility": False,
            "augmented_map_route_globally_stopped": False,
            "scalar_plus_ETO_route_globally_stopped": False,
            "route_universe_complete": False,
            "GO": False,
            "ARCHITECTURE_INFEASIBLE": False,
            "REROUTE": False,
            "STOP_SELECTED_ROUTE": False,
            "ARITHMETIC_FRONTIER": False,
            "deterministic_all_prefix": False,
            "production_literal_physical_weight": False,
            "positive_fixed_X_power_L2": False,
            "strict_one_over_400_endpoint": False,
            "hard_packet_oX": False,
            "prime_pair_lower_bound": False,
            "twin_prime_theorem": False,
        },
    }


def validate_snapshot(snapshot: dict[str, Any]) -> dict[str, bool]:
    schema = load_json(SNAPSHOT_SCHEMA)
    assert_strict_schema_shape(schema)
    assert_strict_schema_shape(load_json(AUDIT_SCHEMA))
    if set(snapshot) != TOP_LEVEL_SNAPSHOT_FIELDS:
        raise ValueError("snapshot top-level fields differ from contract")
    if set(snapshot) != set(schema["required"]):
        raise ValueError("snapshot fields differ from schema")
    if snapshot["schema"] != SNAPSHOT_SCHEMA_ID:
        raise ValueError("snapshot schema id drift")
    if snapshot["ordered_valid_verdicts"] != ORDERED_VERDICTS:
        raise ValueError("valid-verdict precedence drift")
    if snapshot["snapshot"]["hash_mode"] != HASH_MODE:
        raise ValueError("hash mode drift")
    if snapshot["snapshot"]["hash_semantics"] != HASH_SEMANTICS:
        raise ValueError("hashes were assigned proof semantics")
    if snapshot["snapshot"]["classifier_evidence_mode"] != SOURCE_LOCKED:
        raise ValueError("current classifier is not source locked")
    expected_locks = {
        lock["source_id"]: lock
        for lock in [
            source_lock("TPC161.integration_script", TPC161_SCRIPT),
            source_lock("TPC161.manifest_schema", TPC161_MANIFEST_SCHEMA),
            source_lock("TPC161.manifest", TPC161_MANIFEST),
            source_lock("TPC161.audit_schema", TPC161_AUDIT_SCHEMA),
            source_lock("TPC161.audit", TPC161_AUDIT),
            source_lock("TPC156.decision", TPC156_DECISION),
            source_lock("TPC160.audit", TPC160_AUDIT),
            source_lock(
                "TPC162.synthetic_route_universe_fixture",
                ROUTE_UNIVERSE_FIXTURE,
            ),
            source_lock(
                "TPC162.synthetic_route_crosswalk_fixture",
                ROUTE_CROSSWALK_FIXTURE,
            ),
        ]
    }
    actual_locks = {lock["source_id"]: lock for lock in snapshot["source_locks"]}
    if actual_locks != expected_locks:
        raise ValueError("dynamic source-lock table is stale")
    if snapshot["snapshot"]["source_manifest_sha256"] != canonical_hash(
        TPC161_MANIFEST
    ):
        raise ValueError("source manifest pointer is stale")
    if snapshot["snapshot"]["snapshot_schema_sha256"] != canonical_hash(
        SNAPSHOT_SCHEMA
    ):
        raise ValueError("snapshot schema pointer is stale")
    validate_routes(snapshot["route_universe"], SOURCE_LOCKED)
    if snapshot["route_universe"] != current_routes():
        raise ValueError("TPC-161 route universe was not preserved")
    validate_gate_projection(snapshot["gate_projection"])
    validate_frontiers(snapshot["typed_frontiers"])
    validate_endpoint(snapshot["endpoint_ledger_v3"])
    manifest = load_json(TPC161_MANIFEST)
    if snapshot["endpoint_ledger_v3"][
        "source_nonduplicating_ledger"
    ] != manifest["endpoint_ledger_v3"]:
        raise ValueError("TPC-161 endpoint-V3 ledger was not preserved")
    imported = snapshot["imported_state"]
    if imported["tpc161_verdict"] != "NOT_TESTABLE":
        raise ValueError("imported TPC-161 verdict drift")
    if imported["first_missing"] != FIRST_MISSING:
        raise ValueError("imported first missing drift")
    if imported["selected_root_minimal_not_testable_nodes"] != [
        record["node_id"] for record in source_selected_blocker_records(manifest)
    ]:
        raise ValueError("imported selected-root blocker antichain drift")
    if imported["current_artifacts_only_stop_scope"] != "CURRENT_ARTIFACTS_ONLY":
        raise ValueError("scoped stop was promoted")
    if imported["occurrence_augmented_map_globally_stopped"]:
        raise ValueError("augmented map route was globally stopped")
    if imported["scalar_plus_ETO_globally_stopped"]:
        raise ValueError("scalar-plus-ETO route was globally stopped")
    if imported["route_universe_complete"]:
        raise ValueError("route-universe completeness was invented")
    if imported["strongest_arithmetic_export"] != (
        "A159.almost_endpoint_prefix"
    ):
        raise ValueError("strongest arithmetic export drift")
    if imported["strongest_arithmetic_level"] != (
        "PROVED_L1_ACTUAL_PREFIX_ALMOST_ENDPOINT"
    ):
        raise ValueError("strongest arithmetic level drift")
    if imported["deterministic_all_prefix"]:
        raise ValueError("almost endpoint was promoted to every prefix")
    if imported["positive_fixed_X_power"]:
        raise ValueError("log decay was promoted to fixed-X power")
    if imported["production_literal_weight"] != "NOT_TESTABLE":
        raise ValueError("conditional interface was promoted to production")
    blocker_ids = [
        record["node_id"]
        for record in snapshot["typed_frontiers"][
            "minimal_not_testable_antichain"
        ]
    ]
    source_blockers = source_selected_blocker_records(manifest)
    if blocker_ids != [record["node_id"] for record in source_blockers]:
        raise ValueError("minimal typed blocker antichain drift")
    if snapshot["typed_frontiers"][
        "minimal_not_testable_antichain"
    ] != source_blockers:
        raise ValueError("typed blocker metadata drift")
    source_parent_ready = source_parent_ready_records(manifest)
    if snapshot["typed_frontiers"][
        "parent_ready_open_frontier"
    ] != source_parent_ready:
        raise ValueError("parent-ready OPEN frontier drift")
    if snapshot["endpoint_ledger_v3"]["arithmetic"][
        "deterministic_all_prefix"
    ]:
        raise ValueError("endpoint ledger falsely claims all prefixes")
    if parse_fraction(
        snapshot["endpoint_ledger_v3"]["arithmetic"][
            "sigma_actual_fixed_X_lower"
        ]
    ) != 0:
        raise ValueError("log saving received a positive X-power exponent")
    state = {
        "evidence_mode": snapshot["snapshot"]["classifier_evidence_mode"],
        "gates": snapshot["gate_projection"],
        "typed_frontiers": snapshot["typed_frontiers"],
        "routes": snapshot["route_universe"],
        "endpoint_ledger_v3": snapshot["endpoint_ledger_v3"],
    }
    verdict = decide_valid(state)
    if verdict != snapshot["current_verdict"] or verdict != "NOT_TESTABLE":
        raise ValueError("current MVP6 verdict drift")
    if physical_endpoint_certified(snapshot["endpoint_ledger_v3"]):
        raise ValueError("physical endpoint falsely passes")
    if full_endpoint_certified(snapshot["endpoint_ledger_v3"]):
        raise ValueError("full endpoint falsely passes")
    if any(snapshot["claim_boundary"].values()):
        raise ValueError("claim boundary contains a false positive")
    return {
        "strict_snapshot_schema": True,
        "dynamic_tpc161_source_locks": True,
        "direct_tpc156_and_tpc160_anchors": True,
        "hashes_integrity_only": True,
        "file_hash_backed_classifier_sources": True,
        "route_universe_requirement_preserved": True,
        "fresh_registry_requirement_preserved": True,
        "scoped_stop_not_globalized": True,
        "typed_blocker_antichain": True,
        "transitive_ancestry_verified": True,
        "scope_mismatch_blocker_supported": True,
        "parent_ready_open_frontier_separate": True,
        "endpoint_v3_complete_fields": True,
        "actual_periodic_core_L1_retained": True,
        "almost_endpoint_not_all_prefix": True,
        "log_saving_not_fixed_X_power": True,
        "weighted_interface_not_production_weight": True,
        "current_verdict_not_testable": True,
        "claim_boundary": True,
    }


def synthetic_gates(
    *,
    structural_status: str,
    arithmetic_status: str,
    arithmetic_evidence: str = "L2_ACTUAL_POSITIVE_TARGET",
) -> dict[str, dict[str, Any]]:
    gates: dict[str, dict[str, Any]] = {}
    for index in range(1, 10):
        structural = index in {1, 6, 7, 8, 9}
        gates[f"H{index}"] = {
            "status": structural_status if structural else arithmetic_status,
            "evidence": (
                "L1_STRUCTURAL"
                if structural
                else arithmetic_evidence
            ),
            "structural": structural,
            "scope_match": True,
            "source_node": f"synthetic.H{index}",
        }
    return gates


def synthetic_frontiers(
    *,
    blocker: bool,
    parent_ready_open: bool,
    scope_mismatch_blocker: bool = False,
) -> dict[str, Any]:
    if blocker and scope_mismatch_blocker:
        raise ValueError("synthetic blocker modes are mutually exclusive")
    return {
        "minimal_not_testable_antichain": (
            [
                {
                    "node_id": "synthetic.missing",
                    "status": (
                        "PROVED"
                        if scope_mismatch_blocker
                        else "NOT_TESTABLE"
                    ),
                    "role": "STRUCTURAL_CARRIER",
                    "scope_match": not scope_mismatch_blocker,
                    "transitive_ancestor_node_ids": [
                        "synthetic.proved_parent"
                    ],
                }
            ]
            if blocker or scope_mismatch_blocker
            else []
        ),
        "parent_ready_open_frontier": (
            [
                {
                    "node_id": "synthetic.open_arithmetic",
                    "status": "OPEN",
                    "role": "ARITHMETIC_TARGET",
                    "scope_match": True,
                    "all_active_parents_proved": True,
                    "target_level": "L2_ACTUAL_POSITIVE_TARGET",
                }
            ]
            if parent_ready_open
            else []
        ),
        "selection_rule": "synthetic typed frontier",
        "frontiers_are_type_disjoint": True,
    }


def synthetic_routes(
    *,
    selected_stopped: bool = False,
    all_stopped: bool = False,
    complete_universe: bool = False,
    alternative: bool = False,
    fresh_registry: bool = True,
) -> dict[str, Any]:
    classifier_sources: dict[str, Any] = {}
    completeness_source_id = "fixture.synthetic.route_universe.complete"
    crosswalk_source_id = "fixture.synthetic.crosswalk.r1.r2"
    if complete_universe:
        complete_source = source_record(ROUTE_UNIVERSE_FIXTURE)
        classifier_sources[complete_source["source_id"]] = complete_source
    if alternative:
        crosswalk_source = source_record(ROUTE_CROSSWALK_FIXTURE)
        classifier_sources[crosswalk_source["source_id"]] = crosswalk_source
    records: dict[str, Any] = {}
    for route_id, selected in (("r1", True), ("r2", False)):
        stopped = all_stopped or (selected and selected_stopped)
        stop_source_id = None
        if stopped:
            stop_source = synthetic_stop_record(route_id)
            stop_source_id = stop_source["source_id"]
            classifier_sources[stop_source_id] = stop_source
        registry = (
            "registry.r1"
            if selected or not fresh_registry
            else "registry.r2"
        )
        records[route_id] = {
            "selected": selected,
            "stopped": stopped,
            "state": "STOP_SCOPED" if stopped else "OPEN",
            "source_export": stop_source_id,
            "scope_id": "scope.actual",
            "carrier_id": "carrier.actual",
            "normalization_id": "norm.actual",
            "registry_id": registry,
            "coverage": (
                "COMPLETE_DECLARED_ROUTE_CELL"
                if stopped
                else "OPEN_SELECTED_ROUTE"
            ),
        }
    return {
        "routes": ["r1", "r2"],
        "selected_route": "r1",
        "selected_root": "synthetic.root",
        "typed_alternative": "r2" if alternative else None,
        "typed_alternative_crosswalk": (
            crosswalk_source_id if alternative else None
        ),
        "universe_completeness": {
            "status": "PROVED" if complete_universe else "NOT_PROVED",
            "source_export": (
                completeness_source_id
                if complete_universe
                else None
            ),
            "scope": "scope.actual",
        },
        "route_evidence_registry": classifier_sources,
        "records": records,
    }


def synthetic_endpoint(
    *,
    physical_pass: bool,
    full_pass: bool,
) -> dict[str, Any]:
    endpoint = current_endpoint_v3()
    if physical_pass:
        endpoint["literal_audit"] = {
            key: ("STRICT_PASS" if key == "strict_one_over_400_budget" else "PROVED")
            for key in endpoint["literal_audit"]
        }
        endpoint["physical"] = {
            "lambda_required_strict_upper": fraction_record(Fraction(1, 400)),
            "lambda_phys_upper": fraction_record(Fraction(1, 500)),
            "registry_complete": True,
            "unknown_cost_policy": "UNKNOWN_IS_NOT_ZERO",
            "state": "STRICT_PASS",
        }
        source_physical = endpoint["source_nonduplicating_ledger"][
            "ledgers"
        ]["physical"]
        source_physical.update(
            {
                "fixed_X_lambda_upper": fraction_record(Fraction(1, 500)),
                "registry_complete": True,
                "state": "STRICT_PASS",
            }
        )
        endpoint["source_nonduplicating_ledger"]["invariants"][
            "physical_loss_registry_complete"
        ] = True
        for charge in endpoint["source_nonduplicating_ledger"][
            "charge_registry"
        ]:
            if charge["owner_ledger"] == "physical":
                charge["state"] = "PROVED"
                charge["value"] = "certified_future_fixture"
    if full_pass:
        endpoint["arithmetic"].update(
            {
                "deterministic_all_prefix": True,
                "sigma_actual_fixed_X_lower": fraction_record(Fraction(1, 300)),
                "state": "TARGET_CERTIFIED",
            }
        )
        endpoint["full_synthesis"] = {
            "strict_net_slack": fraction_record(Fraction(1, 750)),
            "scope_compatible": True,
            "state": "STRICT_PASS",
        }
        source = endpoint["source_nonduplicating_ledger"]
        source["ledgers"]["arithmetic"].update(
            {
                "fixed_X_sigma": fraction_record(Fraction(1, 300)),
                "state": "TARGET_CERTIFIED",
            }
        )
        source["target"]["one_over_400_paid"] = True
        source["ledgers"]["full_synthesis"].update(
            {
                "net_fixed_X_slack": fraction_record(Fraction(1, 750)),
                "state": "STRICT_PASS",
            }
        )
    return endpoint


def synthetic_state(
    *,
    structural_status: str,
    arithmetic_status: str,
    blocker: bool,
    parent_ready_open: bool,
    routes: dict[str, Any] | None = None,
    physical_pass: bool = False,
    full_pass: bool = False,
    arithmetic_evidence: str = "L2_ACTUAL_POSITIVE_TARGET",
    scope_mismatch_blocker: bool = False,
    evidence_mode: str = SYNTHETIC_REACHABILITY,
) -> dict[str, Any]:
    return {
        "evidence_mode": evidence_mode,
        "gates": synthetic_gates(
            structural_status=structural_status,
            arithmetic_status=arithmetic_status,
            arithmetic_evidence=arithmetic_evidence,
        ),
        "typed_frontiers": synthetic_frontiers(
            blocker=blocker,
            parent_ready_open=parent_ready_open,
            scope_mismatch_blocker=scope_mismatch_blocker,
        ),
        "routes": routes or synthetic_routes(),
        "endpoint_ledger_v3": synthetic_endpoint(
            physical_pass=physical_pass,
            full_pass=full_pass,
        ),
    }


def scenario_regressions() -> dict[str, Any]:
    scenarios = {
        "GO": synthetic_state(
            structural_status="PROVED",
            arithmetic_status="PROVED",
            blocker=False,
            parent_ready_open=False,
            physical_pass=True,
            full_pass=True,
        ),
        "ARCHITECTURE_INFEASIBLE": synthetic_state(
            structural_status="OPEN",
            arithmetic_status="OPEN",
            blocker=False,
            parent_ready_open=True,
            routes=synthetic_routes(
                all_stopped=True,
                complete_universe=True,
            ),
        ),
        "REROUTE": synthetic_state(
            structural_status="REFUTED",
            arithmetic_status="OPEN",
            blocker=False,
            parent_ready_open=True,
            routes=synthetic_routes(
                selected_stopped=True,
                alternative=True,
            ),
        ),
        "STOP_ROUTE": synthetic_state(
            structural_status="REFUTED",
            arithmetic_status="OPEN",
            blocker=False,
            parent_ready_open=True,
            routes=synthetic_routes(selected_stopped=True),
        ),
        "NOT_TESTABLE": synthetic_state(
            structural_status="NOT_TESTABLE",
            arithmetic_status="OPEN",
            blocker=True,
            parent_ready_open=True,
        ),
        "ARITHMETIC_FRONTIER": synthetic_state(
            structural_status="PROVED",
            arithmetic_status="OPEN",
            blocker=False,
            parent_ready_open=True,
            physical_pass=True,
        ),
        "OPEN": synthetic_state(
            structural_status="OPEN",
            arithmetic_status="OPEN",
            blocker=False,
            parent_ready_open=True,
        ),
    }
    outcomes = {name: classify(state) for name, state in scenarios.items()}
    if any(name != outcome for name, outcome in outcomes.items()):
        raise ValueError(f"verdict reachability failure: {outcomes}")

    malformed = copy.deepcopy(scenarios["REROUTE"])
    malformed["routes"]["records"]["r2"]["registry_id"] = (
        malformed["routes"]["records"]["r1"]["registry_id"]
    )
    outcomes["INVALID"] = classify(malformed)
    if outcomes["INVALID"] != "INVALID":
        raise ValueError("outer INVALID scenario is unreachable")

    label_only_crosswalk = copy.deepcopy(scenarios["REROUTE"])
    label_only_crosswalk["routes"]["typed_alternative_crosswalk"] = (
        "theorem.fabricated"
    )
    if classify(label_only_crosswalk) != "INVALID":
        raise ValueError("unregistered reroute crosswalk was accepted")

    no_completeness = synthetic_state(
        structural_status="OPEN",
        arithmetic_status="OPEN",
        blocker=False,
        parent_ready_open=True,
        routes=synthetic_routes(all_stopped=True, complete_universe=False),
    )
    if classify(no_completeness) == "ARCHITECTURE_INFEASIBLE":
        raise ValueError("unproved route universe produced architecture stop")

    fake_completeness = copy.deepcopy(scenarios["ARCHITECTURE_INFEASIBLE"])
    fake_completeness["routes"]["universe_completeness"][
        "source_export"
    ] = "theorem.fabricated"
    if classify(fake_completeness) != "INVALID":
        raise ValueError("unregistered route-universe source was accepted")

    synthetic_as_theorem = copy.deepcopy(
        scenarios["ARCHITECTURE_INFEASIBLE"]
    )
    synthetic_as_theorem["evidence_mode"] = SOURCE_LOCKED
    if classify(synthetic_as_theorem) != "INVALID":
        raise ValueError("synthetic fixture was accepted as theorem evidence")

    hash_drift = copy.deepcopy(scenarios["REROUTE"])
    crosswalk_id = hash_drift["routes"]["typed_alternative_crosswalk"]
    hash_drift["routes"]["route_evidence_registry"][crosswalk_id][
        "canonical_utf8_lf_sha256"
    ] = "0" * 64
    if classify(hash_drift) != "INVALID":
        raise ValueError("classifier source hash drift was accepted")

    scope_mismatch = synthetic_state(
        structural_status="PROVED",
        arithmetic_status="OPEN",
        blocker=False,
        scope_mismatch_blocker=True,
        parent_ready_open=True,
    )
    if classify(scope_mismatch) != "NOT_TESTABLE":
        raise ValueError("scope-mismatch blocker did not produce NT")

    actual_core_only = synthetic_state(
        structural_status="PROVED",
        arithmetic_status="OPEN",
        arithmetic_evidence="L1_ACTUAL_PREFIX_ALMOST_ENDPOINT",
        blocker=False,
        parent_ready_open=True,
        physical_pass=True,
    )
    if classify(actual_core_only) == "ARITHMETIC_FRONTIER":
        raise ValueError("L1 actual core produced pseudo-frontier")

    return {
        "outcomes": outcomes,
        "unproved_route_universe_not_architecture_infeasible": True,
        "route_universe_completeness_requires_registered_source": True,
        "reroute_requires_fresh_registry": True,
        "reroute_crosswalk_requires_registered_source": True,
        "synthetic_sources_are_not_theorem_evidence": True,
        "classifier_source_hashes_verified": True,
        "scope_mismatch_is_a_typed_blocker": True,
        "typed_blocker_and_parent_ready_open_are_distinct": True,
        "L1_actual_core_not_arithmetic_frontier": True,
    }


def mutation_regressions(snapshot: dict[str, Any]) -> dict[str, bool]:
    mutations: dict[str, bool] = {}

    def rejected(name: str, mutate: Any) -> None:
        candidate = copy.deepcopy(snapshot)
        mutate(candidate)
        try:
            validate_snapshot(candidate)
        except (KeyError, TypeError, ValueError):
            mutations[name] = True
        else:
            mutations[name] = False

    rejected(
        "reject_hash_proof_semantics",
        lambda obj: obj["snapshot"].__setitem__("hash_semantics", "PROOF"),
    )
    rejected(
        "reject_current_artifacts_stop_as_actual_impossibility",
        lambda obj: obj["claim_boundary"].__setitem__(
            "current_artifacts_stop_is_actual_carrier_impossibility", True
        ),
    )
    rejected(
        "reject_augmented_map_global_stop",
        lambda obj: obj["imported_state"].__setitem__(
            "occurrence_augmented_map_globally_stopped", True
        ),
    )
    rejected(
        "reject_scalar_plus_ETO_global_stop",
        lambda obj: obj["imported_state"].__setitem__(
            "scalar_plus_ETO_globally_stopped", True
        ),
    )
    rejected(
        "reject_unproved_route_universe_as_complete",
        lambda obj: obj["imported_state"].__setitem__(
            "route_universe_complete", True
        ),
    )
    rejected(
        "reject_fabricated_classifier_source",
        lambda obj: obj["route_universe"][
            "universe_completeness"
        ].update(
            {
                "status": "PROVED",
                "source_export": "theorem.fabricated",
            }
        ),
    )
    rejected(
        "reject_wrong_first_missing",
        lambda obj: obj["typed_frontiers"][
            "minimal_not_testable_antichain"
        ][0].__setitem__("node_id", "H1.frontier_occurrence_lift"),
    )
    rejected(
        "reject_selected_root_antichain_collapse",
        lambda obj: obj["typed_frontiers"].__setitem__(
            "minimal_not_testable_antichain",
            obj["typed_frontiers"]["minimal_not_testable_antichain"][:1],
        ),
    )
    rejected(
        "reject_transitive_ancestry_drift",
        lambda obj: obj["typed_frontiers"][
            "minimal_not_testable_antichain"
        ][0].__setitem__("transitive_ancestor_node_ids", []),
    )
    rejected(
        "reject_frontier_type_merge",
        lambda obj: obj["typed_frontiers"][
            "parent_ready_open_frontier"
        ].append(
            {
                "node_id": FIRST_MISSING,
                "status": "OPEN",
                "role": "ARITHMETIC_TARGET",
                "scope_match": True,
                "all_active_parents_proved": True,
                "target_level": "L2_ACTUAL_POSITIVE_TARGET",
            }
        ),
    )
    rejected(
        "reject_almost_endpoint_as_all_prefix",
        lambda obj: obj["imported_state"].__setitem__(
            "deterministic_all_prefix", True
        ),
    )
    rejected(
        "reject_log_saving_as_positive_fixed_X_power",
        lambda obj: obj["imported_state"].__setitem__(
            "positive_fixed_X_power", True
        ),
    )
    rejected(
        "reject_weighted_interface_as_production_weight",
        lambda obj: obj["imported_state"].__setitem__(
            "production_literal_weight", "PROVED"
        ),
    )
    rejected(
        "reject_endpoint_pass_with_unknown_literal_fields",
        lambda obj: obj["endpoint_ledger_v3"]["physical"].update(
            {
                "lambda_phys_upper": fraction_record(Fraction(1, 500)),
                "registry_complete": True,
                "state": "STRICT_PASS",
            }
        ),
    )
    rejected(
        "reject_positive_X_power_in_current_ledger",
        lambda obj: obj["endpoint_ledger_v3"]["arithmetic"].__setitem__(
            "sigma_actual_fixed_X_lower",
            fraction_record(Fraction(1, 1000)),
        ),
    )
    return mutations


def build_audit(snapshot: dict[str, Any], rendered: str) -> dict[str, Any]:
    checks = validate_snapshot(snapshot)
    scenarios = scenario_regressions()
    mutations = mutation_regressions(snapshot)
    status = (
        all(checks.values())
        and all(
            value
            for key, value in scenarios.items()
            if key != "outcomes"
        )
        and all(mutations.values())
    )
    return {
        "schema": AUDIT_SCHEMA_ID,
        "status": "PASS" if status else "FAIL",
        "snapshot_sha256": rendered_hash(rendered),
        "checks": checks,
        "scenario_verdicts": scenarios["outcomes"],
        "mutation_regressions": mutations,
        "current_verdict": snapshot["current_verdict"],
        "first_missing": snapshot["imported_state"]["first_missing"],
        "claim_boundary": snapshot["claim_boundary"],
    }


def validate_audit_shape(audit: dict[str, Any]) -> None:
    schema = load_json(AUDIT_SCHEMA)
    assert_strict_schema_shape(schema)
    if set(audit) != set(schema["required"]):
        raise ValueError("audit top-level fields differ from schema")
    if audit["schema"] != AUDIT_SCHEMA_ID or audit["status"] != "PASS":
        raise ValueError("audit schema or status drift")
    if audit["current_verdict"] != "NOT_TESTABLE":
        raise ValueError("audit verdict drift")
    if audit["first_missing"] != FIRST_MISSING:
        raise ValueError("audit first-missing pointer drift")


def write_canonical(path: Path, rendered: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="\n") as stream:
        stream.write(rendered)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--check",
        action="store_true",
        help="compare deterministic committed artifacts without writing",
    )
    args = parser.parse_args()
    snapshot = build_snapshot()
    snapshot_rendered = canonical_json(snapshot)
    audit = build_audit(snapshot, snapshot_rendered)
    validate_audit_shape(audit)
    audit_rendered = canonical_json(audit)
    if args.check:
        for path, expected in (
            (SNAPSHOT_PATH, snapshot_rendered),
            (AUDIT_PATH, audit_rendered),
        ):
            if not path.is_file():
                raise SystemExit(f"TPC-162 CHECK FAIL: missing {path.name}")
            existing = normalize_lf(path.read_text(encoding="utf-8"))
            if existing != expected:
                raise SystemExit(f"TPC-162 CHECK FAIL: stale {path.name}")
        print("TPC-162 CHECK PASS")
    else:
        write_canonical(SNAPSHOT_PATH, snapshot_rendered)
        write_canonical(AUDIT_PATH, audit_rendered)
        print("TPC-162 GENERATE PASS")
    print(
        json.dumps(
            {
                "status": audit["status"],
                "verdict": audit["current_verdict"],
                "first_missing": audit["first_missing"],
                "snapshot_sha256": audit["snapshot_sha256"],
            },
            sort_keys=True,
        )
    )
    if audit["status"] != "PASS":
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
