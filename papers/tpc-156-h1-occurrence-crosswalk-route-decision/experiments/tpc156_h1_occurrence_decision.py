#!/usr/bin/env python3
"""Build and verify the source-locked TPC-156 H1 route decision."""

from __future__ import annotations

import argparse
import copy
import hashlib
import json
import subprocess
import sys
from pathlib import Path
from typing import Any, Iterable


HERE = Path(__file__).resolve().parent
PAPER_DIR = HERE.parent
PAPERS_DIR = PAPER_DIR.parent
REPO_DIR = PAPERS_DIR.parent

TPC152 = PAPERS_DIR / "tpc-152-mvp5-frontier-occurrence-lift-route-decision"
TPC153 = PAPERS_DIR / "tpc-153-canonical-cut-occurrence-shadow"
TPC154 = PAPERS_DIR / "tpc-154-conservative-completion-fiber-obstruction"
TPC155 = PAPERS_DIR / "tpc-155-theorem-backed-occurrence-witness-verifier"

TPC152_SCRIPT = TPC152 / "experiments" / "tpc152_mvp5_route_audit.py"
TPC152_SNAPSHOT = TPC152 / "experiments" / "tpc152_mvp5_snapshot.json"
TPC153_SCRIPT = TPC153 / "experiments" / "tpc153_cut_occurrence_shadow.py"
TPC153_CERT = (
    TPC153 / "experiments" / "tpc153_cut_occurrence_shadow_certificate.json"
)
TPC153_SHADOW = TPC153 / "samples" / "tpc153_cut_occurrence_shadow.jsonl"
TPC154_SCRIPT = (
    TPC154 / "experiments" / "tpc154_completion_fiber_obstruction.py"
)
TPC154_CERT = (
    TPC154
    / "experiments"
    / "tpc154_completion_fiber_obstruction_certificate.json"
)
TPC154_COMPLETIONS = (
    TPC154 / "samples" / "tpc154_formal_completions.jsonl"
)
TPC155_SCRIPT = (
    TPC155 / "experiments" / "tpc155_occurrence_witness_verifier.py"
)
TPC155_AUDIT = (
    TPC155 / "experiments" / "tpc155_occurrence_witness_audit.json"
)
TPC155_PRODUCTION = (
    TPC155 / "samples" / "tpc155_production_witness_status.json"
)

SCHEMA_PATH = HERE / "tpc156_h1_occurrence_decision.schema.json"
DECISION_PATH = HERE / "tpc156_h1_occurrence_decision.json"
AUDIT_PATH = HERE / "tpc156_h1_occurrence_audit.json"

LOCK_MODE = "CANONICAL_UTF8_LF_V2"
HASH_SEMANTICS = "INTEGRITY_ONLY"
SCHEMA_ID = "tpc-156-h1-occurrence-crosswalk-decision-v1"
FIRST_MISSING = "H1.theorem_backed_occurrence_provenance_crosswalk"

TERMINAL_TYPES = ["ELIGIBLE_TAIL_OPEN", "FRONTIER_UNMAPPED"]
DEFECT_IDS = [
    "D_L",
    "D_QD",
    "D_QZ",
    "D_G",
    "D_P",
    "D_DZ",
    "D_GP",
    "D_cover",
    "D_rec",
    "D_occ",
]
MAP_COMPONENTS = [
    FIRST_MISSING,
    "H1.defect.D_L",
    "H1.defect.D_QD",
    "H1.defect.D_QZ",
    "H1.defect.D_G",
    "H1.defect.D_P",
    "H1.defect.D_DZ",
    "H1.defect.D_GP",
    "H1.defect.D_cover",
    "H1.defect.D_rec",
    "H1.frontier_occurrence_registry_totality",
]
SCALAR_COMPONENTS = [
    "H1.complete_FUM_scalar_oX",
    "H1.theorem_backed_ETO_disposition",
]
REQUIRED_ARTIFACT = (
    "for every ELIGIBLE_TAIL_OPEN and FRONTIER_UNMAPPED cut path, "
    "a nonempty conservative row-separated one-to-many edge family "
    "with exact occurrence, canonical-parent, stage, multiplier, "
    "native, h0, physical-normalization, support-status, QD, QZ, G, "
    "P_h0, cover, reconnection, occurrence-registry, and trusted "
    "theorem-source lineage"
)


def normalize_lf(text: str) -> str:
    return text.replace("\r\n", "\n").replace("\r", "\n")


def canonical_json(payload: Any) -> str:
    return json.dumps(
        payload,
        ensure_ascii=False,
        indent=2,
        sort_keys=True,
    ) + "\n"


def sha256_text(text: str) -> str:
    return hashlib.sha256(normalize_lf(text).encode("utf-8")).hexdigest()


def load_json(path: Path) -> dict[str, Any]:
    if not path.is_file():
        raise FileNotFoundError(f"missing source artifact: {path}")
    value = json.loads(normalize_lf(path.read_text(encoding="utf-8")))
    if not isinstance(value, dict):
        raise ValueError(f"source artifact is not an object: {path}")
    return value


