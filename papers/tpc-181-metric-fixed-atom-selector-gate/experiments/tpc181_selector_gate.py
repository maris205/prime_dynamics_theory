#!/usr/bin/env python3
"""Build and audit the TPC-181 metric-to-fixed-atom selector gate."""

from __future__ import annotations

import argparse
import copy
import hashlib
import json
import re
from pathlib import Path
from typing import Any, Callable


HERE = Path(__file__).resolve().parent
PAPER = HERE.parent
REPO = PAPER.parents[1]
MANIFEST_OUTPUT = HERE / "tpc181_selector_gate.json"
AUDIT_OUTPUT = HERE / "tpc181_selector_gate_audit.json"
MANIFEST_SCHEMA = PAPER / "schemas" / "tpc181-selector-gate-v1.schema.json"
AUDIT_SCHEMA = (
    PAPER / "schemas" / "tpc181-selector-gate-audit-v1.schema.json"
)

SOURCE_PATHS = {
    "TPC170.audit": REPO
    / "papers"
    / "tpc-170-metric-packet-corridor-return"
    / "experiments"
    / "tpc170_metric_corridor_audit.json",
    "TPC171.manifest": REPO
    / "papers"
    / "tpc-171-source-locked-occurrence-phase-return-integration"
    / "experiments"
    / "tpc171_integration_manifest.json",
    "TPC172.snapshot": REPO
    / "papers"
    / "tpc-172-mvp7-occurrence-phase-atomic-route-decision"
    / "experiments"
    / "tpc172_mvp7_snapshot.json",
    "TPC180.census": REPO
    / "papers"
    / "tpc-180-production-phase-registry-census"
    / "experiments"
    / "tpc180_phase_registry_census.json",
}

POINTWISE_IDS = [
    "O161.bad_endpoint_pointwise_fixed_atom",
    "O161.direct_additive_twist_fixed_atom",
]


def canonical_bytes(path: Path) -> bytes:
    text = path.read_text(encoding="utf-8-sig")
    text = text.replace("\r\n", "\n").replace("\r", "\n")
    return text.encode("utf-8")


def sha256(path: Path) -> str:
    return hashlib.sha256(canonical_bytes(path)).hexdigest()


def relpath(path: Path) -> str:
    return path.relative_to(REPO).as_posix()


def load_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8-sig"))


def validate_json_schema(
    instance: Any, schema: dict[str, Any], location: str = "$"
) -> None:
    """Validate the Draft-2020-12 subset used by the committed schemas."""

    if "const" in schema and instance != schema["const"]:
        raise ValueError(f"{location}: const mismatch")
    if "enum" in schema and instance not in schema["enum"]:
        raise ValueError(f"{location}: value not in enum")
    expected = schema.get("type")
    if expected is not None:
        matches = {
            "object": isinstance(instance, dict),
            "array": isinstance(instance, list),
            "string": isinstance(instance, str),
            "integer": isinstance(instance, int) and not isinstance(instance, bool),
            "number": (
                isinstance(instance, (int, float))
                and not isinstance(instance, bool)
            ),
            "boolean": isinstance(instance, bool),
            "null": instance is None,
        }.get(expected)
        if matches is not True:
            raise ValueError(f"{location}: expected type {expected}")
    if isinstance(instance, dict):
        required = schema.get("required", [])
        missing = [key for key in required if key not in instance]
        if missing:
            raise ValueError(f"{location}: missing required keys {missing}")
        properties = schema.get("properties", {})
        additional = schema.get("additionalProperties", True)
        for key, value in instance.items():
            if key in properties:
                validate_json_schema(value, properties[key], f"{location}.{key}")
            elif additional is False:
                raise ValueError(f"{location}: unexpected key {key}")
            elif isinstance(additional, dict):
                validate_json_schema(value, additional, f"{location}.{key}")
    if isinstance(instance, list):
        if len(instance) < schema.get("minItems", 0):
            raise ValueError(f"{location}: too few items")
        if "maxItems" in schema and len(instance) > schema["maxItems"]:
            raise ValueError(f"{location}: too many items")
        item_schema = schema.get("items")
        if isinstance(item_schema, dict):
            for index, value in enumerate(instance):
                validate_json_schema(
                    value, item_schema, f"{location}[{index}]"
                )
    if isinstance(instance, str):
        if len(instance) < schema.get("minLength", 0):
            raise ValueError(f"{location}: string too short")
        if "pattern" in schema and re.search(schema["pattern"], instance) is None:
            raise ValueError(f"{location}: pattern mismatch")
    if (
        isinstance(instance, (int, float))
        and not isinstance(instance, bool)
        and "minimum" in schema
        and instance < schema["minimum"]
    ):
        raise ValueError(f"{location}: below minimum")


