#!/usr/bin/env python3
"""Build and audit the TPC-193 literal fixed-atom mechanism gate."""

from __future__ import annotations

import argparse
import copy
import hashlib
import json
from pathlib import Path
from typing import Any, Callable


HERE = Path(__file__).resolve().parent
PAPER = HERE.parent
REPO = PAPER.parents[1]
STEM = "tpc193_literal_fixed_atom_candidate_mechanism_gate"
PAYLOAD_PATH = HERE / f"{STEM}.json"
AUDIT_PATH = HERE / f"{STEM}_audit.json"
PAYLOAD_SCHEMA_PATH = (
    PAPER
    / "schemas"
    / "tpc193-literal-fixed-atom-candidate-mechanism-gate-v1.schema.json"
)
AUDIT_SCHEMA_PATH = (
    PAPER
    / "schemas"
    / "tpc193-literal-fixed-atom-candidate-mechanism-gate-audit-v1.schema.json"
)

SCHEMA_URI = "https://json-schema.org/draft/2020-12/schema"
HASH_MODE = "CANONICAL_UTF8_LF_V2"

SOURCE_PATHS = {
    "TPC129.main": REPO
    / "papers"
    / "tpc-129-log-chowla-quantifier-firewall"
    / "main.tex",
    "TPC138.main": REPO
    / "papers"
    / "tpc-138-even-carrier-shift-one-firewall"
    / "main.tex",
    "TPC149.main": REPO
    / "papers"
    / "tpc-149-small-polylog-determinant-two-mobius-corridor"
    / "main.tex",
    "TPC158.main": REPO
    / "papers"
    / "tpc-158-additive-phase-major-minor-gate"
    / "main.tex",
    "TPC159.readme": REPO
    / "papers"
    / "tpc-159-dyadic-shadow-prefix-lifting"
    / "README.md",
    "TPC167.main": REPO
    / "papers"
    / "tpc-167-direct-additive-twist-parseval"
    / "main.tex",
    "TPC168.readme": REPO
    / "papers"
    / "tpc-168-separated-phase-registry-sieve"
    / "README.md",
    "TPC169.main": REPO
    / "papers"
    / "tpc-169-maximal-prefix-phase-metric"
    / "main.tex",
    "TPC170.audit": REPO
    / "papers"
    / "tpc-170-metric-packet-corridor-return"
    / "experiments"
    / "tpc170_metric_corridor_audit.json",
    "TPC180.census": REPO
    / "papers"
    / "tpc-180-production-phase-registry-census"
    / "experiments"
    / "tpc180_phase_registry_census.json",
    "TPC181.gate": REPO
    / "papers"
    / "tpc-181-metric-fixed-atom-selector-gate"
    / "experiments"
    / "tpc181_selector_gate.json",
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
    "TPC187.payload": REPO
    / "papers"
    / "tpc-187-size-only-local-oscillation-barrier"
    / "experiments"
    / "tpc187_size_only_local_oscillation_barrier.json",
    "TPC189.payload": REPO
    / "papers"
    / "tpc-189-direct-twist-literal-target-contract"
    / "experiments"
    / "tpc189_direct_twist_literal_target_contract.json",
    "TPC190.payload": REPO
    / "papers"
    / "tpc-190-parseval-to-atom-method-barrier"
    / "experiments"
    / "tpc190_parseval_to_atom_method_barrier.json",
    "TPC192.payload": REPO
    / "papers"
    / "tpc-192-mvp9-pointwise-frontier-route-decision"
    / "experiments"
    / "tpc192_mvp9_pointwise_frontier_route_decision.json",
}

REQUIRED_AXES = {
    "carrier_axis": "ACTUAL_FIXED_H0_PACKET",
    "decay_axis": "FIXED_X_POWER_FIXED_ATOM",
    "endpoint_axis": "DETERMINISTIC_ALL_PREFIX",
    "phase_axis": "NAMED_FIXED_ATOM",
    "scale_axis": "DETERMINISTIC_ALL_SCALE",
    "support_axis": "ACTUAL_ACTIVE_SUPPORT",
}

ELIGIBILITY_KEYS = [
    "all_constants_ranges_normalizations_losses_exposed",
    "carrier_axis_match",
    "decay_axis_match",
    "direct_literal_two_mobius",
    "endpoint_axis_match",
    "formula_complete_target_available",
    "normalization_q_over_endpoint_natural",
    "not_stopped_cell_repackage",
    "phase_axis_match",
    "prescribed_atom_source_locked_or_uniform",
    "scale_axis_match",
    "support_axis_match",
    "theorem_backed",
]

MUTATION_NAMES = [
    "reject_extra_top_level",
    "reject_drop_candidate",
    "reject_duplicate_candidate",
    "reject_unreviewed_primary_source",
    "reject_source_hash_drift",
    "reject_source_path_traversal",
    "reject_hash_as_theorem_evidence",
    "reject_target_domain_fabrication",
    "reject_block_cumulative_identification",
    "reject_direct_to_bad_formula_promotion",
    "reject_named_atom_fabrication",
    "reject_tw_log_as_natural",
    "reject_tt_exceptional_as_all_scale",
    "reject_phase_metric_as_named_atom",
    "reject_stopped_cell_reentry",
    "reject_fixed_h0_as_decay",
    "reject_candidate_eligibility_promotion",
    "reject_eligible_count_promotion",
    "reject_candidate_selection_when_empty",
    "reject_tpc194_progression",
    "reject_pointwise_route_stop",
    "reject_architecture_stop",
    "reject_global_nonexistence",
    "reject_endpoint_credit",
    "reject_strict_budget_payment",
    "reject_L2_promotion",
    "reject_twin_prime_claim",
    "reject_false_to_integer_zero",
    "reject_true_to_integer_one",
    "reject_duplicate_json_key",
    "reject_nonfinite_number",
]


class DuplicateKeyError(ValueError):
    """Raised when strict JSON parsing sees a repeated object key."""


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


def load_json(path: Path) -> dict[str, Any]:
    value = strict_loads(path.read_text(encoding="utf-8-sig"))
    if not isinstance(value, dict):
        raise ValueError(f"{path}: expected JSON object")
    return value


def canonical_text(value: Any) -> str:
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


def canonical_file_bytes(path: Path) -> bytes:
    text = path.read_text(encoding="utf-8-sig")
    return text.replace("\r\n", "\n").replace("\r", "\n").encode("utf-8")


def sha256_file(path: Path) -> str:
    return hashlib.sha256(canonical_file_bytes(path)).hexdigest()


def safe_repo_relative(path: Path) -> str:
    resolved_repo = REPO.resolve()
    resolved = path.resolve()
    if not resolved.is_relative_to(resolved_repo):
        raise ValueError(f"source escapes repository: {path}")
    return resolved.relative_to(resolved_repo).as_posix()


