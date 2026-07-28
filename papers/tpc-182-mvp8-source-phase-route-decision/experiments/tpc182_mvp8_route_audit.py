#!/usr/bin/env python3
"""Build the TPC-182 / MVP8 source--phase route snapshot.

The classifier is deliberately downstream-driven.  It imports the actual
TPC-175, TPC-179, TPC-180, and TPC-181 results and fails closed if the
structural or phase conclusions have been promoted.  Source hashes are
integrity locks only.
"""

from __future__ import annotations

import argparse
import copy
import hashlib
import json
import re
from pathlib import Path
from typing import Any


HERE = Path(__file__).resolve().parent
PAPER = HERE.parent
PAPERS = PAPER.parent
REPO = PAPERS.parent

TPC172 = (
    PAPERS
    / "tpc-172-mvp7-occurrence-phase-atomic-route-decision"
    / "experiments"
    / "tpc172_mvp7_snapshot.json"
)
TPC175 = (
    PAPERS
    / "tpc-175-declared-corpus-local-edge-family"
    / "experiments"
    / "tpc175_local_edge_family.json"
)
TPC176 = (
    PAPERS
    / "tpc-176-source-backed-coverage-gluing-audit"
    / "experiments"
    / "tpc176_coverage_gluing_audit.json"
)
TPC177 = (
    PAPERS
    / "tpc-177-actual-active-support-vacuity-firewall"
    / "experiments"
    / "tpc177_active_support_audit.json"
)
TPC178 = (
    PAPERS
    / "tpc-178-canonical-minimal-representation-eligibility"
    / "experiments"
    / "tpc178_representation_audit.json"
)
TPC179 = (
    PAPERS
    / "tpc-179-h1-structural-corpus-exhaustion-integration"
    / "experiments"
    / "tpc179_h1_integration.json"
)
TPC180 = (
    PAPERS
    / "tpc-180-production-phase-registry-census"
    / "experiments"
    / "tpc180_phase_registry_census.json"
)
TPC181 = (
    PAPERS
    / "tpc-181-metric-fixed-atom-selector-gate"
    / "experiments"
    / "tpc181_selector_gate.json"
)

SNAPSHOT = HERE / "tpc182_mvp8_snapshot.json"
AUDIT = HERE / "tpc182_mvp8_route_audit.json"
SNAPSHOT_SCHEMA = (
    PAPER / "schemas" / "tpc182-mvp8-snapshot-v1.schema.json"
)
AUDIT_SCHEMA = PAPER / "schemas" / "tpc182-mvp8-audit-v1.schema.json"

HASH_MODE = "CANONICAL_UTF8_LF_V2"
SCHEMA_ID = "tpc-182-mvp8-source-phase-route-decision-v1"
AUDIT_SCHEMA_ID = "tpc-182-mvp8-source-phase-route-audit-v1"

STRUCTURAL_ROOTS = [
    "H1.source_backed_local_occurrence_edge_family",
    "H1.actual_active_support_certificate",
    "H1.canonical_minimal_representation_certificate",
]
H9_ROOTS = [
    "H9.literal_weight_registry",
    "H9.phase_cell_registry",
    "H9.endpoint_registry",
    "H9.normalization_registry",
]
POINTWISE_ROUTES = [
    "O161.bad_endpoint_pointwise_fixed_atom",
    "O161.direct_additive_twist_fixed_atom",
]

UPSTREAM_SOURCES = [
    ("TPC172.snapshot", TPC172),
    ("TPC175.local_edge_family", TPC175),
    ("TPC176.coverage_gluing", TPC176),
    ("TPC177.active_support", TPC177),
    ("TPC178.representation", TPC178),
    ("TPC179.h1_integration", TPC179),
    ("TPC180.phase_registry", TPC180),
    ("TPC181.selector_gate", TPC181),
]

CLAIM_BOUNDARY = {
    "scoped_empty_family_is_global_nonexistence": False,
    "empty_gluing_is_production_totality": False,
    "vacuity_closes_active_support": False,
    "archive_address_is_physical_canonicality": False,
    "fixed_h0_data_fact_is_decay": False,
    "phase_registry_is_decay": False,
    "Lebesgue_ae_is_named_fixed_atom": False,
    "metric_power_is_fixed_atom_power": False,
    "scoped_method_stop_is_architecture_stop": False,
    "scoped_method_stop_kills_pointwise_routes": False,
    "program_positive_L2": False,
    "strict_one_over_400": False,
    "prime_pair_lower_bound": False,
    "twin_prime_theorem": False,
}

PROGRESS_CLASSIFICATION = {
    "new_L0_contract_or_machine_diagnostic": True,
    "new_L1_scoped_source_obstruction": True,
    "new_L1_scoped_metric_to_atom_obstruction": True,
    "new_production_local_occurrence_family": False,
    "new_actual_active_support": False,
    "new_canonical_minimal_representation": False,
    "new_named_fixed_atom_theorem": False,
    "new_program_positive_L2": False,
    "strict_one_over_400": False,
}

PROVED_QUANTIFIERS = {
    "carrier_axis": "EXPLICIT_PACKET_CORRIDOR",
    "phase_axis": "LEBESGUE_AE_FIXED_PHASE",
    "endpoint_axis": "ALL_PREFIX_THETA_SHELL",
    "scale_axis": "EVENTUALLY_PRESCRIBED_SCHEDULE",
    "decay_axis": "FIXED_X_POWER_PHASE_METRIC",
    "support_axis": "ACTUAL_CORE",
}

REQUIRED_QUANTIFIERS = {
    "carrier_axis": "ACTUAL_FIXED_H0_PACKET",
    "phase_axis": "NAMED_FIXED_ATOM",
    "endpoint_axis": "DETERMINISTIC_ALL_PREFIX",
    "scale_axis": "DETERMINISTIC_ALL_SCALE",
    "decay_axis": "FIXED_X_POWER_FIXED_ATOM",
    "support_axis": "ACTUAL_ACTIVE_SUPPORT",
}

EXPECTED_MUTATION_NAMES = {
    "reject_scoped_empty_as_global_nonexistence",
    "reject_empty_gluing_as_totality",
    "reject_archive_address_as_physical_canonicality",
    "reject_phase_registry_decay",
    "reject_ae_as_named_atom",
    "reject_metric_power_as_fixed_atom_power",
    "reject_scoped_stop_as_architecture_stop",
    "reject_pointwise_route_stop",
    "reject_named_atom_sigma_promotion",
    "reject_go_without_literal_gate",
    "reject_one_over_400_without_complete_ledger",
    "reject_program_positive_L2_progress",
    "reject_named_atom_theorem_progress",
    "reject_fixed_h0_fact_as_decay",
    "reject_vacuity_as_active_support",
    "reject_scoped_stop_kills_pointwise_routes",
    "reject_program_positive_L2_boundary",
    "reject_empty_source_locks",
    "reject_source_hash_drift",
    "reject_source_hash_as_theorem",
    "reject_occurrence_architecture_stop",
    "reject_upstream_tpc176_unmatched_cut_drift",
    "reject_upstream_tpc176_totality_promotion",
    "reject_upstream_tpc179_architecture_infeasible",
    "reject_upstream_tpc180_global_nonexistence",
    "reject_upstream_tpc180_unsourced_phase_locator",
    "reject_upstream_tpc180_generic_scan_promotion",
    "reject_upstream_tpc180_phase_registry_decay",
    "reject_upstream_tpc181_architecture_stopped",
    "reject_upstream_tpc181_architecture_reroute",
    "reject_upstream_tpc181_pointwise_stop",
}


def normalize(text: str) -> str:
    return text.replace("\r\n", "\n").replace("\r", "\n")


def canonical_json(value: Any) -> str:
    return json.dumps(value, ensure_ascii=False, indent=2, sort_keys=True) + "\n"


