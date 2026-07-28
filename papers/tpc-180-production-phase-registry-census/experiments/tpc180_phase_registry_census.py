#!/usr/bin/env python3
"""Build and audit the TPC-180 production phase-registry census.

The generator is intentionally negative-data preserving.  It inventories
source-locked fields already present in TPC-157--172, records the proved
fixed-h0=2 core fact, and refuses to manufacture a named phase, locator, or
production packet-coordinate row when those values are absent upstream.
"""

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
MANIFEST_OUTPUT = HERE / "tpc180_phase_registry_census.json"
AUDIT_OUTPUT = HERE / "tpc180_phase_registry_census_audit.json"
MANIFEST_SCHEMA = (
    PAPER / "schemas" / "tpc180-phase-registry-census-v1.schema.json"
)
AUDIT_SCHEMA = (
    PAPER / "schemas" / "tpc180-phase-registry-census-audit-v1.schema.json"
)

SOURCE_PATHS = {
    "TPC157.audit": REPO
    / "papers"
    / "tpc-157-literal-weight-periodic-approximation"
    / "experiments"
    / "tpc157_periodic_approximation_audit.json",
    "TPC158.audit": REPO
    / "papers"
    / "tpc-158-additive-phase-major-minor-gate"
    / "experiments"
    / "tpc158_phase_gate_audit.json",
    "TPC159.audit": REPO
    / "papers"
    / "tpc-159-dyadic-shadow-prefix-lifting"
    / "experiments"
    / "tpc159_dyadic_shadow_audit.json",
    "TPC161.manifest": REPO
    / "papers"
    / "tpc-161-source-locked-occurrence-return-integration"
    / "experiments"
    / "tpc161_occurrence_return_manifest.json",
    "TPC167.audit": REPO
    / "papers"
    / "tpc-167-direct-additive-twist-parseval"
    / "experiments"
    / "tpc167_parseval_audit.json",
    "TPC168.audit": REPO
    / "papers"
    / "tpc-168-separated-phase-registry-sieve"
    / "experiments"
    / "tpc168_registry_sieve_audit.json",
    "TPC169.audit": REPO
    / "papers"
    / "tpc-169-maximal-prefix-phase-metric"
    / "experiments"
    / "tpc169_maximal_prefix_audit.json",
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
}