def source_lock(source_id: str, path: Path) -> dict[str, Any]:
    if not path.is_file():
        raise ValueError(f"missing source: {path}")
    return {
        "canonical_utf8_lf_sha256": sha256_file(path),
        "hash_semantics": "INTEGRITY_ONLY",
        "path": safe_repo_relative(path),
        "source_id": source_id,
    }


def build_source_locks() -> list[dict[str, Any]]:
    return [
        source_lock(source_id, path)
        for source_id, path in sorted(SOURCE_PATHS.items())
    ]


def require(condition: bool, message: str) -> None:
    if not condition:
        raise ValueError(message)


def assert_source_semantics() -> dict[str, dict[str, Any]]:
    p180 = load_json(SOURCE_PATHS["TPC180.census"])
    p181 = load_json(SOURCE_PATHS["TPC181.gate"])
    p183 = load_json(SOURCE_PATHS["TPC183.payload"])
    p184 = load_json(SOURCE_PATHS["TPC184.payload"])
    p187 = load_json(SOURCE_PATHS["TPC187.payload"])
    p189 = load_json(SOURCE_PATHS["TPC189.payload"])
    p190 = load_json(SOURCE_PATHS["TPC190.payload"])
    p192 = load_json(SOURCE_PATHS["TPC192.payload"])

    require(
        p192["verdict"] == "NOT_TESTABLE"
        and p192["selected_pointwise_first_missing"]
        == "LITERAL_FIXED_ATOM_ARITHMETIC_CANCELLATION",
        "TPC-192 frontier drift",
    )
    require(
        p189["required_quantifier_signature"] == REQUIRED_AXES
        and p189["fixed_atom_decay_obtained"] is False,
        "TPC-189 six-axis contract drift",
    )
    require(
        p180["candidate_registry"]["named_physical_atom_id"] is None
        and p180["candidate_registry"]["phase_value_mod_1"] is None
        and p180["candidate_registry"]["phase_value_source_locator"] is None
        and p180["candidate_registry"]["packet_schedule_source_locator"] is None
        and p180["source_census"]["production_packet_coordinate_rows"] == 0,
        "TPC-180 missing phase registry drift",
    )
    require(
        p181["route_decision"]["metric_uncontrolled_atomic"] == "STOP_SCOPED",
        "TPC-181 stopped cell drift",
    )
    require(
        p187["stop_scoped"]["cell"] == "SIZE_ONLY_LOCAL_OSCILLATION_METHOD",
        "TPC-187 stopped cell drift",
    )
    require(
        p190["stop_scoped"]["cell"] == "PARSEVAL_CHEBYSHEV_TO_PRESCRIBED_ATOM",
        "TPC-190 stopped cell drift",
    )
    require(
        "specializes separately at N=T" in p183["theorem"]
        and "cumulative" in p184["result"]
        and "q/N-normalized" in p189["result"],
        "TPC-183/184/189 interface wording drift",
    )

    text167 = SOURCE_PATHS["TPC167.main"].read_text(encoding="utf-8")
    text149 = SOURCE_PATHS["TPC149.main"].read_text(encoding="utf-8")
    text129 = SOURCE_PATHS["TPC129.main"].read_text(encoding="utf-8")
    text138 = SOURCE_PATHS["TPC138.main"].read_text(encoding="utf-8")
    text158 = SOURCE_PATHS["TPC158.main"].read_text(encoding="utf-8")
    text159 = SOURCE_PATHS["TPC159.readme"].read_text(encoding="utf-8")
    text168 = SOURCE_PATHS["TPC168.readme"].read_text(encoding="utf-8")
    text169 = SOURCE_PATHS["TPC169.main"].read_text(encoding="utf-8")

    require(
        "I_N=\\{z\\in\\mathbb Z:N<t(z)\\le2N\\}" in text167
        and "F_N(\\alpha)=\\frac qN" in text167,
        "TPC-167 literal block formula drift",
    )
    require(
        "N<ad+asz\\le2N" in text149,
        "TPC-149 terminal block formula drift",
    )
    require(
        "reciprocal cancellation has no formal implication" in text129,
        "TPC-129 Tauberian firewall drift",
    )
    require(
        "actual squarefree carrier is odd" in text138.lower(),
        "TPC-138 carrier firewall drift",
    )
    require(
        "L\\left|\\alpha-\\frac{k}{R}\\right|" in text158,
        "TPC-158 major-arc range drift",
    )
    require(
        "0 < t(z) <= T" in text159,
        "TPC-159 cumulative prefix formula drift",
    )
    require(
        "fixed_atom = false" in text168,
        "TPC-168 phase registry boundary drift",
    )
    require(
        "\\int_{\\T}G_T(\\alpha)^2" in text169,
        "TPC-169 phase maximal formula drift",
    )

    return {
        "TPC180": p180,
        "TPC181": p181,
        "TPC183": p183,
        "TPC184": p184,
        "TPC187": p187,
        "TPC189": p189,
        "TPC190": p190,
        "TPC192": p192,
    }


def primary_sources() -> list[dict[str, Any]]:
    return [
        {
            "id": "HR21.SHIFT_ONE_PARITY",
            "locator": "arXiv:2103.06853",
            "review_status": "REVIEWED_SCREENED_NON_DIRECT",
            "theorem_locator": "quantitative shift-one conclusions only",
            "title": "Expansion, Divisibility and Parity",
            "why_not_direct": (
                "TPC-138 proves that the even/determinant-one transfer is "
                "disjoint from the active odd determinant-two carrier."
            ),
            "year": 2021,
        },
        {
            "id": "MRT15.AVERAGED_CHOWLA",
            "locator": "doi:10.2140/ant.2015.9.2167",
            "review_status": "REVIEWED_SCREENED_NON_DIRECT",
            "theorem_locator": "averaged Chowla theorem and short Fourier sum",
            "title": "An Averaged Form of Chowla's Conjecture",
            "why_not_direct": (
                "The two-factor theorem averages shifts; the Fourier theorem "
                "has one multiplicative factor and averages interval origins."
            ),
            "year": 2015,
        },
        {
            "id": "PILATTE23.ALMOST_SCALE_SHIFT_ONE",
            "locator": "arXiv:2310.19357",
            "review_status": "REVIEWED_SCREENED_NON_DIRECT",
            "theorem_locator": "two-point logarithmic Chowla quantitative bound",
            "title": "Improved Bounds for the Two-Point Logarithmic Chowla Conjecture",
            "why_not_direct": (
                "The shift-one input does not transfer to the active odd "
                "determinant-two carrier and has no prescribed additive atom."
            ),
            "year": 2023,
        },
        {
            "id": "PILATTE26.FOURIER_UNIFORMITY",
            "locator": "arXiv:2604.26564v1",
            "review_status": "REVIEWED_SCREENED_NON_DIRECT",
            "theorem_locator": "Theorem 1.2 / abstract Fourier-uniformity estimate",
            "title": "Improved Bounds for the Fourier Uniformity Conjecture",
            "why_not_direct": (
                "It controls one Liouville factor uniformly in phase after "
                "averaging the interval origin; a second affine Möbius factor "
                "cannot be inserted by a theorem-backed operation."
            ),
            "year": 2026,
        },
        {
            "id": "TAO16.LOG_TWO_POINT",
            "locator": "doi:10.1017/fmp.2016.6",
            "review_status": "REVIEWED_SCREENED_NON_DIRECT",
            "theorem_locator": "Theorem 1.3",
            "title": (
                "The Logarithmically Averaged Chowla and Elliott "
                "Conjectures for Two-Point Correlations"
            ),
            "why_not_direct": (
                "Its fixed-affine logarithmic zero-phase theorem is subsumed "
                "for the fixed-atom screen by TW25."
            ),
            "year": 2016,
        },
        {
            "id": "TT26.QUANTITATIVE_CORRELATION",
            "locator": "arXiv:2512.01739v2",
            "review_status": "REVIEWED_DIRECT_CANDIDATE",
            "theorem_locator": "Theorem 3.1",
            "title": (
                "Quantitative Correlations and Some Problems on Prime "
                "Factors of Consecutive Integers"
            ),
            "why_not_direct": "",
            "year": 2026,
        },
        {
            "id": "TW25.LOG_TWISTED_AFFINE",
            "locator": "doi:10.1007/s00209-025-03770-2",
            "review_status": "REVIEWED_DIRECT_CANDIDATE",
            "theorem_locator": "Lemma 4.2(1)",
            "title": "On a Bohr Set Analogue of Chowla's Conjecture",
            "why_not_direct": "",
            "year": 2025,
        },
    ]