def validate_schema_file(path: Path, instance: dict[str, Any]) -> None:
    schema = load_json(path)
    if schema.get("$schema") != "https://json-schema.org/draft/2020-12/schema":
        raise ValueError(f"unexpected schema dialect: {path.name}")
    validate_json_schema(instance, schema)


def source_lock(source_id: str, path: Path) -> dict[str, Any]:
    return {
        "source_id": source_id,
        "path": relpath(path),
        "canonical_utf8_lf_sha256": sha256(path),
        "hash_semantics": "INTEGRITY_ONLY",
    }


def find_node(records: list[dict[str, Any]], node_id: str) -> dict[str, Any]:
    matches = [record for record in records if record.get("node_id") == node_id]
    if len(matches) != 1:
        raise ValueError(f"expected one node {node_id!r}, got {len(matches)}")
    return matches[0]


def assert_upstream(payloads: dict[str, dict[str, Any]]) -> dict[str, Any]:
    p170 = payloads["TPC170.audit"]
    p171 = payloads["TPC171.manifest"]
    p172 = payloads["TPC172.snapshot"]
    p180 = payloads["TPC180.census"]

    if (
        p170["status"] != "PASS"
        or p170["packet_borel_cantelli"]["status"]
        != "PROVED_L1_ACTUAL_CORE_PHASE_METRIC_PACKET_CORRIDOR"
        or p170["fixed_atom_stop"]["status"]
        != "PROVED_SCOPED_METRIC_TO_ATOM_NONIMPLICATION"
        or p170["fixed_atom_stop"]["quantifier_proved"]
        != "LEBESGUE_AE_FIXED_PHASE"
        or p170["fixed_atom_stop"]["quantifier_not_proved"]
        != "NAMED_FIXED_ATOM_OR_SCALE_DEPENDENT_SELECTOR"
    ):
        raise ValueError("TPC-170 metric/fixed-atom contract drift")

    bridge = find_node(p171["nodes"], "H2.metric_fixed_atom_crosswalk")
    uncontrolled = find_node(p171["nodes"], "N170.uncontrolled_atomic_promotion")
    if (
        bridge["status"] != "NOT_TESTABLE"
        or bridge["scope_id"] != "scope.source_backed_metric_to_fixed_atom"
        or uncontrolled["status"] != "STOPPED"
        or uncontrolled["scope_id"] != "scope.uncontrolled_atomic_promotion_only"
    ):
        raise ValueError("TPC-171 selector nodes drift")

    open_frontier = p172["typed_frontiers"]["parent_ready_open_frontier"]
    open_by_id = {item["node_id"]: item for item in open_frontier}
    if set(open_by_id) != set(POINTWISE_IDS):
        raise ValueError("TPC-172 pointwise frontier drift")
    if any(open_by_id[node_id]["status"] != "OPEN" for node_id in POINTWISE_IDS):
        raise ValueError("TPC-172 pointwise status drift")

    if (
        p180["status"] != "PASS"
        or p180["decision"]["verdict"] != "NOT_TESTABLE"
        or p180["decision"]["production_phase_registry_constructed"] is not False
        or p180["candidate_registry"]["named_physical_atom_id"] is not None
        or p180["candidate_registry"]["phase_value_mod_1"] is not None
        or p180["candidate_registry"]["phase_value_source_locator"] is not None
    ):
        raise ValueError("TPC-180 missing-registry census drift")

    return {
        "bridge": bridge,
        "uncontrolled": uncontrolled,
        "open_by_id": open_by_id,
    }