def canonical_bytes(path: Path) -> bytes:
    text = normalize(path.read_text(encoding="utf-8"))
    if path.suffix == ".json":
        text = canonical_json(json.loads(text))
    elif not text.endswith("\n"):
        text += "\n"
    return text.encode("utf-8")


def canonical_hash(path: Path) -> str:
    return hashlib.sha256(canonical_bytes(path)).hexdigest()


def rel(path: Path) -> str:
    return path.relative_to(REPO).as_posix()


def load(path: Path) -> dict[str, Any]:
    if not path.is_file():
        raise ValueError(f"missing required upstream: {rel(path)}")
    value = json.loads(normalize(path.read_text(encoding="utf-8")))
    if not isinstance(value, dict):
        raise ValueError(f"object expected: {rel(path)}")
    return value


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
        if len(instance) < schema.get("minProperties", 0):
            raise ValueError(f"{location}: too few properties")
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
    schema = load(path)
    if schema.get("$schema") != "https://json-schema.org/draft/2020-12/schema":
        raise ValueError(f"unexpected schema dialect: {path.name}")
    validate_json_schema(instance, schema)


def source_lock(source_id: str, path: Path) -> dict[str, str]:
    return {
        "source_id": source_id,
        "path": rel(path),
        "canonical_utf8_lf_sha256": canonical_hash(path),
        "hash_mode": HASH_MODE,
        "hash_semantics": "INTEGRITY_ONLY",
    }


def value_at(value: dict[str, Any], *paths: tuple[str, ...]) -> Any:
    """Return the first present nested path, or None.

    This permits the upstream papers to expose both compact and elaborated
    ledgers without weakening the semantic checks below.
    """

    for path in paths:
        current: Any = value
        ok = True
        for key in path:
            if not isinstance(current, dict) or key not in current:
                ok = False
                break
            current = current[key]
        if ok:
            return current
    return None


def require_boundary(
    payload: dict[str, Any],
    *,
    false_fields: set[str],
    true_fields: set[str],
    label: str,
) -> None:
    boundary = payload.get("claim_boundary")
    if not isinstance(boundary, dict):
        raise ValueError(f"{label} claim boundary missing")
    if set(boundary) != false_fields | true_fields:
        raise ValueError(f"{label} claim-boundary key drift")
    if any(boundary[field] is not False for field in false_fields):
        raise ValueError(f"{label} claim boundary promoted")
    if any(boundary[field] is not True for field in true_fields):
        raise ValueError(f"{label} positive scoped fact lost")


