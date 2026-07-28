#!/usr/bin/env python3
"""Build the TPC-163 source census and native-key collision certificate."""

from __future__ import annotations

import argparse
import copy
import hashlib
import json
from collections import Counter, defaultdict
from pathlib import Path
from typing import Any


HERE = Path(__file__).resolve().parent
PAPER = HERE.parent
PAPERS = PAPER.parent
REPO = PAPERS.parent

TPC153 = PAPERS / "tpc-153-canonical-cut-occurrence-shadow"
TPC154 = PAPERS / "tpc-154-conservative-completion-fiber-obstruction"
TPC155 = PAPERS / "tpc-155-theorem-backed-occurrence-witness-verifier"
TPC156 = PAPERS / "tpc-156-h1-occurrence-crosswalk-route-decision"
TPC161 = PAPERS / "tpc-161-source-locked-occurrence-return-integration"
TPC162 = PAPERS / "tpc-162-mvp6-actual-carrier-endpoint-route-decision"

SHADOW = TPC153 / "samples" / "tpc153_cut_occurrence_shadow.jsonl"
TPC153_MAIN = TPC153 / "main.tex"
TPC153_CERT = (
    TPC153 / "experiments" / "tpc153_cut_occurrence_shadow_certificate.json"
)
TPC154_MAIN = TPC154 / "main.tex"
TPC154_CERT = (
    TPC154
    / "experiments"
    / "tpc154_completion_fiber_obstruction_certificate.json"
)
TPC154_COMPLETIONS = TPC154 / "samples" / "tpc154_formal_completions.jsonl"
TPC155_STATUS = TPC155 / "samples" / "tpc155_production_witness_status.json"
TPC155_AUDIT = (
    TPC155 / "experiments" / "tpc155_occurrence_witness_audit.json"
)
TPC156_DECISION = (
    TPC156 / "experiments" / "tpc156_h1_occurrence_decision.json"
)
TPC161_MANIFEST = (
    TPC161 / "experiments" / "tpc161_occurrence_return_manifest.json"
)
TPC162_SNAPSHOT = TPC162 / "experiments" / "tpc162_mvp6_snapshot.json"

SCHEMA = PAPER / "schemas" / "tpc163-source-census-v1.schema.json"
SAMPLE = PAPER / "samples" / "tpc163_native_collision_witness.json"
CENSUS = HERE / "tpc163_source_census.json"
AUDIT = HERE / "tpc163_source_census_audit.json"

HASH_MODE = "CANONICAL_UTF8_LF_V2"
SCHEMA_ID = "tpc-163-source-locator-census-v1"
EDGE_CLASSES = [
    "actual_occurrence_edge",
    "actual_active_support",
    "canonical_parent_or_minimal_representation",
    "ordered_stage_chain",
    "exact_downstream_multiplier",
    "QD",
    "QZ",
    "G",
    "P_h0_downstream",
    "affine_native_d_crosswalk",
    "physical_cover",
    "reconnection",
    "occurrence_registry",
]


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


def load_jsonl(path: Path) -> list[dict[str, Any]]:
    rows = []
    for line in normalize(path.read_text(encoding="utf-8")).splitlines():
        if line.strip():
            value = json.loads(line)
            if not isinstance(value, dict):
                raise ValueError("JSONL row is not an object")
            rows.append(value)
    return rows


def source_lock(source_id: str, path: Path) -> dict[str, str]:
    return {
        "source_id": source_id,
        "path": rel(path),
        "canonical_utf8_lf_sha256": canonical_hash(path),
        "hash_mode": HASH_MODE,
        "hash_semantics": "INTEGRITY_ONLY",
    }


