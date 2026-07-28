#!/usr/bin/env python3
"""Generate and verify the TPC-177 active-support vacuity firewall."""

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
OUTPUT = HERE / "tpc177_active_support_audit.json"
SCHEMA = PAPER / "schemas" / "tpc177-active-support-audit-v1.schema.json"

TPC166_DECISION = (
    PAPERS
    / "tpc-166-refined-h1-crosswalk-frontier-decision"
    / "experiments"
    / "tpc166_refined_h1_frontier.json"
)
TPC171_MANIFEST = (
    PAPERS
    / "tpc-171-source-locked-occurrence-phase-return-integration"
    / "experiments"
    / "tpc171_integration_manifest.json"
)
TPC175_FAMILY = (
    PAPERS
    / "tpc-175-declared-corpus-local-edge-family"
    / "experiments"
    / "tpc175_local_edge_family.json"
)
TPC176_AUDIT = (
    PAPERS
    / "tpc-176-source-backed-coverage-gluing-audit"
    / "experiments"
    / "tpc176_coverage_gluing_audit.json"
)

HASH_MODE = "CANONICAL_UTF8_LF_V2"
SCOPE = "FROZEN_CONTIGUOUS_OCCURRENCE_SOURCE_CORRIDOR_TPC133_172"
SCHEMA_ID = "tpc-177-actual-active-support-vacuity-audit-v1"
H1_NODE = "H1.actual_active_support_certificate"
H9_NODE = "H9.literal_weight_registry"


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


def node_by_id(manifest: dict[str, Any], node_id: str) -> dict[str, Any]:
    matches = [node for node in manifest["nodes"] if node["node_id"] == node_id]
    if len(matches) != 1:
        raise ValueError(f"expected exactly one node {node_id}")
    return matches[0]


def validate_upstream(
    decision: dict[str, Any],
    manifest: dict[str, Any],
    family: dict[str, Any],
    coverage: dict[str, Any],
) -> dict[str, Any]:
    antichain = decision["minimal_not_testable_root_antichain"]
    if H1_NODE not in antichain:
        raise ValueError("TPC-166 active-support root missing")
    h9 = node_by_id(manifest, H9_NODE)
    if (
        h9["status"] != "NOT_TESTABLE"
        or h9["role"] != "PHYSICAL_REGISTRY"
        or h9["quantifier_signature"]["decay_axis"] != "NONE"
    ):
        raise ValueError("TPC-171 literal-weight registry drift")
    if (
        family.get("scope") != SCOPE
        or family.get("family_cardinality") != 0
        or family.get("eligible_carrier_count") != 0
        or family.get("qualifying_claim_ids") != []
    ):
        raise ValueError("TPC-175 eligible family drift")
    ledger = coverage["coverage_ledger"]
    if (
        coverage.get("schema")
        != "tpc-176-source-backed-coverage-gluing-audit-v1"
        or coverage.get("status") != "PASS"
        or ledger["eligible_carrier_count"] != 0
        or ledger["covered_carrier_count"] != 0
        or ledger["duplicate_carrier_count"] != 0
        or ledger["unmatched_carrier_count"] != 0
        or ledger["production_totality_proved"] is not False
    ):
        raise ValueError("TPC-176 coverage ledger drift")
    return h9


