#!/usr/bin/env python3
"""Independent read-only verifier for the finite TPC-204 certificate.

This file imports neither ``build_tpc204.py`` nor the authoritative
materialization module.  Its frozen constants, source checks, exact-schema
implementation, candidate-row digests, and mutation runner provide a
separate failure mode from the producer.
"""

from __future__ import annotations

import argparse
import copy
import hashlib
import json
from pathlib import Path
from typing import Any


HERE = Path(__file__).resolve().parent
PAPER = HERE.parent
REPO = PAPER.parents[1]

PAYLOAD_PATH = HERE / "tpc204_source_locked_production_registry_crosswalk.json"
AUDIT_PATH = (
    HERE / "tpc204_source_locked_production_registry_crosswalk_audit.json"
)
PAYLOAD_SCHEMA_PATH = (
    PAPER
    / "schemas"
    / "tpc204-source-locked-production-registry-crosswalk-v1.schema.json"
)
AUDIT_SCHEMA_PATH = (
    PAPER
    / "schemas"
    / "tpc204-source-locked-production-registry-crosswalk-audit-v1.schema.json"
)
MANIFEST_PATH = HERE / "tpc204_certificate_manifest.json"

SCHEMA_URI = "https://json-schema.org/draft/2020-12/schema"
PAYLOAD_SCHEMA_ID = (
    "tpc204-source-locked-production-registry-crosswalk-v1.schema.json"
)
AUDIT_SCHEMA_ID = (
    "tpc204-source-locked-production-registry-crosswalk-audit-v1.schema.json"
)
CORPUS_ID = "TPC204_DECLARED_PLAUSIBLE_PRODUCTION_CROSSWALK_CORPUS_V1"
STOP_CELL = f"{CORPUS_ID}=STOP_SCOPED"

PAYLOAD_RAW_SHA256 = (
    "3d6e7aab3d9e165cc1d6f822f7146feb0d0fddbc1e976ed4312739b0418f4ff2"
)
AUDIT_RAW_SHA256 = (
    "b26a90b565c0aa13a871cf15707c3bd2f63e47734aba992e154cf255ec3d7f39"
)
PAYLOAD_SCHEMA_RAW_SHA256 = (
    "0d7b8512176166bc085a6f7cbaca29a4355b3825917b5924db469be6d3609585"
)
AUDIT_SCHEMA_RAW_SHA256 = (
    "63ae0ac9606cc81292935d147c71dd14c2c8b8a060aa01217effb33aa241fb17"
)

FORMULA_TYPES = [
    {
        "id": "CORE_TERMINAL_BLOCK",
        "domain": "N<t(z)<=2N",
        "normalization": "q/N",
    },
    {
        "id": "CORE_CUMULATIVE_PREFIX",
        "domain": "0<t(z)<=T",
        "normalization": "q/T",
    },
    {
        "id": "PHYSICAL_PACKET_PREFIX",
        "domain": "z in I_xi_X and z<=T",
        "normalization": "UNNORMALIZED_INSIDE_OUTER_PACKET_SUM",
    },
]

PRODUCTION_AXES = [
    "named_production_atom",
    "packet_schedule",
    "common_X_N_q_ranges",
    "uniform_constant_C",
    "positive_sigma",
    "target_normalization_selection",
    "complete_physical_loss_ledger",
]

GATE_ORDER = [
    "OBJECT_TYPE_ELIGIBILITY",
    "NAMED_PRODUCTION_ATOM",
    "EXACT_PACKET_SCHEDULE",
    "COMMON_X_N_Q_RANGES",
    "UNIFORM_CONSTANT_C",
    "POSITIVE_SIGMA",
    "TARGET_NORMALIZATION_SELECTION",
    "COMPLETE_PHYSICAL_LOSS_LEDGER",
    "CORE_TERMINAL_BLOCK_CROSSWALK",
    "CORE_CUMULATIVE_PREFIX_CROSSWALK",
    "PHYSICAL_PACKET_PREFIX_CROSSWALK",
]

STOP_SCOPED = [
    "TPC181_PHASE_METRIC_UNCONTROLLED_ATOMIC=STOP_SCOPED",
    "TPC187_SIZE_ONLY_LOCAL_OSCILLATION_METHOD=STOP_SCOPED",
    "TPC190_PARSEVAL_CHEBYSHEV_TO_PRESCRIBED_ATOM=STOP_SCOPED",
    "TPC193_DECLARED_CANDIDATE_MECHANISM_CORPUS_V1=STOP_SCOPED",
    "FACTORWISE_SINGLE_MOBIUS_FOURIER_TO_LITERAL_PRODUCT=STOP_SCOPED",
    "ONE_FUNCTION_PRETENTIOUSNESS_DIRECT_APPLICATION_TO_CZ=STOP_SCOPED",
    STOP_CELL,
]

EXPECTED_CANDIDATES = [
    (
        "H9.phase_cell_registry",
        "EMPTY_SOURCE_LOCKED_REGISTRY_SLOT",
        "TPC180.payload#/candidate_registry",
        None,
        "8f24347d88e449c523931c87cf8be120ce3682ffc7866bc67c874d806cde79eb",
    ),
    (
        "TT26.RATIONAL_PERIODIC_ATOM",
        "TERMINAL_BLOCK_LOG_POWER_THEOREM",
        "TPC193.payload#/candidate_inventory/1",
        "CORE_TERMINAL_BLOCK",
        "2828ca9817487f9f69c12251198348bcb81e2c5abd044a57a62e4b1572f6e08c",
    ),
    (
        "A159.DYADIC_SHADOW_ALMOST_ENDPOINT_PREFIX",
        "CUMULATIVE_PREFIX_OUTSIDE_SHADOW_THEOREM",
        "TPC159.main#thm:main+eq:main",
        "CORE_CUMULATIVE_PREFIX",
        "8664e6a36572c7e86e93bc88ac64b3152ddcf864f87f00be18e03469f4f8f199",
    ),
    (
        "A167.DIRECT_ADDITIVE_TWIST_PHASE_L2",
        "TERMINAL_BLOCK_PHASE_L2_THEOREM",
        "TPC167.main#thm:parseval+eq:power",
        "CORE_TERMINAL_BLOCK",
        "4da9a88f761324631b2d57354f6668b3242e4e262a066f38715da428d68c33a8",
    ),
    (
        "TPC183.N_EQUALS_T_SPECIALIZATION_PROPOSAL",
        "INVALID_TERMINAL_TO_CUMULATIVE_SPECIALIZATION",
        "TPC183.payload#/theorem",
        None,
        "74027d3810aad39d88b3e56b87cdddd972da81ad0743b55b0c07a3d7caf2ceeb",
    ),
    (
        "O161.BAD_ENDPOINT_POINTWISE_FIXED_ATOM_CONTRACT",
        "VERBAL_CUMULATIVE_ALL_PREFIX_TARGET_WITHOUT_NAMED_ATOM_VALUE",
        "TPC184.payload#/result",
        None,
        "89421bc5000c9485b1dd650b89c3f3ab30301601f8144a0faa381035a364a0e2",
    ),
    (
        "O161.DIRECT_ADDITIVE_TWIST_FIXED_ATOM_CONTRACT",
        "VERBAL_DIRECT_TARGET_WITHOUT_LITERAL_PREFIX_DOMAIN",
        "TPC189.payload#/result",
        None,
        "65414d6e4838e565dcb2464ef61fb319d32784d5cf492bdbb61224e3c62025be",
    ),
    (
        "TW25.LOG_TWISTED_AFFINE",
        "LOG_WEIGHTED_FIXED_ATOM_AFFINE_THEOREM",
        "TPC193.payload#/candidate_inventory/0",
        None,
        "2e57331892fae1bc0a6e8cc0eb44338e3e53b18df9833f8c6bbab5150376c13f",
    ),
    (
        "PHYSICAL_PACKET_PREFIX",
        "RESOLVED_PER_PACKET_UNNORMALIZED_PHYSICAL_PREFIX",
        "TPC194.payload#/finite_certificate/resolved_packet_formula",
        "PHYSICAL_PACKET_PREFIX",
        "4d35646610537c07180f4a004b17423757a7cdb1eaa26db2f4fa58e5903de5a2",
    ),
]

