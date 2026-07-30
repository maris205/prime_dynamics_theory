#!/usr/bin/env python3
"""Authoritative finite contract for the TPC-205 pair-native interface.

TPC-205 freezes an exact post-TT-star ordered-pair carrier, the fields that a
future production pair registry would have to contain, and the type mismatch
between that bilinear carrier and the linear H1 cut-to-occurrence edge.  It
does not materialize a production pair occurrence or prove a reopen theorem.
"""

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
STEM = "tpc205_pair_native_registry_interface"
PAYLOAD_PATH = HERE / f"{STEM}.json"
AUDIT_PATH = HERE / f"{STEM}_audit.json"
PAYLOAD_SCHEMA_PATH = (
    PAPER / "schemas" / "tpc205-pair-native-registry-interface-v1.schema.json"
)
AUDIT_SCHEMA_PATH = (
    PAPER
    / "schemas"
    / "tpc205-pair-native-registry-interface-audit-v1.schema.json"
)
L0_FIXTURE_PATH = PAPER / "samples" / "tpc205_pair_native_l0_fixtures.json"
L0_SCHEMA_PATH = (
    PAPER / "schemas" / "tpc205-pair-native-l0-interface-v1.schema.json"
)
MANIFEST_PATH = HERE / "tpc205_certificate_manifest.json"

SCHEMA_URI = "https://json-schema.org/draft/2020-12/schema"
HASH_MODE = "CANONICAL_UTF8_LF_V2"
AUTHORIZATION_SCOPE = (
    "FINITE_PAIR_NATIVE_POST_TTSTAR_REGISTRY_AND_ARCHITECTURE_REROUTE_INTERFACE"
)
CLASSIFICATION = "PAIR_NATIVE_POST_TTSTAR_REGISTRY_INTERFACE_L1"
THEOREM_STATUS = "PROVED_TYPED_INTERFACE_AND_FIRST_MISSING_L1"
VERDICT = "PAIR_NATIVE_ARCHITECTURE_REROUTE_INTERFACE_CERTIFIED_NOT_REOPENED"
FIRST_MISSING = (
    "SOURCE_LOCKED_POST_TTSTAR_ORDERED_PAIR_REGISTRY_WITH_COMPLETE_"
    "PAIR_COEFFICIENT_AND_GLOBAL_NORMALIZATION"
)
PAIR_STOP_CELL = (
    "TPC18_TPC93_POST_TTSTAR_PAIR_DIRECT_COMPOSITION_V1=STOP_SCOPED"
)
SOURCE_SNAPSHOT_COMMIT = "88ead9383270ab40a6350616554d519ede6f0782"

SOURCE_SPECS = [
    {
        "id": "TPC18.opened_d",
        "path": (
            "papers/tpc-18-mobius-tail-determinant-dispersion/"
            "sections/opened-d-dispersion.tex"
        ),
        "anchors": [
            r"\cC_D^{\mathrm{off}}",
            r"\sum_{\substack{\alpha_1\ne\alpha_2}}",
            r"B_{\alpha_1}(j)B_{\alpha_2}(j).",
            r"Here and below the prime and support restrictions",
        ],
    },
    {
        "id": "TPC18.stopping",
        "path": (
            "papers/tpc-18-mobius-tail-determinant-dispersion/"
            "sections/stopping-closure.tex"
        ),
        "anchors": [
            r"There are $O(\log X)$ slices",
            r"Sum the $O(\log X)$ divisor slices",
            r"|\cC_D^{\mathrm{gen}}|",
        ],
    },
    {
        "id": "TPC25.provenance",
        "path": (
            "papers/tpc-25-zero-before-separation/sections/provenance.tex"
        ),
        "anchors": [
            r"\gamma_\alpha",
            r"\mathfrak m(\alpha_1,\alpha_2)=0",
            r"The two sides of a bilinear packet",
        ],
    },
    {
        "id": "TPC25.zero_first",
        "path": (
            "papers/tpc-25-zero-before-separation/sections/zero-first.tex"
        ),
        "anchors": [
            r"\mathcal Z^0_{S,T}",
            r"X^{-s+\kappa+o(1)}",
            r"For a Hermitian convention the second factor is conjugated",
        ],
    },
    {
        "id": "TPC32.physical_shell",
        "path": (
            "papers/tpc-32-matched-cutoff-frequency-gate/"
            "sections/physical-matched-shell.tex"
        ),
        "anchors": [
            r"\mathfrak A_{\alpha,\gamma}(j)",
            r"\cK^{\mathrm{sh}}_{\alpha,\gamma}(j)",
            r"=C_m(j)\mathsf H_{n;T,U_0}(j)",
            r"No separability of the generic",
        ],
    },
    {
        "id": "TPC32.content",
        "path": (
            "papers/tpc-32-matched-cutoff-frequency-gate/"
            "sections/canonical-content-factorization.tex"
        ),
        "anchors": [
            "No complex conjugation is implicit.",
            r"\gamma_\alpha^{(1)}\gamma_\gamma^{(2)}",
        ],
    },
    {
        "id": "TPC32.certificate",
        "path": (
            "papers/tpc-32-matched-cutoff-frequency-gate/"
            "experiments/tpc32_certificate.json"
        ),
        "anchors": [
            '"primitive_witness"',
            '"rows"',
            '"targets"',
            '"primitive_finite_witness_is_twin_prime_asymptotic_evidence": false',
        ],
    },
    {
        "id": "TPC93.decorated_export",
        "path": (
            "papers/tpc-93-literal-low-window-affine-export/"
            "sections/decorated-affine-export.tex"
        ),
        "anchors": [
            r"\omega=(L,\alpha,\gamma,j,u)",
            r"\sum_{v\mid d,e}\lambda_{G_X^{\rm row}}(v)",
            r"no new fiber normalization is introduced",
            r"The labels \(L\) and \(R\) form a disjoint union",
        ],
    },
    {
        "id": "TPC143.main",
        "path": "papers/tpc-143-frontier-occurrence-lift-contract/main.tex",
        "anchors": [
            r"L_X:\mathbb C^{\Ccut}\longrightarrow\mathbb C^{\Occ}",
            "signed or",
            "complex.",
            r"\one_{\Occ}^{T}L_X=\one_{\Ccut}^{T}",
        ],
    },
    {
        "id": "TPC174.main",
        "path": "papers/tpc-174-local-occurrence-edge-witness-schema/main.tex",
        "anchors": [
            "exact nonzero rational weight",
            "exact column sum one",
            "SYNTHETIC\\_L0\\_ONLY",
        ],
    },
    {
        "id": "TPC179.main",
        "path": (
            "papers/tpc-179-h1-structural-corpus-exhaustion-integration/"
            "main.tex"
        ),
        "anchors": [
            r"\mathcal B_{H1}=\{E,A,M\}",
            r"\texttt{current\_verdict}&=\mathsf{NOT\_TESTABLE}",
            "none suppresses another",
        ],
    },
    {
        "id": "TPC133.rows",
        "path": (
            "papers/tpc-133-executable-native-entrance/"
            "samples/tpc133_native_atoms.jsonl"
        ),
        "anchors": [
            "e550d2d7be48d85076919a8adf86ba446f88f75b404df48c0483d3cf27b59369",
            "633e20ac5a83d425471be3ba095df10a1635c3f45ce5cac6def9d5ba936152d9",
        ],
    },
    {
        "id": "TPC136.cuts",
        "path": (
            "papers/tpc-136-complete-native-cut-archive/"
            "samples/tpc136_cut_paths.jsonl"
        ),
        "anchors": [
            "2eef9d8670c23ffc10b2a9cab0d488b0908293cfdb482667da824e702a1347cc",
            "cdc0f7363ab88106ce65bb46da800c05c3fba2b391d9490d7b2ca8bab8c816db",
        ],
    },
    {
        "id": "TPC204.payload",
        "path": (
            "papers/tpc-204-source-locked-production-registry-crosswalk/"
            "experiments/tpc204_source_locked_production_registry_crosswalk.json"
        ),
        "anchors": [
            '"complete_crosswalk_count": 0',
            '"first_common_missing_gate_id": "NAMED_PRODUCTION_ATOM"',
            '"reopen_trigger_passed": false',
        ],
    },
    {
        "id": "TPC18.tail_interface",
        "path": (
            "papers/tpc-18-mobius-tail-determinant-dispersion/"
            "sections/tail-interface.tex"
        ),
        "anchors": [
            r"\label{eq:source-power-error}",
            r"XL^{-1/2}X^\eps.",
            "In particular this has arbitrary logarithmic saving",
        ],
    },
    {
        "id": "TPC25.one_sided_closure",
        "path": (
            "papers/tpc-25-zero-before-separation/"
            "sections/one-sided-closure.tex"
        ),
        "anchors": [
            r"\label{eq:tpc25-zero-in-closure}",
            r"after all dyadic and divisor multiplicities.  The global principal",
            r"conductor cell is \(O(Q^2X^\eps)\)",
            r"\(O(JQ^2L^{-1}X^\eps)\)",
            r"Fixed bounded-overlap",
        ],
    },
    {
        "id": "TPC93.row_window",
        "path": (
            "papers/tpc-93-literal-low-window-affine-export/"
            "sections/row-window.tex"
        ),
        "anchors": [
            r"\label{eq:row-tail-return}",
            r"X^{o(1)}N_{0,X}R^{1/2-K}.",
            r"not a maximum over \(r\)",
        ],
    },
]

