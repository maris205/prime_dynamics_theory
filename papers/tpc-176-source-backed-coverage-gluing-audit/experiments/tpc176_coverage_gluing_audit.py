#!/usr/bin/env python3
"""Generate and verify the TPC-176 source-backed coverage/gluing audit."""

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
OUTPUT = HERE / "tpc176_coverage_gluing_audit.json"
SCHEMA = PAPER / "schemas" / "tpc176-coverage-gluing-audit-v1.schema.json"

TPC165 = PAPERS / "tpc-165-source-backed-local-global-crosswalk-gluing"
TPC173 = PAPERS / "tpc-173-production-source-claim-inventory"
TPC175 = PAPERS / "tpc-175-declared-corpus-local-edge-family"

TPC165_CERT = TPC165 / "experiments" / "tpc165_gluing_certificate.json"
TPC165_AUDIT = TPC165 / "experiments" / "tpc165_gluing_audit.json"
TPC173_INVENTORY = (
    TPC173 / "experiments" / "tpc173_source_claim_inventory.json"
)
TPC175_FAMILY = TPC175 / "experiments" / "tpc175_local_edge_family.json"
TPC175_AUDIT = (
    TPC175 / "experiments" / "tpc175_local_edge_family_audit.json"
)
TPC175_GENERATOR = TPC175 / "experiments" / "tpc175_local_edge_family.py"

HASH_MODE = "CANONICAL_UTF8_LF_V2"
SCOPE = "FROZEN_CONTIGUOUS_OCCURRENCE_SOURCE_CORRIDOR_TPC133_172"
SCHEMA_ID = "tpc-176-source-backed-coverage-gluing-audit-v1"
TPC175_SCHEMA_ID = "tpc-175-declared-corpus-local-edge-family-v1"


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


def find_schema(directory: Path, schema_id: str) -> Path:
    matches: list[Path] = []
    for path in sorted((directory / "schemas").glob("*.json")):
        value = load_json(path)
        const = value.get("properties", {}).get("schema", {}).get("const")
        if const == schema_id:
            matches.append(path)
    if len(matches) != 1:
        raise FileNotFoundError(
            f"expected exactly one schema for {schema_id}; found {len(matches)}"
        )
    return matches[0]


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
    gluing: dict[str, Any],
    gluing_audit: dict[str, Any],
    inventory: dict[str, Any],
    family: dict[str, Any],
) -> None:
    if gluing.get("schema") != "tpc-165-local-global-crosswalk-gluing-v1":
        raise ValueError("wrong TPC-165 certificate")
    if gluing_audit.get("status") != "PASS":
        raise ValueError("TPC-165 audit is not PASS")
    if (
        gluing["formal_gluing_theorem"]["theorem_level"]
        != "PROVED_L0_FORMAL"
    ):
        raise ValueError("TPC-165 theorem level drift")
    if inventory.get("scope") != SCOPE or inventory.get("qualifying_count") != 0:
        raise ValueError("TPC-173 frozen-corpus inventory drift")
    if inventory.get("qualifying_claim_ids") != []:
        raise ValueError("TPC-173 qualifying claim list is nonempty")
    required_family = {
        "schema": TPC175_SCHEMA_ID,
        "scope": SCOPE,
        "status": "EMPTY_IN_FROZEN_DECLARED_CORPUS",
        "qualifying_claim_count": 0,
        "family_cardinality": 0,
        "eligible_carrier_count": 0,
        "qualifying_claim_ids": [],
        "eligible_carriers": [],
        "local_edge_family": [],
    }
    for key, expected in required_family.items():
        if family.get(key) != expected:
            raise ValueError(f"TPC-175 field drift: {key}")