def validate_upstreams(
    m172: dict[str, Any],
    f175: dict[str, Any],
    c176: dict[str, Any],
    s177: dict[str, Any],
    r178: dict[str, Any],
    h179: dict[str, Any],
    p180: dict[str, Any],
    g181: dict[str, Any],
) -> None:
    if m172.get("current_verdict") != "NOT_TESTABLE":
        raise ValueError("TPC-172 baseline verdict drift")
    if m172.get("imported_state", {}).get("named_fixed_atom") is not False:
        raise ValueError("TPC-172 named atom was promoted")

    expected_scope = "FROZEN_CONTIGUOUS_OCCURRENCE_SOURCE_CORRIDOR_TPC133_172"
    if (
        f175.get("schema")
        != "tpc-175-declared-corpus-local-edge-family-v1"
        or f175.get("scope") != expected_scope
        or f175.get("status") != "EMPTY_IN_FROZEN_DECLARED_CORPUS"
        or f175.get("family_cardinality") != 0
        or f175.get("qualifying_claim_count") != 0
        or f175.get("eligible_carrier_count") != 0
    ):
        raise ValueError("TPC-175 exact scoped empty-family result drift")
    expected_coverage175 = {
        "coverage_fraction": "0/2988",
        "covered_cut_count": 0,
        "duplicated_cut_count": 0,
        "formal_global_totality_proved": False,
        "production_cut_count": 2988,
        "production_local_patch_present": False,
        "production_overlap_cocycle_testable": False,
        "tpc165_gluing_instantiated": False,
        "unmatched_cut_count": 2988,
    }
    if f175.get("coverage") != expected_coverage175:
        raise ValueError("TPC-175 exact coverage ledger drift")
    h1_175 = f175.get("h1_status", {})
    if (
        h1_175.get(STRUCTURAL_ROOTS[0])
        != "EMPTY_IN_FROZEN_DECLARED_CORPUS"
        or h1_175.get(STRUCTURAL_ROOTS[1]) != "NOT_TESTABLE"
        or h1_175.get(STRUCTURAL_ROOTS[2]) != "NOT_TESTABLE"
        or h1_175.get("actual_carrier_impossibility") is not False
        or h1_175.get("selected_architecture_stopped") is not False
    ):
        raise ValueError("TPC-175 H1 scope or architecture drift")
    require_boundary(
        f175,
        false_fields={
            "actual_active_support_proved",
            "canonical_minimal_representation_proved",
            "empty_family_is_mathematical_nonexistence",
            "fixed_h0_2_edge_theorem_proved",
            "formal_global_totality_proved",
            "named_fixed_phase_theorem",
            "positive_fixed_X_L2",
            "prime_pair_lower_bound",
            "production_local_occurrence_family_nonempty",
            "strict_one_over_400",
            "twin_prime_theorem",
        },
        true_fields=set(),
        label="TPC-175",
    )

    if (
        c176.get("schema")
        != "tpc-176-source-backed-coverage-gluing-audit-v1"
        or c176.get("status") != "PASS"
    ):
        raise ValueError("TPC-176 identity drift")
    input176 = c176.get("input_family", {})
    if (
        input176.get("scope") != expected_scope
        or input176.get("family_status")
        != "EMPTY_IN_FROZEN_DECLARED_CORPUS"
        or input176.get("proved_local_edge_count") != 0
        or input176.get("eligible_carrier_count") != 0
        or input176.get("maximal_in_frozen_declared_corpus") is not True
        or input176.get("mathematical_nonexistence_claim") is not False
    ):
        raise ValueError("TPC-176 imported family scope drift")
    ledger176 = c176.get("coverage_ledger", {})
    expected_counts176 = {
        "covered_carrier_count": 0,
        "covered_cut_count": 0,
        "covered_plus_duplicate_plus_unmatched_carriers": 0,
        "covered_plus_duplicate_plus_unmatched_cuts": 2988,
        "declared_production_cut_count": 2988,
        "duplicate_carrier_count": 0,
        "duplicate_cut_count": 0,
        "eligible_carrier_count": 0,
        "unmatched_carrier_count": 0,
        "unmatched_cut_count": 2988,
    }
    if any(ledger176.get(key) != value for key, value in expected_counts176.items()):
        raise ValueError("TPC-176 exact coverage counts drift")
    if (
        ledger176.get("coverage_universe")
        != "TPC175_FROZEN_PRODUCTION_CUT_ADDRESSES"
        or ledger176.get("partition_identity_verified") is not True
        or ledger176.get("production_totality_proved") is not False
        or ledger176.get("global_physical_carrier_universe_declared") is not False
        or ledger176.get("archive_cut_paths_imported_as_unmatched_carriers")
        is not False
        or ledger176.get("unmatched_cuts_are_actual_physical_carriers")
        is not False
    ):
        raise ValueError("TPC-176 coverage scope promoted")
    gluing176 = c176.get("tpc165_gluing_gate", {})
    if (
        gluing176.get("gluing_theorem_invoked") is not False
        or gluing176.get("nonempty_local_family_precondition_met") is not False
        or gluing176.get("overlap_cocycle_precondition_met") is not False
        or gluing176.get("production_formal_totality_status") != "NOT_TESTABLE"
        or gluing176.get("empty_quotient_promoted_to_formal_totality")
        is not False
    ):
        raise ValueError("TPC-176 gluing gate promotion")
    route176 = c176.get("route_decision", {})
    if (
        route176.get("method_cell_status")
        != "STOP_SCOPED_EMPTY_PROVED_LOCAL_EDGE_FAMILY"
        or route176.get("stop_scope") != expected_scope
        or route176.get("h1_local_edge_root_closed") is not False
        or route176.get("h1_local_edge_root_status") != "NOT_TESTABLE"
        or route176.get("occurrence_augmented_architecture_status")
        != "NOT_TESTABLE"
        or route176.get("occurrence_augmented_architecture_stopped") is not False
    ):
        raise ValueError("TPC-176 scoped stop or architecture drift")
    require_boundary(
        c176,
        false_fields={
            "actual_active_support_proved",
            "canonical_minimal_representation_proved",
            "fixed_h0_2_arithmetic_progress",
            "mathematical_nonexistence_proved",
            "named_fixed_phase_theorem",
            "prime_pair_lower_bound",
            "production_formal_totality_proved",
            "production_local_occurrence_family_proved_nonempty",
            "program_positive_L2",
            "strict_one_over_400",
            "twin_prime_theorem",
        },
        true_fields={
            "fixed_h0_2_preserved_as_requirement",
            "scoped_corpus_exhaustion_proved",
        },
        label="TPC-176",
    )

    support177 = s177.get("h1_active_support_root", {})
    vacuity177 = s177.get("vacuity_firewall", {})
    literal177 = s177.get("h9_literal_weight_separation", {})
    if (
        s177.get("schema")
        != "tpc-177-actual-active-support-vacuity-audit-v1"
        or s177.get("status") != "PASS"
        or s177.get("eligible_domain", {}).get("scope") != expected_scope
        or s177.get("eligible_domain", {}).get("eligible_carrier_count") != 0
        or support177.get("node_id") != STRUCTURAL_ROOTS[1]
        or support177.get("status") != "NOT_TESTABLE"
        or support177.get("closed") is not False
        or vacuity177.get("existential_active_support_proved") is not False
        or literal177.get("node_id") != "H9.literal_weight_registry"
        or literal177.get("registry_closed_by_tpc177") is not False
        or literal177.get("decay_axis") != "NONE"
    ):
        raise ValueError("TPC-177 support/vacuity/H9 separation drift")
    coefficient177 = s177.get("coefficient_audit", {})
    if (
        coefficient177.get("tested_eligible_carrier_count") != 0
        or coefficient177.get("universal_statement_is_vacuous") is not True
        or coefficient177.get("universal_all_eligible_carriers_active") is not True
    ):
        raise ValueError("TPC-177 empty-domain semantics drift")
    require_boundary(
        s177,
        false_fields={
            "active_carrier_mathematical_nonexistence_proved",
            "actual_active_support_proved",
            "fixed_h0_2_arithmetic_progress",
            "h9_literal_weight_registry_closed",
            "named_fixed_phase_theorem",
            "prime_pair_lower_bound",
            "production_local_occurrence_family_proved_nonempty",
            "program_positive_L2",
            "strict_one_over_400",
            "twin_prime_theorem",
        },
        true_fields={
            "empty_domain_audit_passed",
            "fixed_h0_2_preserved_as_requirement",
        },
        label="TPC-177",
    )

    root178 = r178.get("h1_representation_root", {})
    audit178 = r178.get("representation_audit", {})
    archive178 = r178.get("archive_key_import", {})
    if (
        r178.get("schema")
        != "tpc-178-canonical-minimal-representation-audit-v1"
        or r178.get("status") != "PASS"
        or r178.get("eligible_domain", {}).get("scope") != expected_scope
        or r178.get("eligible_domain", {}).get("eligible_physical_carrier_count")
        != 0
        or root178.get("node_id") != STRUCTURAL_ROOTS[2]
        or root178.get("status") != "NOT_TESTABLE"
        or root178.get("closed") is not False
        or audit178.get("status") != "ELIGIBILITY_BLOCKED_EMPTY_CARRIER_DOMAIN"
        or audit178.get("canonicality_proved") is not False
        or audit178.get("minimality_proved") is not False
        or archive178.get("role") != "ARCHIVE_ADDRESS"
        or archive178.get("canonical_physical_representation") is not False
        or archive178.get("minimal_physical_representation") is not False
        or archive178.get("occurrence_identifier") is not False
    ):
        raise ValueError("TPC-178 representation/archive scope drift")
    require_boundary(
        r178,
        false_fields={
            "actual_active_support_proved",
            "actual_occurrence_identifier_proved",
            "canonical_minimal_representation_proved",
            "fixed_h0_2_arithmetic_progress",
            "named_fixed_phase_theorem",
            "noncanonical_physical_counterexample_proved",
            "prime_pair_lower_bound",
            "program_positive_L2",
            "strict_one_over_400",
            "twin_prime_theorem",
        },
        true_fields={
            "archive_row_separation_proved",
            "fixed_h0_2_preserved_as_requirement",
        },
        label="TPC-178",
    )

    if (
        h179.get("schema")
        != "tpc-179-h1-structural-corpus-exhaustion-integration-v1"
        or h179.get("scope") != expected_scope
        or h179.get("status") != "PASS"
        or h179.get("current_verdict") != "NOT_TESTABLE"
        or h179.get("first_missing") != STRUCTURAL_ROOTS[0]
        or h179.get("minimal_root_antichain") != STRUCTURAL_ROOTS
    ):
        raise ValueError("TPC-179 structural identity/frontier drift")
    fixed179 = h179.get("fixed_h0", {})
    if (
        fixed179.get("required_physical_value") != 2
        or fixed179.get("requirement_preserved") is not True
        or fixed179.get("fixed_h0_arithmetic_progress") is not False
        or fixed179.get("used_as_arithmetic_evidence") is not False
    ):
        raise ValueError("TPC-179 fixed-h0 boundary drift")
    cells179 = {
        cell.get("cell_id"): cell for cell in h179.get("scoped_route_cells", [])
    }
    if set(cells179) != {
        "production_local_edge_extraction_from_tpc133_172",
        "occurrence_augmented_h1_architecture",
    }:
        raise ValueError("TPC-179 route-cell identity drift")
    extraction179 = cells179["production_local_edge_extraction_from_tpc133_172"]
    architecture179 = cells179["occurrence_augmented_h1_architecture"]
    if (
        extraction179.get("status") != "STOP_SCOPED"
        or extraction179.get("scope") != expected_scope
        or extraction179.get("global_infeasibility_proved") is not False
        or extraction179.get("complete_architecture") is not False
        or architecture179.get("status") != "NOT_TESTABLE"
        or architecture179.get("complete_architecture") is not True
        or architecture179.get("global_infeasibility_proved") is not False
    ):
        raise ValueError("TPC-179 scoped stop or architecture promotion")
    require_boundary(
        h179,
        false_fields={
            "actual_active_support_proved",
            "architecture_infeasible",
            "canonical_minimal_representation_proved",
            "fixed_h0_2_arithmetic_progress",
            "formal_global_totality_proved",
            "mathematical_nonexistence_proved",
            "named_fixed_phase_theorem",
            "occurrence_augmented_architecture_stopped",
            "prime_pair_lower_bound",
            "production_local_occurrence_family_proved_nonempty",
            "program_positive_L2",
            "strict_one_over_400",
            "twin_prime_theorem",
        },
        true_fields={
            "fixed_h0_2_preserved_as_requirement",
            "l1_scoped_corpus_exhaustion",
            "scoped_extraction_cell_stopped",
            "three_root_h1_antichain_recomputed",
        },
        label="TPC-179",
    )

    if (
        p180.get("schema")
        != "tpc-180-production-phase-registry-census-v1"
        or p180.get("status") != "PASS"
        or p180.get("snapshot", {}).get("scope")
        != "FROZEN_SOURCE_LOCKED_TPC157_172_PHASE_REGISTRY_CORPUS"
        or p180.get("snapshot", {}).get("hash_semantics") != "INTEGRITY_ONLY"
    ):
        raise ValueError("TPC-180 identity/scope drift")
    census180 = p180.get("source_census", {})
    if (
        census180.get("detection_mode")
        != "EXPLICIT_MAPPED_FROZEN_CORPUS_CENSUS"
        or census180.get("future_new_fields_automatically_scanned") is not False
        or census180.get("mapped_field_count") != 7
        or len(census180.get("fixed_h0_records", [])) != 3
        or len(census180.get("phase_obligation_records", [])) != 4
        or census180.get("value_bearing_named_phase_records") != 0
        or census180.get("value_bearing_named_phase_locators") != 0
        or census180.get("production_packet_coordinate_rows") != 0
        or census180.get("census_semantics")
        != (
            "NO_VALUE_RECORD_IN_EXPLICITLY_MAPPED_FROZEN_FIELDS_"
            "NOT_A_GENERIC_SCAN_OR_MATHEMATICAL_NONEXISTENCE"
        )
    ):
        raise ValueError("TPC-180 mapped-field census scope drift")
    expected_fixed_records180 = [
        ("TPC157.audit", "JSON_POINTER", "/theorem/fixed_h0", 2),
        ("TPC159.audit", "JSON_POINTER", "/theorem/fixed_h0", 2),
        (
            "TPC171.manifest",
            "JSON_POINTER",
            "/endpoint_ledger_v4/literal_gate/fixed_physical_h0",
            "PROVED",
        ),
    ]
    actual_fixed_records180 = [
        (
            row.get("source_id"),
            row.get("locator", {}).get("kind"),
            row.get("locator", {}).get("value"),
            row.get("value"),
        )
        for row in census180.get("fixed_h0_records", [])
    ]
    expected_phase_records180 = [
        (
            "TPC158.audit",
            "JSON_POINTER",
            "/route_decision/production_phase_cell",
            "NOT_TESTABLE",
        ),
        (
            "TPC161.manifest",
            "QUERY_SELECTOR",
            "registries.artifacts[key=artifact.phase_cell_registry].status",
            "MISSING",
        ),
        (
            "TPC171.manifest",
            "QUERY_SELECTOR",
            "nodes[node_id=H9.phase_cell_registry].status",
            "NOT_TESTABLE",
        ),
        (
            "TPC172.snapshot",
            "JSON_POINTER",
            "/imported_state/production_phase_registry",
            False,
        ),
    ]
    actual_phase_records180 = [
        (
            row.get("source_id"),
            row.get("locator", {}).get("kind"),
            row.get("locator", {}).get("value"),
            row.get("value"),
        )
        for row in census180.get("phase_obligation_records", [])
    ]
    if (
        actual_fixed_records180 != expected_fixed_records180
        or actual_phase_records180 != expected_phase_records180
    ):
        raise ValueError("TPC-180 mapped field locator/value drift")
    candidate180 = p180.get("candidate_registry", {})
    if (
        candidate180.get("status") != "NOT_TESTABLE"
        or candidate180.get("fixed_h0_value") != 2
        or candidate180.get("registry_id") is not None
        or candidate180.get("named_physical_atom_id") is not None
        or candidate180.get("phase_value_mod_1") is not None
        or candidate180.get("phase_value_source_locator") is not None
        or candidate180.get("packet_schedule_source_locator") is not None
        or candidate180.get("packet_coordinate_rows") != []
        or candidate180.get("first_missing")
        != "named_physical_atom_id_and_phase_value_source_locator"
    ):
        raise ValueError("TPC-180 registry facts were promoted or lost")
    contract180 = p180.get("registry_contract", {})
    if (
        contract180.get("node_id") != "H9.phase_cell_registry"
        or contract180.get("status") != "NOT_TESTABLE"
        or contract180.get("role") != "PHYSICAL_REGISTRY_DATA"
        or contract180.get("decay_axis") != "NONE"
        or contract180.get("registry_creates_decay") is not False
        or contract180.get("quantifier_signature", {}).get("phase_axis")
        != "NAMED_FIXED_ATOM"
        or contract180.get("quantifier_signature", {}).get("support_axis")
        != "ACTUAL_ACTIVE_SUPPORT"
        or contract180.get("representative_rule", {}).get(
            "production_mapping_present"
        )
        is not False
    ):
        raise ValueError("TPC-180 phase-registry contract drift")
    decision180 = p180.get("decision", {})
    if (
        decision180.get("verdict") != "NOT_TESTABLE"
        or decision180.get("production_phase_registry_constructed") is not False
        or decision180.get("first_missing")
        != "named_physical_atom_id_and_phase_value_source_locator"
        or decision180.get("next_gate") != "H2.metric_fixed_atom_crosswalk"
        or decision180.get("pointwise_routes_preserved") != POINTWISE_ROUTES
        or p180.get("level_ledger", {}).get("L2") != "NONE"
        or p180.get("level_ledger", {}).get("new_program_positive_L2") is not False
    ):
        raise ValueError("TPC-180 decision/level drift")
    require_boundary(
        p180,
        false_fields={
            "fixed_atom_decay",
            "metric_to_fixed_selector",
            "named_physical_phase_identified",
            "phase_value_invented",
            "prime_pair_lower_bound",
            "production_packet_schedule_identified",
            "production_phase_registry",
            "program_positive_L2",
            "scoped_census_is_global_nonexistence",
            "strict_one_over_400",
            "twin_prime_theorem",
        },
        true_fields=set(),
        label="TPC-180",
    )

    if (
        g181.get("schema") != "tpc-181-metric-to-fixed-selector-gate-v1"
        or g181.get("status") != "PASS"
        or g181.get("snapshot", {}).get("scope")
        != "TPC170_METRIC_THEOREM_TO_NAMED_FIXED_ATOM"
        or g181.get("snapshot", {}).get("hash_semantics") != "INTEGRITY_ONLY"
    ):
        raise ValueError("TPC-181 identity/scope drift")
    metric181 = g181.get("metric_input", {})
    if (
        metric181.get("phase_quantifier") != "LEBESGUE_AE_FIXED_PHASE"
        or metric181.get("scale_quantifier")
        != "EVENTUALLY_PRESCRIBED_SCHEDULE"
        or metric181.get("endpoint_quantifier") != "ALL_PREFIX_THETA_SHELL"
        or metric181.get("metric_power") != "every delta<1/4"
    ):
        raise ValueError("TPC-181 metric quantifier drift")
    registry181 = g181.get("registry_input", {})
    if (
        registry181.get("node_id") != "H9.phase_cell_registry"
        or registry181.get("status") != "NOT_TESTABLE"
        or registry181.get("named_physical_atom_id") is not None
        or registry181.get("phase_value_mod_1") is not None
        or registry181.get("phase_value_source_locator") is not None
        or registry181.get("production_packet_coordinate_rows") != 0
    ):
        raise ValueError("TPC-181 registry input promoted")
    selector181 = g181.get("selector_gate", {})
    if (
        selector181.get("node_id") != "H2.metric_fixed_atom_crosswalk"
        or selector181.get("status") != "NOT_TESTABLE"
        or selector181.get("route_kind") != "ARITHMETIC_SUBROUTE"
        or selector181.get("scope_id") != "SOURCE_BACKED_METRIC_TO_FIXED_ATOM"
        or selector181.get("selector_constructed") is not False
        or selector181.get("fixed_atom_decay_obtained") is not False
    ):
        raise ValueError("TPC-181 selector gate promoted")
    obstruction181 = g181.get("scoped_obstruction", {})
    if (
        obstruction181.get("status")
        != "PROVED_L1_SCOPED_LOGICAL_OBSTRUCTION"
        or obstruction181.get("scope") != "UNCONTROLLED_ATOMIC_PROMOTION_ONLY"
        or obstruction181.get("stopped_method")
        != "phase_metric_uncontrolled_atomic"
        or obstruction181.get("does_not_stop_architecture") is not True
        or obstruction181.get("does_not_stop_pointwise_theorems") is not True
        or obstruction181.get("witness", {}).get("named_atom_in_good_set")
        is not False
        or obstruction181.get("witness", {}).get("null_set_lebesgue_measure")
        != 0
    ):
        raise ValueError("TPC-181 scoped obstruction drift")
    pointwise181 = g181.get("pointwise_routes", [])
    if [row.get("node_id") for row in pointwise181] != POINTWISE_ROUTES or any(
        row.get("state") != "OPEN_PARENT_READY"
        or row.get("role") != "ARITHMETIC_TARGET"
        or row.get("stopped_by_metric_nonimplication") is not False
        or row.get("quantifier_signature") != REQUIRED_QUANTIFIERS
        for row in pointwise181
    ):
        raise ValueError("TPC-181 pointwise frontier drift")
    decision181 = g181.get("route_decision", {})
    if (
        decision181.get("metric_uncontrolled_atomic") != "STOP_SCOPED"
        or decision181.get("metric_source_backed_bridge") != "NOT_TESTABLE"
        or decision181.get("pointwise_frontier") != POINTWISE_ROUTES
        or decision181.get("return_to_pointwise_frontier") is not True
        or decision181.get("architecture_reroute") is not False
        or g181.get("level_ledger", {}).get("L2") != "NONE"
        or g181.get("level_ledger", {}).get(
            "metric_delta_below_one_quarter_is_fixed_atom_eligible"
        )
        is not False
        or g181.get("level_ledger", {}).get("new_program_positive_L2") is not False
    ):
        raise ValueError("TPC-181 selector decision or level drift")
    require_boundary(
        g181,
        false_fields={
            "Lebesgue_ae_promoted_to_fixed_atom",
            "architecture_stopped",
            "metric_power_promoted_to_fixed_atom_power",
            "named_fixed_atom_selected",
            "pointwise_routes_stopped",
            "prime_pair_lower_bound",
            "production_phase_registry",
            "program_positive_L2",
            "scale_dependent_selector_covered",
            "strict_one_over_400",
            "twin_prime_theorem",
        },
        true_fields=set(),
        label="TPC-181",
    )


