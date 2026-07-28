#!/usr/bin/env python3
"""Generate and verify the TPC-179 H1 structural integration."""

from __future__ import annotations

import argparse
import copy
import hashlib
import json
from pathlib import Path
from typing import Any, Callable


HERE = Path(__file__).resolve().parent
PAPER = HERE.parent
PAPERS = PAPER.parent
REPO = PAPERS.parent
OUTPUT = HERE / "tpc179_h1_integration.json"
AUDIT = HERE / "tpc179_h1_integration_audit.json"
OUTPUT_SCHEMA = PAPER / "schemas" / "tpc179-h1-integration-v1.schema.json"
AUDIT_SCHEMA = (
    PAPER / "schemas" / "tpc179-h1-integration-audit-v1.schema.json"
)

TPC166 = PAPERS / "tpc-166-refined-h1-crosswalk-frontier-decision"
TPC173 = PAPERS / "tpc-173-production-source-claim-inventory"
TPC174 = PAPERS / "tpc-174-local-occurrence-edge-witness-schema"
TPC175 = PAPERS / "tpc-175-declared-corpus-local-edge-family"
TPC176 = PAPERS / "tpc-176-source-backed-coverage-gluing-audit"
TPC177 = PAPERS / "tpc-177-actual-active-support-vacuity-firewall"
TPC178 = PAPERS / "tpc-178-canonical-minimal-representation-eligibility"

TPC166_DECISION = TPC166 / "experiments" / "tpc166_refined_h1_frontier.json"
TPC173_INVENTORY = TPC173 / "experiments" / "tpc173_source_claim_inventory.json"
TPC173_AUDIT = (
    TPC173 / "experiments" / "tpc173_source_claim_inventory_audit.json"
)
TPC174_CONTRACT = TPC174 / "experiments" / "tpc174_witness_contract.json"
TPC174_AUDIT = (
    TPC174 / "experiments" / "tpc174_witness_contract_audit.json"
)
TPC175_FAMILY = TPC175 / "experiments" / "tpc175_local_edge_family.json"
TPC175_AUDIT = (
    TPC175 / "experiments" / "tpc175_local_edge_family_audit.json"
)
TPC176_AUDIT = TPC176 / "experiments" / "tpc176_coverage_gluing_audit.json"
TPC177_AUDIT = TPC177 / "experiments" / "tpc177_active_support_audit.json"
TPC178_AUDIT = TPC178 / "experiments" / "tpc178_representation_audit.json"

HASH_MODE = "CANONICAL_UTF8_LF_V2"
SCOPE = "FROZEN_CONTIGUOUS_OCCURRENCE_SOURCE_CORRIDOR_TPC133_172"
SCHEMA_ID = "tpc-179-h1-structural-corpus-exhaustion-integration-v1"
AUDIT_SCHEMA_ID = (
    "tpc-179-h1-structural-corpus-exhaustion-integration-audit-v1"
)
LOCAL = "H1.source_backed_local_occurrence_edge_family"
SUPPORT = "H1.actual_active_support_certificate"
REPRESENTATION = "H1.canonical_minimal_representation_certificate"
ANTICHAIN = [LOCAL, SUPPORT, REPRESENTATION]


def normalize_lf(text: str) -> str:
    return text.replace("\r\n", "\n").replace("\r", "\n")


def canonical_json(value: Any) -> str:
    return json.dumps(value, ensure_ascii=False, indent=2, sort_keys=True) + "\n"


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


def repo_relative(path: Path) -> str:
    return path.resolve().relative_to(REPO.resolve()).as_posix()


def load_json(path: Path) -> dict[str, Any]:
    value = json.loads(normalize_lf(path.read_text(encoding="utf-8")))
    if not isinstance(value, dict):
        raise TypeError(f"expected JSON object: {path}")
    return value


def source_lock(source_id: str, path: Path) -> dict[str, Any]:
    if not path.is_file():
        raise FileNotFoundError(path)
    return {
        "source_id": source_id,
        "path": repo_relative(path),
        "canonical_utf8_lf_sha256": sha256(path),
        "hash_mode": HASH_MODE,
        "hash_semantics": "INTEGRITY_ONLY",
    }


