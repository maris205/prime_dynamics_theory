#!/usr/bin/env python3
"""Generate and verify the TPC-178 representation-eligibility audit."""

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
OUTPUT = HERE / "tpc178_representation_audit.json"
SCHEMA = PAPER / "schemas" / "tpc178-representation-audit-v1.schema.json"

TPC164_CERT = (
    PAPERS
    / "tpc-164-minimal-archived-separation-key"
    / "experiments"
    / "tpc164_minimal_key_certificate.json"
)
TPC164_AUDIT = (
    PAPERS
    / "tpc-164-minimal-archived-separation-key"
    / "experiments"
    / "tpc164_minimal_key_audit.json"
)
TPC166_DECISION = (
    PAPERS
    / "tpc-166-refined-h1-crosswalk-frontier-decision"
    / "experiments"
    / "tpc166_refined_h1_frontier.json"
)
TPC175_FAMILY = (
    PAPERS
    / "tpc-175-declared-corpus-local-edge-family"
    / "experiments"
    / "tpc175_local_edge_family.json"
)
TPC177_AUDIT = (
    PAPERS
    / "tpc-177-actual-active-support-vacuity-firewall"
    / "experiments"
    / "tpc177_active_support_audit.json"
)

HASH_MODE = "CANONICAL_UTF8_LF_V2"
SCOPE = "FROZEN_CONTIGUOUS_OCCURRENCE_SOURCE_CORRIDOR_TPC133_172"
SCHEMA_ID = "tpc-178-canonical-minimal-representation-audit-v1"
H1_NODE = "H1.canonical_minimal_representation_certificate"
ARCHIVE_KEY = ["ell", "k", "native_d", "jL", "jK"]


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


def validate_upstream(
    archive: dict[str, Any],
    archive_audit: dict[str, Any],
    decision: dict[str, Any],
    family: dict[str, Any],
    support: dict[str, Any],
) -> None:
    if (
        archive.get("schema")
        != "tpc-164-minimal-archived-separation-key-v1"
        or archive["selected_archived_key"] != ARCHIVE_KEY
        or archive["exhaustive_search"]["row_count"] != 2988
        or archive["exhaustive_search"]["minimum_cardinality"] != 5
        or archive["exhaustive_search"]["minimum_key_count"] != 1
    ):
        raise ValueError("TPC-164 archive-key theorem drift")
    if archive_audit.get("status") != "PASS":
        raise ValueError("TPC-164 audit is not PASS")
    if H1_NODE not in decision["minimal_not_testable_root_antichain"]:
        raise ValueError("TPC-166 representation root missing")
    if (
        family.get("scope") != SCOPE
        or family.get("eligible_carrier_count") != 0
        or family.get("eligible_carriers") != []
        or family.get("local_edge_family") != []
    ):
        raise ValueError("TPC-175 eligible carrier drift")
    if (
        support.get("schema")
        != "tpc-177-actual-active-support-vacuity-audit-v1"
        or support.get("status") != "PASS"
        or support["eligible_domain"]["eligible_carrier_count"] != 0
        or support["h1_active_support_root"]["status"] != "NOT_TESTABLE"
        or support["vacuity_firewall"]["status"]
        != "VACUOUS_EMPTY_ELIGIBLE_DOMAIN"
    ):
        raise ValueError("TPC-177 vacuity firewall drift")