def relative_path(path: Path) -> str:
    return path.resolve().relative_to(REPO_DIR.resolve()).as_posix()


def source_lock(source_id: str, path: Path) -> dict[str, str]:
    if not path.is_file():
        raise FileNotFoundError(f"missing allowlisted logical source: {path}")
    text = path.read_text(encoding="utf-8")
    return {
        "source_id": source_id,
        "path": relative_path(path),
        "canonical_utf8_lf_sha256": sha256_text(text),
    }


def run_source_check(script: Path) -> None:
    if not script.is_file():
        raise FileNotFoundError(f"missing source audit script: {script}")
    result = subprocess.run(
        [sys.executable, str(script), "--check"],
        cwd=script.parent.parent,
        check=False,
        capture_output=True,
    )
    if result.returncode:
        detail = normalize_lf(
            (result.stderr or result.stdout).decode("utf-8", errors="replace")
        ).strip()
        raise ValueError(
            f"source audit failed for {script.name}: {detail[:1000]}"
        )


def run_all_source_checks() -> None:
    for script in (
        TPC152_SCRIPT,
        TPC153_SCRIPT,
        TPC154_SCRIPT,
        TPC155_SCRIPT,
    ):
        run_source_check(script)


def recursive_values(payload: Any, key: str) -> list[Any]:
    found: list[Any] = []
    if isinstance(payload, dict):
        for current_key, value in payload.items():
            if current_key == key:
                found.append(value)
            found.extend(recursive_values(value, key))
    elif isinstance(payload, list):
        for value in payload:
            found.extend(recursive_values(value, key))
    return found


def unique_recursive_value(payload: Any, key: str) -> Any:
    values = recursive_values(payload, key)
    if not values:
        raise ValueError(f"missing source field: {key}")
    first = values[0]
    if any(value != first for value in values[1:]):
        raise ValueError(f"ambiguous source field: {key}")
    return first


def load_sources() -> dict[str, dict[str, Any]]:
    return {
        "tpc152": load_json(TPC152_SNAPSHOT),
        "tpc153": load_json(TPC153_CERT),
        "tpc154": load_json(TPC154_CERT),
        "tpc155_audit": load_json(TPC155_AUDIT),
        "tpc155_production": load_json(TPC155_PRODUCTION),
    }


def validate_source_semantics(sources: dict[str, dict[str, Any]]) -> None:
    tpc152 = sources["tpc152"]
    if tpc152.get("current_verdict") != "NOT_TESTABLE":
        raise ValueError("TPC-152 source verdict drifted")
    first152 = tpc152.get("first_missing")
    if not isinstance(first152, dict) or first152.get(
        "node_id"
    ) != "H1.frontier_occurrence_lift":
        raise ValueError("TPC-152 first-missing pointer drifted")

    tpc153 = sources["tpc153"]
    if tpc153.get("status") != "PASS":
        raise ValueError("TPC-153 certificate did not pass")
    exports153 = tpc153.get("theorem_exports", {})
    if exports153.get("H1.cut_occurrence_shadow") != (
        "PROVED_L1_STRUCTURAL"
    ):
        raise ValueError("TPC-153 shadow theorem is unavailable")
    if exports153.get("H1.frontier_occurrence_lift") != "NOT_TESTABLE":
        raise ValueError("TPC-153 actual-lift boundary drifted")
    if exports153.get(
        "current_schema_only_actual_lift_derivation"
    ) != "STOP_DECLARED_ROUTE":
        raise ValueError("TPC-153 scoped stop is unavailable")
    census = tpc153.get("census", {})
    counts = census.get("production_terminal_type_counts", {})
    if counts != {
        "ELIGIBLE_TAIL_OPEN": 0,
        "FRONTIER_UNMAPPED": 2988,
    }:
        raise ValueError("TPC-153 production census drifted")
    if census.get("synthetic_ETO_in_production_census") is not False:
        raise ValueError("synthetic ETO entered the production census")
    if tpc153.get("claim_boundary", {}).get(
        "shadow_is_actual_occurrence_lift"
    ) is not False:
        raise ValueError("TPC-153 shadow was promoted to an actual lift")

    tpc154 = sources["tpc154"]
    if tpc154.get("status") != "PASS":
        raise ValueError("TPC-154 certificate did not pass")
    exports154 = tpc154.get("theorem_exports", {})
    expected154 = {
        "H1.formal_completion_fiber_nonuniqueness":
            "PROVED_L0_SCHEMA",
        "H1.current_artifacts_only_canonical_actual_lift":
            "STOP_DECLARED_ROUTE",
        "H1.augmented_actual_occurrence_lift": "NOT_TESTABLE",
    }
    for key, expected in expected154.items():
        if exports154.get(key) != expected:
            raise ValueError(f"TPC-154 export drifted: {key}")
    if exports154.get("selected_augmented_route_stopped") is not False:
        raise ValueError("TPC-154 incorrectly stopped the augmented route")

    audit155 = sources["tpc155_audit"]
    if audit155.get("status") != "PASS":
        raise ValueError("TPC-155 audit did not pass")
    production155 = sources["tpc155_production"]
    witness_present = unique_recursive_value(
        production155, "production_witness_present"
    )
    witness_status = unique_recursive_value(
        production155, "current_production_actual_witness_status"
    )
    if witness_present is not False or witness_status != "NOT_TESTABLE":
        raise ValueError("TPC-155 production witness boundary drifted")
    if unique_recursive_value(
        production155, "partial_shadow_status"
    ) != "PROVED_L1_STRUCTURAL":
        raise ValueError("TPC-155 imported shadow status drifted")
    first155 = production155.get("first_missing")
    if not isinstance(first155, dict) or first155.get(
        "node_id"
    ) != FIRST_MISSING:
        raise ValueError("TPC-155 first-missing pointer drifted")
    for field in (
        "occurrence_lift_candidate_status",
        "QD_status",
        "QZ_status",
        "G_status",
        "P_h0_status",
        "physical_cover_status",
        "reconnection_status",
        "occurrence_registry_status",
    ):
        if unique_recursive_value(production155, field) != "NOT_TESTABLE":
            raise ValueError(f"TPC-155 production status drifted: {field}")


