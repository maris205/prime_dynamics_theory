#!/usr/bin/env python3
"""Authoritative materializer/contract module for the finite TPC-204 census.

The contract is deliberately narrower than a mathematical reopen:

* enumerate a declared, source-locked set of plausible production-crosswalk
  objects;
* audit all seven production axes for every object;
* preserve the three noninterchangeable formula types from TPC-194; and
* return either one unique complete crosswalk or a source-backed first
  mismatch.

The current source snapshot has no complete crosswalk.  The shared first
production-axis mismatch is the absence of a source-locked named production
atom.  User authorization is workflow input only and never theorem evidence.
"""

from __future__ import annotations

import argparse
import copy
import hashlib
import importlib.util
import json
from functools import lru_cache
from pathlib import Path
from typing import Any, Callable


HERE = Path(__file__).resolve().parent
PAPER = HERE.parent
REPO = PAPER.parents[1]
STEM = "tpc204_source_locked_production_registry_crosswalk"
PAYLOAD_PATH = HERE / f"{STEM}.json"
AUDIT_PATH = HERE / f"{STEM}_audit.json"
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
HASH_MODE = "CANONICAL_UTF8_LF_V2"
CORPUS_ID = "TPC204_DECLARED_PLAUSIBLE_PRODUCTION_CROSSWALK_CORPUS_V1"
NEW_STOP_CELL = f"{CORPUS_ID}=STOP_SCOPED"

SOURCE_PATHS = {
    "TPC159.main": REPO
    / "papers"
    / "tpc-159-dyadic-shadow-prefix-lifting"
    / "main.tex",
    "TPC159.audit": REPO
    / "papers"
    / "tpc-159-dyadic-shadow-prefix-lifting"
    / "experiments"
    / "tpc159_dyadic_shadow_audit.json",
    "TPC167.main": REPO
    / "papers"
    / "tpc-167-direct-additive-twist-parseval"
    / "main.tex",
    "TPC167.audit": REPO
    / "papers"
    / "tpc-167-direct-additive-twist-parseval"
    / "experiments"
    / "tpc167_parseval_audit.json",
    "TPC180.payload": REPO
    / "papers"
    / "tpc-180-production-phase-registry-census"
    / "experiments"
    / "tpc180_phase_registry_census.json",
    "TPC183.payload": REPO
    / "papers"
    / "tpc-183-pointwise-parent-interface-comparison"
    / "experiments"
    / "tpc183_pointwise_parent_interface_comparison.json",
    "TPC184.payload": REPO
    / "papers"
    / "tpc-184-bad-endpoint-literal-target-contract"
    / "experiments"
    / "tpc184_bad_endpoint_literal_target_contract.json",
    "TPC189.payload": REPO
    / "papers"
    / "tpc-189-direct-twist-literal-target-contract"
    / "experiments"
    / "tpc189_direct_twist_literal_target_contract.json",
    "TPC193.main": REPO
    / "papers"
    / "tpc-193-literal-fixed-atom-candidate-mechanism-gate"
    / "main.tex",
    "TPC193.payload": REPO
    / "papers"
    / "tpc-193-literal-fixed-atom-candidate-mechanism-gate"
    / "experiments"
    / "tpc193_literal_fixed_atom_candidate_mechanism_gate.json",
    "TPC194.main": REPO
    / "papers"
    / "tpc-194-maximal-source-backed-direct-prefix"
    / "main.tex",
    "TPC194.payload": REPO
    / "papers"
    / "tpc-194-maximal-source-backed-direct-prefix"
    / "experiments"
    / "tpc194_maximal_source_backed_direct_prefix.json",
    "TPC194.hardener": REPO
    / "papers"
    / "tpc-194-maximal-source-backed-direct-prefix"
    / "experiments"
    / "tpc194_certificate_hardening.py",
    "TPC194.manifest": REPO
    / "papers"
    / "tpc-194-maximal-source-backed-direct-prefix"
    / "experiments"
    / "tpc194_certificate_hardening_manifest.json",
    "TPC203.payload": REPO
    / "papers"
    / "tpc-203-mvp10-direct-pointwise-route-decision"
    / "experiments"
    / "tpc203_mvp10_direct_pointwise_route_decision.json",
}

ACTIVE_ARTIFACTS = [
    (
        "papers/tpc-204-source-locked-production-registry-crosswalk/"
        "experiments/build_tpc204.py"
    ),
    (
        "papers/tpc-204-source-locked-production-registry-crosswalk/"
        "experiments/tpc204_source_locked_production_registry_crosswalk.py"
    ),
    (
        "papers/tpc-204-source-locked-production-registry-crosswalk/"
        "experiments/tpc204_independent_checker.py"
    ),
    (
        "papers/tpc-204-source-locked-production-registry-crosswalk/"
        "experiments/tpc204_source_locked_production_registry_crosswalk.json"
    ),
    (
        "papers/tpc-204-source-locked-production-registry-crosswalk/"
        "experiments/tpc204_source_locked_production_registry_crosswalk_audit.json"
    ),
    (
        "papers/tpc-204-source-locked-production-registry-crosswalk/"
        "schemas/tpc204-source-locked-production-registry-crosswalk-v1.schema.json"
    ),
    (
        "papers/tpc-204-source-locked-production-registry-crosswalk/"
        "schemas/tpc204-source-locked-production-registry-crosswalk-audit-v1.schema.json"
    ),
    "papers/tpc-204-source-locked-production-registry-crosswalk/README.md",
    "papers/tpc-204-source-locked-production-registry-crosswalk/main.tex",
    "papers/tpc-204-source-locked-production-registry-crosswalk/references.bib",
    (
        "papers/tpc-204-source-locked-production-registry-crosswalk/"
        "tpc-204-source-locked-production-registry-crosswalk.pdf"
    ),
]

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
    NEW_STOP_CELL,
]