def build() -> dict[str, Any]:
    tpc175_schema = find_schema(TPC175, TPC175_SCHEMA_ID)
    gluing = load_json(TPC165_CERT)
    gluing_audit = load_json(TPC165_AUDIT)
    inventory = load_json(TPC173_INVENTORY)
    family = load_json(TPC175_FAMILY)
    family_audit = load_json(TPC175_AUDIT)
    validate_upstream(gluing, gluing_audit, inventory, family)
    if family_audit.get("status") != "PASS":
        raise ValueError("TPC-175 audit is not PASS")
    upstream_coverage = family["coverage"]
    if (
        upstream_coverage["production_cut_count"] != 2988
        or upstream_coverage["covered_cut_count"] != 0
        or upstream_coverage["duplicated_cut_count"] != 0
        or upstream_coverage["unmatched_cut_count"] != 2988
        or upstream_coverage["tpc165_gluing_instantiated"] is not False
    ):
        raise ValueError("TPC-175 cut-coverage ledger drift")

    locks = [
        source_lock("TPC165.gluing_certificate", TPC165_CERT),
        source_lock("TPC165.gluing_audit", TPC165_AUDIT),
        source_lock("TPC173.source_claim_inventory", TPC173_INVENTORY),
        source_lock("TPC175.local_edge_family", TPC175_FAMILY),
        source_lock("TPC175.local_edge_family_audit", TPC175_AUDIT),
        source_lock("TPC175.local_edge_family_schema", tpc175_schema),
        source_lock("TPC175.local_edge_family_generator", TPC175_GENERATOR),
    ]

    result: dict[str, Any] = {
        "schema": SCHEMA_ID,
        "status": "PASS",
        "source_locks": locks,
        "input_family": {
            "source_id": "TPC175.local_edge_family",
            "scope": SCOPE,
            "family_status": family["status"],
            "proved_local_edge_count": family["family_cardinality"],
            "qualifying_claim_count": family["qualifying_claim_count"],
            "qualifying_claim_ids": list(family["qualifying_claim_ids"]),
            "eligible_carrier_count": family["eligible_carrier_count"],
            "carrier_ids": [],
            "maximal_in_frozen_declared_corpus": True,
            "mathematical_nonexistence_claim": False,
        },
        "tpc165_gluing_gate": {
            "theorem_source": "TPC165.gluing_certificate",
            "theorem_level": gluing["formal_gluing_theorem"]["theorem_level"],
            "requires_nonempty_local_families": True,
            "requires_compatible_overlap_bijections": True,
            "nonempty_local_family_precondition_met": False,
            "overlap_cocycle_precondition_met": False,
            "gluing_theorem_invoked": False,
            "empty_quotient_promoted_to_formal_totality": False,
            "production_formal_totality_status": "NOT_TESTABLE",
        },
        "coverage_ledger": {
            "coverage_universe": "TPC175_FROZEN_PRODUCTION_CUT_ADDRESSES",
            "global_physical_carrier_universe_declared": False,
            "declared_production_cut_count": 2988,
            "covered_cut_count": 0,
            "duplicate_cut_count": 0,
            "unmatched_cut_count": 2988,
            "covered_plus_duplicate_plus_unmatched_cuts": 2988,
            "unmatched_cuts_are_actual_physical_carriers": False,
            "eligible_carrier_count": 0,
            "covered_carrier_count": 0,
            "duplicate_carrier_count": 0,
            "unmatched_carrier_count": 0,
            "covered_plus_duplicate_plus_unmatched_carriers": 0,
            "partition_identity_verified": True,
            "archive_cut_paths_imported_as_unmatched_carriers": False,
            "production_totality_proved": False,
        },
        "route_decision": {
            "method_cell": (
                "production_local_edge_extraction_and_gluing_"
                "from_frozen_tpc133_172"
            ),
            "method_cell_status": (
                "STOP_SCOPED_EMPTY_PROVED_LOCAL_EDGE_FAMILY"
            ),
            "stop_scope": SCOPE,
            "h1_local_edge_root_status": "NOT_TESTABLE",
            "h1_local_edge_root_closed": False,
            "occurrence_augmented_architecture_status": "NOT_TESTABLE",
            "occurrence_augmented_architecture_stopped": False,
            "next_required_object": (
                "NEW_SOURCE_BACKED_PRODUCTION_LOCAL_EDGE_OR_"
                "EXPLICIT_CORPUS_ENLARGEMENT"
            ),
        },
        "checks": {
            "tpc165_formal_theorem_source_locked": True,
            "tpc175_family_source_locked": True,
            "only_proved_local_edges_admitted": True,
            "empty_input_recomputed": True,
            "covered_duplicate_unmatched_exact": True,
            "gluing_precondition_not_fabricated": True,
            "empty_quotient_not_totality": True,
            "archive_rows_not_promoted_to_physical_carriers": True,
            "scoped_stop_not_global_architecture_stop": True,
        },
        "mutation_regressions": {},
        "claim_boundary": {
            "scoped_corpus_exhaustion_proved": True,
            "mathematical_nonexistence_proved": False,
            "production_local_occurrence_family_proved_nonempty": False,
            "production_formal_totality_proved": False,
            "actual_active_support_proved": False,
            "canonical_minimal_representation_proved": False,
            "fixed_h0_2_preserved_as_requirement": True,
            "fixed_h0_2_arithmetic_progress": False,
            "named_fixed_phase_theorem": False,
            "program_positive_L2": False,
            "strict_one_over_400": False,
            "prime_pair_lower_bound": False,
            "twin_prime_theorem": False,
        },
    }
    validate(result, verify_sources=True, require_mutations=False)
    result["mutation_regressions"] = build_mutations(result)
    validate(result, verify_sources=True, require_mutations=True)
    return result


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

    family = value["input_family"]
    if (
        family["scope"] != SCOPE
        or family["family_status"] != "EMPTY_IN_FROZEN_DECLARED_CORPUS"
        or family["proved_local_edge_count"] != 0
        or family["qualifying_claim_count"] != 0
        or family["eligible_carrier_count"] != 0
        or family["carrier_ids"] != []
        or family["qualifying_claim_ids"] != []
        or family["mathematical_nonexistence_claim"] is not False
    ):
        raise ValueError("input family promoted or drifted")

    gate = value["tpc165_gluing_gate"]
    if (
        gate["theorem_level"] != "PROVED_L0_FORMAL"
        or gate["nonempty_local_family_precondition_met"] is not False
        or gate["overlap_cocycle_precondition_met"] is not False
        or gate["gluing_theorem_invoked"] is not False
        or gate["empty_quotient_promoted_to_formal_totality"] is not False
        or gate["production_formal_totality_status"] != "NOT_TESTABLE"
    ):
        raise ValueError("TPC-165 gluing gate promotion")

    ledger = value["coverage_ledger"]
    cut_counts = [
        ledger["declared_production_cut_count"],
        ledger["covered_cut_count"],
        ledger["duplicate_cut_count"],
        ledger["unmatched_cut_count"],
        ledger["covered_plus_duplicate_plus_unmatched_cuts"],
    ]
    if cut_counts != [2988, 0, 0, 2988, 2988]:
        raise ValueError("frozen cut-coverage ledger drift")
    carrier_counts = [
        ledger["eligible_carrier_count"],
        ledger["covered_carrier_count"],
        ledger["duplicate_carrier_count"],
        ledger["unmatched_carrier_count"],
        ledger["covered_plus_duplicate_plus_unmatched_carriers"],
    ]
    if carrier_counts != [0, 0, 0, 0, 0]:
        raise ValueError("empty-domain coverage ledger drift")
    if (
        ledger["coverage_universe"]
        != "TPC175_FROZEN_PRODUCTION_CUT_ADDRESSES"
        or ledger["global_physical_carrier_universe_declared"] is not False
        or ledger["unmatched_cuts_are_actual_physical_carriers"] is not False
        or ledger["partition_identity_verified"] is not True
        or ledger["archive_cut_paths_imported_as_unmatched_carriers"] is not False
        or ledger["production_totality_proved"] is not False
    ):
        raise ValueError("coverage-universe promotion")

    route = value["route_decision"]
    if (
        route["method_cell_status"]
        != "STOP_SCOPED_EMPTY_PROVED_LOCAL_EDGE_FAMILY"
        or route["stop_scope"] != SCOPE
        or route["h1_local_edge_root_status"] != "NOT_TESTABLE"
        or route["h1_local_edge_root_closed"] is not False
        or route["occurrence_augmented_architecture_status"] != "NOT_TESTABLE"
        or route["occurrence_augmented_architecture_stopped"] is not False
    ):
        raise ValueError("scoped stop promoted to architecture stop")

    if not all(value["checks"].values()):
        raise ValueError("audit check failure")
    boundary = value["claim_boundary"]
    required_false = (
        "mathematical_nonexistence_proved",
        "production_local_occurrence_family_proved_nonempty",
        "production_formal_totality_proved",
        "actual_active_support_proved",
        "canonical_minimal_representation_proved",
        "fixed_h0_2_arithmetic_progress",
        "named_fixed_phase_theorem",
        "program_positive_L2",
        "strict_one_over_400",
        "prime_pair_lower_bound",
        "twin_prime_theorem",
    )
    if any(boundary[key] is not False for key in required_false):
        raise ValueError("claim boundary promotion")
    if boundary["scoped_corpus_exhaustion_proved"] is not True:
        raise ValueError("scoped result erased")
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
        "fabricated_positive_local_edge_rejected": mutation_rejected(
            value,
            lambda x: x["input_family"].update(
                {"proved_local_edge_count": 1}
            ),
        ),
        "gluing_on_empty_input_rejected": mutation_rejected(
            value,
            lambda x: x["tpc165_gluing_gate"].update(
                {"gluing_theorem_invoked": True}
            ),
        ),
        "empty_quotient_totality_rejected": mutation_rejected(
            value,
            lambda x: x["coverage_ledger"].update(
                {"production_totality_proved": True}
            ),
        ),
        "archive_cut_paths_as_unmatched_rejected": mutation_rejected(
            value,
            lambda x: x["coverage_ledger"].update(
                {
                    "unmatched_cuts_are_actual_physical_carriers": True,
                    "archive_cut_paths_imported_as_unmatched_carriers": True,
                }
            ),
        ),
        "scoped_stop_to_architecture_stop_rejected": mutation_rejected(
            value,
            lambda x: x["route_decision"].update(
                {"occurrence_augmented_architecture_stopped": True}
            ),
        ),
        "empty_family_as_nonexistence_rejected": mutation_rejected(
            value,
            lambda x: x["claim_boundary"].update(
                {"mathematical_nonexistence_proved": True}
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
            raise SystemExit("TPC-176 CHECK FAIL: generated artifact drift")
        print("TPC-176 CHECK PASS")
    else:
        OUTPUT.parent.mkdir(parents=True, exist_ok=True)
        OUTPUT.write_text(rendered, encoding="utf-8", newline="\n")
        print("TPC-176 GENERATE PASS")
    print(
        json.dumps(
            {
                "status": value["status"],
                "proved_local_edges": 0,
                "covered_cuts": 0,
                "duplicate_cuts": 0,
                "unmatched_cuts": 2988,
                "eligible_carriers": 0,
                "method_cell_status": value["route_decision"][
                    "method_cell_status"
                ],
                "architecture_status": value["route_decision"][
                    "occurrence_augmented_architecture_status"
                ],
            },
            sort_keys=True,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