def build_source_locks() -> list[dict[str, str]]:
    specs = [
        ("TPC152.audit_script", TPC152_SCRIPT),
        ("TPC152.snapshot", TPC152_SNAPSHOT),
        ("TPC153.audit_script", TPC153_SCRIPT),
        ("TPC153.shadow_certificate", TPC153_CERT),
        ("TPC153.production_shadow", TPC153_SHADOW),
        ("TPC154.audit_script", TPC154_SCRIPT),
        ("TPC154.obstruction_certificate", TPC154_CERT),
        ("TPC154.formal_completions", TPC154_COMPLETIONS),
        ("TPC155.audit_script", TPC155_SCRIPT),
        ("TPC155.witness_audit", TPC155_AUDIT),
        ("TPC155.production_status", TPC155_PRODUCTION),
    ]
    return [source_lock(source_id, path) for source_id, path in specs]


def imported_evidence(
    sources: dict[str, dict[str, Any]]
) -> dict[str, Any]:
    tpc153 = sources["tpc153"]
    tpc154 = sources["tpc154"]
    production155 = sources["tpc155_production"]
    return {
        "tpc152": {
            "current_verdict": sources["tpc152"]["current_verdict"],
            "first_missing": sources["tpc152"]["first_missing"]["node_id"],
        },
        "tpc153": {
            "status": tpc153["status"],
            "theorem_exports": tpc153["theorem_exports"],
            "production_terminal_type_counts": (
                tpc153["census"]["production_terminal_type_counts"]
            ),
            "synthetic_ETO_is_L0_only": True,
        },
        "tpc154": {
            "status": tpc154["status"],
            "theorem_exports": tpc154["theorem_exports"],
            "obstruction_scope": "CURRENT_ARTIFACTS_ONLY",
            "actual_carrier_impossibility_proved": False,
        },
        "tpc155": {
            "audit_status": sources["tpc155_audit"]["status"],
            "production_witness_present": unique_recursive_value(
                production155, "production_witness_present"
            ),
            "current_production_actual_witness_status": (
                unique_recursive_value(
                    production155,
                    "current_production_actual_witness_status",
                )
            ),
            "partial_shadow_status": unique_recursive_value(
                production155, "partial_shadow_status"
            ),
            "first_missing": production155["first_missing"]["node_id"],
            "occurrence_lift_candidate_status": unique_recursive_value(
                production155, "occurrence_lift_candidate_status"
            ),
            "QD_status": unique_recursive_value(production155, "QD_status"),
            "QZ_status": unique_recursive_value(production155, "QZ_status"),
            "G_status": unique_recursive_value(production155, "G_status"),
            "P_h0_status": unique_recursive_value(
                production155, "P_h0_status"
            ),
            "physical_cover_status": unique_recursive_value(
                production155, "physical_cover_status"
            ),
            "reconnection_status": unique_recursive_value(
                production155, "reconnection_status"
            ),
            "occurrence_registry_status": unique_recursive_value(
                production155, "occurrence_registry_status"
            ),
            "cover_reconnection_registry_are_separate": True,
            "synthetic_witness_is_production_evidence": False,
        },
    }


def node(
    status: str,
    level: str,
    *,
    parents: Iterable[str] = (),
    dependency_mode: str = "ALL",
    parent_clauses: list[list[str]] | None = None,
    evidence: str,
) -> dict[str, Any]:
    record: dict[str, Any] = {
        "status": status,
        "program_level": level,
        "dependency_mode": dependency_mode,
        "evidence": evidence,
    }
    if dependency_mode == "ANY_CLAUSE":
        if parent_clauses is None:
            raise ValueError("ANY_CLAUSE node requires parent clauses")
        record["parent_clauses"] = parent_clauses
    else:
        record["parents"] = list(parents)
    return record


