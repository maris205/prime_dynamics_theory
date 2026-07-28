#!/usr/bin/env python3
"""Build and audit the TPC-171 source-locked integration manifest.

The script imports the frozen TPC-163--170 machine-readable exports, records
their exact quantifiers, constructs a typed proof DAG, and enforces the
separation between architecture routes, arithmetic method subroutes, physical
registries, and program-positive L2 targets.  Hashes are integrity locks only.
"""

from __future__ import annotations

import argparse
import copy
import hashlib
import json
from pathlib import Path
from typing import Any, Iterable


HERE = Path(__file__).resolve().parent
PAPER = HERE.parent
PAPERS = PAPER.parent
REPO = PAPERS.parent
MANIFEST = HERE / "tpc171_integration_manifest.json"
AUDIT = HERE / "tpc171_integration_audit.json"
MANIFEST_SCHEMA = PAPER / "schemas" / "tpc171-integration-manifest-v1.schema.json"
AUDIT_SCHEMA = PAPER / "schemas" / "tpc171-integration-audit-v1.schema.json"
HASH_MODE = "CANONICAL_UTF8_LF_V2"

Q_AXES = (
    "carrier_axis",
    "phase_axis",
    "endpoint_axis",
    "scale_axis",
    "decay_axis",
    "support_axis",
)

Q_ALLOWED = {
    "carrier_axis": {
        "FROZEN_ARCHIVE",
        "FORMAL_LOCAL_FAMILIES",
        "ACTUAL_CORE_SINGLE_CELL",
        "SEPARATED_PHASE_REGISTRY",
        "EXPLICIT_PACKET_CORRIDOR",
        "ALL_NONSOFT_CUT_PATHS",
        "ACTUAL_OCCURRENCE_CARRIER",
        "ACTUAL_FIXED_H0_PACKET",
        "LITERAL_WEIGHT_REGISTRY",
        "PHYSICAL_PHASE_REGISTRY",
        "PHYSICAL_ENDPOINT_REGISTRY",
        "PHYSICAL_NORMALIZATION_REGISTRY",
    },
    "phase_axis": {
        "NOT_APPLICABLE",
        "LEBESGUE_L2",
        "FINITE_REGISTRY_DENSITY",
        "LEBESGUE_AE_FIXED_PHASE",
        "NAMED_FIXED_ATOM",
        "UNIFORM_ALL_PHASE",
    },
    "endpoint_axis": {
        "NOT_APPLICABLE",
        "TERMINAL_INTERVAL",
        "ALL_PREFIX_THETA_SHELL",
        "DETERMINISTIC_ALL_PREFIX",
    },
    "scale_axis": {
        "FROZEN_FINITE_PACKET",
        "EVERY_DECLARED_SCALE",
        "EVENTUALLY_PRESCRIBED_SCHEDULE",
        "DETERMINISTIC_ALL_SCALE",
    },
    "decay_axis": {
        "NONE",
        "SCHEMA_ONLY",
        "FIXED_X_POWER_PHASE_AVERAGED",
        "FIXED_X_POWER_PHASE_METRIC",
        "FIXED_X_POWER_FIXED_ATOM",
        "LOG_SAVING",
    },
    "support_axis": {
        "FORMAL_ARCHIVE",
        "FORMAL_LOCAL_FAMILY",
        "SOURCE_BACKED_LOCAL_SUPPORT",
        "FORMAL_OCCURRENCE",
        "ACTUAL_CORE",
        "ACTUAL_ACTIVE_SUPPORT",
    },
}

STATUSES = {"PROVED", "NOT_TESTABLE", "OPEN", "STOPPED"}
ROLES = {
    "STRUCTURAL",
    "STRUCTURAL_NEGATIVE",
    "PHYSICAL_REGISTRY",
    "ARITHMETIC_CORE",
    "ARITHMETIC_TARGET",
    "ARITHMETIC_NEGATIVE",
    "ROOT",
}
ARITHMETIC_ROLES = {
    "ARITHMETIC_CORE",
    "ARITHMETIC_TARGET",
    "ARITHMETIC_NEGATIVE",
}

NINE_DEFECTS = (
    "D_L",
    "D_QD",
    "D_QZ",
    "D_G",
    "D_P",
    "D_DZ",
    "D_GP",
    "D_cover",
    "D_rec",
)


def canonical_json(value: Any) -> str:
    return json.dumps(value, ensure_ascii=False, indent=2, sort_keys=True) + "\n"


def normalize_lf(text: str) -> str:
    return text.replace("\r\n", "\n").replace("\r", "\n")


def canonical_bytes(path: Path) -> bytes:
    text = normalize_lf(path.read_text(encoding="utf-8"))
    if path.suffix == ".json":
        text = canonical_json(json.loads(text))
    elif not text.endswith("\n"):
        text += "\n"
    return text.encode("utf-8")


def sha256(path: Path) -> str:
    return hashlib.sha256(canonical_bytes(path)).hexdigest()


def payload_sha256(value: Any) -> str:
    return hashlib.sha256(canonical_json(value).encode("utf-8")).hexdigest()


def paper_dir(number: int) -> Path:
    matches = sorted(path for path in PAPERS.glob(f"tpc-{number}-*") if path.is_dir())
    if len(matches) != 1:
        raise FileNotFoundError(
            f"expected exactly one TPC-{number} directory, found {len(matches)}"
        )
    return matches[0]


def repo_relative(path: Path) -> str:
    return path.resolve().relative_to(REPO.resolve()).as_posix()


def load_json(path: Path) -> dict[str, Any]:
    value = json.loads(normalize_lf(path.read_text(encoding="utf-8")))
    if not isinstance(value, dict):
        raise ValueError(f"expected JSON object: {path}")
    return value


def find_json(number: int, schema_id: str) -> tuple[Path, dict[str, Any]]:
    matches: list[tuple[Path, dict[str, Any]]] = []
    for path in sorted(paper_dir(number).rglob("*.json")):
        value = load_json(path)
        if value.get("schema") == schema_id:
            matches.append((path, value))
    if len(matches) != 1:
        raise ValueError(
            f"TPC-{number}: expected one {schema_id} object, found {len(matches)}"
        )
    return matches[0]


def source_locks() -> list[dict[str, Any]]:
    locks: list[dict[str, Any]] = []
    for number in range(163, 171):
        directory = paper_dir(number)
        candidates = [directory / "main.tex"]
        candidates.extend(sorted((directory / "schemas").glob("*.json")))
        candidates.extend(sorted((directory / "experiments").glob("*.py")))
        candidates.extend(sorted((directory / "experiments").glob("*.json")))
        if any(not path.is_file() for path in candidates):
            raise FileNotFoundError(f"TPC-{number} has an incomplete source bundle")
        for path in candidates:
            locks.append(
                {
                    "source_id": f"TPC{number}.{path.relative_to(directory).as_posix()}",
                    "paper": f"TPC-{number}",
                    "path": repo_relative(path),
                    "kind": (
                        "LATEX"
                        if path.suffix == ".tex"
                        else "SCRIPT"
                        if path.suffix == ".py"
                        else "SCHEMA"
                        if path.parent.name == "schemas"
                        else "OUTPUT"
                    ),
                    "canonical_utf8_lf_sha256": sha256(path),
                    "hash_semantics": "INTEGRITY_ONLY",
                }
            )
    return locks


def q(
    carrier: str,
    phase: str,
    endpoint: str,
    scale: str,
    decay: str,
    support: str,
) -> dict[str, str]:
    value = dict(
        zip(Q_AXES, (carrier, phase, endpoint, scale, decay, support), strict=True)
    )
    validate_q(value)
    return value


def validate_q(value: dict[str, Any]) -> None:
    if set(value) != set(Q_AXES):
        raise ValueError("quantifier signature does not have exactly six axes")
    for axis in Q_AXES:
        if value[axis] not in Q_ALLOWED[axis]:
            raise ValueError(f"invalid {axis}: {value[axis]}")


def import_record(
    paper: str,
    export_id: str,
    status: str,
    evidence_level: str,
    artifact_id: str,
    carrier_id: str,
    scope_id: str,
    normalization_id: str,
    signature: dict[str, str],
    *,
    promotion_eligible: bool = False,
) -> dict[str, Any]:
    return {
        "paper": paper,
        "export_id": export_id,
        "status": status,
        "evidence_level": evidence_level,
        "artifact_id": artifact_id,
        "artifact_readiness": "READY",
        "carrier_id": carrier_id,
        "scope_id": scope_id,
        "normalization_id": normalization_id,
        "quantifier_signature": signature,
        "promotion_eligible": promotion_eligible,
    }


def node(
    node_id: str,
    node_type: str,
    role: str,
    status: str,
    parents: Iterable[str],
    signature: dict[str, str],
    *,
    evidence_id: str | None = None,
    scope_id: str,
    carrier_id: str,
    normalization_id: str,
    route_kind: str | None = None,
) -> dict[str, Any]:
    return {
        "node_id": node_id,
        "node_type": node_type,
        "role": role,
        "status": status,
        "parents": list(parents),
        "evidence_id": evidence_id,
        "scope_id": scope_id,
        "carrier_id": carrier_id,
        "normalization_id": normalization_id,
        "route_kind": route_kind,
        "quantifier_signature": signature,
    }


def ancestors(nodes_by_id: dict[str, dict[str, Any]], start: str) -> set[str]:
    seen: set[str] = set()
    stack = list(nodes_by_id[start]["parents"])
    while stack:
        current = stack.pop()
        if current in seen:
            continue
        if current not in nodes_by_id:
            raise ValueError(f"unknown parent {current}")
        seen.add(current)
        stack.extend(nodes_by_id[current]["parents"])
    return seen


