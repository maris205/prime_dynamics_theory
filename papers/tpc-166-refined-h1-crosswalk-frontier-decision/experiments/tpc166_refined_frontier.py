#!/usr/bin/env python3
"""Build the refined three-root H1 crosswalk frontier decision."""

from __future__ import annotations

import argparse
import copy
import hashlib
import json
from pathlib import Path
from typing import Any


HERE = Path(__file__).resolve().parent
PAPER = HERE.parent
PAPERS = PAPER.parent
REPO = PAPERS.parent

TPC156 = PAPERS / "tpc-156-h1-occurrence-crosswalk-route-decision"
TPC162 = PAPERS / "tpc-162-mvp6-actual-carrier-endpoint-route-decision"
TPC163 = PAPERS / "tpc-163-source-locator-census-native-key-collision"
TPC164 = PAPERS / "tpc-164-minimal-archived-separation-key"
TPC165 = PAPERS / "tpc-165-source-backed-local-global-crosswalk-gluing"

TPC156_DECISION = (
    TPC156 / "experiments" / "tpc156_h1_occurrence_decision.json"
)
TPC162_SNAPSHOT = TPC162 / "experiments" / "tpc162_mvp6_snapshot.json"
TPC162_AUDIT = TPC162 / "experiments" / "tpc162_mvp6_route_audit.json"
TPC163_CENSUS = TPC163 / "experiments" / "tpc163_source_census.json"
TPC163_AUDIT = TPC163 / "experiments" / "tpc163_source_census_audit.json"
TPC164_CERT = TPC164 / "experiments" / "tpc164_minimal_key_certificate.json"
TPC164_AUDIT = TPC164 / "experiments" / "tpc164_minimal_key_audit.json"
TPC165_CERT = TPC165 / "experiments" / "tpc165_gluing_certificate.json"
TPC165_AUDIT = TPC165 / "experiments" / "tpc165_gluing_audit.json"

SCHEMA = PAPER / "schemas" / "tpc166-refined-h1-frontier-v1.schema.json"
SAMPLE = PAPER / "samples" / "tpc166_refined_frontier_excerpt.json"
DECISION = HERE / "tpc166_refined_h1_frontier.json"
AUDIT = HERE / "tpc166_refined_h1_frontier_audit.json"

HASH_MODE = "CANONICAL_UTF8_LF_V2"
SCHEMA_ID = "tpc-166-refined-h1-crosswalk-frontier-v1"

MONOLITH = "H1.theorem_backed_occurrence_provenance_crosswalk"
LOCAL = "H1.source_backed_local_occurrence_edge_family"
SUPPORT = "H1.actual_active_support_certificate"
CANONICAL = "H1.canonical_minimal_representation_certificate"
OVERLAP = "H1.local_overlap_bijection_cocycle"
TOTALITY = "H1.glued_formal_occurrence_totality"
WITNESS = "H1.production_occurrence_witness"
KEY = "S164.minimal_archived_separation_key"
GLUING = "S165.finite_typed_gluing_theorem"
EXPECTED_ANTICHAIN = [LOCAL, SUPPORT, CANONICAL]


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


def load_json(path: Path) -> dict[str, Any]:
    value = json.loads(normalize(path.read_text(encoding="utf-8")))
    if not isinstance(value, dict):
        raise ValueError(f"object expected: {path}")
    return value


def source_lock(source_id: str, path: Path) -> dict[str, str]:
    return {
        "source_id": source_id,
        "path": rel(path),
        "canonical_utf8_lf_sha256": canonical_hash(path),
        "hash_mode": HASH_MODE,
        "hash_semantics": "INTEGRITY_ONLY",
    }


def node_map(value: dict[str, Any]) -> dict[str, dict[str, Any]]:
    nodes = value["refined_dag"]["nodes"]
    mapping = {node["node_id"]: node for node in nodes}
    if len(mapping) != len(nodes):
        raise ValueError("duplicate DAG node")
    return mapping