def build_nodes() -> dict[str, dict[str, Any]]:
    nodes: dict[str, dict[str, Any]] = {
        "H1.cut_occurrence_shadow": node(
            "PROVED",
            "L1_STRUCTURAL",
            evidence="TPC-153 canonical conservative shadow",
        ),
        "H1.current_artifacts_only_canonical_actual_lift": node(
            "STOPPED",
            "L0_SCHEMA",
            evidence=(
                "TPC-154 conservative formal-completion nonuniqueness; "
                "current-artifacts-only scope"
            ),
        ),
        FIRST_MISSING: node(
            "NOT_TESTABLE",
            "L1_STRUCTURAL_TARGET",
            parents=["H1.cut_occurrence_shadow"],
            evidence="TPC-155 reports no theorem-backed production witness",
        ),
        "H1.frontier_occurrence_lift": node(
            "NOT_TESTABLE",
            "L1_STRUCTURAL_TARGET",
            parents=[FIRST_MISSING],
            evidence="actual row-separated conservative matrix unavailable",
        ),
        "H1.frontier_QD_totality": node(
            "NOT_TESTABLE",
            "L1_STRUCTURAL_TARGET",
            parents=["H1.frontier_occurrence_lift"],
            evidence="literal determinant-fiber map unavailable",
        ),
        "H1.frontier_QZ_totality": node(
            "NOT_TESTABLE",
            "L1_STRUCTURAL_TARGET",
            parents=["H1.frontier_occurrence_lift"],
            evidence="literal ordered zero-mode map unavailable",
        ),
        "H1.frontier_G_totality": node(
            "NOT_TESTABLE",
            "L1_STRUCTURAL_TARGET",
            parents=["H1.frontier_occurrence_lift"],
            evidence="literal physical grouping map unavailable",
        ),
        "H1.frontier_P_h0_totality": node(
            "NOT_TESTABLE",
            "L1_STRUCTURAL_TARGET",
            parents=["H1.frontier_occurrence_lift"],
            evidence="downstream prescribed-shift selector unavailable",
        ),
        "H1.frontier_cover_totality": node(
            "NOT_TESTABLE",
            "L1_STRUCTURAL_TARGET",
            parents=["H1.frontier_occurrence_lift"],
            evidence="production physical cover unavailable",
        ),
        "H1.frontier_reconnection": node(
            "NOT_TESTABLE",
            "L1_STRUCTURAL_TARGET",
            parents=[
                "H1.frontier_occurrence_lift",
                "H1.frontier_cover_totality",
            ],
            evidence="production reconnection unavailable",
        ),
        "H1.frontier_occurrence_registry_totality": node(
            "NOT_TESTABLE",
            "L1_STRUCTURAL_TARGET",
            parents=[
                "H1.frontier_occurrence_lift",
                "H1.frontier_cover_totality",
                "H1.frontier_reconnection",
            ],
            evidence="production row-level occurrence registry unavailable",
        ),
        "H1.complete_FUM_scalar_oX": node(
            "NOT_TESTABLE",
            "L1_ANALYTIC_TARGET",
            evidence="no complete original-scale FUM o(X) theorem",
        ),
        "H1.theorem_backed_ETO_disposition": node(
            "NOT_TESTABLE",
            "L1_STRUCTURAL_OR_ANALYTIC_TARGET",
            evidence=(
                "finite empty ETO census is not a growing-scale "
                "disposition theorem"
            ),
        ),
    }

    defect_parents = {
        "D_L": ["H1.frontier_occurrence_lift"],
        "D_QD": ["H1.frontier_QD_totality"],
        "D_QZ": ["H1.frontier_QZ_totality"],
        "D_G": ["H1.frontier_G_totality"],
        "D_P": ["H1.frontier_P_h0_totality"],
        "D_DZ": [
            "H1.frontier_QD_totality",
            "H1.frontier_QZ_totality",
        ],
        "D_GP": [
            "H1.frontier_G_totality",
            "H1.frontier_P_h0_totality",
        ],
        "D_cover": ["H1.frontier_cover_totality"],
        "D_rec": ["H1.frontier_reconnection"],
    }
    for defect_id, parents in defect_parents.items():
        nodes[f"H1.defect.{defect_id}"] = node(
            "NOT_TESTABLE",
            "L1_STRUCTURAL_TARGET",
            parents=parents,
            evidence=f"{defect_id} is not evaluable on production data",
        )

    nodes["H1.map_clause"] = node(
        "NOT_TESTABLE",
        "L1_STRUCTURAL_TARGET",
        parents=MAP_COMPONENTS,
        evidence="trusted crosswalk and map-route completion unavailable",
    )
    nodes["H1.scalar_clause"] = node(
        "NOT_TESTABLE",
        "L1_ANALYTIC_TARGET",
        parents=SCALAR_COMPONENTS,
        evidence="both scalar-plus-ETO factors are unavailable",
    )
    nodes["H1.frontier_totalization"] = node(
        "NOT_TESTABLE",
        "L1_TARGET",
        dependency_mode="ANY_CLAUSE",
        parent_clauses=[
            ["H1.map_clause"],
            ["H1.scalar_clause"],
        ],
        evidence="neither declared sufficient clause is proved",
    )
    return nodes