EXCLUSION_LEDGER_DIGEST = (
    "c7251c8b10408cabfd22745d529e5b98937108f3e7c35098a4331800d00bb3e1"
)
SOURCE_LOCKS_DIGEST = (
    "e4dd35a035a376118c296e6ea450cd31ea2bf5096f275270e821cc2af5853303"
)
FORMULA_REGISTRY_DIGEST = (
    "742fc459a259a84e5891e7546468d18b95fbf19d820b73d0039989c19381ee4b"
)
STOP_SCOPED_DIGEST = (
    "dcc724177f1a95a286a8328a657a6ad51286951916935cd7d29b1522986718cc"
)
CANDIDATE_UNIVERSE_DIGEST = (
    "ecbb4a7ab23399428e7f3c4f45212727f27c484d5bf3e66116ee7509daa31e47"
)

EXPECTED_SOURCE_PATHS = [
    (
        "TPC159.audit",
        "papers/tpc-159-dyadic-shadow-prefix-lifting/"
        "experiments/tpc159_dyadic_shadow_audit.json",
    ),
    (
        "TPC159.main",
        "papers/tpc-159-dyadic-shadow-prefix-lifting/main.tex",
    ),
    (
        "TPC167.audit",
        "papers/tpc-167-direct-additive-twist-parseval/"
        "experiments/tpc167_parseval_audit.json",
    ),
    (
        "TPC167.main",
        "papers/tpc-167-direct-additive-twist-parseval/main.tex",
    ),
    (
        "TPC180.payload",
        "papers/tpc-180-production-phase-registry-census/"
        "experiments/tpc180_phase_registry_census.json",
    ),
    (
        "TPC183.payload",
        "papers/tpc-183-pointwise-parent-interface-comparison/"
        "experiments/tpc183_pointwise_parent_interface_comparison.json",
    ),
    (
        "TPC184.payload",
        "papers/tpc-184-bad-endpoint-literal-target-contract/"
        "experiments/tpc184_bad_endpoint_literal_target_contract.json",
    ),
    (
        "TPC189.payload",
        "papers/tpc-189-direct-twist-literal-target-contract/"
        "experiments/tpc189_direct_twist_literal_target_contract.json",
    ),
    (
        "TPC193.main",
        "papers/tpc-193-literal-fixed-atom-candidate-mechanism-gate/main.tex",
    ),
    (
        "TPC193.payload",
        "papers/tpc-193-literal-fixed-atom-candidate-mechanism-gate/"
        "experiments/tpc193_literal_fixed_atom_candidate_mechanism_gate.json",
    ),
    (
        "TPC194.hardener",
        "papers/tpc-194-maximal-source-backed-direct-prefix/"
        "experiments/tpc194_certificate_hardening.py",
    ),
    (
        "TPC194.main",
        "papers/tpc-194-maximal-source-backed-direct-prefix/main.tex",
    ),
    (
        "TPC194.manifest",
        "papers/tpc-194-maximal-source-backed-direct-prefix/"
        "experiments/tpc194_certificate_hardening_manifest.json",
    ),
    (
        "TPC194.payload",
        "papers/tpc-194-maximal-source-backed-direct-prefix/"
        "experiments/tpc194_maximal_source_backed_direct_prefix.json",
    ),
    (
        "TPC203.payload",
        "papers/tpc-203-mvp10-direct-pointwise-route-decision/"
        "experiments/tpc203_mvp10_direct_pointwise_route_decision.json",
    ),
]

ACTIVE_ARTIFACTS = [
    "papers/tpc-204-source-locked-production-registry-crosswalk/"
    "experiments/build_tpc204.py",
    "papers/tpc-204-source-locked-production-registry-crosswalk/"
    "experiments/tpc204_source_locked_production_registry_crosswalk.py",
    "papers/tpc-204-source-locked-production-registry-crosswalk/"
    "experiments/tpc204_independent_checker.py",
    "papers/tpc-204-source-locked-production-registry-crosswalk/"
    "experiments/tpc204_source_locked_production_registry_crosswalk.json",
    "papers/tpc-204-source-locked-production-registry-crosswalk/"
    "experiments/tpc204_source_locked_production_registry_crosswalk_audit.json",
    "papers/tpc-204-source-locked-production-registry-crosswalk/"
    "schemas/tpc204-source-locked-production-registry-crosswalk-v1.schema.json",
    "papers/tpc-204-source-locked-production-registry-crosswalk/"
    "schemas/tpc204-source-locked-production-registry-crosswalk-audit-v1.schema.json",
    "papers/tpc-204-source-locked-production-registry-crosswalk/README.md",
    "papers/tpc-204-source-locked-production-registry-crosswalk/main.tex",
    "papers/tpc-204-source-locked-production-registry-crosswalk/references.bib",
    "papers/tpc-204-source-locked-production-registry-crosswalk/"
    "tpc-204-source-locked-production-registry-crosswalk.pdf",
]

BASE_MUTATIONS = [
    "extra_top_level",
    "drop_decision",
    "bool_for_paper",
    "integer_for_authorization_flag",
    "drop_candidate",
    "duplicate_candidate",
    "change_axis_status",
    "corrupt_formula_tuple",
    "source_hash_drift",
    "drop_stop_cell",
    "promote_claim_flag",
    "advance_first_mismatch",
]

SEMANTIC_MUTATIONS = [
    "authorization_implies_direct_trigger",
    "authorization_implies_reopen",
    "promote_verdict_to_unique",
    "forge_complete_count",
    "forge_unique_candidate_id",
    "drop_candidate",
    "add_synthetic_candidate",
    "duplicate_candidate_id",
    "reorder_candidates",
    "change_inclusion_predicate",
    "drop_excluded_record",
    "forge_universe_digest",
    "forge_source_lock_hash",
    "promote_hash_to_theorem_evidence",
    "fabricate_named_atom",
    "fabricate_packet_schedule",
    "fabricate_common_ranges",
    "fabricate_uniform_C",
    "treat_log_saving_as_positive_sigma",
    "select_normalization_by_fiat",
    "mark_loss_ledger_complete",
    "drop_axis_row",
    "duplicate_axis_row",
    "advance_first_mismatch",
    "clear_first_mismatch",
    "merge_terminal_and_cumulative",
    "merge_terminal_and_physical",
    "merge_cumulative_and_physical",
    "corrupt_terminal_tuple",
    "corrupt_cumulative_tuple",
    "corrupt_physical_tuple",
    "drop_crosswalk_row",
    "set_crosswalk_exact",
    "direct_trigger_passed",
    "fixed_atom_decay_obtained",
    "grant_endpoint_credit",
    "pay_strict_one_over_400",
    "promote_L2",
    "stop_bad_endpoint_parent",
    "stop_direct_parent",
    "stop_global_architecture",
    "unstop_TPC193_V1",
    "global_nonexistence_claim",
    "bool_for_candidate_count",
    "integer_for_boolean_claim",
]