def build_snapshot() -> tuple[dict[str, Any], dict[str, Any]]:
    for schema in (SNAPSHOT_SCHEMA, AUDIT_SCHEMA):
        if not schema.is_file():
            raise ValueError(f"missing schema: {rel(schema)}")

    m172 = load(TPC172)
    f175 = load(TPC175)
    c176 = load(TPC176)
    s177 = load(TPC177)
    r178 = load(TPC178)
    h179 = load(TPC179)
    p180 = load(TPC180)
    g181 = load(TPC181)
    validate_upstreams(m172, f175, c176, s177, r178, h179, p180, g181)

    source_locks = [
        source_lock(source_id, path) for source_id, path in UPSTREAM_SOURCES
    ]

    blockers = copy.deepcopy(
        m172["typed_frontiers"]["minimal_not_testable_antichain"]
    )
    blocker_ids = [row["node_id"] for row in blockers]
    if blocker_ids != STRUCTURAL_ROOTS + H9_ROOTS:
        raise ValueError("MVP7 blocker order drift")
    pointwise_frontier = copy.deepcopy(g181["pointwise_routes"])

    route_cells = {
        "architecture": {
            "occurrence_augmented_map": {
                "route_kind": "ARCHITECTURE_ROUTE",
                "state": "OPEN_NOT_TESTABLE",
                "stopped": False,
            },
            "current_declared_corpus_edge_extraction": {
                "route_kind": "ARCHITECTURE_SOURCE_CELL",
                "scope_id": (
                    "FROZEN_CONTIGUOUS_OCCURRENCE_SOURCE_CORRIDOR_TPC133_172"
                ),
                "state": "STOP_SCOPED",
                "stopped": True,
                "architecture_stopped": False,
                "fresh_source_or_new_theorem_can_reopen": True,
            },
        },
        "arithmetic_subroutes": {
            "phase_metric_uncontrolled_atomic": {
                "route_kind": "ARITHMETIC_SUBROUTE",
                "scope_id": "UNCONTROLLED_ATOMIC_PROMOTION_ONLY",
                "state": "STOP_SCOPED",
            },
            "phase_metric_source_backed": {
                "route_kind": "ARITHMETIC_SUBROUTE",
                "scope_id": "SOURCE_BACKED_METRIC_TO_FIXED_ATOM",
                "state": "OPEN_NOT_TESTABLE",
            },
            "bad_endpoint_pointwise_fixed_atom": {
                "route_kind": "ARITHMETIC_SUBROUTE",
                "state": "OPEN_PARENT_READY",
            },
            "direct_additive_twist_fixed_atom": {
                "route_kind": "ARITHMETIC_SUBROUTE",
                "state": "OPEN_PARENT_READY",
            },
        },
    }

    endpoint_ledger = {
        "contract": "MVP8_FIXED_H0_NON_DUPLICATING_ENDPOINT_V5",
        "sigma_required": {"numerator": 1, "denominator": 400},
        "named_fixed_atom_sigma": {"numerator": 0, "denominator": 1},
        "phase_metric_sigma": "every delta<1/4",
        "phase_metric_sigma_scope": (
            "LEBESGUE_AE_EVENTUALLY_PRESCRIBED_PACKET_SCHEDULE"
        ),
        "phase_metric_eligible_for_named_atom_charge": False,
        "literal_gate": {
            "literal_physical_coefficients": "NOT_TESTABLE",
            "fixed_physical_h0": "PROVED_DATA_FACT_ONLY",
            "physical_atomic_normalization": "NOT_TESTABLE",
            "canonical_or_minimal_representation": "NOT_TESTABLE",
            "actual_active_support": "NOT_TESTABLE",
            "strict_one_over_400_budget": "NOT_TESTABLE",
        },
        "registry_gate": {
            "source_backed_local_occurrence_edge_family": "NOT_TESTABLE",
            "actual_active_support_certificate": "NOT_TESTABLE",
            "canonical_minimal_representation_certificate": "NOT_TESTABLE",
            "literal_weight_registry": "NOT_TESTABLE",
            "phase_cell_registry": "NOT_TESTABLE",
            "endpoint_registry": "NOT_TESTABLE",
            "normalization_registry": "NOT_TESTABLE",
        },
        "strict_net_slack": None,
        "one_over_400_paid": False,
        "state": "INCOMPLETE",
    }

    snapshot = {
        "schema": SCHEMA_ID,
        "snapshot": {
            "date": "2026-07-28",
            "hash_mode": HASH_MODE,
            "hash_semantics": "INTEGRITY_ONLY",
            "classifier_evidence_mode": "SOURCE_LOCKED",
        },
        "source_locks": source_locks,
        "current_verdict": "NOT_TESTABLE",
        "first_missing": STRUCTURAL_ROOTS[0],
        "structural_result": {
            "declared_corpus_scope": (
                "FROZEN_CONTIGUOUS_OCCURRENCE_SOURCE_CORRIDOR_TPC133_172"
            ),
            "qualifying_local_edge_count": 0,
            "scoped_extraction_cell": "STOP_SCOPED",
            "global_architecture_status": "OPEN_NOT_TESTABLE",
            "covered_cut_count": 0,
            "production_cut_count": 2988,
            "unmatched_cut_count": 2988,
            "actual_active_support": "NOT_TESTABLE",
            "canonical_minimal_representation": "NOT_TESTABLE",
            "minimal_root_antichain": STRUCTURAL_ROOTS,
        },
        "phase_result": {
            "fixed_h0": 2,
            "fixed_h0_semantics": "SOURCE_BACKED_DATA_FACT_ONLY",
            "production_phase_registry": "NOT_TESTABLE",
            "named_physical_atom": False,
            "production_packet_coordinate_rows": 0,
            "proved_phase_quantifier": "LEBESGUE_AE_FIXED_PHASE",
            "required_phase_quantifier": "NAMED_FIXED_ATOM",
            "metric_source_backed_bridge": "NOT_TESTABLE",
            "metric_uncontrolled_atomic": "STOP_SCOPED",
            "pointwise_routes": POINTWISE_ROUTES,
        },
        "typed_frontiers": {
            "minimal_not_testable_antichain": blockers,
            "parent_ready_open_frontier": pointwise_frontier,
            "frontiers_are_type_disjoint": True,
        },
        "route_cells": route_cells,
        "endpoint_ledger_v5": endpoint_ledger,
        "quantifier_projection": {
            "proved": copy.deepcopy(PROVED_QUANTIFIERS),
            "required": copy.deepcopy(REQUIRED_QUANTIFIERS),
            "promotion_complete": False,
            "failed_axes": [
                "carrier_axis",
                "phase_axis",
                "endpoint_axis",
                "scale_axis",
                "decay_axis",
                "support_axis",
            ],
        },
        "progress_classification": copy.deepcopy(PROGRESS_CLASSIFICATION),
        "next_forced_objects": {
            "structural": (
                "NEW_EXPLICIT_SOURCE_CORPUS_OR_NEW_THEOREM_BACKED_LOCAL_EDGE"
            ),
            "phase_bridge": (
                "SOURCE_LOCKED_NAMED_ATOM_PLUS_SCHEDULE_SPECIFIC_AVOIDANCE"
            ),
            "pointwise_arithmetic": POINTWISE_ROUTES,
        },
        "claim_boundary": copy.deepcopy(CLAIM_BOUNDARY),
    }
    validate_snapshot(snapshot)

    mutations: dict[str, bool] = {}

    def reject(name: str, mutate: Any) -> None:
        trial = copy.deepcopy(snapshot)
        mutate(trial)
        try:
            validate_snapshot(trial)
        except (KeyError, TypeError, ValueError):
            mutations[name] = True
        else:
            mutations[name] = False

    upstreams = [m172, f175, c176, s177, r178, h179, p180, g181]

    def reject_upstream(name: str, index: int, mutate: Any) -> None:
        trial = copy.deepcopy(upstreams)
        mutate(trial[index])
        try:
            validate_upstreams(*trial)
        except (KeyError, TypeError, ValueError):
            mutations[name] = True
        else:
            mutations[name] = False

    reject(
        "reject_scoped_empty_as_global_nonexistence",
        lambda obj: obj["claim_boundary"].update(
            {"scoped_empty_family_is_global_nonexistence": True}
        ),
    )
    reject(
        "reject_empty_gluing_as_totality",
        lambda obj: obj["claim_boundary"].update(
            {"empty_gluing_is_production_totality": True}
        ),
    )
    reject(
        "reject_archive_address_as_physical_canonicality",
        lambda obj: obj["claim_boundary"].update(
            {"archive_address_is_physical_canonicality": True}
        ),
    )
    reject(
        "reject_phase_registry_decay",
        lambda obj: obj["claim_boundary"].update(
            {"phase_registry_is_decay": True}
        ),
    )
    reject(
        "reject_ae_as_named_atom",
        lambda obj: obj["claim_boundary"].update(
            {"Lebesgue_ae_is_named_fixed_atom": True}
        ),
    )
    reject(
        "reject_metric_power_as_fixed_atom_power",
        lambda obj: obj["endpoint_ledger_v5"].update(
            {"phase_metric_eligible_for_named_atom_charge": True}
        ),
    )
    reject(
        "reject_scoped_stop_as_architecture_stop",
        lambda obj: obj["route_cells"]["architecture"][
            "current_declared_corpus_edge_extraction"
        ].update({"architecture_stopped": True}),
    )
    reject(
        "reject_pointwise_route_stop",
        lambda obj: obj["route_cells"]["arithmetic_subroutes"][
            "direct_additive_twist_fixed_atom"
        ].update({"state": "STOP_SCOPED"}),
    )
    reject(
        "reject_named_atom_sigma_promotion",
        lambda obj: obj["endpoint_ledger_v5"].update(
            {"named_fixed_atom_sigma": {"numerator": 1, "denominator": 5}}
        ),
    )
    reject(
        "reject_go_without_literal_gate",
        lambda obj: obj.update({"current_verdict": "GO"}),
    )
    reject(
        "reject_one_over_400_without_complete_ledger",
        lambda obj: obj["endpoint_ledger_v5"].update(
            {"one_over_400_paid": True}
        ),
    )
    reject(
        "reject_program_positive_L2_progress",
        lambda obj: obj["progress_classification"].update(
            {"new_program_positive_L2": True}
        ),
    )
    reject(
        "reject_named_atom_theorem_progress",
        lambda obj: obj["progress_classification"].update(
            {"new_named_fixed_atom_theorem": True}
        ),
    )
    reject(
        "reject_fixed_h0_fact_as_decay",
        lambda obj: obj["claim_boundary"].update(
            {"fixed_h0_data_fact_is_decay": True}
        ),
    )
    reject(
        "reject_vacuity_as_active_support",
        lambda obj: obj["claim_boundary"].update(
            {"vacuity_closes_active_support": True}
        ),
    )
    reject(
        "reject_scoped_stop_kills_pointwise_routes",
        lambda obj: obj["claim_boundary"].update(
            {"scoped_method_stop_kills_pointwise_routes": True}
        ),
    )
    reject(
        "reject_program_positive_L2_boundary",
        lambda obj: obj["claim_boundary"].update(
            {"program_positive_L2": True}
        ),
    )
    reject(
        "reject_empty_source_locks",
        lambda obj: obj.update({"source_locks": []}),
    )
    reject(
        "reject_source_hash_drift",
        lambda obj: obj["source_locks"][0].update(
            {"canonical_utf8_lf_sha256": "0" * 64}
        ),
    )
    reject(
        "reject_source_hash_as_theorem",
        lambda obj: obj["source_locks"][0].update(
            {"hash_semantics": "THEOREM_EVIDENCE"}
        ),
    )
    reject(
        "reject_occurrence_architecture_stop",
        lambda obj: obj["route_cells"]["architecture"][
            "occurrence_augmented_map"
        ].update({"stopped": True}),
    )
    reject_upstream(
        "reject_upstream_tpc176_unmatched_cut_drift",
        2,
        lambda obj: obj["coverage_ledger"].update({"unmatched_cut_count": 0}),
    )
    reject_upstream(
        "reject_upstream_tpc176_totality_promotion",
        2,
        lambda obj: obj["coverage_ledger"].update(
            {"production_totality_proved": True}
        ),
    )
    reject_upstream(
        "reject_upstream_tpc179_architecture_infeasible",
        5,
        lambda obj: obj["claim_boundary"].update(
            {"architecture_infeasible": True}
        ),
    )
    reject_upstream(
        "reject_upstream_tpc180_global_nonexistence",
        6,
        lambda obj: obj["claim_boundary"].update(
            {"scoped_census_is_global_nonexistence": True}
        ),
    )
    reject_upstream(
        "reject_upstream_tpc180_unsourced_phase_locator",
        6,
        lambda obj: obj["candidate_registry"].update(
            {"phase_value_source_locator": "UNSOURCED"}
        ),
    )
    reject_upstream(
        "reject_upstream_tpc180_generic_scan_promotion",
        6,
        lambda obj: obj["source_census"].update(
            {"future_new_fields_automatically_scanned": True}
        ),
    )
    reject_upstream(
        "reject_upstream_tpc180_phase_registry_decay",
        6,
        lambda obj: obj["registry_contract"].update(
            {"decay_axis": "FIXED_X_POWER_FIXED_ATOM"}
        ),
    )
    reject_upstream(
        "reject_upstream_tpc181_architecture_stopped",
        7,
        lambda obj: obj["claim_boundary"].update(
            {"architecture_stopped": True}
        ),
    )
    reject_upstream(
        "reject_upstream_tpc181_architecture_reroute",
        7,
        lambda obj: obj["route_decision"].update(
            {"architecture_reroute": True}
        ),
    )
    reject_upstream(
        "reject_upstream_tpc181_pointwise_stop",
        7,
        lambda obj: obj["pointwise_routes"][0].update(
            {"stopped_by_metric_nonimplication": True}
        ),
    )

    audit = {
        "schema": AUDIT_SCHEMA_ID,
        "status": "PASS" if all(mutations.values()) else "FAIL",
        "snapshot_sha256": hashlib.sha256(
            canonical_json(snapshot).encode("utf-8")
        ).hexdigest(),
        "current_verdict": snapshot["current_verdict"],
        "first_missing": snapshot["first_missing"],
        "checks": {
            "all_source_locks_recomputed": True,
            "tpc175_scoped_empty_family_preserved": True,
            "tpc176_zero_coverage_not_totality": True,
            "tpc177_vacuity_firewall_preserved": True,
            "tpc178_archive_address_not_canonicality": True,
            "tpc179_three_roots_preserved": True,
            "tpc180_registry_decay_axis_none": True,
            "tpc181_uncontrolled_selector_stop_scoped": True,
            "two_pointwise_routes_open_parent_ready": True,
            "six_axis_quantifiers_complete": True,
            "strict_one_over_400_unpaid": True,
        },
        "mutation_regressions": mutations,
        "claim_boundary": copy.deepcopy(snapshot["claim_boundary"]),
    }
    validate_audit(audit, snapshot)
    validate_schema_file(SNAPSHOT_SCHEMA, snapshot)
    validate_schema_file(AUDIT_SCHEMA, audit)
    return snapshot, audit