def minimal_blockers(
    nodes_by_id: dict[str, dict[str, Any]], root: str
) -> list[str]:
    active = ancestors(nodes_by_id, root) | {root}
    raw = {
        node_id
        for node_id in active
        if nodes_by_id[node_id]["status"] == "NOT_TESTABLE"
        and nodes_by_id[node_id]["node_type"] == "TARGET"
    }
    minimal = []
    for candidate in raw:
        candidate_ancestors = ancestors(nodes_by_id, candidate)
        if not (candidate_ancestors & raw):
            minimal.append(candidate)
    order = {
        "H1.source_backed_local_occurrence_edge_family": 0,
        "H1.actual_active_support_certificate": 1,
        "H1.canonical_minimal_representation_certificate": 2,
        "H9.literal_weight_registry": 3,
        "H9.phase_cell_registry": 4,
        "H9.endpoint_registry": 5,
        "H9.normalization_registry": 6,
    }
    return sorted(minimal, key=lambda item: (order.get(item, 100), item))


def parent_ready_open(
    nodes_by_id: dict[str, dict[str, Any]], root: str
) -> list[str]:
    active = ancestors(nodes_by_id, root) | {root}
    result = []
    for node_id in active:
        record = nodes_by_id[node_id]
        if record["status"] != "OPEN":
            continue
        if all(nodes_by_id[parent]["status"] == "PROVED" for parent in record["parents"]):
            result.append(node_id)
    return sorted(result)