def direct_parents(record: dict[str, Any]) -> list[str]:
    mode = record["dependency_mode"]
    if mode == "ANY_CLAUSE":
        return [
            parent
            for clause in record["parent_clauses"]
            for parent in clause
        ]
    if mode == "ALL":
        return list(record["parents"])
    raise ValueError(f"unknown dependency mode: {mode}")


def validate_dag(nodes: dict[str, dict[str, Any]]) -> None:
    allowed_statuses = {"PROVED", "STOPPED", "NOT_TESTABLE", "OPEN"}
    for node_id, record in nodes.items():
        if record["status"] not in allowed_statuses:
            raise ValueError(f"unknown node status: {node_id}")
        for parent in direct_parents(record):
            if parent not in nodes:
                raise ValueError(f"missing parent {parent} for {node_id}")

    visiting: set[str] = set()
    visited: set[str] = set()

    def visit(node_id: str) -> None:
        if node_id in visiting:
            raise ValueError("cycle in typed H1 DAG")
        if node_id in visited:
            return
        visiting.add(node_id)
        for parent in direct_parents(nodes[node_id]):
            visit(parent)
        visiting.remove(node_id)
        visited.add(node_id)

    for node_id in nodes:
        visit(node_id)


def ancestor_closure(
    nodes: dict[str, dict[str, Any]], root: str
) -> set[str]:
    closure: set[str] = set()

    def add(node_id: str) -> None:
        if node_id in closure:
            return
        closure.add(node_id)
        for parent in direct_parents(nodes[node_id]):
            add(parent)

    add(root)
    return closure


def missing_ancestors(
    nodes: dict[str, dict[str, Any]], node_id: str
) -> set[str]:
    result: set[str] = set()
    stack = list(direct_parents(nodes[node_id]))
    while stack:
        current = stack.pop()
        if current in result:
            continue
        if nodes[current]["status"] == "NOT_TESTABLE":
            result.add(current)
        stack.extend(direct_parents(nodes[current]))
    return result


def minimal_missing(
    nodes: dict[str, dict[str, Any]], root: str
) -> list[str]:
    closure = ancestor_closure(nodes, root)
    missing = {
        node_id
        for node_id in closure
        if nodes[node_id]["status"] == "NOT_TESTABLE"
    }
    minimal = [
        node_id
        for node_id in missing
        if not (missing_ancestors(nodes, node_id) & missing)
    ]
    return sorted(minimal)


def build_decision(
    sources: dict[str, dict[str, Any]]
) -> dict[str, Any]:
    counts = sources["tpc153"]["census"][
        "production_terminal_type_counts"
    ]
    nodes = build_nodes()
    validate_dag(nodes)
    map_minimal = minimal_missing(nodes, "H1.map_clause")
    scalar_minimal = minimal_missing(nodes, "H1.scalar_clause")
    if map_minimal != [FIRST_MISSING]:
        raise ValueError("unexpected selected-map minimal antichain")
    if scalar_minimal != sorted(SCALAR_COMPONENTS):
        raise ValueError("unexpected scalar-route minimal antichain")
    return {
        "schema": SCHEMA_ID,
        "source_lock_policy": {
            "normalization": LOCK_MODE,
            "hash_semantics": HASH_SEMANTICS,
        },
        "source_locks": build_source_locks(),
        "imported_evidence": imported_evidence(sources),
        "production_census": {
            "ELIGIBLE_TAIL_OPEN": counts["ELIGIBLE_TAIL_OPEN"],
            "FRONTIER_UNMAPPED": counts["FRONTIER_UNMAPPED"],
            "nonsoft_total": sum(counts.values()),
        },
        "nodes": nodes,
        "defects": {defect_id: "NOT_EVALUABLE" for defect_id in DEFECT_IDS},
        "h1_contract": {
            "nonsoft_domain": {
                "operator": "DISJOINT_UNION",
                "terminal_types": TERMINAL_TYPES,
            },
            "map_clause": {
                "operator": "ALL",
                "components": MAP_COMPONENTS,
            },
            "scalar_clause": {
                "operator": "ALL",
                "components": SCALAR_COMPONENTS,
            },
            "frontier_totalization": {
                "operator": "ANY_CLAUSE",
                "clauses": ["H1.map_clause", "H1.scalar_clause"],
            },
            "cover_reconnection_registry_are_independent": True,
            "required_artifact": REQUIRED_ARTIFACT,
        },
        "minimal_missing_antichains": {
            "selected_occurrence_augmented_map_route": map_minimal,
            "scalar_plus_ETO_route": scalar_minimal,
            "canonical_selected_representative": FIRST_MISSING,
            "selection_rule": (
                "selected clause; then minimal missing ancestor; "
                "then canonical node identifier"
            ),
        },
        "routes": {
            "selected_route": "occurrence_augmented_map",
            "current_archive_only_actual_lift": {
                "state": "STOP_DECLARED_ROUTE",
                "stopped": True,
                "scope": "CURRENT_ARTIFACTS_ONLY",
                "source": "TPC-154",
            },
            "occurrence_augmented_map": {
                "state": "OPEN_NOT_TESTABLE",
                "stopped": False,
                "first_missing": FIRST_MISSING,
            },
            "scalar_plus_ETO": {
                "state": "OPEN_NOT_TESTABLE",
                "stopped": False,
                "missing": sorted(SCALAR_COMPONENTS),
            },
            "route_universe_completeness": {
                "status": "NOT_PROVED",
                "source_theorem": None,
            },
            "architecture_infeasible": False,
        },
        "first_missing_selected_route": FIRST_MISSING,
        "current_verdict": "NOT_TESTABLE",
        "claim_boundary": {
            "production_actual_lift_claimed": False,
            "fixed_X_power_L2_claimed": False,
            "one_over_400_endpoint_claimed": False,
            "prime_pair_or_twin_prime_claimed": False,
            "architecture_infeasible_claimed": False,
        },
    }