ACTIVE_ARTIFACTS = [
    (
        "papers/tpc-205-pair-native-post-ttstar-registry-interface/"
        "experiments/build_tpc205.py"
    ),
    (
        "papers/tpc-205-pair-native-post-ttstar-registry-interface/"
        "experiments/tpc205_pair_native_registry_interface.py"
    ),
    (
        "papers/tpc-205-pair-native-post-ttstar-registry-interface/"
        "experiments/tpc205_independent_checker.py"
    ),
    (
        "papers/tpc-205-pair-native-post-ttstar-registry-interface/"
        "experiments/tpc205_pair_native_registry_interface.json"
    ),
    (
        "papers/tpc-205-pair-native-post-ttstar-registry-interface/"
        "experiments/tpc205_pair_native_registry_interface_audit.json"
    ),
    (
        "papers/tpc-205-pair-native-post-ttstar-registry-interface/"
        "schemas/tpc205-pair-native-registry-interface-v1.schema.json"
    ),
    (
        "papers/tpc-205-pair-native-post-ttstar-registry-interface/"
        "schemas/tpc205-pair-native-registry-interface-audit-v1.schema.json"
    ),
    (
        "papers/tpc-205-pair-native-post-ttstar-registry-interface/"
        "schemas/tpc205-pair-native-l0-interface-v1.schema.json"
    ),
    (
        "papers/tpc-205-pair-native-post-ttstar-registry-interface/"
        "samples/tpc205_pair_native_l0_fixtures.json"
    ),
    "papers/tpc-205-pair-native-post-ttstar-registry-interface/README.md",
    "papers/tpc-205-pair-native-post-ttstar-registry-interface/main.tex",
    "papers/tpc-205-pair-native-post-ttstar-registry-interface/references.bib",
    (
        "papers/tpc-205-pair-native-post-ttstar-registry-interface/"
        "tpc-205-pair-native-post-ttstar-registry-interface.pdf"
    ),
]


def require(condition: bool, code: str) -> None:
    if not condition:
        raise RuntimeError(code)


def canonical(value: Any) -> str:
    return (
        json.dumps(value, ensure_ascii=False, indent=2, sort_keys=True)
        + "\n"
    )


def compact_canonical(value: Any) -> bytes:
    return json.dumps(
        value, ensure_ascii=False, separators=(",", ":"), sort_keys=True
    ).encode("utf-8")


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def sha256_value(value: Any) -> str:
    return sha256_bytes(canonical(value).encode("utf-8"))


def canonical_text_bytes(path: Path) -> bytes:
    text = path.read_text(encoding="utf-8")
    return text.replace("\r\n", "\n").replace("\r", "\n").encode("utf-8")


def raw_sha256(path: Path) -> str:
    return sha256_bytes(path.read_bytes())


def strict_same(left: Any, right: Any) -> bool:
    if type(left) is not type(right):
        return False
    if isinstance(left, dict):
        return set(left) == set(right) and all(
            strict_same(left[key], right[key]) for key in left
        )
    if isinstance(left, list):
        return len(left) == len(right) and all(
            strict_same(a, b) for a, b in zip(left, right)
        )
    return left == right


def strict_equal(left: Any, right: Any, code: str) -> None:
    require(strict_same(left, right), f"STRICT_EQUALITY:{code}")


def reject_constant(token: str) -> None:
    raise ValueError(f"non-finite JSON constant: {token}")


