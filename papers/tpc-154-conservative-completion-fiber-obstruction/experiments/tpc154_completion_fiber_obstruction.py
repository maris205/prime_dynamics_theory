#!/usr/bin/env python3
"""Build the TPC-154 conservative completion-fiber obstruction.

For each production TPC-153 partial occurrence, the audit constructs two
different *formal schema completions*: one has one child of weight one and
the other has two row-separated children of weight one half.  Both forget
to the same unit cut-shadow column.  These are model completions in the
maximal current-schema class, not claims about the unknown actual carrier.

Default mode writes deterministic UTF-8/LF artifacts.  ``--check`` is
read-only and requires byte-for-byte canonical agreement.
"""

from __future__ import annotations

import argparse
import copy
import hashlib
import importlib.util
import json
import sys
from fractions import Fraction
from pathlib import Path
from types import ModuleType
from typing import Any, Iterable


sys.dont_write_bytecode = True

HERE = Path(__file__).resolve().parent
PAPER = HERE.parent
PAPERS = PAPER.parent
TPC153 = PAPERS / "tpc-153-canonical-cut-occurrence-shadow"
TPC153_SCRIPT = TPC153 / "experiments" / "tpc153_cut_occurrence_shadow.py"
TPC153_SHADOW = TPC153 / "samples" / "tpc153_cut_occurrence_shadow.jsonl"
TPC153_SYNTHETIC = TPC153 / "samples" / "tpc153_synthetic_eto_regression.json"
TPC153_CERTIFICATE = (
    TPC153 / "experiments" / "tpc153_cut_occurrence_shadow_certificate.json"
)
TPC153_SCHEMA = TPC153 / "schemas" / "tpc153-cut-occurrence-shadow-v1.schema.json"
SCHEMA = PAPER / "schemas" / "tpc154-conservative-completion-v1.schema.json"
OUT_COMPLETIONS = PAPER / "samples" / "tpc154_formal_completions.jsonl"
OUT_CERTIFICATE = HERE / "tpc154_completion_fiber_obstruction_certificate.json"

ROW_SCHEMA = "tpc154-conservative-completion-fiber-v1"
CERTIFICATE_SCHEMA = "tpc-154-completion-fiber-obstruction-certificate-v1"


def normalize_lf(text: str) -> str:
    return text.replace("\r\n", "\n").replace("\r", "\n")


def canonical_json(value: Any) -> str:
    return json.dumps(value, ensure_ascii=False, indent=2, sort_keys=True) + "\n"


def canonical_compact(value: Any) -> str:
    return json.dumps(
        value, ensure_ascii=False, separators=(",", ":"), sort_keys=True
    )


def render_jsonl(records: Iterable[dict[str, Any]]) -> str:
    return "".join(canonical_compact(record) + "\n" for record in records)


