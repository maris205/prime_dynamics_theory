#!/usr/bin/env python3
"""Build the maximal defensible TPC-175 local-edge family."""

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

TPC173 = PAPERS / "tpc-173-production-source-claim-inventory"
TPC174 = PAPERS / "tpc-174-local-occurrence-edge-witness-schema"
TPC163 = PAPERS / "tpc-163-source-locator-census-native-key-collision"

INVENTORY = TPC173 / "experiments" / "tpc173_source_claim_inventory.json"
INVENTORY_AUDIT = (
    TPC173 / "experiments" / "tpc173_source_claim_inventory_audit.json"
)
WITNESS_CONTRACT = TPC174 / "experiments" / "tpc174_witness_contract.json"
WITNESS_AUDIT = TPC174 / "experiments" / "tpc174_witness_contract_audit.json"
SYNTHETIC_WITNESS = (
    TPC174 / "samples" / "tpc174_synthetic_local_edge_witness.json"
)
TPC163_CENSUS = TPC163 / "experiments" / "tpc163_source_census.json"

SCHEMA = PAPER / "schemas" / "tpc175-declared-corpus-local-edge-family-v1.schema.json"
FAMILY = HERE / "tpc175_local_edge_family.json"
AUDIT = HERE / "tpc175_local_edge_family_audit.json"

HASH_MODE = "CANONICAL_UTF8_LF_V2"
SCHEMA_ID = "tpc-175-declared-corpus-local-edge-family-v1"
SCOPE_ID = "FROZEN_CONTIGUOUS_OCCURRENCE_SOURCE_CORRIDOR_TPC133_172"

