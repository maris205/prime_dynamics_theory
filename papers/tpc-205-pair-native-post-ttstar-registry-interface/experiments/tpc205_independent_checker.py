#!/usr/bin/env python3
"""Independent read-only verifier for the finite TPC-205 contract.

This module imports neither the builder nor the authoritative materializer.
It independently freezes the source paths and hashes, relation and gate
types, archive identities, finite arithmetic, claim firewall, exact schemas,
mutation names, and manifest allowlist.
"""

from __future__ import annotations

import argparse
import copy
import hashlib
import json
from math import gcd
from pathlib import Path
from typing import Any


HERE = Path(__file__).resolve().parent
PAPER = HERE.parent
REPO = PAPER.parents[1]
PAYLOAD_PATH = HERE / "tpc205_pair_native_registry_interface.json"
AUDIT_PATH = HERE / "tpc205_pair_native_registry_interface_audit.json"
PAYLOAD_SCHEMA_PATH = (
    PAPER / "schemas" / "tpc205-pair-native-registry-interface-v1.schema.json"
)
AUDIT_SCHEMA_PATH = (
    PAPER
    / "schemas"
    / "tpc205-pair-native-registry-interface-audit-v1.schema.json"
)
L0_PATH = PAPER / "samples" / "tpc205_pair_native_l0_fixtures.json"
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
SOURCE_SNAPSHOT_COMMIT = "88ead9383270ab40a6350616554d519ede6f0782"

PAYLOAD_KEYS = {
    "authorization",
    "claim_firewall",
    "classification",
    "decision",
    "first_missing",
    "first_missing_subgates",
    "fixtures",
    "formula_contract",
    "gates",
    "h1_type_separation",
    "loss_ledger",
    "normalization_contract",
    "paper",
    "registry_contract",
    "relation_types",
    "route_state",
    "schema",
    "source_child_contract",
    "source_locks",
    "source_snapshot_commit",
    "stop_scoped",
    "summary_counts",
    "theorem_status",
    "verdict",
}

AUDIT_KEYS = {
    "all_checks_pass",
    "base_mutation_registry",
    "checks",
    "finite_check_result",
    "l0_fixture_sha256",
    "l0_schema_sha256",
    "paper",
    "payload_schema_sha256",
    "payload_sha256",
    "schema",
    "semantic_mutation_registry",
}