def sha256_text(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def digest_object(value: Any) -> str:
    return sha256_text(canonical_compact(value))


def canonical_file_text(path: Path) -> str:
    return normalize_lf(path.read_text(encoding="utf-8"))


def validate_schema_contract() -> str:
    schema = json.loads(canonical_file_text(SCHEMA))
    required = {
        "schema",
        "source",
        "completion_A",
        "completion_B",
        "fiber_comparison",
        "claim_boundary",
        "integrity_sha256",
    }
    if schema.get("$schema") != "https://json-schema.org/draft/2020-12/schema":
        raise ValueError("TPC-154 schema draft drift")
    if schema.get("$id") != "tpc154-conservative-completion-v1.schema.json":
        raise ValueError("TPC-154 schema identifier drift")
    if set(schema.get("required", [])) != required:
        raise ValueError("TPC-154 schema required-field contract drift")
    if set(schema.get("properties", {})) != required:
        raise ValueError("TPC-154 schema property contract drift")
    if schema.get("additionalProperties") is not False:
        raise ValueError("TPC-154 schema is not closed")
    properties = schema["properties"]
    if properties["schema"].get("const") != ROW_SCHEMA:
        raise ValueError("TPC-154 row schema const drift")
    completion_a = properties["completion_A"]["allOf"][1]["properties"]
    completion_b = properties["completion_B"]["allOf"][1]["properties"]
    if completion_a["branch_count"].get("const") != 1:
        raise ValueError("TPC-154 Completion A schema drift")
    if completion_b["branch_count"].get("const") != 2:
        raise ValueError("TPC-154 Completion B schema drift")
    return "PASS"


def load_module(name: str, path: Path) -> ModuleType:
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise ImportError(f"cannot load source generator: {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def parse_jsonl(text: str) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for line_number, line in enumerate(normalize_lf(text).splitlines(), 1):
        if not line.strip():
            continue
        try:
            rows.append(json.loads(line))
        except json.JSONDecodeError as exc:
            raise ValueError(f"invalid JSONL line {line_number}: {exc}") from exc
    return rows


def load_tpc153_source() -> tuple[
    list[dict[str, Any]], dict[str, Any], dict[str, Any], dict[str, Any]
]:
    module = load_module("tpc154_source_tpc153", TPC153_SCRIPT)
    shadow_text, synthetic_text, certificate_text = module.build()
    if canonical_file_text(TPC153_SHADOW) != shadow_text:
        raise ValueError("TPC-153 production shadow has generator drift")
    if canonical_file_text(TPC153_SYNTHETIC) != synthetic_text:
        raise ValueError("TPC-153 synthetic ETO fixture has generator drift")
    if canonical_file_text(TPC153_CERTIFICATE) != certificate_text:
        raise ValueError("TPC-153 certificate has generator drift")
    certificate = json.loads(certificate_text)
    if certificate["status"] != "PASS":
        raise ValueError("TPC-153 source certificate is not PASS")
    if certificate["source"]["lock_mode"] != "CANONICAL_UTF8_LF_V2":
        raise ValueError("TPC-153 source lock mode drift")
    source_lock = {
        "lock_mode": "CANONICAL_UTF8_LF_V2",
        "semantic_generation_chain": "PASS",
        "hashes_are_integrity_only": True,
        "tpc153_shadow_sha256": sha256_text(shadow_text),
        "tpc153_synthetic_eto_sha256": sha256_text(synthetic_text),
        "tpc153_certificate_sha256": sha256_text(certificate_text),
        "tpc153_schema_sha256": sha256_text(canonical_file_text(TPC153_SCHEMA)),
    }
    return (
        parse_jsonl(shadow_text),
        json.loads(synthetic_text),
        certificate,
        source_lock,
    )


def rational_record(value: Fraction) -> dict[str, Any]:
    return {
        "ring": "Q",
        "numerator": value.numerator,
        "denominator": value.denominator,
    }


def parse_rational(value: dict[str, Any]) -> Fraction:
    if value.get("ring") != "Q" or value.get("denominator", 0) <= 0:
        raise ValueError("edge coefficient is not an exact normalized rational")
    return Fraction(value["numerator"], value["denominator"])


def source_descriptor(
    source: dict[str, Any], source_scope: str
) -> dict[str, Any]:
    if source_scope == "PRODUCTION_CURRENT_ARCHIVE":
        lineage = source["lineage"]
        scope = lineage["packet_scope"]
        return {
            "source_scope": source_scope,
            "partial_occurrence_id": source["partial_occurrence_id"],
            "source_cut_path_id": source["source_cut_path_id"],
            "cut_terminal_type": source["cut_terminal_type"],
            "native_tuple": list(lineage["native_tuple"]),
            "source_h0": scope["h0"],
            "physical_normalization": scope["physical_normalization"],
            "support_role": "FORMAL_SUPPORT_ENVELOPE",
            "source_integrity_sha256": source["integrity_sha256"],
        }
    if source_scope != "SYNTHETIC_L0_ONLY":
        raise ValueError("unknown completion source scope")
    inputs = source["policy_inputs"]
    return {
        "source_scope": source_scope,
        "partial_occurrence_id": "synthetic-cut-shadow|eto-policy-regression",
        "source_cut_path_id": "SYNTHETIC_L0_ONLY|ETO|policy-regression",
        "cut_terminal_type": source["synthetic_terminal_type"],
        "native_tuple": [0, 0, 0],
        "source_h0": 2,
        "physical_normalization": "SYNTHETIC_L0_ONLY",
        "support_role": "FORMAL_SUPPORT_ENVELOPE",
        "source_integrity_sha256": source["integrity_sha256"],
        "synthetic_policy_inputs": copy.deepcopy(inputs),
    }


def child_annotation(
    descriptor: dict[str, Any],
    completion_id: str,
    branch_index: int,
    branch_count: int,
    edge_weight: Fraction,
) -> dict[str, Any]:
    token = hashlib.sha256(
        (
            descriptor["partial_occurrence_id"]
            + "|"
            + completion_id
            + "|"
            + str(branch_index)
        ).encode("utf-8")
    ).hexdigest()[:20]
    h0 = descriptor["source_h0"]
    variant = 0 if completion_id == "A_ONE_CHILD" else branch_index + 1
    parent_slopes = [3 + 2 * variant, 1 + 2 * branch_index]
    ordered_targets = [h0 + parent_slopes[0], h0 + parent_slopes[1]]
    determinant = ordered_targets[0] - ordered_targets[1]
    edge = {
        "formal_occurrence_id": f"formal-occ|{completion_id}|{token}",
        "row_separated_edge_id": f"formal-edge|{completion_id}|{token}",
        "source_partial_occurrence_id": descriptor["partial_occurrence_id"],
        "branch_index": branch_index,
        "branch_count": branch_count,
        "forgetting_pushforward_weight": rational_record(edge_weight),
        "lineage_echo": {
            "native_tuple": list(descriptor["native_tuple"]),
            "source_h0": h0,
            "physical_normalization": descriptor["physical_normalization"],
            "source_support_role": descriptor["support_role"],
            "actual_active_support": "UNDECIDED",
        },
        "canonical_parent_and_QD": {
            "canonical_parent_key_alpha_gamma_j": (
                f"FORMAL_ONLY|parent|{completion_id}|{token}"
            ),
            "row_ids_and_integer_slopes": {
                "row_ids": [f"formal-row-x|{token}", f"formal-row-y|{token}"],
                "integer_slopes": parent_slopes,
            },
            "ordered_targets_x_y": ordered_targets,
            "content_gcd": 1,
            "signed_determinant_numerator": determinant,
            "exact_determinant_label": (
                f"FORMAL_ONLY|det={determinant}|{completion_id}"
            ),
            "inverse_aggregation_relation": "FORMAL_FREE_COMPLETION_ONLY",
            "physical_and_computational_multiplicity": {
                "physical": 1,
                "computational": branch_count,
            },
            "literal_parent_coefficient": rational_record(edge_weight),
            "determinant_bin_map_edge": f"FORMAL_ONLY|QD|{token}",
        },
        "outer_zero_mode_and_QZ": {
            "outer_affine_key": f"FORMAL_ONLY|outer|{completion_id}|{token}",
            "ordered_coordinate_and_rank": {
                "coordinate": branch_index,
                "rank": branch_index + 1,
            },
            "arithmetic_sign": 1 if branch_index % 2 == 0 else -1,
            "outer_weight": rational_record(edge_weight),
            "factor_allocation_id": f"FORMAL_ONLY|factor|{token}",
            "content_remainder_destination": f"FORMAL_ONLY|remainder|{token}",
            "zero_mode_map_edge": f"FORMAL_ONLY|QZ|{token}",
        },
        "physical_grouping_G": {
            "physical_occurrence_id": f"FORMAL_ONLY|physical-occ|{token}",
            "physical_group_id": (
                f"FORMAL_ONLY|group|{completion_id}|{branch_index}"
            ),
            "exact_reconstruction_multiplier": rational_record(Fraction(1)),
            "multiplicity_and_inverse_aggregation": {
                "multiplicity": branch_count,
                "relation": "FORMAL_FREE_COMPLETION_ONLY",
            },
            "physical_cover_class": "FORMAL_SCHEMA_COMPLETION_ONLY",
            "reconnection_destination": f"FORMAL_ONLY|reconnect|{token}",
            "physical_map_edge": f"FORMAL_ONLY|G|{token}",
        },
        "downstream_shift_selector": {
            "stage_id": f"FORMAL_ONLY|stage|{completion_id}|{branch_index}",
            "source_shift_tag": h0,
            "target_shift_tag": h0 + (0 if completion_id == "A_ONE_CHILD" else 2 * branch_index),
            "source_and_target_selector_domains": {
                "source": "CUT_SHADOW",
                "target": f"FORMAL_ONLY|target-domain|{completion_id}",
            },
            "stage_matrix_edge": f"FORMAL_ONLY|stage-edge|{token}",
            "shift_preservation_source": None,
        },
        "affine_corridor_consumer": {
            "native_tuple_d": descriptor["native_tuple"][2],
            "affine_D_intercept_d": 10 + variant,
            "affine_D_slope_s": 3 + variant,
            "affine_V_intercept_u": 7 + branch_index,
            "affine_V_slope_a": 2 + branch_index,
            "native_d_equals_affine_d_crosswalk_status": "NOT_SOURCED",
            "coefficient_l1_mass": rational_record(abs(edge_weight)),
            "endpoint_ledger_token": f"FORMAL_ONLY|ledger|{token}",
        },
        "provenance_status": {
            "schema_fields_populated": True,
            "theorem_backed_actual_provenance": False,
            "formal_completion_only": True,
        },
    }
    edge["integrity_sha256"] = digest_object(edge)
    return edge


def completion(
    descriptor: dict[str, Any], completion_id: str
) -> dict[str, Any]:
    if completion_id == "A_ONE_CHILD":
        weights = [Fraction(1)]
    elif completion_id == "B_TWO_CHILD_EQUAL_SPLIT":
        weights = [Fraction(1, 2), Fraction(1, 2)]
    else:
        raise ValueError("unknown formal completion")
    edges = [
        child_annotation(
            descriptor,
            completion_id,
            index,
            len(weights),
            weight,
        )
        for index, weight in enumerate(weights)
    ]
    return {
        "completion_id": completion_id,
        "matrix_scope": "FORMAL_CURRENT_SCHEMA_COMPLETION",
        "branch_count": len(edges),
        "edges": edges,
        "column_sum": rational_record(sum(weights, Fraction())),
        "forgets_to_unit_shadow_column": True,
    }


def build_completion_row(
    source: dict[str, Any], source_scope: str
) -> dict[str, Any]:
    descriptor = source_descriptor(source, source_scope)
    row: dict[str, Any] = {
        "schema": ROW_SCHEMA,
        "source": descriptor,
        "completion_A": completion(descriptor, "A_ONE_CHILD"),
        "completion_B": completion(descriptor, "B_TWO_CHILD_EQUAL_SPLIT"),
        "fiber_comparison": {
            "same_forgetting_target": True,
            "same_pushforward_column": rational_record(Fraction(1)),
            "row_separated_branch_counts_differ": True,
            "canonical_completion_selected_by_current_schema": False,
        },
        "claim_boundary": {
            "is_actual_downstream_completion": False,
            "proves_two_actual_carrier_completions_exist": False,
            "stops_augmented_occurrence_route": False,
            "proves_positive_fixed_h0_L2": False,
            "proves_twin_prime_theorem": False,
        },
    }
    row["integrity_sha256"] = digest_object(row)
    return row


def expected_rows(
    production: list[dict[str, Any]], synthetic: dict[str, Any]
) -> list[dict[str, Any]]:
    return [
        *(build_completion_row(row, "PRODUCTION_CURRENT_ARCHIVE")
          for row in production),
        build_completion_row(synthetic, "SYNTHETIC_L0_ONLY"),
    ]


def validate_edge(
    edge: dict[str, Any],
    descriptor: dict[str, Any],
    completion_id: str,
    branch_count: int,
) -> None:
    unsigned = dict(edge)
    recorded_hash = unsigned.pop("integrity_sha256")
    if recorded_hash != digest_object(unsigned):
        raise ValueError("formal edge integrity failure")
    if edge["source_partial_occurrence_id"] != descriptor["partial_occurrence_id"]:
        raise ValueError("formal edge changed its forgetting target")
    if edge["branch_count"] != branch_count:
        raise ValueError("formal edge branch count drift")
    echo = edge["lineage_echo"]
    if echo["native_tuple"] != descriptor["native_tuple"]:
        raise ValueError("native tuple was not inherited")
    if echo["source_h0"] != descriptor["source_h0"]:
        raise ValueError("source h0 was not inherited")
    if echo["physical_normalization"] != descriptor["physical_normalization"]:
        raise ValueError("physical normalization was not inherited")
    if echo["source_support_role"] != "FORMAL_SUPPORT_ENVELOPE":
        raise ValueError("formal support namespace drift")
    if echo["actual_active_support"] != "UNDECIDED":
        raise ValueError("formal completion promoted active support")
    if edge["provenance_status"]["theorem_backed_actual_provenance"]:
        raise ValueError("formal annotation was promoted to actual provenance")
    if not edge["provenance_status"]["formal_completion_only"]:
        raise ValueError("formal completion scope was erased")
    corridor = edge["affine_corridor_consumer"]
    if corridor["native_tuple_d"] != descriptor["native_tuple"][2]:
        raise ValueError("native d lineage drift")
    if corridor["native_d_equals_affine_d_crosswalk_status"] != "NOT_SOURCED":
        raise ValueError("native d was silently identified with affine d")
    if not edge["canonical_parent_and_QD"]["canonical_parent_key_alpha_gamma_j"]:
        raise ValueError("formal parent field missing")
    if not edge["downstream_shift_selector"]["stage_id"]:
        raise ValueError("formal stage field missing")
    if completion_id not in edge["formal_occurrence_id"]:
        raise ValueError("completion identity not row separated")


def validate_completions(
    rows: list[dict[str, Any]],
    production: list[dict[str, Any]],
    synthetic: dict[str, Any],
) -> dict[str, Any]:
    expected = expected_rows(production, synthetic)
    if rows != expected:
        raise ValueError("completion archive does not exactly descend from sources")
    production_ids = {row["partial_occurrence_id"] for row in production}
    seen_production: set[str] = set()
    all_edge_ids: set[str] = set()
    scope_counts = {
        "PRODUCTION_CURRENT_ARCHIVE": 0,
        "SYNTHETIC_L0_ONLY": 0,
    }
    terminal_counts = {
        "ELIGIBLE_TAIL_OPEN": 0,
        "FRONTIER_UNMAPPED": 0,
    }
    for row in rows:
        unsigned = dict(row)
        recorded_hash = unsigned.pop("integrity_sha256")
        if recorded_hash != digest_object(unsigned):
            raise ValueError("completion-fiber row integrity failure")
        descriptor = row["source"]
        scope = descriptor["source_scope"]
        scope_counts[scope] += 1
        terminal_counts[descriptor["cut_terminal_type"]] += 1
        if scope == "PRODUCTION_CURRENT_ARCHIVE":
            partial_id = descriptor["partial_occurrence_id"]
            if partial_id in seen_production or partial_id not in production_ids:
                raise ValueError("production source deleted, duplicated, or invented")
            seen_production.add(partial_id)
        for key, completion_id, branch_count in (
            ("completion_A", "A_ONE_CHILD", 1),
            ("completion_B", "B_TWO_CHILD_EQUAL_SPLIT", 2),
        ):
            candidate = row[key]
            if candidate["completion_id"] != completion_id:
                raise ValueError("formal completion identifier drift")
            if candidate["branch_count"] != branch_count:
                raise ValueError("formal branch count drift")
            if len(candidate["edges"]) != branch_count:
                raise ValueError("formal edge list length drift")
            total = Fraction()
            for edge in candidate["edges"]:
                validate_edge(edge, descriptor, completion_id, branch_count)
                edge_id = edge["row_separated_edge_id"]
                if edge_id in all_edge_ids:
                    raise ValueError("row-separated edge identifier duplicated")
                all_edge_ids.add(edge_id)
                total += parse_rational(edge["forgetting_pushforward_weight"])
            if total != 1 or parse_rational(candidate["column_sum"]) != 1:
                raise ValueError("formal completion is not column conservative")
            if not candidate["forgets_to_unit_shadow_column"]:
                raise ValueError("formal completion lost its forgetting pushforward")
        if not row["fiber_comparison"]["same_forgetting_target"]:
            raise ValueError("completion alternatives do not share a fiber")
        if not row["fiber_comparison"]["row_separated_branch_counts_differ"]:
            raise ValueError("non-equivalence witness was erased")
        if row["fiber_comparison"]["canonical_completion_selected_by_current_schema"]:
            raise ValueError("current schema falsely selected a completion")
        if any(row["claim_boundary"].values()):
            raise ValueError("formal completion row contains a forbidden positive claim")
    if seen_production != production_ids:
        raise ValueError("production completion domain is incomplete")
    if scope_counts != {
        "PRODUCTION_CURRENT_ARCHIVE": len(production),
        "SYNTHETIC_L0_ONLY": 1,
    }:
        raise ValueError("production and synthetic namespaces were conflated")
    return {
        "source_fiber_count": len(rows),
        "production_fiber_count": len(production),
        "synthetic_ETO_fiber_count": 1,
        "scope_counts": scope_counts,
        "terminal_type_counts_including_synthetic": terminal_counts,
        "completion_A_edges": len(rows),
        "completion_B_edges": 2 * len(rows),
        "all_edge_ids_unique": True,
        "A_and_B_column_sums": rational_record(Fraction(1)),
        "A_and_B_have_different_row_separated_branch_count": True,
    }


def mutation_regressions(
    rows: list[dict[str, Any]],
    production: list[dict[str, Any]],
    synthetic: dict[str, Any],
) -> dict[str, bool]:
    if not rows:
        raise ValueError("mutation regressions need completion rows")
    # The production archive is validated in full before this function.  Use
    # two real FUM fibers plus the synthetic ETO fiber for local fail-closed
    # mutations so that every ``--check`` remains inexpensive.
    fixture_production = production[:2]
    fixture_rows = expected_rows(fixture_production, synthetic)

    def rehash_edge(edge: dict[str, Any]) -> None:
        unsigned = dict(edge)
        unsigned.pop("integrity_sha256", None)
        edge["integrity_sha256"] = digest_object(unsigned)

    def rehash_row(row: dict[str, Any]) -> None:
        for key in ("completion_A", "completion_B"):
            for edge in row[key]["edges"]:
                rehash_edge(edge)
        unsigned = dict(row)
        unsigned.pop("integrity_sha256", None)
        row["integrity_sha256"] = digest_object(unsigned)

    def rejected(mutator) -> bool:
        trial = copy.deepcopy(fixture_rows)
        mutator(trial)
        for row in trial:
            rehash_row(row)
        try:
            validate_completions(trial, fixture_production, synthetic)
        except ValueError:
            return True
        return False

    tests = {
        "deleted_production_fiber_rejected": rejected(lambda value: value.pop(0)),
        "duplicated_production_fiber_rejected": rejected(
            lambda value: value.insert(1, copy.deepcopy(value[0]))
        ),
        "synthetic_ETO_omission_rejected": rejected(lambda value: value.pop()),
        "cross_fiber_edge_rejected": rejected(
            lambda value: value[0]["completion_B"]["edges"][0].__setitem__(
                "source_partial_occurrence_id", value[1]["source"]["partial_occurrence_id"]
            )
        ),
        "nonconservative_split_rejected": rejected(
            lambda value: value[0]["completion_B"]["edges"][0].__setitem__(
                "forgetting_pushforward_weight", rational_record(Fraction(1, 3))
            )
        ),
        "native_lineage_drift_rejected": rejected(
            lambda value: value[0]["completion_A"]["edges"][0]["lineage_echo"].__setitem__(
                "native_tuple", [9, 9, 9]
            )
        ),
        "h0_lineage_drift_rejected": rejected(
            lambda value: value[0]["completion_A"]["edges"][0]["lineage_echo"].__setitem__(
                "source_h0", value[0]["source"]["source_h0"] + 2
            )
        ),
        "normalization_drift_rejected": rejected(
            lambda value: value[0]["completion_A"]["edges"][0]["lineage_echo"].__setitem__(
                "physical_normalization", "fabricated-normalization"
            )
        ),
        "parent_field_deletion_rejected": rejected(
            lambda value: value[0]["completion_A"]["edges"][0][
                "canonical_parent_and_QD"
            ].__setitem__("canonical_parent_key_alpha_gamma_j", "")
        ),
        "stage_field_deletion_rejected": rejected(
            lambda value: value[0]["completion_A"]["edges"][0][
                "downstream_shift_selector"
            ].__setitem__("stage_id", "")
        ),
        "active_support_promotion_rejected": rejected(
            lambda value: value[0]["completion_A"]["edges"][0]["lineage_echo"].__setitem__(
                "actual_active_support", "PRESENT"
            )
        ),
        "actual_provenance_promotion_rejected": rejected(
            lambda value: value[0]["completion_A"]["edges"][0][
                "provenance_status"
            ].__setitem__("theorem_backed_actual_provenance", True)
        ),
        "canonical_selection_promotion_rejected": rejected(
            lambda value: value[0]["fiber_comparison"].__setitem__(
                "canonical_completion_selected_by_current_schema", True
            )
        ),
        "native_d_affine_d_conflation_rejected": rejected(
            lambda value: value[0]["completion_A"]["edges"][0][
                "affine_corridor_consumer"
            ].__setitem__(
                "native_d_equals_affine_d_crosswalk_status", "ASSUMED_EQUAL"
            )
        ),
        "false_L2_claim_rejected": rejected(
            lambda value: value[0]["claim_boundary"].__setitem__(
                "proves_positive_fixed_h0_L2", True
            )
        ),
    }
    return tests


def build() -> tuple[str, str]:
    schema_status = validate_schema_contract()
    production, synthetic, source_certificate, source_lock = load_tpc153_source()
    rows = expected_rows(production, synthetic)
    completion_text = render_jsonl(rows)
    validation = validate_completions(rows, production, synthetic)
    mutations = mutation_regressions(rows, production, synthetic)
    if not all(mutations.values()):
        raise ValueError("one or more completion mutation regressions failed")
    if source_certificate["theorem_exports"]["H1.cut_occurrence_shadow"] != (
        "PROVED_L1_STRUCTURAL"
    ):
        raise ValueError("TPC-153 cut shadow export drift")
    if source_certificate["theorem_exports"]["H1.frontier_occurrence_lift"] != (
        "NOT_TESTABLE"
    ):
        raise ValueError("TPC-153 actual-lift boundary drift")

    certificate = {
        "schema": CERTIFICATE_SCHEMA,
        "status": "PASS",
        "source": {
            **source_lock,
            "tpc154_schema_contract_validation": schema_status,
            "tpc154_schema_sha256": sha256_text(canonical_file_text(SCHEMA)),
        },
        "artifacts": {
            "formal_completions_sha256": sha256_text(completion_text),
        },
        "finite_certificate": validation,
        "formal_completion_class": {
            "name": "MAXIMAL_CURRENT_SCHEMA_FREE_COMPLETION_CLASS",
            "constraints": [
                "one or more row-separated formal children per partial occurrence",
                "exact rational forgetting weights sum to one in every source column",
                "native tuple, source h0, normalization, and formal support are echoed",
                "all absent downstream groups are explicitly populated as FORMAL_ONLY",
                "no actual-support or theorem-backed provenance condition is imposed",
            ],
            "completion_A": "one child of exact weight 1",
            "completion_B": "two row-separated children of exact weight 1/2 each",
            "same_forgetting_pushforward": True,
            "inequivalent_branch_count": True,
        },
        "theorem_exports": {
            "H1.formal_completion_fiber_nonuniqueness": "PROVED_L0_SCHEMA",
            "H1.current_artifacts_only_canonical_actual_lift": "STOP_DECLARED_ROUTE",
            "H1.augmented_actual_occurrence_lift": "NOT_TESTABLE",
            "selected_augmented_route_stopped": False,
        },
        "obstruction_scope": {
            "stopped_route": "CURRENT_ARTIFACTS_ONLY_CANONICAL_ACTUAL_LIFT_DERIVATION",
            "reason": (
                "two inequivalent conservative formal completions have the same "
                "TPC-153 forgetting pushforward on every source column"
            ),
            "actual_carrier_impossibility_proved": False,
            "two_actual_carrier_completions_constructed": False,
            "augmented_theorem_backed_route_remains_open": True,
        },
        "first_missing": {
            "node_id": "H1.theorem_backed_occurrence_provenance_crosswalk",
            "required_artifact": (
                "external theorem-backed row-level cut-to-stage-to-parent-to-"
                "physical-occurrence crosswalk, including exact edge multipliers "
                "and support status, on every ETO and FUM source"
            ),
        },
        "mutation_regression": mutations,
        "claim_boundary": {
            "formal_completion_is_actual_occurrence_lift": False,
            "actual_branch_multiplicity_identified": False,
            "actual_parent_stage_or_shift_identified": False,
            "actual_active_support_proved": False,
            "frontier_scalar_oX": False,
            "positive_fixed_h0_L2": False,
            "endpoint_1_over_400": False,
            "prime_pair_or_twin_prime_theorem": False,
        },
    }
    return completion_text, canonical_json(certificate)


def write_lf(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="\n") as stream:
        stream.write(text)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--check",
        action="store_true",
        help="compare committed deterministic artifacts without writing",
    )
    args = parser.parse_args()
    completions_text, certificate_text = build()
    outputs = {
        OUT_COMPLETIONS: completions_text,
        OUT_CERTIFICATE: certificate_text,
    }
    if args.check:
        for path, expected in outputs.items():
            if not path.is_file() or canonical_file_text(path) != expected:
                raise SystemExit(f"DRIFT: {path}")
        print("TPC-154 CHECK PASS")
    else:
        for path, text in outputs.items():
            write_lf(path, text)
        print("TPC-154 WRITE PASS")
    certificate = json.loads(certificate_text)
    print(json.dumps({
        "status": certificate["status"],
        "formal_nonuniqueness": certificate["theorem_exports"][
            "H1.formal_completion_fiber_nonuniqueness"
        ],
        "actual_lift": certificate["theorem_exports"][
            "H1.augmented_actual_occurrence_lift"
        ],
        "selected_augmented_route_stopped": certificate["theorem_exports"][
            "selected_augmented_route_stopped"
        ],
    }, sort_keys=True))


if __name__ == "__main__":
    main()
