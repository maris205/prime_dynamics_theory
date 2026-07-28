#!/usr/bin/env python3
"""Build the TPC-173 frozen production source-claim inventory.

The inventory is deliberately closed-world.  It reviews every theorem-bearing
main.tex in the contiguous TPC-133--172 occurrence/source corridor and keeps
the machine-readable production/status substrate separate from theorem
evidence.  A zero qualifying count is therefore a statement about this exact
declared corpus, never a mathematical nonexistence assertion.
"""

from __future__ import annotations

import argparse
import copy
import hashlib
import json
from collections import Counter
from pathlib import Path
from typing import Any


HERE = Path(__file__).resolve().parent
PAPER = HERE.parent
PAPERS = PAPER.parent
REPO = PAPERS.parent

INVENTORY = HERE / "tpc173_source_claim_inventory.json"
AUDIT = HERE / "tpc173_source_claim_inventory_audit.json"
SCHEMA = PAPER / "schemas" / "tpc173-production-source-claim-inventory-v1.schema.json"

HASH_MODE = "CANONICAL_UTF8_LF_V2"
SCHEMA_ID = "tpc-173-production-source-claim-inventory-v1"
SCOPE_ID = "FROZEN_CONTIGUOUS_OCCURRENCE_SOURCE_CORRIDOR_TPC133_172"

QUALIFICATION_REQUIREMENTS = (
    "SOURCE_PATH_AND_CANONICAL_HASH",
    "RESOLVING_THEOREM_LOCATOR",
    "RESOLVING_FORMULA_LOCATOR",
    "NONEMPTY_DERIVATION_AST",
    "ACTUAL_LOCAL_OCCURRENCE_EDGE_CONCLUSION",
    "FIVE_FIELD_PRODUCTION_CUT_ADDRESS",
    "EXACT_EDGE_WEIGHT",
    "FIXED_H0_EQUALS_2_LINEAGE",
    "PHYSICAL_NORMALIZATION_LINEAGE",
)

REVIEWED_NO_CANDIDATE = {
    137: "prime-square logarithmic arithmetic theorem; no cut-to-occurrence conclusion",
    138: "shift-one firewall theorem; no cut-to-occurrence conclusion",
    139: "growing affine-uniformity diagram; no cut-to-occurrence conclusion",
    140: "exceptional-scale selector gate; no cut-to-occurrence conclusion",
    147: "periodic residue reassembly; no local occurrence producer statement",
    148: "quotient Mobius fiber lift; no production cut-address occurrence edge",
    157: "literal-weight approximation; consumes a future physical registry",
    158: "additive-phase major/minor gate; no structural local occurrence edge",
    159: "dyadic shadow-prefix arithmetic lifting; no structural local occurrence edge",
    160: "exceptional-variation Abel return; consumes rather than creates a registry",
}


def candidate(
    paper: int,
    claim_id: str,
    theorem_label: str | None,
    formula_label: str | None,
    carrier: str,
    conclusion_type: str,
    derivation_op: str,
    gaps: list[str],
    *,
    production_cut_address: list[str] | None = None,
    exact_edge_weight: dict[str, int] | None = None,
    fixed_h0: int | None = None,
    physical_normalization: str | None = None,
) -> dict[str, Any]:
    return {
        "paper": paper,
        "claim_id": claim_id,
        "theorem_locator": (
            {"kind": "LATEX_LABEL", "value": theorem_label}
            if theorem_label is not None
            else None
        ),
        "formula_locator": (
            {"kind": "LATEX_LABEL", "value": formula_label}
            if formula_label is not None
            else None
        ),
        "carrier": carrier,
        "conclusion_type": conclusion_type,
        "derivation_ast": {"op": derivation_op, "inputs": [f"TPC-{paper}"]},
        "production_cut_address": production_cut_address,
        "exact_edge_weight": exact_edge_weight,
        "fixed_h0": fixed_h0,
        "physical_normalization": physical_normalization,
        "qualification_gaps": gaps,
    }