def build_payload() -> dict[str, Any]:
    payloads = {key: load_json(path) for key, path in SOURCE_PATHS.items()}
    extracted = assert_upstream(payloads)
    p170 = payloads["TPC170.audit"]
    p180 = payloads["TPC180.census"]

    pointwise_routes = []
    for node_id in POINTWISE_IDS:
        imported = extracted["open_by_id"][node_id]
        pointwise_routes.append(
            {
                "node_id": node_id,
                "state": "OPEN_PARENT_READY",
                "role": imported["role"],
                "quantifier_signature": copy.deepcopy(
                    imported["quantifier_signature"]
                ),
                "stopped_by_metric_nonimplication": False,
            }
        )

    result: dict[str, Any] = {
        "schema": "tpc-181-metric-to-fixed-selector-gate-v1",
        "status": "PASS",
        "snapshot": {
            "date": "2026-07-28",
            "scope": "TPC170_METRIC_THEOREM_TO_NAMED_FIXED_ATOM",
            "hash_mode": "CANONICAL_UTF8_LF_V2",
            "hash_semantics": "INTEGRITY_ONLY",
        },
        "source_locks": [
            source_lock(source_id, path)
            for source_id, path in sorted(SOURCE_PATHS.items())
        ],
        "metric_input": {
            "export_id": p170["packet_borel_cantelli"]["export_id"],
            "status": p170["packet_borel_cantelli"]["status"],
            "phase_quantifier": p170["fixed_atom_stop"]["quantifier_proved"],
            "corridor_uniformity": p170["packet_borel_cantelli"][
                "corridor_uniformity"
            ],
            "scale_quantifier": "EVENTUALLY_PRESCRIBED_SCHEDULE",
            "endpoint_quantifier": "ALL_PREFIX_THETA_SHELL",
            "metric_power": p170["power_corollary"]["admissible_delta"],
            "schedule_dependence": p170["fixed_atom_stop"]["schedule_dependence"],
        },
        "registry_input": {
            "source": "TPC180.census",
            "node_id": "H9.phase_cell_registry",
            "status": p180["candidate_registry"]["status"],
            "named_physical_atom_id": None,
            "phase_value_mod_1": None,
            "phase_value_source_locator": None,
            "production_packet_coordinate_rows": 0,
        },
        "selector_gate": {
            "node_id": "H2.metric_fixed_atom_crosswalk",
            "status": "NOT_TESTABLE",
            "route_kind": "ARITHMETIC_SUBROUTE",
            "scope_id": "SOURCE_BACKED_METRIC_TO_FIXED_ATOM",
            "required_inputs": [
                "source_locked_H9_phase_registry_with_exact_named_atom",
                "exact_prescribed_production_packet_schedule",
                "schedule_specific_named_atom_null_set_avoidance_theorem",
            ],
            "ordered_missing": [
                "H9.phase_cell_registry.named_atom_value_and_locator",
                "H2.metric_fixed_atom_crosswalk.schedule_specific_avoidance_theorem",
            ],
            "selector_constructed": False,
            "fixed_atom_decay_obtained": False,
        },
        "scoped_obstruction": {
            "status": "PROVED_L1_SCOPED_LOGICAL_OBSTRUCTION",
            "stopped_method": "phase_metric_uncontrolled_atomic",
            "scope": "UNCONTROLLED_ATOMIC_PROMOTION_ONLY",
            "statement": (
                "Lebesgue-full eventual good-set membership does not imply "
                "membership of a prescribed singleton phase."
            ),
            "witness": {
                "named_atom": "alpha_star",
                "null_set": "{alpha_star}",
                "null_set_lebesgue_measure": 0,
                "full_measure_good_set": "Torus_without_{alpha_star}",
                "named_atom_in_good_set": False,
            },
            "schedule_specific_form": (
                "TPC170 proves measure(limsup E_n)=0; it does not prove "
                "alpha_star notin limsup E_n for a named alpha_star."
            ),
            "does_not_claim_literal_mobius_lower_bound": True,
            "does_not_stop_pointwise_theorems": True,
            "does_not_stop_architecture": True,
        },
        "source_backed_bridge_contract": {
            "status": "MISSING",
            "minimum_fields": [
                "theorem_id",
                "source_path",
                "source_locator",
                "named_atom_registry_id",
                "exact_phase_value_mod_1",
                "production_schedule_hash",
                "good_set_definition_for_that_schedule",
                "proof_alpha_star_notin_limsup_E_n",
                "same_fixed_alpha_across_scales",
                "coverage_of_all_declared_production_packets",
            ],
            "acceptable_sufficient_hypotheses": [
                {
                    "id": "SCHEDULE_SPECIFIC_EXCEPTIONAL_SET_AVOIDANCE",
                    "statement": (
                        "For the exact source-locked alpha_star and exact "
                        "production schedule, prove alpha_star is outside "
                        "the TPC-170 limsup exceptional set."
                    ),
                },
                {
                    "id": "DIRECT_POINT_EVALUATION_DOMINATION",
                    "statement": (
                        "Prove a source-compatible evaluation/continuity "
                        "bound strong enough to dominate G_n,p(alpha_star) "
                        "by controlled values with a summable error."
                    ),
                },
                {
                    "id": "INDEPENDENT_POINTWISE_FIXED_PHASE_THEOREM",
                    "statement": (
                        "Replace the metric quantifier by a theorem directly "
                        "at the named fixed atom; this exits the metric bridge "
                        "and enters an O161 pointwise route."
                    ),
                },
            ],
            "insufficient_inputs": [
                "Lebesgue_almost_every_phase",
                "phase_L2_average",
                "density_one_finite_registry",
                "phase_chosen_after_reading_the_bad_set",
                "scale_dependent_phase_selector",
                "registry_identity_without_avoidance_theorem",
                "source_hash_without_theorem_statement",
            ],
        },
        "pointwise_routes": pointwise_routes,
        "route_decision": {
            "metric_source_backed_bridge": "NOT_TESTABLE",
            "metric_uncontrolled_atomic": "STOP_SCOPED",
            "return_to_pointwise_frontier": True,
            "pointwise_frontier": POINTWISE_IDS,
            "architecture_reroute": False,
            "reason": (
                "The selector method is blocked, while its scoped "
                "nonimplication does not bear on independent pointwise "
                "fixed-atom estimates."
            ),
        },
        "level_ledger": {
            "L0": (
                "source locks, schema validation, and finite mutation "
                "diagnostics"
            ),
            "L1": (
                "rigorous singleton-versus-a.e. quantifier nonimplication "
                "and typed selector-gate obstruction"
            ),
            "L2": "NONE",
            "metric_delta_below_one_quarter_is_fixed_atom_eligible": False,
            "new_program_positive_L2": False,
        },
        "claim_boundary": {
            "production_phase_registry": False,
            "named_fixed_atom_selected": False,
            "Lebesgue_ae_promoted_to_fixed_atom": False,
            "metric_power_promoted_to_fixed_atom_power": False,
            "scale_dependent_selector_covered": False,
            "pointwise_routes_stopped": False,
            "architecture_stopped": False,
            "program_positive_L2": False,
            "strict_one_over_400": False,
            "prime_pair_lower_bound": False,
            "twin_prime_theorem": False,
        },
        "checks": {
            "tpc170_quantifier_preserved": True,
            "tpc180_missing_registry_preserved": True,
            "singleton_nonimplication_exact": True,
            "schedule_dependence_explicit": True,
            "additional_hypotheses_typed": True,
            "two_O161_routes_open_parent_ready": True,
            "metric_power_not_fixed_atom_power": True,
            "L0_L1_L2_separated": True,
        },
        "mutation_regressions": {},
    }
    result["mutation_regressions"] = mutation_regressions(result)
    validate_payload(result)
    return result