def build() -> dict[str, Any]:
    _, census163 = find_json(163, "tpc-163-source-locator-census-v1")
    _, key164 = find_json(164, "tpc-164-minimal-archived-separation-key-v1")
    # TPC-165 and TPC-166 publish one primary decision object each.  Their
    # schema identifiers are intentionally resolved exactly after the files
    # freeze; accepting a filename or an arbitrary theorem label is forbidden.
    _, gluing165 = find_json(165, "tpc-165-local-global-crosswalk-gluing-v1")
    _, decision166 = find_json(166, "tpc-166-refined-h1-crosswalk-frontier-v1")
    _, parseval167 = find_json(167, "tpc-167-parseval-audit-v1")
    _, sieve168 = find_json(168, "tpc-168-registry-sieve-audit-v1")
    _, maximal169 = find_json(169, "tpc-169-maximal-prefix-audit-v1")
    _, corridor170 = find_json(170, "tpc-170-metric-corridor-audit-v1")

    if census163["production_crosswalk_edge_census"]["theorem_backed_edge_count"] != 0:
        raise ValueError("TPC-163 production edge census drift")
    collision = census163["native_key_collision"]
    if (
        census163["production_archive"]["row_count"],
        collision["native_tuple_count"],
        collision["rows_in_collision_classes"],
        collision["excess_rows_over_native_keys"],
    ) != (2988, 866, 2976, 2122):
        raise ValueError("TPC-163 census constants drift")
    if key164["minimal_separating_keys"] != [
        ["ell", "k", "native_d", "jL", "jK"]
    ]:
        raise ValueError("TPC-164 unique minimal key drift")
    if key164["claim_boundary"]["canonical_minimal_representation_proved"]:
        raise ValueError("archive addressing promoted to canonical representation")

    if gluing165["formal_gluing_theorem"]["theorem_level"] != "PROVED_L0_FORMAL":
        raise ValueError("TPC-165 formal theorem level drift")
    if gluing165["production_status"]["source_backed_local_edge_count"] != 0:
        raise ValueError("TPC-165 production edge census drift")
    if any(
        item["production_status"] != "NOT_TESTABLE"
        for item in gluing165["three_gate_separation"].values()
    ):
        raise ValueError("TPC-165 production gate was promoted")

    parallel = decision166["minimal_not_testable_root_antichain"]
    expected_roots = [
        "H1.source_backed_local_occurrence_edge_family",
        "H1.actual_active_support_certificate",
        "H1.canonical_minimal_representation_certificate",
    ]
    if parallel != expected_roots:
        raise ValueError("TPC-166 parallel-root order or identity drift")
    if (
        decision166["current_decision"]["verdict"] != "NOT_TESTABLE"
        or decision166["current_decision"]["selected_route_stopped"]
        or decision166["current_decision"]["actual_carrier_impossibility"]
    ):
        raise ValueError("TPC-166 H1 route status drift")

    arithmetic_sources = (parseval167, sieve168, maximal169, corridor170)
    for source in arithmetic_sources:
        if source["status"] != "PASS":
            raise ValueError("arithmetic source audit is not PASS")
        boundary = source["claim_boundary"]
        if boundary["program_positive_L2"] or boundary["fixed_atom"]:
            raise ValueError("phase-metric source promoted to program L2 or fixed atom")
    if corridor170["fixed_atom_stop"]["status"] != (
        "PROVED_SCOPED_METRIC_TO_ATOM_NONIMPLICATION"
    ):
        raise ValueError("TPC-170 scoped stop drift")

    q_archive = q(
        "FROZEN_ARCHIVE",
        "NOT_APPLICABLE",
        "NOT_APPLICABLE",
        "FROZEN_FINITE_PACKET",
        "SCHEMA_ONLY",
        "FORMAL_ARCHIVE",
    )
    q_formal = q(
        "FORMAL_LOCAL_FAMILIES",
        "NOT_APPLICABLE",
        "NOT_APPLICABLE",
        "FROZEN_FINITE_PACKET",
        "SCHEMA_ONLY",
        "FORMAL_LOCAL_FAMILY",
    )
    q_occurrence = q(
        "ACTUAL_OCCURRENCE_CARRIER",
        "NOT_APPLICABLE",
        "NOT_APPLICABLE",
        "DETERMINISTIC_ALL_SCALE",
        "NONE",
        "ACTUAL_ACTIVE_SUPPORT",
    )
    q_local_edge = q(
        "ACTUAL_OCCURRENCE_CARRIER",
        "NOT_APPLICABLE",
        "NOT_APPLICABLE",
        "DETERMINISTIC_ALL_SCALE",
        "NONE",
        "SOURCE_BACKED_LOCAL_SUPPORT",
    )
    q_canonical = q(
        "ACTUAL_OCCURRENCE_CARRIER",
        "NOT_APPLICABLE",
        "NOT_APPLICABLE",
        "DETERMINISTIC_ALL_SCALE",
        "NONE",
        "FORMAL_OCCURRENCE",
    )
    q_cell = q(
        "ACTUAL_CORE_SINGLE_CELL",
        "LEBESGUE_L2",
        "TERMINAL_INTERVAL",
        "EVERY_DECLARED_SCALE",
        "FIXED_X_POWER_PHASE_AVERAGED",
        "ACTUAL_CORE",
    )
    q_registry = q(
        "SEPARATED_PHASE_REGISTRY",
        "FINITE_REGISTRY_DENSITY",
        "TERMINAL_INTERVAL",
        "EVERY_DECLARED_SCALE",
        "FIXED_X_POWER_PHASE_AVERAGED",
        "ACTUAL_CORE",
    )
    q_maximal = q(
        "ACTUAL_CORE_SINGLE_CELL",
        "LEBESGUE_L2",
        "ALL_PREFIX_THETA_SHELL",
        "EVERY_DECLARED_SCALE",
        "FIXED_X_POWER_PHASE_AVERAGED",
        "ACTUAL_CORE",
    )
    q_corridor = q(
        "EXPLICIT_PACKET_CORRIDOR",
        "LEBESGUE_AE_FIXED_PHASE",
        "ALL_PREFIX_THETA_SHELL",
        "EVENTUALLY_PRESCRIBED_SCHEDULE",
        "FIXED_X_POWER_PHASE_METRIC",
        "ACTUAL_CORE",
    )
    q_fixed_estimate = q(
        "ACTUAL_FIXED_H0_PACKET",
        "NAMED_FIXED_ATOM",
        "DETERMINISTIC_ALL_PREFIX",
        "DETERMINISTIC_ALL_SCALE",
        "FIXED_X_POWER_FIXED_ATOM",
        "ACTUAL_ACTIVE_SUPPORT",
    )
    q_packet_data = q(
        "ACTUAL_FIXED_H0_PACKET",
        "NAMED_FIXED_ATOM",
        "DETERMINISTIC_ALL_PREFIX",
        "DETERMINISTIC_ALL_SCALE",
        "NONE",
        "ACTUAL_ACTIVE_SUPPORT",
    )
    q_weight_registry = q(
        "LITERAL_WEIGHT_REGISTRY",
        "NOT_APPLICABLE",
        "NOT_APPLICABLE",
        "DETERMINISTIC_ALL_SCALE",
        "NONE",
        "ACTUAL_ACTIVE_SUPPORT",
    )
    q_phase_registry = q(
        "PHYSICAL_PHASE_REGISTRY",
        "NAMED_FIXED_ATOM",
        "NOT_APPLICABLE",
        "DETERMINISTIC_ALL_SCALE",
        "NONE",
        "ACTUAL_ACTIVE_SUPPORT",
    )
    q_endpoint_registry = q(
        "PHYSICAL_ENDPOINT_REGISTRY",
        "NOT_APPLICABLE",
        "DETERMINISTIC_ALL_PREFIX",
        "DETERMINISTIC_ALL_SCALE",
        "NONE",
        "ACTUAL_ACTIVE_SUPPORT",
    )
    q_normalization_registry = q(
        "PHYSICAL_NORMALIZATION_REGISTRY",
        "NOT_APPLICABLE",
        "NOT_APPLICABLE",
        "DETERMINISTIC_ALL_SCALE",
        "NONE",
        "ACTUAL_ACTIVE_SUPPORT",
    )

    imports = [
        import_record(
            "TPC-163",
            "S163.frozen_source_edge_census",
            "PROVED",
            "L0_SOURCE_CENSUS_SCOPED",
            "artifact.frozen_source_census",
            "carrier.frozen_cut_archive",
            "scope.frozen_declared_corpus",
            "norm.physical_atomic",
            q_archive,
        ),
        import_record(
            "TPC-164",
            "S164.unique_minimal_archive_address",
            "PROVED",
            "L0_ARCHIVE_ADDRESSING",
            "artifact.minimal_archive_key",
            "carrier.frozen_cut_archive",
            "scope.frozen_archive_addressing",
            "norm.physical_atomic",
            q_archive,
        ),
        import_record(
            "TPC-165",
            "S165.compatible_local_family_gluing",
            "PROVED",
            "L0_FORMAL_LOCAL_GLUING",
            "artifact.formal_local_gluing",
            "carrier.formal_local_families",
            "scope.formal_compatible_local_families",
            "norm.physical_atomic",
            q_formal,
        ),
        import_record(
            "TPC-166",
            "D166.three_factor_crosswalk_contract",
            "PROVED",
            "L1_STRUCTURAL_DECISION",
            "artifact.three_factor_crosswalk_contract",
            "carrier.all_nonsoft_cut_paths",
            "scope.actual_occurrence_augmented_route",
            "norm.physical_atomic",
            q_archive,
        ),
        import_record(
            "TPC-167",
            "A167.direct_additive_twist_phase_L2",
            "PROVED",
            "L1_ACTUAL_CORE_PHASE_METRIC_SINGLE_CELL",
            "artifact.phase_parseval",
            "carrier.determinant_two_actual_core",
            "scope.actual_core_single_cell_phase_metric",
            "norm.q_over_N",
            q_cell,
        ),
        import_record(
            "TPC-168",
            "A168.actual_core_registry_density",
            "PROVED",
            "L1_ACTUAL_CORE_PHASE_METRIC_FINITE_REGISTRY",
            "artifact.separated_phase_sieve",
            "carrier.determinant_two_actual_core",
            "scope.separated_finite_phase_registry",
            "norm.q_over_N",
            q_registry,
        ),
        import_record(
            "TPC-169",
            "A169.phase_maximal_all_prefix",
            "PROVED",
            "L1_ACTUAL_CORE_PHASE_METRIC_MAXIMAL_PREFIX",
            "artifact.phase_maximal_prefix",
            "carrier.determinant_two_actual_core",
            "scope.phase_metric_all_prefix",
            "norm.q_over_T",
            q_maximal,
        ),
        import_record(
            "TPC-170",
            "A170.metric_packet_corridor",
            "PROVED",
            "L1_ACTUAL_CORE_PHASE_METRIC_PACKET_CORRIDOR",
            "artifact.metric_packet_corridor",
            "carrier.explicit_prescribed_packet_corridor",
            "scope.phase_metric_packet_corridor",
            "norm.q_over_T",
            q_corridor,
        ),
    ]

    nodes: list[dict[str, Any]] = [
        node(
            "S163.source_edge_census",
            "EVIDENCE",
            "STRUCTURAL_NEGATIVE",
            "PROVED",
            [],
            q_archive,
            evidence_id="S163.frozen_source_edge_census",
            scope_id="scope.frozen_declared_corpus",
            carrier_id="carrier.frozen_cut_archive",
            normalization_id="norm.physical_atomic",
        ),
        node(
            "S164.minimal_archive_address",
            "EVIDENCE",
            "STRUCTURAL",
            "PROVED",
            [],
            q_archive,
            evidence_id="S164.unique_minimal_archive_address",
            scope_id="scope.frozen_archive_addressing",
            carrier_id="carrier.frozen_cut_archive",
            normalization_id="norm.physical_atomic",
        ),
        node(
            "S165.formal_local_gluing",
            "EVIDENCE",
            "STRUCTURAL",
            "PROVED",
            [],
            q_formal,
            evidence_id="S165.compatible_local_family_gluing",
            scope_id="scope.formal_compatible_local_families",
            carrier_id="carrier.formal_local_families",
            normalization_id="norm.physical_atomic",
        ),
        node(
            "D166.crosswalk_factor_contract",
            "EVIDENCE",
            "STRUCTURAL",
            "PROVED",
            [],
            q_archive,
            evidence_id="D166.three_factor_crosswalk_contract",
            scope_id="scope.actual_occurrence_augmented_route",
            carrier_id="carrier.all_nonsoft_cut_paths",
            normalization_id="norm.physical_atomic",
        ),
        node(
            "A167.phase_parseval",
            "EVIDENCE",
            "ARITHMETIC_CORE",
            "PROVED",
            [],
            q_cell,
            evidence_id="A167.direct_additive_twist_phase_L2",
            scope_id="scope.actual_core_single_cell_phase_metric",
            carrier_id="carrier.determinant_two_actual_core",
            normalization_id="norm.q_over_N",
        ),
        node(
            "A168.separated_registry_sieve",
            "EVIDENCE",
            "ARITHMETIC_CORE",
            "PROVED",
            ["A167.phase_parseval"],
            q_registry,
            evidence_id="A168.actual_core_registry_density",
            scope_id="scope.separated_finite_phase_registry",
            carrier_id="carrier.determinant_two_actual_core",
            normalization_id="norm.q_over_N",
        ),
        node(
            "A169.phase_maximal_prefix",
            "EVIDENCE",
            "ARITHMETIC_CORE",
            "PROVED",
            ["A167.phase_parseval"],
            q_maximal,
            evidence_id="A169.phase_maximal_all_prefix",
            scope_id="scope.phase_metric_all_prefix",
            carrier_id="carrier.determinant_two_actual_core",
            normalization_id="norm.q_over_T",
        ),
        node(
            "A170.metric_packet_corridor",
            "EVIDENCE",
            "ARITHMETIC_CORE",
            "PROVED",
            ["A168.separated_registry_sieve", "A169.phase_maximal_prefix"],
            q_corridor,
            evidence_id="A170.metric_packet_corridor",
            scope_id="scope.phase_metric_packet_corridor",
            carrier_id="carrier.explicit_prescribed_packet_corridor",
            normalization_id="norm.q_over_T",
        ),
        node(
            "N170.uncontrolled_atomic_promotion",
            "SCOPED_STOP",
            "ARITHMETIC_NEGATIVE",
            "STOPPED",
            ["A170.metric_packet_corridor"],
            q_corridor,
            evidence_id="N170.metric_to_atom_nonimplication",
            scope_id="scope.uncontrolled_atomic_promotion_only",
            carrier_id="carrier.arbitrary_atomic_phase_registry",
            normalization_id="norm.q_over_T",
            route_kind="ARITHMETIC_SUBROUTE",
        ),
        node(
            "H1.source_backed_local_occurrence_edge_family",
            "TARGET",
            "STRUCTURAL",
            "NOT_TESTABLE",
            ["S163.source_edge_census", "S165.formal_local_gluing", "D166.crosswalk_factor_contract"],
            q_local_edge,
            scope_id="scope.actual_occurrence_augmented_route",
            carrier_id="carrier.actual_occurrence_edges",
            normalization_id="norm.physical_atomic",
            route_kind="ARCHITECTURE_ROUTE",
        ),
        node(
            "H1.actual_active_support_certificate",
            "TARGET",
            "STRUCTURAL",
            "NOT_TESTABLE",
            ["S165.formal_local_gluing", "D166.crosswalk_factor_contract"],
            q_occurrence,
            scope_id="scope.actual_occurrence_augmented_route",
            carrier_id="carrier.actual_active_occurrences",
            normalization_id="norm.physical_atomic",
            route_kind="ARCHITECTURE_ROUTE",
        ),
        node(
            "H1.canonical_minimal_representation_certificate",
            "TARGET",
            "STRUCTURAL",
            "NOT_TESTABLE",
            ["S164.minimal_archive_address", "S165.formal_local_gluing", "D166.crosswalk_factor_contract"],
            q_canonical,
            scope_id="scope.actual_occurrence_augmented_route",
            carrier_id="carrier.actual_active_occurrences",
            normalization_id="norm.physical_atomic",
            route_kind="ARCHITECTURE_ROUTE",
        ),
        node(
            "H1.actual_occurrence_lift",
            "ALL",
            "STRUCTURAL",
            "NOT_TESTABLE",
            [
                "H1.source_backed_local_occurrence_edge_family",
                "H1.actual_active_support_certificate",
                "H1.canonical_minimal_representation_certificate",
            ],
            q_occurrence,
            scope_id="scope.actual_occurrence_augmented_route",
            carrier_id="carrier.actual_active_occurrences",
            normalization_id="norm.physical_atomic",
            route_kind="ARCHITECTURE_ROUTE",
        ),
    ]

    for defect in NINE_DEFECTS:
        nodes.append(
            node(
                f"H1.defect.{defect}",
                "TARGET",
                "STRUCTURAL",
                "NOT_TESTABLE",
                ["H1.actual_occurrence_lift"],
                q_occurrence,
                scope_id="scope.actual_occurrence_augmented_route",
                carrier_id="carrier.actual_active_occurrences",
                normalization_id="norm.physical_atomic",
                route_kind="ARCHITECTURE_ROUTE",
            )
        )

    nodes.extend(
        [
            node(
                "H1.occurrence_registry_totality",
                "TARGET",
                "PHYSICAL_REGISTRY",
                "NOT_TESTABLE",
                ["H1.actual_occurrence_lift"],
                q_occurrence,
                scope_id="scope.actual_occurrence_augmented_route",
                carrier_id="carrier.actual_active_occurrences",
                normalization_id="norm.physical_atomic",
                route_kind="ARCHITECTURE_ROUTE",
            ),
            node(
                "H1.map_clause",
                "ALL",
                "STRUCTURAL",
                "NOT_TESTABLE",
                [
                    "H1.actual_occurrence_lift",
                    *(f"H1.defect.{defect}" for defect in NINE_DEFECTS),
                    "H1.occurrence_registry_totality",
                ],
                q_occurrence,
                scope_id="scope.actual_occurrence_augmented_route",
                carrier_id="carrier.actual_active_occurrences",
                normalization_id="norm.physical_atomic",
                route_kind="ARCHITECTURE_ROUTE",
            ),
            node(
                "H1.complete_FUM_scalar_oX",
                "TARGET",
                "ARITHMETIC_TARGET",
                "NOT_TESTABLE",
                [],
                q_archive,
                scope_id="scope.complete_original_scale_FUM",
                carrier_id="carrier.all_nonsoft_cut_paths",
                normalization_id="norm.physical_atomic",
                route_kind="ARCHITECTURE_ROUTE",
            ),
            node(
                "H1.theorem_backed_ETO_disposition",
                "TARGET",
                "STRUCTURAL",
                "NOT_TESTABLE",
                [],
                q_archive,
                scope_id="scope.growing_scale_ETO",
                carrier_id="carrier.all_nonsoft_cut_paths",
                normalization_id="norm.physical_atomic",
                route_kind="ARCHITECTURE_ROUTE",
            ),
            node(
                "H1.scalar_clause",
                "ALL",
                "STRUCTURAL",
                "NOT_TESTABLE",
                ["H1.complete_FUM_scalar_oX", "H1.theorem_backed_ETO_disposition"],
                q_archive,
                scope_id="scope.scalar_plus_ETO_route",
                carrier_id="carrier.all_nonsoft_cut_paths",
                normalization_id="norm.physical_atomic",
                route_kind="ARCHITECTURE_ROUTE",
            ),
            node(
                "H9.literal_weight_registry",
                "TARGET",
                "PHYSICAL_REGISTRY",
                "NOT_TESTABLE",
                [],
                q_weight_registry,
                scope_id="scope.actual_fixed_h0_endpoint",
                carrier_id="carrier.actual_fixed_h0_packet",
                normalization_id="norm.endpoint_amplitude",
            ),
            node(
                "H9.phase_cell_registry",
                "TARGET",
                "PHYSICAL_REGISTRY",
                "NOT_TESTABLE",
                [],
                q_phase_registry,
                scope_id="scope.actual_fixed_h0_endpoint",
                carrier_id="carrier.actual_fixed_h0_packet",
                normalization_id="norm.endpoint_amplitude",
            ),
            node(
                "H9.endpoint_registry",
                "TARGET",
                "PHYSICAL_REGISTRY",
                "NOT_TESTABLE",
                [],
                q_endpoint_registry,
                scope_id="scope.actual_fixed_h0_endpoint",
                carrier_id="carrier.actual_fixed_h0_packet",
                normalization_id="norm.endpoint_amplitude",
            ),
            node(
                "H9.normalization_registry",
                "TARGET",
                "PHYSICAL_REGISTRY",
                "NOT_TESTABLE",
                [],
                q_normalization_registry,
                scope_id="scope.actual_fixed_h0_endpoint",
                carrier_id="carrier.actual_fixed_h0_packet",
                normalization_id="norm.endpoint_amplitude",
            ),
            node(
                "O161.direct_additive_twist_fixed_atom",
                "TARGET",
                "ARITHMETIC_TARGET",
                "OPEN",
                [],
                q_fixed_estimate,
                scope_id="scope.actual_core_named_fixed_phase",
                carrier_id="carrier.determinant_two_actual_core",
                normalization_id="norm.q_over_N",
                route_kind="ARITHMETIC_SUBROUTE",
            ),
            node(
                "O161.bad_endpoint_pointwise_fixed_atom",
                "TARGET",
                "ARITHMETIC_TARGET",
                "OPEN",
                [],
                q_fixed_estimate,
                scope_id="scope.actual_core_named_fixed_phase_endpoint",
                carrier_id="carrier.determinant_two_actual_core",
                normalization_id="norm.q_over_T",
                route_kind="ARITHMETIC_SUBROUTE",
            ),
            node(
                "H2.metric_fixed_atom_crosswalk",
                "TARGET",
                "ARITHMETIC_TARGET",
                "NOT_TESTABLE",
                ["A170.metric_packet_corridor", "H9.phase_cell_registry"],
                q_fixed_estimate,
                scope_id="scope.source_backed_metric_to_fixed_atom",
                carrier_id="carrier.actual_fixed_h0_packet",
                normalization_id="norm.endpoint_amplitude",
                route_kind="ARITHMETIC_SUBROUTE",
            ),
            node(
                "H2.phase_metric_clause",
                "ALL",
                "ARITHMETIC_TARGET",
                "NOT_TESTABLE",
                ["A170.metric_packet_corridor", "H2.metric_fixed_atom_crosswalk"],
                q_fixed_estimate,
                scope_id="scope.actual_fixed_h0_endpoint",
                carrier_id="carrier.actual_fixed_h0_packet",
                normalization_id="norm.endpoint_amplitude",
                route_kind="ARITHMETIC_SUBROUTE",
            ),
            node(
                "H2.phase_direct_clause",
                "ALL",
                "ARITHMETIC_TARGET",
                "OPEN",
                ["O161.direct_additive_twist_fixed_atom"],
                q_fixed_estimate,
                scope_id="scope.actual_fixed_h0_endpoint",
                carrier_id="carrier.actual_fixed_h0_packet",
                normalization_id="norm.endpoint_amplitude",
                route_kind="ARITHMETIC_SUBROUTE",
            ),
            node(
                "H2.phase_return",
                "ANY_CLAUSE",
                "ARITHMETIC_TARGET",
                "NOT_TESTABLE",
                ["H2.phase_metric_clause", "H2.phase_direct_clause"],
                q_fixed_estimate,
                scope_id="scope.actual_fixed_h0_endpoint",
                carrier_id="carrier.actual_fixed_h0_packet",
                normalization_id="norm.endpoint_amplitude",
            ),
            node(
                "H4.metric_all_prefix_clause",
                "ALL",
                "ARITHMETIC_TARGET",
                "NOT_TESTABLE",
                ["A169.phase_maximal_prefix", "H2.metric_fixed_atom_crosswalk", "H9.endpoint_registry"],
                q_fixed_estimate,
                scope_id="scope.actual_fixed_h0_endpoint",
                carrier_id="carrier.actual_fixed_h0_packet",
                normalization_id="norm.endpoint_amplitude",
                route_kind="ARITHMETIC_SUBROUTE",
            ),
            node(
                "H4.pointwise_endpoint_clause",
                "ALL",
                "ARITHMETIC_TARGET",
                "OPEN",
                ["O161.bad_endpoint_pointwise_fixed_atom"],
                q_fixed_estimate,
                scope_id="scope.actual_fixed_h0_endpoint",
                carrier_id="carrier.actual_fixed_h0_packet",
                normalization_id="norm.endpoint_amplitude",
                route_kind="ARITHMETIC_SUBROUTE",
            ),
            node(
                "H4.endpoint_return",
                "ANY_CLAUSE",
                "ARITHMETIC_TARGET",
                "NOT_TESTABLE",
                ["H4.metric_all_prefix_clause", "H4.pointwise_endpoint_clause"],
                q_fixed_estimate,
                scope_id="scope.actual_fixed_h0_endpoint",
                carrier_id="carrier.actual_fixed_h0_packet",
                normalization_id="norm.endpoint_amplitude",
            ),
            node(
                "H3.actual_packet_saving",
                "ALL",
                "ARITHMETIC_TARGET",
                "NOT_TESTABLE",
                [
                    "H9.literal_weight_registry",
                    "H2.phase_return",
                    "H4.endpoint_return",
                    "H9.normalization_registry",
                ],
                q_fixed_estimate,
                scope_id="scope.actual_fixed_h0_endpoint",
                carrier_id="carrier.actual_fixed_h0_packet",
                normalization_id="norm.endpoint_amplitude",
            ),
            node(
                "H3.fixed_X_power_upgrade",
                "TARGET",
                "ARITHMETIC_TARGET",
                "NOT_TESTABLE",
                ["H3.actual_packet_saving"],
                q_fixed_estimate,
                scope_id="scope.actual_fixed_h0_endpoint",
                carrier_id="carrier.actual_fixed_h0_packet",
                normalization_id="norm.endpoint_amplitude",
            ),
            node(
                "H5.complete_four_sign_return",
                "TARGET",
                "ARITHMETIC_TARGET",
                "NOT_TESTABLE",
                ["H3.fixed_X_power_upgrade", "H1.occurrence_registry_totality"],
                q_fixed_estimate,
                scope_id="scope.actual_fixed_h0_endpoint",
                carrier_id="carrier.actual_fixed_h0_packet",
                normalization_id="norm.endpoint_amplitude",
            ),
            node(
                "H6.physical_cover",
                "ALL",
                "STRUCTURAL",
                "NOT_TESTABLE",
                ["H1.defect.D_cover"],
                q_packet_data,
                scope_id="scope.actual_fixed_h0_endpoint",
                carrier_id="carrier.actual_fixed_h0_packet",
                normalization_id="norm.endpoint_amplitude",
            ),
            node(
                "H7.fixed_h0_totality",
                "ALL",
                "STRUCTURAL",
                "NOT_TESTABLE",
                ["H1.defect.D_P"],
                q_packet_data,
                scope_id="scope.actual_fixed_h0_endpoint",
                carrier_id="carrier.actual_fixed_h0_packet",
                normalization_id="norm.endpoint_amplitude",
            ),
            node(
                "H8.final_reconnection",
                "ALL",
                "STRUCTURAL",
                "NOT_TESTABLE",
                ["H1.defect.D_rec", "H6.physical_cover", "H7.fixed_h0_totality"],
                q_packet_data,
                scope_id="scope.actual_fixed_h0_endpoint",
                carrier_id="carrier.actual_fixed_h0_packet",
                normalization_id="norm.endpoint_amplitude",
            ),
            node(
                "H9.physical_registry",
                "ALL",
                "PHYSICAL_REGISTRY",
                "NOT_TESTABLE",
                [
                    "H1.occurrence_registry_totality",
                    "H9.literal_weight_registry",
                    "H9.phase_cell_registry",
                    "H9.endpoint_registry",
                    "H9.normalization_registry",
                ],
                q_packet_data,
                scope_id="scope.actual_fixed_h0_endpoint",
                carrier_id="carrier.actual_fixed_h0_packet",
                normalization_id="norm.endpoint_amplitude",
            ),
            node(
                "ROOT.map_synthesis",
                "ALL",
                "ROOT",
                "NOT_TESTABLE",
                [
                    "H1.map_clause",
                    "H2.phase_return",
                    "H3.actual_packet_saving",
                    "H3.fixed_X_power_upgrade",
                    "H4.endpoint_return",
                    "H5.complete_four_sign_return",
                    "H6.physical_cover",
                    "H7.fixed_h0_totality",
                    "H8.final_reconnection",
                    "H9.physical_registry",
                ],
                q_fixed_estimate,
                scope_id="scope.actual_fixed_h0_endpoint",
                carrier_id="carrier.actual_fixed_h0_packet",
                normalization_id="norm.endpoint_amplitude",
                route_kind="ARCHITECTURE_ROUTE",
            ),
            node(
                "ROOT.scalar_synthesis",
                "ALL",
                "ROOT",
                "NOT_TESTABLE",
                [
                    "H1.scalar_clause",
                    "H2.phase_return",
                    "H3.actual_packet_saving",
                    "H3.fixed_X_power_upgrade",
                    "H4.endpoint_return",
                    "H5.complete_four_sign_return",
                    "H9.physical_registry",
                ],
                q_fixed_estimate,
                scope_id="scope.actual_fixed_h0_endpoint",
                carrier_id="carrier.actual_fixed_h0_packet",
                normalization_id="norm.endpoint_amplitude",
                route_kind="ARCHITECTURE_ROUTE",
            ),
        ]
    )

    nodes_by_id = {record["node_id"]: record for record in nodes}
    if len(nodes_by_id) != len(nodes):
        raise ValueError("duplicate DAG node")
    for record in nodes:
        if record["status"] not in STATUSES or record["role"] not in ROLES:
            raise ValueError("invalid DAG node status or role")
        validate_q(record["quantifier_signature"])
        for parent in record["parents"]:
            if parent not in nodes_by_id:
                raise ValueError(f"unknown DAG parent: {parent}")
    # Cycle check.
    for node_id in nodes_by_id:
        if node_id in ancestors(nodes_by_id, node_id):
            raise ValueError("DAG contains a cycle")
    if nodes_by_id["H1.source_backed_local_occurrence_edge_family"][
        "quantifier_signature"
    ]["support_axis"] != "SOURCE_BACKED_LOCAL_SUPPORT":
        raise ValueError("local occurrence edges promoted to active support")
    if nodes_by_id["H1.canonical_minimal_representation_certificate"][
        "quantifier_signature"
    ]["support_axis"] != "FORMAL_OCCURRENCE":
        raise ValueError("canonical representation promoted to active support")
    if nodes_by_id["H1.actual_active_support_certificate"][
        "quantifier_signature"
    ]["support_axis"] != "ACTUAL_ACTIVE_SUPPORT":
        raise ValueError("active-support certificate lost its target quantifier")
    if nodes_by_id["H1.actual_occurrence_lift"]["quantifier_signature"][
        "support_axis"
    ] != "ACTUAL_ACTIVE_SUPPORT":
        raise ValueError("actual lift lacks active-support target")
    registry_axes = {
        "H9.literal_weight_registry": (
            "LITERAL_WEIGHT_REGISTRY",
            "NOT_APPLICABLE",
            "NOT_APPLICABLE",
        ),
        "H9.phase_cell_registry": (
            "PHYSICAL_PHASE_REGISTRY",
            "NAMED_FIXED_ATOM",
            "NOT_APPLICABLE",
        ),
        "H9.endpoint_registry": (
            "PHYSICAL_ENDPOINT_REGISTRY",
            "NOT_APPLICABLE",
            "DETERMINISTIC_ALL_PREFIX",
        ),
        "H9.normalization_registry": (
            "PHYSICAL_NORMALIZATION_REGISTRY",
            "NOT_APPLICABLE",
            "NOT_APPLICABLE",
        ),
    }
    for node_id, (carrier_axis, phase_axis, endpoint_axis) in registry_axes.items():
        signature = nodes_by_id[node_id]["quantifier_signature"]
        if (
            signature["carrier_axis"] != carrier_axis
            or signature["phase_axis"] != phase_axis
            or signature["endpoint_axis"] != endpoint_axis
            or signature["decay_axis"] != "NONE"
        ):
            raise ValueError(f"data registry carries theorem decay or wrong data axis: {node_id}")

    blockers = minimal_blockers(nodes_by_id, "ROOT.map_synthesis")
    expected_blockers = [
        "H1.source_backed_local_occurrence_edge_family",
        "H1.actual_active_support_certificate",
        "H1.canonical_minimal_representation_certificate",
        "H9.literal_weight_registry",
        "H9.phase_cell_registry",
        "H9.endpoint_registry",
        "H9.normalization_registry",
    ]
    if blockers != expected_blockers:
        raise ValueError(f"selected-root blocker antichain drift: {blockers}")
    open_frontier = parent_ready_open(nodes_by_id, "ROOT.map_synthesis")
    if open_frontier != [
        "O161.bad_endpoint_pointwise_fixed_atom",
        "O161.direct_additive_twist_fixed_atom",
    ]:
        raise ValueError(f"parent-ready OPEN frontier drift: {open_frontier}")

    h9_ancestors = sorted(ancestors(nodes_by_id, "H9.physical_registry"))
    if any(nodes_by_id[item]["role"] in ARITHMETIC_ROLES for item in h9_ancestors):
        raise ValueError("H9 has an arithmetic ancestor")

    route_families = {
        "architecture": {
            "selected_route": "occurrence_augmented_map",
            "selected_root": "ROOT.map_synthesis",
            "universe_completeness": {
                "status": "NOT_PROVED",
                "source_export": None,
                "scope": "actual_fixed_h0_physical_architectures",
            },
            "records": {
                "current_schema_only_canonical_lift": {
                    "route_kind": "ARCHITECTURE_ROUTE",
                    "state": "STOP_SCOPED",
                    "stopped": True,
                    "selected": False,
                    "root_node": None,
                    "scope_id": "CURRENT_ARCHIVE_FIELDS_ONLY",
                    "source_export": "TPC154.current_schema_only_lift",
                    "registry_id": "registry.current_archive",
                },
                "occurrence_augmented_map": {
                    "route_kind": "ARCHITECTURE_ROUTE",
                    "state": "OPEN_NOT_TESTABLE",
                    "stopped": False,
                    "selected": True,
                    "root_node": "ROOT.map_synthesis",
                    "scope_id": "ACTUAL_OCCURRENCE_AUGMENTED_CARRIER",
                    "source_export": None,
                    "registry_id": "registry.production_occurrence",
                },
                "scalar_plus_ETO": {
                    "route_kind": "ARCHITECTURE_ROUTE",
                    "state": "OPEN_NOT_TESTABLE",
                    "stopped": False,
                    "selected": False,
                    "root_node": "ROOT.scalar_synthesis",
                    "scope_id": "COMPLETE_ORIGINAL_SCALE_FUM_PLUS_ETO",
                    "source_export": None,
                    "registry_id": "registry.scalar_plus_ETO",
                },
            },
            "typed_alternative": None,
            "typed_alternative_crosswalk": None,
        },
        "arithmetic_subroutes": {
            "records": {
                "periodic_major": {
                    "route_kind": "ARITHMETIC_SUBROUTE",
                    "state": "OPEN_NOT_TESTABLE",
                    "scope_id": "SMALL_PERIOD_MAJOR_ARC",
                },
                "direct_twist_fixed_atom": {
                    "route_kind": "ARITHMETIC_SUBROUTE",
                    "state": "OPEN_PARENT_READY",
                    "scope_id": "NAMED_FIXED_PHASE",
                },
                "phase_metric_source_backed": {
                    "route_kind": "ARITHMETIC_SUBROUTE",
                    "state": "OPEN_NOT_TESTABLE",
                    "scope_id": "SOURCE_BACKED_METRIC_TO_FIXED_ATOM",
                },
                "phase_metric_uncontrolled_atomic": {
                    "route_kind": "ARITHMETIC_SUBROUTE",
                    "state": "STOP_SCOPED",
                    "scope_id": "UNCONTROLLED_ATOMIC_PROMOTION_ONLY",
                },
                "bad_endpoint_pointwise_fixed_atom": {
                    "route_kind": "ARITHMETIC_SUBROUTE",
                    "state": "OPEN_PARENT_READY",
                    "scope_id": "NAMED_FIXED_PHASE_ENDPOINT",
                },
            },
            "architecture_reroute_eligible": False,
        },
    }

    charges = [
        {
            "charge_id": "ARITH.phase_metric_power",
            "owner": "arithmetic",
            "quantity_kind": "FIXED_X_POWER_PHASE_METRIC",
            "state": "PROVED",
            "value": "every delta<1/4 on the explicit packet schedule",
            "eligible_for_named_fixed_atom": False,
            "source_export": "A170.metric_packet_corridor",
        },
        {
            "charge_id": "ARITH.packet_union",
            "owner": "arithmetic",
            "quantity_kind": "POLYLOG_PACKET_UNION_COST",
            "state": "PROVED_PAID",
            "value": "included in the Borel-Cantelli summability condition",
            "eligible_for_named_fixed_atom": False,
            "source_export": "A170.metric_packet_corridor",
        },
        {
            "charge_id": "PHYS.phase_atom_crosswalk",
            "owner": "physical",
            "quantity_kind": "METRIC_TO_NAMED_ATOM_COST",
            "state": "NOT_TESTABLE",
            "value": None,
            "eligible_for_named_fixed_atom": False,
            "source_export": None,
        },
        {
            "charge_id": "PHYS.literal_weight",
            "owner": "physical",
            "quantity_kind": "LITERAL_WEIGHT_COST",
            "state": "NOT_TESTABLE",
            "value": None,
            "eligible_for_named_fixed_atom": False,
            "source_export": None,
        },
        {
            "charge_id": "PHYS.endpoint",
            "owner": "physical",
            "quantity_kind": "DETERMINISTIC_ENDPOINT_COST",
            "state": "NOT_TESTABLE",
            "value": None,
            "eligible_for_named_fixed_atom": False,
            "source_export": None,
        },
        {
            "charge_id": "PHYS.four_sign_reconnection",
            "owner": "physical",
            "quantity_kind": "RECONNECTION_COST",
            "state": "NOT_TESTABLE",
            "value": None,
            "eligible_for_named_fixed_atom": False,
            "source_export": None,
        },
    ]

    return {
        "schema": "tpc-171-source-locked-occurrence-phase-return-integration-v1",
        "snapshot": {
            "date": "2026-07-28",
            "source_range": "TPC-163--170",
            "hash_mode": HASH_MODE,
            "hash_semantics": "INTEGRITY_ONLY",
            "selected_architecture_route": "occurrence_augmented_map",
            "selected_root": "ROOT.map_synthesis",
        },
        "source_locks": source_locks(),
        "quantifier_contract": {
            "axes": list(Q_AXES),
            "allowed_values": {key: sorted(value) for key, value in Q_ALLOWED.items()},
            "promotion_policy": (
                "No import may be promoted from phase average, registry density, "
                "or Lebesgue-a.e. phase to a named fixed atom; from formal to "
                "active support; or from an explicit schedule to all scales."
            ),
        },
        "imports": imports,
        "structural_state": {
            "production_cut_count": 2988,
            "native_triple_count": 866,
            "collision_row_count": 2976,
            "collision_excess": 2122,
            "production_theorem_edge_count": 0,
            "unique_minimal_archive_address": [
                "ell",
                "k",
                "native_d",
                "jL",
                "jK",
            ],
            "archive_key_semantics": "ADDRESSING_ONLY",
            "formal_gluing": "PROVED_FOR_SUPPLIED_COMPATIBLE_LOCAL_FAMILIES",
            "formal_totality": "NOT_TESTABLE",
            "actual_active_support": "NOT_TESTABLE",
            "canonical_minimality": "NOT_TESTABLE",
            "parallel_crosswalk_roots": expected_roots,
            "map_clause": "NOT_TESTABLE",
            "scalar_clause": "NOT_TESTABLE",
        },
        "arithmetic_state": {
            "strongest_export": "A170.metric_packet_corridor",
            "strongest_level": "L1_ACTUAL_CORE_PHASE_METRIC_PACKET_CORRIDOR",
            "analytic_norm": "L2_PHASE_MAXIMAL_BC",
            "phase_quantifier": "LEBESGUE_AE_FIXED_PHASE",
            "endpoint_quantifier": "ALL_PREFIX_THETA_SHELL",
            "program_positive_L2": False,
            "named_fixed_atom": False,
            "production_phase_registry": False,
            "metric_to_uncontrolled_atom_route": "STOP_SCOPED",
            "pointwise_fixed_atom_routes": "OPEN",
        },
        "route_families": route_families,
        "nodes": nodes,
        "typed_frontiers": {
            "minimal_not_testable_antichain": [
                {
                    "node_id": item,
                    "role": nodes_by_id[item]["role"],
                    "status": "NOT_TESTABLE",
                    "quantifier_signature": nodes_by_id[item]["quantifier_signature"],
                }
                for item in blockers
            ],
            "parent_ready_open_frontier": [
                {
                    "node_id": item,
                    "role": nodes_by_id[item]["role"],
                    "status": "OPEN",
                    "quantifier_signature": nodes_by_id[item]["quantifier_signature"],
                }
                for item in open_frontier
            ],
            "selection_rule": (
                "SELECTED_ARCHITECTURE_ROOT_THEN_MINIMAL_MISSING_ANCESTOR_"
                "THEN_DECLARED_OBLIGATION_ORDER_THEN_NODE_ID"
            ),
            "frontiers_are_type_disjoint": True,
        },
        "h9_arithmetic_firewall": {
            "root_node": "H9.physical_registry",
            "transitive_ancestor_ids": h9_ancestors,
            "arithmetic_ancestor_ids": [
                item for item in h9_ancestors if nodes_by_id[item]["role"] in ARITHMETIC_ROLES
            ],
            "firewall_pass": True,
            "policy": "H9_MUST_HAVE_NO_DIRECT_OR_TRANSITIVE_ARITHMETIC_ANCESTOR",
        },
        "endpoint_ledger_v4": {
            "contract": "MVP7_FIXED_H0_NON_DUPLICATING_ENDPOINT_V4",
            "scale": "AMPLITUDE",
            "literal_gate": {
                "literal_physical_coefficients": "NOT_TESTABLE",
                "fixed_physical_h0": "PROVED",
                "physical_atomic_normalization": "NOT_TESTABLE",
                "canonical_or_minimal_representation": "NOT_TESTABLE",
                "actual_active_support": "NOT_TESTABLE",
                "strict_one_over_400_budget": "NOT_TESTABLE",
            },
            "registry_gate": {
                "source_backed_local_occurrence_edge_family": "NOT_TESTABLE",
                "active_support_certificate": "NOT_TESTABLE",
                "canonical_minimal_representation_certificate": "NOT_TESTABLE",
                "occurrence_registry": "NOT_TESTABLE",
                "literal_weight_registry": "NOT_TESTABLE",
                "phase_registry": "NOT_TESTABLE",
                "endpoint_registry": "NOT_TESTABLE",
                "normalization_registry": "NOT_TESTABLE",
            },
            "phase_mode": {
                "proved": "LEBESGUE_AE_FIXED_PHASE",
                "required": "NAMED_FIXED_ATOM",
                "atom_concentration_bound": None,
                "separation_bound": None,
                "fixed_atom_crosswalk": "NOT_TESTABLE",
            },
            "endpoint_mode": {
                "proved": "ALL_PREFIX_THETA_SHELL_IN_PHASE_METRIC",
                "required": "DETERMINISTIC_ALL_PREFIX_AT_NAMED_FIXED_ATOM",
            },
            "charge_registry": charges,
            "invariants": {
                "charge_ids_unique": len({item["charge_id"] for item in charges})
                == len(charges),
                "each_charge_has_one_owner": True,
                "metric_power_not_charged_as_named_atom_power": True,
                "unknown_is_not_zero": True,
                "full_synthesis_references_not_recharges": True,
            },
            "arithmetic": {
                "phase_metric_sigma": "every delta<1/4",
                "phase_metric_sigma_scope": "LEBESGUE_AE_EXPLICIT_PACKET_SCHEDULE",
                "named_fixed_atom_sigma": {"numerator": 0, "denominator": 1},
                "sigma_required": {"numerator": 1, "denominator": 400},
                "state": "PHASE_METRIC_ONLY",
            },
            "physical": {
                "registry_complete": False,
                "lambda_upper": None,
                "state": "NOT_TESTABLE",
            },
            "full_synthesis": {
                "scope_compatible": False,
                "strict_net_slack": None,
                "one_over_400_paid": False,
                "state": "INCOMPLETE",
            },
        },
        "first_missing": {
            "node_id": "H1.source_backed_local_occurrence_edge_family",
            "status": "NOT_TESTABLE",
            "selected_route": "occurrence_augmented_map",
            "minimal_not_testable_nodes": blockers,
            "selection_rule": (
                "SELECTED_ARCHITECTURE_ROOT_THEN_MINIMAL_MISSING_ANCESTOR_"
                "THEN_DECLARED_OBLIGATION_ORDER_THEN_NODE_ID"
            ),
        },
        "progress_classification": {
            "structural_progress": "THREE_FACTOR_CROSSWALK_GAP_LOCALIZED",
            "arithmetic_progress": "ACTUAL_CORE_PHASE_METRIC_ALL_PREFIX_PACKET_CORRIDOR",
            "actual_fixed_atom_progress": False,
            "actual_active_support_progress": False,
            "new_program_positive_L2": False,
            "strict_one_over_400": False,
        },
        "claim_boundary": {
            "source_hashes_prove_theorems": False,
            "zero_frozen_edges_mean_actual_edges_do_not_exist": False,
            "archive_address_is_occurrence_identity": False,
            "formal_gluing_is_actual_totality": False,
            "formal_support_is_actual_active_support": False,
            "phase_average_is_named_fixed_atom": False,
            "registry_density_identifies_distinguished_phase": False,
            "Lebesgue_ae_covers_production_phase": False,
            "metric_all_prefix_is_deterministic_physical_endpoint": False,
            "program_positive_L2": False,
            "strict_one_over_400": False,
            "prime_pair_lower_bound": False,
            "twin_prime_theorem": False,
            "architecture_route_universe_complete": False,
            "arithmetic_subroute_is_architecture_reroute": False,
        },
        "current_verdict": "NOT_TESTABLE",
    }