def validate_snapshot(value: dict[str, Any]) -> None:
    required = {
        "schema",
        "snapshot",
        "source_locks",
        "current_verdict",
        "first_missing",
        "structural_result",
        "phase_result",
        "typed_frontiers",
        "route_cells",
        "endpoint_ledger_v5",
        "quantifier_projection",
        "progress_classification",
        "next_forced_objects",
        "claim_boundary",
    }
    if set(value) != required or value["schema"] != SCHEMA_ID:
        raise ValueError("snapshot contract drift")
    if value["current_verdict"] != "NOT_TESTABLE":
        raise ValueError("MVP8 verdict promotion")
    if value["first_missing"] != STRUCTURAL_ROOTS[0]:
        raise ValueError("first-missing drift")
    if value["snapshot"] != {
        "date": "2026-07-28",
        "hash_mode": HASH_MODE,
        "hash_semantics": "INTEGRITY_ONLY",
        "classifier_evidence_mode": "SOURCE_LOCKED",
    }:
        raise ValueError("snapshot identity or hash semantics drift")
    expected_locks = [
        source_lock(source_id, path) for source_id, path in UPSTREAM_SOURCES
    ]
    if value["source_locks"] != expected_locks:
        raise ValueError("source lock registry/hash drift")
    structural = value["structural_result"]
    if (
        set(structural)
        != {
            "declared_corpus_scope",
            "qualifying_local_edge_count",
            "scoped_extraction_cell",
            "global_architecture_status",
            "covered_cut_count",
            "production_cut_count",
            "unmatched_cut_count",
            "actual_active_support",
            "canonical_minimal_representation",
            "minimal_root_antichain",
        }
        or structural["declared_corpus_scope"]
        != "FROZEN_CONTIGUOUS_OCCURRENCE_SOURCE_CORRIDOR_TPC133_172"
        or structural["qualifying_local_edge_count"] != 0
        or structural["scoped_extraction_cell"] != "STOP_SCOPED"
        or structural["global_architecture_status"] != "OPEN_NOT_TESTABLE"
        or structural["covered_cut_count"] != 0
        or structural["production_cut_count"] != 2988
        or structural["unmatched_cut_count"] != 2988
        or structural["actual_active_support"] != "NOT_TESTABLE"
        or structural["canonical_minimal_representation"] != "NOT_TESTABLE"
        or structural["minimal_root_antichain"] != STRUCTURAL_ROOTS
    ):
        raise ValueError("structural result drift")
    phase = value["phase_result"]
    if (
        set(phase)
        != {
            "fixed_h0",
            "fixed_h0_semantics",
            "production_phase_registry",
            "named_physical_atom",
            "production_packet_coordinate_rows",
            "proved_phase_quantifier",
            "required_phase_quantifier",
            "metric_source_backed_bridge",
            "metric_uncontrolled_atomic",
            "pointwise_routes",
        }
        or phase["fixed_h0"] != 2
        or phase["fixed_h0_semantics"] != "SOURCE_BACKED_DATA_FACT_ONLY"
        or phase["production_phase_registry"] != "NOT_TESTABLE"
        or phase["named_physical_atom"] is not False
        or phase["production_packet_coordinate_rows"] != 0
        or phase["proved_phase_quantifier"] != "LEBESGUE_AE_FIXED_PHASE"
        or phase["required_phase_quantifier"] != "NAMED_FIXED_ATOM"
        or phase["metric_source_backed_bridge"] != "NOT_TESTABLE"
        or phase["metric_uncontrolled_atomic"] != "STOP_SCOPED"
        or phase["pointwise_routes"] != POINTWISE_ROUTES
    ):
        raise ValueError("phase result drift")
    blocker_ids = [
        row["node_id"]
        for row in value["typed_frontiers"]["minimal_not_testable_antichain"]
    ]
    blockers = value["typed_frontiers"]["minimal_not_testable_antichain"]
    if (
        blocker_ids != STRUCTURAL_ROOTS + H9_ROOTS
        or any(row.get("status") != "NOT_TESTABLE" for row in blockers)
    ):
        raise ValueError("seven-root antichain drift")
    frontier = value["typed_frontiers"]["parent_ready_open_frontier"]
    if (
        [row["node_id"] for row in frontier] != POINTWISE_ROUTES
        or any(
            row["state"] != "OPEN_PARENT_READY"
            or row.get("role") != "ARITHMETIC_TARGET"
            or row.get("stopped_by_metric_nonimplication") is not False
            or row.get("quantifier_signature") != REQUIRED_QUANTIFIERS
            for row in frontier
        )
        or value["typed_frontiers"]["frontiers_are_type_disjoint"] is not True
    ):
        raise ValueError("pointwise frontier drift")
    occurrence_map = value["route_cells"]["architecture"][
        "occurrence_augmented_map"
    ]
    if (
        occurrence_map.get("route_kind") != "ARCHITECTURE_ROUTE"
        or occurrence_map.get("state") != "OPEN_NOT_TESTABLE"
        or occurrence_map.get("stopped") is not False
    ):
        raise ValueError("occurrence architecture drift")
    extraction = value["route_cells"]["architecture"][
        "current_declared_corpus_edge_extraction"
    ]
    if (
        extraction.get("route_kind") != "ARCHITECTURE_SOURCE_CELL"
        or extraction.get("scope_id")
        != "FROZEN_CONTIGUOUS_OCCURRENCE_SOURCE_CORRIDOR_TPC133_172"
        or extraction["state"] != "STOP_SCOPED"
        or extraction.get("stopped") is not True
        or extraction["architecture_stopped"] is not False
        or extraction.get("fresh_source_or_new_theorem_can_reopen") is not True
    ):
        raise ValueError("scoped structural stop promoted")
    arithmetic = value["route_cells"]["arithmetic_subroutes"]
    if (
        set(arithmetic)
        != {
            "phase_metric_uncontrolled_atomic",
            "phase_metric_source_backed",
            "bad_endpoint_pointwise_fixed_atom",
            "direct_additive_twist_fixed_atom",
        }
        or any(
            cell.get("route_kind") != "ARITHMETIC_SUBROUTE"
            for cell in arithmetic.values()
        )
        or arithmetic["phase_metric_uncontrolled_atomic"].get("scope_id")
        != "UNCONTROLLED_ATOMIC_PROMOTION_ONLY"
        or arithmetic["phase_metric_uncontrolled_atomic"]["state"]
        != "STOP_SCOPED"
        or arithmetic["phase_metric_source_backed"].get("scope_id")
        != "SOURCE_BACKED_METRIC_TO_FIXED_ATOM"
        or arithmetic["phase_metric_source_backed"]["state"]
        != "OPEN_NOT_TESTABLE"
        or arithmetic["bad_endpoint_pointwise_fixed_atom"]["state"]
        != "OPEN_PARENT_READY"
        or arithmetic["direct_additive_twist_fixed_atom"]["state"]
        != "OPEN_PARENT_READY"
    ):
        raise ValueError("arithmetic route-cell drift")
    ledger = value["endpoint_ledger_v5"]
    expected_literal_gate = {
        "literal_physical_coefficients": "NOT_TESTABLE",
        "fixed_physical_h0": "PROVED_DATA_FACT_ONLY",
        "physical_atomic_normalization": "NOT_TESTABLE",
        "canonical_or_minimal_representation": "NOT_TESTABLE",
        "actual_active_support": "NOT_TESTABLE",
        "strict_one_over_400_budget": "NOT_TESTABLE",
    }
    expected_registry_gate = {
        "source_backed_local_occurrence_edge_family": "NOT_TESTABLE",
        "actual_active_support_certificate": "NOT_TESTABLE",
        "canonical_minimal_representation_certificate": "NOT_TESTABLE",
        "literal_weight_registry": "NOT_TESTABLE",
        "phase_cell_registry": "NOT_TESTABLE",
        "endpoint_registry": "NOT_TESTABLE",
        "normalization_registry": "NOT_TESTABLE",
    }
    if (
        set(ledger)
        != {
            "contract",
            "sigma_required",
            "named_fixed_atom_sigma",
            "phase_metric_sigma",
            "phase_metric_sigma_scope",
            "phase_metric_eligible_for_named_atom_charge",
            "literal_gate",
            "registry_gate",
            "strict_net_slack",
            "one_over_400_paid",
            "state",
        }
        or ledger["contract"] != "MVP8_FIXED_H0_NON_DUPLICATING_ENDPOINT_V5"
        or ledger["sigma_required"] != {"numerator": 1, "denominator": 400}
        or ledger["named_fixed_atom_sigma"] != {"numerator": 0, "denominator": 1}
        or ledger["phase_metric_sigma"] != "every delta<1/4"
        or ledger["phase_metric_sigma_scope"]
        != "LEBESGUE_AE_EVENTUALLY_PRESCRIBED_PACKET_SCHEDULE"
        or ledger["phase_metric_eligible_for_named_atom_charge"] is not False
        or ledger["literal_gate"] != expected_literal_gate
        or ledger["registry_gate"] != expected_registry_gate
        or ledger["one_over_400_paid"] is not False
        or ledger["strict_net_slack"] is not None
        or ledger["state"] != "INCOMPLETE"
    ):
        raise ValueError("endpoint ledger promotion")
    projection = value["quantifier_projection"]
    if (
        projection["proved"] != PROVED_QUANTIFIERS
        or projection["required"] != REQUIRED_QUANTIFIERS
        or projection["failed_axes"] != list(PROVED_QUANTIFIERS)
        or projection["promotion_complete"] is not False
    ):
        raise ValueError("quantifier projection drift")
    if value["progress_classification"] != PROGRESS_CLASSIFICATION:
        raise ValueError("progress classification drift")
    if value["next_forced_objects"] != {
        "structural": (
            "NEW_EXPLICIT_SOURCE_CORPUS_OR_NEW_THEOREM_BACKED_LOCAL_EDGE"
        ),
        "phase_bridge": (
            "SOURCE_LOCKED_NAMED_ATOM_PLUS_SCHEDULE_SPECIFIC_AVOIDANCE"
        ),
        "pointwise_arithmetic": POINTWISE_ROUTES,
    }:
        raise ValueError("next forced object drift")
    if value["claim_boundary"] != CLAIM_BOUNDARY:
        raise ValueError("claim boundary was promoted or changed")