def validate_upstream(rows: list[dict[str, Any]]) -> None:
    cert = load_json(TPC153_CERT)
    obstruction = load_json(TPC154_CERT)
    status = load_json(TPC155_STATUS)
    audit = load_json(TPC155_AUDIT)
    decision = load_json(TPC156_DECISION)
    manifest = load_json(TPC161_MANIFEST)
    snapshot = load_json(TPC162_SNAPSHOT)
    if cert.get("status") != "PASS" or cert.get("census", {}).get(
        "production_shadow_rows"
    ) != 2988:
        raise ValueError("TPC-153 production shadow drift")
    if canonical_hash(SHADOW) != cert["artifacts"]["production_shadow_sha256"]:
        raise ValueError("TPC-153 shadow hash drift")
    if obstruction.get("status") != "PASS":
        raise ValueError("TPC-154 obstruction certificate is not PASS")
    if obstruction.get("theorem_exports", {}).get(
        "H1.formal_completion_fiber_nonuniqueness"
    ) != "PROVED_L0_SCHEMA":
        raise ValueError("TPC-154 formal obstruction theorem drift")
    if obstruction.get("obstruction_scope", {}).get(
        "two_actual_carrier_completions_constructed"
    ) is not False:
        raise ValueError("TPC-154 formal completions promoted to actual")
    if obstruction.get("claim_boundary", {}).get(
        "formal_completion_is_actual_occurrence_lift"
    ) is not False:
        raise ValueError("TPC-154 actual-lift boundary drift")
    if canonical_hash(TPC154_COMPLETIONS) != obstruction["artifacts"][
        "formal_completions_sha256"
    ]:
        raise ValueError("TPC-154 formal-completion hash drift")
    if status.get("production_witness_present") is not False:
        raise ValueError("TPC-155 production witness status drift")
    if status.get("current_production_actual_witness_status") != "NOT_TESTABLE":
        raise ValueError("TPC-155 production status was promoted")
    if audit.get("status") != "PASS":
        raise ValueError("TPC-155 audit is not PASS")
    if decision.get("first_missing_selected_route") != (
        "H1.theorem_backed_occurrence_provenance_crosswalk"
    ):
        raise ValueError("TPC-156 first missing drift")
    if manifest.get("current_verdict") != "NOT_TESTABLE":
        raise ValueError("TPC-161 verdict drift")
    if snapshot.get("current_verdict") != "NOT_TESTABLE":
        raise ValueError("TPC-162 verdict drift")
    if len(rows) != 2988:
        raise ValueError("production shadow row count drift")


def positive_claim(
    claim_id: str,
    locator: str,
    formula_locator: str,
    derivation_ast: dict[str, Any],
) -> dict[str, Any]:
    source_text = normalize(TPC153_MAIN.read_text(encoding="utf-8"))
    for token in (f"\\label{{{locator}}}", f"\\label{{{formula_locator}}}"):
        if token not in source_text:
            raise ValueError(f"missing positive-claim locator: {token}")
    return {
        "claim_id": claim_id,
        "claim_level": "PROVED_L1_STRUCTURAL_SHADOW_ONLY",
        "source_path": rel(TPC153_MAIN),
        "canonical_utf8_lf_sha256": canonical_hash(TPC153_MAIN),
        "theorem_locator": {"kind": "LATEX_LABEL", "value": locator},
        "formula_locator": {"kind": "LATEX_LABEL", "value": formula_locator},
        "derivation_ast": derivation_ast,
        "production_actual_occurrence_semantics": False,
    }


def formal_obstruction_claim(
    claim_id: str,
    locator: str,
    formula_locator: str,
    derivation_ast: dict[str, Any],
) -> dict[str, Any]:
    source_text = normalize(TPC154_MAIN.read_text(encoding="utf-8"))
    for token in (f"\\label{{{locator}}}", f"\\label{{{formula_locator}}}"):
        if token not in source_text:
            raise ValueError(f"missing formal-obstruction locator: {token}")
    return {
        "claim_id": claim_id,
        "claim_level": "FORMAL_ONLY/SCOPED_OBSTRUCTION",
        "source_path": rel(TPC154_MAIN),
        "canonical_utf8_lf_sha256": canonical_hash(TPC154_MAIN),
        "theorem_locator": {"kind": "LATEX_LABEL", "value": locator},
        "formula_locator": {"kind": "LATEX_LABEL", "value": formula_locator},
        "derivation_ast": derivation_ast,
        "production_actual_occurrence_semantics": False,
    }