def candidate_inventory() -> list[dict[str, Any]]:
    return [
        {
            "axis_map": {
                "carrier_axis": "FIXED_DETERMINANT_TWO_AFFINE_PAIR",
                "decay_axis": "QUALITATIVE_LOG_AVERAGED_O1",
                "endpoint_axis": "LOG_WEIGHTED_CUMULATIVE_PREFIX",
                "phase_axis": "EVERY_FIXED_ADDITIVE_ATOM",
                "scale_axis": "ASYMPTOTIC_FIXED_DATA",
                "support_axis": "FORMAL_FIXED_AFFINE_SUPPORT",
            },
            "candidate_id": "TW25.LOG_TWISTED_AFFINE",
            "constant_range_normalization_loss": {
                "constants": (
                    "qualitative o(1), depending on the fixed affine data "
                    "and fixed atom; no effective rate is asserted"
                ),
                "losses": [
                    "reciprocal weight 1/n",
                    "normalization 1/log X",
                    "fixed affine data",
                    "no uniform pointwise power",
                ],
                "normalization": (
                    "(1/log X) sum_(n<=X) f1(a1*n+h1) "
                    "f2(a2*n+h2) e(gamma*n)/n"
                ),
                "range": (
                    "fixed positive nonparallel affine forms; every fixed "
                    "gamma in R; X tends to infinity"
                ),
            },
            "direct_specialization": {
                "affine_form_1": "(a1,h1)=(s,d+s*z0)",
                "affine_form_2": "(a2,h2)=(a,u+a*z0)",
                "determinant": (
                    "a1*h2-a2*h1=s*(u+a*z0)-a*(d+s*z0)"
                    "=s*u-a*d=2"
                ),
                "functions": "f1=f2=mu",
                "phase": "gamma=-alpha_star",
                "translation_effect": (
                    "choose fixed z0 so both intercepts are positive; "
                    "determinant unchanged; phase gains one unit scalar"
                ),
            },
            "eligibility_checks": {
                "all_constants_ranges_normalizations_losses_exposed": True,
                "carrier_axis_match": False,
                "decay_axis_match": False,
                "direct_literal_two_mobius": True,
                "endpoint_axis_match": False,
                "formula_complete_target_available": False,
                "normalization_q_over_endpoint_natural": False,
                "not_stopped_cell_repackage": True,
                "phase_axis_match": True,
                "prescribed_atom_source_locked_or_uniform": True,
                "scale_axis_match": False,
                "support_axis_match": False,
                "theorem_backed": True,
            },
            "eligible": False,
            "first_failure": "NORMALIZATION_NOT_NATURAL_Q_OVER_ENDPOINT",
            "source_ids": ["TW25.LOG_TWISTED_AFFINE", "TPC129.main"],
            "theorem_statement": (
                "For fixed nonparallel affine forms and f1 "
                "nonpretentious, the logarithmic average of "
                "f1(a1*n+h1)f2(a2*n+h2)e(gamma*n) tends to zero for "
                "every fixed gamma."
            ),
        },
        {
            "axis_map": {
                "carrier_axis": "ACTUAL_DETERMINANT_TWO_PERIODIC_CORE",
                "decay_axis": "LOG_POWER_ONLY",
                "endpoint_axis": "TERMINAL_DYADIC_BLOCK",
                "phase_axis": "RATIONAL_PERIODIC_ATOM_IF_SOURCE_BACKED",
                "scale_axis": "ALL_BUT_LOG_DENSITY_EXCEPTIONAL_SET",
                "support_axis": "ACTUAL_CORE_NOT_ACTUAL_ACTIVE_SUPPORT",
            },
            "candidate_id": "TT26.RATIONAL_PERIODIC_ATOM",
            "constant_range_normalization_loss": {
                "constants": (
                    "absolute eta_0,kappa_0>0 and an absolute implicit "
                    "constant inherited through TPC-149"
                ),
                "losses": [
                    "q*R <= (log X)^eta_0",
                    "N outside E_X_star",
                    "single terminal block",
                    "saving (log X)^(-kappa_0)",
                ],
                "normalization": (
                    "(q/N) sum_(N<t(z)<=2N) c_z rho(z)"
                ),
                "range": (
                    "sqrt(X)<=N<=X outside E_X_star; rational atom "
                    "alpha_star=r/R; bounded period-R rho"
                ),
            },
            "direct_specialization": {
                "affine_form_1": "d+s*z",
                "affine_form_2": "u+a*z",
                "determinant": "s*u-a*d=2",
                "functions": "literal product mu(d+s*z)*mu(u+a*z)",
                "phase": "rho(z)=e(-r*z/R) when alpha_star=r/R",
                "translation_effect": "not required",
            },
            "eligibility_checks": {
                "all_constants_ranges_normalizations_losses_exposed": True,
                "carrier_axis_match": True,
                "decay_axis_match": False,
                "direct_literal_two_mobius": True,
                "endpoint_axis_match": False,
                "formula_complete_target_available": False,
                "normalization_q_over_endpoint_natural": True,
                "not_stopped_cell_repackage": True,
                "phase_axis_match": False,
                "prescribed_atom_source_locked_or_uniform": False,
                "scale_axis_match": False,
                "support_axis_match": False,
                "theorem_backed": True,
            },
            "eligible": False,
            "first_failure": (
                "NAMED_ATOM_VALUE_AND_RATIONAL_DENOMINATOR_SOURCE_ABSENT"
            ),
            "source_ids": [
                "TT26.QUANTITATIVE_CORRELATION",
                "TPC149.main",
                "TPC158.main",
            ],
            "theorem_statement": (
                "Outside one logarithmically sparse scale set, the "
                "q/N-normalized literal determinant-two core has a "
                "log-power bound against every bounded small-period "
                "multiplier."
            ),
        },
    ]