def validate_schema_top(value: dict[str, Any], schema_path: Path) -> None:
    schema = load_json(schema_path)
    if set(value) != set(schema["properties"]):
        raise ValueError(f"strict top-level schema mismatch for {schema_path.name}")
    if value["schema"] != schema["properties"]["schema"]["const"]:
        raise ValueError("schema id mismatch")


def validate_manifest(value: dict[str, Any], *, verify_sources: bool = True) -> None:
    validate_schema_top(value, MANIFEST_SCHEMA)
    if value["snapshot"]["hash_semantics"] != "INTEGRITY_ONLY":
        raise ValueError("source hash promoted to proof semantics")
    if value["current_verdict"] != "NOT_TESTABLE":
        raise ValueError("current verdict drift")
    if value["claim_boundary"] != {
        key: False for key in value["claim_boundary"]
    }:
        raise ValueError("claim boundary contains a promotion")
    if value["snapshot"]["selected_architecture_route"] != (
        value["route_families"]["architecture"]["selected_route"]
    ):
        raise ValueError("selected route drift")

    architecture = value["route_families"]["architecture"]
    arithmetic = value["route_families"]["arithmetic_subroutes"]
    if sum(
        bool(record["selected"]) for record in architecture["records"].values()
    ) != 1:
        raise ValueError("architecture selection is not unique")
    if any(
        record["route_kind"] != "ARCHITECTURE_ROUTE"
        for record in architecture["records"].values()
    ):
        raise ValueError("arithmetic subroute inserted into architecture universe")
    if any(
        record["route_kind"] != "ARITHMETIC_SUBROUTE"
        for record in arithmetic["records"].values()
    ):
        raise ValueError("architecture route inserted into arithmetic methods")
    if arithmetic["architecture_reroute_eligible"]:
        raise ValueError("arithmetic method made architecture-reroute eligible")
    if architecture["universe_completeness"]["status"] != "NOT_PROVED":
        raise ValueError("route-universe completeness promotion")

    for record in value["imports"]:
        validate_q(record["quantifier_signature"])
        if record["promotion_eligible"]:
            raise ValueError("current import marked promotion eligible")
    imports = {record["export_id"]: record for record in value["imports"]}
    if len(imports) != 8:
        raise ValueError("import registry drift")
    if imports["A170.metric_packet_corridor"]["quantifier_signature"][
        "phase_axis"
    ] != "LEBESGUE_AE_FIXED_PHASE":
        raise ValueError("TPC-170 phase quantifier drift")
    if imports["A170.metric_packet_corridor"]["quantifier_signature"][
        "support_axis"
    ] != "ACTUAL_CORE":
        raise ValueError("TPC-170 promoted to active support")

    nodes = value["nodes"]
    by_id = {record["node_id"]: record for record in nodes}
    if len(by_id) != len(nodes):
        raise ValueError("duplicate node id")
    for record in nodes:
        validate_q(record["quantifier_signature"])
        if record["status"] not in STATUSES or record["role"] not in ROLES:
            raise ValueError("invalid node")
        for parent in record["parents"]:
            if parent not in by_id:
                raise ValueError("unknown node parent")
    for node_id in by_id:
        if node_id in ancestors(by_id, node_id):
            raise ValueError("DAG cycle")
    if by_id["H1.source_backed_local_occurrence_edge_family"][
        "quantifier_signature"
    ]["support_axis"] != "SOURCE_BACKED_LOCAL_SUPPORT":
        raise ValueError("local occurrence edges promoted to active support")
    if by_id["H1.canonical_minimal_representation_certificate"][
        "quantifier_signature"
    ]["support_axis"] != "FORMAL_OCCURRENCE":
        raise ValueError("canonical representation promoted to active support")
    if by_id["H1.actual_active_support_certificate"][
        "quantifier_signature"
    ]["support_axis"] != "ACTUAL_ACTIVE_SUPPORT":
        raise ValueError("active-support target quantifier drift")
    actual_lift = by_id["H1.actual_occurrence_lift"]
    if (
        actual_lift["quantifier_signature"]["support_axis"]
        != "ACTUAL_ACTIVE_SUPPORT"
        or set(actual_lift["parents"])
        != {
            "H1.source_backed_local_occurrence_edge_family",
            "H1.actual_active_support_certificate",
            "H1.canonical_minimal_representation_certificate",
        }
    ):
        raise ValueError("actual lift does not consume all three production roots")
    registry_axes = {
        "H9.literal_weight_registry": (
            "LITERAL_WEIGHT_REGISTRY",
            "NOT_APPLICABLE",
            "NOT_APPLICABLE",
        ),
        "H9.phase_cell_registry": (
            "PHYSICAL_PHASE_REGISTRY",
            "NAMED_FIXED_ATOM",
            "NOT_APPLICABLE",
        ),
        "H9.endpoint_registry": (
            "PHYSICAL_ENDPOINT_REGISTRY",
            "NOT_APPLICABLE",
            "DETERMINISTIC_ALL_PREFIX",
        ),
        "H9.normalization_registry": (
            "PHYSICAL_NORMALIZATION_REGISTRY",
            "NOT_APPLICABLE",
            "NOT_APPLICABLE",
        ),
    }
    for node_id, (carrier_axis, phase_axis, endpoint_axis) in registry_axes.items():
        signature = by_id[node_id]["quantifier_signature"]
        if (
            signature["carrier_axis"] != carrier_axis
            or signature["phase_axis"] != phase_axis
            or signature["endpoint_axis"] != endpoint_axis
            or signature["decay_axis"] != "NONE"
        ):
            raise ValueError(f"data registry carries theorem decay or wrong data axis: {node_id}")

    blockers = minimal_blockers(by_id, "ROOT.map_synthesis")
    recorded = [
        item["node_id"]
        for item in value["typed_frontiers"]["minimal_not_testable_antichain"]
    ]
    if recorded != blockers:
        raise ValueError("typed blocker antichain drift")
    open_nodes = parent_ready_open(by_id, "ROOT.map_synthesis")
    recorded_open = [
        item["node_id"]
        for item in value["typed_frontiers"]["parent_ready_open_frontier"]
    ]
    if recorded_open != open_nodes:
        raise ValueError("parent-ready OPEN frontier drift")
    if set(recorded) & set(recorded_open):
        raise ValueError("NOT_TESTABLE and OPEN frontiers merged")
    if value["first_missing"]["node_id"] != blockers[0]:
        raise ValueError("first missing drift")

    h9_ancestors = sorted(ancestors(by_id, "H9.physical_registry"))
    arithmetic_ancestors = [
        item for item in h9_ancestors if by_id[item]["role"] in ARITHMETIC_ROLES
    ]
    firewall = value["h9_arithmetic_firewall"]
    if (
        firewall["transitive_ancestor_ids"] != h9_ancestors
        or firewall["arithmetic_ancestor_ids"] != arithmetic_ancestors
        or arithmetic_ancestors
        or not firewall["firewall_pass"]
    ):
        raise ValueError("H9 arithmetic firewall failure")

    structural = value["structural_state"]
    if (
        structural["production_cut_count"],
        structural["native_triple_count"],
        structural["collision_row_count"],
        structural["collision_excess"],
        structural["production_theorem_edge_count"],
    ) != (2988, 866, 2976, 2122, 0):
        raise ValueError("structural source summary drift")
    if structural["archive_key_semantics"] != "ADDRESSING_ONLY":
        raise ValueError("archive key promoted")
    if structural["actual_active_support"] != "NOT_TESTABLE":
        raise ValueError("formal support promoted")

    arithmetic_state = value["arithmetic_state"]
    if (
        arithmetic_state["program_positive_L2"]
        or arithmetic_state["named_fixed_atom"]
        or arithmetic_state["production_phase_registry"]
    ):
        raise ValueError("phase metric promoted to physical pointwise theorem")
    if arithmetic_state["metric_to_uncontrolled_atom_route"] != "STOP_SCOPED":
        raise ValueError("TPC-170 scoped stop drift")

    ledger = value["endpoint_ledger_v4"]
    if any(
        ledger["literal_gate"][key] != "NOT_TESTABLE"
        for key in (
            "literal_physical_coefficients",
            "physical_atomic_normalization",
            "canonical_or_minimal_representation",
            "actual_active_support",
            "strict_one_over_400_budget",
        )
    ):
        raise ValueError("endpoint V4 literal gate promotion")
    if ledger["literal_gate"]["fixed_physical_h0"] != "PROVED":
        raise ValueError("fixed h0 anchor lost")
    if ledger["phase_mode"]["proved"] != "LEBESGUE_AE_FIXED_PHASE":
        raise ValueError("phase-mode quantifier drift")
    if ledger["phase_mode"]["required"] != "NAMED_FIXED_ATOM":
        raise ValueError("fixed-atom requirement weakened")
    if ledger["arithmetic"]["named_fixed_atom_sigma"] != {
        "numerator": 0,
        "denominator": 1,
    }:
        raise ValueError("metric power charged as fixed-atom power")
    if ledger["full_synthesis"]["one_over_400_paid"]:
        raise ValueError("1/400 marked paid")
    charges = ledger["charge_registry"]
    if len({item["charge_id"] for item in charges}) != len(charges):
        raise ValueError("duplicate endpoint charge")
    if any(
        item["quantity_kind"].startswith("FIXED_X_POWER_PHASE")
        and item["eligible_for_named_fixed_atom"]
        for item in charges
    ):
        raise ValueError("metric power promoted in charge ledger")

    if verify_sources:
        expected_paths: set[str] = set()
        for number in range(163, 171):
            directory = paper_dir(number)
            candidates = [directory / "main.tex"]
            candidates.extend(sorted((directory / "schemas").glob("*.json")))
            candidates.extend(sorted((directory / "experiments").glob("*.py")))
            candidates.extend(sorted((directory / "experiments").glob("*.json")))
            expected_paths.update(repo_relative(path) for path in candidates)
        recorded_paths = {item["path"] for item in value["source_locks"]}
        if recorded_paths != expected_paths:
            raise ValueError("source-lock coverage drift")
        for record in value["source_locks"]:
            if record["hash_semantics"] != "INTEGRITY_ONLY":
                raise ValueError("source lock has theorem semantics")
            path = REPO / record["path"]
            if not path.is_file() or sha256(path) != record["canonical_utf8_lf_sha256"]:
                raise ValueError("source hash drift")