def build() -> tuple[dict[str, Any], dict[str, Any], dict[str, Any]]:
    rows = load_jsonl(SHADOW)
    validate_upstream(rows)
    path_ids = [row["source_cut_path_id"] for row in rows]
    if len(path_ids) != len(set(path_ids)):
        raise ValueError("shadow source paths are not unique")
    terminal = Counter(row["cut_terminal_type"] for row in rows)
    packet_scopes = {
        canonical_json(row["lineage"]["packet_scope"]) for row in rows
    }
    by_native: dict[tuple[int, int, int], list[str]] = defaultdict(list)
    for row in rows:
        native = tuple(row["lineage"]["native_tuple"])
        by_native[native].append(row["source_cut_path_id"])
        if (
            row["actual_completion"]["status"] != "NOT_PRESENT"
            or row["selectors"]["downstream_selector"]["status"]
            != "NOT_PRESENT"
            or row["support_namespaces"]["actual_active_support"]
            != "UNDECIDED"
            or row["support_namespaces"]["canonical_parent_carrier"]
            != "NOT_PRESENT"
        ):
            raise ValueError("shadow row contains promoted occurrence data")
    multiplicities = Counter(len(value) for value in by_native.values())
    collision_groups = {
        native: sorted(paths)
        for native, paths in by_native.items()
        if len(paths) > 1
    }
    collision_tuple_count = len(collision_groups)
    rows_in_collision = sum(len(value) for value in collision_groups.values())
    excess = sum(len(value) - 1 for value in collision_groups.values())
    locks = [
        source_lock("TPC153.main", TPC153_MAIN),
        source_lock("TPC153.certificate", TPC153_CERT),
        source_lock("TPC153.shadow", SHADOW),
        source_lock("TPC154.main", TPC154_MAIN),
        source_lock("TPC154.certificate", TPC154_CERT),
        source_lock("TPC154.formal_completions", TPC154_COMPLETIONS),
        source_lock("TPC155.production_status", TPC155_STATUS),
        source_lock("TPC155.audit", TPC155_AUDIT),
        source_lock("TPC156.decision", TPC156_DECISION),
        source_lock("TPC161.manifest", TPC161_MANIFEST),
        source_lock("TPC162.snapshot", TPC162_SNAPSHOT),
    ]
    claims = [
        positive_claim(
            "S153.cut_to_shadow_basis_injection",
            "thm:shadow",
            "eq:shadow",
            {
                "op": "basis_injection",
                "domain_key": "source_cut_path_id",
                "row_key": "partial_occurrence_id",
                "edge_weight": {"numerator": 1, "denominator": 1},
            },
        ),
        positive_claim(
            "S153.shadow_column_conservation",
            "thm:shadow",
            "eq:shadow-conservation",
            {
                "op": "column_sum",
                "input": "S153.cut_to_shadow_basis_injection",
                "value": {"numerator": 1, "denominator": 1},
            },
        ),
    ]
    formal_claims = [
        formal_obstruction_claim(
            "S154.formal_completion_fiber_nonuniqueness",
            "thm:nonunique",
            "eq:column",
            {
                "op": "construct_two_formal_completions",
                "input": "S153.cut_to_shadow_basis_injection",
                "completion_A": {
                    "formal_child_count": 1,
                    "weight": {"numerator": 1, "denominator": 1},
                },
                "completion_B": {
                    "formal_child_count": 2,
                    "each_weight": {"numerator": 1, "denominator": 2},
                },
                "same_forgetting_pushforward": True,
            },
        ),
        formal_obstruction_claim(
            "S154.current_artifacts_only_recovery_obstruction",
            "thm:obstruction",
            "eq:column",
            {
                "op": "fiber_nonidentifiability",
                "inputs": [
                    "S154.formal_completion_fiber_nonuniqueness",
                    "cor:branch",
                    "prop:labels",
                ],
                "stopped_route": (
                    "CURRENT_ARTIFACTS_ONLY_CANONICAL_ACTUAL_LIFT_DERIVATION"
                ),
                "augmented_theorem_backed_route_remains_open": True,
            },
        ),
    ]
    census = {
        "schema": SCHEMA_ID,
        "scope": (
            "FROZEN_DECLARED_SOURCE_CORPUS_TPC153_154_155_156_161_162"
        ),
        "source_locks": locks,
        "production_archive": {
            "row_count": len(rows),
            "terminal_type_counts": {
                "ELIGIBLE_TAIL_OPEN": terminal.get("ELIGIBLE_TAIL_OPEN", 0),
                "FRONTIER_UNMAPPED": terminal.get("FRONTIER_UNMAPPED", 0),
            },
            "source_path_count": len(set(path_ids)),
            "packet_scope_count": len(packet_scopes),
        },
        "positive_shadow_claims": claims,
        "positive_formal_obstruction_claims": formal_claims,
        "production_crosswalk_edge_census": {
            "required_edge_classes": EDGE_CLASSES,
            "coverage_by_edge_class": {key: 0 for key in EDGE_CLASSES},
            "theorem_backed_edge_count": 0,
            "status": "EMPTY_IN_FROZEN_DECLARED_CORPUS",
            "detection_mode": "EXPLICIT_MAPPED_FROZEN_CORPUS_CENSUS",
            "future_new_fields_automatically_scanned": False,
        },
        "native_key_collision": {
            "native_tuple_count": len(by_native),
            "collision_tuple_count": collision_tuple_count,
            "rows_in_collision_classes": rows_in_collision,
            "excess_rows_over_native_keys": excess,
            "multiplicity_distribution": {
                str(key): value for key, value in sorted(multiplicities.items())
            },
            "maximum_multiplicity": max(multiplicities),
            "native_tuple_is_row_key": False,
        },
        "claim_boundary": {
            "shadow_is_actual_occurrence_lift": False,
            "zero_edges_means_actual_edges_do_not_exist": False,
            "native_tuple_is_production_crosswalk_key": False,
            "production_crosswalk_proved": False,
            "actual_active_support_proved": False,
            "canonical_minimal_representation_proved": False,
            "positive_fixed_X_L2": False,
            "twin_prime_theorem": False,
        },
    }
    first_native = sorted(collision_groups)[0]
    sample = {
        "schema": "tpc-163-native-collision-witness-v1",
        "fixture_scope": "PRODUCTION_ARCHIVE_EXCERPT",
        "native_tuple": list(first_native),
        "multiplicity": len(collision_groups[first_native]),
        "source_cut_path_ids": collision_groups[first_native],
        "statement": (
            "Distinct production cut paths share one native tuple; "
            "this is a key-collision witness, not an occurrence lift."
        ),
        "claim_boundary": {
            "synthetic": False,
            "actual_occurrence_data": False,
        },
    }
    validate_census(census)
    mutations = mutation_regressions(census)
    audit = {
        "schema": "tpc-163-source-census-audit-v1",
        "status": "PASS" if all(mutations.values()) else "FAIL",
        "census_sha256": hashlib.sha256(
            canonical_json(census).encode("utf-8")
        ).hexdigest(),
        "checks": {
            "source_locks_recomputed": True,
            "positive_shadow_and_formal_claims_have_path_hash_locator_and_ast": True,
            "formal_obstruction_cannot_contribute_actual_edge": True,
            "production_crosswalk_edge_count_is_zero_in_scope": True,
            "edge_census_is_explicit_mapped_not_generic_scanner": True,
            "native_collision_counts_recomputed": True,
        },
        "mutation_regressions": mutations,
        "claim_boundary": copy.deepcopy(census["claim_boundary"]),
    }
    if audit["status"] != "PASS":
        raise ValueError("TPC-163 mutation audit failed")
    return census, sample, audit