def build() -> dict[str, Any]:
    decision = load_json(TPC166_DECISION)
    manifest = load_json(TPC171_MANIFEST)
    family = load_json(TPC175_FAMILY)
    coverage = load_json(TPC176_AUDIT)
    h9 = validate_upstream(decision, manifest, family, coverage)

    value: dict[str, Any] = {
        "schema": SCHEMA_ID,
        "status": "PASS",
        "source_locks": [
            source_lock("TPC166.refined_h1_frontier", TPC166_DECISION),
            source_lock("TPC171.integration_manifest", TPC171_MANIFEST),
            source_lock("TPC175.local_edge_family", TPC175_FAMILY),
            source_lock("TPC176.coverage_gluing_audit", TPC176_AUDIT),
        ],
        "eligible_domain": {
            "scope": SCOPE,
            "source": "TPC176.coverage_gluing_audit",
            "eligibility_rule": (
                "SOURCE_BACKED_PROVED_LOCAL_EDGE_CARRIER_ONLY"
            ),
            "eligible_carrier_count": 0,
            "eligible_carrier_ids": [],
            "formal_archive_rows_admitted": False,
            "synthetic_carriers_admitted": False,
        },
        "coefficient_audit": {
            "required_record_fields": [
                "eligible_carrier_id",
                "literal_target_expression_locator",
                "literal_physical_coefficient",
                "physical_normalization",
                "nonzero_proof_locator",
            ],
            "tested_eligible_carrier_count": 0,
            "nonzero_literal_coefficient_count": 0,
            "zero_literal_coefficient_count": 0,
            "missing_coefficient_record_count": 0,
            "classified_total": 0,
            "partition_identity_verified": True,
            "universal_all_eligible_carriers_active": True,
            "universal_statement_is_vacuous": True,
        },
        "vacuity_firewall": {
            "status": "VACUOUS_EMPTY_ELIGIBLE_DOMAIN",
            "universal_statement_true": True,
            "existential_active_support_witness_count": 0,
            "existential_active_support_proved": False,
            "empty_domain_promoted_to_existence": False,
            "mathematical_nonexistence_proved": False,
        },
        "h1_active_support_root": {
            "node_id": H1_NODE,
            "status": "NOT_TESTABLE",
            "closed": False,
            "support_semantics": "ACTUAL_ACTIVE_SUPPORT",
            "reason": (
                "NO_SOURCE_BACKED_ELIGIBLE_CARRIER; "
                "EMPTY_DOMAIN_UNIVERSAL_HAS_NO_EXISTENTIAL_CONTENT"
            ),
        },
        "h9_literal_weight_separation": {
            "node_id": H9_NODE,
            "source_status": h9["status"],
            "registry_role": h9["role"],
            "decay_axis": h9["quantifier_signature"]["decay_axis"],
            "imported_as_h1_support_evidence": False,
            "consumed_by_tpc177": False,
            "logically_identical_to_h1_active_support_root": False,
            "registry_identification_creates_decay": False,
            "registry_closed_by_tpc177": False,
        },
        "checks": {
            "eligible_domain_source_locked": True,
            "no_formal_or_synthetic_carrier_admitted": True,
            "coefficient_partition_recomputed": True,
            "empty_domain_vacuity_explicit": True,
            "existential_witness_not_fabricated": True,
            "h1_root_remains_not_testable": True,
            "h1_h9_roles_disjoint": True,
            "h9_decay_axis_none_preserved": True,
        },
        "mutation_regressions": {},
        "claim_boundary": {
            "empty_domain_audit_passed": True,
            "actual_active_support_proved": False,
            "active_carrier_mathematical_nonexistence_proved": False,
            "production_local_occurrence_family_proved_nonempty": False,
            "h9_literal_weight_registry_closed": False,
            "fixed_h0_2_preserved_as_requirement": True,
            "fixed_h0_2_arithmetic_progress": False,
            "named_fixed_phase_theorem": False,
            "program_positive_L2": False,
            "strict_one_over_400": False,
            "prime_pair_lower_bound": False,
            "twin_prime_theorem": False,
        },
    }
    validate(value, verify_sources=True, require_mutations=False)
    value["mutation_regressions"] = build_mutations(value)
    validate(value, verify_sources=True, require_mutations=True)
    return value


def validate(
    value: dict[str, Any],
    *,
    verify_sources: bool,
    require_mutations: bool = True,
) -> None:
    schema = load_json(SCHEMA)
    if set(value) != set(schema["properties"]):
        raise ValueError("strict top-level schema mismatch")
    if value["schema"] != SCHEMA_ID or value["status"] != "PASS":
        raise ValueError("schema or status drift")
    if verify_sources:
        validate_source_locks(value["source_locks"])

    domain = value["eligible_domain"]
    if (
        domain["scope"] != SCOPE
        or domain["eligible_carrier_count"] != 0
        or domain["eligible_carrier_ids"] != []
        or domain["formal_archive_rows_admitted"] is not False
        or domain["synthetic_carriers_admitted"] is not False
    ):
        raise ValueError("eligible-domain fabrication")

    audit = value["coefficient_audit"]
    counts = [
        audit["tested_eligible_carrier_count"],
        audit["nonzero_literal_coefficient_count"],
        audit["zero_literal_coefficient_count"],
        audit["missing_coefficient_record_count"],
        audit["classified_total"],
    ]
    if counts != [0, 0, 0, 0, 0]:
        raise ValueError("empty coefficient ledger drift")
    if (
        audit["partition_identity_verified"] is not True
        or audit["universal_all_eligible_carriers_active"] is not True
        or audit["universal_statement_is_vacuous"] is not True
    ):
        raise ValueError("vacuity classification drift")

    firewall = value["vacuity_firewall"]
    if (
        firewall["status"] != "VACUOUS_EMPTY_ELIGIBLE_DOMAIN"
        or firewall["universal_statement_true"] is not True
        or firewall["existential_active_support_witness_count"] != 0
        or firewall["existential_active_support_proved"] is not False
        or firewall["empty_domain_promoted_to_existence"] is not False
        or firewall["mathematical_nonexistence_proved"] is not False
    ):
        raise ValueError("vacuity firewall failure")

    root = value["h1_active_support_root"]
    if (
        root["node_id"] != H1_NODE
        or root["status"] != "NOT_TESTABLE"
        or root["closed"] is not False
        or root["support_semantics"] != "ACTUAL_ACTIVE_SUPPORT"
    ):
        raise ValueError("H1 active-support promotion")

    h9 = value["h9_literal_weight_separation"]
    if (
        h9["node_id"] != H9_NODE
        or h9["source_status"] != "NOT_TESTABLE"
        or h9["registry_role"] != "PHYSICAL_REGISTRY"
        or h9["decay_axis"] != "NONE"
        or h9["imported_as_h1_support_evidence"] is not False
        or h9["consumed_by_tpc177"] is not False
        or h9["logically_identical_to_h1_active_support_root"] is not False
        or h9["registry_identification_creates_decay"] is not False
        or h9["registry_closed_by_tpc177"] is not False
    ):
        raise ValueError("H1/H9 separation failure")

    if not all(value["checks"].values()):
        raise ValueError("audit check failure")
    boundary = value["claim_boundary"]
    required_false = (
        "actual_active_support_proved",
        "active_carrier_mathematical_nonexistence_proved",
        "production_local_occurrence_family_proved_nonempty",
        "h9_literal_weight_registry_closed",
        "fixed_h0_2_arithmetic_progress",
        "named_fixed_phase_theorem",
        "program_positive_L2",
        "strict_one_over_400",
        "prime_pair_lower_bound",
        "twin_prime_theorem",
    )
    if any(boundary[key] is not False for key in required_false):
        raise ValueError("claim boundary promotion")
    if boundary["empty_domain_audit_passed"] is not True:
        raise ValueError("valid empty-domain audit erased")
    if require_mutations and (
        not value["mutation_regressions"]
        or not all(value["mutation_regressions"].values())
    ):
        raise ValueError("mutation regression failure")