def validate_decision(
    decision: dict[str, Any],
    sources: dict[str, dict[str, Any]],
) -> None:
    if decision.get("schema") != SCHEMA_ID:
        raise ValueError("decision schema drifted")
    if decision.get("source_lock_policy") != {
        "normalization": LOCK_MODE,
        "hash_semantics": HASH_SEMANTICS,
    }:
        raise ValueError("source-lock policy drifted")
    if decision.get("source_locks") != build_source_locks():
        raise ValueError("source locks drifted")
    if decision.get("imported_evidence") != imported_evidence(sources):
        raise ValueError("imported evidence drifted")

    census = decision.get("production_census", {})
    if census != {
        "ELIGIBLE_TAIL_OPEN": 0,
        "FRONTIER_UNMAPPED": 2988,
        "nonsoft_total": 2988,
    }:
        raise ValueError("production census drifted")

    nodes = decision.get("nodes")
    if not isinstance(nodes, dict):
        raise ValueError("typed nodes are missing")
    validate_dag(nodes)
    expected_nodes = build_nodes()
    if nodes != expected_nodes:
        raise ValueError("typed H1 node graph drifted")

    expected_defects = {
        defect_id: "NOT_EVALUABLE" for defect_id in DEFECT_IDS
    }
    if decision.get("defects") != expected_defects:
        raise ValueError("production defect vector was promoted")

    contract = decision.get("h1_contract", {})
    if contract.get("nonsoft_domain") != {
        "operator": "DISJOINT_UNION",
        "terminal_types": TERMINAL_TYPES,
    }:
        raise ValueError("ETO/FUM nonsoft domain was compressed")
    if contract.get("map_clause") != {
        "operator": "ALL",
        "components": MAP_COMPONENTS,
    }:
        raise ValueError("map clause is incomplete or compressed")
    if contract.get("scalar_clause") != {
        "operator": "ALL",
        "components": SCALAR_COMPONENTS,
    }:
        raise ValueError("scalar-plus-ETO clause is incomplete")
    if contract.get("frontier_totalization") != {
        "operator": "ANY_CLAUSE",
        "clauses": ["H1.map_clause", "H1.scalar_clause"],
    }:
        raise ValueError("H1 alternative operator drifted")
    if contract.get(
        "cover_reconnection_registry_are_independent"
    ) is not True:
        raise ValueError("cover/reconnection/registry were compressed")
    if contract.get("required_artifact") != REQUIRED_ARTIFACT:
        raise ValueError("required crosswalk artifact drifted")

    expected_minimal = {
        "selected_occurrence_augmented_map_route": [FIRST_MISSING],
        "scalar_plus_ETO_route": sorted(SCALAR_COMPONENTS),
        "canonical_selected_representative": FIRST_MISSING,
        "selection_rule": (
            "selected clause; then minimal missing ancestor; "
            "then canonical node identifier"
        ),
    }
    if decision.get("minimal_missing_antichains") != expected_minimal:
        raise ValueError("minimal missing antichains drifted")
    if minimal_missing(nodes, "H1.map_clause") != [FIRST_MISSING]:
        raise ValueError("selected-map minimal missing node drifted")
    if minimal_missing(nodes, "H1.scalar_clause") != sorted(
        SCALAR_COMPONENTS
    ):
        raise ValueError("scalar-route minimal antichain drifted")

    routes = decision.get("routes", {})
    if routes.get("selected_route") != "occurrence_augmented_map":
        raise ValueError("selected route drifted")
    if routes.get("current_archive_only_actual_lift") != {
        "state": "STOP_DECLARED_ROUTE",
        "stopped": True,
        "scope": "CURRENT_ARTIFACTS_ONLY",
        "source": "TPC-154",
    }:
        raise ValueError("scoped current-archive stop drifted")
    if routes.get("occurrence_augmented_map", {}).get("stopped") is not False:
        raise ValueError("augmented occurrence route was falsely stopped")
    if routes.get("scalar_plus_ETO", {}).get("stopped") is not False:
        raise ValueError("scalar-plus-ETO route was falsely stopped")
    universe = routes.get("route_universe_completeness", {})
    if universe != {"status": "NOT_PROVED", "source_theorem": None}:
        raise ValueError("route-universe completeness was fabricated")
    if routes.get("architecture_infeasible") is not False:
        raise ValueError("architecture infeasibility was fabricated")

    if decision.get("first_missing_selected_route") != FIRST_MISSING:
        raise ValueError("first-missing pointer drifted")
    if decision.get("current_verdict") != "NOT_TESTABLE":
        raise ValueError("production verdict drifted")
    boundary = decision.get("claim_boundary", {})
    if set(boundary) != {
        "production_actual_lift_claimed",
        "fixed_X_power_L2_claimed",
        "one_over_400_endpoint_claimed",
        "prime_pair_or_twin_prime_claimed",
        "architecture_infeasible_claimed",
    } or any(boundary.values()):
        raise ValueError("claim boundary was promoted")