def validate_semantics(obj: dict[str, Any]) -> None:
    expected_top_keys = {
        "schema",
        "status",
        "snapshot",
        "source_locks",
        "metric_input",
        "registry_input",
        "selector_gate",
        "scoped_obstruction",
        "source_backed_bridge_contract",
        "pointwise_routes",
        "route_decision",
        "level_ledger",
        "claim_boundary",
        "checks",
        "mutation_regressions",
    }
    if set(obj) != expected_top_keys:
        raise ValueError("top-level key drift")
    if obj["schema"] != "tpc-181-metric-to-fixed-selector-gate-v1":
        raise ValueError("schema drift")
    if obj["status"] != "PASS":
        raise ValueError("status drift")
    metric = obj["metric_input"]
    if (
        metric["phase_quantifier"] != "LEBESGUE_AE_FIXED_PHASE"
        or metric["scale_quantifier"] != "EVENTUALLY_PRESCRIBED_SCHEDULE"
        or metric["endpoint_quantifier"] != "ALL_PREFIX_THETA_SHELL"
    ):
        raise ValueError("TPC-170 quantifier promotion")
    registry = obj["registry_input"]
    if (
        registry["status"] != "NOT_TESTABLE"
        or registry["named_physical_atom_id"] is not None
        or registry["phase_value_mod_1"] is not None
        or registry["phase_value_source_locator"] is not None
        or registry["production_packet_coordinate_rows"] != 0
    ):
        raise ValueError("missing production registry promoted")
    gate = obj["selector_gate"]
    if (
        gate["node_id"] != "H2.metric_fixed_atom_crosswalk"
        or gate["status"] != "NOT_TESTABLE"
        or gate["selector_constructed"] is not False
        or gate["fixed_atom_decay_obtained"] is not False
    ):
        raise ValueError("selector gate promoted")
    obstruction = obj["scoped_obstruction"]
    if (
        obstruction["status"] != "PROVED_L1_SCOPED_LOGICAL_OBSTRUCTION"
        or obstruction["scope"] != "UNCONTROLLED_ATOMIC_PROMOTION_ONLY"
        or obstruction["witness"]["null_set_lebesgue_measure"] != 0
        or obstruction["witness"]["named_atom_in_good_set"] is not False
        or obstruction["does_not_stop_pointwise_theorems"] is not True
    ):
        raise ValueError("scoped obstruction drift")
    routes = obj["pointwise_routes"]
    if [route["node_id"] for route in routes] != POINTWISE_IDS:
        raise ValueError("pointwise route identity drift")
    if any(
        route["state"] != "OPEN_PARENT_READY"
        or route["stopped_by_metric_nonimplication"] is not False
        or route["quantifier_signature"]["phase_axis"] != "NAMED_FIXED_ATOM"
        or route["quantifier_signature"]["decay_axis"]
        != "FIXED_X_POWER_FIXED_ATOM"
        for route in routes
    ):
        raise ValueError("pointwise route status/signature drift")
    if (
        obj["route_decision"]["metric_uncontrolled_atomic"] != "STOP_SCOPED"
        or obj["route_decision"]["return_to_pointwise_frontier"] is not True
        or obj["route_decision"]["architecture_reroute"] is not False
    ):
        raise ValueError("route decision drift")
    if (
        obj["level_ledger"]["L2"] != "NONE"
        or obj["level_ledger"][
            "metric_delta_below_one_quarter_is_fixed_atom_eligible"
        ]
        is not False
    ):
        raise ValueError("metric result promoted to fixed-atom L2")
    positive_claims = {
        "production_phase_registry",
        "named_fixed_atom_selected",
        "Lebesgue_ae_promoted_to_fixed_atom",
        "metric_power_promoted_to_fixed_atom_power",
        "scale_dependent_selector_covered",
        "pointwise_routes_stopped",
        "architecture_stopped",
        "program_positive_L2",
        "strict_one_over_400",
        "prime_pair_lower_bound",
        "twin_prime_theorem",
    }
    if (
        set(obj["claim_boundary"]) != positive_claims
        or any(obj["claim_boundary"].values())
    ):
        raise ValueError("claim boundary promoted")