def mutation_rejected(
    value: dict[str, Any],
    mutate: Callable[[dict[str, Any]], None],
    *,
    verify_sources: bool = False,
) -> bool:
    clone = copy.deepcopy(value)
    mutate(clone)
    try:
        validate(clone, verify_sources=verify_sources, require_mutations=False)
    except (KeyError, TypeError, ValueError):
        return True
    return False


def build_mutations(value: dict[str, Any]) -> dict[str, bool]:
    return {
        "fabricated_eligible_carrier_rejected": mutation_rejected(
            value,
            lambda x: x["eligible_domain"].update(
                {"eligible_carrier_count": 1}
            ),
        ),
        "fabricated_nonzero_coefficient_rejected": mutation_rejected(
            value,
            lambda x: x["coefficient_audit"].update(
                {"nonzero_literal_coefficient_count": 1}
            ),
        ),
        "vacuity_to_existence_rejected": mutation_rejected(
            value,
            lambda x: x["vacuity_firewall"].update(
                {"existential_active_support_proved": True}
            ),
        ),
        "h1_root_proved_promotion_rejected": mutation_rejected(
            value,
            lambda x: x["h1_active_support_root"].update(
                {"status": "PROVED", "closed": True}
            ),
        ),
        "implicit_h9_import_rejected": mutation_rejected(
            value,
            lambda x: x["h9_literal_weight_separation"].update(
                {"imported_as_h1_support_evidence": True}
            ),
        ),
        "h9_decay_creation_rejected": mutation_rejected(
            value,
            lambda x: x["h9_literal_weight_separation"].update(
                {
                    "decay_axis": "FIXED_X_POWER_FIXED_ATOM",
                    "registry_identification_creates_decay": True,
                }
            ),
        ),
        "program_L2_promotion_rejected": mutation_rejected(
            value,
            lambda x: x["claim_boundary"].update(
                {"program_positive_L2": True}
            ),
        ),
        "source_hash_drift_rejected": mutation_rejected(
            value,
            lambda x: x["source_locks"][0].update(
                {"canonical_utf8_lf_sha256": "0" * 64}
            ),
            verify_sources=True,
        ),
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()
    value = build()
    rendered = canonical_json(value)
    if args.check:
        if (
            not OUTPUT.is_file()
            or normalize_lf(OUTPUT.read_text(encoding="utf-8")) != rendered
        ):
            raise SystemExit("TPC-177 CHECK FAIL: generated artifact drift")
        print("TPC-177 CHECK PASS")
    else:
        OUTPUT.parent.mkdir(parents=True, exist_ok=True)
        OUTPUT.write_text(rendered, encoding="utf-8", newline="\n")
        print("TPC-177 GENERATE PASS")
    print(
        json.dumps(
            {
                "status": value["status"],
                "eligible_carriers": 0,
                "active_support_root": value["h1_active_support_root"][
                    "status"
                ],
                "vacuity_status": value["vacuity_firewall"]["status"],
                "h9_decay_axis": value["h9_literal_weight_separation"][
                    "decay_axis"
                ],
            },
            sort_keys=True,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