def build_payload_base() -> dict[str, Any]:
    sources = assert_source_semantics()
    p180 = sources["TPC180"]
    candidates = candidate_inventory()
    primary = primary_sources()
    eligible_ids = [
        item["candidate_id"] for item in candidates if item["eligible"]
    ]

    return {
        "candidate_inventory": candidates,
        "checks": {
            "all_primary_sources_reviewed": True,
            "all_repository_sources_locked": True,
            "candidate_eligibility_recomputed": True,
            "candidate_statements_expose_native_losses": True,
            "declared_corpus_exhaustion_not_global_nonexistence": True,
            "direct_block_and_bad_prefix_not_identified": True,
            "direct_to_bad_not_formula_promoted": True,
            "eligible_count_zero": True,
            "fixed_h0_data_not_decay": True,
            "named_atom_absence_preserved": True,
            "no_tpc194_selected": True,
            "pointwise_parents_remain_open": True,
            "schema_exact_and_closed": True,
            "source_hashes_are_integrity_only": True,
            "stopped_method_cells_not_repackaged": True,
            "strict_budget_unpaid": True,
            "target_contract_incompleteness_preserved": True,
            "tw_log_average_not_natural_prefix": True,
            "tt_exceptional_log_power_not_all_scale_power": True,
        },
        "claim_boundary": {
            "architecture_stopped": False,
            "block_equals_cumulative_prefix": False,
            "declared_corpus_is_global_mathematical_nonexistence": False,
            "direct_implies_bad_formula_certified": False,
            "fixed_h0_data_is_decay": False,
            "fixed_atom_decay_obtained": False,
            "hash_integrity_is_theorem_evidence": False,
            "named_physical_atom_identified": False,
            "pointwise_parents_stopped": False,
            "prime_pair_lower_bound": False,
            "program_positive_L2": False,
            "strict_one_over_400": False,
            "tpc194_authorized": False,
            "twin_prime_theorem": False,
        },
        "classification": "SOURCE_LOCKED_CANDIDATE_GATE_L1",
        "corpus_partition": {
            "direct_candidate_count": len(candidates),
            "eligible_candidate_count": len(eligible_ids),
            "eligible_candidate_ids": eligible_ids,
            "not_mapped_count": 0,
            "not_reviewed_count": 0,
            "primary_source_record_count": len(primary),
            "reviewed_primary_source_count": len(primary),
            "screened_non_direct_count": len(primary) - len(candidates),
            "selected_candidate_id": None,
            "smallest_genuine_sublemma": None,
        },
        "declared_mechanism_corpus": {
            "as_of_date": "2026-07-28",
            "closed_world_semantics": (
                "EXHAUSTIVE_ONLY_WITHIN_THE_EXPLICIT_SEVEN_PRIMARY_SOURCE_"
                "RECORDS_AND_LOCKED_REPOSITORY_INTERFACES"
            ),
            "direct_candidate_ids": [
                item["candidate_id"] for item in candidates
            ],
            "primary_source_records": primary,
            "scope_id": "TPC193_DECLARED_PRIMARY_THEOREM_CORPUS_V1",
            "screened_non_direct_source_ids": [
                item["id"]
                for item in primary
                if item["review_status"]
                == "REVIEWED_SCREENED_NON_DIRECT"
            ],
            "search_surface": [
                "repository direct arithmetic lineage TPC-108,129,138-140,149,157-170,181,187,190",
                "fixed-atom affine multiplicative correlation theorems",
                "additive-twist and Fourier-uniformity theorems through 2026-07-28",
            ],
        },
        "endpoint_ledger": {
            "named_atom_sigma_credit": {"denominator": 1, "numerator": 0},
            "required_strict_budget": {"denominator": 400, "numerator": 1},
            "state": "UNPAID",
        },
        "level_ledger": {
            "L0": (
                "literal formula comparison, source census, candidate "
                "registry, strict schemas and executed mutation diagnostics"
            ),
            "L1": (
                "scoped declared-corpus exhaustion and formula-interface "
                "fail-closed route decision"
            ),
            "L2": "NONE",
            "fixed_h0_gate": "SOURCE_BACKED_DATA_FACT_ONLY",
            "new_program_positive_L2": False,
        },
        "mutation_regressions": {
            name: True for name in MUTATION_NAMES
        },
        "paper": 193,
        "qualification_contract": {
            "eligibility_is_conjunction_of": ELIGIBILITY_KEYS,
            "excluded_inputs": [
                "PHASE_L2",
                "LEBESGUE_AE_PHASE",
                "SIZE_ONLY_BOUND",
                "REPACKAGED_STOPPED_METHOD_CELL",
            ],
            "required_quantifier_signature": copy.deepcopy(REQUIRED_AXES),
            "statement_must_expose": [
                "theorem locator",
                "literal coefficient",
                "constant dependencies",
                "parameter ranges",
                "normalization",
                "all losses",
            ],
        },
        "route_decision": {
            "architecture_stopped": False,
            "arithmetic_first_missing": (
                "LITERAL_FIXED_ATOM_ARITHMETIC_CANCELLATION"
            ),
            "bad_endpoint_parent": "OPEN_PARENT_READY",
            "batch_stop": "USER_CONFIRMATION_REQUIRED",
            "direct_implies_bad_formula_status": "NOT_FORMULA_CERTIFIED",
            "direct_parent": "OPEN_PARENT_READY",
            "gate_first_missing": (
                "DIRECT_TARGET_SUMMATION_DOMAIN_AND_PREFIX_INDEX"
            ),
            "global_mathematical_nonexistence": False,
            "next_paper": None,
            "pointwise_parents_stopped": False,
            "reopen_triggers": [
                (
                    "formula-complete direct target with source-backed atom, "
                    "prefix domain, ranges, constant, exponent and loss ledger"
                ),
                (
                    "new theorem-backed natural q/N fixed-atom power estimate "
                    "preserving all six axes"
                ),
            ],
            "stop_scope": (
                "TPC193_DECLARED_CANDIDATE_MECHANISM_CORPUS_V1"
            ),
            "verdict": "NO_ELIGIBLE_MECHANISM_IN_DECLARED_CORPUS",
        },
        "schema": "tpc-193-literal-fixed-atom-candidate-mechanism-gate-v1",
        "snapshot": {
            "date": "2026-07-28",
            "hash_mode": HASH_MODE,
            "hash_semantics": "INTEGRITY_ONLY",
            "source_of_truth": "REPOSITORY_ARTIFACTS_NOT_CHAT_MEMORY",
        },
        "source_locks": build_source_locks(),
        "stopped_method_cells": [
            {
                "cell": "phase_metric_uncontrolled_atomic",
                "reentry_allowed": False,
                "source_paper": 181,
                "stop_scope": "UNCONTROLLED_ATOMIC_PROMOTION_ONLY",
            },
            {
                "cell": "SIZE_ONLY_LOCAL_OSCILLATION_METHOD",
                "reentry_allowed": False,
                "source_paper": 187,
                "stop_scope": "SIZE_ONLY_LOCAL_OSCILLATION_METHOD",
            },
            {
                "cell": "PARSEVAL_CHEBYSHEV_TO_PRESCRIBED_ATOM",
                "reentry_allowed": False,
                "source_paper": 190,
                "stop_scope": "PARSEVAL_CHEBYSHEV_TO_PRESCRIBED_ATOM",
            },
        ],
        "target_contract": {
            "direct_target": {
                "admissible_parameter_ranges": None,
                "named_atom_id": p180["candidate_registry"][
                    "named_physical_atom_id"
                ],
                "packet_schedule_source_locator": p180["candidate_registry"][
                    "packet_schedule_source_locator"
                ],
                "phase_value_mod_1": p180["candidate_registry"][
                    "phase_value_mod_1"
                ],
                "phase_value_source_locator": p180["candidate_registry"][
                    "phase_value_source_locator"
                ],
                "positive_exponent_sigma": None,
                "prefix_index_set": None,
                "required_bound_skeleton": (
                    "|F_N(alpha_star)| <= C * X^(-sigma)"
                ),
                "summation_domain": None,
                "uniform_constant_C": None,
                "total_physical_loss": None,
            },
            "fixed_h0": {
                "semantics": "SOURCE_BACKED_DATA_FACT_ONLY",
                "value": 2,
            },
            "formula_audit": {
                "block_and_cumulative_are_identical": False,
                "direct_to_bad_claimed_by_tpc183": True,
                "direct_to_bad_formula_certified": False,
                "interpretation_if_block_retained": (
                    "N=T leaves T<t(z)<=2T and does not yield 0<t(z)<=T"
                ),
                "interpretation_if_cumulative_intended": (
                    "the replacement direct formula and prefix range are "
                    "not written in TPC-183 or TPC-189"
                ),
                "status": "NOT_TESTABLE",
            },
            "literal_core": {
                "coefficient": "c_z=mu(d+s*z)*mu(u+a*z)",
                "coprimality": "gcd(a,s)=1",
                "determinant": "s*u-a*d=2",
                "fiber_coordinate": "t(z)=a*d+q*z",
                "fixed_shift_identity": (
                    "t(z)=a*(d+s*z), t(z)+2=s*(u+a*z)"
                ),
                "parity": "a*s is odd",
                "q": "q=a*s",
                "ranges": "a,s>=1; d,u in Z; z in Z",
            },
            "ordered_missing": [
                "direct_target_summation_domain",
                "direct_target_prefix_index_set",
                "named_physical_atom_id",
                "phase_value_mod_1",
                "phase_value_source_locator",
                "packet_schedule_source_locator_and_rows",
                "admissible_X_N_q_ranges",
                "uniform_constant_C_and_positive_sigma",
                "complete_physical_loss_ledger",
            ],
            "source_formula_variants": [
                {
                    "domain": "N<t(z)<=2N",
                    "formula_id": "TPC167_BLOCK_DIRECT_TWIST",
                    "normalization": "q/N",
                    "role": "EXPLICIT_DIRECT_TRANSFORM",
                    "source_id": "TPC167.main",
                },
                {
                    "contract_role_source_id": "TPC184.payload",
                    "domain": "0<t(z)<=T",
                    "domain_normalization_source_id": "TPC159.readme",
                    "formula_id": "AUDIT_COMBINED_CUMULATIVE_FIXED_ATOM_TARGET",
                    "normalization": "q/T",
                    "phase_convention_source_id": "TPC167.main",
                    "role": "AUDITED_BAD_ENDPOINT_TARGET",
                },
            ],
            "status": "NOT_TESTABLE_FORMULA_INCOMPLETE",
        },
        "title": "A Literal Fixed-Atom Candidate-Mechanism Gate",
    }