REQUIRED_PACKET_FIELDS = [
    "ambient_scale_id",
    "packet_id",
    "a",
    "s",
    "d",
    "u",
    "q_equals_a_times_s",
    "determinant_witness_su_minus_ad_equals_2",
    "canonical_representative_id",
    "representative_translation_index",
    "terminal_scale_T",
    "multiplier_source_locator",
    "covariant_multiplier_translation",
    "fiber_coordinate_z",
    "physical_occurrence_locator",
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


def find_record(records: list[dict[str, Any]], key: str, value: str) -> dict[str, Any]:
    matches = [record for record in records if record.get(key) == value]
    if len(matches) != 1:
        raise ValueError(f"expected one record with {key}={value!r}, got {len(matches)}")
    return matches[0]


def assert_upstream(payloads: dict[str, dict[str, Any]]) -> dict[str, Any]:
    p157 = payloads["TPC157.audit"]
    p158 = payloads["TPC158.audit"]
    p159 = payloads["TPC159.audit"]
    p161 = payloads["TPC161.manifest"]
    p167 = payloads["TPC167.audit"]
    p168 = payloads["TPC168.audit"]
    p169 = payloads["TPC169.audit"]
    p170 = payloads["TPC170.audit"]
    p171 = payloads["TPC171.manifest"]
    p172 = payloads["TPC172.snapshot"]

    if p157["status"] != "PASS" or p157["theorem"]["fixed_h0"] != 2:
        raise ValueError("TPC-157 fixed-h0 source fact drift")
    if p159["status"] != "PASS" or p159["theorem"]["fixed_h0"] != 2:
        raise ValueError("TPC-159 fixed-h0 source fact drift")
    if p158["route_decision"]["production_phase_cell"] != "NOT_TESTABLE":
        raise ValueError("TPC-158 production phase-cell status drift")

    artifact161 = find_record(
        p161["registries"]["artifacts"], "key", "artifact.phase_cell_registry"
    )
    node161 = find_record(p161["nodes"], "node_id", "H9.phase_cell_registry")
    if (
        artifact161["status"] != "MISSING"
        or node161["status"] != "NOT_TESTABLE"
        or node161["required_artifact_id"] != "artifact.phase_cell_registry"
    ):
        raise ValueError("TPC-161 phase-registry obligation drift")

    for label, payload, field in [
        ("TPC167", p167, "specified_phase"),
        ("TPC168", p168, "distinguished_phase"),
        ("TPC169", p169, "specified_phase"),
        ("TPC170", p170, "named_fixed_phase"),
    ]:
        if payload["status"] != "PASS" or payload["claim_boundary"][field] is not False:
            raise ValueError(f"{label} named-phase boundary drift")
    if p170["claim_boundary"]["production_phase_registry"] is not False:
        raise ValueError("TPC-170 production phase-registry boundary drift")
    if (
        p170["packet_borel_cantelli"]["status"]
        != "PROVED_L1_ACTUAL_CORE_PHASE_METRIC_PACKET_CORRIDOR"
        or p170["fixed_atom_stop"]["quantifier_proved"]
        != "LEBESGUE_AE_FIXED_PHASE"
        or p170["fixed_atom_stop"]["quantifier_not_proved"]
        != "NAMED_FIXED_ATOM_OR_SCALE_DEPENDENT_SELECTOR"
        or p170["representative_invariance"][
            "requires_covariant_multiplier_translation"
        ]
        is not True
    ):
        raise ValueError("TPC-170 packet/quantifier contract drift")

    node171 = find_record(p171["nodes"], "node_id", "H9.phase_cell_registry")
    metric171 = find_record(p171["nodes"], "node_id", "A170.metric_packet_corridor")
    bridge171 = find_record(p171["nodes"], "node_id", "H2.metric_fixed_atom_crosswalk")
    expected_phase_signature = {
        "carrier_axis": "PHYSICAL_PHASE_REGISTRY",
        "decay_axis": "NONE",
        "endpoint_axis": "NOT_APPLICABLE",
        "phase_axis": "NAMED_FIXED_ATOM",
        "scale_axis": "DETERMINISTIC_ALL_SCALE",
        "support_axis": "ACTUAL_ACTIVE_SUPPORT",
    }
    if (
        node171["status"] != "NOT_TESTABLE"
        or node171["evidence_id"] is not None
        or node171["parents"] != []
        or node171["quantifier_signature"] != expected_phase_signature
    ):
        raise ValueError("TPC-171 H9 phase leaf drift")
    if (
        p171["arithmetic_state"]["production_phase_registry"] is not False
        or p171["arithmetic_state"]["named_fixed_atom"] is not False
        or p171["endpoint_ledger_v4"]["literal_gate"]["fixed_physical_h0"]
        != "PROVED"
        or metric171["quantifier_signature"]["phase_axis"]
        != "LEBESGUE_AE_FIXED_PHASE"
        or bridge171["status"] != "NOT_TESTABLE"
    ):
        raise ValueError("TPC-171 phase bridge/ledger state drift")

    if (
        p172["imported_state"]["production_phase_registry"] is not False
        or p172["imported_state"]["named_fixed_atom"] is not False
        or p172["next_forced_objects"]["metric_bridge"]
        != "H2.metric_fixed_atom_crosswalk"
        or "H9.phase_cell_registry"
        not in p172["next_forced_objects"]["physical_registries"]
    ):
        raise ValueError("TPC-172 forced-object state drift")

    return {
        "tpc161_artifact": artifact161,
        "tpc161_node": node161,
        "tpc171_phase_node": node171,
        "tpc171_metric_node": metric171,
        "tpc171_bridge_node": bridge171,
    }


def build_payload() -> dict[str, Any]:
    payloads = {key: load_json(path) for key, path in SOURCE_PATHS.items()}
    extracted = assert_upstream(payloads)
    p170 = payloads["TPC170.audit"]
    p171 = payloads["TPC171.manifest"]
    p172 = payloads["TPC172.snapshot"]

    locks = [
        source_lock(source_id, path)
        for source_id, path in sorted(SOURCE_PATHS.items())
    ]
    phase_node = extracted["tpc171_phase_node"]
    result: dict[str, Any] = {
        "schema": "tpc-180-production-phase-registry-census-v1",
        "status": "PASS",
        "snapshot": {
            "date": "2026-07-28",
            "scope": "FROZEN_SOURCE_LOCKED_TPC157_172_PHASE_REGISTRY_CORPUS",
            "hash_mode": "CANONICAL_UTF8_LF_V2",
            "hash_semantics": "INTEGRITY_ONLY",
        },
        "source_locks": locks,
        "source_census": {
            "detection_mode": "EXPLICIT_MAPPED_FROZEN_CORPUS_CENSUS",
            "future_new_fields_automatically_scanned": False,
            "mapped_field_count": 7,
            "fixed_h0_records": [
                {
                    "source_id": "TPC157.audit",
                    "locator": {
                        "kind": "JSON_POINTER",
                        "value": "/theorem/fixed_h0",
                    },
                    "value": 2,
                    "status": "PRESENT_SOURCE_BACKED",
                },
                {
                    "source_id": "TPC159.audit",
                    "locator": {
                        "kind": "JSON_POINTER",
                        "value": "/theorem/fixed_h0",
                    },
                    "value": 2,
                    "status": "PRESENT_SOURCE_BACKED",
                },
                {
                    "source_id": "TPC171.manifest",
                    "locator": {
                        "kind": "JSON_POINTER",
                        "value": (
                            "/endpoint_ledger_v4/literal_gate/"
                            "fixed_physical_h0"
                        ),
                    },
                    "value": "PROVED",
                    "status": "PRESENT_SOURCE_BACKED",
                },
            ],
            "phase_obligation_records": [
                {
                    "source_id": "TPC158.audit",
                    "locator": {
                        "kind": "JSON_POINTER",
                        "value": "/route_decision/production_phase_cell",
                    },
                    "value": "NOT_TESTABLE",
                },
                {
                    "source_id": "TPC161.manifest",
                    "locator": {
                        "kind": "QUERY_SELECTOR",
                        "value": (
                            "registries.artifacts[key="
                            "artifact.phase_cell_registry].status"
                        ),
                    },
                    "value": extracted["tpc161_artifact"]["status"],
                },
                {
                    "source_id": "TPC171.manifest",
                    "locator": {
                        "kind": "QUERY_SELECTOR",
                        "value": (
                            "nodes[node_id=H9.phase_cell_registry].status"
                        ),
                    },
                    "value": phase_node["status"],
                },
                {
                    "source_id": "TPC172.snapshot",
                    "locator": {
                        "kind": "JSON_POINTER",
                        "value": (
                            "/imported_state/production_phase_registry"
                        ),
                    },
                    "value": p172["imported_state"]["production_phase_registry"],
                },
            ],
            "value_bearing_named_phase_records": 0,
            "value_bearing_named_phase_locators": 0,
            "production_packet_coordinate_rows": 0,
            "census_semantics": (
                "NO_VALUE_RECORD_IN_EXPLICITLY_MAPPED_FROZEN_FIELDS_"
                "NOT_A_GENERIC_SCAN_OR_MATHEMATICAL_NONEXISTENCE"
            ),
        },
        "registry_contract": {
            "node_id": "H9.phase_cell_registry",
            "status": "NOT_TESTABLE",
            "role": "PHYSICAL_REGISTRY_DATA",
            "quantifier_signature": copy.deepcopy(phase_node["quantifier_signature"]),
            "decay_axis": "NONE",
            "registry_creates_decay": False,
            "required_identity_fields": [
                "named_physical_atom_id",
                "phase_value_mod_1",
                "phase_value_source_locator",
                "fixed_h0_value",
                "fixed_h0_source_locator",
                "packet_schedule_source_locator",
            ],
            "required_packet_coordinate_fields": REQUIRED_PACKET_FIELDS,
            "representative_rule": {
                "equivalence": p170["representative_invariance"]["equation"],
                "actual_representatives_must_be_canonicalized": True,
                "covariant_multiplier_translation_required": p170[
                    "representative_invariance"
                ]["requires_covariant_multiplier_translation"],
                "theorem_status": p170["representative_invariance"]["status"],
                "production_mapping_present": False,
            },
        },
        "candidate_registry": {
            "registry_id": None,
            "named_physical_atom_id": None,
            "phase_value_mod_1": None,
            "phase_value_source_locator": None,
            "fixed_h0_value": 2,
            "fixed_h0_source_locators": [
                "TPC157.audit#/theorem/fixed_h0",
                "TPC159.audit#/theorem/fixed_h0",
                "TPC171.manifest#/endpoint_ledger_v4/literal_gate/fixed_physical_h0",
            ],
            "packet_schedule_source_locator": None,
            "packet_coordinate_rows": [],
            "status": "NOT_TESTABLE",
            "first_missing": "named_physical_atom_id_and_phase_value_source_locator",
        },
        "packet_theorem_interface": {
            "export_id": p170["packet_borel_cantelli"]["export_id"],
            "status": p170["packet_borel_cantelli"]["status"],
            "corridor_uniformity": p170["packet_borel_cantelli"][
                "corridor_uniformity"
            ],
            "phase_quantifier": p170["fixed_atom_stop"]["quantifier_proved"],
            "named_atom_quantifier": p170["fixed_atom_stop"][
                "quantifier_not_proved"
            ],
            "schedule_dependence": p170["fixed_atom_stop"]["schedule_dependence"],
            "production_phase_registry": p170["claim_boundary"][
                "production_phase_registry"
            ],
            "source_locked_physical_packet_map_present": False,
        },
        "decision": {
            "verdict": "NOT_TESTABLE",
            "production_phase_registry_constructed": False,
            "constructible_output": "SOURCE_LOCKED_MISSING_VALUE_CENSUS_AND_SCHEMA_ONLY",
            "first_missing": "named_physical_atom_id_and_phase_value_source_locator",
            "independent_missing": [
                "production_packet_schedule_source_locator",
                "packet_coordinate_rows",
                "canonical_representative_and_covariant_multiplier_mapping",
            ],
            "next_gate": "H2.metric_fixed_atom_crosswalk",
            "pointwise_routes_preserved": p172["next_forced_objects"][
                "arithmetic_alternatives"
            ],
        },
        "level_ledger": {
            "L0": (
                "machine census, strict schema, source hashes, and finite "
                "missing-field diagnostics"
            ),
            "L1": (
                "scoped source-interface conclusion: the frozen corpus does "
                "not instantiate the production phase registry contract"
            ),
            "L2": "NONE",
            "fixed_h0_gate": "PROVED_DATA_FACT_ONLY_NOT_A_CANCELLATION_EXPONENT",
            "new_program_positive_L2": False,
        },
        "claim_boundary": {
            "named_physical_phase_identified": False,
            "phase_value_invented": False,
            "production_packet_schedule_identified": False,
            "production_phase_registry": False,
            "metric_to_fixed_selector": False,
            "fixed_atom_decay": False,
            "program_positive_L2": False,
            "strict_one_over_400": False,
            "prime_pair_lower_bound": False,
            "twin_prime_theorem": False,
            "scoped_census_is_global_nonexistence": False,
        },
        "checks": {
            "all_sources_locked": True,
            "fixed_h0_2_source_backed": True,
            "phase_obligation_not_confused_with_phase_value": True,
            "named_phase_value_and_locator_absent": True,
            "packet_coordinate_rows_absent": True,
            "representative_covariance_requirement_preserved": True,
            "decay_axis_none": True,
            "no_phase_synthesized": True,
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
        "source_census",
        "registry_contract",
        "candidate_registry",
        "packet_theorem_interface",
        "decision",
        "level_ledger",
        "claim_boundary",
        "checks",
        "mutation_regressions",
    }
    if set(obj) != expected_top_keys:
        raise ValueError("top-level key drift")
    if obj["schema"] != "tpc-180-production-phase-registry-census-v1":
        raise ValueError("schema drift")
    if obj["status"] != "PASS":
        raise ValueError("audit status drift")
    census = obj["source_census"]
    if (
        census["detection_mode"]
        != "EXPLICIT_MAPPED_FROZEN_CORPUS_CENSUS"
        or census["future_new_fields_automatically_scanned"] is not False
        or census["mapped_field_count"] != 7
        or census["value_bearing_named_phase_records"] != 0
        or census["value_bearing_named_phase_locators"] != 0
        or census["production_packet_coordinate_rows"] != 0
    ):
        raise ValueError("missing-value census promoted")
    records = census["fixed_h0_records"] + census["phase_obligation_records"]
    if len(records) != census["mapped_field_count"]:
        raise ValueError("mapped field count drift")
    for record in records:
        locator = record.get("locator")
        if (
            not isinstance(locator, dict)
            or set(locator) != {"kind", "value"}
            or locator["kind"] not in {"JSON_POINTER", "QUERY_SELECTOR"}
            or not locator["value"]
        ):
            raise ValueError("typed source locator drift")
    contract = obj["registry_contract"]
    if (
        contract["node_id"] != "H9.phase_cell_registry"
        or contract["status"] != "NOT_TESTABLE"
        or contract["decay_axis"] != "NONE"
        or contract["registry_creates_decay"] is not False
        or contract["quantifier_signature"]["phase_axis"] != "NAMED_FIXED_ATOM"
        or contract["quantifier_signature"]["support_axis"]
        != "ACTUAL_ACTIVE_SUPPORT"
    ):
        raise ValueError("H9 phase registry contract drift")
    candidate = obj["candidate_registry"]
    forbidden_values = [
        candidate["registry_id"],
        candidate["named_physical_atom_id"],
        candidate["phase_value_mod_1"],
        candidate["phase_value_source_locator"],
        candidate["packet_schedule_source_locator"],
    ]
    if any(value is not None for value in forbidden_values):
        raise ValueError("unsourced production phase value synthesized")
    if candidate["packet_coordinate_rows"] != []:
        raise ValueError("unsourced packet-coordinate row synthesized")
    if candidate["fixed_h0_value"] != 2 or candidate["status"] != "NOT_TESTABLE":
        raise ValueError("fixed-h0 or registry status drift")
    if obj["decision"]["production_phase_registry_constructed"] is not False:
        raise ValueError("census promoted to production registry")
    if obj["decision"]["next_gate"] != "H2.metric_fixed_atom_crosswalk":
        raise ValueError("next phase gate drift")
    if obj["level_ledger"]["L2"] != "NONE":
        raise ValueError("registry census promoted to L2")
    expected_boundary_keys = {
        "named_physical_phase_identified",
        "phase_value_invented",
        "production_packet_schedule_identified",
        "production_phase_registry",
        "metric_to_fixed_selector",
        "fixed_atom_decay",
        "program_positive_L2",
        "strict_one_over_400",
        "prime_pair_lower_bound",
        "twin_prime_theorem",
        "scoped_census_is_global_nonexistence",
    }
    if (
        set(obj["claim_boundary"]) != expected_boundary_keys
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
        "reject_obligation_as_phase_value": mutation_rejected(
            obj,
            lambda value: value["candidate_registry"].__setitem__(
                "phase_value_mod_1", 0
            ),
        ),
        "reject_missing_locator_fabrication": mutation_rejected(
            obj,
            lambda value: value["candidate_registry"].__setitem__(
                "phase_value_source_locator", "UNSOURCED"
            ),
        ),
        "reject_synthetic_packet_row": mutation_rejected(
            obj,
            lambda value: value["candidate_registry"]["packet_coordinate_rows"].append(
                {"packet_id": "synthetic"}
            ),
        ),
        "reject_registry_decay_promotion": mutation_rejected(
            obj,
            lambda value: value["registry_contract"].__setitem__(
                "decay_axis", "FIXED_X_POWER_FIXED_ATOM"
            ),
        ),
        "reject_census_as_global_nonexistence": mutation_rejected(
            obj,
            lambda value: value["claim_boundary"].__setitem__(
                "scoped_census_is_global_nonexistence", True
            ),
        ),
        "reject_fixed_h0_fact_as_L2": mutation_rejected(
            obj, lambda value: value["level_ledger"].__setitem__("L2", "PROVED")
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
        "all_sources_locked",
        "fixed_h0_2_source_backed",
        "phase_obligation_not_confused_with_phase_value",
        "named_phase_value_and_locator_absent",
        "packet_coordinate_rows_absent",
        "representative_covariance_requirement_preserved",
        "decay_axis_none",
        "no_phase_synthesized",
    }
    expected_mutation_keys = {
        "reject_obligation_as_phase_value",
        "reject_missing_locator_fabrication",
        "reject_synthetic_packet_row",
        "reject_registry_decay_promotion",
        "reject_census_as_global_nonexistence",
        "reject_fixed_h0_fact_as_L2",
        "reject_extra_positive_claim_field",
    }
    if not obj["source_locks"]:
        raise ValueError("empty source-lock registry")
    if any(lock["hash_semantics"] != "INTEGRITY_ONLY" for lock in obj["source_locks"]):
        raise ValueError("source hash promoted to theorem evidence")
    if (
        set(obj["mutation_regressions"]) != expected_mutation_keys
        or set(obj["mutation_regressions"].values()) != {True}
    ):
        raise ValueError("one or more mutation regressions failed")
    if (
        set(obj["checks"]) != expected_check_keys
        or set(obj["checks"].values()) != {True}
    ):
        raise ValueError("one or more checks failed")
    validate_schema_file(MANIFEST_SCHEMA, obj)


def render_json(obj: dict[str, Any]) -> str:
    return json.dumps(obj, indent=2, sort_keys=True, ensure_ascii=False) + "\n"


def build_audit(manifest: dict[str, Any], manifest_text: str) -> dict[str, Any]:
    return {
        "schema": "tpc-180-production-phase-registry-census-audit-v1",
        "status": "PASS",
        "manifest_schema": manifest["schema"],
        "manifest_payload_sha256": hashlib.sha256(
            manifest_text.encode("utf-8")
        ).hexdigest(),
        "verdict": manifest["decision"]["verdict"],
        "production_phase_registry_constructed": manifest["decision"][
            "production_phase_registry_constructed"
        ],
        "first_missing": manifest["decision"]["first_missing"],
        "source_lock_count": len(manifest["source_locks"]),
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
        "verdict",
        "production_phase_registry_constructed",
        "first_missing",
        "source_lock_count",
        "checks",
        "mutation_regressions",
        "claim_boundary",
    }
    if set(audit) != expected_keys:
        raise ValueError("audit top-level key drift")
    if audit["schema"] != "tpc-180-production-phase-registry-census-audit-v1":
        raise ValueError("audit schema drift")
    if audit["status"] != "PASS" or audit["verdict"] != "NOT_TESTABLE":
        raise ValueError("audit verdict drift")
    if audit["production_phase_registry_constructed"] is not False:
        raise ValueError("audit promoted census to registry")
    if audit["manifest_payload_sha256"] != hashlib.sha256(
        manifest_text.encode("utf-8")
    ).hexdigest():
        raise ValueError("audit manifest payload hash drift")
    if set(audit["checks"].values()) != {True}:
        raise ValueError("audit checks failed")
    if set(audit["mutation_regressions"].values()) != {True}:
        raise ValueError("audit mutation regression failed")
    if any(audit["claim_boundary"].values()):
        raise ValueError("audit claim boundary promoted")
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
        print("TPC-180 check: PASS")
        return 0

    MANIFEST_OUTPUT.write_text(expected_text, encoding="utf-8", newline="\n")
    AUDIT_OUTPUT.write_text(expected_audit_text, encoding="utf-8", newline="\n")
    print(f"wrote {MANIFEST_OUTPUT.relative_to(REPO)}")
    print(f"wrote {AUDIT_OUTPUT.relative_to(REPO)}")
    print("TPC-180 audit: PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