STRICT_TYPE_MUTATIONS = [
    "authorization_true_to_integer",
    "authorization_false_to_integer",
    "route_false_to_integer",
    "endpoint_integer_to_boolean",
    "formula_false_to_integer",
]


class VerificationError(RuntimeError):
    """Raised when the frozen independent contract is violated."""


class DuplicateKeyError(ValueError):
    """Raised when a JSON object repeats a key."""


def require(condition: bool, code: str) -> None:
    if not condition:
        raise VerificationError(code)


def strict_value_equal(actual: Any, expected: Any) -> bool:
    if type(actual) is not type(expected):
        return False
    if type(actual) is dict:
        if set(actual) != set(expected):
            return False
        return all(
            strict_value_equal(actual[key], expected[key]) for key in actual
        )
    if type(actual) is list:
        if len(actual) != len(expected):
            return False
        return all(
            strict_value_equal(left, right)
            for left, right in zip(actual, expected)
        )
    return actual == expected


def strict_equal(actual: Any, expected: Any, code: str) -> None:
    require(strict_value_equal(actual, expected), code)


def no_duplicate_pairs(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
    result: dict[str, Any] = {}
    for key, value in pairs:
        if key in result:
            raise DuplicateKeyError(f"duplicate JSON key: {key}")
        result[key] = value
    return result


def reject_nonfinite(token: str) -> None:
    raise ValueError(f"nonfinite JSON number: {token}")


def load_json(path: Path) -> Any:
    return json.loads(
        path.read_text(encoding="utf-8-sig"),
        object_pairs_hook=no_duplicate_pairs,
        parse_constant=reject_nonfinite,
    )


def pretty_canonical(value: Any) -> str:
    return (
        json.dumps(
            value,
            ensure_ascii=False,
            sort_keys=True,
            indent=2,
            allow_nan=False,
        )
        + "\n"
    )


def compact_canonical(value: Any) -> str:
    return json.dumps(
        value,
        ensure_ascii=False,
        sort_keys=True,
        separators=(",", ":"),
        allow_nan=False,
    )


def value_digest(value: Any) -> str:
    return hashlib.sha256(compact_canonical(value).encode("utf-8")).hexdigest()


def raw_digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def normalized_text_digest(path: Path) -> str:
    text = path.read_text(encoding="utf-8-sig")
    normalized = text.replace("\r\n", "\n").replace("\r", "\n")
    return hashlib.sha256(normalized.encode("utf-8")).hexdigest()


def require_repo_path(relative: str, code: str) -> Path:
    require(type(relative) is str and relative != "", f"{code}:TYPE")
    root = REPO.resolve()
    target = (REPO / relative).resolve()
    require(target == root or root in target.parents, f"{code}:ESCAPE")
    require(target.is_file(), f"{code}:MISSING")
    return target


def exact_schema(value: Any, schema_id: str | None = None) -> dict[str, Any]:
    def rec(item: Any) -> dict[str, Any]:
        if type(item) is dict:
            return {
                "type": "object",
                "properties": {key: rec(val) for key, val in item.items()},
                "required": list(item.keys()),
                "additionalProperties": False,
            }
        if type(item) is list:
            return {
                "type": "array",
                "prefixItems": [rec(val) for val in item],
                "items": False,
                "minItems": len(item),
                "maxItems": len(item),
            }
        if type(item) is bool:
            return {"type": "boolean", "const": item}
        if type(item) is int:
            return {"type": "integer", "const": item}
        if type(item) is float:
            return {"type": "number", "const": item}
        if type(item) is str:
            return {"type": "string", "const": item}
        if item is None:
            return {"type": "null", "const": None}
        raise TypeError(f"unsupported value type: {type(item)}")

    schema = rec(value)
    schema["$schema"] = SCHEMA_URI
    if schema_id is not None:
        schema["$id"] = schema_id
    return schema


def schema_accepts(schema: dict[str, Any], value: Any) -> bool:
    expected_type = schema.get("type")
    if expected_type == "object":
        if type(value) is not dict:
            return False
        if schema.get("additionalProperties") is not False:
            return False
        if set(value) != set(schema["required"]):
            return False
        properties = schema["properties"]
        if set(properties) != set(value):
            return False
        return all(schema_accepts(properties[key], value[key]) for key in value)
    if expected_type == "array":
        if type(value) is not list:
            return False
        if len(value) != schema["minItems"] or len(value) != schema["maxItems"]:
            return False
        if schema.get("items") is not False:
            return False
        if len(schema["prefixItems"]) != len(value):
            return False
        return all(
            schema_accepts(subschema, item)
            for subschema, item in zip(schema["prefixItems"], value)
        )
    if expected_type == "boolean":
        return type(value) is bool and value == schema["const"]
    if expected_type == "integer":
        return type(value) is int and value == schema["const"]
    if expected_type == "number":
        return type(value) is float and value == schema["const"]
    if expected_type == "string":
        return type(value) is str and value == schema["const"]
    if expected_type == "null":
        return value is None and schema.get("const") is None
    return False


def normalize_required_order(value: Any) -> Any:
    if type(value) is dict:
        normalized: dict[str, Any] = {}
        for key, item in value.items():
            if key == "required":
                normalized[key] = sorted(item)
            else:
                normalized[key] = normalize_required_order(item)
        return normalized
    if type(value) is list:
        return [normalize_required_order(item) for item in value]
    return value


def verify_generated_file(
    path: Path,
    expected_raw_sha256: str,
    code: str,
) -> Any:
    value = load_json(path)
    strict_equal(
        path.read_text(encoding="utf-8"),
        pretty_canonical(value),
        f"{code}:NONCANONICAL",
    )
    strict_equal(raw_digest(path), expected_raw_sha256, f"{code}:RAW_HASH")
    return value


def verify_source_locks(payload: dict[str, Any]) -> None:
    rows = payload["source_locks"]
    require(type(rows) is list and len(rows) == 15, "SOURCE_LOCK_COUNT")
    expected_pairs = EXPECTED_SOURCE_PATHS
    actual_pairs = [(row["source_id"], row["path"]) for row in rows]
    strict_equal(actual_pairs, expected_pairs, "SOURCE_LOCK_ORDER_OR_PATH")
    strict_equal(
        value_digest(rows),
        SOURCE_LOCKS_DIGEST,
        "SOURCE_LOCK_LEDGER_DIGEST",
    )
    for row in rows:
        strict_equal(
            set(row),
            {
                "source_id",
                "path",
                "canonical_utf8_lf_sha256",
                "hash_semantics",
            },
            f"SOURCE_LOCK_KEYS:{row.get('source_id')}",
        )
        strict_equal(
            row["hash_semantics"],
            "INTEGRITY_ONLY",
            f"SOURCE_LOCK_MODE:{row['source_id']}",
        )
        target = require_repo_path(row["path"], f"SOURCE_LOCK:{row['source_id']}")
        strict_equal(
            normalized_text_digest(target),
            row["canonical_utf8_lf_sha256"],
            f"SOURCE_LOCK_HASH:{row['source_id']}",
        )


def verify_payload_semantics(
    payload: dict[str, Any],
    *,
    enforce_frozen_digest: bool,
) -> None:
    strict_equal(
        payload["schema"],
        "tpc-204-source-locked-production-registry-crosswalk-v1",
        "SCHEMA",
    )
    strict_equal(payload["paper"], 204, "PAPER")
    require(type(payload["paper"]) is int, "PAPER_TYPE")
    strict_equal(
        payload["classification"],
        "PRODUCTION_REGISTRY_CROSSWALK_CENSUS_L1",
        "CLASSIFICATION",
    )
    strict_equal(
        payload["authorization"],
        {
            "authorization_record": (
                "USER_EXPLICIT_FINITE_TPC204_AUTHORIZATION_2026_07_30"
            ),
            "authorized_scope": (
                "FINITE_EXACT_MATCHING_OR_FIRST_MISMATCH_CROSSWALK_AUDIT"
            ),
            "implies_any_reopen_trigger": False,
            "implies_direct_trigger_pass": False,
            "is_mathematical_evidence": False,
            "tpc204_authorized": True,
        },
        "AUTHORIZATION",
    )
    strict_equal(
        payload["snapshot"],
        {
            "canonical_candidate_order": (
                "SOURCE_LINEAGE_THEN_LITERAL_OBJECT_ROLE"
            ),
            "corpus_id": CORPUS_ID,
            "corpus_scope": (
                "EXACT_DECLARED_DIRECT_PRODUCTION_LINEAGE_OBJECTS_ONLY"
            ),
            "date": "2026-07-30",
            "discovery_rule": (
                "EXPLICIT_SOURCE_BINDINGS_AND_CANONICAL_OBJECT_SELECTORS"
            ),
            "future_sources_automatically_included": False,
            "global_repository_exhaustion_claimed": False,
            "hash_mode": "CANONICAL_UTF8_LF_V2",
        },
        "SNAPSHOT",
    )

    contract = payload["candidate_universe_contract"]
    strict_equal(
        contract["inclusion_predicate"],
        (
            "SOURCE_BACKED_DISTINCT_OBJECT_IN_DECLARED_LINEAGE_WITH_"
            "A_LITERAL_REGISTRY_FORMULA_THEOREM_OR_TARGET_ROLE_RELEVANT_"
            "TO_THE_PRODUCTION_CROSSWALK"
        ),
        "INCLUSION_PREDICATE",
    )
    strict_equal(
        contract["exclusion_predicate"],
        (
            "AUXILIARY_PHASE_MEASURE_GRID_INTERVAL_OR_DUPLICATE_IMPORT_"
            "WITHOUT_A_DISTINCT_PRODUCTION_CROSSWALK_OBJECT"
        ),
        "EXCLUSION_PREDICATE",
    )
    for key, expected in {
        "candidate_count": 9,
        "audited_candidate_count": 9,
        "omitted_candidate_count": 0,
        "duplicate_candidate_count": 0,
        "axis_cell_count": 63,
        "crosswalk_cell_count": 27,
        "excluded_record_count": 4,
    }.items():
        strict_equal(contract[key], expected, f"UNIVERSE_COUNT:{key}")
        require(type(contract[key]) is int, f"UNIVERSE_COUNT_TYPE:{key}")
    strict_equal(
        contract["candidate_universe_digest"],
        CANDIDATE_UNIVERSE_DIGEST,
        "UNIVERSE_DIGEST",
    )

    expected_ids = [row[0] for row in EXPECTED_CANDIDATES]
    strict_equal(
        contract["included_candidate_ids"],
        expected_ids,
        "UNIVERSE_INCLUDED_IDS",
    )
    candidates = payload["candidate_audits"]
    require(type(candidates) is list and len(candidates) == 9, "CANDIDATE_COUNT")
    strict_equal(
        [row["candidate_id"] for row in candidates],
        expected_ids,
        "CANDIDATE_ORDER",
    )
    require(len(set(expected_ids)) == 9, "EXPECTED_ID_DUPLICATE")
    for row, expected in zip(candidates, EXPECTED_CANDIDATES):
        candidate_id, object_type, locator, native_formula, row_digest = expected
        strict_equal(row["candidate_id"], candidate_id, "CANDIDATE_ID")
        strict_equal(
            row["object_type"],
            object_type,
            f"OBJECT_TYPE:{candidate_id}",
        )
        strict_equal(
            row["primary_source_locator"],
            locator,
            f"PRIMARY_LOCATOR:{candidate_id}",
        )
        strict_equal(
            row["native_formula_type"],
            native_formula,
            f"NATIVE_FORMULA:{candidate_id}",
        )
        strict_equal(
            row["object_type_eligible_for_finite_audit"],
            True,
            f"OBJECT_ELIGIBILITY:{candidate_id}",
        )
        strict_equal(
            [cell["axis_id"] for cell in row["axis_audit"]],
            PRODUCTION_AXES,
            f"AXIS_ORDER:{candidate_id}",
        )
        require(
            all(cell["production_match"] is False for cell in row["axis_audit"]),
            f"PRODUCTION_PROMOTION:{candidate_id}",
        )
        strict_equal(
            row["first_mismatch_gate_id"],
            "NAMED_PRODUCTION_ATOM",
            f"FIRST_MISMATCH:{candidate_id}",
        )
        strict_equal(
            row["first_mismatch_gate_index"],
            1,
            f"FIRST_MISMATCH_INDEX:{candidate_id}",
        )
        strict_equal(
            [cell["formula_type_id"] for cell in row["formula_crosswalk_audit"]],
            [formula["id"] for formula in FORMULA_TYPES],
            f"FORMULA_ORDER:{candidate_id}",
        )
        require(
            all(
                cell["exact_crosswalk"] is False
                for cell in row["formula_crosswalk_audit"]
            ),
            f"CROSSWALK_PROMOTION:{candidate_id}",
        )
        strict_equal(
            row["complete_crosswalk"],
            False,
            f"COMPLETE_PROMOTION:{candidate_id}",
        )
        strict_equal(
            value_digest(row),
            row_digest,
            f"CANDIDATE_ROW_DIGEST:{candidate_id}",
        )

    strict_equal(payload["production_axes"], PRODUCTION_AXES, "PRODUCTION_AXES")
    strict_equal(
        payload["gate_order"],
        [
            {"gate_id": gate_id, "index": index}
            for index, gate_id in enumerate(GATE_ORDER)
        ],
        "GATE_ORDER",
    )
    strict_equal(
        payload["formula_type_registry"],
        FORMULA_TYPES,
        "FORMULA_REGISTRY",
    )
    strict_equal(
        value_digest(payload["formula_type_registry"]),
        FORMULA_REGISTRY_DIGEST,
        "FORMULA_REGISTRY_DIGEST",
    )
    strict_equal(
        payload["formula_type_distinctness"],
        {
            "block_equals_cumulative": False,
            "block_equals_physical": False,
            "cumulative_equals_physical": False,
            "pairwise_distinct": True,
        },
        "FORMULA_DISTINCTNESS",
    )
    strict_equal(
        value_digest(payload["excluded_record_ledger"]),
        EXCLUSION_LEDGER_DIGEST,
        "EXCLUSION_LEDGER",
    )
    strict_equal(
        [row["record_id"] for row in payload["excluded_record_ledger"]],
        [
            "TPC167.prop:grid",
            "TPC167.cor:measure",
            "TPC159.cor:interval",
            "TPC203.tpc194_import_contract",
        ],
        "EXCLUSION_IDS",
    )

    strict_equal(
        payload["decision"],
        {
            "batch_stop": "USER_CONFIRMATION_REQUIRED",
            "complete_crosswalk_candidate_ids": [],
            "complete_crosswalk_count": 0,
            "direct_trigger": "FAIL",
            "first_common_missing_gate_id": "NAMED_PRODUCTION_ATOM",
            "first_common_missing_production_axis": "named_production_atom",
            "next_paper": None,
            "next_route": (
                "SEARCH_FOR_SOURCE_LOCKED_NAMED_PRODUCTION_ATOM_RECORD_"
                "OR_GENUINE_FIXED_ATOM_THEOREM"
            ),
            "reopen_trigger_passed": False,
            "theorem_backed_natural_q_over_N_fixed_atom_power": False,
            "theorem_status": (
                "PROVED_LOCKED_REGISTRY_FIRST_MISMATCH_"
                "NO_COMPLETE_CROSSWALK_L1"
            ),
            "tpc205_authorized": False,
            "unique_complete_crosswalk": False,
            "unique_complete_crosswalk_candidate_id": None,
            "verdict": "FIRST_MISMATCH_CERTIFIED_NOT_TESTABLE",
        },
        "DECISION",
    )
    strict_equal(
        payload["first_missing_nodes"],
        {
            "direct_crosswalk_subgate": "NAMED_PRODUCTION_ATOM",
            "direct_production_parent": (
                "SOURCE_LOCKED_PRODUCTION_PACKET_PREFIX_CROSSWALK"
            ),
            "global": "H1.source_backed_local_occurrence_edge_family",
            "selected_pointwise": (
                "LITERAL_FIXED_ATOM_ARITHMETIC_CANCELLATION"
            ),
        },
        "FIRST_MISSING_NODES",
    )
    strict_equal(
        payload["route_state"],
        {
            "L2_result": "NONE",
            "bad_endpoint_O161_parent": "OPEN",
            "direct_twist_O161_parent": "OPEN",
            "fixed_atom_decay_obtained": False,
            "global_architecture": "OPEN",
            "literal_fixed_atom_cancellation_obtained": False,
            "program_positive_L2": False,
        },
        "ROUTE_STATE",
    )
    strict_equal(
        payload["endpoint_ledger"],
        {
            "named_atom_sigma_credit": {"denominator": 1, "numerator": 0},
            "required_strict_budget": {"denominator": 400, "numerator": 1},
            "state": "UNPAID",
        },
        "ENDPOINT_LEDGER",
    )
    strict_equal(payload["stop_scoped"], STOP_SCOPED, "STOP_SCOPED")
    strict_equal(
        value_digest(payload["stop_scoped"]),
        STOP_SCOPED_DIGEST,
        "STOP_SCOPED_DIGEST",
    )
    claim = payload["claim_boundary"]
    strict_equal(
        set(claim),
        {
            "authorization_implies_direct_trigger",
            "authorization_implies_reopen",
            "authorization_is_theorem_evidence",
            "block_equals_cumulative_prefix",
            "block_equals_physical_prefix",
            "cumulative_equals_physical_prefix",
            "finite_corpus_stop_is_global_nonexistence",
            "first_mismatch_is_complete_crosswalk",
            "fixed_atom_decay_obtained",
            "hash_integrity_is_theorem_evidence",
            "log_saving_is_positive_X_power",
            "packet_key_is_production_packet_schedule",
            "phase_L2_is_named_atom_control",
            "prime_pair_lower_bound",
            "program_positive_L2",
            "strict_one_over_400",
            "symbolic_packet_atom_is_named_production_atom",
            "twin_prime_theorem",
            "unique_crosswalk_would_imply_direct_trigger",
        },
        "CLAIM_FIREWALL_KEYS",
    )
    require(
        all(type(value) is bool and value is False for value in claim.values()),
        "CLAIM_FIREWALL_PROMOTION",
    )
    strict_equal(
        payload["level_ledger"],
        {
            "L0": (
                "SOURCE_LOCKS_EXACT_SCHEMA_CANDIDATE_ENUMERATION_"
                "AND_MUTATION_CERTIFICATE"
            ),
            "L1": (
                "SCOPED_FIRST_MISMATCH_THEOREM_FOR_THE_DECLARED_"
                "PRODUCTION_CROSSWALK_CORPUS"
            ),
            "L2": "NONE",
        },
        "LEVEL_LEDGER",
    )
    strict_equal(
        payload["upstream_semantic_summary"],
        {
            "source_semantics_verified": True,
            "tpc159_all_prefix_power": False,
            "tpc167_fixed_atom": False,
            "tpc180_value_bearing_registry_rows": 0,
            "tpc193_direct_candidates": 2,
            "tpc193_eligible_candidates": 0,
            "tpc194_formula_types": 3,
            "tpc194_hardening_artifacts": 2,
            "tpc194_manifest_pins": 12,
            "tpc194_missing_production_axes": 7,
            "tpc203_direct_first_missing": (
                "SOURCE_LOCKED_PRODUCTION_PACKET_PREFIX_CROSSWALK"
            ),
        },
        "UPSTREAM_SUMMARY",
    )
    strict_equal(
        payload["result_summary"],
        (
            "Nine distinct plausible crosswalk objects are source-locked "
            "and audited on all seven production axes and all three formula "
            "types.  No complete crosswalk exists in the declared corpus; "
            "the shared first production-axis mismatch is the absence of a "
            "source-locked named production atom."
        ),
        "RESULT_SUMMARY",
    )
    verify_source_locks(payload)
    if enforce_frozen_digest:
        strict_equal(
            raw_digest(PAYLOAD_PATH),
            PAYLOAD_RAW_SHA256,
            "FROZEN_PAYLOAD_DIGEST",
        )


def assert_anchor(
    relative: str,
    anchor: str,
    fragments: list[str],
    code: str,
    radius: int = 2200,
) -> None:
    path = require_repo_path(relative, code)
    text = path.read_text(encoding="utf-8")
    strict_equal(text.count(anchor), 1, f"{code}:ANCHOR_COUNT")
    index = text.index(anchor)
    window = text[max(0, index - radius) : min(len(text), index + radius)]
    for fragment in fragments:
        require(fragment in window, f"{code}:FRAGMENT:{fragment}")


def verify_upstream_semantics() -> None:
    source_map = dict(EXPECTED_SOURCE_PATHS)
    p159 = load_json(REPO / source_map["TPC159.audit"])
    p167 = load_json(REPO / source_map["TPC167.audit"])
    p180 = load_json(REPO / source_map["TPC180.payload"])
    p184 = load_json(REPO / source_map["TPC184.payload"])
    p189 = load_json(REPO / source_map["TPC189.payload"])
    p193 = load_json(REPO / source_map["TPC193.payload"])
    p194 = load_json(REPO / source_map["TPC194.payload"])
    p203 = load_json(REPO / source_map["TPC203.payload"])

    strict_equal(
        p159["claim_boundary"]["positive_fixed_X_power"],
        False,
        "TPC159_POSITIVE_POWER",
    )
    strict_equal(
        p159["claim_boundary"]["all_deterministic_prefixes"],
        False,
        "TPC159_ALL_PREFIX",
    )
    strict_equal(
        p167["claim_boundary"]["fixed_atom"],
        False,
        "TPC167_FIXED_ATOM",
    )
    strict_equal(
        p167["claim_boundary"]["specified_phase"],
        False,
        "TPC167_SPECIFIED_PHASE",
    )
    registry = p180["candidate_registry"]
    for key in [
        "registry_id",
        "named_physical_atom_id",
        "phase_value_mod_1",
        "phase_value_source_locator",
        "packet_schedule_source_locator",
    ]:
        require(registry[key] is None, f"TPC180_NON_NULL:{key}")
    strict_equal(registry["packet_coordinate_rows"], [], "TPC180_PACKET_ROWS")
    strict_equal(registry["status"], "NOT_TESTABLE", "TPC180_STATUS")

    strict_equal(p184["verdict"], "TARGET_WELL_TYPED_OPEN", "TPC184_VERDICT")
    strict_equal(
        p184["required_quantifier_signature"],
        {
            "carrier_axis": "ACTUAL_FIXED_H0_PACKET",
            "decay_axis": "FIXED_X_POWER_FIXED_ATOM",
            "endpoint_axis": "DETERMINISTIC_ALL_PREFIX",
            "phase_axis": "NAMED_FIXED_ATOM",
            "scale_axis": "DETERMINISTIC_ALL_SCALE",
            "support_axis": "ACTUAL_ACTIVE_SUPPORT",
        },
        "TPC184_SIGNATURE",
    )
    strict_equal(
        p184["smallest_literal_missing_theorem"],
        "POINTWISE_NAMED_ATOM_CONTROL_INSIDE_TPC159_DYADIC_SHADOW",
        "TPC184_FIRST_MISSING",
    )
    strict_equal(p189["verdict"], "TARGET_WELL_TYPED_OPEN", "TPC189_VERDICT")
    strict_equal(
        p189["smallest_literal_missing_theorem"],
        "DIRECT_ADDITIVE_TWIST_NAMED_ATOM_POWER_SAVING",
        "TPC189_FIRST_MISSING",
    )
    strict_equal(
        [row["candidate_id"] for row in p193["candidate_inventory"]],
        ["TW25.LOG_TWISTED_AFFINE", "TT26.RATIONAL_PERIODIC_ATOM"],
        "TPC193_CANDIDATES",
    )
    require(
        all(row["eligible"] is False for row in p193["candidate_inventory"]),
        "TPC193_ELIGIBILITY",
    )
    strict_equal(
        p194["finite_certificate"]["formula_type_registry"],
        FORMULA_TYPES,
        "TPC194_FORMULA_TYPES",
    )
    completion = p194["finite_certificate"]["completion_axes"]
    strict_equal(
        {key for key, value in completion.items() if value == "MISSING"},
        set(PRODUCTION_AXES),
        "TPC194_MISSING_AXIS_SET",
    )
    strict_equal(
        p203["first_missing_nodes"]["direct_production"],
        "SOURCE_LOCKED_PRODUCTION_PACKET_PREFIX_CROSSWALK",
        "TPC203_DIRECT_FIRST_MISSING",
    )
    strict_equal(p203["verdict"], "NOT_TESTABLE", "TPC203_VERDICT")

    assert_anchor(
        source_map["TPC159.main"],
        r"\label{eq:source}",
        [r"\frac qN", r"N<t(z)\le2N", r"(\log X)^{-\kappa_0}"],
        "TPC159_SOURCE_FORMULA",
    )
    assert_anchor(
        source_map["TPC159.main"],
        r"\label{eq:main}",
        [r"\frac qT|A_\rho(T)|", r"2^{-J}", r"\frac qT"],
        "TPC159_CUMULATIVE_FORMULA",
    )
    assert_anchor(
        source_map["TPC167.main"],
        r"\label{eq:transform}",
        [r"F_N(\alpha)=\frac qN", r"\sum_{z\in I_N}c_z\e(-\alpha z)"],
        "TPC167_TERMINAL_FORMULA",
    )
    assert_anchor(
        source_map["TPC193.main"],
        r"\label{prop:formula}",
        [
            r"does not uniquely instantiate",
            r"is not formula-certified by the locked formulas",
        ],
        "TPC193_FORMULA_SEPARATION",
    )
    assert_anchor(
        source_map["TPC194.main"],
        r"\label{eq:physical-prefix}",
        [r"z\in I_{\xi,X}", r"z\leq T", r"\e(-\alpha_{\xi,X}z)"],
        "TPC194_PHYSICAL_PREFIX",
    )

    upstream_manifest = load_json(REPO / source_map["TPC194.manifest"])
    upstream_rows = upstream_manifest["artifacts"]
    require(type(upstream_rows) is list and len(upstream_rows) == 12, "TPC194_MANIFEST_COUNT")
    for row in upstream_rows:
        strict_equal(set(row), {"path", "raw_sha256"}, "TPC194_MANIFEST_KEYS")
        target = require_repo_path(row["path"], "TPC194_MANIFEST_PATH")
        strict_equal(
            raw_digest(target),
            row["raw_sha256"],
            f"TPC194_MANIFEST_HASH:{row['path']}",
        )


def mutate_base(payload: dict[str, Any], name: str) -> dict[str, Any]:
    obj = copy.deepcopy(payload)
    if name == "extra_top_level":
        obj["extra"] = True
    elif name == "drop_decision":
        del obj["decision"]
    elif name == "bool_for_paper":
        obj["paper"] = True
    elif name == "integer_for_authorization_flag":
        obj["authorization"]["tpc204_authorized"] = 1
    elif name == "drop_candidate":
        obj["candidate_audits"].pop()
    elif name == "duplicate_candidate":
        obj["candidate_audits"].append(copy.deepcopy(obj["candidate_audits"][0]))
    elif name == "change_axis_status":
        obj["candidate_audits"][0]["axis_audit"][0]["native_status"] = "PRESENT"
    elif name == "corrupt_formula_tuple":
        obj["formula_type_registry"][0]["domain"] = "0<t(z)<=T"
    elif name == "source_hash_drift":
        obj["source_locks"][0]["canonical_utf8_lf_sha256"] = "0" * 64
    elif name == "drop_stop_cell":
        obj["stop_scoped"].pop()
    elif name == "promote_claim_flag":
        obj["claim_boundary"]["fixed_atom_decay_obtained"] = True
    elif name == "advance_first_mismatch":
        obj["candidate_audits"][0]["first_mismatch_gate_index"] = 2
    else:
        raise KeyError(name)
    return obj


def mutate_semantic(payload: dict[str, Any], name: str) -> dict[str, Any]:
    obj = copy.deepcopy(payload)
    candidate0 = obj["candidate_audits"][0]
    if name == "authorization_implies_direct_trigger":
        obj["authorization"]["implies_direct_trigger_pass"] = True
    elif name == "authorization_implies_reopen":
        obj["authorization"]["implies_any_reopen_trigger"] = True
    elif name == "promote_verdict_to_unique":
        obj["decision"]["verdict"] = "UNIQUE_COMPLETE_CROSSWALK"
    elif name == "forge_complete_count":
        obj["decision"]["complete_crosswalk_count"] = 1
    elif name == "forge_unique_candidate_id":
        obj["decision"]["unique_complete_crosswalk_candidate_id"] = (
            candidate0["candidate_id"]
        )
    elif name == "drop_candidate":
        obj["candidate_audits"].pop()
    elif name == "add_synthetic_candidate":
        synthetic = copy.deepcopy(candidate0)
        synthetic["candidate_id"] = "SYNTHETIC"
        obj["candidate_audits"].append(synthetic)
    elif name == "duplicate_candidate_id":
        obj["candidate_audits"][1]["candidate_id"] = candidate0["candidate_id"]
    elif name == "reorder_candidates":
        obj["candidate_audits"][0], obj["candidate_audits"][1] = (
            obj["candidate_audits"][1],
            obj["candidate_audits"][0],
        )
    elif name == "change_inclusion_predicate":
        obj["candidate_universe_contract"]["inclusion_predicate"] = "ANY_RECORD"
    elif name == "drop_excluded_record":
        obj["excluded_record_ledger"].pop()
    elif name == "forge_universe_digest":
        obj["candidate_universe_contract"]["candidate_universe_digest"] = "0" * 64
    elif name == "forge_source_lock_hash":
        obj["source_locks"][0]["canonical_utf8_lf_sha256"] = "0" * 64
    elif name == "promote_hash_to_theorem_evidence":
        obj["source_locks"][0]["hash_semantics"] = "THEOREM_EVIDENCE"
    elif name == "fabricate_named_atom":
        candidate0["axis_audit"][0]["production_match"] = True
    elif name == "fabricate_packet_schedule":
        candidate0["axis_audit"][1]["production_match"] = True
    elif name == "fabricate_common_ranges":
        candidate0["axis_audit"][2]["production_match"] = True
    elif name == "fabricate_uniform_C":
        candidate0["axis_audit"][3]["production_match"] = True
    elif name == "treat_log_saving_as_positive_sigma":
        obj["candidate_audits"][1]["axis_audit"][4]["production_match"] = True
    elif name == "select_normalization_by_fiat":
        candidate0["axis_audit"][5]["production_match"] = True
    elif name == "mark_loss_ledger_complete":
        candidate0["axis_audit"][6]["production_match"] = True
    elif name == "drop_axis_row":
        candidate0["axis_audit"].pop()
    elif name == "duplicate_axis_row":
        candidate0["axis_audit"].append(copy.deepcopy(candidate0["axis_audit"][0]))
    elif name == "advance_first_mismatch":
        candidate0["first_mismatch_gate_id"] = "EXACT_PACKET_SCHEDULE"
        candidate0["first_mismatch_gate_index"] = 2
    elif name == "clear_first_mismatch":
        candidate0["first_mismatch_gate_id"] = ""
    elif name == "merge_terminal_and_cumulative":
        obj["formula_type_distinctness"]["block_equals_cumulative"] = True
    elif name == "merge_terminal_and_physical":
        obj["formula_type_distinctness"]["block_equals_physical"] = True
    elif name == "merge_cumulative_and_physical":
        obj["formula_type_distinctness"]["cumulative_equals_physical"] = True
    elif name == "corrupt_terminal_tuple":
        obj["formula_type_registry"][0]["normalization"] = "q/T"
    elif name == "corrupt_cumulative_tuple":
        obj["formula_type_registry"][1]["domain"] = "N<t(z)<=2N"
    elif name == "corrupt_physical_tuple":
        obj["formula_type_registry"][2]["normalization"] = "q/N"
    elif name == "drop_crosswalk_row":
        candidate0["formula_crosswalk_audit"].pop()
    elif name == "set_crosswalk_exact":
        candidate0["formula_crosswalk_audit"][0]["exact_crosswalk"] = True
    elif name == "direct_trigger_passed":
        obj["decision"]["direct_trigger"] = "PASS"
    elif name == "fixed_atom_decay_obtained":
        obj["route_state"]["fixed_atom_decay_obtained"] = True
    elif name == "grant_endpoint_credit":
        obj["endpoint_ledger"]["named_atom_sigma_credit"]["numerator"] = 1
    elif name == "pay_strict_one_over_400":
        obj["endpoint_ledger"]["state"] = "PAID"
    elif name == "promote_L2":
        obj["route_state"]["L2_result"] = "POSITIVE"
    elif name == "stop_bad_endpoint_parent":
        obj["route_state"]["bad_endpoint_O161_parent"] = "STOPPED"
    elif name == "stop_direct_parent":
        obj["route_state"]["direct_twist_O161_parent"] = "STOPPED"
    elif name == "stop_global_architecture":
        obj["route_state"]["global_architecture"] = "STOPPED"
    elif name == "unstop_TPC193_V1":
        obj["stop_scoped"] = [
            cell for cell in obj["stop_scoped"] if not cell.startswith("TPC193_")
        ]
    elif name == "global_nonexistence_claim":
        obj["claim_boundary"]["finite_corpus_stop_is_global_nonexistence"] = True
    elif name == "bool_for_candidate_count":
        obj["candidate_universe_contract"]["candidate_count"] = False
    elif name == "integer_for_boolean_claim":
        obj["claim_boundary"]["program_positive_L2"] = 0
    else:
        raise KeyError(name)
    return obj


def mutate_strict_type(payload: dict[str, Any], name: str) -> dict[str, Any]:
    obj = copy.deepcopy(payload)
    if name == "authorization_true_to_integer":
        obj["authorization"]["tpc204_authorized"] = 1
    elif name == "authorization_false_to_integer":
        obj["authorization"]["is_mathematical_evidence"] = 0
    elif name == "route_false_to_integer":
        obj["route_state"]["program_positive_L2"] = 0
    elif name == "endpoint_integer_to_boolean":
        obj["endpoint_ledger"]["named_atom_sigma_credit"]["numerator"] = False
    elif name == "formula_false_to_integer":
        obj["formula_type_distinctness"]["block_equals_cumulative"] = 0
    else:
        raise KeyError(name)
    return obj


def semantic_rejected(payload: dict[str, Any]) -> bool:
    try:
        verify_payload_semantics(payload, enforce_frozen_digest=False)
    except (
        VerificationError,
        DuplicateKeyError,
        KeyError,
        TypeError,
        ValueError,
    ):
        return True
    return False


def verify_mutations(
    payload: dict[str, Any],
    payload_schema: dict[str, Any],
) -> None:
    for name in BASE_MUTATIONS:
        mutated = mutate_base(payload, name)
        require(
            compact_canonical(mutated) != compact_canonical(payload),
            f"BASE_MUTATION_NOOP:{name}",
        )
        require(
            not schema_accepts(payload_schema, mutated),
            f"BASE_SCHEMA_ACCEPTED:{name}",
        )
    for name in SEMANTIC_MUTATIONS:
        mutated = mutate_semantic(payload, name)
        require(
            compact_canonical(mutated) != compact_canonical(payload),
            f"SEMANTIC_MUTATION_NOOP:{name}",
        )
        regenerated = exact_schema(mutated)
        require(
            schema_accepts(regenerated, mutated),
            f"REGENERATED_SCHEMA_REJECTED_FIXTURE:{name}",
        )
        require(semantic_rejected(mutated), f"SEMANTIC_MUTATION_ACCEPTED:{name}")
    for name in STRICT_TYPE_MUTATIONS:
        mutated = mutate_strict_type(payload, name)
        regenerated = exact_schema(mutated)
        require(
            schema_accepts(regenerated, mutated),
            f"TYPE_SCHEMA_REJECTED_FIXTURE:{name}",
        )
        require(semantic_rejected(mutated), f"STRICT_TYPE_ACCEPTED:{name}")


def verify_audit(
    audit: dict[str, Any],
    payload: dict[str, Any],
    payload_schema: dict[str, Any],
) -> None:
    strict_equal(
        audit["schema"],
        "tpc-204-source-locked-production-registry-crosswalk-audit-v1",
        "AUDIT_SCHEMA_FIELD",
    )
    strict_equal(audit["paper"], 204, "AUDIT_PAPER")
    strict_equal(audit["payload_sha256"], PAYLOAD_RAW_SHA256, "AUDIT_PAYLOAD_HASH")
    strict_equal(
        audit["payload_schema_sha256"],
        PAYLOAD_SCHEMA_RAW_SHA256,
        "AUDIT_PAYLOAD_SCHEMA_HASH",
    )
    checks = audit["checks"]
    strict_equal(
        set(checks),
        {
            "L2_none",
            "TPC193_V1_stop_scoped",
            "all_candidates_audited",
            "all_source_locks_integrity_only",
            "authorization_not_mathematical_evidence",
            "authorization_scope_exact",
            "axis_cells_63",
            "candidate_count_9",
            "complete_crosswalk_count_0",
            "crosswalk_cells_27",
            "declared_candidate_universe_closed",
            "direct_trigger_fail",
            "endpoint_credit_zero",
            "formula_types_pairwise_distinct",
            "new_TPC204_stop_scoped",
            "parents_and_architecture_open",
            "shared_first_mismatch_named_production_atom",
            "strict_one_over_400_unpaid",
            "upstream_TPC194_hardening_verified",
        },
        "AUDIT_CHECK_KEYS",
    )
    require(
        all(type(value) is bool and value is True for value in checks.values()),
        "AUDIT_CHECK_FALSE",
    )
    expected_result = {
        "axis_cells_verified": 63,
        "complete_crosswalks": 0,
        "crosswalk_cells_verified": 27,
        "declared_candidates_verified": 9,
        "excluded_records_verified": 4,
        "formula_types_verified": 3,
        "mathematical_reopen": False,
        "new_stop_cell": STOP_CELL,
        "production_axes_per_candidate": 7,
        "semantic_contract_version": 1,
        "shared_first_mismatch_gate": "NAMED_PRODUCTION_ATOM",
    }
    strict_equal(
        audit["finite_check_result"],
        expected_result,
        "AUDIT_FINITE_RESULT",
    )
    strict_equal(
        audit["semantic_contract_result"],
        expected_result,
        "AUDIT_SEMANTIC_RESULT",
    )
    strict_equal(
        [row["name"] for row in audit["base_mutation_registry"]],
        BASE_MUTATIONS,
        "AUDIT_BASE_MUTATION_NAMES",
    )
    require(
        all(
            row["payload_changed"] is True
            and row["rejected_by_active_schema"] is True
            for row in audit["base_mutation_registry"]
        ),
        "AUDIT_BASE_MUTATION_FLAG",
    )
    strict_equal(
        [row["name"] for row in audit["semantic_mutation_registry"]],
        SEMANTIC_MUTATIONS,
        "AUDIT_SEMANTIC_MUTATION_NAMES",
    )
    require(
        all(
            row["payload_changed"] is True
            and row["regenerated_schema_accepts"] is True
            and row["independent_semantic_checker_rejected"] is True
            for row in audit["semantic_mutation_registry"]
        ),
        "AUDIT_SEMANTIC_MUTATION_FLAG",
    )
    strict_equal(audit["all_checks_pass"], True, "AUDIT_ALL_CHECKS")
    verify_mutations(payload, payload_schema)


def verify_manifest() -> int:
    manifest = load_json(MANIFEST_PATH)
    strict_equal(
        MANIFEST_PATH.read_text(encoding="utf-8"),
        pretty_canonical(manifest),
        "MANIFEST_NONCANONICAL",
    )
    strict_equal(
        set(manifest),
        {"artifacts", "mode", "schema", "semantic_contract"},
        "MANIFEST_KEYS",
    )
    strict_equal(
        manifest["schema"],
        "tpc204-certificate-manifest-v1",
        "MANIFEST_SCHEMA",
    )
    strict_equal(
        manifest["mode"],
        "MANUALLY_REFRESHED_NOT_GENERATOR_SIGNED",
        "MANIFEST_MODE",
    )
    strict_equal(
        manifest["semantic_contract"],
        {
            "base_mutations": 12,
            "complete_crosswalks": 0,
            "contract": "TPC204_FINITE_PRODUCTION_REGISTRY_CROSSWALK_V1",
            "declared_candidates": 9,
            "formula_types": 3,
            "manifest_trust": (
                "REPOSITORY_PIN_REQUIRES_GIT_REVIEW_NOT_EXTERNAL_SIGNATURE"
            ),
            "production_axes": 7,
            "semantic_mutations": 45,
            "shared_first_mismatch": "NAMED_PRODUCTION_ATOM",
        },
        "MANIFEST_SEMANTICS",
    )
    rows = manifest["artifacts"]
    strict_equal(
        [row["path"] for row in rows],
        ACTIVE_ARTIFACTS,
        "MANIFEST_ARTIFACT_ORDER",
    )
    for row in rows:
        strict_equal(set(row), {"path", "raw_sha256"}, "MANIFEST_ROW_KEYS")
        target = require_repo_path(row["path"], "MANIFEST_PATH")
        strict_equal(
            raw_digest(target),
            row["raw_sha256"],
            f"MANIFEST_HASH:{row['path']}",
        )
    return len(rows)


def verify() -> dict[str, Any]:
    payload = verify_generated_file(
        PAYLOAD_PATH,
        PAYLOAD_RAW_SHA256,
        "PAYLOAD",
    )
    audit = verify_generated_file(AUDIT_PATH, AUDIT_RAW_SHA256, "AUDIT")
    payload_schema = verify_generated_file(
        PAYLOAD_SCHEMA_PATH,
        PAYLOAD_SCHEMA_RAW_SHA256,
        "PAYLOAD_SCHEMA",
    )
    audit_schema = verify_generated_file(
        AUDIT_SCHEMA_PATH,
        AUDIT_SCHEMA_RAW_SHA256,
        "AUDIT_SCHEMA",
    )
    strict_equal(
        normalize_required_order(payload_schema),
        normalize_required_order(exact_schema(payload, PAYLOAD_SCHEMA_ID)),
        "PAYLOAD_SCHEMA_NOT_EXACT",
    )
    strict_equal(
        normalize_required_order(audit_schema),
        normalize_required_order(exact_schema(audit, AUDIT_SCHEMA_ID)),
        "AUDIT_SCHEMA_NOT_EXACT",
    )
    require(schema_accepts(payload_schema, payload), "PAYLOAD_SCHEMA_REJECTS")
    require(schema_accepts(audit_schema, audit), "AUDIT_SCHEMA_REJECTS")
    verify_payload_semantics(payload, enforce_frozen_digest=True)
    verify_upstream_semantics()
    verify_audit(audit, payload, payload_schema)
    manifest_count = verify_manifest()
    return {
        "paper": 204,
        "independent_checker": True,
        "imports_materializer": False,
        "declared_candidates_verified": 9,
        "axis_cells_verified": 63,
        "crosswalk_cells_verified": 27,
        "complete_crosswalks": 0,
        "shared_first_mismatch_gate": "NAMED_PRODUCTION_ATOM",
        "base_mutations_rejected": len(BASE_MUTATIONS),
        "semantic_mutations_rejected": len(SEMANTIC_MUTATIONS),
        "strict_type_mutations_rejected": len(STRICT_TYPE_MUTATIONS),
        "source_locks_verified": len(EXPECTED_SOURCE_PATHS),
        "manifest_artifacts_verified": manifest_count,
        "verdict": "FIRST_MISMATCH_CERTIFIED_NOT_TESTABLE",
    }


def main() -> None:
    if not __debug__:
        raise RuntimeError(
            "optimized Python disables upstream assertion contracts; "
            "the independent TPC-204 checker fails closed"
        )
    parser = argparse.ArgumentParser()
    parser.add_argument("--check", action="store_true")
    parser.parse_args()
    print(json.dumps(verify(), sort_keys=True))


if __name__ == "__main__":
    main()