CANDIDATE_SPECS: list[dict[str, Any]] = [
    candidate(
        133,
        "S133.executable_native_entrance",
        "thm:generator",
        "eq:coefficient",
        "NATIVE_ATOM_ARCHIVE",
        "NATIVE_SOURCE_ENUMERATION",
        "enumerate_native_atoms",
        ["NO_DOWNSTREAM_OCCURRENCE_ROW", "NO_LOCAL_OCCURRENCE_EDGE"],
        fixed_h0=2,
        physical_normalization="nu_X",
    ),
    candidate(
        134,
        "S134.boundary_complete_path_conservation",
        "thm:archive",
        None,
        "DYADIC_PATH_ARCHIVE",
        "CUT_PRECURSOR_CONSERVATION",
        "dyadic_path_expansion",
        [
            "NO_FORMULA_LOCATOR",
            "NO_DOWNSTREAM_OCCURRENCE_ROW",
            "NO_LOCAL_OCCURRENCE_EDGE",
        ],
        fixed_h0=2,
        physical_normalization="nu_X",
    ),
    candidate(
        135,
        "S135.eligible_frontier_decomposition",
        "thm:partition",
        "eq:geometry",
        "FRONTIER_CLASSIFICATION",
        "CUT_CLASSIFICATION_ONLY",
        "classify_cut_frontier",
        ["NO_DOWNSTREAM_OCCURRENCE_ROW", "NO_LOCAL_OCCURRENCE_EDGE"],
        fixed_h0=2,
        physical_normalization="nu_X",
    ),
    candidate(
        136,
        "S136.complete_native_cut_archive",
        "thm:cut",
        None,
        "NONSOFT_CUT_ARCHIVE",
        "CUT_ARCHIVE_ONLY",
        "compose_cut_archive",
        [
            "NO_FORMULA_LOCATOR",
            "NO_DOWNSTREAM_OCCURRENCE_ROW",
            "NO_LOCAL_OCCURRENCE_EDGE",
        ],
        production_cut_address=["ell", "k", "native_d", "jL", "jK"],
        fixed_h0=2,
        physical_normalization="nu_X",
    ),
    candidate(
        141,
        "D141.source_locked_non_escalating_merge",
        "thm:merge",
        "eq:cut",
        "INTEGRATION_MANIFEST",
        "CONDITIONAL_INTEGRATION_INTERFACE",
        "merge_source_locked_exports",
        ["NO_ACTUAL_LOCAL_OCCURRENCE_CONCLUSION", "NO_PRODUCTION_EDGE_ROWS"],
    ),
    candidate(
        142,
        "D142.mvp4_route_decision",
        "thm:decision",
        "eq:synthesis",
        "ROUTE_DECISION",
        "NOT_TESTABLE_STATUS",
        "classify_route",
        ["CONCLUSION_IS_STATUS_NOT_EDGE", "NO_PRODUCTION_EDGE_ROWS"],
    ),
    candidate(
        143,
        "D143.audited_occurrence_lift_verdict",
        "thm:verdict",
        "eq:conservation",
        "OCCURRENCE_LIFT_CONTRACT",
        "NOT_TESTABLE_STATUS",
        "audit_missing_occurrence_lift",
        ["CONCLUSION_EXPLICITLY_NOT_TESTABLE", "NO_PRODUCTION_EDGE_ROWS"],
        production_cut_address=["ell", "k", "native_d", "jL", "jK"],
        fixed_h0=2,
        physical_normalization="nu_X",
    ),
    candidate(
        144,
        "S144.simultaneous_quotient_lift",
        "thm:kernel",
        "eq:kernels",
        "ASSUMED_OCCURRENCE_SPACE",
        "ABSTRACT_CONDITIONAL_QUOTIENT_THEOREM",
        "compare_quotient_kernels",
        [
            "ASSUMES_OCCURRENCE_SPACE",
            "NO_PRODUCTION_CUT_ADDRESS",
            "NO_PRODUCTION_EDGE_ROWS",
        ],
    ),
    candidate(
        145,
        "S145.row_separated_commuting_square",
        "thm:pathwise",
        "eq:square",
        "ASSUMED_ROW_SEPARATED_OCCURRENCE_LIFT",
        "ABSTRACT_CONDITIONAL_COMMUTATION_THEOREM",
        "test_edgewise_shift_preservation",
        [
            "ASSUMES_OCCURRENCE_LIFT",
            "NO_PRODUCTION_CUT_ADDRESS",
            "NO_PRODUCTION_EDGE_ROWS",
        ],
        fixed_h0=2,
    ),
    candidate(
        146,
        "S146.four_map_completion_criterion",
        "thm:criterion",
        "eq:zero",
        "ASSUMED_COMPLETE_OCCURRENCE_REGISTRY",
        "ABSTRACT_CONDITIONAL_COMPLETION_THEOREM",
        "test_zero_defect_vector",
        [
            "ASSUMES_LITERAL_SOURCE_MATRICES",
            "ASSUMES_COMPLETE_OCCURRENCE_REGISTRY",
            "NO_PRODUCTION_EDGE_ROWS",
        ],
    ),
    candidate(
        149,
        "A149.actual_determinant_two_core_corridor",
        "thm:main",
        "eq:main",
        "ACTUAL_DETERMINANT_TWO_CORE",
        "ARITHMETIC_CORE_THEOREM",
        "bound_core_mobius_correlation",
        [
            "NO_FIVE_FIELD_CUT_ADDRESS",
            "NO_CUT_TO_OCCURRENCE_EDGE",
            "NO_EDGE_WEIGHT_OR_LINEAGE",
        ],
        fixed_h0=2,
    ),
    candidate(
        150,
        "D150.actual_corridor_selector_ledger",
        "thm:log-ledger",
        "eq:log-ledger",
        "ACTUAL_CORE_SELECTOR_LEDGER",
        "CONDITIONAL_ARITHMETIC_INTERFACE",
        "audit_selector_ledger",
        ["OCCURRENCE_LIFT_REMAINS_MISSING", "NO_CUT_TO_OCCURRENCE_EDGE"],
        fixed_h0=2,
    ),
    candidate(
        151,
        "D151.source_locked_frontier_merge",
        "thm:status",
        "eq:quotient",
        "FRONTIER_INTEGRATION_DAG",
        "NOT_TESTABLE_STATUS",
        "merge_frontier_interfaces",
        ["FIRST_MISSING_IS_OCCURRENCE_LIFT", "NO_PRODUCTION_EDGE_ROWS"],
    ),
    candidate(
        152,
        "D152.mvp5_route_decision",
        "thm:decision",
        None,
        "ROUTE_DECISION",
        "NOT_TESTABLE_STATUS",
        "classify_route",
        [
            "NO_FORMULA_LOCATOR",
            "FIRST_MISSING_IS_OCCURRENCE_LIFT",
            "NO_PRODUCTION_EDGE_ROWS",
        ],
    ),
    candidate(
        153,
        "S153.cut_to_shadow_basis_injection",
        "thm:shadow",
        "eq:shadow",
        "PARTIAL_CUT_OCCURRENCE_SHADOW",
        "PROVED_L1_STRUCTURAL_SHADOW_ONLY",
        "basis_injection",
        ["SHADOW_ROW_IS_NOT_ACTUAL_OCCURRENCE"],
        production_cut_address=["ell", "k", "native_d", "jL", "jK"],
        exact_edge_weight={"numerator": 1, "denominator": 1},
        fixed_h0=2,
        physical_normalization="nu_X",
    ),
    candidate(
        153,
        "S153.shadow_column_conservation",
        "thm:shadow",
        "eq:shadow-conservation",
        "PARTIAL_CUT_OCCURRENCE_SHADOW",
        "PROVED_L1_STRUCTURAL_SHADOW_ONLY",
        "column_sum",
        ["SHADOW_ROW_IS_NOT_ACTUAL_OCCURRENCE"],
        production_cut_address=["ell", "k", "native_d", "jL", "jK"],
        exact_edge_weight={"numerator": 1, "denominator": 1},
        fixed_h0=2,
        physical_normalization="nu_X",
    ),
    candidate(
        154,
        "S154.formal_completion_fiber_nonuniqueness",
        "thm:nonunique",
        "eq:column",
        "FORMAL_COMPLETION_FIBER",
        "FORMAL_ONLY_SCOPED_OBSTRUCTION",
        "construct_two_formal_completions",
        ["FORMAL_CHILDREN_ARE_NOT_ACTUAL_OCCURRENCES", "NO_PRODUCTION_EDGE_ROWS"],
    ),
    candidate(
        154,
        "S154.current_artifacts_only_recovery_obstruction",
        "thm:obstruction",
        "eq:column",
        "CURRENT_SCHEMA_ONLY",
        "FORMAL_ONLY_SCOPED_OBSTRUCTION",
        "fiber_nonidentifiability",
        ["OBSTRUCTION_SCOPE_IS_CURRENT_ARTIFACTS_ONLY", "NO_PRODUCTION_EDGE_ROWS"],
    ),
    candidate(
        155,
        "S155.verifier_internal_soundness",
        "thm:soundness",
        "eq:induced-map",
        "SUPPLIED_OCCURRENCE_WITNESS",
        "CONDITIONAL_VERIFIER_THEOREM",
        "verify_supplied_bundle",
        [
            "PRODUCTION_WITNESS_ABSENT",
            "EXTERNAL_THEOREM_TRUTH_NOT_PROVED_BY_VERIFIER",
            "NO_PRODUCTION_EDGE_ROWS",
        ],
    ),
    candidate(
        156,
        "D156.h1_crosswalk_contract",
        "thm:h1",
        "eq:column-conservation",
        "TRUSTED_CROSSWALK_CONTRACT",
        "CONDITIONAL_ROUTE_INTERFACE",
        "evaluate_crosswalk_contract",
        ["TRUSTED_PRODUCTION_CROSSWALK_ABSENT", "NO_PRODUCTION_EDGE_ROWS"],
    ),
    candidate(
        161,
        "D161.occurrence_return_integration",
        "thm:integration",
        "eq:h1",
        "INTEGRATION_DAG",
        "NOT_TESTABLE_STATUS",
        "integrate_occurrence_and_return",
        ["CROSSWALK_REMAINS_UNAVAILABLE", "NO_PRODUCTION_EDGE_ROWS"],
    ),
    candidate(
        162,
        "D162.mvp6_route_decision",
        "thm:mvp6",
        "eq:current-blockers",
        "ROUTE_DECISION",
        "NOT_TESTABLE_STATUS",
        "classify_route",
        ["FIRST_MISSING_IS_CROSSWALK", "NO_PRODUCTION_EDGE_ROWS"],
    ),
    candidate(
        163,
        "S163.frozen_source_edge_census",
        "thm:census",
        "eq:zero-edges",
        "FROZEN_TPC153_154_155_156_161_162_CORPUS",
        "SCOPED_EMPTY_CENSUS",
        "count_source_locator_admissible_claims",
        ["CONCLUSION_IS_SCOPED_ZERO_COUNT_NOT_EDGE", "NO_PRODUCTION_EDGE_ROWS"],
    ),
    candidate(
        164,
        "S164.unique_minimal_archive_address",
        "thm:minimal-key",
        "eq:min-key",
        "FROZEN_CUT_ARCHIVE",
        "ARCHIVE_ADDRESS_ONLY",
        "exhaust_field_subsets",
        [
            "ADDRESS_IS_NOT_OCCURRENCE_ID",
            "NO_ACTUAL_OCCURRENCE_CONCLUSION",
            "NO_EDGE_WEIGHT",
        ],
        production_cut_address=["ell", "k", "native_d", "jL", "jK"],
    ),
    candidate(
        165,
        "S165.compatible_local_family_gluing",
        "thm:gluing",
        "eq:matrix-conservation",
        "SUPPLIED_FORMAL_LOCAL_FAMILIES",
        "PROVED_L0_FORMAL_CONDITIONAL",
        "quotient_compatible_local_rows",
        [
            "LOCAL_FAMILIES_ARE_HYPOTHESES",
            "FORMAL_ROWS_NOT_ACTUAL_OCCURRENCES",
            "PRODUCTION_LOCAL_FAMILY_ABSENT",
        ],
    ),
    candidate(
        166,
        "D166.three_factor_crosswalk_contract",
        "thm:antichain",
        "eq:antichain",
        "CROSSWALK_SUBDAG",
        "L1_STRUCTURAL_FRONTIER",
        "compute_minimal_unresolved_roots",
        ["LOCAL_EDGE_FAMILY_IS_UNRESOLVED_ROOT", "NO_PRODUCTION_EDGE_ROWS"],
    ),
    candidate(
        167,
        "A167.direct_additive_twist_phase_L2",
        "thm:parseval",
        "eq:parseval",
        "ACTUAL_DETERMINANT_TWO_CORE",
        "L1_PHASE_METRIC_ARITHMETIC",
        "parseval_in_phase",
        ["NO_FIVE_FIELD_CUT_ADDRESS", "NO_CUT_TO_OCCURRENCE_EDGE"],
        fixed_h0=2,
    ),
    candidate(
        168,
        "A168.actual_core_registry_density",
        "thm:sampling",
        "eq:sampling",
        "SEPARATED_PHASE_REGISTRY",
        "L1_PHASE_METRIC_ARITHMETIC",
        "finite_phase_sampling",
        ["NO_FIVE_FIELD_CUT_ADDRESS", "NO_CUT_TO_OCCURRENCE_EDGE"],
        fixed_h0=2,
    ),
    candidate(
        169,
        "A169.phase_maximal_all_prefix",
        "thm:core",
        "eq:core",
        "ACTUAL_DETERMINANT_TWO_CORE",
        "L1_PHASE_METRIC_ARITHMETIC",
        "maximal_parseval",
        ["NO_FIVE_FIELD_CUT_ADDRESS", "NO_CUT_TO_OCCURRENCE_EDGE"],
        fixed_h0=2,
    ),
    candidate(
        170,
        "A170.metric_packet_corridor",
        "thm:bc",
        "eq:summability",
        "EXPLICIT_ACTUAL_CORE_PACKET_CORRIDOR",
        "L1_PHASE_METRIC_ARITHMETIC",
        "borel_cantelli_packet_control",
        [
            "NO_FIVE_FIELD_CUT_ADDRESS",
            "NO_CUT_TO_OCCURRENCE_EDGE",
            "PHASE_IS_LEBESGUE_AE_NOT_NAMED_ATOM",
        ],
        fixed_h0=2,
    ),
    candidate(
        171,
        "D171.occurrence_phase_return_verdict",
        "thm:verdict",
        "eq:verdict",
        "INTEGRATED_ROUTE_DAG",
        "NOT_TESTABLE_STATUS",
        "integrate_source_locked_routes",
        ["FIRST_MISSING_IS_LOCAL_EDGE_FAMILY", "NO_PRODUCTION_EDGE_ROWS"],
    ),
    candidate(
        172,
        "D172.mvp7_route_decision",
        "thm:mvp7",
        "eq:mvp7",
        "ROUTE_DECISION",
        "NOT_TESTABLE_STATUS",
        "classify_route",
        ["FIRST_MISSING_IS_LOCAL_EDGE_FAMILY", "NO_PRODUCTION_EDGE_ROWS"],
    ),
]