EXPECTED_SOURCES = [
    (
        "TPC18.opened_d",
        (
            "papers/tpc-18-mobius-tail-determinant-dispersion/"
            "sections/opened-d-dispersion.tex"
        ),
        "36249c8baa2495034acabeb0ba7d5a5f665f2d536b605e9691e2e420e399f1f8",
        [
            r"\cC_D^{\mathrm{off}}",
            r"\sum_{\substack{\alpha_1\ne\alpha_2}}",
            r"B_{\alpha_1}(j)B_{\alpha_2}(j).",
            r"Here and below the prime and support restrictions",
        ],
    ),
    (
        "TPC18.stopping",
        (
            "papers/tpc-18-mobius-tail-determinant-dispersion/"
            "sections/stopping-closure.tex"
        ),
        "5ff68d4207ada5fe2bea819716aaf095e2742fc63eef4a7d9f7573735df65ee4",
        [
            r"There are $O(\log X)$ slices",
            r"Sum the $O(\log X)$ divisor slices",
            r"|\cC_D^{\mathrm{gen}}|",
        ],
    ),
    (
        "TPC25.provenance",
        "papers/tpc-25-zero-before-separation/sections/provenance.tex",
        "21382acf28d8fc3d3cff499cd767075206ba9e2d24913e95414138b4317f0f00",
        [
            r"\gamma_\alpha",
            r"\mathfrak m(\alpha_1,\alpha_2)=0",
            r"The two sides of a bilinear packet",
        ],
    ),
    (
        "TPC25.zero_first",
        "papers/tpc-25-zero-before-separation/sections/zero-first.tex",
        "4fd2e42a8b95e61c52c77cb8bd0bfa101eacaf588d9b8610cacc3ac2dfaaf25b",
        [
            r"\mathcal Z^0_{S,T}",
            r"X^{-s+\kappa+o(1)}",
            r"For a Hermitian convention the second factor is conjugated",
        ],
    ),
    (
        "TPC32.physical_shell",
        (
            "papers/tpc-32-matched-cutoff-frequency-gate/"
            "sections/physical-matched-shell.tex"
        ),
        "b2c3b2b0312db64af5b3151402be929c1671429c1376fe24454a78b4c60d90bd",
        [
            r"\mathfrak A_{\alpha,\gamma}(j)",
            r"\cK^{\mathrm{sh}}_{\alpha,\gamma}(j)",
            r"=C_m(j)\mathsf H_{n;T,U_0}(j)",
            r"No separability of the generic",
        ],
    ),
    (
        "TPC32.content",
        (
            "papers/tpc-32-matched-cutoff-frequency-gate/"
            "sections/canonical-content-factorization.tex"
        ),
        "c3c826a59e9032d0836dd962cd2654962b61134b9ed8718b7529d2c5fd1a4772",
        [
            "No complex conjugation is implicit.",
            r"\gamma_\alpha^{(1)}\gamma_\gamma^{(2)}",
        ],
    ),
    (
        "TPC32.certificate",
        (
            "papers/tpc-32-matched-cutoff-frequency-gate/"
            "experiments/tpc32_certificate.json"
        ),
        "77ac56e2f4f3543224876e8a0374564c81c1b4a9f17800f18ca5249e12954d36",
        [
            '"primitive_witness"',
            '"rows"',
            '"targets"',
            '"primitive_finite_witness_is_twin_prime_asymptotic_evidence": false',
        ],
    ),
    (
        "TPC93.decorated_export",
        (
            "papers/tpc-93-literal-low-window-affine-export/"
            "sections/decorated-affine-export.tex"
        ),
        "c0d45f64a100bb21ac67cce124c46bc2ebfd3740810af1355fb21420d4262f03",
        [
            r"\omega=(L,\alpha,\gamma,j,u)",
            r"\sum_{v\mid d,e}\lambda_{G_X^{\rm row}}(v)",
            r"no new fiber normalization is introduced",
            r"The labels \(L\) and \(R\) form a disjoint union",
        ],
    ),
    (
        "TPC143.main",
        "papers/tpc-143-frontier-occurrence-lift-contract/main.tex",
        "4965d5ad640999fda1be2a75b82dabdbb2cef6ad17df770fa2e53fc08b2e9627",
        [
            r"L_X:\mathbb C^{\Ccut}\longrightarrow\mathbb C^{\Occ}",
            "signed or",
            "complex.",
            r"\one_{\Occ}^{T}L_X=\one_{\Ccut}^{T}",
        ],
    ),
    (
        "TPC174.main",
        "papers/tpc-174-local-occurrence-edge-witness-schema/main.tex",
        "912398392187568bc2f77f6c0f960f481286beb55f6c4a43ec0a0a4300ebd448",
        [
            "exact nonzero rational weight",
            "exact column sum one",
            "SYNTHETIC\\_L0\\_ONLY",
        ],
    ),
    (
        "TPC179.main",
        (
            "papers/tpc-179-h1-structural-corpus-exhaustion-integration/"
            "main.tex"
        ),
        "ef3611d57741448950da204746c8e6bc3125a97a82d6eb1709dd25cb25a258be",
        [
            r"\mathcal B_{H1}=\{E,A,M\}",
            r"\texttt{current\_verdict}&=\mathsf{NOT\_TESTABLE}",
            "none suppresses another",
        ],
    ),
    (
        "TPC133.rows",
        (
            "papers/tpc-133-executable-native-entrance/"
            "samples/tpc133_native_atoms.jsonl"
        ),
        "a1956cf182ad219da10d850de7c7e57de69b8c287fb698e44faa5c795c3840a8",
        [
            "e550d2d7be48d85076919a8adf86ba446f88f75b404df48c0483d3cf27b59369",
            "633e20ac5a83d425471be3ba095df10a1635c3f45ce5cac6def9d5ba936152d9",
        ],
    ),
    (
        "TPC136.cuts",
        (
            "papers/tpc-136-complete-native-cut-archive/"
            "samples/tpc136_cut_paths.jsonl"
        ),
        "a4be1c1b41221b585e3abbf67294b0f784d556cd0209e6ce87ccb905af285f18",
        [
            "2eef9d8670c23ffc10b2a9cab0d488b0908293cfdb482667da824e702a1347cc",
            "cdc0f7363ab88106ce65bb46da800c05c3fba2b391d9490d7b2ca8bab8c816db",
        ],
    ),
    (
        "TPC204.payload",
        (
            "papers/tpc-204-source-locked-production-registry-crosswalk/"
            "experiments/tpc204_source_locked_production_registry_crosswalk.json"
        ),
        "3d6e7aab3d9e165cc1d6f822f7146feb0d0fddbc1e976ed4312739b0418f4ff2",
        [
            '"complete_crosswalk_count": 0',
            '"first_common_missing_gate_id": "NAMED_PRODUCTION_ATOM"',
            '"reopen_trigger_passed": false',
        ],
    ),
    (
        "TPC18.tail_interface",
        (
            "papers/tpc-18-mobius-tail-determinant-dispersion/"
            "sections/tail-interface.tex"
        ),
        "5f50b44fde7e672b28aeb45b1b53e95f90c26bb8d35052081fa3a7e419712389",
        [
            r"\label{eq:source-power-error}",
            r"XL^{-1/2}X^\eps.",
            "In particular this has arbitrary logarithmic saving",
        ],
    ),
    (
        "TPC25.one_sided_closure",
        (
            "papers/tpc-25-zero-before-separation/"
            "sections/one-sided-closure.tex"
        ),
        "aeaf0268d73ce0fbb95777238d2b4b2ccd417d53d19707c96332e5bc3a795c9e",
        [
            r"\label{eq:tpc25-zero-in-closure}",
            r"after all dyadic and divisor multiplicities.  The global principal",
            r"conductor cell is \(O(Q^2X^\eps)\)",
            r"\(O(JQ^2L^{-1}X^\eps)\)",
            r"Fixed bounded-overlap",
        ],
    ),
    (
        "TPC93.row_window",
        (
            "papers/tpc-93-literal-low-window-affine-export/"
            "sections/row-window.tex"
        ),
        "aaaa038907b505bd85d7cbf318bd3047bc3c37b2316243872a5a48824df06ea6",
        [
            r"\label{eq:row-tail-return}",
            r"X^{o(1)}N_{0,X}R^{1/2-K}.",
            r"not a maximum over \(r\)",
        ],
    ),
]