def topological_order(nodes: dict[str, dict[str, Any]]) -> list[str]:
    temporary: set[str] = set()
    permanent: set[str] = set()
    order: list[str] = []

    def visit(node_id: str) -> None:
        if node_id in permanent:
            return
        if node_id in temporary:
            raise ValueError("cycle in refined H1 DAG")
        temporary.add(node_id)
        for parent in nodes[node_id]["parents"]:
            if parent not in nodes:
                raise ValueError("missing parent node")
            visit(parent)
        temporary.remove(node_id)
        permanent.add(node_id)
        order.append(node_id)

    for node_id in nodes:
        visit(node_id)
    return order


def unresolved_root_antichain(
    nodes: dict[str, dict[str, Any]], target: str
) -> list[str]:
    ancestors: set[str] = set()

    def collect(node_id: str) -> None:
        if node_id in ancestors:
            return
        ancestors.add(node_id)
        for parent in nodes[node_id]["parents"]:
            collect(parent)

    collect(target)
    unresolved = {
        node_id
        for node_id in ancestors
        if nodes[node_id]["status"] == "NOT_TESTABLE"
    }
    roots = [
        node_id
        for node_id in unresolved
        if not any(parent in unresolved for parent in nodes[node_id]["parents"])
    ]
    preferred = {node_id: index for index, node_id in enumerate(EXPECTED_ANTICHAIN)}
    return sorted(roots, key=lambda item: (preferred.get(item, 99), item))


def validate_decision(value: dict[str, Any]) -> None:
    required = {
        "schema",
        "source_locks",
        "historical_pointer",
        "refinement_scope",
        "refined_dag",
        "minimal_not_testable_root_antichain",
        "selection",
        "production_evidence",
        "current_decision",
        "claim_boundary",
    }
    if set(value) != required or value.get("schema") != SCHEMA_ID:
        raise ValueError("decision contract drift")
    expected_locks = {
        "TPC156.decision": canonical_hash(TPC156_DECISION),
        "TPC162.snapshot": canonical_hash(TPC162_SNAPSHOT),
        "TPC162.audit": canonical_hash(TPC162_AUDIT),
        "TPC163.census": canonical_hash(TPC163_CENSUS),
        "TPC163.audit": canonical_hash(TPC163_AUDIT),
        "TPC164.certificate": canonical_hash(TPC164_CERT),
        "TPC164.audit": canonical_hash(TPC164_AUDIT),
        "TPC165.certificate": canonical_hash(TPC165_CERT),
        "TPC165.audit": canonical_hash(TPC165_AUDIT),
    }
    observed_locks = {
        item["source_id"]: item["canonical_utf8_lf_sha256"]
        for item in value["source_locks"]
    }
    if observed_locks != expected_locks:
        raise ValueError("source-lock drift")
    historical = value["historical_pointer"]
    if (
        historical.get("source") != "TPC162"
        or historical.get("frozen_first_missing") != MONOLITH
        or historical.get("retroactively_rewritten") is not False
    ):
        raise ValueError("TPC-162 historical pointer was rewritten")
    scope = value["refinement_scope"]
    if (
        scope.get("target_subdag")
        != "HISTORICAL_MONOLITHIC_CROSSWALK_SUBDAG_ONLY"
        or scope.get("is_full_H1_map_clause") is not False
        or scope.get("is_full_H1_minimal_blocker_antichain") is not False
        or scope.get("full_map_clause_additional_requirements")
        != "NINE_ZERO_DEFECTS_PLUS_INDEPENDENT_OCCURRENCE_REGISTRY"
        or scope.get("scalar_plus_ETO_clause_status")
        != "INDEPENDENT_NOT_TESTABLE"
    ):
        raise ValueError("crosswalk sub-DAG was promoted to full H1 scope")
    nodes = node_map(value)
    order = topological_order(nodes)
    if set(order) != set(nodes) or value["refined_dag"].get("acyclic") is not True:
        raise ValueError("DAG validation drift")
    expected_status = {
        KEY: "PROVED",
        GLUING: "PROVED",
        LOCAL: "NOT_TESTABLE",
        SUPPORT: "NOT_TESTABLE",
        CANONICAL: "NOT_TESTABLE",
        OVERLAP: "NOT_TESTABLE",
        TOTALITY: "NOT_TESTABLE",
        WITNESS: "NOT_TESTABLE",
        MONOLITH: "NOT_TESTABLE",
    }
    if set(nodes) != set(expected_status):
        raise ValueError("refined node universe drift")
    if any(nodes[node_id]["status"] != status for node_id, status in expected_status.items()):
        raise ValueError("refined node status drift")
    expected_parents = {
        KEY: [],
        GLUING: [],
        LOCAL: [],
        SUPPORT: [],
        CANONICAL: [],
        OVERLAP: [LOCAL],
        TOTALITY: [KEY, GLUING, LOCAL, OVERLAP],
        WITNESS: [TOTALITY, SUPPORT, CANONICAL],
        MONOLITH: [WITNESS],
    }
    if any(nodes[node_id]["parents"] != parents for node_id, parents in expected_parents.items()):
        raise ValueError("refined dependency relation drift")
    roots = unresolved_root_antichain(nodes, MONOLITH)
    if roots != EXPECTED_ANTICHAIN:
        raise ValueError("computed minimal unresolved antichain drift")
    if value["minimal_not_testable_root_antichain"] != roots:
        raise ValueError("declared antichain does not match DAG")
    selection = value["selection"]
    if (
        selection.get("canonical_selected_representative") != LOCAL
        or selection.get("refined_first_child_pointer") != LOCAL
        or selection.get("selection_erases_other_antichain_members") is not False
        or selection.get("full_antichain_preserved") != EXPECTED_ANTICHAIN
    ):
        raise ValueError("frontier selection erased an independent root")
    evidence = value["production_evidence"]
    if (
        evidence.get("theorem_backed_local_occurrence_edge_count") != 0
        or evidence.get("production_local_patch_family") != "NOT_TESTABLE"
    ):
        raise ValueError("production local-edge evidence promoted")
    current = value["current_decision"]
    if (
        current.get("verdict") != "NOT_TESTABLE"
        or current.get("selected_route_stopped") is not False
        or current.get("actual_carrier_impossibility") is not False
    ):
        raise ValueError("current decision promoted or stopped")
    if any(value["claim_boundary"].values()):
        raise ValueError("claim boundary promoted")