DATA_STATUS_SUBSTRATE = (
    "papers/tpc-143-frontier-occurrence-lift-contract/samples/"
    "tpc143_frontier_lift_obligations.jsonl",
    "papers/tpc-153-canonical-cut-occurrence-shadow/experiments/"
    "tpc153_cut_occurrence_shadow_certificate.json",
    "papers/tpc-153-canonical-cut-occurrence-shadow/samples/"
    "tpc153_cut_occurrence_shadow.jsonl",
    "papers/tpc-154-conservative-completion-fiber-obstruction/experiments/"
    "tpc154_completion_fiber_obstruction_certificate.json",
    "papers/tpc-154-conservative-completion-fiber-obstruction/samples/"
    "tpc154_formal_completions.jsonl",
    "papers/tpc-155-theorem-backed-occurrence-witness-verifier/experiments/"
    "tpc155_occurrence_witness_audit.json",
    "papers/tpc-155-theorem-backed-occurrence-witness-verifier/samples/"
    "tpc155_production_witness_status.json",
    "papers/tpc-156-h1-occurrence-crosswalk-route-decision/experiments/"
    "tpc156_h1_occurrence_decision.json",
    "papers/tpc-161-source-locked-occurrence-return-integration/experiments/"
    "tpc161_occurrence_return_manifest.json",
    "papers/tpc-162-mvp6-actual-carrier-endpoint-route-decision/experiments/"
    "tpc162_mvp6_snapshot.json",
    "papers/tpc-163-source-locator-census-native-key-collision/experiments/"
    "tpc163_source_census.json",
    "papers/tpc-163-source-locator-census-native-key-collision/experiments/"
    "tpc163_source_census_audit.json",
    "papers/tpc-164-minimal-archived-separation-key/experiments/"
    "tpc164_minimal_key_certificate.json",
    "papers/tpc-164-minimal-archived-separation-key/experiments/"
    "tpc164_minimal_key_audit.json",
    "papers/tpc-165-source-backed-local-global-crosswalk-gluing/experiments/"
    "tpc165_gluing_certificate.json",
    "papers/tpc-165-source-backed-local-global-crosswalk-gluing/experiments/"
    "tpc165_gluing_audit.json",
    "papers/tpc-166-refined-h1-crosswalk-frontier-decision/experiments/"
    "tpc166_refined_h1_frontier.json",
    "papers/tpc-166-refined-h1-crosswalk-frontier-decision/experiments/"
    "tpc166_refined_h1_frontier_audit.json",
    "papers/tpc-171-source-locked-occurrence-phase-return-integration/experiments/"
    "tpc171_integration_manifest.json",
    "papers/tpc-171-source-locked-occurrence-phase-return-integration/experiments/"
    "tpc171_integration_audit.json",
    "papers/tpc-172-mvp7-occurrence-phase-atomic-route-decision/experiments/"
    "tpc172_mvp7_snapshot.json",
    "papers/tpc-172-mvp7-occurrence-phase-atomic-route-decision/experiments/"
    "tpc172_mvp7_route_audit.json",
)


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