def validate_source_locks(records: list[dict[str, Any]]) -> None:
    ids: set[str] = set()
    for record in records:
        if record["source_id"] in ids:
            raise ValueError("duplicate source lock id")
        ids.add(record["source_id"])
        if (
            record["hash_mode"] != HASH_MODE
            or record["hash_semantics"] != "INTEGRITY_ONLY"
        ):
            raise ValueError("source lock semantic drift")
        path = REPO / record["path"]
        if not path.is_file() or sha256(path) != record["canonical_utf8_lf_sha256"]:
            raise ValueError(f"source lock drift: {record['source_id']}")


def validate_upstream(
    t166: dict[str, Any],
    t173: dict[str, Any],
    a173: dict[str, Any],
    t174: dict[str, Any],
    a174: dict[str, Any],
    t175: dict[str, Any],
    a175: dict[str, Any],
    t176: dict[str, Any],
    t177: dict[str, Any],
    t178: dict[str, Any],
) -> None:
    if t166["minimal_not_testable_root_antichain"] != ANTICHAIN:
        raise ValueError("TPC-166 three-root antichain drift")
    partition = t173["corpus_partition"]["file_disposition_counts"]
    if (
        t173.get("scope") != SCOPE
        or t173.get("qualifying_count") != 0
        or t173.get("qualifying_claim_ids") != []
        or t173.get("max_defensible_family_status")
        != "EMPTY_IN_FROZEN_DECLARED_CORPUS"
        or partition["NOT_MAPPED_YET"] != 0
        or partition["QUALIFYING"] != 0
        or a173.get("status") != "PASS"
    ):
        raise ValueError("TPC-173 inventory drift")
    if (
        t174.get("schema")
        != "tpc-174-local-occurrence-edge-witness-contract-export-v1"
        or t174["source_inventory"]["scope"] != SCOPE
        or t174["production_status"]["qualifying_source_claim_count"] != 0
        or t174["production_status"]["production_witness_present"] is not False
        or t174["production_status"]["status"] != "NOT_TESTABLE"
        or a174.get("status") != "PASS"
    ):
        raise ValueError("TPC-174 witness contract drift")
    coverage175 = t175["coverage"]
    if (
        t175.get("scope") != SCOPE
        or t175.get("status") != "EMPTY_IN_FROZEN_DECLARED_CORPUS"
        or t175.get("family_cardinality") != 0
        or t175.get("eligible_carrier_count") != 0
        or t175.get("local_edge_family") != []
        or coverage175["production_cut_count"] != 2988
        or coverage175["covered_cut_count"] != 0
        or coverage175["duplicated_cut_count"] != 0
        or coverage175["unmatched_cut_count"] != 2988
        or coverage175["tpc165_gluing_instantiated"] is not False
        or a175.get("status") != "PASS"
    ):
        raise ValueError("TPC-175 maximal-family drift")
    coverage176 = t176["coverage_ledger"]
    route176 = t176["route_decision"]
    if (
        t176.get("status") != "PASS"
        or coverage176["declared_production_cut_count"] != 2988
        or coverage176["covered_cut_count"] != 0
        or coverage176["duplicate_cut_count"] != 0
        or coverage176["unmatched_cut_count"] != 2988
        or coverage176["eligible_carrier_count"] != 0
        or route176["method_cell_status"]
        != "STOP_SCOPED_EMPTY_PROVED_LOCAL_EDGE_FAMILY"
        or route176["occurrence_augmented_architecture_status"] != "NOT_TESTABLE"
        or route176["occurrence_augmented_architecture_stopped"] is not False
    ):
        raise ValueError("TPC-176 coverage/gluing drift")
    if (
        t177.get("status") != "PASS"
        or t177["vacuity_firewall"]["status"]
        != "VACUOUS_EMPTY_ELIGIBLE_DOMAIN"
        or t177["h1_active_support_root"]["node_id"] != SUPPORT
        or t177["h1_active_support_root"]["status"] != "NOT_TESTABLE"
        or t177["h1_active_support_root"]["closed"] is not False
    ):
        raise ValueError("TPC-177 active-support drift")
    if (
        t178.get("status") != "PASS"
        or t178["representation_audit"]["status"]
        != "ELIGIBILITY_BLOCKED_EMPTY_CARRIER_DOMAIN"
        or t178["h1_representation_root"]["node_id"] != REPRESENTATION
        or t178["h1_representation_root"]["status"] != "NOT_TESTABLE"
        or t178["h1_representation_root"]["closed"] is not False
        or t178["archive_key_import"]["role"] != "ARCHIVE_ADDRESS"
    ):
        raise ValueError("TPC-178 representation drift")