def mutation_rejected(
    obj: dict[str, Any], mutate: Callable[[dict[str, Any]], None]
) -> bool:
    changed = copy.deepcopy(obj)
    mutate(changed)
    try:
        validate_semantics(changed)
    except (KeyError, TypeError, ValueError):
        return True
    return False


def mutation_regressions(obj: dict[str, Any]) -> dict[str, bool]:
    return {
        "reject_ae_as_named_atom": mutation_rejected(
            obj,
            lambda value: value["selector_gate"].__setitem__(
                "selector_constructed", True
            ),
        ),
        "reject_missing_registry_as_present": mutation_rejected(
            obj,
            lambda value: value["registry_input"].__setitem__(
                "phase_value_mod_1", 0
            ),
        ),
        "reject_metric_power_as_fixed_atom_power": mutation_rejected(
            obj,
            lambda value: value["level_ledger"].__setitem__(
                "metric_delta_below_one_quarter_is_fixed_atom_eligible", True
            ),
        ),
        "reject_scoped_stop_as_pointwise_stop": mutation_rejected(
            obj,
            lambda value: value["pointwise_routes"][0].__setitem__(
                "stopped_by_metric_nonimplication", True
            ),
        ),
        "reject_scoped_stop_as_architecture_stop": mutation_rejected(
            obj,
            lambda value: value["route_decision"].__setitem__(
                "architecture_reroute", True
            ),
        ),
        "reject_scale_dependent_selector": mutation_rejected(
            obj,
            lambda value: value["claim_boundary"].__setitem__(
                "scale_dependent_selector_covered", True
            ),
        ),
        "reject_extra_positive_claim_field": mutation_rejected(
            obj,
            lambda value: value["claim_boundary"].__setitem__(
                "future_positive_theorem", True
            ),
        ),
    }