def validate_audit(audit: dict[str, Any], snapshot: dict[str, Any]) -> None:
    required = {
        "schema",
        "status",
        "snapshot_sha256",
        "current_verdict",
        "first_missing",
        "checks",
        "mutation_regressions",
        "claim_boundary",
    }
    if set(audit) != required or audit["schema"] != AUDIT_SCHEMA_ID:
        raise ValueError("audit contract drift")
    if (
        audit["status"] != "PASS"
        or audit["current_verdict"] != "NOT_TESTABLE"
        or audit["first_missing"] != STRUCTURAL_ROOTS[0]
    ):
        raise ValueError("audit route state drift")
    expected_sha = hashlib.sha256(
        canonical_json(snapshot).encode("utf-8")
    ).hexdigest()
    if audit["snapshot_sha256"] != expected_sha:
        raise ValueError("audit snapshot hash drift")
    expected_checks = {
        "all_source_locks_recomputed": True,
        "tpc175_scoped_empty_family_preserved": True,
        "tpc176_zero_coverage_not_totality": True,
        "tpc177_vacuity_firewall_preserved": True,
        "tpc178_archive_address_not_canonicality": True,
        "tpc179_three_roots_preserved": True,
        "tpc180_registry_decay_axis_none": True,
        "tpc181_uncontrolled_selector_stop_scoped": True,
        "two_pointwise_routes_open_parent_ready": True,
        "six_axis_quantifiers_complete": True,
        "strict_one_over_400_unpaid": True,
    }
    if audit["checks"] != expected_checks:
        raise ValueError("audit checks drift")
    if (
        set(audit["mutation_regressions"]) != EXPECTED_MUTATION_NAMES
        or set(audit["mutation_regressions"].values()) != {True}
    ):
        raise ValueError("audit mutation contract drift")
    if audit["claim_boundary"] != CLAIM_BOUNDARY:
        raise ValueError("audit claim boundary drift")


