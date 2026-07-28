#!/usr/bin/env python3
"""TPC-174 minimal local occurrence-edge witness contract and verifier."""

from __future__ import annotations

import argparse
import copy
import hashlib
import json
from fractions import Fraction
from pathlib import Path
from typing import Any


HERE = Path(__file__).resolve().parent
PAPER = HERE.parent
PAPERS = PAPER.parent
REPO = PAPERS.parent

TPC173 = PAPERS / "tpc-173-production-source-claim-inventory"
SOURCE_INVENTORY = TPC173 / "experiments" / "tpc173_source_claim_inventory.json"
SOURCE_AUDIT = TPC173 / "experiments" / "tpc173_source_claim_inventory_audit.json"

SCHEMA = PAPER / "schemas" / "tpc174-local-occurrence-edge-witness-contract-v1.schema.json"
SAMPLE = PAPER / "samples" / "tpc174_synthetic_local_edge_witness.json"
CONTRACT = HERE / "tpc174_witness_contract.json"
AUDIT = HERE / "tpc174_witness_contract_audit.json"

HASH_MODE = "CANONICAL_UTF8_LF_V2"
SCHEMA_ID = "tpc-174-local-occurrence-edge-witness-contract-v1"

ADDRESS_FIELDS = ("ell", "k", "native_d", "jL", "jK")
WITNESS_FIELDS = {
    "schema",
    "witness_id",
    "evidence_mode",
    "source_inventory_scope",
    "fixed_h0",
    "physical_normalization",
    "phase_semantics",
    "covered_cut_addresses",
    "edges",
    "actual_active_support_claimed",
    "canonical_minimal_representation_claimed",
    "claim_boundary",
}
EDGE_FIELDS = {
    "edge_id",
    "source_cut_address",
    "actual_occurrence_id",
    "exact_edge_weight",
    "h0",
    "physical_normalization",
    "carrier_semantics",
    "support_semantics",
    "actual_active_support_claimed",
    "canonical_minimal_representation_claimed",
    "source_evidence",
}
SOURCE_EVIDENCE_FIELDS = {
    "source_claim_id",
    "source_path",
    "canonical_utf8_lf_sha256",
    "theorem_locator",
    "formula_locator",
    "derivation_ast",
}
WITNESS_CLAIM_BOUNDARY = {
    "production_semantics": False,
    "theorem_semantics": False,
    "actual_active_support_proved": False,
    "canonical_minimal_representation_proved": False,
    "named_fixed_phase_theorem": False,
    "positive_fixed_X_L2": False,
    "strict_one_over_400": False,
    "prime_pair_lower_bound": False,
    "twin_prime_theorem": False,
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


def address_tuple(value: dict[str, Any]) -> tuple[int, int, int, int, int]:
    if set(value) != set(ADDRESS_FIELDS):
        raise ValueError("cut address must contain exactly the five archived key fields")
    result = tuple(value[name] for name in ADDRESS_FIELDS)
    if any(type(item) is not int for item in result):
        raise ValueError("cut address values must be integers")
    return result


def exact_fraction(value: dict[str, Any]) -> Fraction:
    if set(value) != {"numerator", "denominator"}:
        raise ValueError("edge weight must contain numerator and denominator")
    numerator = value["numerator"]
    denominator = value["denominator"]
    if type(numerator) is not int or type(denominator) is not int:
        raise ValueError("edge weight must be integral-rational")
    if denominator <= 0:
        raise ValueError("edge denominator must be positive")
    fraction = Fraction(numerator, denominator)
    if fraction.numerator != numerator or fraction.denominator != denominator:
        raise ValueError("edge weight must be reduced")
    if fraction == 0:
        raise ValueError("a local edge must have nonzero edge weight")
    return fraction


def stable_edge_id(address: dict[str, int], occurrence_id: str) -> str:
    token = {"address": address, "actual_occurrence_id": occurrence_id}
    return "local-edge|" + payload_hash(token)[:24]


def qualifying_claim_map(inventory: dict[str, Any]) -> dict[str, dict[str, Any]]:
    return {
        row["claim_id"]: row
        for row in inventory["claim_inventory"]
        if row["qualification_pass"]
    }


def validate_witness(
    witness: dict[str, Any],
    inventory: dict[str, Any],
    *,
    require_production: bool = False,
) -> dict[str, Any]:
    if not isinstance(witness, dict) or set(witness) != WITNESS_FIELDS:
        raise ValueError("witness must contain exactly the declared root fields")
    if witness.get("schema") != SCHEMA_ID:
        raise ValueError("wrong witness schema")
    if not isinstance(witness.get("witness_id"), str) or not witness["witness_id"]:
        raise ValueError("witness id is required")
    mode = witness.get("evidence_mode")
    if mode not in {"SYNTHETIC_L0_ONLY", "PRODUCTION_CANDIDATE"}:
        raise ValueError("invalid evidence mode")
    if require_production and mode != "PRODUCTION_CANDIDATE":
        raise ValueError("--production requires production evidence mode")
    if witness.get("source_inventory_scope") != inventory["scope"]:
        raise ValueError("source inventory scope drift")
    if witness.get("fixed_h0") != 2:
        raise ValueError("witness must remain on fixed h0=2")
    if witness.get("phase_semantics") != "NOT_APPLICABLE_STRUCTURAL_EDGE":
        raise ValueError("structural edge must not claim a phase theorem")
    if witness.get("actual_active_support_claimed") is not False:
        raise ValueError("local-edge witness cannot promote active support")
    if witness.get("canonical_minimal_representation_claimed") is not False:
        raise ValueError("local-edge witness cannot promote canonical minimality")
    if witness.get("claim_boundary") != WITNESS_CLAIM_BOUNDARY:
        raise ValueError("witness claim boundary drift or undeclared promotion")
    normalization = witness.get("physical_normalization")
    if not isinstance(normalization, str) or not normalization:
        raise ValueError("physical normalization is required")

    covered = witness.get("covered_cut_addresses")
    edges = witness.get("edges")
    if not isinstance(covered, list) or not covered:
        raise ValueError("covered cut-address list must be nonempty")
    if not isinstance(edges, list) or not edges:
        raise ValueError("local edge list must be nonempty")

    covered_keys = [address_tuple(value) for value in covered]
    if len(covered_keys) != len(set(covered_keys)):
        raise ValueError("covered cut addresses must be unique")

    claims = qualifying_claim_map(inventory)
    edge_ids: set[str] = set()
    occurrence_ids: set[str] = set()
    sums = {key: Fraction(0, 1) for key in covered_keys}
    branching = {key: 0 for key in covered_keys}

    for edge in edges:
        if not isinstance(edge, dict) or set(edge) != EDGE_FIELDS:
            raise ValueError("edge must contain exactly the declared fields")
        address = edge.get("source_cut_address")
        if not isinstance(address, dict):
            raise ValueError("edge source address missing")
        key = address_tuple(address)
        if key not in sums:
            raise ValueError("edge source address is outside declared local cover")
        occurrence_id = edge.get("actual_occurrence_id")
        if not isinstance(occurrence_id, str) or not occurrence_id:
            raise ValueError("actual occurrence id is required")
        expected_id = stable_edge_id(address, occurrence_id)
        if edge.get("edge_id") != expected_id:
            raise ValueError("edge id is not the canonical address-occurrence identity")
        if expected_id in edge_ids or occurrence_id in occurrence_ids:
            raise ValueError("edge and occurrence identities must be unique")
        edge_ids.add(expected_id)
        occurrence_ids.add(occurrence_id)

        if edge.get("h0") != 2:
            raise ValueError("edge h0 drift")
        if edge.get("physical_normalization") != normalization:
            raise ValueError("edge normalization drift")
        if edge.get("actual_active_support_claimed") is not False:
            raise ValueError("edge active-support promotion")
        if edge.get("canonical_minimal_representation_claimed") is not False:
            raise ValueError("edge canonical-minimality promotion")

        weight = edge.get("exact_edge_weight")
        if not isinstance(weight, dict):
            raise ValueError("exact edge weight missing")
        sums[key] += exact_fraction(weight)
        branching[key] += 1

        source = edge.get("source_evidence")
        if not isinstance(source, dict) or set(source) != SOURCE_EVIDENCE_FIELDS:
            raise ValueError("source evidence must contain exactly the declared fields")
        if not source.get("derivation_ast"):
            raise ValueError("source derivation AST missing")

        if mode == "PRODUCTION_CANDIDATE":
            if edge.get("carrier_semantics") != "ACTUAL_LOCAL_OCCURRENCE_EDGE":
                raise ValueError("production edge lacks actual local occurrence semantics")
            if edge.get("support_semantics") != "SOURCE_BACKED_LOCAL_SUPPORT_ONLY":
                raise ValueError("production support semantics drift")
            claim_id = source.get("source_claim_id")
            if claim_id not in claims:
                raise ValueError("production source claim is not qualifying in TPC-173")
            claim = claims[claim_id]
            if source.get("source_path") != claim["source_path"]:
                raise ValueError("production source path drift")
            if source.get("canonical_utf8_lf_sha256") != claim[
                "canonical_utf8_lf_sha256"
            ]:
                raise ValueError("production source hash drift")
            if source.get("theorem_locator") != claim["theorem_locator"]:
                raise ValueError("production theorem locator drift")
            if source.get("formula_locator") != claim["formula_locator"]:
                raise ValueError("production formula locator drift")
            if source.get("derivation_ast") != claim["derivation_ast"]:
                raise ValueError("production derivation AST drift")
        else:
            if edge.get("carrier_semantics") != "SYNTHETIC_TYPED_LOCAL_EDGE_ONLY":
                raise ValueError("synthetic carrier semantics drift")
            if edge.get("support_semantics") != "SYNTHETIC_LOCAL_SUPPORT_ONLY":
                raise ValueError("synthetic support semantics drift")
            if source.get("source_claim_id") != "SYNTHETIC_AXIOM_L0":
                raise ValueError("synthetic source id drift")
            for key_name in (
                "source_path",
                "canonical_utf8_lf_sha256",
                "theorem_locator",
                "formula_locator",
            ):
                if source.get(key_name) is not None:
                    raise ValueError("synthetic fixture cannot carry production source locks")

    if any(count == 0 for count in branching.values()):
        raise ValueError("every covered cut address needs at least one local edge")
    if any(total != 1 for total in sums.values()):
        raise ValueError("each covered cut column must sum exactly to one")

    return {
        "status": (
            "PASS_PRODUCTION_CANDIDATE"
            if mode == "PRODUCTION_CANDIDATE"
            else "PASS_SYNTHETIC_L0_ONLY"
        ),
        "evidence_mode": mode,
        "covered_cut_count": len(covered_keys),
        "edge_count": len(edges),
        "unique_occurrence_count": len(occurrence_ids),
        "branching_counts": {
            "|".join(str(item) for item in key): branching[key]
            for key in sorted(branching)
        },
        "every_column_sum": "1",
        "fixed_h0": 2,
        "physical_normalization": normalization,
        "actual_active_support_proved": False,
        "canonical_minimal_representation_proved": False,
        "external_theorem_truth_proved_by_verifier": False,
    }


def build_synthetic() -> dict[str, Any]:
    address = {"ell": 3, "k": 171, "native_d": 1, "jL": 1, "jK": 7}

    def edge(occurrence_id: str, numerator: int, denominator: int) -> dict[str, Any]:
        return {
            "edge_id": stable_edge_id(address, occurrence_id),
            "source_cut_address": address,
            "actual_occurrence_id": occurrence_id,
            "exact_edge_weight": {
                "numerator": numerator,
                "denominator": denominator,
            },
            "h0": 2,
            "physical_normalization": "nu_X",
            "carrier_semantics": "SYNTHETIC_TYPED_LOCAL_EDGE_ONLY",
            "support_semantics": "SYNTHETIC_LOCAL_SUPPORT_ONLY",
            "actual_active_support_claimed": False,
            "canonical_minimal_representation_claimed": False,
            "source_evidence": {
                "source_claim_id": "SYNTHETIC_AXIOM_L0",
                "source_path": None,
                "canonical_utf8_lf_sha256": None,
                "theorem_locator": None,
                "formula_locator": None,
                "derivation_ast": {
                    "op": "synthetic_two_child_local_fiber",
                    "inputs": ["TPC174.SYNTHETIC.NONVACUITY"],
                },
            },
        }

    return {
        "schema": SCHEMA_ID,
        "witness_id": "tpc174-synthetic-two-edge-local-fiber-v1",
        "evidence_mode": "SYNTHETIC_L0_ONLY",
        "source_inventory_scope": (
            "FROZEN_CONTIGUOUS_OCCURRENCE_SOURCE_CORRIDOR_TPC133_172"
        ),
        "fixed_h0": 2,
        "physical_normalization": "nu_X",
        "phase_semantics": "NOT_APPLICABLE_STRUCTURAL_EDGE",
        "covered_cut_addresses": [address],
        "edges": [
            edge("synthetic-occurrence-a", 1, 3),
            edge("synthetic-occurrence-b", 2, 3),
        ],
        "actual_active_support_claimed": False,
        "canonical_minimal_representation_claimed": False,
        "claim_boundary": copy.deepcopy(WITNESS_CLAIM_BOUNDARY),
    }


def expect_rejected(
    witness: dict[str, Any],
    inventory: dict[str, Any],
    *,
    require_production: bool = False,
) -> bool:
    try:
        validate_witness(witness, inventory, require_production=require_production)
    except ValueError:
        return True
    return False


def build_production_join_fixture(
    synthetic: dict[str, Any], inventory: dict[str, Any]
) -> tuple[dict[str, Any], dict[str, Any]]:
    """Build a verifier-only fixture for exercising the production join.

    TPC-173 currently has no qualifying claims.  This local harness marks one
    copied record qualifying solely to prove that the unmutated production
    join is accepted and that a later AST mutation is rejected for the
    intended reason.  It is never written as production evidence.
    """

    joined_inventory = copy.deepcopy(inventory)
    claim = copy.deepcopy(joined_inventory["claim_inventory"][0])
    claim["qualification_pass"] = True
    joined_inventory["claim_inventory"] = [claim]

    witness = copy.deepcopy(synthetic)
    witness["witness_id"] = "tpc174-verifier-only-production-join-fixture-v1"
    witness["evidence_mode"] = "PRODUCTION_CANDIDATE"
    for edge in witness["edges"]:
        edge["carrier_semantics"] = "ACTUAL_LOCAL_OCCURRENCE_EDGE"
        edge["support_semantics"] = "SOURCE_BACKED_LOCAL_SUPPORT_ONLY"
        edge["source_evidence"] = {
            "source_claim_id": claim["claim_id"],
            "source_path": claim["source_path"],
            "canonical_utf8_lf_sha256": claim["canonical_utf8_lf_sha256"],
            "theorem_locator": copy.deepcopy(claim["theorem_locator"]),
            "formula_locator": copy.deepcopy(claim["formula_locator"]),
            "derivation_ast": copy.deepcopy(claim["derivation_ast"]),
        }
    validate_witness(witness, joined_inventory, require_production=True)
    return witness, joined_inventory


def build() -> tuple[dict[str, Any], dict[str, Any], dict[str, Any]]:
    inventory = load_object(SOURCE_INVENTORY)
    source_audit = load_object(SOURCE_AUDIT)
    if source_audit.get("status") != "PASS":
        raise ValueError("TPC-173 source audit is not PASS")
    if inventory.get("qualifying_count") != len(inventory["qualifying_claim_ids"]):
        raise ValueError("TPC-173 qualifying count drift")
    if not SCHEMA.exists():
        raise ValueError("missing TPC-174 schema")

    synthetic = build_synthetic()
    synthetic_result = validate_witness(synthetic, inventory)

    contract = {
        "schema": "tpc-174-local-occurrence-edge-witness-contract-export-v1",
        "witness_schema": SCHEMA_ID,
        "source_inventory": {
            "path": rel(SOURCE_INVENTORY),
            "canonical_utf8_lf_sha256": canonical_hash(SOURCE_INVENTORY),
            "audit_path": rel(SOURCE_AUDIT),
            "audit_sha256": canonical_hash(SOURCE_AUDIT),
            "scope": inventory["scope"],
            "qualifying_count": inventory["qualifying_count"],
            "hash_semantics": "INTEGRITY_ONLY",
        },
        "schema_lock": {
            "path": rel(SCHEMA),
            "canonical_utf8_lf_sha256": canonical_hash(SCHEMA),
            "hash_mode": HASH_MODE,
        },
        "minimal_required_fields": {
            "witness": sorted(WITNESS_FIELDS),
            "edge": sorted(EDGE_FIELDS),
            "source_evidence": sorted(SOURCE_EVIDENCE_FIELDS),
        },
        "identity_rules": {
            "archive_address_is_not_occurrence_id": True,
            "edge_id": "SHA256_24_OF_ADDRESS_PLUS_ACTUAL_OCCURRENCE_ID",
            "edge_ids_unique": True,
            "actual_occurrence_ids_unique": True,
            "covered_cut_addresses_unique": True,
        },
        "completeness_checks": {
            "every_covered_cut_has_nonempty_edge_family": True,
            "every_edge_source_is_in_declared_local_cover": True,
            "every_cut_column_exact_sum": "1",
            "production_source_claim_must_be_tpc173_qualifying": True,
            "production_derivation_ast_must_exactly_match_tpc173": True,
            "fixed_h0_2_edgewise": True,
            "physical_normalization_edgewise": True,
            "root_edge_source_fields_are_closed": True,
            "complete_witness_claim_boundary_is_fixed_false": True,
        },
        "separated_roots": {
            "local_edge_support_semantics": "SOURCE_BACKED_LOCAL_SUPPORT_ONLY",
            "actual_active_support_claimed": False,
            "canonical_minimal_representation_claimed": False,
        },
        "verifier_theorem": {
            "status": "PROVED_L0_FINITE_INTERFACE",
            "soundness": (
                "acceptance implies exact typed local-cover consistency and "
                "per-cut conservation for the supplied records only"
            ),
            "external_theorem_truth_proved": False,
            "production_edge_existence_proved": False,
        },
        "production_status": {
            "status": "NOT_TESTABLE",
            "production_witness_present": False,
            "qualifying_source_claim_count": inventory["qualifying_count"],
            "reason": (
                "TPC-173 supplies no qualifying source claim from which a "
                "production local edge can be instantiated."
            ),
        },
        "synthetic_nonvacuity": {
            "path": rel(SAMPLE),
            "payload_sha256": payload_hash(synthetic),
            "validation": synthetic_result,
        },
        "claim_boundary": {
            "synthetic_fixture_is_production_evidence": False,
            "verifier_acceptance_proves_external_theorem": False,
            "production_local_occurrence_family_proved": False,
            "actual_active_support_proved": False,
            "canonical_minimal_representation_proved": False,
            "named_fixed_phase_theorem": False,
            "positive_fixed_X_L2": False,
            "strict_one_over_400": False,
            "prime_pair_lower_bound": False,
            "twin_prime_theorem": False,
        },
    }

    mutations: dict[str, bool] = {}

    missing_edge = copy.deepcopy(synthetic)
    missing_edge["edges"] = []
    mutations["reject_empty_edge_family"] = expect_rejected(missing_edge, inventory)

    duplicate_occurrence = copy.deepcopy(synthetic)
    duplicate_occurrence["edges"][1]["actual_occurrence_id"] = duplicate_occurrence[
        "edges"
    ][0]["actual_occurrence_id"]
    duplicate_occurrence["edges"][1]["edge_id"] = duplicate_occurrence["edges"][0][
        "edge_id"
    ]
    mutations["reject_duplicate_identity"] = expect_rejected(
        duplicate_occurrence, inventory
    )

    bad_sum = copy.deepcopy(synthetic)
    bad_sum["edges"][1]["exact_edge_weight"] = {"numerator": 1, "denominator": 2}
    mutations["reject_nonconservative_column"] = expect_rejected(bad_sum, inventory)

    h0_drift = copy.deepcopy(synthetic)
    h0_drift["edges"][0]["h0"] = 3
    mutations["reject_h0_drift"] = expect_rejected(h0_drift, inventory)

    normalization_drift = copy.deepcopy(synthetic)
    normalization_drift["edges"][0]["physical_normalization"] = "other_norm"
    mutations["reject_normalization_drift"] = expect_rejected(
        normalization_drift, inventory
    )

    active_promotion = copy.deepcopy(synthetic)
    active_promotion["edges"][0]["actual_active_support_claimed"] = True
    mutations["reject_active_support_promotion"] = expect_rejected(
        active_promotion, inventory
    )

    canonical_promotion = copy.deepcopy(synthetic)
    canonical_promotion["canonical_minimal_representation_claimed"] = True
    mutations["reject_canonical_minimality_promotion"] = expect_rejected(
        canonical_promotion, inventory
    )

    extra_root = copy.deepcopy(synthetic)
    extra_root["undeclared_root_field"] = False
    mutations["reject_undeclared_root_field"] = expect_rejected(extra_root, inventory)

    extra_edge = copy.deepcopy(synthetic)
    extra_edge["edges"][0]["undeclared_edge_field"] = False
    mutations["reject_undeclared_edge_field"] = expect_rejected(extra_edge, inventory)

    extra_source = copy.deepcopy(synthetic)
    extra_source["edges"][0]["source_evidence"]["undeclared_source_field"] = False
    mutations["reject_undeclared_source_field"] = expect_rejected(
        extra_source, inventory
    )

    for field in WITNESS_CLAIM_BOUNDARY:
        boundary_promotion = copy.deepcopy(synthetic)
        boundary_promotion["claim_boundary"][field] = True
        mutations[f"reject_claim_boundary_promotion__{field}"] = expect_rejected(
            boundary_promotion, inventory
        )

    production_join, joined_inventory = build_production_join_fixture(
        synthetic, inventory
    )
    ast_drift = copy.deepcopy(production_join)
    ast_drift["edges"][0]["source_evidence"]["derivation_ast"] = {
        "op": "fabricated_nonempty_ast"
    }
    mutations["reject_production_derivation_ast_drift"] = expect_rejected(
        ast_drift, joined_inventory, require_production=True
    )

    production_promotion = copy.deepcopy(synthetic)
    production_promotion["evidence_mode"] = "PRODUCTION_CANDIDATE"
    for edge in production_promotion["edges"]:
        edge["carrier_semantics"] = "ACTUAL_LOCAL_OCCURRENCE_EDGE"
        edge["support_semantics"] = "SOURCE_BACKED_LOCAL_SUPPORT_ONLY"
        edge["source_evidence"]["source_claim_id"] = (
            "S153.cut_to_shadow_basis_injection"
        )
        edge["source_evidence"]["source_path"] = (
            "papers/tpc-153-canonical-cut-occurrence-shadow/main.tex"
        )
        edge["source_evidence"]["canonical_utf8_lf_sha256"] = "0" * 64
        edge["source_evidence"]["theorem_locator"] = {
            "kind": "LATEX_LABEL",
            "value": "thm:shadow",
        }
        edge["source_evidence"]["formula_locator"] = {
            "kind": "LATEX_LABEL",
            "value": "eq:shadow",
        }
    mutations["reject_shadow_source_as_production_edge"] = expect_rejected(
        production_promotion, inventory, require_production=True
    )

    if not all(mutations.values()):
        raise ValueError("TPC-174 mutation regression failed")

    audit = {
        "schema": "tpc-174-local-occurrence-edge-witness-contract-audit-v1",
        "status": "PASS",
        "contract_sha256": payload_hash(contract),
        "checks": {
            "tpc173_source_lock_verified": True,
            "tpc173_scope_preserved": True,
            "tpc173_qualifying_count": inventory["qualifying_count"],
            "synthetic_fixture_passes": True,
            "synthetic_fixture_is_one_to_many": synthetic_result["edge_count"] == 2,
            "synthetic_fixture_is_not_production": True,
            "production_witness_present": False,
            "production_status_not_testable": True,
            "active_support_root_separated": True,
            "canonical_minimality_root_separated": True,
            "strict_root_edge_source_fields": True,
            "production_derivation_ast_exact_join": True,
            "all_witness_claim_boundary_fields_locked": True,
        },
        "mutation_regressions": mutations,
        "claim_boundary": contract["claim_boundary"],
    }
    return synthetic, contract, audit


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
    parser.add_argument("--witness", type=Path)
    parser.add_argument("--production", action="store_true")
    args = parser.parse_args()

    inventory = load_object(SOURCE_INVENTORY)
    if args.witness is not None:
        witness = load_object(args.witness.resolve())
        result = validate_witness(
            witness, inventory, require_production=args.production
        )
        print(canonical_json(result), end="")
        return
    if args.production:
        raise SystemExit("--production requires --witness")

    synthetic, contract, audit = build()
    write_or_check(SAMPLE, synthetic, args.check)
    write_or_check(CONTRACT, contract, args.check)
    write_or_check(AUDIT, audit, args.check)
    mode = "checked" if args.check else "wrote"
    print(
        f"{mode} TPC-174: synthetic_edges={len(synthetic['edges'])} "
        f"tpc173_qualifying={contract['source_inventory']['qualifying_count']} "
        f"production={contract['production_status']['status']}"
    )


if __name__ == "__main__":
    main()