def mutation_rejected(
    manifest: dict[str, Any],
    mutate: Any,
) -> bool:
    clone = copy.deepcopy(manifest)
    mutate(clone)
    try:
        validate_manifest(clone, verify_sources=True)
    except (ValueError, FileNotFoundError, KeyError, TypeError):
        return True
    return False


def build_audit(manifest: dict[str, Any]) -> dict[str, Any]:
    validate_manifest(manifest)

    def set_import_axis(
        value: dict[str, Any], export_id: str, axis: str, replacement: str
    ) -> None:
        record = next(item for item in value["imports"] if item["export_id"] == export_id)
        record["quantifier_signature"][axis] = replacement

    mutations = {
        "reject_source_hash_as_theorem": mutation_rejected(
            manifest,
            lambda value: value["snapshot"].__setitem__(
                "hash_semantics", "THEOREM_EVIDENCE"
            ),
        ),
        "reject_zero_edge_as_nonexistence": mutation_rejected(
            manifest,
            lambda value: value["claim_boundary"].__setitem__(
                "zero_frozen_edges_mean_actual_edges_do_not_exist", True
            ),
        ),
        "reject_archive_address_as_occurrence_id": mutation_rejected(
            manifest,
            lambda value: value["structural_state"].__setitem__(
                "archive_key_semantics", "CANONICAL_OCCURRENCE_ID"
            ),
        ),
        "reject_formal_support_as_active": mutation_rejected(
            manifest,
            lambda value: value["structural_state"].__setitem__(
                "actual_active_support", "PROVED"
            ),
        ),
        "reject_local_edges_as_active_support": mutation_rejected(
            manifest,
            lambda value: next(
                item
                for item in value["nodes"]
                if item["node_id"]
                == "H1.source_backed_local_occurrence_edge_family"
            )["quantifier_signature"].__setitem__(
                "support_axis", "ACTUAL_ACTIVE_SUPPORT"
            ),
        ),
        "reject_canonicality_as_active_support": mutation_rejected(
            manifest,
            lambda value: next(
                item
                for item in value["nodes"]
                if item["node_id"]
                == "H1.canonical_minimal_representation_certificate"
            )["quantifier_signature"].__setitem__(
                "support_axis", "ACTUAL_ACTIVE_SUPPORT"
            ),
        ),
        "reject_weight_registry_decay_promotion": mutation_rejected(
            manifest,
            lambda value: next(
                item
                for item in value["nodes"]
                if item["node_id"] == "H9.literal_weight_registry"
            )["quantifier_signature"].__setitem__(
                "decay_axis", "FIXED_X_POWER_FIXED_ATOM"
            ),
        ),
        "reject_phase_registry_decay_promotion": mutation_rejected(
            manifest,
            lambda value: next(
                item
                for item in value["nodes"]
                if item["node_id"] == "H9.phase_cell_registry"
            )["quantifier_signature"].__setitem__(
                "decay_axis", "FIXED_X_POWER_FIXED_ATOM"
            ),
        ),
        "reject_endpoint_registry_decay_promotion": mutation_rejected(
            manifest,
            lambda value: next(
                item
                for item in value["nodes"]
                if item["node_id"] == "H9.endpoint_registry"
            )["quantifier_signature"].__setitem__(
                "decay_axis", "FIXED_X_POWER_FIXED_ATOM"
            ),
        ),
        "reject_normalization_registry_decay_promotion": mutation_rejected(
            manifest,
            lambda value: next(
                item
                for item in value["nodes"]
                if item["node_id"] == "H9.normalization_registry"
            )["quantifier_signature"].__setitem__(
                "decay_axis", "FIXED_X_POWER_FIXED_ATOM"
            ),
        ),
        "reject_phase_ae_as_named_atom": mutation_rejected(
            manifest,
            lambda value: set_import_axis(
                value,
                "A170.metric_packet_corridor",
                "phase_axis",
                "NAMED_FIXED_ATOM",
            ),
        ),
        "reject_metric_support_as_physical_active": mutation_rejected(
            manifest,
            lambda value: set_import_axis(
                value,
                "A170.metric_packet_corridor",
                "support_axis",
                "ACTUAL_ACTIVE_SUPPORT",
            ),
        ),
        "reject_metric_power_as_fixed_atom_charge": mutation_rejected(
            manifest,
            lambda value: value["endpoint_ledger_v4"]["charge_registry"][0].__setitem__(
                "eligible_for_named_fixed_atom", True
            ),
        ),
        "reject_named_atom_sigma_promotion": mutation_rejected(
            manifest,
            lambda value: value["endpoint_ledger_v4"]["arithmetic"].__setitem__(
                "named_fixed_atom_sigma", {"numerator": 1, "denominator": 5}
            ),
        ),
        "reject_arithmetic_ancestor_in_H9": mutation_rejected(
            manifest,
            lambda value: next(
                item for item in value["nodes"] if item["node_id"] == "H9.physical_registry"
            )["parents"].append("A170.metric_packet_corridor"),
        ),
        "reject_arithmetic_method_as_architecture_route": mutation_rejected(
            manifest,
            lambda value: value["route_families"]["architecture"]["records"].__setitem__(
                "direct_twist_fixed_atom",
                {
                    "route_kind": "ARITHMETIC_SUBROUTE",
                    "state": "OPEN_PARENT_READY",
                    "stopped": False,
                    "selected": False,
                    "root_node": None,
                    "scope_id": "NAMED_FIXED_PHASE",
                    "source_export": None,
                    "registry_id": "registry.fake",
                },
            ),
        ),
        "reject_arithmetic_method_reroute": mutation_rejected(
            manifest,
            lambda value: value["route_families"]["arithmetic_subroutes"].__setitem__(
                "architecture_reroute_eligible", True
            ),
        ),
        "reject_unproved_route_universe": mutation_rejected(
            manifest,
            lambda value: value["route_families"]["architecture"][
                "universe_completeness"
            ].__setitem__("status", "PROVED"),
        ),
        "reject_blocker_antichain_collapse": mutation_rejected(
            manifest,
            lambda value: value["typed_frontiers"].__setitem__(
                "minimal_not_testable_antichain",
                value["typed_frontiers"]["minimal_not_testable_antichain"][:1],
            ),
        ),
        "reject_open_nt_frontier_merge": mutation_rejected(
            manifest,
            lambda value: value["typed_frontiers"]["parent_ready_open_frontier"].append(
                copy.deepcopy(
                    value["typed_frontiers"]["minimal_not_testable_antichain"][0]
                )
            ),
        ),
        "reject_one_over_400_without_literal_gate": mutation_rejected(
            manifest,
            lambda value: value["endpoint_ledger_v4"]["full_synthesis"].__setitem__(
                "one_over_400_paid", True
            ),
        ),
        "reject_source_hash_drift": mutation_rejected(
            manifest,
            lambda value: value["source_locks"][0].__setitem__(
                "canonical_utf8_lf_sha256", "0" * 64
            ),
        ),
    }
    if not all(mutations.values()):
        raise ValueError(
            f"mutation regression escaped: {[k for k, passed in mutations.items() if not passed]}"
        )

    return {
        "schema": "tpc-171-source-locked-occurrence-phase-return-audit-v1",
        "status": "PASS",
        "manifest_sha256": payload_sha256(manifest),
        "checks": {
            "source_locks_verified": True,
            "six_axis_quantifiers_complete": True,
            "three_parallel_crosswalk_roots_preserved": True,
            "archive_addressing_not_occurrence_identity": True,
            "formal_gluing_not_actual_totality": True,
            "phase_metric_not_named_fixed_atom": True,
            "metric_power_not_program_positive_L2": True,
            "architecture_and_arithmetic_routes_disjoint": True,
            "H9_arithmetic_firewall": True,
            "typed_frontiers_recomputed": True,
            "endpoint_v4_nonduplicating": True,
            "strict_one_over_400_unpaid": True,
        },
        "mutation_regressions": mutations,
        "current_verdict": "NOT_TESTABLE",
        "first_missing": "H1.source_backed_local_occurrence_edge_family",
        "claim_boundary": copy.deepcopy(manifest["claim_boundary"]),
    }