EXCLUSION_LEDGER = [
    {
        "record_id": "TPC167.prop:grid",
        "source_locator": "TPC167.main#prop:grid+eq:grid",
        "reason": "AUXILIARY_COMPLETE_FOURIER_GRID_NOT_PRODUCTION_PACKET_SCHEDULE",
    },
    {
        "record_id": "TPC167.cor:measure",
        "source_locator": "TPC167.main#cor:measure+eq:chebyshev",
        "reason": "LEBESGUE_PHASE_MEASURE_NOT_NAMED_ATOM_CONTROL",
    },
    {
        "record_id": "TPC159.cor:interval",
        "source_locator": "TPC159.main#cor:interval",
        "reason": "INTERVAL_DIFFERENCE_HAS_NO_SINGLE_TARGET_NORMALIZATION",
    },
    {
        "record_id": "TPC203.tpc194_import_contract",
        "source_locator": (
            "TPC203.payload#/finite_certificate/tpc194_import_contract"
        ),
        "reason": "DUPLICATE_UPSTREAM_REVALIDATION_NOT_NEW_CROSSWALK_OBJECT",
    },
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


class ContractError(RuntimeError):
    """Raised when an artifact violates the materialization contract."""


class DuplicateKeyError(ValueError):
    """Raised for duplicate JSON object keys."""


def require(condition: bool, code: str) -> None:
    if not condition:
        raise ContractError(code)


def _pairs_no_duplicates(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
    result: dict[str, Any] = {}
    for key, value in pairs:
        if key in result:
            raise DuplicateKeyError(f"duplicate JSON key: {key}")
        result[key] = value
    return result


def _reject_constant(token: str) -> None:
    raise ValueError(f"nonfinite JSON number: {token}")


def strict_loads(text: str) -> Any:
    return json.loads(
        text,
        object_pairs_hook=_pairs_no_duplicates,
        parse_constant=_reject_constant,
    )


def load_json(path: Path, *, canonical_bytes: bool = False) -> dict[str, Any]:
    text = path.read_text(encoding="utf-8-sig")
    value = strict_loads(text)
    require(type(value) is dict, f"JSON_OBJECT_REQUIRED:{path}")
    if canonical_bytes:
        require(text == canonical(value), f"NONCANONICAL_JSON:{path}")
    return value


def canonical(value: Any) -> str:
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


def canonical_bytes(path: Path) -> bytes:
    text = path.read_text(encoding="utf-8-sig")
    return text.replace("\r\n", "\n").replace("\r", "\n").encode("utf-8")


def canonical_sha256(path: Path) -> str:
    return hashlib.sha256(canonical_bytes(path)).hexdigest()


def raw_sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def sha256_value(value: Any) -> str:
    return hashlib.sha256(canonical(value).encode("utf-8")).hexdigest()


def safe_relative(path: Path) -> str:
    resolved_repo = REPO.resolve()
    resolved = path.resolve()
    require(resolved.is_relative_to(resolved_repo), f"PATH_ESCAPES_REPO:{path}")
    return resolved.relative_to(resolved_repo).as_posix()


def source_lock(source_id: str, path: Path) -> dict[str, Any]:
    require(path.is_file(), f"SOURCE_MISSING:{source_id}")
    return {
        "source_id": source_id,
        "path": safe_relative(path),
        "canonical_utf8_lf_sha256": canonical_sha256(path),
        "hash_semantics": "INTEGRITY_ONLY",
    }


def source_locks() -> list[dict[str, Any]]:
    return [
        source_lock(source_id, path)
        for source_id, path in sorted(SOURCE_PATHS.items())
    ]


def strict_equal(actual: Any, expected: Any, path: str = "$") -> None:
    require(type(actual) is type(expected), f"TYPE_MISMATCH:{path}")
    if type(expected) is dict:
        require(set(actual) == set(expected), f"KEY_SET_MISMATCH:{path}")
        for key in expected:
            strict_equal(actual[key], expected[key], f"{path}.{key}")
    elif type(expected) is list:
        require(len(actual) == len(expected), f"ARRAY_LENGTH_MISMATCH:{path}")
        for index, (left, right) in enumerate(zip(actual, expected)):
            strict_equal(left, right, f"{path}[{index}]")
    else:
        require(actual == expected, f"VALUE_MISMATCH:{path}")


def assert_anchor(
    source_id: str,
    anchor: str,
    required_fragments: list[str],
    *,
    window: int = 1800,
) -> None:
    text = SOURCE_PATHS[source_id].read_text(encoding="utf-8")
    require(text.count(anchor) == 1, f"ANCHOR_NOT_UNIQUE:{source_id}:{anchor}")
    start = text.index(anchor)
    neighborhood = text[max(0, start - window) : start + len(anchor) + window]
    for fragment in required_fragments:
        require(
            fragment in neighborhood,
            f"FORMULA_FRAGMENT_MISSING:{source_id}:{anchor}:{fragment}",
        )


def _load_hardener() -> Any:
    path = SOURCE_PATHS["TPC194.hardener"]
    spec = importlib.util.spec_from_file_location("tpc194_hardener_for_tpc204", path)
    require(spec is not None and spec.loader is not None, "HARDENER_IMPORT_SPEC")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


@lru_cache(maxsize=1)
def upstream_semantic_summary() -> dict[str, Any]:
    p159 = load_json(SOURCE_PATHS["TPC159.audit"])
    p167 = load_json(SOURCE_PATHS["TPC167.audit"])
    p180 = load_json(SOURCE_PATHS["TPC180.payload"])
    p183 = load_json(SOURCE_PATHS["TPC183.payload"])
    p184 = load_json(SOURCE_PATHS["TPC184.payload"])
    p189 = load_json(SOURCE_PATHS["TPC189.payload"])
    p193 = load_json(SOURCE_PATHS["TPC193.payload"])
    p194 = load_json(SOURCE_PATHS["TPC194.payload"])
    p203 = load_json(SOURCE_PATHS["TPC203.payload"])

    assert_anchor(
        "TPC159.main",
        r"\label{eq:source}",
        [
            r"\frac qN",
            r"N<t(z)\le2N",
            r"(\log X)^{-\kappa_0}",
        ],
    )
    assert_anchor(
        "TPC159.main",
        r"\label{thm:main}",
        [r"2^J\sqrt X\le T\le X", r"T\notin\Sshadow_{X,J}"],
    )
    assert_anchor(
        "TPC159.main",
        r"\label{eq:main}",
        [r"\frac qT|A_\rho(T)|", r"2^{-J}", r"\frac qT"],
    )
    assert_anchor(
        "TPC167.main",
        r"\label{eq:transform}",
        [r"F_N(\alpha)=\frac qN", r"\sum_{z\in I_N}c_z\e(-\alpha z)"],
    )
    assert_anchor(
        "TPC167.main",
        r"\label{eq:parseval}",
        [r"\int_{\T}|F_N(\alpha)|^2", r"\frac{q^2}{N^2}E_N"],
    )
    assert_anchor(
        "TPC167.main",
        r"\label{eq:grid}",
        [r"\frac1M\sum_{r=0}^{M-1}", r"\frac{q^2}{N^2}E_N"],
    )
    assert_anchor(
        "TPC193.main",
        r"\label{prop:formula}",
        [
            r"does not uniquely instantiate",
            r"is not formula-certified by the locked formulas",
        ],
    )
    assert_anchor(
        "TPC193.main",
        r"\label{eq:tw}",
        [r"\frac1{\log X}", r"\frac{f_1(a_1n+h_1)f_2(a_2n+h_2)"],
    )
    assert_anchor(
        "TPC193.main",
        r"\label{eq:tt}",
        [r"\frac qN", r"N<t(z)\le2N", r"(\log X)^{-\kappa_0}"],
    )
    assert_anchor(
        "TPC194.main",
        r"\label{eq:physical-prefix}",
        [r"z\in I_{\xi,X}", r"z\leq T", r"\e(-\alpha_{\xi,X}z)"],
    )

    require(
        p159["claim_boundary"]["positive_fixed_X_power"] is False,
        "TPC159_POSITIVE_POWER_DRIFT",
    )
    require(
        p159["claim_boundary"]["all_deterministic_prefixes"] is False,
        "TPC159_PREFIX_QUANTIFIER_DRIFT",
    )
    require(
        p167["claim_boundary"]["fixed_atom"] is False,
        "TPC167_FIXED_ATOM_DRIFT",
    )
    require(
        p167["claim_boundary"]["specified_phase"] is False,
        "TPC167_SPECIFIED_PHASE_DRIFT",
    )
    require(
        p167["theorem"]["program_positive_L2"] is False,
        "TPC167_PROGRAM_L2_DRIFT",
    )

    registry = p180["candidate_registry"]
    strict_equal(
        {
            "registry_id": registry["registry_id"],
            "named_physical_atom_id": registry["named_physical_atom_id"],
            "phase_value_mod_1": registry["phase_value_mod_1"],
            "phase_value_source_locator": registry[
                "phase_value_source_locator"
            ],
            "packet_schedule_source_locator": registry[
                "packet_schedule_source_locator"
            ],
            "packet_coordinate_rows": registry["packet_coordinate_rows"],
            "status": registry["status"],
            "first_missing": registry["first_missing"],
        },
        {
            "registry_id": None,
            "named_physical_atom_id": None,
            "phase_value_mod_1": None,
            "phase_value_source_locator": None,
            "packet_schedule_source_locator": None,
            "packet_coordinate_rows": [],
            "status": "NOT_TESTABLE",
            "first_missing": (
                "named_physical_atom_id_and_phase_value_source_locator"
            ),
        },
        "TPC180.candidate_registry",
    )
    require(
        p180["source_census"]["value_bearing_named_phase_records"] == 0,
        "TPC180_NAMED_PHASE_COUNT_DRIFT",
    )
    require(
        p180["source_census"]["production_packet_coordinate_rows"] == 0,
        "TPC180_PACKET_ROW_COUNT_DRIFT",
    )

    require(
        p183["verdict"] == "PROVED_L1_INTERFACE_ONE_WAY_IMPLICATION",
        "TPC183_VERDICT_DRIFT",
    )
    require(
        p184["verdict"] == "TARGET_WELL_TYPED_OPEN",
        "TPC184_VERDICT_DRIFT",
    )
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
        "TPC184.required_quantifier_signature",
    )
    require(
        p184["result"]
        == (
            "The bad-endpoint target is frozen as a q/T-normalized "
            "cumulative actual-core sum at the prescribed atom, uniformly "
            "over every prefix endpoint and deterministic scale.  TPC-159 "
            "supplies only the complement of its dyadic shadow; TPC-169 "
            "supplies all prefixes only in phase L2.  Neither matches the "
            "contract."
        ),
        "TPC184_RESULT_DRIFT",
    )
    require(
        p184["smallest_literal_missing_theorem"]
        == "POINTWISE_NAMED_ATOM_CONTROL_INSIDE_TPC159_DYADIC_SHADOW",
        "TPC184_FIRST_MISSING_DRIFT",
    )
    require(
        p189["verdict"] == "TARGET_WELL_TYPED_OPEN",
        "TPC189_VERDICT_DRIFT",
    )
    require(
        p189["smallest_literal_missing_theorem"]
        == "DIRECT_ADDITIVE_TWIST_NAMED_ATOM_POWER_SAVING",
        "TPC189_FIRST_MISSING_DRIFT",
    )

    candidates = p193["candidate_inventory"]
    require(
        [row["candidate_id"] for row in candidates]
        == ["TW25.LOG_TWISTED_AFFINE", "TT26.RATIONAL_PERIODIC_ATOM"],
        "TPC193_CANDIDATE_IDS_DRIFT",
    )
    require(
        [row["eligible"] for row in candidates] == [False, False],
        "TPC193_ELIGIBILITY_DRIFT",
    )
    require(
        p193["corpus_partition"]["eligible_candidate_count"] == 0,
        "TPC193_ELIGIBLE_COUNT_DRIFT",
    )

    completion = p194["finite_certificate"]["completion_axes"]
    missing_axes = {
        "named_production_atom",
        "packet_schedule",
        "common_X_N_q_ranges",
        "uniform_constant_C",
        "positive_sigma",
        "target_normalization_selection",
        "complete_physical_loss_ledger",
    }
    require(
        {key for key, value in completion.items() if value == "MISSING"}
        == missing_axes,
        "TPC194_MISSING_AXES_DRIFT",
    )
    strict_equal(
        p194["finite_certificate"]["formula_type_registry"],
        FORMULA_TYPES,
        "TPC194.formula_type_registry",
    )
    require(
        p194["claim_boundary"]["packet_key_is_production_packet_schedule"]
        is False,
        "TPC194_PACKET_KEY_PROMOTION",
    )
    require(
        p194["claim_boundary"]["symbolic_packet_atom_is_named_production_atom"]
        is False,
        "TPC194_SYMBOLIC_ATOM_PROMOTION",
    )
    require(
        p203["first_missing_nodes"]["direct_production"]
        == "SOURCE_LOCKED_PRODUCTION_PACKET_PREFIX_CROSSWALK",
        "TPC203_DIRECT_FIRST_MISSING_DRIFT",
    )
    require(p203["verdict"] == "NOT_TESTABLE", "TPC203_VERDICT_DRIFT")
    require(
        p203["batch_stop"]["tpc204_authorized"] is False,
        "TPC203_HISTORICAL_AUTHORIZATION_DRIFT",
    )

    hardener = _load_hardener()
    hardening_artifacts = hardener.verify_active_artifacts()
    hardening_manifest = hardener.verify_manifest()

    return {
        "source_semantics_verified": True,
        "tpc159_all_prefix_power": False,
        "tpc167_fixed_atom": False,
        "tpc180_value_bearing_registry_rows": 0,
        "tpc193_direct_candidates": 2,
        "tpc193_eligible_candidates": 0,
        "tpc194_missing_production_axes": 7,
        "tpc194_formula_types": 3,
        "tpc194_hardening_artifacts": len(hardening_artifacts),
        "tpc194_manifest_pins": hardening_manifest["artifacts_pinned"],
        "tpc203_direct_first_missing": (
            "SOURCE_LOCKED_PRODUCTION_PACKET_PREFIX_CROSSWALK"
        ),
    }


def axis_row(
    axis_id: str,
    native_status: str,
    native_value: Any,
    source_locator: str,
    failure_code: str,
) -> dict[str, Any]:
    return {
        "axis_id": axis_id,
        "native_status": native_status,
        "native_value": native_value,
        "source_locator": source_locator,
        "production_match": False,
        "failure_code": failure_code,
    }


def candidate(
    candidate_id: str,
    object_type: str,
    primary_source_locator: str,
    native_formula_type: str | None,
    axes: list[dict[str, Any]],
) -> dict[str, Any]:
    require(
        [row["axis_id"] for row in axes] == PRODUCTION_AXES,
        f"AXIS_ORDER_BUILD:{candidate_id}",
    )
    crosswalk_rows = []
    for formula in FORMULA_TYPES:
        if candidate_id == "TPC183.N_EQUALS_T_SPECIALIZATION_PROPOSAL":
            relation = "INVALID_N_EQUALS_T_DOMAIN_CONFLATION"
        elif native_formula_type == formula["id"]:
            relation = "NATIVE_OBJECT_ONLY_NO_PRODUCTION_BRIDGE"
        else:
            relation = "NO_LITERAL_EXACT_CROSSWALK"
        crosswalk_rows.append(
            {
                "formula_type_id": formula["id"],
                "domain": formula["domain"],
                "normalization": formula["normalization"],
                "mapping_direction": "SOURCE_OBJECT_TO_PRODUCTION_PACKET_PREFIX",
                "source_locator": primary_source_locator,
                "relation": relation,
                "exact_crosswalk": False,
            }
        )
    first_index = next(
        index
        for index, row in enumerate(axes, start=1)
        if row["production_match"] is False
    )
    return {
        "candidate_id": candidate_id,
        "object_type": object_type,
        "object_type_eligible_for_finite_audit": True,
        "primary_source_locator": primary_source_locator,
        "native_formula_type": native_formula_type,
        "axis_audit": axes,
        "formula_crosswalk_audit": crosswalk_rows,
        "all_mismatch_gate_ids": [
            GATE_ORDER[index]
            for index, row in enumerate(axes, start=1)
            if row["production_match"] is False
        ]
        + [
            row["formula_type_id"] + "_CROSSWALK"
            for row in crosswalk_rows
            if row["exact_crosswalk"] is False
        ],
        "first_mismatch_gate_id": GATE_ORDER[first_index],
        "first_mismatch_gate_index": first_index,
        "complete_crosswalk": False,
    }


def build_candidates() -> list[dict[str, Any]]:
    return [
        candidate(
            "H9.phase_cell_registry",
            "EMPTY_SOURCE_LOCKED_REGISTRY_SLOT",
            "TPC180.payload#/candidate_registry",
            None,
            [
                axis_row(
                    "named_production_atom",
                    "MISSING",
                    None,
                    "TPC180.payload#/candidate_registry",
                    "NAMED_ATOM_ID_PHASE_VALUE_AND_LOCATOR_NULL",
                ),
                axis_row(
                    "packet_schedule",
                    "MISSING",
                    None,
                    "TPC180.payload#/candidate_registry",
                    "PACKET_SCHEDULE_LOCATOR_NULL",
                ),
                axis_row(
                    "common_X_N_q_ranges",
                    "MISSING",
                    None,
                    "TPC180.payload#/candidate_registry",
                    "NO_COMMON_RANGE_RECORD",
                ),
                axis_row(
                    "uniform_constant_C",
                    "MISSING",
                    None,
                    "TPC180.payload#/candidate_registry",
                    "NO_UNIFORM_CONSTANT_RECORD",
                ),
                axis_row(
                    "positive_sigma",
                    "MISSING",
                    None,
                    "TPC180.payload#/registry_contract/decay_axis",
                    "DECAY_AXIS_NONE",
                ),
                axis_row(
                    "target_normalization_selection",
                    "MISSING",
                    None,
                    "TPC180.payload#/candidate_registry",
                    "NO_TARGET_NORMALIZATION_RECORD",
                ),
                axis_row(
                    "complete_physical_loss_ledger",
                    "MISSING",
                    None,
                    "TPC180.payload#/candidate_registry",
                    "NO_PHYSICAL_LOSS_LEDGER",
                ),
            ],
        ),
        candidate(
            "TT26.RATIONAL_PERIODIC_ATOM",
            "TERMINAL_BLOCK_LOG_POWER_THEOREM",
            "TPC193.payload#/candidate_inventory/1",
            "CORE_TERMINAL_BLOCK",
            [
                axis_row(
                    "named_production_atom",
                    "MISSING",
                    None,
                    "TPC193.payload#/candidate_inventory/1",
                    "RATIONAL_ATOM_VALUE_AND_DENOMINATOR_LOCATOR_ABSENT",
                ),
                axis_row(
                    "packet_schedule",
                    "MISSING",
                    None,
                    "TPC193.payload#/candidate_inventory/1",
                    "NO_PRODUCTION_PACKET_SCHEDULE",
                ),
                axis_row(
                    "common_X_N_q_ranges",
                    "PRESENT_NATIVE_NOT_PRODUCTION_CREDIT",
                    "sqrt(X)<=N<=X outside E_X_star; q*R<=(log X)^eta_0",
                    "TPC193.payload#/candidate_inventory/1/constant_range_normalization_loss/range",
                    "RANGE_NATIVE_TO_TERMINAL_BLOCK_ONLY",
                ),
                axis_row(
                    "uniform_constant_C",
                    "PRESENT_NATIVE_NOT_PRODUCTION_CREDIT",
                    "absolute implicit constant inherited through TPC-149",
                    "TPC193.payload#/candidate_inventory/1/constant_range_normalization_loss/constants",
                    "CONSTANT_NOT_ATTACHED_TO_PRODUCTION_CROSSWALK",
                ),
                axis_row(
                    "positive_sigma",
                    "MISMATCH",
                    "LOG_POWER_ONLY",
                    "TPC193.payload#/candidate_inventory/1/axis_map/decay_axis",
                    "LOG_SAVING_IS_NOT_POSITIVE_X_POWER",
                ),
                axis_row(
                    "target_normalization_selection",
                    "PRESENT_NATIVE_NOT_PRODUCTION_CREDIT",
                    "q/N on N<t(z)<=2N",
                    "TPC193.payload#/candidate_inventory/1/constant_range_normalization_loss/normalization",
                    "TERMINAL_NORMALIZATION_NOT_PRODUCTION_SELECTION",
                ),
                axis_row(
                    "complete_physical_loss_ledger",
                    "MISSING",
                    None,
                    "TPC193.payload#/candidate_inventory/1/constant_range_normalization_loss/losses",
                    "ANALYTIC_LOSSES_NOT_COMPLETE_PHYSICAL_LEDGER",
                ),
            ],
        ),
        candidate(
            "A159.DYADIC_SHADOW_ALMOST_ENDPOINT_PREFIX",
            "CUMULATIVE_PREFIX_OUTSIDE_SHADOW_THEOREM",
            "TPC159.main#thm:main+eq:main",
            "CORE_CUMULATIVE_PREFIX",
            [
                axis_row(
                    "named_production_atom",
                    "MISSING",
                    None,
                    "TPC159.main#thm:main",
                    "RHO_IS_ARBITRARY_PERIODIC_WEIGHT_NOT_NAMED_PRODUCTION_ATOM",
                ),
                axis_row(
                    "packet_schedule",
                    "MISSING",
                    None,
                    "TPC159.audit#/endpoint_shadow",
                    "NO_EXACT_PRODUCTION_PACKET_SCHEDULE",
                ),
                axis_row(
                    "common_X_N_q_ranges",
                    "PRESENT_NATIVE_NOT_PRODUCTION_CREDIT",
                    "2^J*sqrt(X)<=T<=X and T outside S_X_J",
                    "TPC159.main#thm:main",
                    "RANGE_EXCLUDES_DYADIC_SHADOW",
                ),
                axis_row(
                    "uniform_constant_C",
                    "PRESENT_NATIVE_NOT_PRODUCTION_CREDIT",
                    "implicit Vinogradov constant",
                    "TPC159.main#eq:main",
                    "NO_EXPLICIT_PRODUCTION_UNIFORMITY_LEDGER",
                ),
                axis_row(
                    "positive_sigma",
                    "MISMATCH",
                    "LOG_POWER_AND_DYADIC_TAIL_ONLY",
                    "TPC159.audit#/theorem/positive_fixed_X_power",
                    "NO_POSITIVE_FIXED_X_POWER",
                ),
                axis_row(
                    "target_normalization_selection",
                    "PRESENT_NATIVE_NOT_PRODUCTION_CREDIT",
                    "q/T on 0<t(z)<=T",
                    "TPC159.main#eq:main",
                    "CUMULATIVE_NORMALIZATION_NOT_PRODUCTION_SELECTION",
                ),
                axis_row(
                    "complete_physical_loss_ledger",
                    "PRESENT_NATIVE_NOT_PRODUCTION_CREDIT",
                    "(log X)^(-kappa_0)+2^(-J)+q/T plus shadow loss",
                    "TPC159.main#eq:main",
                    "PARTIAL_ANALYTIC_LEDGER_NOT_COMPLETE_PHYSICAL_LEDGER",
                ),
            ],
        ),
        candidate(
            "A167.DIRECT_ADDITIVE_TWIST_PHASE_L2",
            "TERMINAL_BLOCK_PHASE_L2_THEOREM",
            "TPC167.main#thm:parseval+eq:power",
            "CORE_TERMINAL_BLOCK",
            [
                axis_row(
                    "named_production_atom",
                    "MISMATCH",
                    "PHASE_L2",
                    "TPC167.audit#/theorem",
                    "PHASE_L2_IS_NOT_NAMED_PRODUCTION_ATOM",
                ),
                axis_row(
                    "packet_schedule",
                    "MISSING",
                    None,
                    "TPC167.main#prop:grid",
                    "FOURIER_GRID_IS_NOT_PRODUCTION_PACKET_SCHEDULE",
                ),
                axis_row(
                    "common_X_N_q_ranges",
                    "PRESENT_NATIVE_NOT_PRODUCTION_CREDIT",
                    "q<=(log X)^eta_0 and N>=sqrt(X)",
                    "TPC167.audit#/power_envelope",
                    "RANGE_ATTACHED_TO_PHASE_L2_ONLY",
                ),
                axis_row(
                    "uniform_constant_C",
                    "PRESENT_NATIVE_NOT_PRODUCTION_CREDIT",
                    "sqrt(2) with polylog factor in phase L2",
                    "TPC167.main#eq:power",
                    "CONSTANT_HAS_WRONG_NORM_AXIS",
                ),
                axis_row(
                    "positive_sigma",
                    "MISMATCH",
                    "FORMAL_1/4_ONLY_IN_PHASE_L2_WITH_POLYLOG",
                    "TPC167.audit#/power_envelope",
                    "PHASE_L2_POWER_IS_NOT_FIXED_ATOM_POWER",
                ),
                axis_row(
                    "target_normalization_selection",
                    "PRESENT_NATIVE_NOT_PRODUCTION_CREDIT",
                    "q/N on N<t(z)<=2N",
                    "TPC167.main#eq:transform",
                    "TERMINAL_NORMALIZATION_NOT_PRODUCTION_SELECTION",
                ),
                axis_row(
                    "complete_physical_loss_ledger",
                    "MISSING",
                    None,
                    "TPC167.audit#/power_envelope",
                    "NO_COMPLETE_PHYSICAL_LOSS_LEDGER",
                ),
            ],
        ),
        candidate(
            "TPC183.N_EQUALS_T_SPECIALIZATION_PROPOSAL",
            "INVALID_TERMINAL_TO_CUMULATIVE_SPECIALIZATION",
            "TPC183.payload#/theorem",
            None,
            [
                axis_row(
                    "named_production_atom",
                    "MISSING",
                    None,
                    "TPC183.payload#/theorem",
                    "ATOM_OCCURS_ONLY_AS_UNINSTANTIATED_HYPOTHESIS",
                ),
                axis_row(
                    "packet_schedule",
                    "MISSING",
                    None,
                    "TPC183.payload#/proof",
                    "NO_PACKET_SCHEDULE_VALUE",
                ),
                axis_row(
                    "common_X_N_q_ranges",
                    "MISSING",
                    None,
                    "TPC183.payload#/proof",
                    "NO_COMMON_RANGE_VALUE",
                ),
                axis_row(
                    "uniform_constant_C",
                    "MISSING",
                    None,
                    "TPC183.payload#/theorem",
                    "CONSTANT_IS_UNINSTANTIATED_HYPOTHESIS",
                ),
                axis_row(
                    "positive_sigma",
                    "MISSING",
                    None,
                    "TPC183.payload#/theorem",
                    "SIGMA_IS_UNINSTANTIATED_HYPOTHESIS",
                ),
                axis_row(
                    "target_normalization_selection",
                    "MISMATCH",
                    "N=T leaves T<t(z)<=2T and does not give 0<t(z)<=T",
                    "TPC193.main#prop:formula",
                    "TERMINAL_AND_CUMULATIVE_DOMAINS_NOT_IDENTICAL",
                ),
                axis_row(
                    "complete_physical_loss_ledger",
                    "MISSING",
                    None,
                    "TPC183.payload#/theorem",
                    "NO_PHYSICAL_LOSS_LEDGER",
                ),
            ],
        ),
        candidate(
            "O161.BAD_ENDPOINT_POINTWISE_FIXED_ATOM_CONTRACT",
            "VERBAL_CUMULATIVE_ALL_PREFIX_TARGET_WITHOUT_NAMED_ATOM_VALUE",
            "TPC184.payload#/result",
            None,
            [
                axis_row(
                    "named_production_atom",
                    "MISSING",
                    None,
                    "TPC184.payload#/required_quantifier_signature/phase_axis",
                    "PRESCRIBED_BAD_ENDPOINT_ATOM_HAS_NO_SOURCE_LOCKED_VALUE",
                ),
                axis_row(
                    "packet_schedule",
                    "MISSING",
                    None,
                    "TPC184.payload#/required_quantifier_signature/endpoint_axis",
                    "ALL_PREFIX_QUANTIFIER_IS_NOT_EXACT_PRODUCTION_SCHEDULE",
                ),
                axis_row(
                    "common_X_N_q_ranges",
                    "MISSING",
                    None,
                    "TPC184.payload#/result",
                    "NO_LITERAL_COMMON_X_N_Q_RANGE_VALUES",
                ),
                axis_row(
                    "uniform_constant_C",
                    "MISSING",
                    None,
                    "TPC184.payload#/result",
                    "NO_UNIFORM_CONSTANT_VALUE",
                ),
                axis_row(
                    "positive_sigma",
                    "MISSING",
                    None,
                    "TPC184.payload#/smallest_literal_missing_theorem",
                    "FIXED_ATOM_POWER_SAVING_INSIDE_SHADOW_OPEN",
                ),
                axis_row(
                    "target_normalization_selection",
                    "PRESENT_NATIVE_NOT_PRODUCTION_CREDIT",
                    "verbal q/T cumulative actual-core all-prefix target",
                    "TPC184.payload#/result",
                    "VERBAL_NORMALIZATION_NOT_ATTACHED_TO_NAMED_ATOM_RECORD",
                ),
                axis_row(
                    "complete_physical_loss_ledger",
                    "MISSING",
                    None,
                    "TPC184.payload#/endpoint_ledger",
                    "NO_COMPLETE_PHYSICAL_LOSS_LEDGER",
                ),
            ],
        ),
        candidate(
            "O161.DIRECT_ADDITIVE_TWIST_FIXED_ATOM_CONTRACT",
            "VERBAL_DIRECT_TARGET_WITHOUT_LITERAL_PREFIX_DOMAIN",
            "TPC189.payload#/result",
            None,
            [
                axis_row(
                    "named_production_atom",
                    "MISSING",
                    None,
                    "TPC189.payload#/result",
                    "PRESCRIBED_ATOM_HAS_NO_SOURCE_LOCKED_VALUE",
                ),
                axis_row(
                    "packet_schedule",
                    "MISSING",
                    None,
                    "TPC189.payload#/result",
                    "NO_PACKET_SCHEDULE_VALUE",
                ),
                axis_row(
                    "common_X_N_q_ranges",
                    "MISSING",
                    None,
                    "TPC189.payload#/result",
                    "NO_COMMON_RANGE_VALUE",
                ),
                axis_row(
                    "uniform_constant_C",
                    "MISSING",
                    None,
                    "TPC189.payload#/result",
                    "NO_UNIFORM_CONSTANT_VALUE",
                ),
                axis_row(
                    "positive_sigma",
                    "MISSING",
                    None,
                    "TPC189.payload#/smallest_literal_missing_theorem",
                    "FIXED_ATOM_POWER_SAVING_OPEN",
                ),
                axis_row(
                    "target_normalization_selection",
                    "PRESENT_NATIVE_NOT_PRODUCTION_CREDIT",
                    "verbal q/N with no literal direct-prefix domain",
                    "TPC189.payload#/result",
                    "NORMALIZATION_NOT_ATTACHED_TO_UNIQUE_LITERAL_OBJECT",
                ),
                axis_row(
                    "complete_physical_loss_ledger",
                    "MISSING",
                    None,
                    "TPC189.payload#/result",
                    "NO_COMPLETE_PHYSICAL_LOSS_LEDGER",
                ),
            ],
        ),
        candidate(
            "TW25.LOG_TWISTED_AFFINE",
            "LOG_WEIGHTED_FIXED_ATOM_AFFINE_THEOREM",
            "TPC193.payload#/candidate_inventory/0",
            None,
            [
                axis_row(
                    "named_production_atom",
                    "MISMATCH",
                    "every fixed gamma but no production atom locator",
                    "TPC193.payload#/candidate_inventory/0",
                    "FIXED_GAMMA_IS_NOT_SOURCE_LOCKED_PRODUCTION_ATOM",
                ),
                axis_row(
                    "packet_schedule",
                    "MISSING",
                    None,
                    "TPC193.payload#/candidate_inventory/0",
                    "NO_PRODUCTION_PACKET_SCHEDULE",
                ),
                axis_row(
                    "common_X_N_q_ranges",
                    "PRESENT_NATIVE_NOT_PRODUCTION_CREDIT",
                    "fixed affine data and X tends to infinity",
                    "TPC193.payload#/candidate_inventory/0/constant_range_normalization_loss/range",
                    "ASYMPTOTIC_FIXED_DATA_NOT_PRODUCTION_RANGE",
                ),
                axis_row(
                    "uniform_constant_C",
                    "MISSING",
                    None,
                    "TPC193.payload#/candidate_inventory/0/constant_range_normalization_loss/constants",
                    "QUALITATIVE_O1_HAS_NO_EFFECTIVE_UNIFORM_C",
                ),
                axis_row(
                    "positive_sigma",
                    "MISMATCH",
                    "QUALITATIVE_LOG_AVERAGED_O1",
                    "TPC193.payload#/candidate_inventory/0/axis_map/decay_axis",
                    "NO_POSITIVE_FIXED_X_POWER",
                ),
                axis_row(
                    "target_normalization_selection",
                    "MISMATCH",
                    "(1/log X) sum ... /n",
                    "TPC193.payload#/candidate_inventory/0/constant_range_normalization_loss/normalization",
                    "LOG_WEIGHTED_NORMALIZATION_NOT_NATURAL_TARGET",
                ),
                axis_row(
                    "complete_physical_loss_ledger",
                    "MISSING",
                    None,
                    "TPC193.payload#/candidate_inventory/0/constant_range_normalization_loss/losses",
                    "NO_COMPLETE_PHYSICAL_LOSS_LEDGER",
                ),
            ],
        ),
        candidate(
            "PHYSICAL_PACKET_PREFIX",
            "RESOLVED_PER_PACKET_UNNORMALIZED_PHYSICAL_PREFIX",
            "TPC194.payload#/finite_certificate/resolved_packet_formula",
            "PHYSICAL_PACKET_PREFIX",
            [
                axis_row(
                    "named_production_atom",
                    "MISMATCH",
                    "symbolic alpha_xi_X",
                    "TPC194.payload#/finite_certificate/resolved_packet_formula/packet_atom",
                    "SYMBOLIC_PACKET_ATOM_IS_NOT_NAMED_PRODUCTION_ATOM",
                ),
                axis_row(
                    "packet_schedule",
                    "MISMATCH",
                    "xi=(theta,c,kappa,r)",
                    "TPC194.payload#/finite_certificate/resolved_packet_formula/key",
                    "RESOLVED_PACKET_KEY_IS_NOT_PRODUCTION_SCHEDULE",
                ),
                axis_row(
                    "common_X_N_q_ranges",
                    "MISSING",
                    None,
                    "TPC194.payload#/finite_certificate/completion_axes/common_X_N_q_ranges",
                    "COMMON_RANGE_MISSING",
                ),
                axis_row(
                    "uniform_constant_C",
                    "MISSING",
                    None,
                    "TPC194.payload#/finite_certificate/completion_axes/uniform_constant_C",
                    "UNIFORM_CONSTANT_MISSING",
                ),
                axis_row(
                    "positive_sigma",
                    "MISSING",
                    None,
                    "TPC194.payload#/finite_certificate/completion_axes/positive_sigma",
                    "POSITIVE_SIGMA_MISSING",
                ),
                axis_row(
                    "target_normalization_selection",
                    "MISSING",
                    None,
                    "TPC194.payload#/finite_certificate/completion_axes/target_normalization_selection",
                    "TARGET_NORMALIZATION_SELECTION_MISSING",
                ),
                axis_row(
                    "complete_physical_loss_ledger",
                    "MISSING",
                    None,
                    "TPC194.payload#/finite_certificate/completion_axes/complete_physical_loss_ledger",
                    "COMPLETE_PHYSICAL_LOSS_LEDGER_MISSING",
                ),
            ],
        ),
    ]


def universe_digest(
    candidates: list[dict[str, Any]], exclusions: list[dict[str, Any]]
) -> str:
    return sha256_value(
        {
            "candidate_ids": [row["candidate_id"] for row in candidates],
            "candidate_locators": [
                row["primary_source_locator"] for row in candidates
            ],
            "excluded_record_ids": [row["record_id"] for row in exclusions],
            "excluded_locators": [row["source_locator"] for row in exclusions],
        }
    )


def build_payload() -> dict[str, Any]:
    upstream = upstream_semantic_summary()
    candidates = build_candidates()
    complete_ids = [
        row["candidate_id"] for row in candidates if row["complete_crosswalk"]
    ]
    require(complete_ids == [], "BUILD_COMPLETE_CANDIDATE_UNEXPECTED")
    return {
        "schema": "tpc-204-source-locked-production-registry-crosswalk-v1",
        "paper": 204,
        "title": (
            "Source-Locked Production Registry Crosswalks: "
            "A Finite Exact-Matching and First-Mismatch Certificate"
        ),
        "classification": "PRODUCTION_REGISTRY_CROSSWALK_CENSUS_L1",
        "authorization": {
            "tpc204_authorized": True,
            "authorization_record": (
                "USER_EXPLICIT_FINITE_TPC204_AUTHORIZATION_2026_07_30"
            ),
            "authorized_scope": (
                "FINITE_EXACT_MATCHING_OR_FIRST_MISMATCH_CROSSWALK_AUDIT"
            ),
            "is_mathematical_evidence": False,
            "implies_direct_trigger_pass": False,
            "implies_any_reopen_trigger": False,
        },
        "snapshot": {
            "date": "2026-07-30",
            "corpus_id": CORPUS_ID,
            "corpus_scope": (
                "EXACT_DECLARED_DIRECT_PRODUCTION_LINEAGE_OBJECTS_ONLY"
            ),
            "discovery_rule": (
                "EXPLICIT_SOURCE_BINDINGS_AND_CANONICAL_OBJECT_SELECTORS"
            ),
            "canonical_candidate_order": (
                "SOURCE_LINEAGE_THEN_LITERAL_OBJECT_ROLE"
            ),
            "future_sources_automatically_included": False,
            "global_repository_exhaustion_claimed": False,
            "hash_mode": HASH_MODE,
        },
        "candidate_universe_contract": {
            "inclusion_predicate": (
                "SOURCE_BACKED_DISTINCT_OBJECT_IN_DECLARED_LINEAGE_WITH_"
                "A_LITERAL_REGISTRY_FORMULA_THEOREM_OR_TARGET_ROLE_RELEVANT_"
                "TO_THE_PRODUCTION_CROSSWALK"
            ),
            "exclusion_predicate": (
                "AUXILIARY_PHASE_MEASURE_GRID_INTERVAL_OR_DUPLICATE_IMPORT_"
                "WITHOUT_A_DISTINCT_PRODUCTION_CROSSWALK_OBJECT"
            ),
            "candidate_count": len(candidates),
            "audited_candidate_count": len(candidates),
            "omitted_candidate_count": 0,
            "duplicate_candidate_count": 0,
            "axis_cell_count": len(candidates) * len(PRODUCTION_AXES),
            "crosswalk_cell_count": len(candidates) * len(FORMULA_TYPES),
            "included_candidate_ids": [
                row["candidate_id"] for row in candidates
            ],
            "excluded_record_count": len(EXCLUSION_LEDGER),
            "candidate_universe_digest": universe_digest(
                candidates, EXCLUSION_LEDGER
            ),
        },
        "gate_order": [
            {"index": index, "gate_id": gate_id}
            for index, gate_id in enumerate(GATE_ORDER)
        ],
        "production_axes": PRODUCTION_AXES,
        "formula_type_registry": copy.deepcopy(FORMULA_TYPES),
        "formula_type_distinctness": {
            "pairwise_distinct": True,
            "block_equals_cumulative": False,
            "block_equals_physical": False,
            "cumulative_equals_physical": False,
        },
        "candidate_audits": candidates,
        "excluded_record_ledger": copy.deepcopy(EXCLUSION_LEDGER),
        "decision": {
            "verdict": "FIRST_MISMATCH_CERTIFIED_NOT_TESTABLE",
            "theorem_status": (
                "PROVED_LOCKED_REGISTRY_FIRST_MISMATCH_"
                "NO_COMPLETE_CROSSWALK_L1"
            ),
            "complete_crosswalk_count": len(complete_ids),
            "complete_crosswalk_candidate_ids": complete_ids,
            "unique_complete_crosswalk": False,
            "unique_complete_crosswalk_candidate_id": None,
            "first_common_missing_production_axis": (
                "named_production_atom"
            ),
            "first_common_missing_gate_id": "NAMED_PRODUCTION_ATOM",
            "direct_trigger": "FAIL",
            "reopen_trigger_passed": False,
            "theorem_backed_natural_q_over_N_fixed_atom_power": False,
            "next_route": (
                "SEARCH_FOR_SOURCE_LOCKED_NAMED_PRODUCTION_ATOM_RECORD_"
                "OR_GENUINE_FIXED_ATOM_THEOREM"
            ),
            "batch_stop": "USER_CONFIRMATION_REQUIRED",
            "next_paper": None,
            "tpc205_authorized": False,
        },
        "first_missing_nodes": {
            "global": "H1.source_backed_local_occurrence_edge_family",
            "selected_pointwise": "LITERAL_FIXED_ATOM_ARITHMETIC_CANCELLATION",
            "direct_production_parent": (
                "SOURCE_LOCKED_PRODUCTION_PACKET_PREFIX_CROSSWALK"
            ),
            "direct_crosswalk_subgate": "NAMED_PRODUCTION_ATOM",
        },
        "route_state": {
            "bad_endpoint_O161_parent": "OPEN",
            "direct_twist_O161_parent": "OPEN",
            "global_architecture": "OPEN",
            "fixed_atom_decay_obtained": False,
            "literal_fixed_atom_cancellation_obtained": False,
            "program_positive_L2": False,
            "L2_result": "NONE",
        },
        "endpoint_ledger": {
            "named_atom_sigma_credit": {"numerator": 0, "denominator": 1},
            "required_strict_budget": {"numerator": 1, "denominator": 400},
            "state": "UNPAID",
        },
        "stop_scoped": STOP_SCOPED,
        "claim_boundary": {
            "authorization_is_theorem_evidence": False,
            "authorization_implies_direct_trigger": False,
            "authorization_implies_reopen": False,
            "first_mismatch_is_complete_crosswalk": False,
            "unique_crosswalk_would_imply_direct_trigger": False,
            "block_equals_cumulative_prefix": False,
            "block_equals_physical_prefix": False,
            "cumulative_equals_physical_prefix": False,
            "symbolic_packet_atom_is_named_production_atom": False,
            "packet_key_is_production_packet_schedule": False,
            "phase_L2_is_named_atom_control": False,
            "log_saving_is_positive_X_power": False,
            "finite_corpus_stop_is_global_nonexistence": False,
            "hash_integrity_is_theorem_evidence": False,
            "fixed_atom_decay_obtained": False,
            "strict_one_over_400": False,
            "program_positive_L2": False,
            "prime_pair_lower_bound": False,
            "twin_prime_theorem": False,
        },
        "level_ledger": {
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
        "upstream_semantic_summary": upstream,
        "source_locks": source_locks(),
        "result_summary": (
            "Nine distinct plausible crosswalk objects are source-locked "
            "and audited on all seven production axes and all three formula "
            "types.  No complete crosswalk exists in the declared corpus; "
            "the shared first production-axis mismatch is the absence of a "
            "source-locked named production atom."
        ),
    }


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
        raise TypeError(f"unsupported schema value: {type(item)}")

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
        properties = schema["properties"]
        if set(value) != set(schema["required"]):
            return False
        if schema.get("additionalProperties") is not False:
            return False
        return all(schema_accepts(properties[key], value[key]) for key in value)
    if expected_type == "array":
        if type(value) is not list:
            return False
        if len(value) != schema["minItems"] or len(value) != schema["maxItems"]:
            return False
        if schema.get("items") is not False:
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
        return value is None
    return False


def semantic_result(payload: dict[str, Any]) -> dict[str, Any]:
    expected = build_payload()
    strict_equal(payload, expected)
    candidates = payload["candidate_audits"]
    require(
        len(candidates)
        == payload["candidate_universe_contract"]["candidate_count"]
        == 9,
        "CANDIDATE_COUNT",
    )
    require(
        len({row["candidate_id"] for row in candidates}) == len(candidates),
        "DUPLICATE_CANDIDATE_ID",
    )
    for row in candidates:
        require(
            len(row["axis_audit"]) == len(PRODUCTION_AXES),
            f"AXIS_COUNT:{row['candidate_id']}",
        )
        require(
            [cell["axis_id"] for cell in row["axis_audit"]]
            == PRODUCTION_AXES,
            f"AXIS_ORDER:{row['candidate_id']}",
        )
        require(
            row["first_mismatch_gate_id"] == "NAMED_PRODUCTION_ATOM",
            f"FIRST_MISMATCH:{row['candidate_id']}",
        )
        require(
            row["first_mismatch_gate_index"] == 1,
            f"FIRST_MISMATCH_INDEX:{row['candidate_id']}",
        )
        require(
            len(row["formula_crosswalk_audit"]) == len(FORMULA_TYPES),
            f"CROSSWALK_COUNT:{row['candidate_id']}",
        )
        require(
            all(
                cell["exact_crosswalk"] is False
                for cell in row["formula_crosswalk_audit"]
            ),
            f"EXACT_CROSSWALK_PROMOTION:{row['candidate_id']}",
        )
        require(
            row["complete_crosswalk"] is False,
            f"COMPLETE_CROSSWALK_PROMOTION:{row['candidate_id']}",
        )
    require(
        payload["decision"]["complete_crosswalk_count"] == 0,
        "COMPLETE_COUNT",
    )
    require(
        payload["decision"]["verdict"]
        == "FIRST_MISMATCH_CERTIFIED_NOT_TESTABLE",
        "VERDICT",
    )
    return {
        "semantic_contract_version": 1,
        "declared_candidates_verified": 9,
        "excluded_records_verified": 4,
        "production_axes_per_candidate": 7,
        "axis_cells_verified": 63,
        "formula_types_verified": 3,
        "crosswalk_cells_verified": 27,
        "complete_crosswalks": 0,
        "shared_first_mismatch_gate": "NAMED_PRODUCTION_ATOM",
        "new_stop_cell": NEW_STOP_CELL,
        "mathematical_reopen": False,
    }


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


def semantic_rejected(value: dict[str, Any]) -> bool:
    try:
        semantic_result(value)
    except (ContractError, DuplicateKeyError, KeyError, TypeError, ValueError):
        return True
    return False


def build_base_mutation_registry(
    payload: dict[str, Any], payload_schema: dict[str, Any]
) -> list[dict[str, Any]]:
    rows = []
    for name in BASE_MUTATIONS:
        mutated = mutate_base(payload, name)
        rows.append(
            {
                "name": name,
                "payload_changed": canonical(mutated) != canonical(payload),
                "rejected_by_active_schema": not schema_accepts(
                    payload_schema, mutated
                ),
            }
        )
    require(
        all(row["payload_changed"] for row in rows),
        "BASE_MUTATION_NOOP",
    )
    require(
        all(row["rejected_by_active_schema"] for row in rows),
        "BASE_MUTATION_ACCEPTED",
    )
    return rows


def build_semantic_mutation_registry(
    payload: dict[str, Any]
) -> list[dict[str, Any]]:
    rows = []
    for name in SEMANTIC_MUTATIONS:
        mutated = mutate_semantic(payload, name)
        regenerated_schema = exact_schema(mutated)
        rows.append(
            {
                "name": name,
                "payload_changed": canonical(mutated) != canonical(payload),
                "regenerated_schema_accepts": schema_accepts(
                    regenerated_schema, mutated
                ),
                "independent_semantic_checker_rejected": semantic_rejected(
                    mutated
                ),
            }
        )
    require(
        all(row["payload_changed"] for row in rows),
        "SEMANTIC_MUTATION_NOOP",
    )
    require(
        all(row["regenerated_schema_accepts"] for row in rows),
        "REGENERATED_SCHEMA_FIXTURE_INVALID",
    )
    require(
        all(row["independent_semantic_checker_rejected"] for row in rows),
        "SEMANTIC_MUTATION_ACCEPTED",
    )
    return rows


def build_audit(
    payload: dict[str, Any],
    payload_schema: dict[str, Any],
) -> dict[str, Any]:
    finite_result = semantic_result(payload)
    base_registry = build_base_mutation_registry(payload, payload_schema)
    semantic_registry = build_semantic_mutation_registry(payload)
    return {
        "schema": (
            "tpc-204-source-locked-production-registry-crosswalk-audit-v1"
        ),
        "paper": 204,
        "payload_sha256": sha256_value(payload),
        "payload_schema_sha256": sha256_value(payload_schema),
        "checks": {
            "authorization_scope_exact": True,
            "authorization_not_mathematical_evidence": True,
            "declared_candidate_universe_closed": True,
            "candidate_count_9": True,
            "all_candidates_audited": True,
            "axis_cells_63": True,
            "crosswalk_cells_27": True,
            "formula_types_pairwise_distinct": True,
            "complete_crosswalk_count_0": True,
            "shared_first_mismatch_named_production_atom": True,
            "direct_trigger_fail": True,
            "parents_and_architecture_open": True,
            "endpoint_credit_zero": True,
            "strict_one_over_400_unpaid": True,
            "L2_none": True,
            "TPC193_V1_stop_scoped": True,
            "new_TPC204_stop_scoped": True,
            "all_source_locks_integrity_only": True,
            "upstream_TPC194_hardening_verified": True,
        },
        "finite_check_result": finite_result,
        "semantic_contract_result": finite_result,
        "base_mutation_registry": base_registry,
        "semantic_mutation_registry": semantic_registry,
        "all_checks_pass": True,
    }


def expected_artifacts() -> tuple[
    dict[str, Any], dict[str, Any], dict[str, Any], dict[str, Any]
]:
    payload = build_payload()
    payload_schema = exact_schema(
        payload,
        "tpc204-source-locked-production-registry-crosswalk-v1.schema.json",
    )
    audit = build_audit(payload, payload_schema)
    audit_schema = exact_schema(
        audit,
        (
            "tpc204-source-locked-production-registry-crosswalk-"
            "audit-v1.schema.json"
        ),
    )
    return payload, audit, payload_schema, audit_schema


def materialize() -> None:
    payload, audit, payload_schema, audit_schema = expected_artifacts()
    PAYLOAD_PATH.write_text(canonical(payload), encoding="utf-8", newline="\n")
    AUDIT_PATH.write_text(canonical(audit), encoding="utf-8", newline="\n")
    PAYLOAD_SCHEMA_PATH.write_text(
        canonical(payload_schema), encoding="utf-8", newline="\n"
    )
    AUDIT_SCHEMA_PATH.write_text(
        canonical(audit_schema), encoding="utf-8", newline="\n"
    )


def verify_active_artifacts() -> dict[str, Any]:
    payload, audit, payload_schema, audit_schema = expected_artifacts()
    disk_payload = load_json(PAYLOAD_PATH, canonical_bytes=True)
    disk_audit = load_json(AUDIT_PATH, canonical_bytes=True)
    disk_payload_schema = load_json(PAYLOAD_SCHEMA_PATH, canonical_bytes=True)
    disk_audit_schema = load_json(AUDIT_SCHEMA_PATH, canonical_bytes=True)
    strict_equal(disk_payload, payload, "payload")
    strict_equal(disk_audit, audit, "audit")
    strict_equal(disk_payload_schema, payload_schema, "payload_schema")
    strict_equal(disk_audit_schema, audit_schema, "audit_schema")
    require(
        schema_accepts(disk_payload_schema, disk_payload),
        "PAYLOAD_SCHEMA_REJECTED",
    )
    require(
        schema_accepts(disk_audit_schema, disk_audit),
        "AUDIT_SCHEMA_REJECTED",
    )
    require(
        all(
            row["rejected_by_active_schema"]
            for row in disk_audit["base_mutation_registry"]
        ),
        "DISK_BASE_MUTATION_FAILURE",
    )
    require(
        all(
            row["independent_semantic_checker_rejected"]
            for row in disk_audit["semantic_mutation_registry"]
        ),
        "DISK_SEMANTIC_MUTATION_FAILURE",
    )
    return {
        **semantic_result(disk_payload),
        "base_mutations_rejected": len(BASE_MUTATIONS),
        "semantic_mutations_rejected": len(SEMANTIC_MUTATIONS),
        "source_locks_verified": len(disk_payload["source_locks"]),
    }


def manifest_semantic_summary() -> dict[str, Any]:
    return {
        "contract": "TPC204_FINITE_PRODUCTION_REGISTRY_CROSSWALK_V1",
        "manifest_trust": (
            "REPOSITORY_PIN_REQUIRES_GIT_REVIEW_NOT_EXTERNAL_SIGNATURE"
        ),
        "declared_candidates": 9,
        "production_axes": 7,
        "formula_types": 3,
        "complete_crosswalks": 0,
        "shared_first_mismatch": "NAMED_PRODUCTION_ATOM",
        "base_mutations": len(BASE_MUTATIONS),
        "semantic_mutations": len(SEMANTIC_MUTATIONS),
    }


def build_manifest() -> dict[str, Any]:
    for relative in ACTIVE_ARTIFACTS:
        require((REPO / relative).is_file(), f"MANIFEST_ARTIFACT_MISSING:{relative}")
    return {
        "schema": "tpc204-certificate-manifest-v1",
        "mode": "MANUALLY_REFRESHED_NOT_GENERATOR_SIGNED",
        "artifacts": [
            {"path": relative, "raw_sha256": raw_sha256(REPO / relative)}
            for relative in ACTIVE_ARTIFACTS
        ],
        "semantic_contract": manifest_semantic_summary(),
    }


def verify_manifest() -> dict[str, Any]:
    require(MANIFEST_PATH.is_file(), "TPC204_MANIFEST_MISSING")
    manifest = load_json(MANIFEST_PATH, canonical_bytes=True)
    require(
        set(manifest) == {"schema", "mode", "artifacts", "semantic_contract"},
        "MANIFEST_KEY_SET",
    )
    require(
        manifest["schema"] == "tpc204-certificate-manifest-v1",
        "MANIFEST_SCHEMA",
    )
    require(
        manifest["mode"] == "MANUALLY_REFRESHED_NOT_GENERATOR_SIGNED",
        "MANIFEST_MODE",
    )
    strict_equal(
        manifest["semantic_contract"],
        manifest_semantic_summary(),
        "manifest.semantic_contract",
    )
    require(
        [row["path"] for row in manifest["artifacts"]] == ACTIVE_ARTIFACTS,
        "MANIFEST_ARTIFACT_ALLOWLIST",
    )
    for row in manifest["artifacts"]:
        require(
            set(row) == {"path", "raw_sha256"},
            f"MANIFEST_ROW_KEYS:{row.get('path')}",
        )
        path = REPO / row["path"]
        require(path.is_file(), f"MANIFEST_ARTIFACT_MISSING:{row['path']}")
        require(
            raw_sha256(path) == row["raw_sha256"],
            f"MANIFEST_HASH_MISMATCH:{row['path']}",
        )
    return {
        "artifacts_pinned": len(manifest["artifacts"]),
        "trust_mode": manifest["semantic_contract"]["manifest_trust"],
    }


def main() -> None:
    if not __debug__:
        raise RuntimeError(
            "optimized Python disables assertions in imported upstream code; "
            "TPC-204 validation fails closed"
        )
    parser = argparse.ArgumentParser()
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--check", action="store_true")
    group.add_argument("--refresh-manifest", action="store_true")
    args = parser.parse_args()

    result = verify_active_artifacts()
    if args.refresh_manifest:
        MANIFEST_PATH.write_text(
            canonical(build_manifest()), encoding="utf-8", newline="\n"
        )
    manifest = verify_manifest()
    print(
        json.dumps(
            {
                "paper": 204,
                "verdict": "FIRST_MISMATCH_CERTIFIED_NOT_TESTABLE",
                "certificate": result,
                "manifest": manifest,
                "refreshed": args.refresh_manifest,
            },
            sort_keys=True,
        )
    )


if __name__ == "__main__":
    main()