def paper_dir(number: int) -> Path:
    matches = sorted(PAPERS.glob(f"tpc-{number}-*"))
    if len(matches) != 1:
        raise ValueError(f"expected one TPC-{number} directory, found {len(matches)}")
    return matches[0]


def label_resolves(text: str, locator: dict[str, str] | None) -> bool:
    if locator is None:
        return False
    return f"\\label{{{locator['value']}}}" in text


def qualification_pass(record: dict[str, Any]) -> bool:
    checks = record["qualification_checks"]
    return all(checks[name] for name in QUALIFICATION_REQUIREMENTS)


def validate_candidate(record: dict[str, Any]) -> None:
    if not record["claim_id"]:
        raise ValueError("empty claim id")
    if not record["derivation_ast"]:
        raise ValueError(f"empty derivation AST: {record['claim_id']}")
    if record["qualification_pass"] != qualification_pass(record):
        raise ValueError(f"qualification mismatch: {record['claim_id']}")
    if record["qualification_pass"] and record["qualification_gaps"]:
        raise ValueError(f"qualifying claim has gaps: {record['claim_id']}")
    if not record["qualification_pass"] and not record["qualification_gaps"]:
        raise ValueError(f"disqualified claim has no explicit gap: {record['claim_id']}")


def validate_inventory(value: dict[str, Any]) -> None:
    required = {
        "schema",
        "scope",
        "hash_mode",
        "hash_semantics",
        "theorem_corpus",
        "data_status_substrate",
        "qualification_contract",
        "corpus_partition",
        "claim_inventory",
        "qualifying_claim_ids",
        "qualifying_count",
        "max_defensible_family_status",
        "next_forced_object",
        "claim_boundary",
    }
    if set(value) != required:
        raise ValueError("inventory top-level contract drift")
    if (
        value["schema"] != SCHEMA_ID
        or value["scope"] != SCOPE_ID
        or value["hash_mode"] != HASH_MODE
        or value["hash_semantics"] != "INTEGRITY_ONLY"
    ):
        raise ValueError("inventory identity or hash semantics drift")
    corpus = value["theorem_corpus"]
    files = corpus["files"]
    if (
        corpus["first_paper"] != 133
        or corpus["last_paper"] != 172
        or corpus["file_count"] != 40
        or len(files) != 40
        or [row["paper"] for row in files] != list(range(133, 173))
    ):
        raise ValueError("declared theorem corpus drift")
    if any(
        row["hash_mode"] != HASH_MODE
        or row["hash_semantics"] != "INTEGRITY_ONLY"
        or not isinstance(row["canonical_utf8_lf_sha256"], str)
        or len(row["canonical_utf8_lf_sha256"]) != 64
        for row in files
    ):
        raise ValueError("theorem-file hash semantics drift")
    substrate = value["data_status_substrate"]
    if (
        substrate["role"] != "DOMAIN_AND_STATUS_ONLY"
        or substrate["artifact_count"] != len(substrate["artifacts"])
        or any(
            row["hash_semantics"]
            != "INTEGRITY_OR_STATUS_ONLY_NOT_THEOREM"
            for row in substrate["artifacts"]
        )
    ):
        raise ValueError("data/status substrate promoted to theorem evidence")
    for record in value["claim_inventory"]:
        validate_candidate(record)
        if (
            record["hash_mode"] != HASH_MODE
            or record["hash_semantics"] != "INTEGRITY_ONLY"
        ):
            raise ValueError("claim hash promoted to theorem evidence")
    counts = value["corpus_partition"]["file_disposition_counts"]
    if counts != {
        "MAPPED_DISQUALIFIED": 30,
        "REVIEWED_NO_CANDIDATE": 10,
        "NOT_MAPPED_YET": 0,
        "QUALIFYING": 0,
    }:
        raise ValueError("file partition drift")
    qualifying = [
        row["claim_id"]
        for row in value["claim_inventory"]
        if row["qualification_pass"]
    ]
    if (
        value["qualifying_claim_ids"] != qualifying
        or value["qualifying_count"] != len(qualifying)
        or qualifying
        or value["max_defensible_family_status"]
        != "EMPTY_IN_FROZEN_DECLARED_CORPUS"
    ):
        raise ValueError("qualifying family drift")
    expected_boundary = {
        "zero_means_mathematical_nonexistence": False,
        "production_local_occurrence_family_proved": False,
        "actual_active_support_proved": False,
        "canonical_minimal_representation_proved": False,
        "fixed_h0_2_preserved_as_requirement": True,
        "positive_fixed_X_L2": False,
        "strict_one_over_400": False,
        "prime_pair_lower_bound": False,
        "twin_prime_theorem": False,
    }
    if value["claim_boundary"] != expected_boundary:
        raise ValueError("claim boundary promotion")