def build_integration() -> dict[str, Any]:
    t166 = load_json(TPC166_DECISION)
    t173 = load_json(TPC173_INVENTORY)
    a173 = load_json(TPC173_AUDIT)
    t174 = load_json(TPC174_CONTRACT)
    a174 = load_json(TPC174_AUDIT)
    t175 = load_json(TPC175_FAMILY)
    a175 = load_json(TPC175_AUDIT)
    t176 = load_json(TPC176_AUDIT)
    t177 = load_json(TPC177_AUDIT)
    t178 = load_json(TPC178_AUDIT)
    validate_upstream(
        t166, t173, a173, t174, a174, t175, a175, t176, t177, t178
    )

    value: dict[str, Any] = {
        "schema": SCHEMA_ID,
        "status": "PASS",
        "source_locks": [
            source_lock("TPC166.refined_h1_frontier", TPC166_DECISION),
            source_lock("TPC173.source_claim_inventory", TPC173_INVENTORY),
            source_lock("TPC173.source_claim_inventory_audit", TPC173_AUDIT),
            source_lock("TPC174.witness_contract", TPC174_CONTRACT),
            source_lock("TPC174.witness_contract_audit", TPC174_AUDIT),
            source_lock("TPC175.local_edge_family", TPC175_FAMILY),
            source_lock("TPC175.local_edge_family_audit", TPC175_AUDIT),
            source_lock("TPC176.coverage_gluing_audit", TPC176_AUDIT),
            source_lock("TPC177.active_support_audit", TPC177_AUDIT),
            source_lock("TPC178.representation_audit", TPC178_AUDIT),
        ],
        "scope": SCOPE,
        "current_verdict": "NOT_TESTABLE",
        "first_missing": LOCAL,
        "minimal_root_antichain": list(ANTICHAIN),
        "root_ledger": [
            {
                "node_id": LOCAL,
                "root_status": "NOT_TESTABLE",
                "closed": False,
                "current_evidence_status": (
                    "EMPTY_IN_FROZEN_DECLARED_CORPUS"
                ),
                "scoped_method_cell": (
                    "production_local_edge_extraction_from_tpc133_172"
                ),
                "scoped_method_cell_status": "STOP_SCOPED",
                "reason": (
                    "ZERO_QUALIFYING_CLAIMS_IN_COMPLETE_FROZEN_CORPUS_"
                    "DOES_NOT_PROVE_MATHEMATICAL_NONEXISTENCE"
                ),
            },
            {
                "node_id": SUPPORT,
                "root_status": "NOT_TESTABLE",
                "closed": False,
                "current_evidence_status": (
                    "VACUOUS_EMPTY_ELIGIBLE_DOMAIN"
                ),
                "scoped_method_cell": "actual_active_support_audit",
                "scoped_method_cell_status": "INPUT_INELIGIBLE",
                "reason": (
                    "EMPTY_DOMAIN_UNIVERSAL_HAS_NO_EXISTENTIAL_"
                    "ACTIVE_SUPPORT_WITNESS"
                ),
            },
            {
                "node_id": REPRESENTATION,
                "root_status": "NOT_TESTABLE",
                "closed": False,
                "current_evidence_status": (
                    "ELIGIBILITY_BLOCKED_EMPTY_CARRIER_DOMAIN"
                ),
                "scoped_method_cell": (
                    "canonical_minimal_representation_audit"
                ),
                "scoped_method_cell_status": "INPUT_INELIGIBLE",
                "reason": (
                    "NO_ELIGIBLE_PHYSICAL_REPRESENTATION_CLASS; "
                    "ARCHIVE_KEY_IS_ADDRESS_ONLY"
                ),
            },
        ],
        "scoped_route_cells": [
            {
                "cell_id": (
                    "production_local_edge_extraction_from_tpc133_172"
                ),
                "cell_type": "SOURCE_EXTRACTION_METHOD",
                "status": "STOP_SCOPED",
                "scope": SCOPE,
                "complete_architecture": False,
                "global_infeasibility_proved": False,
                "reroute_eligible_by_itself": False,
            },
            {
                "cell_id": "occurrence_augmented_h1_architecture",
                "cell_type": "ARCHITECTURE_ROUTE",
                "status": "NOT_TESTABLE",
                "scope": "PHYSICAL_FIXED_H0_OCCURRENCE_RETURN",
                "complete_architecture": True,
                "global_infeasibility_proved": False,
                "reroute_eligible_by_itself": False,
            },
        ],
        "fixed_h0": {
            "required_physical_value": 2,
            "requirement_preserved": True,
            "eligible_carrier_with_fixed_h0_lineage_count": 0,
            "used_as_arithmetic_evidence": False,
            "fixed_h0_arithmetic_progress": False,
            "status": (
                "REQUIREMENT_UNINSTANTIATED_ON_EMPTY_ELIGIBLE_DOMAIN"
            ),
        },
        "next_actions": [
            "EXPLICITLY_ENLARGE_SOURCE_CORPUS_AND_RERUN_TPC173_179",
            "PROVE_NEW_SOURCE_BACKED_PRODUCTION_LOCAL_EDGE_UNDER_TPC174",
            (
                "REROUTE_ONLY_AFTER_A_COMPLETE_ARCHITECTURE_HAS_AN_"
                "EXACT_SOURCE_BACKED_STOP"
            ),
        ],
        "claim_boundary": {
            "l1_scoped_corpus_exhaustion": True,
            "three_root_h1_antichain_recomputed": True,
            "scoped_extraction_cell_stopped": True,
            "mathematical_nonexistence_proved": False,
            "production_local_occurrence_family_proved_nonempty": False,
            "formal_global_totality_proved": False,
            "actual_active_support_proved": False,
            "canonical_minimal_representation_proved": False,
            "occurrence_augmented_architecture_stopped": False,
            "architecture_infeasible": False,
            "fixed_h0_2_preserved_as_requirement": True,
            "fixed_h0_2_arithmetic_progress": False,
            "named_fixed_phase_theorem": False,
            "program_positive_L2": False,
            "strict_one_over_400": False,
            "prime_pair_lower_bound": False,
            "twin_prime_theorem": False,
        },
    }
    validate_integration(value, verify_sources=True)
    return value