def evaluate_h1_scenario(
    *,
    trusted_crosswalk: bool = False,
    zero_defects: Iterable[str] = (),
    registry_complete: bool = False,
    complete_fum_scalar: bool = False,
    eto_disposition: bool = False,
) -> dict[str, Any]:
    zero = set(zero_defects)
    map_pass = (
        trusted_crosswalk
        and set(DEFECT_IDS[:-1]).issubset(zero)
        and registry_complete
        and "D_occ" in zero
    )
    scalar_pass = complete_fum_scalar and eto_disposition
    return {
        "map_clause": "PROVED" if map_pass else "NOT_TESTABLE",
        "scalar_clause": "PROVED" if scalar_pass else "NOT_TESTABLE",
        "H1": "PROVED" if (map_pass or scalar_pass) else "NOT_TESTABLE",
    }


def mutation_rejected(
    decision: dict[str, Any],
    sources: dict[str, dict[str, Any]],
    mutate: Any,
) -> bool:
    candidate = copy.deepcopy(decision)
    mutate(candidate)
    try:
        validate_decision(candidate, sources)
    except (KeyError, TypeError, ValueError):
        return True
    return False


def scenario_regressions() -> dict[str, Any]:
    all_zero = set(DEFECT_IDS)
    baseline = evaluate_h1_scenario()
    map_complete = evaluate_h1_scenario(
        trusted_crosswalk=True,
        zero_defects=all_zero,
        registry_complete=True,
    )
    missing_cover = evaluate_h1_scenario(
        trusted_crosswalk=True,
        zero_defects=all_zero - {"D_cover"},
        registry_complete=True,
    )
    missing_reconnection = evaluate_h1_scenario(
        trusted_crosswalk=True,
        zero_defects=all_zero - {"D_rec"},
        registry_complete=True,
    )
    missing_registry = evaluate_h1_scenario(
        trusted_crosswalk=True,
        zero_defects=all_zero - {"D_occ"},
        registry_complete=False,
    )
    scalar_only = evaluate_h1_scenario(complete_fum_scalar=True)
    eto_only = evaluate_h1_scenario(eto_disposition=True)
    scalar_complete = evaluate_h1_scenario(
        complete_fum_scalar=True,
        eto_disposition=True,
    )
    return {
        "baseline_not_testable": baseline["H1"] == "NOT_TESTABLE",
        "complete_map_clause_closes_H1": map_complete["H1"] == "PROVED",
        "cover_is_independent_and_required": (
            missing_cover["H1"] == "NOT_TESTABLE"
        ),
        "reconnection_is_independent_and_required": (
            missing_reconnection["H1"] == "NOT_TESTABLE"
        ),
        "registry_is_independent_and_required": (
            missing_registry["H1"] == "NOT_TESTABLE"
        ),
        "FUM_scalar_without_ETO_rejected": (
            scalar_only["H1"] == "NOT_TESTABLE"
        ),
        "ETO_without_FUM_scalar_rejected": (
            eto_only["H1"] == "NOT_TESTABLE"
        ),
        "complete_scalar_plus_ETO_closes_H1": (
            scalar_complete["H1"] == "PROVED"
        ),
        "hypothetical_outcomes": {
            "baseline": baseline,
            "complete_map": map_complete,
            "complete_scalar_plus_ETO": scalar_complete,
        },
    }