def validate_audit(value: dict[str, Any], manifest: dict[str, Any]) -> None:
    validate_schema_top(value, AUDIT_SCHEMA)
    if value["status"] != "PASS":
        raise ValueError("audit status is not PASS")
    if value["manifest_sha256"] != payload_sha256(manifest):
        raise ValueError("audit manifest hash drift")
    if not all(value["checks"].values()) or not all(
        value["mutation_regressions"].values()
    ):
        raise ValueError("audit has a failed check")
    if value["claim_boundary"] != manifest["claim_boundary"]:
        raise ValueError("audit claim boundary drift")


def write_or_check(path: Path, value: Any, check: bool) -> None:
    expected = canonical_json(value)
    if check:
        if normalize_lf(path.read_text(encoding="utf-8")) != expected:
            raise ValueError(f"generated artifact drift: {path}")
    else:
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(expected, encoding="utf-8", newline="\n")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()
    manifest = build()
    validate_manifest(manifest)
    audit = build_audit(manifest)
    validate_audit(audit, manifest)
    write_or_check(MANIFEST, manifest, args.check)
    write_or_check(AUDIT, audit, args.check)
    print(
        "PASS: TPC-171 source-locked integration; "
        f"verdict={manifest['current_verdict']}; "
        f"first_missing={manifest['first_missing']['node_id']}"
    )


if __name__ == "__main__":
    main()