def exact_schema(value: Any) -> dict[str, Any]:
    if isinstance(value, dict):
        return {
            "additionalProperties": False,
            "properties": {
                key: exact_schema(item) for key, item in sorted(value.items())
            },
            "required": sorted(value),
            "type": "object",
        }
    if isinstance(value, list):
        return {
            "items": False,
            "maxItems": len(value),
            "minItems": len(value),
            "prefixItems": [exact_schema(item) for item in value],
            "type": "array",
        }
    return {"const": value}


def schema_document(value: Any, schema_id: str, title: str) -> dict[str, Any]:
    return {
        "$id": schema_id,
        "$schema": SCHEMA_URI,
        "title": title,
        **exact_schema(value),
    }


def validate_exact_schema(
    instance: Any, schema: dict[str, Any], location: str = "$"
) -> None:
    if "const" in schema:
        expected = schema["const"]
        if type(instance) is not type(expected) or instance != expected:
            raise ValueError(f"{location}: const mismatch")
    expected_type = schema.get("type")
    if expected_type == "object" and not isinstance(instance, dict):
        raise ValueError(f"{location}: expected object")
    if expected_type == "array" and not isinstance(instance, list):
        raise ValueError(f"{location}: expected array")
    if isinstance(instance, dict):
        required = schema.get("required", [])
        if set(instance) != set(required):
            raise ValueError(f"{location}: object key set mismatch")
        properties = schema.get("properties", {})
        for key, item in instance.items():
            if key not in properties:
                raise ValueError(f"{location}: unexpected key {key}")
            validate_exact_schema(item, properties[key], f"{location}.{key}")
        if schema.get("additionalProperties") is not False:
            raise ValueError(f"{location}: schema object not closed")
    if isinstance(instance, list):
        if len(instance) != schema.get("minItems"):
            raise ValueError(f"{location}: array length mismatch")
        if len(instance) != schema.get("maxItems"):
            raise ValueError(f"{location}: array maximum mismatch")
        prefix = schema.get("prefixItems", [])
        if len(prefix) != len(instance) or schema.get("items") is not False:
            raise ValueError(f"{location}: array schema not exact")
        for index, item in enumerate(instance):
            validate_exact_schema(item, prefix[index], f"{location}[{index}]")


def candidate_is_eligible(candidate: dict[str, Any]) -> bool:
    checks = candidate["eligibility_checks"]
    if set(checks) != set(ELIGIBILITY_KEYS):
        raise ValueError("candidate eligibility key drift")
    if any(not isinstance(checks[key], bool) for key in ELIGIBILITY_KEYS):
        raise ValueError("candidate eligibility values must be boolean")
    return all(checks[key] for key in ELIGIBILITY_KEYS)