def validate_payload(obj: dict[str, Any]) -> None:
    validate_semantics(obj)
    expected_check_keys = {
        "tpc170_quantifier_preserved",
        "tpc180_missing_registry_preserved",
        "singleton_nonimplication_exact",
        "schedule_dependence_explicit",
        "additional_hypotheses_typed",
        "two_O161_routes_open_parent_ready",
        "metric_power_not_fixed_atom_power",
        "L0_L1_L2_separated",
    }
    expected_mutation_keys = {
        "reject_ae_as_named_atom",
        "reject_missing_registry_as_present",
        "reject_metric_power_as_fixed_atom_power",
        "reject_scoped_stop_as_pointwise_stop",
        "reject_scoped_stop_as_architecture_stop",
        "reject_scale_dependent_selector",
        "reject_extra_positive_claim_field",
    }
    if not obj["source_locks"]:
        raise ValueError("empty source locks")
    if any(lock["hash_semantics"] != "INTEGRITY_ONLY" for lock in obj["source_locks"]):
        raise ValueError("hash promoted to theorem evidence")
    if (
        set(obj["checks"]) != expected_check_keys
        or set(obj["checks"].values()) != {True}
    ):
        raise ValueError("one or more checks failed")
    if (
        set(obj["mutation_regressions"]) != expected_mutation_keys
        or set(obj["mutation_regressions"].values()) != {True}
    ):
        raise ValueError("one or more mutation regressions failed")
    validate_schema_file(MANIFEST_SCHEMA, obj)


def render_json(obj: dict[str, Any]) -> str:
    return json.dumps(obj, indent=2, sort_keys=True, ensure_ascii=False) + "\n"


def build_audit(manifest: dict[str, Any], manifest_text: str) -> dict[str, Any]:
    return {
        "schema": "tpc-181-metric-to-fixed-selector-gate-audit-v1",
        "status": "PASS",
        "manifest_schema": manifest["schema"],
        "manifest_payload_sha256": hashlib.sha256(
            manifest_text.encode("utf-8")
        ).hexdigest(),
        "selector_verdict": manifest["selector_gate"]["status"],
        "scoped_stop": manifest["route_decision"]["metric_uncontrolled_atomic"],
        "named_atom_status": (
            "NOT_IDENTIFIED"
            if manifest["registry_input"]["named_physical_atom_id"] is None
            else "IDENTIFIED"
        ),
        "metric_quantifier": manifest["metric_input"]["phase_quantifier"],
        "O161_routes": copy.deepcopy(manifest["pointwise_routes"]),
        "checks": copy.deepcopy(manifest["checks"]),
        "mutation_regressions": copy.deepcopy(manifest["mutation_regressions"]),
        "claim_boundary": copy.deepcopy(manifest["claim_boundary"]),
    }