EXPECTED_CLAIM_BOUNDARY = {
    "empty_family_is_mathematical_nonexistence": False,
    "production_local_occurrence_family_nonempty": False,
    "formal_global_totality_proved": False,
    "actual_active_support_proved": False,
    "canonical_minimal_representation_proved": False,
    "fixed_h0_2_edge_theorem_proved": False,
    "named_fixed_phase_theorem": False,
    "positive_fixed_X_L2": False,
    "strict_one_over_400": False,
    "prime_pair_lower_bound": False,
    "twin_prime_theorem": False,
}
EXPECTED_COVERAGE = {
    "production_cut_count": 2988,
    "covered_cut_count": 0,
    "duplicated_cut_count": 0,
    "unmatched_cut_count": 2988,
    "coverage_fraction": "0/2988",
    "production_local_patch_present": False,
    "production_overlap_cocycle_testable": False,
    "tpc165_gluing_instantiated": False,
    "formal_global_totality_proved": False,
}
EXPECTED_MAXIMALITY = {
    "universe": (
        "TPC174-verifiable production local edges whose source claim "
        "belongs to the TPC173 qualifying inventory"
    ),
    "qualifying_source_universe_cardinality": 0,
    "every_admissible_member_requires_qualifying_source_claim": True,
    "largest_defensible_family_is_empty": True,
    "maximal_within_frozen_declared_corpus": True,
    "mathematical_nonexistence": False,
    "enlarged_corpus_nonexistence": False,
}
EXPECTED_H1_STATUS = {
    "H1.source_backed_local_occurrence_edge_family": (
        "EMPTY_IN_FROZEN_DECLARED_CORPUS"
    ),
    "H1.actual_active_support_certificate": "NOT_TESTABLE",
    "H1.canonical_minimal_representation_certificate": "NOT_TESTABLE",
    "selected_architecture_stopped": False,
    "actual_carrier_impossibility": False,
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


def payload_hash(value: Any) -> str:
    return hashlib.sha256(canonical_json(value).encode("utf-8")).hexdigest()


def rel(path: Path) -> str:
    return path.relative_to(REPO).as_posix()


def load_object(path: Path) -> dict[str, Any]:
    value = json.loads(normalize(path.read_text(encoding="utf-8")))
    if not isinstance(value, dict):
        raise ValueError(f"object expected: {path}")
    return value


def validate_family(value: dict[str, Any]) -> None:
    if value.get("schema") != SCHEMA_ID:
        raise ValueError("wrong TPC-175 schema")
    if value.get("scope") != SCOPE_ID:
        raise ValueError("TPC-175 frozen scope drift")
    if value.get("status") != "EMPTY_IN_FROZEN_DECLARED_CORPUS":
        raise ValueError("current source state requires scoped empty status")
    if value.get("family_cardinality") != len(value.get("local_edge_family", [])):
        raise ValueError("family cardinality mismatch")
    if value.get("eligible_carrier_count") != len(
        value.get("eligible_carriers", [])
    ):
        raise ValueError("eligible carrier count mismatch")
    if value["family_cardinality"] != 0 or value["eligible_carrier_count"] != 0:
        raise ValueError("current frozen corpus has no defensible member")
    if value.get("qualifying_claim_ids") != []:
        raise ValueError("current TPC-173 qualifying claim list is empty")
    if value.get("qualifying_claim_count") != 0:
        raise ValueError("current TPC-173 qualifying claim count is zero")
    if value.get("coverage") != EXPECTED_COVERAGE:
        raise ValueError("empty-family coverage or gluing boundary drift")
    if value.get("maximality_certificate") != EXPECTED_MAXIMALITY:
        raise ValueError("scoped maximality certificate drift")
    if value.get("h1_status") != EXPECTED_H1_STATUS:
        raise ValueError("H1 status or architecture boundary drift")
    if value.get("claim_boundary") != EXPECTED_CLAIM_BOUNDARY:
        raise ValueError("claim boundary drift or undeclared promotion")


def expect_family_rejected(value: dict[str, Any]) -> bool:
    try:
        validate_family(value)
    except (KeyError, TypeError, ValueError):
        return True
    return False


def build() -> tuple[dict[str, Any], dict[str, Any]]:
    inventory = load_object(INVENTORY)
    inventory_audit = load_object(INVENTORY_AUDIT)
    contract = load_object(WITNESS_CONTRACT)
    witness_audit = load_object(WITNESS_AUDIT)
    synthetic = load_object(SYNTHETIC_WITNESS)
    census = load_object(TPC163_CENSUS)

    if inventory_audit.get("status") != "PASS":
        raise ValueError("TPC-173 audit is not PASS")
    if witness_audit.get("status") != "PASS":
        raise ValueError("TPC-174 audit is not PASS")
    if inventory.get("qualifying_count") != 0:
        raise ValueError(
            "TPC-173 now has qualifying claims; TPC-175 must construct rather "
            "than publish the current empty-family theorem"
        )
    if inventory.get("qualifying_claim_ids") != []:
        raise ValueError("TPC-173 qualifying list drift")
    if contract["production_status"]["production_witness_present"] is not False:
        raise ValueError("TPC-174 production witness state changed")
    if synthetic.get("evidence_mode") != "SYNTHETIC_L0_ONLY":
        raise ValueError("TPC-174 fixture lost synthetic firewall")

    production_cut_count = census["production_archive"]["row_count"]
    if production_cut_count != 2988:
        raise ValueError("frozen production cut count drift")

    family = {
        "schema": SCHEMA_ID,
        "scope": inventory["scope"],
        "status": "EMPTY_IN_FROZEN_DECLARED_CORPUS",
        "source_locks": [
            {
                "source_id": "TPC173.inventory",
                "path": rel(INVENTORY),
                "canonical_utf8_lf_sha256": canonical_hash(INVENTORY),
                "hash_mode": HASH_MODE,
                "hash_semantics": "INTEGRITY_ONLY",
            },
            {
                "source_id": "TPC173.audit",
                "path": rel(INVENTORY_AUDIT),
                "canonical_utf8_lf_sha256": canonical_hash(INVENTORY_AUDIT),
                "hash_mode": HASH_MODE,
                "hash_semantics": "INTEGRITY_ONLY",
            },
            {
                "source_id": "TPC174.contract",
                "path": rel(WITNESS_CONTRACT),
                "canonical_utf8_lf_sha256": canonical_hash(WITNESS_CONTRACT),
                "hash_mode": HASH_MODE,
                "hash_semantics": "INTEGRITY_ONLY",
            },
            {
                "source_id": "TPC174.audit",
                "path": rel(WITNESS_AUDIT),
                "canonical_utf8_lf_sha256": canonical_hash(WITNESS_AUDIT),
                "hash_mode": HASH_MODE,
                "hash_semantics": "INTEGRITY_ONLY",
            },
            {
                "source_id": "TPC163.production_cut_census",
                "path": rel(TPC163_CENSUS),
                "canonical_utf8_lf_sha256": canonical_hash(TPC163_CENSUS),
                "hash_mode": HASH_MODE,
                "hash_semantics": "INTEGRITY_AND_FROZEN_CENSUS_ONLY",
            },
        ],
        "admissibility_definition": {
            "source_claim_rule": (
                "every family member must be backed by one TPC-173 claim "
                "with qualification_pass=true"
            ),
            "witness_rule": (
                "every family member must belong to a TPC-174 production "
                "candidate that passes the source-locked verifier"
            ),
            "synthetic_fixtures_eligible": False,
            "shadow_rows_eligible": False,
            "archive_addresses_alone_eligible": False,
            "formal_gluing_hypotheses_alone_eligible": False,
            "actual_core_arithmetic_without_cut_crosswalk_eligible": False,
        },
        "qualifying_claim_ids": [],
        "qualifying_claim_count": 0,
        "eligible_carriers": [],
        "eligible_carrier_count": 0,
        "local_edge_family": [],
        "family_cardinality": 0,
        "coverage": {
            "production_cut_count": production_cut_count,
            "covered_cut_count": 0,
            "duplicated_cut_count": 0,
            "unmatched_cut_count": production_cut_count,
            "coverage_fraction": "0/2988",
            "production_local_patch_present": False,
            "production_overlap_cocycle_testable": False,
            "tpc165_gluing_instantiated": False,
            "formal_global_totality_proved": False,
        },
        "maximality_certificate": copy.deepcopy(EXPECTED_MAXIMALITY),
        "h1_status": copy.deepcopy(EXPECTED_H1_STATUS),
        "next_route": {
            "TPC176": "AUDIT_ZERO_COVERAGE_AND_NONINSTANTIATION_OF_GLUING",
            "TPC177": "NOT_TESTABLE_WITHOUT_SOURCED_CARRIER",
            "TPC178": "NOT_TESTABLE_WITHOUT_SOURCED_CARRIER",
            "TPC179": "RECOMPUTE_THREE_ROOT_H1_FRONTIER_WITH_LOCAL_ROOT_SCOPED_EMPTY",
            "corpus_enlargement_requires_explicit_new_declaration": True,
        },
        "claim_boundary": copy.deepcopy(EXPECTED_CLAIM_BOUNDARY),
    }
    validate_family(family)

    mutations: dict[str, bool] = {}

    fabricated = copy.deepcopy(family)
    fabricated["local_edge_family"] = [
        {
            "edge_id": "fabricated",
            "source_claim_id": "S153.cut_to_shadow_basis_injection",
        }
    ]
    fabricated["family_cardinality"] = 1
    mutations["reject_fabricated_shadow_edge"] = expect_family_rejected(fabricated)

    synthetic_promoted = copy.deepcopy(family)
    synthetic_promoted["eligible_carriers"] = [
        {"source": rel(SYNTHETIC_WITNESS), "evidence_mode": "SYNTHETIC_L0_ONLY"}
    ]
    synthetic_promoted["eligible_carrier_count"] = 1
    mutations["reject_synthetic_fixture_as_eligible_carrier"] = (
        expect_family_rejected(synthetic_promoted)
    )

    global_nonexistence = copy.deepcopy(family)
    global_nonexistence["maximality_certificate"]["mathematical_nonexistence"] = True
    mutations["reject_scoped_empty_to_global_nonexistence"] = (
        expect_family_rejected(global_nonexistence)
    )

    enlarged_nonexistence = copy.deepcopy(family)
    enlarged_nonexistence["maximality_certificate"][
        "enlarged_corpus_nonexistence"
    ] = True
    mutations["reject_scoped_empty_to_enlarged_corpus_nonexistence"] = (
        expect_family_rejected(enlarged_nonexistence)
    )

    gluing_instantiation = copy.deepcopy(family)
    gluing_instantiation["coverage"]["tpc165_gluing_instantiated"] = True
    mutations["reject_empty_family_to_tpc165_gluing_instantiation"] = (
        expect_family_rejected(gluing_instantiation)
    )

    gluing_totality = copy.deepcopy(family)
    gluing_totality["coverage"]["formal_global_totality_proved"] = True
    mutations["reject_empty_family_to_gluing_totality"] = expect_family_rejected(
        gluing_totality
    )

    architecture_stop = copy.deepcopy(family)
    architecture_stop["h1_status"]["selected_architecture_stopped"] = True
    mutations["reject_scoped_empty_to_architecture_stop"] = expect_family_rejected(
        architecture_stop
    )

    actual_impossibility = copy.deepcopy(family)
    actual_impossibility["h1_status"]["actual_carrier_impossibility"] = True
    mutations["reject_scoped_empty_to_actual_carrier_impossibility"] = (
        expect_family_rejected(actual_impossibility)
    )

    maximality_drift = copy.deepcopy(family)
    maximality_drift["maximality_certificate"][
        "largest_defensible_family_is_empty"
    ] = False
    mutations["reject_maximality_diagnostic_drift"] = expect_family_rejected(
        maximality_drift
    )

    for field in EXPECTED_CLAIM_BOUNDARY:
        boundary_promotion = copy.deepcopy(family)
        boundary_promotion["claim_boundary"][field] = True
        mutations[f"reject_claim_boundary_promotion__{field}"] = (
            expect_family_rejected(boundary_promotion)
        )

    if not all(mutations.values()):
        raise ValueError("TPC-175 mutation regression failed")

    audit = {
        "schema": "tpc-175-declared-corpus-local-edge-family-audit-v1",
        "status": "PASS",
        "family_sha256": payload_hash(family),
        "checks": {
            "tpc173_inventory_and_audit_locked": True,
            "tpc174_contract_and_audit_locked": True,
            "qualifying_claim_count_recomputed": 0,
            "eligible_carrier_count_recomputed": 0,
            "family_cardinality_recomputed": 0,
            "production_cut_count_recomputed": production_cut_count,
            "covered_cut_count_recomputed": 0,
            "unmatched_cut_count_recomputed": production_cut_count,
            "maximality_within_declared_corpus": True,
            "mathematical_nonexistence_not_claimed": True,
            "enlarged_corpus_nonexistence_not_claimed": True,
            "tpc165_gluing_not_instantiated": True,
            "formal_global_totality_not_claimed": True,
            "selected_architecture_not_stopped": True,
            "all_claim_boundary_fields_locked": True,
        },
        "mutation_regressions": mutations,
        "claim_boundary": family["claim_boundary"],
    }
    return family, audit


def write_or_check(path: Path, value: dict[str, Any], check: bool) -> None:
    expected = canonical_json(value)
    if check:
        if not path.exists():
            raise SystemExit(f"missing generated artifact: {path}")
        actual = normalize(path.read_text(encoding="utf-8"))
        if actual != expected:
            raise SystemExit(f"generated artifact drift: {path}")
    else:
        path.write_text(expected, encoding="utf-8", newline="\n")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()
    family, audit = build()
    write_or_check(FAMILY, family, args.check)
    write_or_check(AUDIT, audit, args.check)
    mode = "checked" if args.check else "wrote"
    print(
        f"{mode} TPC-175: status={family['status']} "
        f"eligible={family['eligible_carrier_count']} "
        f"family={family['family_cardinality']} "
        f"covered={family['coverage']['covered_cut_count']}/"
        f"{family['coverage']['production_cut_count']}"
    )


if __name__ == "__main__":
    main()