def validate_source_locks(locks: list[dict[str, Any]]) -> None:
    expected = build_source_locks()
    if locks != expected:
        raise ValueError("source lock set or hash drift")
    source_ids = [item["source_id"] for item in locks]
    if len(source_ids) != len(set(source_ids)):
        raise ValueError("duplicate source lock id")
    for item in locks:
        path = Path(item["path"])
        if path.is_absolute() or ".." in path.parts:
            raise ValueError("unsafe source lock path")
        if item["hash_semantics"] != "INTEGRITY_ONLY":
            raise ValueError("source hash promoted beyond integrity")
        if len(item["canonical_utf8_lf_sha256"]) != 64:
            raise ValueError("invalid source hash length")


def validate_semantics(
    obj: dict[str, Any], *, require_mutation_registry: bool = True
) -> None:
    expected_top = {
        "candidate_inventory",
        "checks",
        "claim_boundary",
        "classification",
        "corpus_partition",
        "declared_mechanism_corpus",
        "endpoint_ledger",
        "level_ledger",
        "mutation_regressions",
        "paper",
        "qualification_contract",
        "route_decision",
        "schema",
        "snapshot",
        "source_locks",
        "stopped_method_cells",
        "target_contract",
        "title",
    }
    require(set(obj) == expected_top, "top-level key drift")
    require(obj["paper"] == 193, "paper number drift")
    require(
        obj["schema"]
        == "tpc-193-literal-fixed-atom-candidate-mechanism-gate-v1",
        "schema id drift",
    )
    require(
        obj["classification"] == "SOURCE_LOCKED_CANDIDATE_GATE_L1",
        "classification drift",
    )
    require(
        obj["qualification_contract"]["required_quantifier_signature"]
        == REQUIRED_AXES,
        "six-axis signature drift",
    )
    require(
        obj["qualification_contract"]["eligibility_is_conjunction_of"]
        == ELIGIBILITY_KEYS,
        "eligibility contract drift",
    )
    validate_source_locks(obj["source_locks"])

    primary = obj["declared_mechanism_corpus"]["primary_source_records"]
    primary_ids = [item["id"] for item in primary]
    require(len(primary) == 7, "primary source count drift")
    require(len(primary_ids) == len(set(primary_ids)), "duplicate primary id")
    require(
        all(item["review_status"].startswith("REVIEWED_") for item in primary),
        "unreviewed primary source",
    )
    require(
        obj["declared_mechanism_corpus"]["closed_world_semantics"]
        == (
            "EXHAUSTIVE_ONLY_WITHIN_THE_EXPLICIT_SEVEN_PRIMARY_SOURCE_"
            "RECORDS_AND_LOCKED_REPOSITORY_INTERFACES"
        ),
        "corpus scope widened",
    )

    candidates = obj["candidate_inventory"]
    candidate_ids = [item["candidate_id"] for item in candidates]
    require(
        candidate_ids
        == ["TW25.LOG_TWISTED_AFFINE", "TT26.RATIONAL_PERIODIC_ATOM"],
        "candidate identity/order drift",
    )
    require(
        len(candidate_ids) == len(set(candidate_ids)),
        "duplicate candidate id",
    )
    recomputed_eligible = []
    for candidate in candidates:
        eligible = candidate_is_eligible(candidate)
        require(
            candidate["eligible"] is eligible,
            f"candidate eligibility not recomputed: {candidate['candidate_id']}",
        )
        if eligible:
            recomputed_eligible.append(candidate["candidate_id"])

    partition = obj["corpus_partition"]
    require(partition["primary_source_record_count"] == 7, "primary count drift")
    require(partition["reviewed_primary_source_count"] == 7, "reviewed count drift")
    require(partition["not_reviewed_count"] == 0, "unreviewed count positive")
    require(partition["not_mapped_count"] == 0, "unmapped count positive")
    require(partition["direct_candidate_count"] == 2, "direct count drift")
    require(partition["eligible_candidate_ids"] == recomputed_eligible, "eligible ids drift")
    require(partition["eligible_candidate_count"] == 0, "eligible count drift")
    require(partition["selected_candidate_id"] is None, "candidate selected from empty set")
    require(partition["smallest_genuine_sublemma"] is None, "sublemma fabricated")

    target = obj["target_contract"]
    require(
        target["status"] == "NOT_TESTABLE_FORMULA_INCOMPLETE",
        "target status promoted",
    )
    require(
        target["formula_audit"]["block_and_cumulative_are_identical"] is False,
        "block and cumulative domains identified",
    )
    require(
        target["formula_audit"]["direct_to_bad_formula_certified"] is False,
        "direct-to-bad formula promoted",
    )
    direct = target["direct_target"]
    for key in [
        "admissible_parameter_ranges",
        "named_atom_id",
        "packet_schedule_source_locator",
        "phase_value_mod_1",
        "phase_value_source_locator",
        "positive_exponent_sigma",
        "prefix_index_set",
        "summation_domain",
        "uniform_constant_C",
        "total_physical_loss",
    ]:
        require(direct[key] is None, f"missing direct field fabricated: {key}")
    require(
        target["fixed_h0"]
        == {"semantics": "SOURCE_BACKED_DATA_FACT_ONLY", "value": 2},
        "fixed h0 promoted",
    )

    stopped = obj["stopped_method_cells"]
    require(
        [item["cell"] for item in stopped]
        == [
            "phase_metric_uncontrolled_atomic",
            "SIZE_ONLY_LOCAL_OSCILLATION_METHOD",
            "PARSEVAL_CHEBYSHEV_TO_PRESCRIBED_ATOM",
        ],
        "stopped method registry drift",
    )
    require(
        all(item["reentry_allowed"] is False for item in stopped),
        "stopped method reentered",
    )

    decision = obj["route_decision"]
    require(
        decision["verdict"]
        == "NO_ELIGIBLE_MECHANISM_IN_DECLARED_CORPUS",
        "route verdict drift",
    )
    require(
        decision["gate_first_missing"]
        == "DIRECT_TARGET_SUMMATION_DOMAIN_AND_PREFIX_INDEX",
        "gate first missing drift",
    )
    require(
        decision["arithmetic_first_missing"]
        == "LITERAL_FIXED_ATOM_ARITHMETIC_CANCELLATION",
        "arithmetic first missing drift",
    )
    require(
        decision["next_paper"] is None
        and decision["batch_stop"] == "USER_CONFIRMATION_REQUIRED",
        "TPC-194 progression fabricated",
    )
    require(
        decision["direct_parent"] == "OPEN_PARENT_READY"
        and decision["bad_endpoint_parent"] == "OPEN_PARENT_READY"
        and decision["pointwise_parents_stopped"] is False
        and decision["architecture_stopped"] is False
        and decision["global_mathematical_nonexistence"] is False,
        "scoped stop widened",
    )

    ledger = obj["endpoint_ledger"]
    require(
        ledger
        == {
            "named_atom_sigma_credit": {"denominator": 1, "numerator": 0},
            "required_strict_budget": {"denominator": 400, "numerator": 1},
            "state": "UNPAID",
        },
        "endpoint ledger promoted",
    )
    require(
        obj["level_ledger"]["L2"] == "NONE"
        and obj["level_ledger"]["new_program_positive_L2"] is False
        and obj["level_ledger"]["fixed_h0_gate"]
        == "SOURCE_BACKED_DATA_FACT_ONLY",
        "level ledger promoted",
    )
    require(
        all(value is False for value in obj["claim_boundary"].values()),
        "positive claim boundary promoted",
    )
    require(
        all(value is True for value in obj["checks"].values()),
        "check map contains failure",
    )
    if require_mutation_registry:
        require(
            list(obj["mutation_regressions"]) == sorted(MUTATION_NAMES),
            "mutation registry key drift",
        )
        require(
            all(
                value is True
                for value in obj["mutation_regressions"].values()
            ),
            "mutation regression self-check failed",
        )