EXPECTED_RELATIONS = [
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

EXPECTED_GATES = [
    ("ORDERED_POST_TTSTAR_PAIR_DOMAIN", "PASS_FORMULA"),
    ("TPC18_DISPLAYED_PAIR_COEFFICIENT_WITH_B_ALIASES", "PASS_FORMULA"),
    ("SECOND_ROW_GAMMA_FROM_TTSTAR_EXPANSION", "PASS_FORMULA"),
    ("U_FROM_SUPPLIED_TPC32_93_PARENT_POLARIZATION", "PASS_FORMULA"),
    (
        "TPC93_SOURCE_CHILD_REINDEXING",
        "PASS_L1_ON_SUPPLIED_RETAINED_OMEGA",
    ),
    ("CONCRETE_DUAL_ARCHIVED_ROW_CANDIDATE", "PASS_ROW_ONLY"),
    ("TPC32_TPC93_DERIVED_AFFINE_CHILD", "PASS_DERIVED_L0_ONLY"),
    ("ACTIVE_PRODUCTION_PAIR_OCCURRENCE", "NOT_TESTABLE"),
    ("FULL_LITERAL_PAIR_COEFFICIENT_MATERIALIZATION", "NOT_TESTABLE"),
    ("PAIR_COEFFICIENT_MATERIALIZATION_AND_NONZERO", "NOT_TESTABLE"),
    ("SOURCE_LOCKED_PAIR_TO_OMEGA_CROSSWALK", "FAIL"),
    ("NU_X_NORMALIZED_RETURN_TO_H1", "FAIL"),
    ("H1_E_REPAIR", "FAIL"),
    ("PAIR_NATIVE_FORMULA_GATE", "PASS"),
    ("PAIR_NATIVE_ARCHITECTURE_REROUTE_CANDIDATE", "OPEN"),
    ("PAIR_NATIVE_PRODUCTION_REOPEN_TRIGGER", "FAIL"),
    ("PAIR_NATIVE_STRUCTURAL_REOPEN_TRIGGER", "FAIL"),
    ("TPC32_MATCHED_SHELL_AND_POLARIZATION", "PASS_L1_FORMULA"),
    ("TPC18_PAIR_TO_TPC32_LITERAL_PARENT_CROSSWALK", "NOT_TESTABLE"),
    (
        "TPC93_PROJECTOR_WEIGHTED_REASSEMBLY",
        "PASS_L1_ON_SUPPLIED_RETAINED_OMEGA_AND_TPC93_PHYSICAL_SUPPORT",
    ),
    ("TTSTAR_PAIR_VS_H1_LINEAR_EDGE_TYPE_SEPARATION", "PASS_L1_STRUCTURAL"),
    ("PAIR_NATIVE_ACTIVE_SUPPORT_CERTIFICATE", "NOT_TESTABLE"),
    ("PAIR_NATIVE_CANONICAL_MINIMAL_REPRESENTATION", "NOT_TESTABLE"),
]

EXPECTED_LOSS_IDS = [
    "prime_power_error",
    "dyadic_D_partition",
    "cauchy_factor",
    "diagonal",
    "same_rows",
    "near_rows",
    "large_row_gcd",
    "generic_remainder",
    "tpc25_zero",
    "tpc25_principal",
    "tpc25_drift",
    "tpc25_polylog",
    "tpc32_drift",
    "large_content",
    "tpc93_fourier_tail",
    "square_root_return",
    "full_block_endpoint_reassembly",
]

EXPECTED_STOP_SCOPED = [
    "TPC193_DECLARED_CANDIDATE_MECHANISM_CORPUS_V1=STOP_SCOPED",
    "TPC204_DECLARED_PLAUSIBLE_PRODUCTION_CROSSWALK_CORPUS_V1=STOP_SCOPED",
    "TPC18_25_32_93_194_SINGLE_CUT_OCCURRENCE_COMPOSITE_V1=STOP_SCOPED",
    "TPC18_TPC93_POST_TTSTAR_PAIR_DIRECT_COMPOSITION_V1=STOP_SCOPED",
]

EXPECTED_AUTHORIZATION = {
    "scope": AUTHORIZATION_SCOPE,
    "user_authorized": True,
    "authorization_is_theorem_evidence": False,
}

EXPECTED_FORMULA_CONTRACT = {
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
    "matched_shell": "K_sh(alpha,gamma,j)=C_m(j)H_n(j)+H_m(j)C_n(j)",
    "left_u_rule": "T<u<=U0 and u|N_alpha(j)",
    "right_u_rule": "T<u<=U0 and u|N_gamma(j)",
    "pair_to_omega_bridge": "MISSING",
}

EXPECTED_SOURCE_CHILD_CONTRACT = {
    "supplied_source_atom": "omega=(L/R,alpha,gamma,j,u)",
    "projector_identity": (
        "sum_{v|d,e} lambda_{G_X^row}(v)"
        "=1_{gcd(d,e)<=G_X^row}"
    ),
    "single_child_restores_source": False,
    "weighted_child_sum_restores": "actual-row-gcd-masked source coefficient",
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

EXPECTED_REGISTRY_CONTRACT = {
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

EXPECTED_NORMALIZATION_CONTRACT = {
    "tpc18_object": "UNNORMALIZED_T_D",
    "archived_nu_X_status": "SCOPE_STRING_NOT_NUMERIC_SCALAR",
    "conditional_scalar_identity": (
        "|c_X T_D|^2 <= C_W |c_X|^2 J(E_D+C_D^off)"
    ),
    "global_normalization_return": "MISSING_UNSUPPLIED",
}

EXPECTED_LOSS_LEDGER = [
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

EXPECTED_H1_TYPE_SEPARATION = {
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

EXPECTED_CLAIM_FIREWALL = {
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

EXPECTED_ROUTE_STATE = {
    "H1_architecture": "OPEN",
    "bad_endpoint_O161_parent": "OPEN",
    "direct_twist_O161_parent": "OPEN",
    "global_architecture": "OPEN",
    "pair_native_architecture_reroute": "OPEN",
}

EXPECTED_DECISION = {
    "batch_stop": "USER_CONFIRMATION_REQUIRED",
    "next_paper": None,
    "tpc206_authorized": False,
}

EXPECTED_SUMMARY_COUNTS = {
    "source_locks": 17,
    "relation_types": 4,
    "required_registry_fields": 42,
    "fixtures": 2,
    "production_pair_records": 0,
    "loss_ledger_rows": 17,
    "gates": 23,
}

EXPECTED_AUDIT_CHECKS = {
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
}

EXPECTED_MANIFEST_CONTRACT = {
    "contract": "TPC205_PAIR_NATIVE_REGISTRY_INTERFACE_V1",
    "manifest_trust": (
        "REPOSITORY_PIN_REQUIRES_GIT_REVIEW_NOT_EXTERNAL_SIGNATURE"
    ),
    "source_locks": 17,
    "required_registry_fields": 42,
    "production_pair_records": 0,
    "production_pair_record_scope": (
        "DECLARED_TPC205_REGISTRY_SOURCE_LOCK_CORPUS_ONLY"
    ),
    "L0_fixture_records": 2,
    "base_mutations": 12,
    "semantic_mutations": 37,
    "first_missing": FIRST_MISSING,
    "verdict": VERDICT,
}

FROZEN_RAW_SHA256 = {
    (
        "papers/tpc-205-pair-native-post-ttstar-registry-interface/"
        "experiments/tpc205_pair_native_registry_interface.json"
    ): "07b118b69a16587fe1b9239b585ffa65b6772f005d9c719eb5eba3cc488d586d",
    (
        "papers/tpc-205-pair-native-post-ttstar-registry-interface/"
        "experiments/tpc205_pair_native_registry_interface_audit.json"
    ): "0da38a17912e493b253ecfa669bdd45c4280ee5b5456342929b4535dc61ebcd9",
    (
        "papers/tpc-205-pair-native-post-ttstar-registry-interface/"
        "schemas/tpc205-pair-native-registry-interface-v1.schema.json"
    ): "6976342d326a4379d623eb6efd365f45ce23aaa11becb15abdb5663eae61d55b",
    (
        "papers/tpc-205-pair-native-post-ttstar-registry-interface/"
        "schemas/tpc205-pair-native-registry-interface-audit-v1.schema.json"
    ): "ca0144f4d2f92a0a055ba0c51d2df8921e5976ea9e4ec5b6082d32673f9f5433",
    (
        "papers/tpc-205-pair-native-post-ttstar-registry-interface/"
        "samples/tpc205_pair_native_l0_fixtures.json"
    ): "57d04e78005a7503b84b4172c7d43d8eea2eeb5bbd930dea7048863297a468de",
    (
        "papers/tpc-205-pair-native-post-ttstar-registry-interface/"
        "schemas/tpc205-pair-native-l0-interface-v1.schema.json"
    ): "4f591b96cdc5d4c3aeb8faabcbafb540f9fddb1126019c3bb9f4f0fc9e41f3f4",
}

BASE_MUTATION_NAMES = [
    "top_extra",
    "top_missing_schema",
    "paper_bool",
    "authorization_extra",
    "relation_delete",
    "coefficient_truncate",
    "fixture_extra_field",
    "loss_extra_row",
    "gate_removed",
    "source_anchor_count_bool",
    "first_missing_list",
    "firewall_L2_bool",
]

SEMANTIC_MUTATION_NAMES = [
    "authorization_false",
    "authorization_becomes_evidence",
    "classification_drift",
    "verdict_reopened",
    "pair_arity_one",
    "pair_unordered",
    "pair_mislabeled_linear",
    "coefficient_promoted_complete",
    "implicit_conjugation_added",
    "pair_to_omega_bridge_pass",
    "single_child_restores",
    "production_crosswalk_pass",
    "registry_production_row",
    "pair_quotient_allowed",
    "row_candidate_promoted",
    "row_candidate_nonzero",
    "derived_child_directly_certified",
    "derived_child_asymptotic",
    "nu_X_promoted_scalar",
    "global_normalization_supplied",
    "hard_remainder_controlled",
    "square_root_return_supplied",
    "first_missing_changed",
    "cut_inverse_theorem_invented",
    "h1_repair_true",
    "active_support_closed",
    "representation_closed",
    "architecture_closed",
    "structural_reopen_pass",
    "mathematical_reopen_true",
    "positive_sigma_true",
    "L2_promoted",
    "source_hash_rebound",
    "bad_endpoint_parent_stopped",
    "global_architecture_stopped",
    "tpc206_auto_authorized",
    "batch_stop_removed",
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
    return json.dumps(value, ensure_ascii=False, indent=2, sort_keys=True) + "\n"


def compact_canonical(value: Any) -> bytes:
    return json.dumps(
        value, ensure_ascii=False, separators=(",", ":"), sort_keys=True
    ).encode("utf-8")


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def sha256_value(value: Any) -> str:
    return sha256_bytes(canonical(value).encode("utf-8"))


def raw_sha256(path: Path) -> str:
    return sha256_bytes(path.read_bytes())


def canonical_text_hash(path: Path) -> str:
    text = path.read_text(encoding="utf-8")
    data = text.replace("\r\n", "\n").replace("\r", "\n").encode("utf-8")
    return sha256_bytes(data)


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


def reject_constant(token: str) -> None:
    raise ValueError(f"non-finite JSON constant: {token}")


def unique_object(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
    result: dict[str, Any] = {}
    for key, value in pairs:
        if key in result:
            raise ValueError(f"duplicate JSON key: {key}")
        result[key] = value
    return result


def load_json(path: Path, canonical_bytes: bool = True) -> Any:
    raw = path.read_bytes()
    value = json.loads(
        raw.decode("utf-8"),
        object_pairs_hook=unique_object,
        parse_constant=reject_constant,
    )
    if canonical_bytes:
        require(raw == canonical(value).encode("utf-8"), f"NONCANONICAL:{path}")
    return value


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
        raise TypeError(f"unsupported exact-schema type: {type(item)!r}")

    result = node(value)
    result["$schema"] = SCHEMA_URI
    result["$id"] = schema_id
    return result


def schema_accepts(schema: dict[str, Any], value: Any) -> bool:
    kind = schema.get("type")
    expected = {
        "object": dict,
        "array": list,
        "null": type(None),
        "boolean": bool,
        "integer": int,
        "string": str,
    }
    if kind not in expected or type(value) is not expected[kind]:
        return False
    if "const" in schema and not strict_same(value, schema["const"]):
        return False
    if kind == "object":
        if schema.get("additionalProperties") is not False:
            return False
        if set(value) != set(schema["required"]):
            return False
        return all(
            schema_accepts(schema["properties"][key], value[key])
            for key in value
        )
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


def safe_repo_path(relative: str) -> Path:
    require(type(relative) is str, "SOURCE_PATH_TYPE")
    path = (REPO / relative).resolve()
    root = REPO.resolve()
    require(path == root or root in path.parents, f"SOURCE_PATH_ESCAPE:{relative}")
    require(path.is_file(), f"SOURCE_PATH_MISSING:{relative}")
    return path


def verify_source_locks(payload: dict[str, Any]) -> None:
    locks = payload["source_locks"]
    require(type(locks) is list, "SOURCE_LOCK_LIST")
    require(len(locks) == len(EXPECTED_SOURCES), "SOURCE_LOCK_COUNT")
    for lock, (source_id, relative, digest, anchors) in zip(
        locks, EXPECTED_SOURCES
    ):
        require(
            set(lock)
            == {
                "id",
                "path",
                "hash_mode",
                "hash_semantics",
                "canonical_sha256",
                "required_anchors",
            },
            f"SOURCE_LOCK_KEYS:{source_id}",
        )
        require(lock["id"] == source_id, f"SOURCE_ID:{source_id}")
        require(lock["path"] == relative, f"SOURCE_PATH:{source_id}")
        require(lock["hash_mode"] == HASH_MODE, f"SOURCE_HASH_MODE:{source_id}")
        require(
            lock["hash_semantics"] == "INTEGRITY_ONLY",
            f"SOURCE_HASH_SEMANTICS:{source_id}",
        )
        require(
            lock["canonical_sha256"] == digest,
            f"SOURCE_DECLARED_HASH:{source_id}",
        )
        require(lock["required_anchors"] == anchors, f"SOURCE_ANCHORS:{source_id}")
        path = safe_repo_path(relative)
        require(canonical_text_hash(path) == digest, f"SOURCE_HASH:{source_id}")
        text = path.read_text(encoding="utf-8").replace("\r\n", "\n")
        for anchor in anchors:
            require(anchor in text, f"SOURCE_ANCHOR:{source_id}:{anchor}")


def select_jsonl_unique(path: Path, key: str, value: str) -> tuple[dict[str, Any], int]:
    matches: list[tuple[dict[str, Any], int]] = []
    for line_number, line in enumerate(
        path.read_text(encoding="utf-8").splitlines(), start=1
    ):
        row = json.loads(
            line,
            object_pairs_hook=unique_object,
            parse_constant=reject_constant,
        )
        if type(row) is dict and row.get(key) == value:
            matches.append((row, line_number))
    require(len(matches) == 1, f"JSONL_ID_NOT_UNIQUE:{key}:{value}")
    return matches[0]


def verify_record_integrity(record: dict[str, Any]) -> None:
    require(type(record.get("integrity_sha256")) is str, "INTEGRITY_FIELD")
    body = {key: value for key, value in record.items() if key != "integrity_sha256"}
    require(
        sha256_bytes(compact_canonical(body)) == record["integrity_sha256"],
        f"INTEGRITY_MISMATCH:{record['integrity_sha256']}",
    )


def build_expected_fixtures() -> list[dict[str, Any]]:
    row_path = safe_repo_path(
        "papers/tpc-133-executable-native-entrance/samples/"
        "tpc133_native_atoms.jsonl"
    )
    cut_path = safe_repo_path(
        "papers/tpc-136-complete-native-cut-archive/samples/"
        "tpc136_cut_paths.jsonl"
    )
    row_ids = [
        "X=512|h0=2|ell=103|k=5|d=1",
        "X=512|h0=2|ell=107|k=5|d=1",
    ]
    cut_ids = [
        "cut|X=512|h0=2|ell=103|k=5|d=1|jL=6|jK=3|D0=0|type=TAIL",
        "cut|X=512|h0=2|ell=107|k=5|d=1|jL=6|jK=3|D0=0|type=TAIL",
    ]
    rows = [select_jsonl_unique(row_path, "native_id", value) for value in row_ids]
    cuts = [select_jsonl_unique(cut_path, "cut_path_id", value) for value in cut_ids]
    require([line for _, line in rows] == [724, 736], "ROW_LINE_DRIFT")
    require([line for _, line in cuts] == [2554, 2602], "CUT_LINE_DRIFT")
    for record, _ in rows + cuts:
        verify_record_integrity(record)
    require(
        [record["integrity_sha256"] for record, _ in rows]
        == [
            "e550d2d7be48d85076919a8adf86ba446f88f75b404df48c0483d3cf27b59369",
            "633e20ac5a83d425471be3ba095df10a1635c3f45ce5cac6def9d5ba936152d9",
        ],
        "ROW_INTEGRITIES",
    )
    require(
        [record["integrity_sha256"] for record, _ in cuts]
        == [
            "2eef9d8670c23ffc10b2a9cab0d488b0908293cfdb482667da824e702a1347cc",
            "cdc0f7363ab88106ce65bb46da800c05c3fba2b391d9490d7b2ca8bab8c816db",
        ],
        "CUT_INTEGRITIES",
    )
    for record, _ in cuts:
        require(record["cut_terminal_type"] == "FRONTIER_UNMAPPED", "CUT_STATUS")
        require(
            record["metadata"]["frontier_reason"] == "NO_TAIL_ROOM",
            "CUT_REASON",
        )
    require(
        [record["native_tuple"] for record, _ in rows]
        == [[103, 5, 1], [107, 5, 1]],
        "ROW_NATIVE_TUPLES",
    )
    require(
        [record["metadata"]["native_tuple"] for record, _ in cuts]
        == [[103, 5, 1], [107, 5, 1]],
        "CUT_NATIVE_TUPLES",
    )

    alpha_ell, gamma_ell, j, h0 = 103, 107, 5, 2
    N_alpha = alpha_ell * j + h0
    N_gamma = gamma_ell * j + h0
    expected_pair = {
        "alpha": [103, 1],
        "gamma": [107, 1],
        "j": 5,
        "N_alpha": N_alpha,
        "N_gamma": N_gamma,
        "gcd_targets": gcd(N_alpha, N_gamma),
        "Delta_sharp": alpha_ell - gamma_ell,
        "ordered_row_determinant": h0 * (alpha_ell - gamma_ell),
    }
    cert = load_json(
        safe_repo_path(
            "papers/tpc-32-matched-cutoff-frequency-gate/"
            "experiments/tpc32_certificate.json"
        ),
        canonical_bytes=False,
    )
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
    require(
        strict_same(
            {key: primitive[key] for key in expected_direct},
            expected_direct,
        ),
        "TPC32_DIRECT_FIXTURE",
    )
    ell, gamma, d, e, j2, h = 59, 71, 1, 1, 1, 2
    u = 61
    sigma = (ell * d * j2 + h) // u
    v, d0 = 1, 0
    t = (d // v - d0) // sigma
    u0 = (ell * j2 * v * d0 + h) // sigma
    D_t = d0 + sigma * t
    U_t = u0 + ell * j2 * v * t
    expected_child = {
        "polarization": "L",
        "alpha": [ell, d],
        "gamma": [gamma, e],
        "j": j2,
        "u": u,
        "sigma": sigma,
        "v": v,
        "d0": d0,
        "t": t,
        "u0": u0,
        "D_t": D_t,
        "U_t": U_t,
        "determinant": sigma * U_t - ell * j2 * v * D_t,
        "projector_weight": 1,
    }
    require(
        expected_child["determinant"] == 2
        and expected_child["D_t"] == 1
        and expected_child["U_t"] == 61,
        "DERIVED_CHILD_ARITHMETIC",
    )

    row_relative = (
        "papers/tpc-133-executable-native-entrance/"
        "samples/tpc133_native_atoms.jsonl"
    )
    cut_relative = (
        "papers/tpc-136-complete-native-cut-archive/"
        "samples/tpc136_cut_paths.jsonl"
    )
    return [
        {
            "id": "DUAL_SOURCE_LOCKED_ROW_PAIR_CANDIDATE",
            "evidence_level": "ROW_ONLY",
            "h0": 2,
            "ordered_pair": expected_pair,
            "row_locators": [
                {
                    "path": row_relative,
                    "line": rows[0][1],
                    "native_id": rows[0][0]["native_id"],
                    "integrity_sha256": rows[0][0]["integrity_sha256"],
                },
                {
                    "path": row_relative,
                    "line": rows[1][1],
                    "native_id": rows[1][0]["native_id"],
                    "integrity_sha256": rows[1][0]["integrity_sha256"],
                },
            ],
            "cut_locators": [
                {
                    "path": cut_relative,
                    "line": cuts[0][1],
                    "cut_path_id": cuts[0][0]["cut_path_id"],
                    "integrity_sha256": cuts[0][0]["integrity_sha256"],
                    "terminal": "FRONTIER_UNMAPPED",
                    "reason": "NO_TAIL_ROOM",
                },
                {
                    "path": cut_relative,
                    "line": cuts[1][1],
                    "cut_path_id": cuts[1][0]["cut_path_id"],
                    "integrity_sha256": cuts[1][0]["integrity_sha256"],
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
            "derived_tpc93_fields": expected_child,
            "child_fields_directly_certified_by_tpc32": False,
            "production_occurrence": False,
            "asymptotic_evidence": False,
        },
    ]


def verify_fixtures(
    payload: dict[str, Any], expected_fixtures: list[dict[str, Any]]
) -> None:
    require(
        strict_same(payload["fixtures"], expected_fixtures),
        "FIXTURE_DEEP_CONTRACT",
    )


def expected_source_locks() -> list[dict[str, Any]]:
    return [
        {
            "id": source_id,
            "path": relative,
            "hash_mode": HASH_MODE,
            "hash_semantics": "INTEGRITY_ONLY",
            "canonical_sha256": digest,
            "required_anchors": anchors,
        }
        for source_id, relative, digest, anchors in EXPECTED_SOURCES
    ]


def build_expected_payload(
    expected_fixtures: list[dict[str, Any]],
) -> dict[str, Any]:
    return {
        "schema": "tpc-205-pair-native-registry-interface-v1",
        "paper": 205,
        "authorization": EXPECTED_AUTHORIZATION,
        "classification": CLASSIFICATION,
        "theorem_status": THEOREM_STATUS,
        "verdict": VERDICT,
        "source_snapshot_commit": SOURCE_SNAPSHOT_COMMIT,
        "source_locks": expected_source_locks(),
        "relation_types": EXPECTED_RELATIONS,
        "formula_contract": EXPECTED_FORMULA_CONTRACT,
        "source_child_contract": EXPECTED_SOURCE_CHILD_CONTRACT,
        "registry_contract": EXPECTED_REGISTRY_CONTRACT,
        "fixtures": expected_fixtures,
        "normalization_contract": EXPECTED_NORMALIZATION_CONTRACT,
        "loss_ledger": EXPECTED_LOSS_LEDGER,
        "first_missing": FIRST_MISSING,
        "first_missing_subgates": [
            (
                "PAIR_NATIVE_POST_TTSTAR_ACTUAL_REGISTRY_WITH_FULL_LITERAL_"
                "SCOPE_AND_COEFFICIENT"
            ),
            "TPC18_PAIR_TO_TPC93_RETAINED_SOURCE_ATOM_THEOREM_CROSSWALK",
        ],
        "h1_type_separation": EXPECTED_H1_TYPE_SEPARATION,
        "gates": [
            {"id": gate_id, "status": status}
            for gate_id, status in EXPECTED_GATES
        ],
        "stop_scoped": EXPECTED_STOP_SCOPED,
        "claim_firewall": EXPECTED_CLAIM_FIREWALL,
        "route_state": EXPECTED_ROUTE_STATE,
        "decision": EXPECTED_DECISION,
        "summary_counts": EXPECTED_SUMMARY_COUNTS,
    }


def build_expected_l0(expected_payload: dict[str, Any]) -> dict[str, Any]:
    return {
        "schema": "tpc-205-pair-native-l0-interface-v1",
        "paper": 205,
        "allowed_evidence_modes": ["ROW_ONLY", "DERIVED_L0_ONLY"],
        "production_mode_allowed": False,
        "fixtures": expected_payload["fixtures"],
        "claim_firewall": {
            "production_occurrence": False,
            "asymptotic_evidence": False,
            "schema_acceptance_is_theorem_evidence": False,
        },
    }


def expected_finite_result() -> dict[str, Any]:
    return {
        "source_locks_verified": 17,
        "relation_types_verified": 4,
        "required_registry_fields": 42,
        "fixtures_verified": 2,
        "production_pair_records": 0,
        "loss_ledger_rows_verified": 17,
        "gates_verified": 23,
        "first_missing": FIRST_MISSING,
        "h1_repair": False,
        "architecture_reroute": "OPEN",
        "mathematical_reopen": False,
    }


def build_expected_audit(
    expected_payload: dict[str, Any],
    expected_payload_schema: dict[str, Any],
    expected_l0: dict[str, Any],
    expected_l0_schema: dict[str, Any],
) -> dict[str, Any]:
    return {
        "schema": "tpc-205-pair-native-registry-interface-audit-v1",
        "paper": 205,
        "payload_sha256": sha256_value(expected_payload),
        "payload_schema_sha256": sha256_value(expected_payload_schema),
        "l0_fixture_sha256": sha256_value(expected_l0),
        "l0_schema_sha256": sha256_value(expected_l0_schema),
        "checks": EXPECTED_AUDIT_CHECKS,
        "finite_check_result": expected_finite_result(),
        "base_mutation_registry": [
            {
                "name": name,
                "payload_changed": True,
                "rejected_by_active_schema": True,
            }
            for name in BASE_MUTATION_NAMES
        ],
        "semantic_mutation_registry": [
            {
                "name": name,
                "payload_changed": True,
                "regenerated_schema_accepts": True,
                "semantic_checker_rejected": True,
            }
            for name in SEMANTIC_MUTATION_NAMES
        ],
        "all_checks_pass": True,
    }


def verify_payload_semantics(
    payload: dict[str, Any], expected_payload: dict[str, Any]
) -> None:
    require(type(payload) is dict and set(payload) == PAYLOAD_KEYS, "PAYLOAD_KEYS")
    require(
        strict_same(payload, expected_payload),
        "PAYLOAD_DEEP_STRICT_CONTRACT",
    )
    verify_source_locks(payload)
    verify_fixtures(payload, expected_payload["fixtures"])


def verify_l0(l0: dict[str, Any], expected_l0: dict[str, Any]) -> None:
    require(strict_same(l0, expected_l0), "L0_DEEP_STRICT_CONTRACT")


def verify_audit(
    audit: dict[str, Any],
    expected_audit: dict[str, Any],
) -> None:
    require(type(audit) is dict and set(audit) == AUDIT_KEYS, "AUDIT_KEYS")
    require(
        strict_same(audit, expected_audit),
        "AUDIT_DEEP_STRICT_CONTRACT",
    )


def verify_frozen_raw_hashes() -> None:
    for relative, digest in FROZEN_RAW_SHA256.items():
        path = safe_repo_path(relative)
        require(raw_sha256(path) == digest, f"FROZEN_RAW_HASH:{relative}")


def verify_manifest() -> None:
    manifest = load_json(MANIFEST_PATH)
    require(
        set(manifest) == {"schema", "mode", "artifacts", "semantic_contract"},
        "MANIFEST_KEYS",
    )
    require(manifest["schema"] == "tpc205-certificate-manifest-v1", "MANIFEST_ID")
    require(
        manifest["mode"] == "MANUALLY_REFRESHED_NOT_GENERATOR_SIGNED",
        "MANIFEST_MODE",
    )
    require(
        strict_same(
            [row["path"] for row in manifest["artifacts"]],
            ACTIVE_ARTIFACTS,
        ),
        "MANIFEST_ALLOWLIST",
    )
    for row in manifest["artifacts"]:
        require(set(row) == {"path", "raw_sha256"}, "MANIFEST_ROW_KEYS")
        path = safe_repo_path(row["path"])
        require(raw_sha256(path) == row["raw_sha256"], f"MANIFEST_HASH:{path}")
    require(
        strict_same(manifest["semantic_contract"], EXPECTED_MANIFEST_CONTRACT),
        "MANIFEST_DEEP_STRICT_CONTRACT",
    )


def verify_strict_type_mutations(expected_payload: dict[str, Any]) -> int:
    mutations = []
    cases = [
        (["paper"], True),
        (["summary_counts", "source_locks"], True),
        (["fixtures", 0, "h0"], True),
        (["fixtures", 0, "production_occurrence"], 0),
        (["decision", "tpc206_authorized"], 0),
        (["claim_firewall", "fixed_atom_credit"], False),
    ]
    for path, replacement in cases:
        mutated = copy.deepcopy(expected_payload)
        cursor = mutated
        for key in path[:-1]:
            cursor = cursor[key]
        cursor[path[-1]] = replacement
        rejected = False
        try:
            verify_payload_semantics(mutated, expected_payload)
        except (RuntimeError, KeyError, TypeError, ValueError):
            rejected = True
        require(rejected, f"STRICT_TYPE_MUTATION_ACCEPTED:{path}")
        mutations.append(path)
    return len(mutations)


def set_path(value: dict[str, Any], path: list[Any], replacement: Any) -> dict[str, Any]:
    result = copy.deepcopy(value)
    cursor: Any = result
    for key in path[:-1]:
        cursor = cursor[key]
    cursor[path[-1]] = replacement
    return result


def verify_base_mutations(
    expected_payload: dict[str, Any],
    expected_payload_schema: dict[str, Any],
) -> int:
    cases = [
        ("top_extra", lambda p: {**p, "unexpected": 1}),
        (
            "top_missing_schema",
            lambda p: {key: value for key, value in p.items() if key != "schema"},
        ),
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
                p["loss_ledger"]
                + [{"id": "invented", "status": "PAID", "value": "0"}],
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
    require([name for name, _ in cases] == BASE_MUTATION_NAMES, "BASE_CASE_NAMES")
    for name, mutate in cases:
        mutated = mutate(copy.deepcopy(expected_payload))
        require(
            not strict_same(mutated, expected_payload),
            f"BASE_MUTATION_NOOP:{name}",
        )
        require(
            not schema_accepts(expected_payload_schema, mutated),
            f"BASE_MUTATION_ACCEPTED:{name}",
        )
    return len(cases)


def semantic_mutation_cases() -> list[tuple[str, list[Any], Any]]:
    return [
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
        ("architecture_closed", ["gates", 14, "status"], "CLOSED"),
        ("structural_reopen_pass", ["gates", 16, "status"], "PASS"),
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
        ("L2_promoted", ["claim_firewall", "L2_result"], "POSITIVE"),
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


def verify_semantic_mutations(expected_payload: dict[str, Any]) -> int:
    cases = semantic_mutation_cases()
    require(
        [name for name, _, _ in cases] == SEMANTIC_MUTATION_NAMES,
        "SEMANTIC_CASE_NAMES",
    )
    for name, path, replacement in cases:
        mutated = set_path(expected_payload, path, replacement)
        require(
            not strict_same(mutated, expected_payload),
            f"SEMANTIC_MUTATION_NOOP:{name}",
        )
        regenerated = exact_schema(mutated, f"mutation-{name}.schema.json")
        require(
            schema_accepts(regenerated, mutated),
            f"SEMANTIC_REGENERATED_SCHEMA_REJECTED:{name}",
        )
        rejected = False
        try:
            verify_payload_semantics(mutated, expected_payload)
        except (RuntimeError, KeyError, TypeError, ValueError):
            rejected = True
        require(rejected, f"SEMANTIC_MUTATION_ACCEPTED:{name}")
    return len(cases)


def verify_l0_hardening_mutation(expected_l0: dict[str, Any]) -> int:
    mutated = set_path(
        expected_l0,
        ["claim_firewall", "production_occurrence"],
        0,
    )
    regenerated = exact_schema(mutated, "mutation-l0-bool-int.schema.json")
    require(schema_accepts(regenerated, mutated), "L0_MUTATION_SCHEMA_REJECTED")
    rejected = False
    try:
        verify_l0(mutated, expected_l0)
    except (RuntimeError, KeyError, TypeError, ValueError):
        rejected = True
    require(rejected, "L0_MUTATION_ACCEPTED")
    return 1


def verify_audit_hardening_mutations(expected_audit: dict[str, Any]) -> int:
    cases = [
        ("empty_checks", ["checks"], {}),
        ("renamed_checks", ["checks"], {"everything": True}),
        (
            "finite_result_extra",
            ["finite_check_result"],
            {**expected_audit["finite_check_result"], "invented": True},
        ),
        (
            "finite_zero_bool",
            ["finite_check_result", "production_pair_records"],
            False,
        ),
        (
            "mutation_row_extra",
            ["base_mutation_registry", 0],
            {**expected_audit["base_mutation_registry"][0], "invented": True},
        ),
    ]
    for name, path, replacement in cases:
        mutated = set_path(expected_audit, path, replacement)
        regenerated = exact_schema(mutated, f"mutation-audit-{name}.schema.json")
        require(
            schema_accepts(regenerated, mutated),
            f"AUDIT_MUTATION_SCHEMA_REJECTED:{name}",
        )
        rejected = False
        try:
            verify_audit(mutated, expected_audit)
        except (RuntimeError, KeyError, TypeError, ValueError):
            rejected = True
        require(rejected, f"AUDIT_MUTATION_ACCEPTED:{name}")
    return len(cases)


def main() -> None:
    if not __debug__:
        raise RuntimeError("TPC-205 independent validation fails closed under -O")
    parser = argparse.ArgumentParser()
    parser.add_argument("--check", action="store_true", required=True)
    parser.parse_args()

    payload = load_json(PAYLOAD_PATH)
    audit = load_json(AUDIT_PATH)
    payload_schema = load_json(PAYLOAD_SCHEMA_PATH)
    audit_schema = load_json(AUDIT_SCHEMA_PATH)
    l0 = load_json(L0_PATH)
    l0_schema = load_json(L0_SCHEMA_PATH)

    expected_fixtures = build_expected_fixtures()
    expected_payload = build_expected_payload(expected_fixtures)
    expected_payload_schema = exact_schema(
        expected_payload,
        "tpc205-pair-native-registry-interface-v1.schema.json",
    )
    expected_l0 = build_expected_l0(expected_payload)
    expected_l0_schema = exact_schema(
        expected_l0,
        "tpc205-pair-native-l0-interface-v1.schema.json",
    )
    expected_audit = build_expected_audit(
        expected_payload,
        expected_payload_schema,
        expected_l0,
        expected_l0_schema,
    )
    expected_audit_schema = exact_schema(
        expected_audit,
        "tpc205-pair-native-registry-interface-audit-v1.schema.json",
    )

    verify_payload_semantics(payload, expected_payload)
    verify_l0(l0, expected_l0)
    verify_audit(audit, expected_audit)
    require(
        strict_same(payload_schema, expected_payload_schema),
        "PAYLOAD_SCHEMA_EXACT",
    )
    require(strict_same(audit_schema, expected_audit_schema), "AUDIT_SCHEMA_EXACT")
    require(strict_same(l0_schema, expected_l0_schema), "L0_SCHEMA_EXACT")
    require(schema_accepts(payload_schema, payload), "PAYLOAD_SCHEMA_ACCEPTANCE")
    require(schema_accepts(audit_schema, audit), "AUDIT_SCHEMA_ACCEPTANCE")
    require(schema_accepts(l0_schema, l0), "L0_SCHEMA_ACCEPTANCE")
    base_count = verify_base_mutations(expected_payload, expected_payload_schema)
    semantic_count = verify_semantic_mutations(expected_payload)
    strict_type_count = verify_strict_type_mutations(expected_payload)
    l0_hardening_count = verify_l0_hardening_mutation(expected_l0)
    audit_hardening_count = verify_audit_hardening_mutations(expected_audit)
    verify_frozen_raw_hashes()
    verify_manifest()

    print(
        json.dumps(
            {
                "paper": 205,
                "independent_checker": True,
                "imports_materializer": False,
                "source_locks_verified": 17,
                "relation_types_verified": 4,
                "required_registry_fields": 42,
                "production_pair_records": 0,
                "production_pair_record_scope": (
                    "DECLARED_TPC205_REGISTRY_SOURCE_LOCK_CORPUS_ONLY"
                ),
                "L0_fixtures_verified": 2,
                "gates_verified": 23,
                "base_mutations_rejected": base_count,
                "semantic_mutations_rejected": semantic_count,
                "strict_type_mutations_rejected": strict_type_count,
                "L0_hardening_mutations_rejected": l0_hardening_count,
                "audit_hardening_mutations_rejected": audit_hardening_count,
                "manifest_artifacts_verified": len(ACTIVE_ARTIFACTS),
                "manifest_is_external_signature": False,
                "hash_integrity_is_theorem_evidence": False,
                "verdict": VERDICT,
            },
            sort_keys=True,
        )
    )


if __name__ == "__main__":
    main()