def validate_integration(
    value: dict[str, Any], *, verify_sources: bool
) -> None:
    schema = load_json(OUTPUT_SCHEMA)
    if set(value) != set(schema["properties"]):
        raise ValueError("strict integration top-level schema mismatch")
    if value["schema"] != SCHEMA_ID or value["status"] != "PASS":
        raise ValueError("integration schema or status drift")
    if verify_sources:
        validate_source_locks(value["source_locks"])
    if (
        value["scope"] != SCOPE
        or value["current_verdict"] != "NOT_TESTABLE"
        or value["first_missing"] != LOCAL
        or value["minimal_root_antichain"] != ANTICHAIN
        or len(set(value["minimal_root_antichain"])) != 3
    ):
        raise ValueError("integrated verdict or antichain drift")

    roots = value["root_ledger"]
    if [record["node_id"] for record in roots] != ANTICHAIN:
        raise ValueError("root-ledger ordering drift")
    if any(
        record["root_status"] != "NOT_TESTABLE"
        or record["closed"] is not False
        for record in roots
    ):
        raise ValueError("H1 root promotion")
    if (
        roots[0]["current_evidence_status"]
        != "EMPTY_IN_FROZEN_DECLARED_CORPUS"
        or roots[0]["scoped_method_cell_status"] != "STOP_SCOPED"
        or roots[1]["current_evidence_status"]
        != "VACUOUS_EMPTY_ELIGIBLE_DOMAIN"
        or roots[2]["current_evidence_status"]
        != "ELIGIBILITY_BLOCKED_EMPTY_CARRIER_DOMAIN"
    ):
        raise ValueError("root evidence-status drift")

    cells = {record["cell_id"]: record for record in value["scoped_route_cells"]}
    extraction = cells["production_local_edge_extraction_from_tpc133_172"]
    architecture = cells["occurrence_augmented_h1_architecture"]
    if (
        extraction["cell_type"] != "SOURCE_EXTRACTION_METHOD"
        or extraction["status"] != "STOP_SCOPED"
        or extraction["scope"] != SCOPE
        or extraction["complete_architecture"] is not False
        or extraction["global_infeasibility_proved"] is not False
        or architecture["cell_type"] != "ARCHITECTURE_ROUTE"
        or architecture["status"] != "NOT_TESTABLE"
        or architecture["complete_architecture"] is not True
        or architecture["global_infeasibility_proved"] is not False
    ):
        raise ValueError("scoped stop promoted to architecture stop")

    h0 = value["fixed_h0"]
    if (
        h0["required_physical_value"] != 2
        or h0["requirement_preserved"] is not True
        or h0["eligible_carrier_with_fixed_h0_lineage_count"] != 0
        or h0["used_as_arithmetic_evidence"] is not False
        or h0["fixed_h0_arithmetic_progress"] is not False
        or h0["status"]
        != "REQUIREMENT_UNINSTANTIATED_ON_EMPTY_ELIGIBLE_DOMAIN"
    ):
        raise ValueError("fixed-h0 boundary drift")

    boundary = value["claim_boundary"]
    required_true = (
        "l1_scoped_corpus_exhaustion",
        "three_root_h1_antichain_recomputed",
        "scoped_extraction_cell_stopped",
        "fixed_h0_2_preserved_as_requirement",
    )
    if any(boundary[field] is not True for field in required_true):
        raise ValueError("proved scoped boundary erased")
    required_false = (
        "mathematical_nonexistence_proved",
        "production_local_occurrence_family_proved_nonempty",
        "formal_global_totality_proved",
        "actual_active_support_proved",
        "canonical_minimal_representation_proved",
        "occurrence_augmented_architecture_stopped",
        "architecture_infeasible",
        "fixed_h0_2_arithmetic_progress",
        "named_fixed_phase_theorem",
        "program_positive_L2",
        "strict_one_over_400",
        "prime_pair_lower_bound",
        "twin_prime_theorem",
    )
    if any(boundary[field] is not False for field in required_false):
        raise ValueError("claim boundary promotion")