def build() -> tuple[dict[str, Any], dict[str, Any], dict[str, Any]]:
    t156 = load_json(TPC156_DECISION)
    t162 = load_json(TPC162_SNAPSHOT)
    t162_audit = load_json(TPC162_AUDIT)
    t163 = load_json(TPC163_CENSUS)
    t163_audit = load_json(TPC163_AUDIT)
    t164 = load_json(TPC164_CERT)
    t164_audit = load_json(TPC164_AUDIT)
    t165 = load_json(TPC165_CERT)
    t165_audit = load_json(TPC165_AUDIT)
    if any(
        audit.get("status") != "PASS"
        for audit in (t162_audit, t163_audit, t164_audit, t165_audit)
    ):
        raise ValueError("upstream audit is not PASS")
    required_defects = [
        "H1.defect.D_L",
        "H1.defect.D_QD",
        "H1.defect.D_QZ",
        "H1.defect.D_G",
        "H1.defect.D_P",
        "H1.defect.D_DZ",
        "H1.defect.D_GP",
        "H1.defect.D_cover",
        "H1.defect.D_rec",
    ]
    map_components = t156.get("h1_contract", {}).get("map_clause", {}).get(
        "components"
    )
    scalar_components = t156.get("h1_contract", {}).get(
        "scalar_clause", {}
    ).get("components")
    if (
        t156.get("current_verdict") != "NOT_TESTABLE"
        or map_components
        != [
            MONOLITH,
            *required_defects,
            "H1.frontier_occurrence_registry_totality",
        ]
        or scalar_components
        != [
            "H1.complete_FUM_scalar_oX",
            "H1.theorem_backed_ETO_disposition",
        ]
    ):
        raise ValueError("TPC-156 full H1 clause scope drift")
    if (
        t162.get("current_verdict") != "NOT_TESTABLE"
        or t162.get("gate_projection", {}).get("H1", {}).get("source_node")
        != MONOLITH
    ):
        raise ValueError("TPC-162 historical frontier drift")
    if t163.get("production_crosswalk_edge_census", {}).get(
        "theorem_backed_edge_count"
    ) != 0:
        raise ValueError("TPC-163 production edge count drift")
    if t164.get("selected_archived_key") != [
        "ell", "k", "native_d", "jL", "jK"
    ]:
        raise ValueError("TPC-164 key drift")
    if (
        t165.get("formal_gluing_theorem", {}).get("theorem_level")
        != "PROVED_L0_FORMAL"
        or t165.get("production_status", {}).get(
            "source_backed_local_edge_count"
        )
        != 0
    ):
        raise ValueError("TPC-165 gluing interface drift")
    locks = [
        source_lock("TPC156.decision", TPC156_DECISION),
        source_lock("TPC162.snapshot", TPC162_SNAPSHOT),
        source_lock("TPC162.audit", TPC162_AUDIT),
        source_lock("TPC163.census", TPC163_CENSUS),
        source_lock("TPC163.audit", TPC163_AUDIT),
        source_lock("TPC164.certificate", TPC164_CERT),
        source_lock("TPC164.audit", TPC164_AUDIT),
        source_lock("TPC165.certificate", TPC165_CERT),
        source_lock("TPC165.audit", TPC165_AUDIT),
    ]
    nodes = [
        {
            "node_id": KEY,
            "role": "ARCHIVE_ADDRESS",
            "status": "PROVED",
            "parents": [],
            "source": "TPC164",
        },
        {
            "node_id": GLUING,
            "role": "FORMAL_DESCENT_THEOREM",
            "status": "PROVED",
            "parents": [],
            "source": "TPC165",
        },
        {
            "node_id": LOCAL,
            "role": "SOURCE_BACKED_LOCAL_EDGE_ROOT",
            "status": "NOT_TESTABLE",
            "parents": [],
            "source": None,
        },
        {
            "node_id": SUPPORT,
            "role": "ACTUAL_CARRIER_ROOT",
            "status": "NOT_TESTABLE",
            "parents": [],
            "source": None,
        },
        {
            "node_id": CANONICAL,
            "role": "REPRESENTATION_ROOT",
            "status": "NOT_TESTABLE",
            "parents": [],
            "source": None,
        },
        {
            "node_id": OVERLAP,
            "role": "LOCAL_COMPATIBILITY",
            "status": "NOT_TESTABLE",
            "parents": [LOCAL],
            "source": None,
        },
        {
            "node_id": TOTALITY,
            "role": "FORMAL_GLOBAL_CARRIER",
            "status": "NOT_TESTABLE",
            "parents": [KEY, GLUING, LOCAL, OVERLAP],
            "source": None,
        },
        {
            "node_id": WITNESS,
            "role": "PRODUCTION_TYPED_WITNESS",
            "status": "NOT_TESTABLE",
            "parents": [TOTALITY, SUPPORT, CANONICAL],
            "source": None,
        },
        {
            "node_id": MONOLITH,
            "role": "HISTORICAL_MONOLITHIC_TARGET",
            "status": "NOT_TESTABLE",
            "parents": [WITNESS],
            "source": "TPC162_HISTORICAL_POINTER",
        },
    ]
    decision: dict[str, Any] = {
        "schema": SCHEMA_ID,
        "source_locks": locks,
        "historical_pointer": {
            "source": "TPC162",
            "frozen_first_missing": MONOLITH,
            "retroactively_rewritten": False,
            "interpretation": (
                "TPC-162 remains historically correct at its declared "
                "monolithic interface."
            ),
        },
        "refinement_scope": {
            "target_subdag": "HISTORICAL_MONOLITHIC_CROSSWALK_SUBDAG_ONLY",
            "is_full_H1_map_clause": False,
            "is_full_H1_minimal_blocker_antichain": False,
            "full_map_clause_additional_requirements": (
                "NINE_ZERO_DEFECTS_PLUS_INDEPENDENT_OCCURRENCE_REGISTRY"
            ),
            "nine_zero_defect_nodes": required_defects,
            "independent_occurrence_registry_node": (
                "H1.frontier_occurrence_registry_totality"
            ),
            "scalar_plus_ETO_clause_status": "INDEPENDENT_NOT_TESTABLE",
            "scalar_plus_ETO_nodes": scalar_components,
            "deferred_full_H1_graph_integration": "TPC171",
        },
        "refined_dag": {
            "target": MONOLITH,
            "dependency_direction": "PARENT_IS_PREREQUISITE",
            "acyclic": True,
            "nodes": nodes,
        },
        "minimal_not_testable_root_antichain": list(EXPECTED_ANTICHAIN),
        "selection": {
            "canonical_selected_representative": LOCAL,
            "refined_first_child_pointer": LOCAL,
            "selection_reason": (
                "It is the first constructible source-producing object in "
                "the local-to-global branch."
            ),
            "full_antichain_preserved": list(EXPECTED_ANTICHAIN),
            "selection_erases_other_antichain_members": False,
        },
        "production_evidence": {
            "theorem_backed_local_occurrence_edge_count": 0,
            "production_local_patch_family": "NOT_TESTABLE",
            "production_overlap_cocycle": "NOT_TESTABLE",
            "production_formal_occurrence_totality": "NOT_TESTABLE",
            "production_actual_active_support": "NOT_TESTABLE",
            "production_canonical_minimal_representation": "NOT_TESTABLE",
        },
        "current_decision": {
            "verdict": "NOT_TESTABLE",
            "selected_route_stopped": False,
            "actual_carrier_impossibility": False,
            "next_forced_object": LOCAL,
            "parallel_independent_roots": [SUPPORT, CANONICAL],
        },
        "claim_boundary": {
            "tpc162_historical_first_missing_rewritten": False,
            "three_roots_are_full_H1_minimal_blocker_antichain": False,
            "production_local_occurrence_family_proved": False,
            "actual_active_support_proved": False,
            "canonical_minimal_representation_proved": False,
            "production_crosswalk_proved": False,
            "selected_route_stopped": False,
            "positive_fixed_X_L2": False,
            "prime_pair_lower_bound": False,
            "twin_prime_theorem": False,
        },
    }
    validate_decision(decision)
    sample = {
        "schema": "tpc-166-refined-frontier-excerpt-v1",
        "scope": "HISTORICAL_MONOLITHIC_CROSSWALK_SUBDAG_ONLY",
        "historical_first_missing": MONOLITH,
        "refined_first_child_pointer": LOCAL,
        "minimal_not_testable_root_antichain": list(EXPECTED_ANTICHAIN),
        "descendant_chain": [
            OVERLAP,
            TOTALITY,
            WITNESS,
            MONOLITH,
        ],
        "current_verdict": "NOT_TESTABLE",
        "claim_boundary": {
            "historical_pointer_rewritten": False,
            "selected_representative_is_only_root": False,
            "three_roots_are_full_H1_antichain": False,
            "production_evidence": False,
        },
    }

    def rejected(mutator: Any) -> bool:
        candidate = copy.deepcopy(decision)
        mutator(candidate)
        try:
            validate_decision(candidate)
        except (KeyError, TypeError, ValueError):
            return True
        return False

    def erase_support(value: dict[str, Any]) -> None:
        value["minimal_not_testable_root_antichain"].remove(SUPPORT)
        value["selection"]["full_antichain_preserved"].remove(SUPPORT)

    def erase_canonical(value: dict[str, Any]) -> None:
        value["minimal_not_testable_root_antichain"].remove(CANONICAL)
        value["selection"]["full_antichain_preserved"].remove(CANONICAL)

    def rewrite_history(value: dict[str, Any]) -> None:
        value["historical_pointer"]["frozen_first_missing"] = LOCAL
        value["historical_pointer"]["retroactively_rewritten"] = True

    def fabricate_local_edge(value: dict[str, Any]) -> None:
        value["production_evidence"]["theorem_backed_local_occurrence_edge_count"] = 1

    def force_go(value: dict[str, Any]) -> None:
        value["current_decision"]["verdict"] = "GO"

    def stop_route(value: dict[str, Any]) -> None:
        value["current_decision"]["selected_route_stopped"] = True

    def create_cycle(value: dict[str, Any]) -> None:
        for node in value["refined_dag"]["nodes"]:
            if node["node_id"] == LOCAL:
                node["parents"] = [MONOLITH]

    def select_outside(value: dict[str, Any]) -> None:
        value["selection"]["canonical_selected_representative"] = OVERLAP

    def promote_to_full_h1(value: dict[str, Any]) -> None:
        value["refinement_scope"]["is_full_H1_map_clause"] = True
        value["refinement_scope"][
            "is_full_H1_minimal_blocker_antichain"
        ] = True

    mutations = {
        "active_support_root_erasure_rejected": rejected(erase_support),
        "canonical_minimality_root_erasure_rejected": rejected(erase_canonical),
        "historical_first_missing_rewrite_rejected": rejected(rewrite_history),
        "fabricated_local_edge_rejected": rejected(fabricate_local_edge),
        "not_testable_to_go_promotion_rejected": rejected(force_go),
        "selected_route_stop_promotion_rejected": rejected(stop_route),
        "dependency_cycle_rejected": rejected(create_cycle),
        "representative_outside_antichain_rejected": rejected(select_outside),
        "crosswalk_subdag_to_full_h1_promotion_rejected": rejected(
            promote_to_full_h1
        ),
    }
    if not all(mutations.values()):
        raise ValueError("mutation regression failed")
    audit = {
        "schema": "tpc-166-refined-h1-frontier-audit-v1",
        "status": "PASS",
        "decision_sha256": hashlib.sha256(
            canonical_json(decision).encode("utf-8")
        ).hexdigest(),
        "checks": {
            "all_nine_source_locks_recomputed": True,
            "dag_acyclicity_recomputed": True,
            "minimal_not_testable_root_antichain_recomputed": True,
            "crosswalk_subdag_scope_preserved": True,
            "full_map_and_scalar_clauses_remain_external": True,
            "historical_pointer_preserved": True,
            "production_local_edge_count_remains_zero": True,
            "current_verdict_remains_not_testable": True,
        },
        "mutation_regressions": mutations,
        "claim_boundary": decision["claim_boundary"],
    }
    return decision, sample, audit


def output_bytes(value: dict[str, Any]) -> bytes:
    return canonical_json(value).encode("utf-8")


def write_or_check(path: Path, value: dict[str, Any], check: bool) -> None:
    expected = output_bytes(value)
    if check:
        if not path.exists() or path.read_bytes() != expected:
            raise ValueError(f"generated artifact drift: {path}")
    else:
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_bytes(expected)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()
    decision, sample, audit = build()
    write_or_check(DECISION, decision, args.check)
    write_or_check(SAMPLE, sample, args.check)
    write_or_check(AUDIT, audit, args.check)
    mode = "CHECK" if args.check else "GENERATE"
    print(f"TPC-166 {mode} PASS")
    print(
        json.dumps(
            {
                "status": audit["status"],
                "verdict": decision["current_decision"]["verdict"],
                "historical_first_missing": decision["historical_pointer"][
                    "frozen_first_missing"
                ],
                "refined_first_child": decision["selection"][
                    "refined_first_child_pointer"
                ],
                "minimal_root_count": len(
                    decision["minimal_not_testable_root_antichain"]
                ),
                "production_local_edges": decision["production_evidence"][
                    "theorem_backed_local_occurrence_edge_count"
                ],
            },
            sort_keys=True,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