def validate_audit(audit: dict[str, Any], manifest_text: str) -> None:
    expected_keys = {
        "schema",
        "status",
        "manifest_schema",
        "manifest_payload_sha256",
        "selector_verdict",
        "scoped_stop",
        "named_atom_status",
        "metric_quantifier",
        "O161_routes",
        "checks",
        "mutation_regressions",
        "claim_boundary",
    }
    if set(audit) != expected_keys:
        raise ValueError("audit top-level key drift")
    if audit["schema"] != "tpc-181-metric-to-fixed-selector-gate-audit-v1":
        raise ValueError("audit schema drift")
    if (
        audit["status"] != "PASS"
        or audit["selector_verdict"] != "NOT_TESTABLE"
        or audit["scoped_stop"] != "STOP_SCOPED"
        or audit["named_atom_status"] != "NOT_IDENTIFIED"
        or audit["metric_quantifier"] != "LEBESGUE_AE_FIXED_PHASE"
    ):
        raise ValueError("selector audit state drift")
    if audit["manifest_payload_sha256"] != hashlib.sha256(
        manifest_text.encode("utf-8")
    ).hexdigest():
        raise ValueError("selector audit payload hash drift")
    if [route["node_id"] for route in audit["O161_routes"]] != POINTWISE_IDS:
        raise ValueError("selector audit O161 route drift")
    if any(route["state"] != "OPEN_PARENT_READY" for route in audit["O161_routes"]):
        raise ValueError("selector audit closed an O161 route")
    if set(audit["checks"].values()) != {True}:
        raise ValueError("selector audit checks failed")
    if set(audit["mutation_regressions"].values()) != {True}:
        raise ValueError("selector audit mutation regression failed")
    if any(audit["claim_boundary"].values()):
        raise ValueError("selector audit claim boundary promoted")
    validate_schema_file(AUDIT_SCHEMA, audit)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()

    expected = build_payload()
    expected_text = render_json(expected)
    expected_audit = build_audit(expected, expected_text)
    expected_audit_text = render_json(expected_audit)
    validate_audit(expected_audit, expected_text)
    validate_schema_file(MANIFEST_SCHEMA, expected)
    validate_schema_file(AUDIT_SCHEMA, expected_audit)
    if args.check:
        for path in (MANIFEST_OUTPUT, AUDIT_OUTPUT):
            if not path.exists():
                raise SystemExit(f"missing generated output: {path}")
        actual = load_json(MANIFEST_OUTPUT)
        validate_payload(actual)
        actual_text = MANIFEST_OUTPUT.read_text(encoding="utf-8")
        actual_audit = load_json(AUDIT_OUTPUT)
        validate_audit(actual_audit, actual_text)
        validate_schema_file(MANIFEST_SCHEMA, actual)
        validate_schema_file(AUDIT_SCHEMA, actual_audit)
        if (
            actual_text != expected_text
            or AUDIT_OUTPUT.read_text(encoding="utf-8") != expected_audit_text
        ):
            raise SystemExit("generated outputs are stale; rerun without --check")
        print("TPC-181 check: PASS")
        return 0

    MANIFEST_OUTPUT.write_text(expected_text, encoding="utf-8", newline="\n")
    AUDIT_OUTPUT.write_text(expected_audit_text, encoding="utf-8", newline="\n")
    print(f"wrote {MANIFEST_OUTPUT.relative_to(REPO)}")
    print(f"wrote {AUDIT_OUTPUT.relative_to(REPO)}")
    print("TPC-181 audit: PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