def build() -> dict[str, Any]:
    archive = load_json(TPC164_CERT)
    archive_audit = load_json(TPC164_AUDIT)
    decision = load_json(TPC166_DECISION)
    family = load_json(TPC175_FAMILY)
    support = load_json(TPC177_AUDIT)
    validate_upstream(archive, archive_audit, decision, family, support)

    value: dict[str, Any] = {
        "schema": SCHEMA_ID,
        "status": "PASS",
        "source_locks": [
            source_lock("TPC164.minimal_key_certificate", TPC164_CERT),
            source_lock("TPC164.minimal_key_audit", TPC164_AUDIT),
            source_lock("TPC166.refined_h1_frontier", TPC166_DECISION),
            source_lock("TPC175.local_edge_family", TPC175_FAMILY),
            source_lock("TPC177.active_support_audit", TPC177_AUDIT),
        ],
        "eligible_domain": {
            "scope": SCOPE,
            "source": "TPC175.local_edge_family",
            "eligibility_rule": (
                "SOURCE_BACKED_ACTUAL_OCCURRENCE_CARRIER_REQUIRED"
            ),
            "eligible_physical_carrier_count": 0,
            "eligible_physical_carrier_ids": [],
            "physical_representation_class_count": 0,
        },
        "archive_key_import": {
            "source": "TPC164.minimal_key_certificate",
            "selected_key": ARCHIVE_KEY,
            "frozen_archive_row_count": 2988,
            "minimum_field_cardinality": 5,
            "unique_minimum_separating_key": True,
            "role": "ARCHIVE_ADDRESS",
            "occurrence_identifier": False,
            "physical_parent_identifier": False,
            "physical_equivalence_class_selector": False,
            "canonical_physical_representation": False,
            "minimal_physical_representation": False,
        },
        "representation_contract": {
            "required_objects": [
                "source_backed_eligible_actual_carrier",
                "nonempty_physical_representation_space",
                "source_locked_physical_equivalence_relation",
                "literal_contribution_invariance_theorem",
                "canonical_selector_or_minimality_functional",
                "existence_theorem",
                "uniqueness_or_attained_minimum_theorem",
                "literal_coefficient_fixed_h0_normalization_lineage",
            ],
            "all_required_objects_present": False,
            "archive_injectivity_satisfies_contract": False,
        },
        "representation_audit": {
            "status": "ELIGIBILITY_BLOCKED_EMPTY_CARRIER_DOMAIN",
            "eligible_carriers_tested": 0,
            "representation_classes_tested": 0,
            "canonical_representatives_proved": 0,
            "minimal_representatives_proved": 0,
            "noncanonical_counterexamples_proved": 0,
            "zero_counterexamples_promoted_to_canonicality": False,
            "canonicality_proved": False,
            "minimality_proved": False,
            "noncanonicality_proved": False,
            "mathematical_nonexistence_proved": False,
        },
        "h1_representation_root": {
            "node_id": H1_NODE,
            "status": "NOT_TESTABLE",
            "closed": False,
            "reason": (
                "NO_SOURCE_BACKED_ELIGIBLE_CARRIER_OR_"
                "PHYSICAL_REPRESENTATION_CLASS"
            ),
            "archive_key_does_not_close_root": True,
        },
        "checks": {
            "tpc164_archive_key_source_locked": True,
            "archive_key_role_preserved": True,
            "eligible_carrier_domain_source_locked": True,
            "representation_contract_explicit": True,
            "empty_domain_not_canonicality": True,
            "zero_counterexamples_not_positive_certificate": True,
            "h1_representation_root_remains_not_testable": True,
            "fixed_h0_lineage_not_fabricated": True,
        },
        "mutation_regressions": {},
        "claim_boundary": {
            "archive_row_separation_proved": True,
            "actual_occurrence_identifier_proved": False,
            "actual_active_support_proved": False,
            "canonical_minimal_representation_proved": False,
            "noncanonical_physical_counterexample_proved": False,
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
        or domain["eligible_physical_carrier_count"] != 0
        or domain["eligible_physical_carrier_ids"] != []
        or domain["physical_representation_class_count"] != 0
    ):
        raise ValueError("representation eligibility fabricated")

    key = value["archive_key_import"]
    if (
        key["selected_key"] != ARCHIVE_KEY
        or key["frozen_archive_row_count"] != 2988
        or key["minimum_field_cardinality"] != 5
        or key["unique_minimum_separating_key"] is not True
        or key["role"] != "ARCHIVE_ADDRESS"
    ):
        raise ValueError("archive-key theorem drift")
    forbidden_key_promotions = (
        "occurrence_identifier",
        "physical_parent_identifier",
        "physical_equivalence_class_selector",
        "canonical_physical_representation",
        "minimal_physical_representation",
    )
    if any(key[field] is not False for field in forbidden_key_promotions):
        raise ValueError("archive key promoted to physical representation")

    contract = value["representation_contract"]
    if (
        contract["all_required_objects_present"] is not False
        or contract["archive_injectivity_satisfies_contract"] is not False
        or len(contract["required_objects"]) != 8
    ):
        raise ValueError("representation contract promoted")

    audit = value["representation_audit"]
    counts = [
        audit["eligible_carriers_tested"],
        audit["representation_classes_tested"],
        audit["canonical_representatives_proved"],
        audit["minimal_representatives_proved"],
        audit["noncanonical_counterexamples_proved"],
    ]
    if counts != [0, 0, 0, 0, 0]:
        raise ValueError("empty representation ledger drift")
    if audit["status"] != "ELIGIBILITY_BLOCKED_EMPTY_CARRIER_DOMAIN":
        raise ValueError("wrong representation audit status")
    audit_false = (
        "zero_counterexamples_promoted_to_canonicality",
        "canonicality_proved",
        "minimality_proved",
        "noncanonicality_proved",
        "mathematical_nonexistence_proved",
    )
    if any(audit[field] is not False for field in audit_false):
        raise ValueError("empty representation audit promoted")

    root = value["h1_representation_root"]
    if (
        root["node_id"] != H1_NODE
        or root["status"] != "NOT_TESTABLE"
        or root["closed"] is not False
        or root["archive_key_does_not_close_root"] is not True
    ):
        raise ValueError("H1 representation root promotion")

    if not all(value["checks"].values()):
        raise ValueError("audit check failure")
    boundary = value["claim_boundary"]
    required_false = (
        "actual_occurrence_identifier_proved",
        "actual_active_support_proved",
        "canonical_minimal_representation_proved",
        "noncanonical_physical_counterexample_proved",
        "fixed_h0_2_arithmetic_progress",
        "named_fixed_phase_theorem",
        "program_positive_L2",
        "strict_one_over_400",
        "prime_pair_lower_bound",
        "twin_prime_theorem",
    )
    if any(boundary[field] is not False for field in required_false):
        raise ValueError("claim boundary promotion")
    if boundary["archive_row_separation_proved"] is not True:
        raise ValueError("TPC-164 archive theorem erased")
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
                {"eligible_physical_carrier_count": 1}
            ),
        ),
        "archive_key_as_occurrence_id_rejected": mutation_rejected(
            value,
            lambda x: x["archive_key_import"].update(
                {"occurrence_identifier": True}
            ),
        ),
        "archive_key_as_physical_canonical_rejected": mutation_rejected(
            value,
            lambda x: x["archive_key_import"].update(
                {"canonical_physical_representation": True}
            ),
        ),
        "zero_counterexamples_as_canonicality_rejected": mutation_rejected(
            value,
            lambda x: x["representation_audit"].update(
                {
                    "zero_counterexamples_promoted_to_canonicality": True,
                    "canonicality_proved": True,
                }
            ),
        ),
        "h1_root_proved_promotion_rejected": mutation_rejected(
            value,
            lambda x: x["h1_representation_root"].update(
                {"status": "PROVED", "closed": True}
            ),
        ),
        "fixed_h0_progress_promotion_rejected": mutation_rejected(
            value,
            lambda x: x["claim_boundary"].update(
                {"fixed_h0_2_arithmetic_progress": True}
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
            raise SystemExit("TPC-178 CHECK FAIL: generated artifact drift")
        print("TPC-178 CHECK PASS")
    else:
        OUTPUT.parent.mkdir(parents=True, exist_ok=True)
        OUTPUT.write_text(rendered, encoding="utf-8", newline="\n")
        print("TPC-178 GENERATE PASS")
    print(
        json.dumps(
            {
                "status": value["status"],
                "eligible_carriers": 0,
                "representation_status": value["representation_audit"][
                    "status"
                ],
                "h1_representation_root": value["h1_representation_root"][
                    "status"
                ],
                "archive_key_role": value["archive_key_import"]["role"],
            },
            sort_keys=True,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