def unique_object(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
    result: dict[str, Any] = {}
    for key, value in pairs:
        if key in result:
            raise ValueError(f"duplicate JSON key: {key}")
        result[key] = value
    return result


def load_json(path: Path, canonical_bytes: bool = False) -> Any:
    raw = path.read_bytes()
    value = json.loads(
        raw.decode("utf-8"),
        object_pairs_hook=unique_object,
        parse_constant=reject_constant,
    )
    if canonical_bytes:
        require(raw == canonical(value).encode("utf-8"), f"NONCANONICAL:{path}")
    return value


def read_jsonl_record(path: Path, line_number: int) -> dict[str, Any]:
    lines = path.read_text(encoding="utf-8").splitlines()
    require(1 <= line_number <= len(lines), f"JSONL_LINE_RANGE:{path}")
    record = json.loads(
        lines[line_number - 1],
        object_pairs_hook=unique_object,
        parse_constant=reject_constant,
    )
    require(type(record) is dict, f"JSONL_RECORD_TYPE:{path}:{line_number}")
    return record


def select_jsonl_unique(
    path: Path, key: str, expected_value: str
) -> tuple[dict[str, Any], int]:
    matches: list[tuple[dict[str, Any], int]] = []
    for line_number, line in enumerate(
        path.read_text(encoding="utf-8").splitlines(), start=1
    ):
        record = json.loads(
            line,
            object_pairs_hook=unique_object,
            parse_constant=reject_constant,
        )
        if type(record) is dict and record.get(key) == expected_value:
            matches.append((record, line_number))
    require(
        len(matches) == 1,
        f"JSONL_SEMANTIC_ID_NOT_UNIQUE:{path}:{key}:{expected_value}",
    )
    return matches[0]


def verify_integrity_record(record: dict[str, Any]) -> None:
    require(
        type(record.get("integrity_sha256")) is str,
        "RECORD_INTEGRITY_FIELD",
    )
    expected = record["integrity_sha256"]
    body = {key: value for key, value in record.items() if key != "integrity_sha256"}
    require(
        sha256_bytes(compact_canonical(body)) == expected,
        f"RECORD_INTEGRITY_MISMATCH:{expected}",
    )


def build_source_locks() -> list[dict[str, Any]]:
    locks = []
    for spec in SOURCE_SPECS:
        path = REPO / spec["path"]
        require(path.is_file(), f"SOURCE_MISSING:{spec['id']}")
        text = canonical_text_bytes(path).decode("utf-8")
        for anchor in spec["anchors"]:
            require(anchor in text, f"SOURCE_ANCHOR_MISSING:{spec['id']}:{anchor}")
        locks.append(
            {
                "id": spec["id"],
                "path": spec["path"],
                "hash_mode": HASH_MODE,
                "hash_semantics": "INTEGRITY_ONLY",
                "canonical_sha256": sha256_bytes(canonical_text_bytes(path)),
                "required_anchors": list(spec["anchors"]),
            }
        )
    return locks


RELATION_TYPES = [
    {
        "id": "TTSTAR_BILINEAR_PAIR_TERM",
        "origin": "TPC18.eq:d-off",
        "arity": 2,
        "ordered": True,
        "source_object": "post-Cauchy row-pair",
        "linear_cut_edge": False,
    },
    {
        "id": "LINEAR_CUT_TO_OCCURRENCE_EDGE",
        "origin": "TPC143.occurrence_lift",
        "arity": 1,
        "ordered": False,
        "source_object": "production cut column",
        "linear_cut_edge": True,
    },
    {
        "id": "TPC93_RETAINED_SOURCE_ATOM",
        "origin": "TPC93.eq:source-left-atom",
        "arity": 5,
        "ordered": True,
        "source_object": "supplied omega=(L/R,alpha,gamma,j,u)",
        "linear_cut_edge": False,
    },
    {
        "id": "TPC93_SOURCE_CHILD",
        "origin": "TPC93.thm:source-child-reconstruction",
        "arity": 2,
        "ordered": True,
        "source_object": "child=(theta,t) indexed by supplied omega and v",
        "linear_cut_edge": False,
    },
]

FORMULA_CONTRACT = {
    "ordered_domain": (
        "same opened-D packet: sum_j sum_{alpha!=gamma}; "
        "alpha=(ell_alpha,d_alpha), gamma=(ell_gamma,d_gamma)"
    ),
    "displayed_coefficient_factors": [
        "mu(d_alpha)",
        "mu(d_gamma)",
        "log(ell_alpha)",
        "log(ell_gamma)",
        "r_R(N_alpha(j))",
        "r_R(N_gamma(j))",
        "B_alpha(j)",
        "B_gamma(j)",
    ],
    "coefficient_status": "DISPLAYED_WITH_B_ALIASES_NOT_FULLY_MATERIALIZED",
    "support_restrictions_status": "UNDERSTOOD_BY_TPC18_NOT_LITERALIZED",
    "conjugation_rule": "NO_IMPLICIT_CONJUGATION",
    "second_row_gamma_rule": "GENERATED_BY_TTSTAR_SQUARE_EXPANSION",
    "diagonal_rule": "SEPARATE_E_D_NOT_AN_OFF_DIAGONAL_PARENT",
    "support_nonzero_rule": "FORMULA_SUPPORT_DOES_NOT_IMPLY_ACTIVE_NONZERO",
    "matched_shell": (
        "K_sh(alpha,gamma,j)=C_m(j)H_n(j)+H_m(j)C_n(j)"
    ),
    "left_u_rule": "T<u<=U0 and u|N_alpha(j)",
    "right_u_rule": "T<u<=U0 and u|N_gamma(j)",
    "pair_to_omega_bridge": "MISSING",
}

SOURCE_CHILD_CONTRACT = {
    "supplied_source_atom": "omega=(L/R,alpha,gamma,j,u)",
    "projector_identity": (
        "sum_{v|d,e} lambda_{G_X^row}(v)"
        "=1_{gcd(d,e)<=G_X^row}"
    ),
    "single_child_restores_source": False,
    "weighted_child_sum_restores": (
        "actual-row-gcd-masked source coefficient"
    ),
    "weighted_reassembly_support": (
        "ON_TPC93_PHYSICAL_SQUAREFREE_AND_TARGET_PRIMITIVE_SUPPORT"
    ),
    "source_sign_coprimality": "(d,u)=1_FROM_TARGET_PRIMITIVITY",
    "source_child_inverse": "PASS_ON_SUPPLIED_RETAINED_OMEGA",
    "polarizations": ["L", "R"],
    "fiber_normalization": "NO_NEW_FIBER_NORMALIZATION",
    "downstream_xi_template": "CONDITIONAL_ON_SEPARATELY_SUPPLIED_FIELDS",
    "production_pair_to_omega_crosswalk": "FAIL",
}

REGISTRY_CONTRACT = {
    "registry_mode": "TYPED_INTERFACE_ONLY",
    "production_row_count": 0,
    "production_row_count_scope": (
        "DECLARED_TPC205_REGISTRY_SOURCE_LOCK_CORPUS_ONLY"
    ),
    "identity_scope_fields": [
        "X",
        "h0",
        "delta",
        "R",
        "V",
        "D0",
        "L",
        "K",
        "D",
        "J",
        "Q",
        "T",
        "U0",
        "G_X_row",
        "packet_id",
        "source_locator",
    ],
    "ordered_pair_fields": [
        "alpha=(ell_alpha,d_alpha)",
        "gamma=(ell_gamma,d_gamma)",
        "j",
        "N_alpha(j)",
        "N_gamma(j)",
        "joint_mask_value",
        "literal_pair_coefficient_ast",
        "relation_type=TTSTAR_BILINEAR_PAIR_TERM",
        "formal_support_status",
        "numeric_nonzero_status",
    ],
    "source_child_fields": [
        "polarization",
        "u",
        "sigma",
        "v",
        "iota",
        "theta",
        "t",
        "projector_weight",
        "child_to_source_inverse",
        "content_child",
        "frequency_child",
        "resolved_xi",
    ],
    "normalization_fields": [
        "source_normalization",
        "linear_normalization",
        "quadratic_normalization",
        "target_normalization",
    ],
    "id_semantics": {
        "edge_instance_id": "UNIQUE_PER_TRANSFORMATION_ROW",
        "target_occurrence_id": "MAY_BE_SHARED_BY_MANY_TO_ONE_THEOREM",
        "ids_must_be_distinct_fields": True,
    },
    "ordered_pair_quotient": "FORBIDDEN",
}

NORMALIZATION_CONTRACT = {
    "tpc18_object": "UNNORMALIZED_T_D",
    "archived_nu_X_status": "SCOPE_STRING_NOT_NUMERIC_SCALAR",
    "conditional_scalar_identity": (
        "|c_X T_D|^2 <= C_W |c_X|^2 J(E_D+C_D^off)"
    ),
    "global_normalization_return": "MISSING_UNSUPPLIED",
}

LOSS_LEDGER = [
    {
        "id": "prime_power_error",
        "status": "SOURCE_BACKED_BOUND",
        "value": "X L^(-1/2) X^eps",
        "scope": "TPC18_HYPOTHESES_ONLY_NOT_ATTACHED_TO_PRODUCTION_PAIR",
    },
    {
        "id": "dyadic_D_partition",
        "status": "SOURCE_BACKED_ACCOUNTING",
        "value": (
            "fixed bounded overlap; O(log X) nonempty slices; "
            "at most one O(log X) reassembly/pigeonhole factor"
        ),
        "scope": "TPC18_HYPOTHESES_ONLY_NOT_ATTACHED_TO_PRODUCTION_PAIR",
    },
    {
        "id": "cauchy_factor",
        "status": "SOURCE_BACKED_ACCOUNTING",
        "value": "J",
        "scope": "TPC18_HYPOTHESES_ONLY_NOT_ATTACHED_TO_PRODUCTION_PAIR",
    },
    {
        "id": "diagonal",
        "status": "SOURCE_BACKED_BOUND",
        "value": "E_D << X^(1+eps)",
        "scope": "TPC18_HYPOTHESES_ONLY_NOT_ATTACHED_TO_PRODUCTION_PAIR",
    },
    {
        "id": "same_rows",
        "status": "SOURCE_BACKED_BOUND",
        "value": "XQ L^(-1) X^eps",
        "scope": "TPC18_HYPOTHESES_ONLY_NOT_ATTACHED_TO_PRODUCTION_PAIR",
    },
    {
        "id": "near_rows",
        "status": "SOURCE_BACKED_BOUND",
        "value": "XQ (X^(-kappa)+L^(-1)) X^eps",
        "scope": "TPC18_HYPOTHESES_ONLY_NOT_ATTACHED_TO_PRODUCTION_PAIR",
    },
    {
        "id": "large_row_gcd",
        "status": "SOURCE_BACKED_BOUND",
        "value": "XQ X^(-kappa+eps)",
        "scope": "TPC18_HYPOTHESES_ONLY_NOT_ATTACHED_TO_PRODUCTION_PAIR",
    },
    {
        "id": "generic_remainder",
        "status": "UNCONTROLLED_HARD_REMAINDER",
        "value": "MISSING",
        "scope": "TPC18_HYPOTHESES_ONLY_NOT_ATTACHED_TO_PRODUCTION_PAIR",
    },
    {
        "id": "tpc25_zero",
        "status": "SOURCE_BACKED_BOUND",
        "value": "XQ{(log X)^(-A)+X^(-s+kappa+o(1))}",
        "scope": (
            "TPC25_THEOREM_HYPOTHESES_ONLY_NOT_COMPOSED_WITH_TPC18_PAIR"
        ),
    },
    {
        "id": "tpc25_principal",
        "status": "SOURCE_BACKED_BOUND",
        "value": "Q^2 X^eps",
        "scope": (
            "TPC25_THEOREM_HYPOTHESES_ONLY_NOT_COMPOSED_WITH_TPC18_PAIR"
        ),
    },
    {
        "id": "tpc25_drift",
        "status": "SOURCE_BACKED_BOUND",
        "value": "JQ^2 L^(-1) X^eps",
        "scope": (
            "TPC25_THEOREM_HYPOTHESES_ONLY_NOT_COMPOSED_WITH_TPC18_PAIR"
        ),
    },
    {
        "id": "tpc25_polylog",
        "status": "SOURCE_BACKED_ACCOUNTING",
        "value": "(log X)^(O(1))",
        "scope": (
            "TPC25_THEOREM_HYPOTHESES_ONLY_NOT_COMPOSED_WITH_TPC18_PAIR"
        ),
    },
    {
        "id": "tpc32_drift",
        "status": "SOURCE_BACKED_BOUND",
        "value": "X^eps XQ/L",
        "scope": (
            "TPC32_THEOREM_HYPOTHESES_ONLY_NOT_COMPOSED_WITH_TPC18_PAIR"
        ),
    },
    {
        "id": "large_content",
        "status": "SOURCE_BACKED_BOUND",
        "value": "X^eps XQ(1/J+1/C)",
        "scope": (
            "TPC32_THEOREM_HYPOTHESES_ONLY_NOT_COMPOSED_WITH_TPC18_PAIR"
        ),
    },
    {
        "id": "tpc93_fourier_tail",
        "status": "SOURCE_BACKED_BOUND",
        "value": "X^(o(1)) N0 Rwin^(1/2-K)",
        "scope": (
            "TPC93_THEOREM_HYPOTHESES_ONLY_NOT_COMPOSED_WITH_TPC18_PAIR"
        ),
    },
    {
        "id": "square_root_return",
        "status": "MISSING_UNSUPPLIED",
        "value": "MISSING",
        "scope": "GLOBAL_RETURN_SLOT_UNSUPPLIED",
    },
    {
        "id": "full_block_endpoint_reassembly",
        "status": "MISSING_UNSUPPLIED",
        "value": "MISSING",
        "scope": "GLOBAL_RETURN_SLOT_UNSUPPLIED",
    },
]

H1_TYPE_SEPARATION = {
    "pair_relation": "TTSTAR_BILINEAR_PAIR_TERM",
    "h1_relation": "LINEAR_CUT_TO_OCCURRENCE_EDGE",
    "tpc143_conceptual_entries": "SIGNED_OR_COMPLEX_ALLOWED",
    "tpc174_finite_contract": (
        "NONZERO_EXACT_RATIONAL_WEIGHTS_AND_PER_CUT_COLUMN_SUM_ONE"
    ),
    "cut_inverse_aggregation_theorem": "MISSING",
    "h1_E_repair": False,
    "active_support_root_A": "NOT_TESTABLE",
    "canonical_minimal_root_M": "NOT_TESTABLE",
}

GATES = [
    {
        "id": "ORDERED_POST_TTSTAR_PAIR_DOMAIN",
        "status": "PASS_FORMULA",
    },
    {
        "id": "TPC18_DISPLAYED_PAIR_COEFFICIENT_WITH_B_ALIASES",
        "status": "PASS_FORMULA",
    },
    {
        "id": "SECOND_ROW_GAMMA_FROM_TTSTAR_EXPANSION",
        "status": "PASS_FORMULA",
    },
    {
        "id": "U_FROM_SUPPLIED_TPC32_93_PARENT_POLARIZATION",
        "status": "PASS_FORMULA",
    },
    {
        "id": "TPC93_SOURCE_CHILD_REINDEXING",
        "status": "PASS_L1_ON_SUPPLIED_RETAINED_OMEGA",
    },
    {
        "id": "CONCRETE_DUAL_ARCHIVED_ROW_CANDIDATE",
        "status": "PASS_ROW_ONLY",
    },
    {
        "id": "TPC32_TPC93_DERIVED_AFFINE_CHILD",
        "status": "PASS_DERIVED_L0_ONLY",
    },
    {
        "id": "ACTIVE_PRODUCTION_PAIR_OCCURRENCE",
        "status": "NOT_TESTABLE",
    },
    {
        "id": "FULL_LITERAL_PAIR_COEFFICIENT_MATERIALIZATION",
        "status": "NOT_TESTABLE",
    },
    {
        "id": "PAIR_COEFFICIENT_MATERIALIZATION_AND_NONZERO",
        "status": "NOT_TESTABLE",
    },
    {
        "id": "SOURCE_LOCKED_PAIR_TO_OMEGA_CROSSWALK",
        "status": "FAIL",
    },
    {
        "id": "NU_X_NORMALIZED_RETURN_TO_H1",
        "status": "FAIL",
    },
    {"id": "H1_E_REPAIR", "status": "FAIL"},
    {"id": "PAIR_NATIVE_FORMULA_GATE", "status": "PASS"},
    {
        "id": "PAIR_NATIVE_ARCHITECTURE_REROUTE_CANDIDATE",
        "status": "OPEN",
    },
    {
        "id": "PAIR_NATIVE_PRODUCTION_REOPEN_TRIGGER",
        "status": "FAIL",
    },
    {
        "id": "PAIR_NATIVE_STRUCTURAL_REOPEN_TRIGGER",
        "status": "FAIL",
    },
    {
        "id": "TPC32_MATCHED_SHELL_AND_POLARIZATION",
        "status": "PASS_L1_FORMULA",
    },
    {
        "id": "TPC18_PAIR_TO_TPC32_LITERAL_PARENT_CROSSWALK",
        "status": "NOT_TESTABLE",
    },
    {
        "id": "TPC93_PROJECTOR_WEIGHTED_REASSEMBLY",
        "status": (
            "PASS_L1_ON_SUPPLIED_RETAINED_OMEGA_AND_TPC93_PHYSICAL_SUPPORT"
        ),
    },
    {
        "id": "TTSTAR_PAIR_VS_H1_LINEAR_EDGE_TYPE_SEPARATION",
        "status": "PASS_L1_STRUCTURAL",
    },
    {
        "id": "PAIR_NATIVE_ACTIVE_SUPPORT_CERTIFICATE",
        "status": "NOT_TESTABLE",
    },
    {
        "id": "PAIR_NATIVE_CANONICAL_MINIMAL_REPRESENTATION",
        "status": "NOT_TESTABLE",
    },
]

STOP_SCOPED = [
    "TPC193_DECLARED_CANDIDATE_MECHANISM_CORPUS_V1=STOP_SCOPED",
    "TPC204_DECLARED_PLAUSIBLE_PRODUCTION_CROSSWALK_CORPUS_V1=STOP_SCOPED",
    "TPC18_25_32_93_194_SINGLE_CUT_OCCURRENCE_COMPOSITE_V1=STOP_SCOPED",
    PAIR_STOP_CELL,
]

CLAIM_FIREWALL = {
    "production_pair_occurrence_proved": False,
    "pair_to_omega_crosswalk_proved": False,
    "h1_repair_proved": False,
    "structural_reopen": False,
    "mathematical_reopen": False,
    "fixed_atom_decay_obtained": False,
    "positive_sigma_obtained": False,
    "strict_one_over_400_paid": False,
    "fixed_atom_credit": 0,
    "program_positive_L2": False,
    "L2_result": "NONE",
    "twin_prime_theorem": False,
    "user_authorization_is_theorem_evidence": False,
}

ROUTE_STATE = {
    "H1_architecture": "OPEN",
    "bad_endpoint_O161_parent": "OPEN",
    "direct_twist_O161_parent": "OPEN",
    "global_architecture": "OPEN",
    "pair_native_architecture_reroute": "OPEN",
}

DECISION = {
    "batch_stop": "USER_CONFIRMATION_REQUIRED",
    "next_paper": None,
    "tpc206_authorized": False,
}


def build_fixtures() -> list[dict[str, Any]]:
    row_path = REPO / SOURCE_SPECS[11]["path"]
    cut_path = REPO / SOURCE_SPECS[12]["path"]
    alpha_native_id = "X=512|h0=2|ell=103|k=5|d=1"
    gamma_native_id = "X=512|h0=2|ell=107|k=5|d=1"
    alpha_cut_id = (
        "cut|X=512|h0=2|ell=103|k=5|d=1|jL=6|jK=3|D0=0|type=TAIL"
    )
    gamma_cut_id = (
        "cut|X=512|h0=2|ell=107|k=5|d=1|jL=6|jK=3|D0=0|type=TAIL"
    )
    row_alpha, row_alpha_line = select_jsonl_unique(
        row_path, "native_id", alpha_native_id
    )
    row_gamma, row_gamma_line = select_jsonl_unique(
        row_path, "native_id", gamma_native_id
    )
    cut_alpha, cut_alpha_line = select_jsonl_unique(
        cut_path, "cut_path_id", alpha_cut_id
    )
    cut_gamma, cut_gamma_line = select_jsonl_unique(
        cut_path, "cut_path_id", gamma_cut_id
    )
    require(
        [row_alpha_line, row_gamma_line, cut_alpha_line, cut_gamma_line]
        == [724, 736, 2554, 2602],
        "ARCHIVE_LOCATOR_DRIFT",
    )
    for record in [row_alpha, row_gamma, cut_alpha, cut_gamma]:
        verify_integrity_record(record)
    require(row_alpha["native_tuple"] == [103, 5, 1], "ROW_ALPHA_TUPLE")
    require(row_gamma["native_tuple"] == [107, 5, 1], "ROW_GAMMA_TUPLE")
    require(
        cut_alpha["metadata"]["native_tuple"] == [103, 5, 1],
        "CUT_ALPHA_TUPLE",
    )
    require(
        cut_gamma["metadata"]["native_tuple"] == [107, 5, 1],
        "CUT_GAMMA_TUPLE",
    )
    for record in [cut_alpha, cut_gamma]:
        require(
            record["cut_terminal_type"] == "FRONTIER_UNMAPPED",
            "CUT_TERMINAL_STATUS",
        )
        require(
            record["metadata"]["frontier_reason"] == "NO_TAIL_ROOM",
            "CUT_FRONTIER_REASON",
        )

    cert_path = REPO / SOURCE_SPECS[6]["path"]
    cert = load_json(cert_path)
    primitive = cert["coherent_witness_summary"]["primitive_witness"]
    expected_direct = {
        "L": 100,
        "R": 12,
        "T": 50,
        "U0": 200,
        "C": 30,
        "h": 2,
        "j": 1,
        "d": 1,
        "rows": [59, 71, 101, 107, 137, 149, 179, 191, 197],
        "targets": [61, 73, 103, 109, 139, 151, 181, 193, 199],
    }
    for key, value in expected_direct.items():
        strict_equal(primitive[key], value, f"TPC32_FIXTURE:{key}")

    ell = 59
    gamma_ell = 71
    d = 1
    e = 1
    j = 1
    h0 = 2
    u = 61
    sigma = (ell * d * j + h0) // u
    v = 1
    d0 = 0
    t = (d // v - d0) // sigma
    u0 = (ell * j * v * d0 + h0) // sigma
    D_t = d0 + sigma * t
    U_t = u0 + ell * j * v * t
    require(sigma == 1 and t == 1 and u0 == 2, "DERIVED_CHILD_PARAMETERS")
    require(D_t == 1 and U_t == 61, "DERIVED_CHILD_VALUES")
    require(sigma * U_t - ell * j * v * D_t == 2, "DERIVED_DETERMINANT")

    return [
        {
            "id": "DUAL_SOURCE_LOCKED_ROW_PAIR_CANDIDATE",
            "evidence_level": "ROW_ONLY",
            "h0": 2,
            "ordered_pair": {
                "alpha": [103, 1],
                "gamma": [107, 1],
                "j": 5,
                "N_alpha": 517,
                "N_gamma": 537,
                "gcd_targets": 1,
                "Delta_sharp": -4,
                "ordered_row_determinant": -8,
            },
            "row_locators": [
                {
                    "path": SOURCE_SPECS[11]["path"],
                    "line": row_alpha_line,
                    "native_id": row_alpha["native_id"],
                    "integrity_sha256": row_alpha["integrity_sha256"],
                },
                {
                    "path": SOURCE_SPECS[11]["path"],
                    "line": row_gamma_line,
                    "native_id": row_gamma["native_id"],
                    "integrity_sha256": row_gamma["integrity_sha256"],
                },
            ],
            "cut_locators": [
                {
                    "path": SOURCE_SPECS[12]["path"],
                    "line": cut_alpha_line,
                    "cut_path_id": cut_alpha["cut_path_id"],
                    "integrity_sha256": cut_alpha["integrity_sha256"],
                    "terminal": "FRONTIER_UNMAPPED",
                    "reason": "NO_TAIL_ROOM",
                },
                {
                    "path": SOURCE_SPECS[12]["path"],
                    "line": cut_gamma_line,
                    "cut_path_id": cut_gamma["cut_path_id"],
                    "integrity_sha256": cut_gamma["integrity_sha256"],
                    "terminal": "FRONTIER_UNMAPPED",
                    "reason": "NO_TAIL_ROOM",
                },
            ],
            "pair_occurrence_id": None,
            "joint_mask_value": None,
            "numeric_nonzero_status": "UNDECIDED",
            "production_occurrence": False,
        },
        {
            "id": "TPC32_PRIMITIVE_FIXTURE_PLUS_TPC93_FORMULAS_DERIVED_L0_ONLY",
            "evidence_level": "DERIVED_L0_ONLY",
            "direct_tpc32_fields": expected_direct,
            "derived_tpc93_fields": {
                "polarization": "L",
                "alpha": [ell, d],
                "gamma": [gamma_ell, e],
                "j": j,
                "u": u,
                "sigma": sigma,
                "v": v,
                "d0": d0,
                "t": t,
                "u0": u0,
                "D_t": D_t,
                "U_t": U_t,
                "determinant": 2,
                "projector_weight": 1,
            },
            "child_fields_directly_certified_by_tpc32": False,
            "production_occurrence": False,
            "asymptotic_evidence": False,
        },
    ]


def build_payload() -> dict[str, Any]:
    fixtures = build_fixtures()
    return {
        "schema": "tpc-205-pair-native-registry-interface-v1",
        "paper": 205,
        "authorization": {
            "scope": AUTHORIZATION_SCOPE,
            "user_authorized": True,
            "authorization_is_theorem_evidence": False,
        },
        "classification": CLASSIFICATION,
        "theorem_status": THEOREM_STATUS,
        "verdict": VERDICT,
        "source_snapshot_commit": SOURCE_SNAPSHOT_COMMIT,
        "source_locks": build_source_locks(),
        "relation_types": copy.deepcopy(RELATION_TYPES),
        "formula_contract": copy.deepcopy(FORMULA_CONTRACT),
        "source_child_contract": copy.deepcopy(SOURCE_CHILD_CONTRACT),
        "registry_contract": copy.deepcopy(REGISTRY_CONTRACT),
        "fixtures": fixtures,
        "normalization_contract": copy.deepcopy(NORMALIZATION_CONTRACT),
        "loss_ledger": copy.deepcopy(LOSS_LEDGER),
        "first_missing": FIRST_MISSING,
        "first_missing_subgates": [
            (
                "PAIR_NATIVE_POST_TTSTAR_ACTUAL_REGISTRY_WITH_FULL_LITERAL_"
                "SCOPE_AND_COEFFICIENT"
            ),
            "TPC18_PAIR_TO_TPC93_RETAINED_SOURCE_ATOM_THEOREM_CROSSWALK",
        ],
        "h1_type_separation": copy.deepcopy(H1_TYPE_SEPARATION),
        "gates": copy.deepcopy(GATES),
        "stop_scoped": copy.deepcopy(STOP_SCOPED),
        "claim_firewall": copy.deepcopy(CLAIM_FIREWALL),
        "route_state": copy.deepcopy(ROUTE_STATE),
        "decision": copy.deepcopy(DECISION),
        "summary_counts": {
            "source_locks": len(SOURCE_SPECS),
            "relation_types": len(RELATION_TYPES),
            "required_registry_fields": (
                len(REGISTRY_CONTRACT["identity_scope_fields"])
                + len(REGISTRY_CONTRACT["ordered_pair_fields"])
                + len(REGISTRY_CONTRACT["source_child_fields"])
                + len(REGISTRY_CONTRACT["normalization_fields"])
            ),
            "fixtures": len(fixtures),
            "production_pair_records": 0,
            "loss_ledger_rows": len(LOSS_LEDGER),
            "gates": len(GATES),
        },
    }


def semantic_result(payload: dict[str, Any]) -> dict[str, Any]:
    require(type(payload) is dict, "PAYLOAD_TYPE")
    require(type(payload.get("paper")) is int, "PAPER_STRICT_INT")
    require(payload["paper"] == 205, "PAPER_VALUE")
    require(
        payload["authorization"]["scope"] == AUTHORIZATION_SCOPE,
        "AUTHORIZATION_SCOPE",
    )
    require(payload["authorization"]["user_authorized"] is True, "AUTHORIZATION")
    require(
        payload["authorization"]["authorization_is_theorem_evidence"] is False,
        "AUTHORIZATION_EVIDENCE",
    )
    require(payload["classification"] == CLASSIFICATION, "CLASSIFICATION")
    require(payload["theorem_status"] == THEOREM_STATUS, "THEOREM_STATUS")
    require(payload["verdict"] == VERDICT, "VERDICT")
    require(
        payload["source_snapshot_commit"] == SOURCE_SNAPSHOT_COMMIT,
        "SOURCE_SNAPSHOT_COMMIT",
    )
    strict_equal(payload["source_locks"], build_source_locks(), "source_locks")
    strict_equal(payload["relation_types"], RELATION_TYPES, "relation_types")
    strict_equal(payload["formula_contract"], FORMULA_CONTRACT, "formula_contract")
    strict_equal(
        payload["source_child_contract"],
        SOURCE_CHILD_CONTRACT,
        "source_child_contract",
    )
    strict_equal(
        payload["registry_contract"], REGISTRY_CONTRACT, "registry_contract"
    )
    strict_equal(payload["fixtures"], build_fixtures(), "fixtures")
    strict_equal(
        payload["normalization_contract"],
        NORMALIZATION_CONTRACT,
        "normalization_contract",
    )
    strict_equal(payload["loss_ledger"], LOSS_LEDGER, "loss_ledger")
    require(payload["first_missing"] == FIRST_MISSING, "FIRST_MISSING")
    require(
        payload["first_missing_subgates"]
        == [
            (
                "PAIR_NATIVE_POST_TTSTAR_ACTUAL_REGISTRY_WITH_FULL_LITERAL_"
                "SCOPE_AND_COEFFICIENT"
            ),
            "TPC18_PAIR_TO_TPC93_RETAINED_SOURCE_ATOM_THEOREM_CROSSWALK",
        ],
        "FIRST_MISSING_SUBGATES",
    )
    strict_equal(
        payload["h1_type_separation"],
        H1_TYPE_SEPARATION,
        "h1_type_separation",
    )
    strict_equal(payload["gates"], GATES, "gates")
    strict_equal(payload["stop_scoped"], STOP_SCOPED, "stop_scoped")
    strict_equal(payload["claim_firewall"], CLAIM_FIREWALL, "claim_firewall")
    strict_equal(payload["route_state"], ROUTE_STATE, "route_state")
    strict_equal(payload["decision"], DECISION, "decision")
    expected_counts = {
        "source_locks": len(SOURCE_SPECS),
        "relation_types": len(RELATION_TYPES),
        "required_registry_fields": 42,
        "fixtures": 2,
        "production_pair_records": 0,
        "loss_ledger_rows": len(LOSS_LEDGER),
        "gates": len(GATES),
    }
    strict_equal(payload["summary_counts"], expected_counts, "summary_counts")
    return {
        "source_locks_verified": len(payload["source_locks"]),
        "relation_types_verified": len(payload["relation_types"]),
        "required_registry_fields": payload["summary_counts"][
            "required_registry_fields"
        ],
        "fixtures_verified": len(payload["fixtures"]),
        "production_pair_records": 0,
        "loss_ledger_rows_verified": len(payload["loss_ledger"]),
        "gates_verified": len(payload["gates"]),
        "first_missing": FIRST_MISSING,
        "h1_repair": False,
        "architecture_reroute": "OPEN",
        "mathematical_reopen": False,
    }


def exact_schema(value: Any, schema_id: str) -> dict[str, Any]:
    def node(item: Any) -> dict[str, Any]:
        if type(item) is dict:
            return {
                "type": "object",
                "properties": {key: node(item[key]) for key in sorted(item)},
                "required": sorted(item),
                "additionalProperties": False,
            }
        if type(item) is list:
            return {
                "type": "array",
                "prefixItems": [node(child) for child in item],
                "items": False,
                "minItems": len(item),
                "maxItems": len(item),
            }
        if item is None:
            return {"type": "null", "const": None}
        if type(item) is bool:
            return {"type": "boolean", "const": item}
        if type(item) is int:
            return {"type": "integer", "const": item}
        if type(item) is str:
            return {"type": "string", "const": item}
        raise TypeError(f"unsupported schema value: {type(item)!r}")

    result = node(value)
    result["$schema"] = SCHEMA_URI
    result["$id"] = schema_id
    return result


def schema_accepts(schema: dict[str, Any], value: Any) -> bool:
    kind = schema.get("type")
    expected_types = {
        "object": dict,
        "array": list,
        "null": type(None),
        "boolean": bool,
        "integer": int,
        "string": str,
    }
    if kind not in expected_types or type(value) is not expected_types[kind]:
        return False
    if "const" in schema and not strict_same(value, schema["const"]):
        return False
    if kind == "object":
        properties = schema["properties"]
        if set(value) != set(schema["required"]):
            return False
        if schema.get("additionalProperties") is not False:
            return False
        return all(schema_accepts(properties[key], value[key]) for key in value)
    if kind == "array":
        if schema.get("items") is not False:
            return False
        if not (schema["minItems"] == len(value) == schema["maxItems"]):
            return False
        return all(
            schema_accepts(child_schema, child)
            for child_schema, child in zip(schema["prefixItems"], value)
        )
    return True


def set_path(value: Any, path: list[Any], replacement: Any) -> Any:
    result = copy.deepcopy(value)
    cursor = result
    for key in path[:-1]:
        cursor = cursor[key]
    cursor[path[-1]] = replacement
    return result


BASE_MUTATIONS: list[tuple[str, Callable[[dict[str, Any]], dict[str, Any]]]] = [
    ("top_extra", lambda p: {**p, "unexpected": 1}),
    ("top_missing_schema", lambda p: {k: v for k, v in p.items() if k != "schema"}),
    ("paper_bool", lambda p: set_path(p, ["paper"], True)),
    (
        "authorization_extra",
        lambda p: set_path(
            p,
            ["authorization"],
            {**p["authorization"], "implied_reopen": True},
        ),
    ),
    (
        "relation_delete",
        lambda p: set_path(p, ["relation_types"], p["relation_types"][:-1]),
    ),
    (
        "coefficient_truncate",
        lambda p: set_path(
            p,
            ["formula_contract", "displayed_coefficient_factors"],
            p["formula_contract"]["displayed_coefficient_factors"][:-1],
        ),
    ),
    (
        "fixture_extra_field",
        lambda p: set_path(
            p,
            ["fixtures", 0],
            {**p["fixtures"][0], "promoted": True},
        ),
    ),
    (
        "loss_extra_row",
        lambda p: set_path(
            p,
            ["loss_ledger"],
            p["loss_ledger"] + [{"id": "invented", "status": "PAID", "value": "0"}],
        ),
    ),
    ("gate_removed", lambda p: set_path(p, ["gates"], p["gates"][:-1])),
    (
        "source_anchor_count_bool",
        lambda p: set_path(p, ["summary_counts", "source_locks"], True),
    ),
    (
        "first_missing_list",
        lambda p: set_path(p, ["first_missing"], [p["first_missing"]]),
    ),
    (
        "firewall_L2_bool",
        lambda p: set_path(p, ["claim_firewall", "L2_result"], False),
    ),
]

SEMANTIC_MUTATIONS: list[tuple[str, list[Any], Any]] = [
    ("authorization_false", ["authorization", "user_authorized"], False),
    (
        "authorization_becomes_evidence",
        ["authorization", "authorization_is_theorem_evidence"],
        True,
    ),
    ("classification_drift", ["classification"], "PAIR_NATIVE_THEOREM_L2"),
    ("verdict_reopened", ["verdict"], "REOPENED"),
    ("pair_arity_one", ["relation_types", 0, "arity"], 1),
    ("pair_unordered", ["relation_types", 0, "ordered"], False),
    (
        "pair_mislabeled_linear",
        ["relation_types", 0, "linear_cut_edge"],
        True,
    ),
    (
        "coefficient_promoted_complete",
        ["formula_contract", "coefficient_status"],
        "FULLY_MATERIALIZED",
    ),
    (
        "implicit_conjugation_added",
        ["formula_contract", "conjugation_rule"],
        "IMPLICIT_HERMITIAN",
    ),
    (
        "pair_to_omega_bridge_pass",
        ["formula_contract", "pair_to_omega_bridge"],
        "PASS",
    ),
    (
        "single_child_restores",
        ["source_child_contract", "single_child_restores_source"],
        True,
    ),
    (
        "production_crosswalk_pass",
        ["source_child_contract", "production_pair_to_omega_crosswalk"],
        "PASS",
    ),
    (
        "registry_production_row",
        ["registry_contract", "production_row_count"],
        1,
    ),
    (
        "pair_quotient_allowed",
        ["registry_contract", "ordered_pair_quotient"],
        "ALLOWED",
    ),
    (
        "row_candidate_promoted",
        ["fixtures", 0, "production_occurrence"],
        True,
    ),
    (
        "row_candidate_nonzero",
        ["fixtures", 0, "numeric_nonzero_status"],
        "PROVED_NONZERO",
    ),
    (
        "derived_child_directly_certified",
        ["fixtures", 1, "child_fields_directly_certified_by_tpc32"],
        True,
    ),
    (
        "derived_child_asymptotic",
        ["fixtures", 1, "asymptotic_evidence"],
        True,
    ),
    (
        "nu_X_promoted_scalar",
        ["normalization_contract", "archived_nu_X_status"],
        "NUMERIC_SCALAR",
    ),
    (
        "global_normalization_supplied",
        ["normalization_contract", "global_normalization_return"],
        "SUPPLIED",
    ),
    (
        "hard_remainder_controlled",
        ["loss_ledger", 7, "status"],
        "SOURCE_BACKED_BOUND",
    ),
    (
        "square_root_return_supplied",
        ["loss_ledger", 15, "status"],
        "SUPPLIED",
    ),
    ("first_missing_changed", ["first_missing"], "NONE"),
    (
        "cut_inverse_theorem_invented",
        ["h1_type_separation", "cut_inverse_aggregation_theorem"],
        "PROVED",
    ),
    ("h1_repair_true", ["h1_type_separation", "h1_E_repair"], True),
    (
        "active_support_closed",
        ["h1_type_separation", "active_support_root_A"],
        "PROVED",
    ),
    (
        "representation_closed",
        ["h1_type_separation", "canonical_minimal_root_M"],
        "PROVED",
    ),
    (
        "architecture_closed",
        ["gates", 14, "status"],
        "CLOSED",
    ),
    (
        "structural_reopen_pass",
        ["gates", 16, "status"],
        "PASS",
    ),
    (
        "mathematical_reopen_true",
        ["claim_firewall", "mathematical_reopen"],
        True,
    ),
    (
        "positive_sigma_true",
        ["claim_firewall", "positive_sigma_obtained"],
        True,
    ),
    (
        "L2_promoted",
        ["claim_firewall", "L2_result"],
        "POSITIVE",
    ),
    (
        "source_hash_rebound",
        ["source_locks", 0, "canonical_sha256"],
        "0" * 64,
    ),
    (
        "bad_endpoint_parent_stopped",
        ["route_state", "bad_endpoint_O161_parent"],
        "STOPPED",
    ),
    (
        "global_architecture_stopped",
        ["route_state", "global_architecture"],
        "STOPPED",
    ),
    (
        "tpc206_auto_authorized",
        ["decision", "tpc206_authorized"],
        True,
    ),
    (
        "batch_stop_removed",
        ["decision", "batch_stop"],
        "CONTINUE_AUTOMATICALLY",
    ),
]


def build_base_mutation_registry(
    payload: dict[str, Any], payload_schema: dict[str, Any]
) -> list[dict[str, Any]]:
    rows = []
    for name, mutate in BASE_MUTATIONS:
        mutated = mutate(copy.deepcopy(payload))
        rows.append(
            {
                "name": name,
                "payload_changed": not strict_same(mutated, payload),
                "rejected_by_active_schema": not schema_accepts(
                    payload_schema, mutated
                ),
            }
        )
    require(all(row["payload_changed"] for row in rows), "BASE_MUTATION_NOOP")
    require(
        all(row["rejected_by_active_schema"] for row in rows),
        "BASE_MUTATION_ACCEPTED",
    )
    return rows


def build_semantic_mutation_registry(
    payload: dict[str, Any],
) -> list[dict[str, Any]]:
    rows = []
    for name, path, replacement in SEMANTIC_MUTATIONS:
        mutated = set_path(payload, path, replacement)
        regenerated = exact_schema(mutated, f"mutation-{name}.schema.json")
        rejected = False
        try:
            semantic_result(mutated)
        except (RuntimeError, KeyError, TypeError, ValueError):
            rejected = True
        rows.append(
            {
                "name": name,
                "payload_changed": not strict_same(mutated, payload),
                "regenerated_schema_accepts": schema_accepts(
                    regenerated, mutated
                ),
                "semantic_checker_rejected": rejected,
            }
        )
    require(all(row["payload_changed"] for row in rows), "SEMANTIC_MUTATION_NOOP")
    require(
        all(row["regenerated_schema_accepts"] for row in rows),
        "REGENERATED_SCHEMA_REJECTED_FIXTURE",
    )
    require(
        all(row["semantic_checker_rejected"] for row in rows),
        "SEMANTIC_MUTATION_ACCEPTED",
    )
    return rows


def build_l0_fixture_payload(payload: dict[str, Any]) -> dict[str, Any]:
    return {
        "schema": "tpc-205-pair-native-l0-interface-v1",
        "paper": 205,
        "allowed_evidence_modes": [
            "ROW_ONLY",
            "DERIVED_L0_ONLY",
        ],
        "production_mode_allowed": False,
        "fixtures": copy.deepcopy(payload["fixtures"]),
        "claim_firewall": {
            "production_occurrence": False,
            "asymptotic_evidence": False,
            "schema_acceptance_is_theorem_evidence": False,
        },
    }


def build_audit(
    payload: dict[str, Any],
    payload_schema: dict[str, Any],
    l0_payload: dict[str, Any],
    l0_schema: dict[str, Any],
) -> dict[str, Any]:
    result = semantic_result(payload)
    return {
        "schema": "tpc-205-pair-native-registry-interface-audit-v1",
        "paper": 205,
        "payload_sha256": sha256_value(payload),
        "payload_schema_sha256": sha256_value(payload_schema),
        "l0_fixture_sha256": sha256_value(l0_payload),
        "l0_schema_sha256": sha256_value(l0_schema),
        "checks": {
            "authorization_scope_exact": True,
            "authorization_not_theorem_evidence": True,
            "ordered_pair_domain_frozen": True,
            "displayed_B_alias_boundary_frozen": True,
            "no_implicit_conjugation": True,
            "supplied_omega_inverse_only": True,
            "tpc93_physical_support_premise_frozen": True,
            "pair_to_omega_crosswalk_fail": True,
            "row_only_candidate_not_promoted": True,
            "derived_L0_child_not_promoted": True,
            "declared_registry_corpus_production_pair_row_count_zero": True,
            "normalization_string_not_scalar": True,
            "loss_rows_retain_source_hypotheses_only": True,
            "hard_remainder_uncontrolled": True,
            "return_slots_missing": True,
            "pair_and_H1_relation_types_distinct": True,
            "H1_E_repair_false": True,
            "A_and_M_roots_not_testable": True,
            "architecture_reroute_open": True,
            "pair_native_triggers_fail": True,
            "endpoint_credit_zero": True,
            "strict_one_over_400_unpaid": True,
            "L2_none": True,
            "pair_stop_scoped": True,
            "L0_interface_rejects_production_mode": True,
        },
        "finite_check_result": result,
        "base_mutation_registry": build_base_mutation_registry(
            payload, payload_schema
        ),
        "semantic_mutation_registry": build_semantic_mutation_registry(payload),
        "all_checks_pass": True,
    }


def expected_artifacts() -> tuple[
    dict[str, Any],
    dict[str, Any],
    dict[str, Any],
    dict[str, Any],
    dict[str, Any],
    dict[str, Any],
]:
    payload = build_payload()
    payload_schema = exact_schema(
        payload, "tpc205-pair-native-registry-interface-v1.schema.json"
    )
    l0_payload = build_l0_fixture_payload(payload)
    l0_schema = exact_schema(
        l0_payload, "tpc205-pair-native-l0-interface-v1.schema.json"
    )
    audit = build_audit(payload, payload_schema, l0_payload, l0_schema)
    audit_schema = exact_schema(
        audit, "tpc205-pair-native-registry-interface-audit-v1.schema.json"
    )
    return payload, audit, payload_schema, audit_schema, l0_payload, l0_schema


def materialize() -> None:
    (
        payload,
        audit,
        payload_schema,
        audit_schema,
        l0_payload,
        l0_schema,
    ) = expected_artifacts()
    PAYLOAD_PATH.write_text(canonical(payload), encoding="utf-8", newline="\n")
    AUDIT_PATH.write_text(canonical(audit), encoding="utf-8", newline="\n")
    PAYLOAD_SCHEMA_PATH.parent.mkdir(parents=True, exist_ok=True)
    PAYLOAD_SCHEMA_PATH.write_text(
        canonical(payload_schema), encoding="utf-8", newline="\n"
    )
    AUDIT_SCHEMA_PATH.write_text(
        canonical(audit_schema), encoding="utf-8", newline="\n"
    )
    L0_FIXTURE_PATH.parent.mkdir(parents=True, exist_ok=True)
    L0_FIXTURE_PATH.write_text(
        canonical(l0_payload), encoding="utf-8", newline="\n"
    )
    L0_SCHEMA_PATH.write_text(canonical(l0_schema), encoding="utf-8", newline="\n")


def verify_active_artifacts() -> dict[str, Any]:
    (
        payload,
        audit,
        payload_schema,
        audit_schema,
        l0_payload,
        l0_schema,
    ) = expected_artifacts()
    disk_payload = load_json(PAYLOAD_PATH, canonical_bytes=True)
    disk_audit = load_json(AUDIT_PATH, canonical_bytes=True)
    disk_payload_schema = load_json(PAYLOAD_SCHEMA_PATH, canonical_bytes=True)
    disk_audit_schema = load_json(AUDIT_SCHEMA_PATH, canonical_bytes=True)
    disk_l0_payload = load_json(L0_FIXTURE_PATH, canonical_bytes=True)
    disk_l0_schema = load_json(L0_SCHEMA_PATH, canonical_bytes=True)
    strict_equal(disk_payload, payload, "payload")
    strict_equal(disk_audit, audit, "audit")
    strict_equal(disk_payload_schema, payload_schema, "payload_schema")
    strict_equal(disk_audit_schema, audit_schema, "audit_schema")
    strict_equal(disk_l0_payload, l0_payload, "l0_payload")
    strict_equal(disk_l0_schema, l0_schema, "l0_schema")
    require(
        schema_accepts(disk_payload_schema, disk_payload),
        "PAYLOAD_SCHEMA_REJECTED",
    )
    require(
        schema_accepts(disk_audit_schema, disk_audit),
        "AUDIT_SCHEMA_REJECTED",
    )
    require(
        schema_accepts(disk_l0_schema, disk_l0_payload),
        "L0_SCHEMA_REJECTED",
    )
    require(
        disk_l0_payload["production_mode_allowed"] is False,
        "L0_PRODUCTION_MODE",
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
            row["semantic_checker_rejected"]
            for row in disk_audit["semantic_mutation_registry"]
        ),
        "DISK_SEMANTIC_MUTATION_FAILURE",
    )
    return {
        **semantic_result(disk_payload),
        "base_mutations_rejected": len(BASE_MUTATIONS),
        "semantic_mutations_rejected": len(SEMANTIC_MUTATIONS),
        "L0_fixtures_verified": len(disk_l0_payload["fixtures"]),
    }


def manifest_semantic_summary() -> dict[str, Any]:
    return {
        "contract": "TPC205_PAIR_NATIVE_REGISTRY_INTERFACE_V1",
        "manifest_trust": (
            "REPOSITORY_PIN_REQUIRES_GIT_REVIEW_NOT_EXTERNAL_SIGNATURE"
        ),
        "source_locks": len(SOURCE_SPECS),
        "required_registry_fields": 42,
        "production_pair_records": 0,
        "production_pair_record_scope": (
            "DECLARED_TPC205_REGISTRY_SOURCE_LOCK_CORPUS_ONLY"
        ),
        "L0_fixture_records": 2,
        "base_mutations": len(BASE_MUTATIONS),
        "semantic_mutations": len(SEMANTIC_MUTATIONS),
        "first_missing": FIRST_MISSING,
        "verdict": VERDICT,
    }


def build_manifest() -> dict[str, Any]:
    for relative in ACTIVE_ARTIFACTS:
        require((REPO / relative).is_file(), f"MANIFEST_MISSING:{relative}")
    return {
        "schema": "tpc205-certificate-manifest-v1",
        "mode": "MANUALLY_REFRESHED_NOT_GENERATOR_SIGNED",
        "artifacts": [
            {"path": relative, "raw_sha256": raw_sha256(REPO / relative)}
            for relative in ACTIVE_ARTIFACTS
        ],
        "semantic_contract": manifest_semantic_summary(),
    }


def verify_manifest() -> dict[str, Any]:
    require(MANIFEST_PATH.is_file(), "TPC205_MANIFEST_MISSING")
    manifest = load_json(MANIFEST_PATH, canonical_bytes=True)
    require(
        set(manifest) == {"schema", "mode", "artifacts", "semantic_contract"},
        "MANIFEST_KEYS",
    )
    require(
        manifest["schema"] == "tpc205-certificate-manifest-v1",
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
        "MANIFEST_ALLOWLIST",
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
            "TPC-205 validation fails closed"
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
                "paper": 205,
                "verdict": VERDICT,
                "certificate": result,
                "manifest": manifest,
                "refreshed": args.refresh_manifest,
            },
            sort_keys=True,
        )
    )


if __name__ == "__main__":
    main()