def write_or_check(path: Path, value: dict[str, Any], check: bool) -> None:
    expected = canonical_json(value)
    if check:
        if not path.is_file() or normalize(
            path.read_text(encoding="utf-8")
        ) != expected:
            raise SystemExit(f"TPC-182 CHECK FAIL: {path.name}")
    else:
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(expected, encoding="utf-8", newline="\n")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()
    snapshot, audit = build_snapshot()
    if args.check:
        actual_snapshot = load(SNAPSHOT)
        actual_audit = load(AUDIT)
        validate_snapshot(actual_snapshot)
        validate_audit(actual_audit, actual_snapshot)
        validate_schema_file(SNAPSHOT_SCHEMA, actual_snapshot)
        validate_schema_file(AUDIT_SCHEMA, actual_audit)
    write_or_check(SNAPSHOT, snapshot, args.check)
    write_or_check(AUDIT, audit, args.check)
    print(
        "TPC-182 "
        + ("CHECK" if args.check else "GENERATE")
        + " PASS "
        + json.dumps(
            {
                "verdict": snapshot["current_verdict"],
                "first_missing": snapshot["first_missing"],
                "local_edges": snapshot["structural_result"][
                    "qualifying_local_edge_count"
                ],
                "phase_registry": snapshot["phase_result"][
                    "production_phase_registry"
                ],
                "uncontrolled_selector": snapshot["phase_result"][
                    "metric_uncontrolled_atomic"
                ],
                "program_positive_L2": snapshot["progress_classification"][
                    "new_program_positive_L2"
                ],
            },
            sort_keys=True,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