def set_path(obj: dict[str, Any], path: list[Any], value: Any) -> None:
    cursor: Any = obj
    for part in path[:-1]:
        cursor = cursor[part]
    cursor[path[-1]] = value


def append_duplicate_candidate(obj: dict[str, Any]) -> None:
    obj["candidate_inventory"].append(
        copy.deepcopy(obj["candidate_inventory"][0])
    )


def append_phase_metric_candidate(obj: dict[str, Any]) -> None:
    item = copy.deepcopy(obj["candidate_inventory"][0])
    item["candidate_id"] = "REPACKAGED.PHASE_METRIC_TO_ATOM"
    item["source_ids"] = ["TPC181.gate"]
    obj["candidate_inventory"].append(item)


def mutation_rejected(
    base: dict[str, Any],
    schema: dict[str, Any],
    mutator: Callable[[dict[str, Any]], None],
) -> bool:
    changed = copy.deepcopy(base)
    mutator(changed)
    try:
        validate_semantics(changed, require_mutation_registry=False)
        validate_exact_schema(changed, schema)
    except (ValueError, KeyError, TypeError):
        return True
    return False


def build_mutation_regressions(
    base: dict[str, Any], schema: dict[str, Any]
) -> dict[str, bool]:
    mutations: dict[str, Callable[[dict[str, Any]], None]] = {
        "reject_extra_top_level": lambda x: x.__setitem__("extra", True),
        "reject_drop_candidate": lambda x: x["candidate_inventory"].pop(),
        "reject_duplicate_candidate": append_duplicate_candidate,
        "reject_unreviewed_primary_source": lambda x: set_path(
            x,
            [
                "declared_mechanism_corpus",
                "primary_source_records",
                0,
                "review_status",
            ],
            "NOT_REVIEWED",
        ),
        "reject_source_hash_drift": lambda x: set_path(
            x,
            ["source_locks", 0, "canonical_utf8_lf_sha256"],
            "0" * 64,
        ),
        "reject_source_path_traversal": lambda x: set_path(
            x, ["source_locks", 0, "path"], "../escape.json"
        ),
        "reject_hash_as_theorem_evidence": lambda x: set_path(
            x,
            ["source_locks", 0, "hash_semantics"],
            "THEOREM_EVIDENCE",
        ),
        "reject_target_domain_fabrication": lambda x: set_path(
            x,
            ["target_contract", "direct_target", "summation_domain"],
            "0<t(z)<=N",
        ),
        "reject_block_cumulative_identification": lambda x: set_path(
            x,
            [
                "target_contract",
                "formula_audit",
                "block_and_cumulative_are_identical",
            ],
            True,
        ),
        "reject_direct_to_bad_formula_promotion": lambda x: set_path(
            x,
            [
                "target_contract",
                "formula_audit",
                "direct_to_bad_formula_certified",
            ],
            True,
        ),
        "reject_named_atom_fabrication": lambda x: set_path(
            x,
            ["target_contract", "direct_target", "named_atom_id"],
            "alpha_star",
        ),
        "reject_tw_log_as_natural": lambda x: set_path(
            x,
            [
                "candidate_inventory",
                0,
                "eligibility_checks",
                "normalization_q_over_endpoint_natural",
            ],
            True,
        ),
        "reject_tt_exceptional_as_all_scale": lambda x: set_path(
            x,
            [
                "candidate_inventory",
                1,
                "eligibility_checks",
                "scale_axis_match",
            ],
            True,
        ),
        "reject_phase_metric_as_named_atom": append_phase_metric_candidate,
        "reject_stopped_cell_reentry": lambda x: set_path(
            x,
            ["stopped_method_cells", 0, "reentry_allowed"],
            True,
        ),
        "reject_fixed_h0_as_decay": lambda x: set_path(
            x,
            ["target_contract", "fixed_h0", "semantics"],
            "FIXED_ATOM_DECAY",
        ),
        "reject_candidate_eligibility_promotion": lambda x: set_path(
            x, ["candidate_inventory", 0, "eligible"], True
        ),
        "reject_eligible_count_promotion": lambda x: set_path(
            x, ["corpus_partition", "eligible_candidate_count"], 1
        ),
        "reject_candidate_selection_when_empty": lambda x: set_path(
            x,
            ["corpus_partition", "selected_candidate_id"],
            "TW25.LOG_TWISTED_AFFINE",
        ),
        "reject_tpc194_progression": lambda x: set_path(
            x, ["route_decision", "next_paper"], 194
        ),
        "reject_pointwise_route_stop": lambda x: set_path(
            x, ["route_decision", "pointwise_parents_stopped"], True
        ),
        "reject_architecture_stop": lambda x: set_path(
            x, ["route_decision", "architecture_stopped"], True
        ),
        "reject_global_nonexistence": lambda x: set_path(
            x,
            ["route_decision", "global_mathematical_nonexistence"],
            True,
        ),
        "reject_endpoint_credit": lambda x: set_path(
            x,
            [
                "endpoint_ledger",
                "named_atom_sigma_credit",
                "numerator",
            ],
            1,
        ),
        "reject_strict_budget_payment": lambda x: set_path(
            x, ["endpoint_ledger", "state"], "PAID"
        ),
        "reject_L2_promotion": lambda x: set_path(
            x, ["level_ledger", "L2"], "POSITIVE"
        ),
        "reject_twin_prime_claim": lambda x: set_path(
            x, ["claim_boundary", "twin_prime_theorem"], True
        ),
        "reject_false_to_integer_zero": lambda x: set_path(
            x, ["claim_boundary", "twin_prime_theorem"], 0
        ),
        "reject_true_to_integer_one": lambda x: set_path(
            x, ["checks", "all_primary_sources_reviewed"], 1
        ),
    }
    result = {
        name: mutation_rejected(base, schema, mutator)
        for name, mutator in mutations.items()
    }
    try:
        strict_loads('{"a":1,"a":2}')
        result["reject_duplicate_json_key"] = False
    except DuplicateKeyError:
        result["reject_duplicate_json_key"] = True
    try:
        strict_loads('{"x":NaN}')
        result["reject_nonfinite_number"] = False
    except ValueError:
        result["reject_nonfinite_number"] = True
    if set(result) != set(MUTATION_NAMES):
        raise ValueError("mutation implementation set drift")
    if not all(value is True for value in result.values()):
        failed = sorted(name for name, passed in result.items() if not passed)
        raise ValueError(f"mutation regressions failed: {failed}")
    return dict(sorted(result.items()))


