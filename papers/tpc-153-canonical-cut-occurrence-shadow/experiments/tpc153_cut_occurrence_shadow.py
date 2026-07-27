#!/usr/bin/env python3
"""Build and audit the canonical cut-occurrence shadow of TPC-153.

The production shadow contains exactly one formal row for every nonsoft
TPC-143 cut obligation.  It is a conservative identity injection into a
partial namespace.  It is deliberately *not* the missing actual occurrence
lift.  Default mode writes deterministic UTF-8/LF artifacts; ``--check`` is
read-only and compares them byte for byte.
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
TPC135 = PAPERS / "tpc-135-tpc17-tpc18-block-frontier"
TPC143 = PAPERS / "tpc-143-frontier-occurrence-lift-contract"
TPC143_SCRIPT = TPC143 / "experiments" / "tpc143_frontier_lift_audit.py"
TPC143_OBLIGATIONS = TPC143 / "samples" / "tpc143_frontier_lift_obligations.jsonl"
TPC143_CERTIFICATE = TPC143 / "experiments" / "tpc143_frontier_lift_certificate.json"
TPC135_SCRIPT = TPC135 / "experiments" / "tpc135_domain_cover_audit.py"
SCHEMA = PAPER / "schemas" / "tpc153-cut-occurrence-shadow-v1.schema.json"
OUT_SHADOW = PAPER / "samples" / "tpc153_cut_occurrence_shadow.jsonl"
OUT_SYNTHETIC = PAPER / "samples" / "tpc153_synthetic_eto_regression.json"
OUT_CERTIFICATE = HERE / "tpc153_cut_occurrence_shadow_certificate.json"

SHADOW_SCHEMA = "tpc153-cut-occurrence-shadow-v1"
SYNTHETIC_SCHEMA = "tpc153-synthetic-eto-regression-v1"
CERTIFICATE_SCHEMA = "tpc-153-cut-occurrence-shadow-certificate-v1"
NONSOFT = {"ELIGIBLE_TAIL_OPEN", "FRONTIER_UNMAPPED"}
MISSING_GROUPS = (
    "canonical_parent_and_QD",
    "outer_zero_mode_and_QZ",
    "physical_grouping_G",
    "downstream_shift_selector",
    "affine_corridor_consumer",
)


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


def canonical_file_text(path: Path) -> str:
    return normalize_lf(path.read_text(encoding="utf-8"))


def validate_schema_contract() -> str:
    schema = json.loads(canonical_file_text(SCHEMA))
    required = {
        "schema",
        "record_scope",
        "partial_occurrence_id",
        "source_cut_path_id",
        "source_obligation_integrity_sha256",
        "cut_terminal_type",
        "required_domain",
        "lineage",
        "cut_classification",
        "cut_coefficient_data",
        "selectors",
        "support_namespaces",
        "actual_completion",
        "claim_boundary",
        "integrity_sha256",
    }
    if schema.get("$schema") != "https://json-schema.org/draft/2020-12/schema":
        raise ValueError("TPC-153 schema draft drift")
    if schema.get("$id") != "tpc153-cut-occurrence-shadow-v1.schema.json":
        raise ValueError("TPC-153 schema identifier drift")
    if set(schema.get("required", [])) != required:
        raise ValueError("TPC-153 schema required-field contract drift")
    if set(schema.get("properties", {})) != required:
        raise ValueError("TPC-153 schema property contract drift")
    if schema.get("additionalProperties") is not False:
        raise ValueError("TPC-153 schema is not closed")
    properties = schema["properties"]
    if properties["schema"].get("const") != SHADOW_SCHEMA:
        raise ValueError("TPC-153 row schema const drift")
    if properties["record_scope"].get("const") != "PRODUCTION_CURRENT_ARCHIVE":
        raise ValueError("TPC-153 production scope const drift")
    if properties["required_domain"].get("const") != (
        "ALL_NONSOFT_CUT_PATHS_ETO_PLUS_FUM"
    ):
        raise ValueError("TPC-153 all-nonsoft domain contract drift")
    return "PASS"


def load_tpc143_source() -> tuple[list[dict[str, Any]], dict[str, Any], dict[str, Any]]:
    """Rerun TPC-143 and bind its generated logical UTF-8/LF artifacts."""
    module = load_module("tpc153_source_tpc143", TPC143_SCRIPT)
    obligations_bytes, certificate_bytes = module.build()
    generated_obligations = normalize_lf(obligations_bytes.decode("utf-8"))
    generated_certificate = normalize_lf(certificate_bytes.decode("utf-8"))
    if canonical_file_text(TPC143_OBLIGATIONS) != generated_obligations:
        raise ValueError("TPC-143 obligation archive has semantic generator drift")
    if canonical_file_text(TPC143_CERTIFICATE) != generated_certificate:
        raise ValueError("TPC-143 certificate has semantic generator drift")
    certificate = json.loads(generated_certificate)
    if certificate.get("status") != "PASS":
        raise ValueError("TPC-143 source certificate is not PASS")
    if certificate["source"]["lock_mode"] != "CANONICAL_UTF8_LF_V2":
        raise ValueError("TPC-143 source is not canonically LF locked")
    rows = parse_jsonl(generated_obligations)
    source_lock = {
        "lock_mode": "CANONICAL_UTF8_LF_V2",
        "semantic_generation_chain": "PASS",
        "hashes_are_integrity_only": True,
        "tpc143_obligations_sha256": sha256_text(generated_obligations),
        "tpc143_certificate_sha256": sha256_text(generated_certificate),
        "tpc143_schema_sha256": sha256_text(canonical_file_text(
            TPC143 / "schemas" / "tpc143-frontier-lift-obligation-v1.schema.json"
        )),
    }
    return rows, certificate, source_lock


def rational_record(value: Fraction) -> dict[str, Any]:
    return {
        "ring": "Q",
        "numerator": value.numerator,
        "denominator": value.denominator,
    }


def build_shadow_row(source: dict[str, Any]) -> dict[str, Any]:
    identity = source["exact_identity"]
    cut_fields = source["cut_fields"]
    partial_id = "cut-shadow|" + hashlib.sha256(
        source["cut_path_id"].encode("utf-8")
    ).hexdigest()[:24]
    row: dict[str, Any] = {
        "schema": SHADOW_SCHEMA,
        "record_scope": "PRODUCTION_CURRENT_ARCHIVE",
        "partial_occurrence_id": partial_id,
        "source_cut_path_id": source["cut_path_id"],
        "source_obligation_integrity_sha256": source["integrity_sha256"],
        "cut_terminal_type": source["cut_terminal_type"],
        "required_domain": "ALL_NONSOFT_CUT_PATHS_ETO_PLUS_FUM",
        "lineage": {
            "packet_scope": copy.deepcopy(identity["packet_scope"]),
            "native_tuple": list(identity["native_tuple"]),
            "upstream_path_id": identity["upstream_path_id"],
        },
        "cut_classification": {
            "source_cut_fields_status": cut_fields["status"],
            "block": copy.deepcopy(cut_fields["block"]),
            "D0": cut_fields["D0"],
            "boundary_rule": cut_fields["boundary_rule"],
            "frontier_reason": cut_fields["frontier_reason"],
        },
        "cut_coefficient_data": {
            "native_coefficient_ast": copy.deepcopy(
                cut_fields["native_coefficient_ast"]
            ),
            "native_constraint_witnesses": copy.deepcopy(
                cut_fields["native_constraint_witnesses"]
            ),
            "dyadic_edge_multiplier_ast": copy.deepcopy(
                cut_fields["dyadic_edge_multiplier_ast"]
            ),
            "shadow_edge_weight": rational_record(Fraction(1)),
            "numeric_coefficient_nonzero_status": "UNDECIDED",
        },
        "selectors": {
            "cut_selector": {
                "map_id": "P_h0_cut",
                "h0": identity["packet_scope"]["h0"],
                "action": "IDENTITY",
                "status": "PROVED_L1",
            },
            "downstream_selector": {
                "status": "NOT_PRESENT",
                "not_inferred_from_cut_selector": True,
            },
        },
        "support_namespaces": {
            "formal_support_envelope": "PRESENT",
            "canonical_parent_carrier": "NOT_PRESENT",
            "actual_active_support": "UNDECIDED",
        },
        "actual_completion": {
            "actual_occurrence_id": None,
            "actual_branch_count": None,
            "status": "NOT_PRESENT",
            "forgotten_field_groups": list(MISSING_GROUPS),
        },
        "claim_boundary": {
            "is_actual_occurrence": False,
            "proves_actual_one_to_many_branching": False,
            "proves_active_nonzero_support": False,
            "proves_positive_fixed_h0_L2": False,
            "proves_twin_prime_theorem": False,
        },
    }
    row["integrity_sha256"] = digest_object(row)
    return row


def source_index(source_rows: list[dict[str, Any]]) -> dict[str, dict[str, Any]]:
    index = {row["cut_path_id"]: row for row in source_rows}
    if len(index) != len(source_rows):
        raise ValueError("TPC-143 source has duplicate cut-path identifiers")
    return index


def validate_shadow(
    rows: list[dict[str, Any]], source_rows: list[dict[str, Any]]
) -> dict[str, Any]:
    sources = source_index(source_rows)
    ids = [row["partial_occurrence_id"] for row in rows]
    cut_ids = [row["source_cut_path_id"] for row in rows]
    if len(rows) != len(source_rows):
        raise ValueError("shadow is not total on all nonsoft source rows")
    if len(ids) != len(set(ids)):
        raise ValueError("partial occurrence identifier is duplicated")
    if len(cut_ids) != len(set(cut_ids)) or set(cut_ids) != set(sources):
        raise ValueError("source cut path is deleted, duplicated, or invented")

    column_sums: dict[str, Fraction] = {}
    terminal_counts = {terminal: 0 for terminal in sorted(NONSOFT)}
    for row in rows:
        cut_id = row["source_cut_path_id"]
        expected = build_shadow_row(sources[cut_id])
        if row != expected:
            raise ValueError(f"shadow row does not exactly descend: {cut_id}")
        unsigned = dict(row)
        recorded_hash = unsigned.pop("integrity_sha256")
        if recorded_hash != digest_object(unsigned):
            raise ValueError(f"shadow integrity failure: {cut_id}")
        terminal = row["cut_terminal_type"]
        if terminal not in NONSOFT:
            raise ValueError("nonsoft shadow contains a soft terminal")
        terminal_counts[terminal] += 1
        weight = row["cut_coefficient_data"]["shadow_edge_weight"]
        if weight["ring"] != "Q" or weight["denominator"] <= 0:
            raise ValueError("shadow weight is not a normalized rational")
        column_sums[cut_id] = column_sums.get(cut_id, Fraction()) + Fraction(
            weight["numerator"], weight["denominator"]
        )
        if row["actual_completion"]["status"] != "NOT_PRESENT":
            raise ValueError("partial shadow was promoted to actual completion")
        if row["support_namespaces"]["actual_active_support"] != "UNDECIDED":
            raise ValueError("formal support was promoted to active support")
        if row["selectors"]["downstream_selector"]["status"] != "NOT_PRESENT":
            raise ValueError("cut selector was promoted downstream")
        if any(row["claim_boundary"].values()):
            raise ValueError("shadow row contains a forbidden positive claim")
    if any(value != 1 for value in column_sums.values()):
        raise ValueError("shadow column conservation failed")
    return {
        "source_column_count": len(column_sums),
        "shadow_row_count": len(rows),
        "unique_partial_occurrence_ids": len(set(ids)),
        "terminal_type_counts": terminal_counts,
        "every_column_sum": rational_record(Fraction(1)),
        "one_transpose_S_equals_one_transpose": True,
    }


def build_synthetic_eto() -> dict[str, Any]:
    """Exercise the ETO branch without asserting a current production row."""
    module = load_module("tpc153_source_tpc135", TPC135_SCRIPT)
    X = 1 << 84
    R = 1 << 21
    V = 1 << 10
    j_L = 38
    j_K = 46
    D0 = module.canonical_maximal_d0(X, R, V, j_L, j_K)
    if D0 <= 0 or module.classify_block(X, R, V, j_L, j_K, D0) != "ELIGIBLE":
        raise ValueError("TPC-135 synthetic eligible policy regression failed")
    fixture = {
        "schema": SYNTHETIC_SCHEMA,
        "fixture_scope": "SYNTHETIC_L0_ONLY",
        "source_policy": "tpc135-large-scale-eligible-case-regression",
        "policy_inputs": {
            "X": X,
            "R": R,
            "V": V,
            "j_L": j_L,
            "j_K": j_K,
            "D0": D0,
        },
        "synthetic_terminal_type": "ELIGIBLE_TAIL_OPEN",
        "shadow_edge_weight": rational_record(Fraction(1)),
        "exercises_all_nonsoft_union": True,
        "belongs_to_current_production_census": False,
        "proves_asymptotic_ETO_existence": False,
        "proves_actual_occurrence_lift": False,
    }
    fixture["integrity_sha256"] = digest_object(fixture)
    return fixture


def validate_synthetic_eto(fixture: dict[str, Any]) -> None:
    if fixture != build_synthetic_eto():
        raise ValueError("synthetic ETO regression drift")
    if fixture["fixture_scope"] != "SYNTHETIC_L0_ONLY":
        raise ValueError("synthetic ETO fixture lost its L0 boundary")
    if fixture["belongs_to_current_production_census"]:
        raise ValueError("synthetic ETO fixture entered production census")
    if fixture["proves_asymptotic_ETO_existence"]:
        raise ValueError("synthetic block was promoted asymptotically")


def mutation_regressions(
    rows: list[dict[str, Any]], source_rows: list[dict[str, Any]]
) -> dict[str, bool]:
    if not rows:
        raise ValueError("mutation regressions need a production row")

    def rehash(row: dict[str, Any]) -> None:
        unsigned = dict(row)
        unsigned.pop("integrity_sha256", None)
        row["integrity_sha256"] = digest_object(unsigned)

    def rejected(mutator) -> bool:
        trial = copy.deepcopy(rows)
        mutator(trial)
        for row in trial:
            rehash(row)
        try:
            validate_shadow(trial, source_rows)
        except ValueError:
            return True
        return False

    tests = {
        "deleted_nonsoft_row_rejected": rejected(lambda value: value.pop()),
        "duplicated_nonsoft_row_rejected": rejected(
            lambda value: value.append(copy.deepcopy(value[0]))
        ),
        "terminal_source_drift_rejected": rejected(
            lambda value: value[0].__setitem__(
                "cut_terminal_type",
                (
                    "ELIGIBLE_TAIL_OPEN"
                    if value[0]["cut_terminal_type"] == "FRONTIER_UNMAPPED"
                    else "FRONTIER_UNMAPPED"
                ),
            )
        ),
        "nonunit_shadow_weight_rejected": rejected(
            lambda value: value[0]["cut_coefficient_data"].__setitem__(
                "shadow_edge_weight", rational_record(Fraction(1, 2))
            )
        ),
        "h0_drift_rejected": rejected(
            lambda value: value[0]["lineage"]["packet_scope"].__setitem__(
                "h0", value[0]["lineage"]["packet_scope"]["h0"] + 2
            )
        ),
        "normalization_drift_rejected": rejected(
            lambda value: value[0]["lineage"]["packet_scope"].__setitem__(
                "physical_normalization", "fabricated-normalization"
            )
        ),
        "active_support_promotion_rejected": rejected(
            lambda value: value[0]["support_namespaces"].__setitem__(
                "actual_active_support", "PRESENT"
            )
        ),
        "actual_completion_promotion_rejected": rejected(
            lambda value: value[0]["actual_completion"].__setitem__(
                "status", "PRESENT"
            )
        ),
        "downstream_selector_promotion_rejected": rejected(
            lambda value: value[0]["selectors"]["downstream_selector"].__setitem__(
                "status", "PROVED_L1"
            )
        ),
        "false_L2_claim_rejected": rejected(
            lambda value: value[0]["claim_boundary"].__setitem__(
                "proves_positive_fixed_h0_L2", True
            )
        ),
    }
    synthetic = build_synthetic_eto()
    promoted = copy.deepcopy(synthetic)
    promoted["belongs_to_current_production_census"] = True
    unsigned = dict(promoted)
    unsigned.pop("integrity_sha256")
    promoted["integrity_sha256"] = digest_object(unsigned)
    try:
        validate_synthetic_eto(promoted)
    except ValueError:
        tests["synthetic_ETO_production_promotion_rejected"] = True
    else:
        tests["synthetic_ETO_production_promotion_rejected"] = False
    return tests


def build() -> tuple[str, str, str]:
    schema_status = validate_schema_contract()
    source_rows, source_certificate, source_lock = load_tpc143_source()
    rows = [build_shadow_row(row) for row in source_rows]
    shadow_text = render_jsonl(rows)
    shadow_validation = validate_shadow(rows, source_rows)
    synthetic = build_synthetic_eto()
    validate_synthetic_eto(synthetic)
    synthetic_text = canonical_json(synthetic)
    mutations = mutation_regressions(rows, source_rows)
    if not all(mutations.values()):
        raise ValueError("one or more shadow mutation regressions failed")

    production_counts = shadow_validation["terminal_type_counts"]
    if production_counts != {
        "ELIGIBLE_TAIL_OPEN": 0,
        "FRONTIER_UNMAPPED": 2988,
    }:
        raise ValueError("unexpected current production ETO/FUM census")
    if source_certificate["census"]["nonsoft_path_count"] != len(rows):
        raise ValueError("TPC-143 census does not match the shadow")

    certificate = {
        "schema": CERTIFICATE_SCHEMA,
        "status": "PASS",
        "source": {
            **source_lock,
            "tpc153_schema_contract_validation": schema_status,
            "tpc153_schema_sha256": sha256_text(canonical_file_text(SCHEMA)),
        },
        "artifacts": {
            "production_shadow_sha256": sha256_text(shadow_text),
            "synthetic_eto_regression_sha256": sha256_text(synthetic_text),
        },
        "census": {
            "production_nonsoft_source_columns": len(source_rows),
            "production_shadow_rows": len(rows),
            "production_terminal_type_counts": production_counts,
            "synthetic_ETO_rows": 1,
            "synthetic_ETO_in_production_census": False,
            "finite_empty_ETO_is_asymptotic_absence": False,
        },
        "matrix_certificate": {
            "map_id": "S_X_cut_occurrence_shadow",
            "domain": "ALL_NONSOFT_CUT_PATHS_ETO_PLUS_FUM",
            "codomain": "PARTIAL_CUT_OCCURRENCE_NAMESPACE",
            "entry_formula": "S[cut-shadow(c),c]=1; all other entries=0",
            "row_separated": True,
            "injective": True,
            "column_conservative": True,
            "identity": "ONE_TRANSPOSE_S_X_EQUALS_ONE_TRANSPOSE",
            "validation": shadow_validation,
        },
        "universal_property": {
            "status": "PROVED_L0_FORMAL",
            "statement": (
                "Every metadata-faithful actual completion with forgetting map "
                "q must satisfy q_pushforward(L_X)=S_X; this does not construct L_X."
            ),
            "actual_completion_existence_assumed": True,
            "actual_completion_constructed": False,
        },
        "theorem_exports": {
            "H1.cut_occurrence_shadow": "PROVED_L1_STRUCTURAL",
            "H1.frontier_occurrence_lift": "NOT_TESTABLE",
            "current_schema_only_actual_lift_derivation": "STOP_DECLARED_ROUTE",
            "selected_augmented_route_stopped": False,
        },
        "first_missing": {
            "node_id": "H1.theorem_backed_occurrence_provenance_crosswalk",
            "required_artifact": (
                "row-separated one-to-many occurrence edges on every ETO and "
                "FUM cut path with source-backed parent, stage, multiplier, "
                "native, h0, normalization, and support-status lineage"
            ),
        },
        "mutation_regression": mutations,
        "claim_boundary": {
            "shadow_is_actual_occurrence_lift": False,
            "actual_one_to_many_branching_proved": False,
            "canonical_parent_or_stage_lineage_proved": False,
            "actual_active_support_proved": False,
            "frontier_scalar_oX": False,
            "positive_fixed_h0_L2": False,
            "endpoint_1_over_400": False,
            "prime_pair_or_twin_prime_theorem": False,
        },
    }
    return shadow_text, synthetic_text, canonical_json(certificate)


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
    shadow_text, synthetic_text, certificate_text = build()
    outputs = {
        OUT_SHADOW: shadow_text,
        OUT_SYNTHETIC: synthetic_text,
        OUT_CERTIFICATE: certificate_text,
    }
    if args.check:
        for path, expected in outputs.items():
            if not path.is_file() or canonical_file_text(path) != expected:
                raise SystemExit(f"DRIFT: {path}")
        print("TPC-153 CHECK PASS")
    else:
        for path, text in outputs.items():
            write_lf(path, text)
        print("TPC-153 WRITE PASS")
    certificate = json.loads(certificate_text)
    print(json.dumps({
        "status": certificate["status"],
        "production": certificate["census"]["production_terminal_type_counts"],
        "shadow": certificate["theorem_exports"]["H1.cut_occurrence_shadow"],
        "actual_lift": certificate["theorem_exports"]["H1.frontier_occurrence_lift"],
    }, sort_keys=True))


if __name__ == "__main__":
    main()