def mutation_rejected(
    value: dict[str, Any],
    mutate: Callable[[dict[str, Any]], None],
    *,
    verify_sources: bool = False,
) -> bool:
    clone = copy.deepcopy(value)
    mutate(clone)
    try:
        validate_integration(clone, verify_sources=verify_sources)
    except (KeyError, TypeError, ValueError):
        return True
    return False


def build_audit(integration: dict[str, Any]) -> dict[str, Any]:
    mutations = {
        "scoped_stop_to_architecture_stop_rejected": mutation_rejected(
            integration,
            lambda x: x["scoped_route_cells"][1].update(
                {"status": "ARCHITECTURE_INFEASIBLE"}
            ),
        ),
        "global_infeasibility_promotion_rejected": mutation_rejected(
            integration,
            lambda x: x["scoped_route_cells"][0].update(
                {"global_infeasibility_proved": True}
            ),
        ),
        "local_root_proved_promotion_rejected": mutation_rejected(
            integration,
            lambda x: x["root_ledger"][0].update(
                {"root_status": "PROVED", "closed": True}
            ),
        ),
        "active_support_root_erasure_rejected": mutation_rejected(
            integration,
            lambda x: x["minimal_root_antichain"].remove(SUPPORT),
        ),
        "representation_root_erasure_rejected": mutation_rejected(
            integration,
            lambda x: x["minimal_root_antichain"].remove(REPRESENTATION),
        ),
        "vacuous_support_promotion_rejected": mutation_rejected(
            integration,
            lambda x: x["claim_boundary"].update(
                {"actual_active_support_proved": True}
            ),
        ),
        "archive_key_canonicality_promotion_rejected": mutation_rejected(
            integration,
            lambda x: x["claim_boundary"].update(
                {"canonical_minimal_representation_proved": True}
            ),
        ),
        "fixed_h0_progress_promotion_rejected": mutation_rejected(
            integration,
            lambda x: x["fixed_h0"].update(
                {
                    "used_as_arithmetic_evidence": True,
                    "fixed_h0_arithmetic_progress": True,
                }
            ),
        ),
        "program_L2_promotion_rejected": mutation_rejected(
            integration,
            lambda x: x["claim_boundary"].update(
                {"program_positive_L2": True}
            ),
        ),
        "source_hash_drift_rejected": mutation_rejected(
            integration,
            lambda x: x["source_locks"][0].update(
                {"canonical_utf8_lf_sha256": "0" * 64}
            ),
            verify_sources=True,
        ),
    }
    if not all(mutations.values()):
        raise ValueError("mutation regression escaped")
    return {
        "schema": AUDIT_SCHEMA_ID,
        "status": "PASS",
        "integration_sha256": payload_sha256(integration),
        "checks": {
            "all_source_locks_verified": True,
            "tpc173_complete_frozen_partition_preserved": True,
            "tpc174_witness_contract_preserved": True,
            "tpc175_empty_maximal_family_preserved": True,
            "tpc176_cut_and_carrier_ledgers_preserved": True,
            "tpc177_vacuity_firewall_preserved": True,
            "tpc178_archive_key_firewall_preserved": True,
            "three_root_antichain_recomputed": True,
            "scoped_stop_architecture_distinction_preserved": True,
            "fixed_h0_requirement_not_promoted": True,
        },
        "mutation_regressions": mutations,
        "current_verdict": integration["current_verdict"],
        "first_missing": integration["first_missing"],
        "claim_boundary": copy.deepcopy(integration["claim_boundary"]),
    }