def build_audit(
    decision: dict[str, Any],
    decision_rendered: str,
    sources: dict[str, dict[str, Any]],
) -> dict[str, Any]:
    validate_decision(decision, sources)
    scenarios = scenario_regressions()
    scenario_checks = {
        key: value
        for key, value in scenarios.items()
        if key != "hypothetical_outcomes"
    }
    mutations = {
        "identity_shadow_actual_lift_promotion_rejected": mutation_rejected(
            decision,
            sources,
            lambda value: value["nodes"][
                "H1.frontier_occurrence_lift"
            ].update({"status": "PROVED"}),
        ),
        "ETO_domain_omission_rejected": mutation_rejected(
            decision,
            sources,
            lambda value: value["h1_contract"]["nonsoft_domain"].update(
                {"terminal_types": ["FRONTIER_UNMAPPED"]}
            ),
        ),
        "compressed_four_map_claim_rejected": mutation_rejected(
            decision,
            sources,
            lambda value: value["h1_contract"]["map_clause"].update(
                {
                    "components": [
                        FIRST_MISSING,
                        "H1.defect.D_QD",
                        "H1.defect.D_QZ",
                        "H1.defect.D_G",
                        "H1.defect.D_P",
                    ]
                }
            ),
        ),
        "cover_registry_compression_rejected": mutation_rejected(
            decision,
            sources,
            lambda value: value["h1_contract"].update(
                {"cover_reconnection_registry_are_independent": False}
            ),
        ),
        "finite_empty_ETO_disposition_rejected": mutation_rejected(
            decision,
            sources,
            lambda value: value["nodes"][
                "H1.theorem_backed_ETO_disposition"
            ].update({"status": "PROVED"}),
        ),
        "scalar_only_pass_rejected": mutation_rejected(
            decision,
            sources,
            lambda value: value["nodes"]["H1.scalar_clause"].update(
                {"status": "PROVED"}
            ),
        ),
        "architecture_infeasible_without_universe_rejected":
            mutation_rejected(
                decision,
                sources,
                lambda value: value["routes"].update(
                    {"architecture_infeasible": True}
                ),
            ),
        "actual_lift_claim_rejected": mutation_rejected(
            decision,
            sources,
            lambda value: value["claim_boundary"].update(
                {"production_actual_lift_claimed": True}
            ),
        ),
        "positive_L2_claim_rejected": mutation_rejected(
            decision,
            sources,
            lambda value: value["claim_boundary"].update(
                {"fixed_X_power_L2_claimed": True}
            ),
        ),
    }
    checks = {
        "source_checks_passed": True,
        "source_semantics_validated": True,
        "canonical_source_locks_valid": True,
        "typed_DAG_acyclic": True,
        "ETO_and_FUM_both_in_contract": True,
        "production_census_exact": True,
        "selected_minimal_missing_exact": True,
        "scalar_antichain_exact": True,
        "nine_defects_and_registry_separate": True,
        "current_schema_stop_scoped": True,
        "augmented_and_scalar_routes_remain_open": True,
        "claim_boundary_intact": True,
    }
    passed = (
        all(checks.values())
        and all(scenario_checks.values())
        and all(mutations.values())
    )
    return {
        "schema": "tpc-156-h1-occurrence-crosswalk-audit-v1",
        "status": "PASS" if passed else "FAIL",
        "decision_sha256": sha256_text(decision_rendered),
        "checks": checks,
        "scenario_checks": scenario_checks,
        "hypothetical_outcomes": scenarios["hypothetical_outcomes"],
        "mutation_regression": mutations,
        "current_verdict": decision["current_verdict"],
        "first_missing_selected_route": (
            decision["first_missing_selected_route"]
        ),
        "claim_boundary": decision["claim_boundary"],
    }


def write_canonical(path: Path, rendered: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="\n") as stream:
        stream.write(rendered)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--check",
        action="store_true",
        help="verify committed deterministic artifacts without writing",
    )
    args = parser.parse_args()

    run_all_source_checks()
    sources = load_sources()
    validate_source_semantics(sources)
    decision = build_decision(sources)
    decision_rendered = canonical_json(decision)
    audit = build_audit(decision, decision_rendered, sources)
    audit_rendered = canonical_json(audit)

    if args.check:
        for path, expected in (
            (DECISION_PATH, decision_rendered),
            (AUDIT_PATH, audit_rendered),
        ):
            if not path.is_file():
                raise SystemExit(f"missing deterministic artifact: {path.name}")
            current = normalize_lf(path.read_text(encoding="utf-8"))
            if current != expected:
                raise SystemExit(f"artifact mismatch: {path.name}")
    else:
        write_canonical(DECISION_PATH, decision_rendered)
        write_canonical(AUDIT_PATH, audit_rendered)

    print(audit_rendered, end="")
    if audit["status"] != "PASS":
        raise SystemExit(1)


if __name__ == "__main__":
    main()