def validate_census(value: dict[str, Any]) -> None:
    required = {
        "schema",
        "scope",
        "source_locks",
        "production_archive",
        "positive_shadow_claims",
        "positive_formal_obstruction_claims",
        "production_crosswalk_edge_census",
        "native_key_collision",
        "claim_boundary",
    }
    if set(value) != required or value["schema"] != SCHEMA_ID:
        raise ValueError("census contract drift")
    if value["scope"] != (
        "FROZEN_DECLARED_SOURCE_CORPUS_TPC153_154_155_156_161_162"
    ):
        raise ValueError("census scope drift")
    if len(value["source_locks"]) != 11:
        raise ValueError("source-lock count drift")
    for lock in value["source_locks"]:
        path = REPO / lock["path"]
        if canonical_hash(path) != lock["canonical_utf8_lf_sha256"]:
            raise ValueError("source-lock hash drift")
    positive_claims = (
        value["positive_shadow_claims"]
        + value["positive_formal_obstruction_claims"]
    )
    if len(value["positive_shadow_claims"]) != 2 or len(
        value["positive_formal_obstruction_claims"]
    ) != 2:
        raise ValueError("positive claim census drift")
    for claim in positive_claims:
        required_claim = {
            "claim_id",
            "claim_level",
            "source_path",
            "canonical_utf8_lf_sha256",
            "theorem_locator",
            "formula_locator",
            "derivation_ast",
            "production_actual_occurrence_semantics",
        }
        if set(claim) != required_claim:
            raise ValueError("positive claim fields drift")
        path = REPO / claim["source_path"]
        if canonical_hash(path) != claim["canonical_utf8_lf_sha256"]:
            raise ValueError("positive claim hash drift")
        text = normalize(path.read_text(encoding="utf-8"))
        for locator in (claim["theorem_locator"], claim["formula_locator"]):
            if (
                set(locator) != {"kind", "value"}
                or locator["kind"] != "LATEX_LABEL"
                or f"\\label{{{locator['value']}}}" not in text
            ):
                raise ValueError("positive claim locator drift")
        if not isinstance(claim["derivation_ast"], dict) or not claim[
            "derivation_ast"
        ]:
            raise ValueError("positive claim derivation AST is absent")
        if claim["production_actual_occurrence_semantics"]:
            raise ValueError("nonactual claim promoted to occurrence semantics")
    if any(
        claim["claim_level"] != "PROVED_L1_STRUCTURAL_SHADOW_ONLY"
        for claim in value["positive_shadow_claims"]
    ):
        raise ValueError("shadow semantic class drift")
    if any(
        claim["claim_level"] != "FORMAL_ONLY/SCOPED_OBSTRUCTION"
        for claim in value["positive_formal_obstruction_claims"]
    ):
        raise ValueError("formal obstruction semantic class drift")
    edge = value["production_crosswalk_edge_census"]
    if (
        edge["required_edge_classes"] != EDGE_CLASSES
        or set(edge["coverage_by_edge_class"]) != set(EDGE_CLASSES)
        or any(edge["coverage_by_edge_class"].values())
        or edge["theorem_backed_edge_count"] != 0
        or edge["status"] != "EMPTY_IN_FROZEN_DECLARED_CORPUS"
        or edge["detection_mode"]
        != "EXPLICIT_MAPPED_FROZEN_CORPUS_CENSUS"
        or edge["future_new_fields_automatically_scanned"] is not False
    ):
        raise ValueError("production edge census was promoted")
    archive = value["production_archive"]
    if (
        archive["row_count"] != 2988
        or archive["source_path_count"] != 2988
        or archive["packet_scope_count"] != 1
        or archive["terminal_type_counts"]
        != {"ELIGIBLE_TAIL_OPEN": 0, "FRONTIER_UNMAPPED": 2988}
    ):
        raise ValueError("archive census drift")
    collision = value["native_key_collision"]
    if collision != {
        "native_tuple_count": 866,
        "collision_tuple_count": 854,
        "rows_in_collision_classes": 2976,
        "excess_rows_over_native_keys": 2122,
        "multiplicity_distribution": {"1": 12, "2": 220, "4": 634},
        "maximum_multiplicity": 4,
        "native_tuple_is_row_key": False,
    }:
        raise ValueError("native collision certificate drift")
    if any(value["claim_boundary"].values()):
        raise ValueError("claim boundary was promoted")