def build_payload() -> dict[str, Any]:
    payload = build_payload_base()
    provisional_schema = schema_document(
        payload,
        "tpc193-literal-fixed-atom-candidate-mechanism-gate-v1.schema.json",
        "TPC-193 literal fixed-atom candidate-mechanism gate",
    )
    payload["mutation_regressions"] = build_mutation_regressions(
        payload, provisional_schema
    )
    validate_semantics(payload)
    return payload


def schema_stats(schema: dict[str, Any]) -> dict[str, int]:
    counts = {
        "array_layers": 0,
        "closed_object_layers": 0,
        "const_nodes": 0,
        "prefix_item_layers": 0,
    }

    def walk(node: Any) -> None:
        if isinstance(node, dict):
            if "const" in node:
                counts["const_nodes"] += 1
            if node.get("type") == "object":
                if node.get("additionalProperties") is not False:
                    raise ValueError("schema object layer is not closed")
                counts["closed_object_layers"] += 1
            if node.get("type") == "array":
                counts["array_layers"] += 1
                if "prefixItems" in node:
                    counts["prefix_item_layers"] += 1
            for value in node.values():
                walk(value)
        elif isinstance(node, list):
            for value in node:
                walk(value)

    walk(schema)
    return counts


def build_audit(
    payload: dict[str, Any], payload_schema: dict[str, Any]
) -> dict[str, Any]:
    payload_text = canonical_text(payload)
    return {
        "audit_execution": {
            "canonical_byte_comparison": True,
            "duplicate_json_keys_rejected": True,
            "mutation_mode": (
                "EXECUTED_DEEP_COPY_AGAINST_SEMANTIC_AND_EXACT_SCHEMA_VALIDATORS"
            ),
            "nonfinite_json_numbers_rejected": True,
            "source_hashes_recomputed": True,
        },
        "claim_boundary": copy.deepcopy(payload["claim_boundary"]),
        "direct_candidate_count": payload["corpus_partition"][
            "direct_candidate_count"
        ],
        "eligible_candidate_count": payload["corpus_partition"][
            "eligible_candidate_count"
        ],
        "gate_first_missing": payload["route_decision"]["gate_first_missing"],
        "manifest_payload_sha256": hashlib.sha256(
            payload_text.encode("utf-8")
        ).hexdigest(),
        "manifest_schema": payload["schema"],
        "mutation_regressions": copy.deepcopy(
            payload["mutation_regressions"]
        ),
        "paper": 193,
        "primary_source_record_count": payload["corpus_partition"][
            "primary_source_record_count"
        ],
        "repository_source_lock_count": len(payload["source_locks"]),
        "route_action": payload["route_decision"]["batch_stop"],
        "schema": (
            "tpc-193-literal-fixed-atom-candidate-mechanism-gate-audit-v1"
        ),
        "schema_hardening": schema_stats(payload_schema),
        "status": "PASS",
        "target_contract_status": payload["target_contract"]["status"],
        "verdict": payload["route_decision"]["verdict"],
    }


def validate_audit(
    audit: dict[str, Any],
    payload: dict[str, Any],
    payload_schema: dict[str, Any],
) -> None:
    expected = build_audit(payload, payload_schema)
    require(audit == expected, "audit semantic or hash drift")
    require(
        all(
            value is True for value in audit["mutation_regressions"].values()
        ),
        "audit mutation regression failure",
    )
    require(
        all(value is False for value in audit["claim_boundary"].values()),
        "audit claim boundary promotion",
    )


def build_all() -> tuple[
    dict[str, Any],
    dict[str, Any],
    dict[str, Any],
    dict[str, Any],
]:
    payload = build_payload()
    payload_schema = schema_document(
        payload,
        "tpc193-literal-fixed-atom-candidate-mechanism-gate-v1.schema.json",
        "TPC-193 literal fixed-atom candidate-mechanism gate",
    )
    audit = build_audit(payload, payload_schema)
    audit_schema = schema_document(
        audit,
        (
            "tpc193-literal-fixed-atom-candidate-mechanism-"
            "gate-audit-v1.schema.json"
        ),
        "TPC-193 literal fixed-atom candidate-mechanism gate audit",
    )
    validate_exact_schema(payload, payload_schema)
    validate_exact_schema(audit, audit_schema)
    validate_audit(audit, payload, payload_schema)
    return payload, audit, payload_schema, audit_schema


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()

    payload, audit, payload_schema, audit_schema = build_all()
    outputs = {
        PAYLOAD_PATH: canonical_text(payload),
        AUDIT_PATH: canonical_text(audit),
        PAYLOAD_SCHEMA_PATH: canonical_text(payload_schema),
        AUDIT_SCHEMA_PATH: canonical_text(audit_schema),
    }

    if args.check:
        for path, expected_text in outputs.items():
            if not path.is_file():
                raise SystemExit(f"missing generated output: {path}")
            actual_text = path.read_text(encoding="utf-8")
            strict_loads(actual_text)
            if actual_text != expected_text:
                raise SystemExit(
                    f"generated output is stale or noncanonical: {path}"
                )
        actual_payload = load_json(PAYLOAD_PATH)
        actual_audit = load_json(AUDIT_PATH)
        actual_payload_schema = load_json(PAYLOAD_SCHEMA_PATH)
        actual_audit_schema = load_json(AUDIT_SCHEMA_PATH)
        validate_semantics(actual_payload)
        validate_exact_schema(actual_payload, actual_payload_schema)
        validate_exact_schema(actual_audit, actual_audit_schema)
        validate_audit(
            actual_audit, actual_payload, actual_payload_schema
        )
    else:
        for path, text in outputs.items():
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(text, encoding="utf-8", newline="\n")

    print(
        json.dumps(
            {
                "check": args.check,
                "direct_candidates": audit["direct_candidate_count"],
                "eligible_candidates": audit["eligible_candidate_count"],
                "mutations": len(audit["mutation_regressions"]),
                "paper": 193,
                "source_locks": audit["repository_source_lock_count"],
                "target_contract": audit["target_contract_status"],
                "verdict": audit["verdict"],
            },
            sort_keys=True,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