def validate_audit(
    audit: dict[str, Any], integration: dict[str, Any]
) -> None:
    schema = load_json(AUDIT_SCHEMA)
    if set(audit) != set(schema["properties"]):
        raise ValueError("strict audit top-level schema mismatch")
    if audit["schema"] != AUDIT_SCHEMA_ID or audit["status"] != "PASS":
        raise ValueError("audit schema or status drift")
    if audit["integration_sha256"] != payload_sha256(integration):
        raise ValueError("integration payload hash drift")
    if not all(audit["checks"].values()) or not all(
        audit["mutation_regressions"].values()
    ):
        raise ValueError("audit check failure")
    if (
        audit["current_verdict"] != "NOT_TESTABLE"
        or audit["first_missing"] != LOCAL
        or audit["claim_boundary"] != integration["claim_boundary"]
    ):
        raise ValueError("audit verdict or claim boundary drift")


def write_or_check(
    path: Path, value: dict[str, Any], check: bool
) -> None:
    rendered = canonical_json(value)
    if check:
        if (
            not path.is_file()
            or normalize_lf(path.read_text(encoding="utf-8")) != rendered
        ):
            raise ValueError(f"generated artifact drift: {path}")
    else:
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(rendered, encoding="utf-8", newline="\n")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()
    integration = build_integration()
    audit = build_audit(integration)
    validate_integration(integration, verify_sources=True)
    validate_audit(audit, integration)
    write_or_check(OUTPUT, integration, args.check)
    write_or_check(AUDIT, audit, args.check)
    mode = "CHECK" if args.check else "GENERATE"
    print(f"TPC-179 {mode} PASS")
    print(
        json.dumps(
            {
                "status": integration["status"],
                "current_verdict": integration["current_verdict"],
                "first_missing": integration["first_missing"],
                "minimal_root_count": len(
                    integration["minimal_root_antichain"]
                ),
                "extraction_cell": integration["scoped_route_cells"][0][
                    "status"
                ],
                "architecture": integration["scoped_route_cells"][1][
                    "status"
                ],
            },
            sort_keys=True,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