def mutation_regressions(census: dict[str, Any]) -> dict[str, bool]:
    tests: dict[str, bool] = {}

    def reject(name: str, mutate: Any) -> None:
        trial = copy.deepcopy(census)
        mutate(trial)
        try:
            validate_census(trial)
        except (KeyError, TypeError, ValueError):
            tests[name] = True
        else:
            tests[name] = False

    reject(
        "fabricated_production_edge_rejected",
        lambda obj: obj["production_crosswalk_edge_census"].update(
            {"theorem_backed_edge_count": 1}
        ),
    )
    reject(
        "future_schema_generic_scanner_promotion_rejected",
        lambda obj: obj["production_crosswalk_edge_census"].update(
            {"future_new_fields_automatically_scanned": True}
        ),
    )
    reject(
        "source_hash_drift_rejected",
        lambda obj: obj["positive_shadow_claims"][0].update(
            {"canonical_utf8_lf_sha256": "0" * 64}
        ),
    )
    reject(
        "missing_formula_locator_rejected",
        lambda obj: obj["positive_shadow_claims"][0]["formula_locator"].update(
            {"value": "theorem.fabricated"}
        ),
    )
    reject(
        "missing_derivation_ast_rejected",
        lambda obj: obj["positive_shadow_claims"][0].update(
            {"derivation_ast": {}}
        ),
    )
    reject(
        "shadow_to_occurrence_promotion_rejected",
        lambda obj: obj["positive_shadow_claims"][0].update(
            {"production_actual_occurrence_semantics": True}
        ),
    )
    reject(
        "formal_obstruction_to_actual_edge_promotion_rejected",
        lambda obj: obj["positive_formal_obstruction_claims"][0].update(
            {"production_actual_occurrence_semantics": True}
        ),
    )
    reject(
        "native_collision_excess_drift_rejected",
        lambda obj: obj["native_key_collision"].update(
            {"excess_rows_over_native_keys": 0}
        ),
    )
    reject(
        "native_tuple_key_promotion_rejected",
        lambda obj: obj["native_key_collision"].update(
            {"native_tuple_is_row_key": True}
        ),
    )
    reject(
        "zero_edges_as_nonexistence_rejected",
        lambda obj: obj["claim_boundary"].update(
            {"zero_edges_means_actual_edges_do_not_exist": True}
        ),
    )
    return tests


def write(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="\n") as handle:
        handle.write(text)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()
    census, sample, audit = build()
    rendered = {
        CENSUS: canonical_json(census),
        SAMPLE: canonical_json(sample),
        AUDIT: canonical_json(audit),
    }
    if args.check:
        for path, expected in rendered.items():
            if not path.is_file() or normalize(
                path.read_text(encoding="utf-8")
            ) != expected:
                raise SystemExit(f"TPC-163 CHECK FAIL: {path.name}")
        print("TPC-163 CHECK PASS")
    else:
        for path, text in rendered.items():
            write(path, text)
        print("TPC-163 GENERATE PASS")
    print(
        json.dumps(
            {
                "status": audit["status"],
                "production_theorem_backed_edges": 0,
                "rows": census["production_archive"]["row_count"],
                "native_tuples": census["native_key_collision"][
                    "native_tuple_count"
                ],
                "collision_excess": census["native_key_collision"][
                    "excess_rows_over_native_keys"
                ],
            },
            sort_keys=True,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