def build() -> tuple[dict[str, Any], dict[str, Any]]:
    if not SCHEMA.exists():
        raise ValueError(f"missing schema: {SCHEMA}")

    candidates_by_paper: dict[int, list[dict[str, Any]]] = {}
    for spec in CANDIDATE_SPECS:
        candidates_by_paper.setdefault(int(spec["paper"]), []).append(copy.deepcopy(spec))

    theorem_files: list[dict[str, Any]] = []
    claim_inventory: list[dict[str, Any]] = []
    for number in range(133, 173):
        main = paper_dir(number) / "main.tex"
        text = normalize(main.read_text(encoding="utf-8"))
        paper_candidates = candidates_by_paper.get(number, [])
        if number in REVIEWED_NO_CANDIDATE:
            if paper_candidates:
                raise ValueError(f"TPC-{number} is both mapped and no-candidate")
            disposition = "REVIEWED_NO_CANDIDATE"
            review_note = REVIEWED_NO_CANDIDATE[number]
        elif paper_candidates:
            disposition = "MAPPED_DISQUALIFIED"
            review_note = "all occurrence-adjacent claims mapped; none meets the edge contract"
        else:
            disposition = "NOT_MAPPED_YET"
            review_note = "no completed claim-level review"

        theorem_files.append(
            {
                "paper": number,
                "path": rel(main),
                "canonical_utf8_lf_sha256": canonical_hash(main),
                "hash_mode": HASH_MODE,
                "hash_semantics": "INTEGRITY_ONLY",
                "disposition": disposition,
                "review_note": review_note,
                "mapped_claim_count": len(paper_candidates),
            }
        )

        for record in paper_candidates:
            theorem_ok = label_resolves(text, record["theorem_locator"])
            formula_ok = label_resolves(text, record["formula_locator"])
            checks = {
                "SOURCE_PATH_AND_CANONICAL_HASH": True,
                "RESOLVING_THEOREM_LOCATOR": theorem_ok,
                "RESOLVING_FORMULA_LOCATOR": formula_ok,
                "NONEMPTY_DERIVATION_AST": bool(record["derivation_ast"]),
                "ACTUAL_LOCAL_OCCURRENCE_EDGE_CONCLUSION": (
                    record["conclusion_type"] == "ACTUAL_LOCAL_OCCURRENCE_EDGE"
                ),
                "FIVE_FIELD_PRODUCTION_CUT_ADDRESS": (
                    record["production_cut_address"]
                    == ["ell", "k", "native_d", "jL", "jK"]
                ),
                "EXACT_EDGE_WEIGHT": record["exact_edge_weight"] is not None,
                "FIXED_H0_EQUALS_2_LINEAGE": record["fixed_h0"] == 2,
                "PHYSICAL_NORMALIZATION_LINEAGE": (
                    record["physical_normalization"] is not None
                ),
            }
            record.update(
                {
                    "source_path": rel(main),
                    "canonical_utf8_lf_sha256": canonical_hash(main),
                    "hash_mode": HASH_MODE,
                    "hash_semantics": "INTEGRITY_ONLY",
                    "qualification_checks": checks,
                }
            )
            record["qualification_pass"] = qualification_pass(record)
            record["disposition"] = (
                "QUALIFYING" if record["qualification_pass"] else "MAPPED_DISQUALIFIED"
            )
            validate_candidate(record)
            claim_inventory.append(record)

    substrate_locks = []
    for relative in DATA_STATUS_SUBSTRATE:
        path = REPO / relative
        if not path.exists():
            raise ValueError(f"missing substrate path: {relative}")
        substrate_locks.append(
            {
                "path": relative,
                "canonical_utf8_lf_sha256": canonical_hash(path),
                "hash_mode": HASH_MODE,
                "hash_semantics": "INTEGRITY_OR_STATUS_ONLY_NOT_THEOREM",
            }
        )

    file_counts = Counter(row["disposition"] for row in theorem_files)
    claim_counts = Counter(row["disposition"] for row in claim_inventory)
    qualifying = [row for row in claim_inventory if row["qualification_pass"]]
    not_mapped = [
        row["path"] for row in theorem_files if row["disposition"] == "NOT_MAPPED_YET"
    ]

    inventory = {
        "schema": SCHEMA_ID,
        "scope": SCOPE_ID,
        "hash_mode": HASH_MODE,
        "hash_semantics": "INTEGRITY_ONLY",
        "theorem_corpus": {
            "selection_rule": (
                "EXACTLY_ONE_MAIN_TEX_FOR_EVERY_INTEGER_PAPER_NUMBER_133_THROUGH_172"
            ),
            "first_paper": 133,
            "last_paper": 172,
            "file_count": len(theorem_files),
            "files": theorem_files,
        },
        "data_status_substrate": {
            "role": "DOMAIN_AND_STATUS_ONLY",
            "artifact_count": len(substrate_locks),
            "artifacts": substrate_locks,
        },
        "qualification_contract": {
            "target": "H1.source_backed_local_occurrence_edge_family",
            "required_fields": list(QUALIFICATION_REQUIREMENTS),
            "active_support_required_here": False,
            "canonical_minimal_representation_required_here": False,
            "reason_for_separation": (
                "active support and canonical minimality are independent H1 roots"
            ),
        },
        "corpus_partition": {
            "file_disposition_counts": {
                name: file_counts[name]
                for name in (
                    "MAPPED_DISQUALIFIED",
                    "REVIEWED_NO_CANDIDATE",
                    "NOT_MAPPED_YET",
                    "QUALIFYING",
                )
            },
            "claim_disposition_counts": {
                name: claim_counts[name]
                for name in ("MAPPED_DISQUALIFIED", "QUALIFYING")
            },
            "not_mapped_yet_paths": not_mapped,
        },
        "claim_inventory": claim_inventory,
        "qualifying_claim_ids": [row["claim_id"] for row in qualifying],
        "qualifying_count": len(qualifying),
        "max_defensible_family_status": (
            "NONEMPTY_IN_DECLARED_CORPUS"
            if qualifying
            else "EMPTY_IN_FROZEN_DECLARED_CORPUS"
        ),
        "next_forced_object": "TPC174.MINIMAL_SOURCE_LOCKED_LOCAL_EDGE_WITNESS_CONTRACT",
        "claim_boundary": {
            "zero_means_mathematical_nonexistence": False,
            "production_local_occurrence_family_proved": False,
            "actual_active_support_proved": False,
            "canonical_minimal_representation_proved": False,
            "fixed_h0_2_preserved_as_requirement": True,
            "positive_fixed_X_L2": False,
            "strict_one_over_400": False,
            "prime_pair_lower_bound": False,
            "twin_prime_theorem": False,
        },
    }

    if len(theorem_files) != 40:
        raise ValueError("declared theorem corpus is not the 40-file interval")
    if set(file_counts) - {
        "MAPPED_DISQUALIFIED",
        "REVIEWED_NO_CANDIDATE",
        "NOT_MAPPED_YET",
        "QUALIFYING",
    }:
        raise ValueError("unknown file disposition")
    if file_counts["NOT_MAPPED_YET"] != 0:
        raise ValueError(f"declared corpus review incomplete: {not_mapped}")
    if len({row["claim_id"] for row in claim_inventory}) != len(claim_inventory):
        raise ValueError("duplicate claim id")
    validate_inventory(inventory)

    def rejected(mutated: dict[str, Any]) -> bool:
        try:
            validate_candidate(mutated)
        except ValueError:
            return True
        return not mutated["qualification_pass"]

    shadow = copy.deepcopy(
        next(row for row in claim_inventory if row["claim_id"] == "S153.cut_to_shadow_basis_injection")
    )
    shadow["qualification_checks"]["ACTUAL_LOCAL_OCCURRENCE_EDGE_CONCLUSION"] = True
    shadow["qualification_pass"] = qualification_pass(shadow)

    verifier = copy.deepcopy(
        next(row for row in claim_inventory if row["claim_id"] == "S155.verifier_internal_soundness")
    )
    verifier["qualification_checks"]["ACTUAL_LOCAL_OCCURRENCE_EDGE_CONCLUSION"] = True
    verifier["qualification_checks"]["FIVE_FIELD_PRODUCTION_CUT_ADDRESS"] = True
    verifier["qualification_checks"]["EXACT_EDGE_WEIGHT"] = True
    verifier["qualification_checks"]["FIXED_H0_EQUALS_2_LINEAGE"] = True
    verifier["qualification_checks"]["PHYSICAL_NORMALIZATION_LINEAGE"] = True
    verifier["qualification_pass"] = qualification_pass(verifier)

    archive_key = copy.deepcopy(
        next(row for row in claim_inventory if row["claim_id"] == "S164.unique_minimal_archive_address")
    )
    archive_key["qualification_checks"]["ACTUAL_LOCAL_OCCURRENCE_EDGE_CONCLUSION"] = True
    archive_key["qualification_pass"] = qualification_pass(archive_key)

    actual_core = copy.deepcopy(
        next(row for row in claim_inventory if row["claim_id"] == "A170.metric_packet_corridor")
    )
    actual_core["qualification_checks"]["FIVE_FIELD_PRODUCTION_CUT_ADDRESS"] = True
    actual_core["qualification_pass"] = qualification_pass(actual_core)

    hash_promotion = copy.deepcopy(inventory)
    hash_promotion["hash_semantics"] = "THEOREM_EVIDENCE"
    try:
        validate_inventory(hash_promotion)
    except ValueError:
        reject_hash_as_theorem = True
    else:
        reject_hash_as_theorem = False

    global_nonexistence_promotion = copy.deepcopy(inventory)
    global_nonexistence_promotion["claim_boundary"][
        "zero_means_mathematical_nonexistence"
    ] = True
    try:
        validate_inventory(global_nonexistence_promotion)
    except ValueError:
        reject_scoped_zero_as_nonexistence = True
    else:
        reject_scoped_zero_as_nonexistence = False

    audit = {
        "schema": "tpc-173-production-source-claim-inventory-audit-v1",
        "status": "PASS",
        "inventory_sha256": hashlib.sha256(
            canonical_json(inventory).encode("utf-8")
        ).hexdigest(),
        "checks": {
            "continuous_tpc133_172_main_tex_corpus": len(theorem_files) == 40,
            "all_source_hashes_recomputed": True,
            "corpus_partition_total": sum(file_counts.values()) == 40,
            "mapped_disqualified_count": file_counts["MAPPED_DISQUALIFIED"],
            "reviewed_no_candidate_count": file_counts["REVIEWED_NO_CANDIDATE"],
            "not_mapped_yet_count": file_counts["NOT_MAPPED_YET"],
            "qualifying_file_count": file_counts["QUALIFYING"],
            "qualifying_claim_count": len(qualifying),
            "old_tpc163_scope_not_promoted_to_global_nonexistence": True,
            "data_status_substrate_not_used_as_theorem_proof": True,
        },
        "mutation_regressions": {
            "reject_shadow_to_actual_occurrence_promotion": rejected(shadow),
            "reject_verifier_contract_to_production_edge_promotion": rejected(verifier),
            "reject_archive_address_to_occurrence_edge_promotion": rejected(archive_key),
            "reject_actual_core_without_cut_crosswalk": rejected(actual_core),
            "reject_hash_as_theorem_semantics": reject_hash_as_theorem,
            "reject_scoped_zero_as_mathematical_nonexistence": (
                reject_scoped_zero_as_nonexistence
            ),
        },
        "claim_boundary": inventory["claim_boundary"],
    }
    for name, value in audit["checks"].items():
        if isinstance(value, bool):
            if not value:
                raise ValueError(f"audit check failed: {name}")
        elif not isinstance(value, int) or value < 0:
            raise ValueError(f"invalid audit count: {name}")
    if not all(audit["mutation_regressions"].values()):
        raise ValueError("mutation regression failed")
    return inventory, audit


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
    inventory, audit = build()
    write_or_check(INVENTORY, inventory, args.check)
    write_or_check(AUDIT, audit, args.check)
    mode = "checked" if args.check else "wrote"
    print(
        f"{mode} TPC-173: files={inventory['theorem_corpus']['file_count']} "
        f"mapped={inventory['corpus_partition']['file_disposition_counts']['MAPPED_DISQUALIFIED']} "
        f"reviewed_no_candidate={inventory['corpus_partition']['file_disposition_counts']['REVIEWED_NO_CANDIDATE']} "
        f"not_mapped={len(inventory['corpus_partition']['not_mapped_yet_paths'])} "
        f"qualifying={inventory['qualifying_count']}"
    )


if __name__ == "__main__":
    main()
