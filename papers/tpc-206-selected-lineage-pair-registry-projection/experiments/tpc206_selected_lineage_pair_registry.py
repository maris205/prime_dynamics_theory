#!/usr/bin/env python3
"""Materialize and verify the finite TPC-206 selected-lineage certificate."""

from __future__ import annotations

import argparse
import copy
import hashlib
import json
import math
import subprocess
from pathlib import Path
from typing import Any, Iterable


HERE = Path(__file__).resolve().parent
PAPER = HERE.parent
REPO = PAPER.parents[1]
PAYLOAD_PATH = HERE / "tpc206_selected_lineage_pair_registry.json"
AUDIT_PATH = HERE / "tpc206_selected_lineage_pair_registry_audit.json"
MANIFEST_PATH = HERE / "tpc206_certificate_manifest.json"
PAYLOAD_SCHEMA_PATH = (
    PAPER / "schemas" / "tpc206-selected-lineage-pair-registry-v1.schema.json"
)
AUDIT_SCHEMA_PATH = (
    PAPER
    / "schemas"
    / "tpc206-selected-lineage-pair-registry-audit-v1.schema.json"
)

PAPER_NUMBER = 206
PARENT_PAPER = 205
SOURCE_SNAPSHOT_COMMIT = "42507087b774d9057ba3794468a4790bf93162d5"
TPC205_COMMIT = "98b3e6c462008b07538b496ed130b1004a84747f"
AUTHORIZATION_SCOPE = (
    "FINITE_SELECTED_LINEAGE_13_OF_42_PROJECTION_AND_FIRST_MISSING_D_THEOREM"
)
CLASSIFICATION = "PAIR_NATIVE_SELECTED_LINEAGE_PROJECTION_L1"
THEOREM_STATUS = (
    "PROVED_SELECTED_SOURCE_LOCKED_13_OF_42_PROJECTION_AND_FIRST_MISSING_D_L1"
)
VERDICT = (
    "SELECTED_SOURCE_LOCKED_13_OF_42_PAIR_REGISTRY_PROJECTION_"
    "CERTIFIED_NOT_REOPENED"
)
PARENT_FIRST_MISSING = (
    "SOURCE_LOCKED_POST_TTSTAR_ORDERED_PAIR_REGISTRY_WITH_COMPLETE_"
    "PAIR_COEFFICIENT_AND_GLOBAL_NORMALIZATION"
)
FIRST_MISSING = (
    "SOURCE_LOCKED_TPC18_OPENED_D_PACKET_LINEAGE_FOR_SELECTED_ORDERED_PAIR"
)
FIRST_MISSING_FIELD = "D"
FIRST_MISSING_INDEX = 9
DECLARED_CORPUS = "DECLARED_TPC206_SELECTED_103_107_LINEAGE_GRAPH_V1"
NEW_STOP_CELL = f"{DECLARED_CORPUS}=STOP_SCOPED"
HASH_MODE = "CANONICAL_UTF8_LF_SHA256"
TPC133_MANIFEST_SHA256 = (
    "bda1a64348bc0d97fca4239b1c2a099a58aea5fbc4908580fc740f114a57fd39"
)

BASELINE_REF_PAIRS = [
    ["refs/heads/main", "a5f6c645504261d36081898a6e7b11e4992fac8d"],
    ["refs/heads/rough-pair-parity", "a5b348d9084833a51e33defae44d04c7cf7dc6d8"],
    ["refs/heads/short-box-sieve-kernels", "a4c8a4a018bf26802033990e13b6f06a8d0190ce"],
    ["refs/heads/structured-sieve-low-conductor", "cc8b3fac16294cff4e26d77f903f77aa73a40400"],
    ["refs/heads/tpc-10-nonzero-mellin-localization", "0709ffab634d9f628ca3f7b7f3910c5d3dd2367f"],
    ["refs/heads/tpc-11-factor-ray-dephasing", "0e4e762ab29ea66cc95e38e310a86b7aad22f29c"],
    ["refs/heads/tpc-12-intra-ray-cancellation", "311ce8b040f65bb2d8f2d6638b990b7b9d018bee"],
    ["refs/heads/tpc-13-radial-mellin-completion", "c8c32ebc3e42ee3c6a4200a86399e4f73386c5ee"],
    ["refs/heads/tpc-14-label-preserving-dispersion", "ceef5b91f79055f2785bdf6e4c301c64753256a6"],
    ["refs/heads/tpc-15-fixed-shift-typeii-interface", "f497caad1dcf6bff7b52361dee191f3dac308bfd"],
    ["refs/heads/tpc-16-dyadic-balanced-corridor", "eaa2b3546eb1cb5e8b3ef5d847aca24fae6faf66"],
    ["refs/heads/tpc-17-maze-next-gate", "5438204e32f990b66c422daa14af7c7436afd4ab"],
    ["refs/heads/tpc-18-determinant-tail-ttstar", "f418ea1a892120fb50b56d16debeece26afc557e"],
    ["refs/heads/tpc-19-primitive-determinant-dispersion", "a6b64bf4fb508b1d0f80530639cbc496a91e318c"],
    ["refs/heads/tpc-20-matched-spectral-reduction", "a7c3a7ed6ac9937fee76c2a4ad9eef6d5355805e"],
    ["refs/heads/tpc-21-fiber-discrepancy-gate", "dc916dc42a2dc4fb4d8e3cca69c2633af60f4894"],
    ["refs/heads/tpc-22-shared-factor-moment", "69291771027bab27ca5e00eaf37fe085c0d5f637"],
    ["refs/heads/tpc-23-one-sided-large-divisor", "9cb078f0aceb105fd807e44e63a63f8082361783"],
    ["refs/heads/tpc-24-asymmetric-zero-mode", "ea932b272601d480160861631d07cdbddf4c9b89"],
    ["refs/heads/tpc-25-row-averaged-zero-mode", "1cf8d0da027cb2212251719a5396e6fcd43f0224"],
    ["refs/heads/tpc-26-both-new-square", "a49b0f2be4ca59d0c3d551f95b49e3508070bb90"],
    ["refs/heads/tpc-27-calibrated-base-closure", SOURCE_SNAPSHOT_COMMIT],
    ["refs/heads/tpc-5-prime-weighted-transfer", "be8cd9dd528d4f58599772146516a2c27e6e2317"],
    ["refs/heads/tpc-6-prime-target-defect", "12fce45af98061ac95d7dcb6a8b3a9a540e33394"],
    ["refs/heads/tpc-7-almost-all-shift-defect", "0c2346b0a799d17bc062f2c2e553f182d386b448"],
    ["refs/heads/tpc-8-low-conductor-second-coefficient", "18655dd8ed978d2247e85858d33e71dcb9863b9a"],
    ["refs/heads/tpc-9-prime-residual-covariance", "ad77517ad8b06bf89f45cc682739b052c5560411"],
    ["refs/heads/twin-prime-correlations", "3317f65f60fa430dc1bab22af3e857eadc312046"],
    ["refs/remotes/origin/HEAD", SOURCE_SNAPSHOT_COMMIT],
    ["refs/remotes/origin/main", SOURCE_SNAPSHOT_COMMIT],
    ["refs/remotes/origin/rough-pair-parity", "a5b348d9084833a51e33defae44d04c7cf7dc6d8"],
    ["refs/remotes/origin/short-box-sieve-kernels", "a4c8a4a018bf26802033990e13b6f06a8d0190ce"],
    ["refs/remotes/origin/structured-sieve-low-conductor", "cc8b3fac16294cff4e26d77f903f77aa73a40400"],
    ["refs/remotes/origin/twin-prime-correlations", "3317f65f60fa430dc1bab22af3e857eadc312046"],
]

BASELINE_TIPS = sorted({oid for _, oid in BASELINE_REF_PAIRS})

EXPECTED_INVENTORY = {
    "ref_count": 34,
    "unique_tip_count": 28,
    "commit_count": 328,
    "reachable_object_count": 12203,
    "commit_object_count": 328,
    "tree_object_count": 3316,
    "blob_object_count": 8559,
    "blob_bytes": 549022045,
    "text_blob_count": 7479,
    "text_blob_bytes": 165158579,
    "record_like_blob_count": 3551,
    "record_like_blob_bytes": 146302386,
    "parseable_json_blob_count": 1707,
    "json_parse_failures": 17,
    "digests": {
        "refs_tsv": "6ab93d0eea746d3f1395ededcc982d221894de47939841964776e3bf0b7ef823",
        "tips_lf": "2e72549ba295cbc6c0fc2efb39bee4b0c11ac1a3a0734afa64da547e43726607",
        "commits_lf": "bbfef7198e46ce6165c00832b53a9b09b94642701f4e4fa76ab5db5ea875bcee",
        "objects_tsv": "3d88cccca291330ad99393f62d9dd4d024f29affbb53ff4201c28d769528ffaf",
        "text_tsv": "51dc91013d8230ac7decce1a63dcfe25cc8e6fa2d65aa4700f74a746fd3e461f",
        "record_like_tsv": "3d11a15ab0524213ce9a99bf7246f0b8f206b3352e4db8b22c40c3fffef89eee",
        "json_tsv": "c8f46549dcaa69288d5635b9bc416603131ab174f5b824d3045d6eca5cbb8b65",
        "structured_keys": "40a5b076fe134099caf98267fff372de0306b770289750f4557f577bde5c2f90",
    },
}

TEXT_SUFFIXES = {
    ".json",
    ".jsonl",
    ".md",
    ".tex",
    ".py",
    ".bib",
    ".txt",
    ".yaml",
    ".yml",
    ".csv",
    ".tsv",
    ".toml",
    ".ini",
    ".cfg",
    ".rst",
}
RECORD_TOKENS = {
    "record",
    "registry",
    "certificate",
    "audit",
    "manifest",
    "result",
    "sample",
    "fixture",
    "archive",
    "schema",
    "ledger",
}
STRUCTURED_KEYS = [
    "pair_record",
    "pair_records",
    "pair_record_id",
    "row_pair",
    "row_pair_id",
    "joint_mask",
    "literal_coefficient",
    "pair_nonzero",
    "coefficient_nonzero",
    "nonzero_status",
    "global_normalization",
    "source_atom",
    "pair_to_omega",
    "ordered_pair",
    "coefficient_ast",
    "packet_schedule",
    "global_normalization_return",
    "pair_to_omega_bridge",
    "pair_to_omega_crosswalk_proved",
    "omega",
]
EXPECTED_STRUCTURED_KEY_COUNTS = {
    "pair_record": [0, 0],
    "pair_records": [0, 0],
    "pair_record_id": [0, 0],
    "row_pair": [0, 0],
    "row_pair_id": [0, 0],
    "joint_mask": [0, 0],
    "literal_coefficient": [0, 0],
    "pair_nonzero": [0, 0],
    "coefficient_nonzero": [0, 0],
    "nonzero_status": [0, 0],
    "global_normalization": [0, 0],
    "source_atom": [0, 0],
    "pair_to_omega": [0, 0],
    "ordered_pair": [4, 4],
    "coefficient_ast": [1, 1],
    "packet_schedule": [6, 6],
    "global_normalization_return": [2, 2],
    "pair_to_omega_bridge": [2, 2],
    "pair_to_omega_crosswalk_proved": [2, 2],
    "omega": [1, 1],
}

FIELD_BLOCKS = {
    "identity_scope": [
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
    "ordered_pair": [
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
    "source_child": [
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
    "normalization": [
        "source_normalization",
        "linear_normalization",
        "quadratic_normalization",
        "target_normalization",
    ],
}

MATERIALIZED_VALUES = {
    "X": 512,
    "h0": 2,
    "delta": {"numerator": 1, "denominator": 4},
    "R": 4,
    "V": 2,
    "D0": 0,
    "L": 64,
    "K": 8,
    "alpha=(ell_alpha,d_alpha)": [103, 1],
    "gamma=(ell_gamma,d_gamma)": [107, 1],
    "j": 5,
    "N_alpha(j)": 517,
    "N_gamma(j)": 537,
}

DERIVATION_RULES = {
    "X": "TPC133_SELECTED_ROWS_LITERAL_PACKET_SCOPE",
    "h0": "TPC133_SELECTED_ROWS_LITERAL_PACKET_SCOPE",
    "delta": "TPC133_CHOSEN_MANIFEST_CERTIFICATE_ARCHIVE_PROVENANCE",
    "R": "TPC133_TRUNCATION_Q_TO_TPC18_R_TYPED_ALIAS",
    "V": "TPC133_SELECTED_ROWS_LITERAL_PACKET_SCOPE",
    "D0": "TPC134_TPC136_SELECTED_PATH_LITERAL",
    "L": "TPC134_L_EQUALS_TWO_TO_JL",
    "K": "TPC134_K_EQUALS_TWO_TO_JK",
    "alpha=(ell_alpha,d_alpha)": "TPC133_ALPHA_ROW_PROJECTION",
    "gamma=(ell_gamma,d_gamma)": "TPC133_GAMMA_ROW_PROJECTION",
    "j": "TPC18_NATIVE_k_EQUALS_d_TIMES_j_ON_SELECTED_ROWS",
    "N_alpha(j)": "ELL_D_J_PLUS_H0",
    "N_gamma(j)": "ELL_D_J_PLUS_H0",
}

FIELD_BLOCKERS = {
    "D": "NO_SELECTED_PAIR_OPENED_D_SLICE_LOCATOR_D_IS_NOT_ROW_DIVISOR_d",
    "J": "CONDITIONAL_K_OVER_D_ONLY_D_UNSUPPLIED",
    "Q": "TPC18_ROW_SCALE_L_TIMES_D_UNSUPPLIED_DO_NOT_REUSE_TPC133_Q",
    "T": "NO_SOURCE_LOCKED_ULTRA_SCHEDULE_FOR_SELECTED_PAIR",
    "U0": "NO_SOURCE_LOCKED_ULTRA_SCHEDULE_FOR_SELECTED_PAIR",
    "G_X_row": "NO_SELECTED_PAIR_ROW_GCD_CUTOFF_ATTACHMENT",
    "packet_id": "NO_JOINT_PRODUCTION_PACKET_ID",
    "source_locator": "TWO_ROW_AND_PATH_LOCATORS_ARE_NOT_ONE_JOINT_PAIR_LOCATOR",
    "joint_mask_value": "NO_EVALUATED_ACTIVE_JOINT_MASK",
    "literal_pair_coefficient_ast": "TPC18_B_ALIASES_NOT_FULLY_MATERIALIZED",
    "relation_type=TTSTAR_BILINEAR_PAIR_TERM": (
        "FORMULA_TYPE_NOT_ATTACHED_TO_AN_ACTUAL_PAIR_RECORD"
    ),
    "formal_support_status": "TPC18_SUPPORT_RESTRICTIONS_NOT_LITERALIZED_ON_CANDIDATE",
    "numeric_nonzero_status": "INDIVIDUAL_SYMBOLIC_ROWS_REMAIN_UNDECIDED",
    "polarization": "NO_SUPPLIED_RETAINED_OMEGA",
    "u": "NO_SUPPLIED_RETAINED_OMEGA",
    "sigma": "NO_SUPPLIED_RETAINED_OMEGA",
    "v": "NO_SUPPLIED_RETAINED_OMEGA",
    "iota": "NO_SUPPLIED_RETAINED_OMEGA",
    "theta": "NO_SUPPLIED_RETAINED_OMEGA",
    "t": "NO_SUPPLIED_RETAINED_OMEGA",
    "projector_weight": "NO_SUPPLIED_RETAINED_OMEGA",
    "child_to_source_inverse": "TPC93_PREMISE_NOT_INSTANTIATED",
    "content_child": "DOWNSTREAM_TEMPLATE_ONLY",
    "frequency_child": "DOWNSTREAM_TEMPLATE_ONLY",
    "resolved_xi": "DOWNSTREAM_TEMPLATE_ONLY",
    "source_normalization": "NU_X_IS_A_SCOPE_LABEL_NOT_A_SCALAR",
    "linear_normalization": "NO_NUMERIC_LINEAR_NORMALIZATION_ATTACHMENT",
    "quadratic_normalization": "NO_SQUARED_NORMALIZATION_ATTACHMENT",
    "target_normalization": "GLOBAL_NORMALIZATION_RETURN_MISSING",
}

SOURCE_PATHS_NEW = [
    {
        "id": "TPC133.main",
        "path": "papers/tpc-133-executable-native-entrance/main.tex",
        "expected_sha256": "5f902b7fc219a50cf31b40c32bb863f180bc7af1a0942dd0d5e5a01d8fe41c16",
        "anchors": [
            r"Q=\lfloor X^{1/2-\delta}\rfloor",
            r"(X,h_0,\ell,k,d)",
            r"together with the packet-scope fields \(Q,U,V,W\)",
        ],
    },
    {
        "id": "TPC133.manifest",
        "path": (
            "papers/tpc-133-executable-native-entrance/"
            "samples/tpc133_packet_manifest.json"
        ),
        "expected_sha256": "bda1a64348bc0d97fca4239b1c2a099a58aea5fbc4908580fc740f114a57fd39",
        "anchors": ['"numerator": 1', '"denominator": 4', '"X": 512'],
    },
    {
        "id": "TPC133.certificate",
        "path": (
            "papers/tpc-133-executable-native-entrance/"
            "experiments/tpc133_native_entrance_certificate.json"
        ),
        "expected_sha256": "e60042995fe25aeb3b6f98df78e89d08bfda4e48231d8f58b6c6aa66516887f3",
        "anchors": ['"delta": "1/4"', '"Q": 4', '"V": 2'],
    },
    {
        "id": "TPC133.generator",
        "path": (
            "papers/tpc-133-executable-native-entrance/"
            "experiments/tpc133_native_entrance.py"
        ),
        "expected_sha256": "85a7263059b6690de3d70c79a3f2e31fbaecded72223c0a19d25c652e18dae9e",
        "anchors": [
            "q_value = floor_rational_power(manifest[\"X\"], exponent)",
            '"Q": q_value',
            '"V": u_value',
        ],
    },
    {
        "id": "TPC134.main",
        "path": (
            "papers/tpc-134-boundary-complete-dyadic-prefix-tail-archive/main.tex"
        ),
        "expected_sha256": "3fe4a6fdbdb4e6b1d28305987e13bd82069c1ff00fd327be7c7a42c7d0d83d55",
        "anchors": [
            r"L=2^{j_L},\quad K=2^{j_K}",
            r"\psi(\ell/L)\psi(k/K)\ne0",
        ],
    },
    {
        "id": "TPC134.paths",
        "path": (
            "papers/tpc-134-boundary-complete-dyadic-prefix-tail-archive/"
            "samples/tpc134_paths.jsonl"
        ),
        "expected_sha256": "efcacc90e7662fdb41c2e3f86fb37d3bd81b64a107c36dfbbb15bb48bde61712",
        "anchors": [
            "fb013b12446318c3f902909a479ddefb8329e771e936e58a2dfcc47a9e450b4f",
            "4e3b8147b8729a169cfcbcd32ef1ee9517f06ce7f4f3edcc7250b1a2f6e8c273",
        ],
    },
    {
        "id": "TPC135.main",
        "path": "papers/tpc-135-tpc17-tpc18-block-frontier/main.tex",
        "expected_sha256": "f776fe1b48d1dd833c45ed1511895ab604b727b603596c2c82f821d335afba18",
        "anchors": [
            r"R=\lfloor X^{1/2-\delta}\rfloor",
            r"L=2^{j_L}",
            r"K=2^{j_K}",
        ],
    },
    {
        "id": "TPC135.checker",
        "path": (
            "papers/tpc-135-tpc17-tpc18-block-frontier/"
            "experiments/tpc135_domain_cover_audit.py"
        ),
        "expected_sha256": "604240f83d83dde71dfcece06cad7a4eb52dbc35dbddec16d7372ed41edfb71c",
        "anchors": [
            'r_value = metadata["Q"]',
            'v_value = metadata["V"]',
        ],
    },
    {
        "id": "TPC135.frontier",
        "path": (
            "papers/tpc-135-tpc17-tpc18-block-frontier/"
            "samples/tpc135_frontier_manifest.json"
        ),
        "expected_sha256": "6655a4c40a57f0a45022ab527b32560a5b2ac3e932368709502cfded43a3fb47",
        "anchors": ['"R": 4', '"V": 2', '"j_L": 6', '"j_K": 3'],
    },
    {
        "id": "TPC136.main",
        "path": "papers/tpc-136-complete-native-cut-archive/main.tex",
        "expected_sha256": "9e55e455077d2bd6c0a177a0627cc11659d9ae2f8396c6a365a5ce5df176ad89",
        "anchors": [
            r"\mathrm{frontier\ unmapped}",
            r"\one^TM_X^{\rm cut}=\one^T",
            "The cut archive is not yet the physical archive",
        ],
    },
    {
        "id": "TPC205.payload",
        "path": (
            "papers/tpc-205-pair-native-post-ttstar-registry-interface/"
            "experiments/tpc205_pair_native_registry_interface.json"
        ),
        "expected_sha256": "07b118b69a16587fe1b9239b585ffa65b6772f005d9c719eb5eba3cc488d586d",
        "anchors": [
            '"required_registry_fields": 42',
            '"production_pair_records": 0',
            '"pair_to_omega_bridge": "MISSING"',
        ],
    },
    {
        "id": "TPC205.main",
        "path": (
            "papers/tpc-205-pair-native-post-ttstar-registry-interface/main.tex"
        ),
        "expected_sha256": "f5586627671e99323e924875a1c066c49ca1a1bb8c210e65b2b3f185887b19d7",
        "anchors": [
            "The machine contract requires 42 fields",
            "DUAL_SOURCE_LOCKED_ROW_PAIR_CANDIDATE",
        ],
    },
]

STOP_SCOPED = [
    "TPC193_DECLARED_CANDIDATE_MECHANISM_CORPUS_V1=STOP_SCOPED",
    "TPC204_DECLARED_PLAUSIBLE_PRODUCTION_CROSSWALK_CORPUS_V1=STOP_SCOPED",
    "TPC18_25_32_93_194_SINGLE_CUT_OCCURRENCE_COMPOSITE_V1=STOP_SCOPED",
    "TPC18_TPC93_POST_TTSTAR_PAIR_DIRECT_COMPOSITION_V1=STOP_SCOPED",
    NEW_STOP_CELL,
]

SEMANTIC_MUTATIONS = [
    "promote_13_to_14",
    "omit_blocked_field",
    "replace_first_missing_D_with_d",
    "reuse_tpc133_Q_as_tpc205_Q",
    "detach_delta_from_manifest_lineage",
    "replace_R_typed_alias_with_name_equality",
    "use_jL_as_L_without_pow2",
    "use_jK_as_K_without_pow2",
    "promote_finite_delta_to_cross_scale_schedule",
    "promote_projection_id_to_production_id",
    "collapse_pair_edge_target_ids",
    "swap_alpha_gamma_quotient",
    "splice_tpc32_child_fields",
    "splice_tpc32_T_U0",
    "manual_u_selection",
    "manual_polarization_selection",
    "promote_row_only_to_production",
    "promote_l0_to_production",
    "promote_shadow_to_actual",
    "promote_formal_to_actual",
    "promote_synthetic_to_actual",
    "support_to_nonzero",
    "null_joint_mask_to_one",
    "B_alias_to_full_literal",
    "implicit_conjugation",
    "nu_X_label_to_scalar",
    "copy_one_normalization_to_four_stages",
    "drop_quadratic_scalar_square",
    "pair_to_omega_pass",
    "remove_supplied_omega_premise",
    "single_child_restores_source",
    "drop_projector_support",
    "pay_hard_remainder",
    "pay_square_root_return",
    "pay_endpoint_return",
    "production_count_zero_to_one",
    "full_join_zero_to_one",
    "mathematical_reopen_true",
    "H1_E_repair_true",
    "fixed_atom_credit_positive",
    "positive_sigma_true",
    "strict_one_over_400_paid",
    "L2_promoted",
    "stop_scoped_removed",
    "stop_scoped_globalized",
    "O161_parent_closed",
    "H1_architecture_closed",
    "authorization_becomes_evidence",
    "source_lock_rebound_with_content",
    "archive_census_omission",
    "structured_key_count_rewrite",
    "selected_scope_globalized",
]

BASE_MUTATIONS = [
    "wrong_schema",
    "wrong_paper_number",
    "wrong_parent_paper",
    "wrong_classification",
    "wrong_theorem_status",
    "wrong_verdict",
    "wrong_source_snapshot",
    "wrong_required_field_count",
    "wrong_materialized_count",
    "wrong_missing_count",
    "wrong_first_missing_index",
    "extra_top_level_key",
]

STRICT_TYPE_MUTATIONS = [
    "paper_true",
    "parent_paper_false",
    "X_true",
    "h0_false",
    "D0_false",
    "field_index_true",
    "materialized_count_true",
    "missing_count_false",
    "delta_numerator_true",
    "delta_denominator_true",
    "authorization_zero",
    "mathematical_reopen_zero",
]

ACTIVE_ARTIFACTS = [
    (
        "papers/tpc-206-selected-lineage-pair-registry-projection/"
        "experiments/build_tpc206.py"
    ),
    (
        "papers/tpc-206-selected-lineage-pair-registry-projection/"
        "experiments/tpc206_selected_lineage_pair_registry.py"
    ),
    (
        "papers/tpc-206-selected-lineage-pair-registry-projection/"
        "experiments/tpc206_independent_checker.py"
    ),
    (
        "papers/tpc-206-selected-lineage-pair-registry-projection/"
        "experiments/tpc206_selected_lineage_pair_registry.json"
    ),
    (
        "papers/tpc-206-selected-lineage-pair-registry-projection/"
        "experiments/tpc206_selected_lineage_pair_registry_audit.json"
    ),
    (
        "papers/tpc-206-selected-lineage-pair-registry-projection/"
        "schemas/tpc206-selected-lineage-pair-registry-v1.schema.json"
    ),
    (
        "papers/tpc-206-selected-lineage-pair-registry-projection/"
        "schemas/tpc206-selected-lineage-pair-registry-audit-v1.schema.json"
    ),
    "papers/tpc-206-selected-lineage-pair-registry-projection/README.md",
    "papers/tpc-206-selected-lineage-pair-registry-projection/main.tex",
    "papers/tpc-206-selected-lineage-pair-registry-projection/references.bib",
    (
        "papers/tpc-206-selected-lineage-pair-registry-projection/"
        "tpc-206-selected-lineage-pair-registry-projection.pdf"
    ),
]


def require(condition: bool, code: str) -> None:
    if not condition:
        raise RuntimeError(code)


def canonical(value: Any) -> str:
    return json.dumps(value, ensure_ascii=False, indent=2, sort_keys=True) + "\n"


def compact(value: Any) -> bytes:
    return json.dumps(
        value, ensure_ascii=False, separators=(",", ":"), sort_keys=True
    ).encode("utf-8")


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def canonical_text_bytes(path: Path) -> bytes:
    text = path.read_text(encoding="utf-8")
    return text.replace("\r\n", "\n").replace("\r", "\n").encode("utf-8")


def snapshot_canonical_text_bytes(relative: str) -> bytes:
    result = subprocess.run(
        ["git", "show", f"{SOURCE_SNAPSHOT_COMMIT}:{relative}"],
        cwd=REPO,
        capture_output=True,
        check=False,
    )
    require(result.returncode == 0, f"SNAPSHOT_SOURCE_MISSING:{relative}")
    text = result.stdout.decode("utf-8")
    return text.replace("\r\n", "\n").replace("\r", "\n").encode("utf-8")


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


def git_output(args: list[str], input_text: str | None = None) -> str:
    result = subprocess.run(
        ["git", *args],
        cwd=REPO,
        input=input_text,
        text=True,
        encoding="utf-8",
        errors="strict",
        capture_output=True,
        check=False,
    )
    require(result.returncode == 0, f"GIT_FAILED:{args}:{result.stderr.strip()}")
    return result.stdout


def tsv_digest(rows: Iterable[str]) -> tuple[str, int]:
    raw = ("".join(f"{row}\n" for row in rows)).encode("utf-8")
    return sha256_bytes(raw), len(raw)


def exact_schema(value: Any, title: str | None = None) -> dict[str, Any]:
    if type(value) is dict:
        schema: dict[str, Any] = {
            "type": "object",
            "properties": {
                key: exact_schema(value[key]) for key in sorted(value)
            },
            "required": sorted(value),
            "additionalProperties": False,
        }
    elif type(value) is list:
        schema = {
            "type": "array",
            "prefixItems": [exact_schema(item) for item in value],
            "items": False,
            "minItems": len(value),
            "maxItems": len(value),
        }
    elif type(value) is bool:
        schema = {"type": "boolean", "const": value}
    elif type(value) is int:
        schema = {"type": "integer", "const": value}
    elif type(value) is float:
        require(math.isfinite(value), "NONFINITE_SCHEMA_FLOAT")
        schema = {"type": "number", "const": value}
    elif type(value) is str:
        schema = {"type": "string", "const": value}
    elif value is None:
        schema = {"type": "null", "const": None}
    else:
        raise TypeError(f"unsupported schema value type: {type(value)}")
    if title is not None:
        schema = {
            "$schema": "https://json-schema.org/draft/2020-12/schema",
            "title": title,
            **schema,
        }
    return schema


def schema_accepts(schema: dict[str, Any], value: Any) -> bool:
    expected_types = {
        "object": dict,
        "array": list,
        "null": type(None),
        "boolean": bool,
        "integer": int,
        "number": float,
        "string": str,
    }
    kind = schema.get("type")
    if kind not in expected_types or type(value) is not expected_types[kind]:
        return False
    if "const" in schema and not strict_same(value, schema["const"]):
        return False
    if kind == "object":
        properties = schema.get("properties")
        required = schema.get("required")
        if type(properties) is not dict or type(required) is not list:
            return False
        if schema.get("additionalProperties") is not False:
            return False
        if set(value) != set(required) or set(properties) != set(required):
            return False
        return all(schema_accepts(properties[key], value[key]) for key in value)
    if kind == "array":
        prefix = schema.get("prefixItems")
        if type(prefix) is not list or schema.get("items") is not False:
            return False
        if not (
            schema.get("minItems") == len(value) == schema.get("maxItems")
            and len(prefix) == len(value)
        ):
            return False
        return all(
            schema_accepts(child_schema, child)
            for child_schema, child in zip(prefix, value)
        )
    return True


def set_path(value: Any, path: list[Any], replacement: Any) -> Any:
    result = copy.deepcopy(value)
    cursor = result
    for key in path[:-1]:
        cursor = cursor[key]
    cursor[path[-1]] = replacement
    return result


BASE_MUTATION_TARGETS = {
    "wrong_schema": (["schema"], "tpc-206-wrong"),
    "wrong_paper_number": (["paper"], 207),
    "wrong_parent_paper": (["parent_paper"], 204),
    "wrong_classification": (["classification"], "PAIR_NATIVE_L2"),
    "wrong_theorem_status": (["theorem_status"], "UNPROVED"),
    "wrong_verdict": (["verdict"], "REOPENED"),
    "wrong_source_snapshot": (["source_snapshot_commit"], "0" * 40),
    "wrong_required_field_count": (
        ["contract_import", "required_field_count"],
        41,
    ),
    "wrong_materialized_count": (["summary_counts", "materialized_fields"], 14),
    "wrong_missing_count": (["summary_counts", "missing_fields"], 28),
    "wrong_first_missing_index": (
        ["selected_lineage_theorem", "first_missing_field_index"],
        10,
    ),
}

STRICT_TYPE_MUTATION_TARGETS = {
    "paper_true": (["paper"], True),
    "parent_paper_false": (["parent_paper"], False),
    "X_true": (["field_ledger", 0, "value"], True),
    "h0_false": (["field_ledger", 1, "value"], False),
    "D0_false": (["field_ledger", 5, "value"], False),
    "field_index_true": (["field_ledger", 8, "one_based_index"], True),
    "materialized_count_true": (["summary_counts", "materialized_fields"], True),
    "missing_count_false": (["summary_counts", "missing_fields"], False),
    "delta_numerator_true": (
        ["field_ledger", 2, "value", "numerator"],
        True,
    ),
    "delta_denominator_true": (
        ["field_ledger", 2, "value", "denominator"],
        True,
    ),
    "authorization_zero": (["authorization", "user_authorized"], 0),
    "mathematical_reopen_zero": (
        ["claim_firewall", "mathematical_reopen"],
        0,
    ),
}

SEMANTIC_MUTATION_TARGETS = {
    "promote_13_to_14": (
        ["selected_lineage_theorem", "selected_graph_materialized_fields"],
        14,
    ),
    "replace_first_missing_D_with_d": (
        ["selected_lineage_theorem", "first_missing_field_id"],
        "d",
    ),
    "reuse_tpc133_Q_as_tpc205_Q": (["field_ledger", 10, "value"], 4),
    "detach_delta_from_manifest_lineage": (
        ["selected_projection", "exact_derivations", 0, "rule_id"],
        "UNLOCKED_DELTA",
    ),
    "replace_R_typed_alias_with_name_equality": (
        ["selected_projection", "exact_derivations", 1, "rule_id"],
        "BARE_NAME_EQUALITY",
    ),
    "use_jL_as_L_without_pow2": (["field_ledger", 6, "value"], 6),
    "use_jK_as_K_without_pow2": (["field_ledger", 7, "value"], 3),
    "promote_finite_delta_to_cross_scale_schedule": (
        ["selected_projection", "exact_derivations", 0, "scope"],
        "ALL_X_CROSS_SCALE_SCHEDULE",
    ),
    "promote_projection_id_to_production_id": (
        ["selected_projection", "id_envelope", "projection_id_semantics"],
        "PRODUCTION_PAIR_RECORD_ID",
    ),
    "swap_alpha_gamma_quotient": (
        ["selected_projection", "orientation"],
        "UNORDERED_SWAP_QUOTIENT",
    ),
    "splice_tpc32_child_fields": (["field_ledger", 26, "value"], "L"),
    "splice_tpc32_T_U0": (["field_ledger", 11, "value"], 50),
    "manual_u_selection": (["field_ledger", 27, "value"], 61),
    "manual_polarization_selection": (["field_ledger", 26, "value"], "L"),
    "promote_row_only_to_production": (
        ["selected_projection", "evidence_level"],
        "PRODUCTION",
    ),
    "promote_l0_to_production": (
        ["comparison_fixture", "production_occurrence"],
        True,
    ),
    "promote_shadow_to_actual": (
        ["selected_projection", "production_occurrence"],
        True,
    ),
    "promote_formal_to_actual": (
        ["field_ledger", 23, "counts_as_production_record"],
        True,
    ),
    "promote_synthetic_to_actual": (
        ["comparison_fixture", "evidence_mode"],
        "PRODUCTION",
    ),
    "support_to_nonzero": (["field_ledger", 24, "value"], "PROVED_NONZERO"),
    "null_joint_mask_to_one": (["field_ledger", 21, "value"], 1),
    "B_alias_to_full_literal": (
        ["field_ledger", 22, "value"],
        {"op": "invented_full_literal"},
    ),
    "implicit_conjugation": (
        ["contract_import", "ordered_pair_quotient"],
        "IMPLICIT_HERMITIAN",
    ),
    "nu_X_label_to_scalar": (["field_ledger", 38, "value"], 1),
    "drop_quadratic_scalar_square": (["field_ledger", 40, "value"], 1),
    "pair_to_omega_pass": (["downstream_gates", 4, "status"], "PASS"),
    "remove_supplied_omega_premise": (
        ["legal_join_rules", "formula_type_without_record_attachment_counts"],
        True,
    ),
    "single_child_restores_source": (
        ["comparison_fixture", "legal_join_with_selected_projection"],
        True,
    ),
    "drop_projector_support": (
        ["comparison_fixture", "reason"],
        "SUPPORT_HYPOTHESES_DROPPED",
    ),
    "pay_hard_remainder": (
        ["claim_firewall", "fixed_atom_decay_obtained"],
        True,
    ),
    "pay_square_root_return": (
        ["claim_firewall", "positive_sigma_obtained"],
        True,
    ),
    "pay_endpoint_return": (
        ["claim_firewall", "strict_one_over_400_paid"],
        True,
    ),
    "production_count_zero_to_one": (
        ["summary_counts", "selected_lineage_production_occurrences"],
        1,
    ),
    "full_join_zero_to_one": (
        ["selected_lineage_theorem", "full_completions_inside_explicit_selected_graph"],
        1,
    ),
    "mathematical_reopen_true": (
        ["claim_firewall", "mathematical_reopen"],
        True,
    ),
    "H1_E_repair_true": (["claim_firewall", "H1_E_repair_proved"], True),
    "fixed_atom_credit_positive": (
        ["claim_firewall", "fixed_atom_credit"],
        1,
    ),
    "positive_sigma_true": (
        ["claim_firewall", "positive_sigma_obtained"],
        True,
    ),
    "strict_one_over_400_paid": (
        ["claim_firewall", "strict_one_over_400_paid"],
        True,
    ),
    "L2_promoted": (["claim_firewall", "L2_result"], "POSITIVE"),
    "stop_scoped_globalized": (
        ["stop_scoped", 4],
        f"{DECLARED_CORPUS}=GLOBAL_STOP",
    ),
    "O161_parent_closed": (
        ["route_state", "bad_endpoint_O161_parent"],
        "CLOSED",
    ),
    "H1_architecture_closed": (["route_state", "H1_architecture"], "CLOSED"),
    "authorization_becomes_evidence": (
        ["authorization", "authorization_is_theorem_evidence"],
        True,
    ),
    "source_lock_rebound_with_content": (
        ["source_locks", 0, "canonical_sha256"],
        "0" * 64,
    ),
    "structured_key_count_rewrite": (
        ["archive_census", "structured_key_counts", "pair_record"],
        [1, 1],
    ),
    "selected_scope_globalized": (
        ["selected_lineage_theorem", "theorem_scope"],
        "ALL_PAST_AND_FUTURE_SOURCES",
    ),
}


def named_mutation(payload: dict[str, Any], name: str, family: str) -> dict[str, Any]:
    if name == "extra_top_level_key":
        return {**copy.deepcopy(payload), "unexpected": 1}
    if name == "omit_blocked_field":
        return set_path(
            payload,
            ["selected_non_splicing_ledger"],
            payload["selected_non_splicing_ledger"][:-1],
        )
    if name == "collapse_pair_edge_target_ids":
        result = set_path(
            payload,
            ["selected_projection", "id_envelope", "edge_instance_id"],
            "collapsed-id",
        )
        return set_path(
            result,
            ["selected_projection", "id_envelope", "target_occurrence_id"],
            "collapsed-id",
        )
    if name == "copy_one_normalization_to_four_stages":
        result = copy.deepcopy(payload)
        for index in range(38, 42):
            result["field_ledger"][index]["value"] = 1
        return result
    if name == "stop_scoped_removed":
        return set_path(payload, ["stop_scoped"], payload["stop_scoped"][:-1])
    if name == "archive_census_omission":
        return set_path(
            payload,
            ["archive_census", "scan_anchor", "ref_pairs"],
            payload["archive_census"]["scan_anchor"]["ref_pairs"][:-1],
        )
    targets = {
        "base": BASE_MUTATION_TARGETS,
        "strict": STRICT_TYPE_MUTATION_TARGETS,
        "semantic": SEMANTIC_MUTATION_TARGETS,
    }[family]
    require(name in targets, f"UNIMPLEMENTED_MUTATION:{family}:{name}")
    path, replacement = targets[name]
    return set_path(payload, path, replacement)


def build_mutation_rows(
    payload: dict[str, Any],
    payload_schema: dict[str, Any],
    names: list[str],
    family: str,
) -> list[dict[str, Any]]:
    rows = []
    for name in names:
        mutated = named_mutation(payload, name, family)
        changed = not strict_same(mutated, payload)
        active_rejected = not schema_accepts(payload_schema, mutated)
        regenerated = exact_schema(mutated, f"TPC-206 mutation {name}")
        rows.append(
            {
                "name": name,
                "payload_changed": changed,
                "active_exact_schema_rejected": active_rejected,
                "regenerated_exact_schema_accepts": schema_accepts(
                    regenerated, mutated
                ),
                "expected_payload_reconstruction_rejected": not strict_same(
                    mutated, payload
                ),
            }
        )
    require(all(row["payload_changed"] for row in rows), f"MUTATION_NOOP:{family}")
    require(
        all(row["active_exact_schema_rejected"] for row in rows),
        f"ACTIVE_SCHEMA_ACCEPTED_MUTATION:{family}",
    )
    require(
        all(row["regenerated_exact_schema_accepts"] for row in rows),
        f"REGENERATED_SCHEMA_REJECTED_MUTATION:{family}",
    )
    require(
        all(row["expected_payload_reconstruction_rejected"] for row in rows),
        f"EXPECTED_REBUILD_ACCEPTED_MUTATION:{family}",
    )
    return rows


def verify_exact_schema(value: Any, schema: dict[str, Any], code: str) -> None:
    expected = exact_schema(value, schema.get("title"))
    strict_equal(schema, expected, code)


def read_jsonl_unique(path: Path, key: str, expected: str) -> tuple[dict[str, Any], int]:
    found: list[tuple[dict[str, Any], int]] = []
    for number, line in enumerate(
        path.read_text(encoding="utf-8").splitlines(), start=1
    ):
        record = json.loads(
            line,
            object_pairs_hook=unique_object,
            parse_constant=reject_constant,
        )
        if type(record) is dict and record.get(key) == expected:
            found.append((record, number))
    require(len(found) == 1, f"SELECTOR_NOT_UNIQUE:{path}:{key}:{expected}")
    return found[0]


def verify_integrity(record: dict[str, Any]) -> None:
    expected = record.get("integrity_sha256")
    require(type(expected) is str, "INTEGRITY_FIELD")
    body = {key: value for key, value in record.items() if key != "integrity_sha256"}
    require(sha256_bytes(compact(body)) == expected, f"INTEGRITY_MISMATCH:{expected}")


def build_source_locks() -> list[dict[str, Any]]:
    tpc205 = load_json(
        REPO
        / "papers/tpc-205-pair-native-post-ttstar-registry-interface/"
        "experiments/tpc205_pair_native_registry_interface.json"
    )
    imported = []
    for lock in tpc205["source_locks"]:
        path = REPO / lock["path"]
        require(path.is_file(), f"IMPORTED_SOURCE_MISSING:{lock['id']}")
        text = canonical_text_bytes(path).decode("utf-8")
        for anchor in lock["required_anchors"]:
            require(anchor in text, f"IMPORTED_ANCHOR:{lock['id']}:{anchor}")
        digest = sha256_bytes(canonical_text_bytes(path))
        require(digest == lock["canonical_sha256"], f"IMPORTED_HASH:{lock['id']}")
        require(
            sha256_bytes(snapshot_canonical_text_bytes(lock["path"])) == digest,
            f"IMPORTED_SNAPSHOT_HASH:{lock['id']}",
        )
        imported.append(
            {
                "id": lock["id"],
                "path": lock["path"],
                "hash_mode": HASH_MODE,
                "hash_semantics": "INTEGRITY_ONLY",
                "canonical_sha256": digest,
                "frozen_expected_sha256": lock["canonical_sha256"],
                "snapshot_commit": SOURCE_SNAPSHOT_COMMIT,
                "required_anchors": list(lock["required_anchors"]),
                "provenance": "TPC205_LOCK_REVERIFIED",
            }
        )
    require(len(imported) == 17, "IMPORTED_SOURCE_LOCK_COUNT")
    added = []
    for spec in SOURCE_PATHS_NEW:
        path = REPO / spec["path"]
        require(path.is_file(), f"NEW_SOURCE_MISSING:{spec['id']}")
        text = canonical_text_bytes(path).decode("utf-8")
        for anchor in spec["anchors"]:
            require(anchor in text, f"NEW_SOURCE_ANCHOR:{spec['id']}:{anchor}")
        digest = sha256_bytes(canonical_text_bytes(path))
        require(digest == spec["expected_sha256"], f"NEW_SOURCE_HASH:{spec['id']}")
        require(
            sha256_bytes(snapshot_canonical_text_bytes(spec["path"])) == digest,
            f"NEW_SNAPSHOT_HASH:{spec['id']}",
        )
        added.append(
            {
                "id": spec["id"],
                "path": spec["path"],
                "hash_mode": HASH_MODE,
                "hash_semantics": "INTEGRITY_ONLY",
                "canonical_sha256": digest,
                "frozen_expected_sha256": spec["expected_sha256"],
                "snapshot_commit": SOURCE_SNAPSHOT_COMMIT,
                "required_anchors": list(spec["anchors"]),
                "provenance": "TPC206_NEW_DERIVATION_LOCK",
            }
        )
    locks = imported + added
    require(len(locks) == 29, "SOURCE_LOCK_COUNT")
    require(len({lock["id"] for lock in locks}) == len(locks), "SOURCE_LOCK_IDS")
    require(len({lock["path"] for lock in locks}) == len(locks), "SOURCE_LOCK_PATHS")
    return locks


def verify_snapshot_objects() -> None:
    for oid in BASELINE_TIPS:
        kind = git_output(["cat-file", "-t", oid]).strip()
        require(kind == "commit", f"BASELINE_TIP_NOT_COMMIT:{oid}")
    require(
        git_output(["merge-base", "--is-ancestor", TPC205_COMMIT, SOURCE_SNAPSHOT_COMMIT])
        == "",
        "TPC205_NOT_ANCESTOR",
    )
    changed = git_output(
        [
            "diff",
            "--name-only",
            f"{TPC205_COMMIT}..{SOURCE_SNAPSHOT_COMMIT}",
            "--",
            "papers/tpc-*",
        ]
    ).strip()
    require(changed == "", "TPC_PATH_CHANGED_AFTER_TPC205")


def batch_object_metadata(oids: list[str]) -> dict[str, tuple[str, int]]:
    input_text = "".join(f"{oid}\n" for oid in oids)
    output = git_output(
        ["cat-file", "--batch-check=%(objectname)\t%(objecttype)\t%(objectsize)"],
        input_text,
    )
    result: dict[str, tuple[str, int]] = {}
    for line in output.splitlines():
        oid, kind, size_text = line.split("\t")
        result[oid] = (kind, int(size_text))
    require(set(result) == set(oids), "OBJECT_METADATA_COVER")
    return result


def collect_json_keys(value: Any, pointer: str, hits: dict[str, list[list[str]]],
                      oid: str, path: str) -> None:
    if type(value) is dict:
        for key, child in value.items():
            escaped = key.replace("~", "~0").replace("/", "~1")
            child_pointer = f"{pointer}/{escaped}"
            if key in hits:
                value_hash = sha256_bytes(compact(child))
                hits[key].append([oid, path, child_pointer, value_hash])
            collect_json_keys(child, child_pointer, hits, oid, path)
    elif type(value) is list:
        for index, child in enumerate(value):
            collect_json_keys(child, f"{pointer}/{index}", hits, oid, path)


def batch_read_blobs(oids: list[str]) -> dict[str, bytes]:
    request = "".join(f"{oid}\n" for oid in oids).encode("ascii")
    result = subprocess.run(
        ["git", "cat-file", "--batch"],
        cwd=REPO,
        input=request,
        capture_output=True,
        check=False,
    )
    require(result.returncode == 0, "BLOB_BATCH_READ")
    output = result.stdout
    cursor = 0
    blobs: dict[str, bytes] = {}
    for expected_oid in oids:
        end = output.find(b"\n", cursor)
        require(end >= 0, f"BLOB_HEADER_TERMINATOR:{expected_oid}")
        header = output[cursor:end].decode("ascii").split()
        require(
            len(header) == 3
            and header[0] == expected_oid
            and header[1] == "blob",
            f"BLOB_HEADER:{expected_oid}",
        )
        size = int(header[2])
        cursor = end + 1
        blobs[expected_oid] = output[cursor:cursor + size]
        require(
            len(blobs[expected_oid]) == size,
            f"BLOB_PAYLOAD_SIZE:{expected_oid}",
        )
        cursor += size
        require(
            output[cursor:cursor + 1] == b"\n",
            f"BLOB_PAYLOAD_TERMINATOR:{expected_oid}",
        )
        cursor += 1
    require(cursor == len(output), "BLOB_BATCH_TRAILING_BYTES")
    return blobs


def scan_declared_git_corpus() -> dict[str, Any]:
    verify_snapshot_objects()
    refs_rows = [f"{name}\t{oid}" for name, oid in sorted(BASELINE_REF_PAIRS)]
    tips_rows = sorted(BASELINE_TIPS)
    rev_objects = git_output(["rev-list", "--objects", *BASELINE_TIPS])
    object_paths: dict[str, str] = {}
    for line in rev_objects.splitlines():
        if " " in line:
            oid, path = line.split(" ", 1)
            if oid not in object_paths or path < object_paths[oid]:
                object_paths[oid] = path
        else:
            object_paths.setdefault(line, "")
    oids = sorted(object_paths)
    metadata = batch_object_metadata(oids)
    object_rows = [
        f"{oid}\t{metadata[oid][0]}\t{metadata[oid][1]}" for oid in oids
    ]
    commits = sorted(oid for oid in oids if metadata[oid][0] == "commit")
    blobs = sorted(oid for oid in oids if metadata[oid][0] == "blob")
    trees = sorted(oid for oid in oids if metadata[oid][0] == "tree")
    text_rows: list[str] = []
    record_rows: list[str] = []
    json_rows: list[str] = []
    json_candidates: list[str] = []
    json_failures = 0
    structured_hits: dict[str, list[list[str]]] = {
        key: [] for key in STRUCTURED_KEYS
    }
    text_bytes = 0
    record_bytes = 0
    blob_bytes = sum(metadata[oid][1] for oid in blobs)
    for oid in blobs:
        path = object_paths[oid]
        lower = path.lower()
        suffix = Path(lower).suffix
        size = metadata[oid][1]
        if suffix not in TEXT_SUFFIXES:
            continue
        text_rows.append(f"{oid}\t{size}\t{path}")
        text_bytes += size
        if any(token in lower for token in RECORD_TOKENS):
            record_rows.append(f"{oid}\t{size}\t{path}")
            record_bytes += size
        if suffix == ".json":
            json_candidates.append(oid)
    json_blob_data = batch_read_blobs(json_candidates)
    for oid in json_candidates:
        path = object_paths[oid]
        size = metadata[oid][1]
        raw = json_blob_data[oid]
        try:
            value = json.loads(
                raw.decode("utf-8-sig"),
                object_pairs_hook=unique_object,
                parse_constant=reject_constant,
            )
        except (UnicodeDecodeError, json.JSONDecodeError, ValueError):
            json_failures += 1
            continue
        json_rows.append(f"{oid}\t{size}\t{path}")
        collect_json_keys(value, "", structured_hits, oid, path)
    structured = {
        "schema": "tpc-reachable-structured-key-audit-v1",
        "parseable_json_blobs": len(json_rows),
        "keys": {
            key: sorted(structured_hits[key]) for key in STRUCTURED_KEYS
        },
    }
    structured_raw = compact(structured) + b"\n"
    refs_digest, refs_bytes = tsv_digest(refs_rows)
    tips_digest, tips_bytes = tsv_digest(tips_rows)
    commits_digest, commits_bytes = tsv_digest(commits)
    objects_digest, objects_bytes = tsv_digest(object_rows)
    text_digest, text_inventory_bytes = tsv_digest(sorted(text_rows))
    record_digest, record_inventory_bytes = tsv_digest(sorted(record_rows))
    json_digest, json_inventory_bytes = tsv_digest(sorted(json_rows))
    result = {
        "definition": {
            "scope": "EXPLICIT_28_TIP_REACHABLE_GIT_OBJECT_CLOSURE",
            "working_tree_included": False,
            "untracked_included": False,
            "text_suffixes": sorted(TEXT_SUFFIXES),
            "record_path_tokens": sorted(RECORD_TOKENS),
            "structured_json_scope": "PARSEABLE_DOT_JSON_BLOBS_ONLY",
            "structured_json_parser": (
                "RFC8259_STRICT_NONFINITE_CONSTANTS_AND_DUPLICATE_KEYS_REJECTED"
            ),
            "jsonl_scope": "TEXT_AND_RECORD_INVENTORY_PLUS_SELECTED_ROW_CHECKS",
            "path_choice": "LEXICOGRAPHICALLY_MINIMUM_REACHABLE_PATH_PER_BLOB",
        },
        "scan_anchor": {
            "head": SOURCE_SNAPSHOT_COMMIT,
            "origin_main": SOURCE_SNAPSHOT_COMMIT,
            "local_main": "a5f6c645504261d36081898a6e7b11e4992fac8d",
            "ref_pairs": copy.deepcopy(sorted(BASELINE_REF_PAIRS)),
            "unique_tips": list(BASELINE_TIPS),
        },
        "counts": {
            "ref_count": len(refs_rows),
            "unique_tip_count": len(tips_rows),
            "commit_count": len(commits),
            "reachable_object_count": len(oids),
            "commit_object_count": len(commits),
            "tree_object_count": len(trees),
            "blob_object_count": len(blobs),
            "blob_bytes": blob_bytes,
            "text_blob_count": len(text_rows),
            "text_blob_bytes": text_bytes,
            "record_like_blob_count": len(record_rows),
            "record_like_blob_bytes": record_bytes,
            "parseable_json_blob_count": len(json_rows),
            "json_parse_failures": json_failures,
        },
        "inventory_bytes": {
            "refs_tsv": refs_bytes,
            "tips_lf": tips_bytes,
            "commits_lf": commits_bytes,
            "objects_tsv": objects_bytes,
            "text_tsv": text_inventory_bytes,
            "record_like_tsv": record_inventory_bytes,
            "json_tsv": json_inventory_bytes,
            "structured_keys": len(structured_raw),
        },
        "digests": {
            "refs_tsv": refs_digest,
            "tips_lf": tips_digest,
            "commits_lf": commits_digest,
            "objects_tsv": objects_digest,
            "text_tsv": text_digest,
            "record_like_tsv": record_digest,
            "json_tsv": json_digest,
            "structured_keys": sha256_bytes(structured_raw),
        },
        "structured_key_counts": {
            key: [
                len({row[0] for row in structured_hits[key]}),
                len(structured_hits[key]),
            ]
            for key in STRUCTURED_KEYS
        },
    }
    strict_equal(result["counts"], {
        key: EXPECTED_INVENTORY[key]
        for key in result["counts"]
    }, "INVENTORY_COUNTS")
    strict_equal(result["digests"], EXPECTED_INVENTORY["digests"], "INVENTORY_DIGESTS")
    strict_equal(
        result["structured_key_counts"],
        EXPECTED_STRUCTURED_KEY_COUNTS,
        "STRUCTURED_KEY_COUNTS",
    )
    return result


def build_lineage() -> dict[str, Any]:
    row_path = (
        REPO
        / "papers/tpc-133-executable-native-entrance/"
        "samples/tpc133_native_atoms.jsonl"
    )
    path_path = (
        REPO
        / "papers/tpc-134-boundary-complete-dyadic-prefix-tail-archive/"
        "samples/tpc134_paths.jsonl"
    )
    cut_path = (
        REPO
        / "papers/tpc-136-complete-native-cut-archive/"
        "samples/tpc136_cut_paths.jsonl"
    )
    alpha_id = "X=512|h0=2|ell=103|k=5|d=1"
    gamma_id = "X=512|h0=2|ell=107|k=5|d=1"
    alpha_path_id = (
        "X=512|h0=2|ell=103|k=5|d=1|jL=6|jK=3|D0=0|type=TAIL"
    )
    gamma_path_id = (
        "X=512|h0=2|ell=107|k=5|d=1|jL=6|jK=3|D0=0|type=TAIL"
    )
    alpha_cut_id = f"cut|{alpha_path_id}"
    gamma_cut_id = f"cut|{gamma_path_id}"
    row_a, row_a_line = read_jsonl_unique(row_path, "native_id", alpha_id)
    row_g, row_g_line = read_jsonl_unique(row_path, "native_id", gamma_id)
    path_a, path_a_line = read_jsonl_unique(path_path, "path_id", alpha_path_id)
    path_g, path_g_line = read_jsonl_unique(path_path, "path_id", gamma_path_id)
    cut_a, cut_a_line = read_jsonl_unique(cut_path, "cut_path_id", alpha_cut_id)
    cut_g, cut_g_line = read_jsonl_unique(cut_path, "cut_path_id", gamma_cut_id)
    records = [row_a, row_g, path_a, path_g, cut_a, cut_g]
    for record in records:
        verify_integrity(record)
    strict_equal(
        [row_a_line, row_g_line, path_a_line, path_g_line, cut_a_line, cut_g_line],
        [724, 736, 2554, 2602, 2554, 2602],
        "SELECTED_DIAGNOSTIC_LINES",
    )
    strict_equal(row_a["native_tuple"], [103, 5, 1], "ALPHA_ROW")
    strict_equal(row_g["native_tuple"], [107, 5, 1], "GAMMA_ROW")
    for row in [row_a, row_g]:
        strict_equal(
            row["packet_scope"],
            {
                "Q": 4,
                "U": 2,
                "V": 2,
                "X": 512,
                "h0": 2,
                "physical_normalization": "nu_X",
                "weight_source_id": "sample-symbolic-bump-v1",
            },
            "ROW_PACKET_SCOPE",
        )
    strict_equal(
        path_a["metadata"]["parent_integrity_sha256"],
        row_a["integrity_sha256"],
        "A_PARENT",
    )
    strict_equal(
        path_g["metadata"]["parent_integrity_sha256"],
        row_g["integrity_sha256"],
        "G_PARENT",
    )
    strict_equal(
        cut_a["metadata"]["upstream_integrity_sha256"],
        path_a["integrity_sha256"],
        "A_UPSTREAM",
    )
    strict_equal(
        cut_g["metadata"]["upstream_integrity_sha256"],
        path_g["integrity_sha256"],
        "G_UPSTREAM",
    )
    for path, cut in [(path_a, cut_a), (path_g, cut_g)]:
        strict_equal(path["block"], {"j_K": 3, "j_L": 6}, "PATH_BLOCK")
        strict_equal(cut["metadata"]["block"], {"j_K": 3, "j_L": 6}, "CUT_BLOCK")
        strict_equal(path["D0"], 0, "PATH_D0")
        strict_equal(cut["metadata"]["D0"], 0, "CUT_D0")
        require(cut["cut_terminal_type"] == "FRONTIER_UNMAPPED", "CUT_TERMINAL")
        require(cut["metadata"]["frontier_reason"] == "NO_TAIL_ROOM", "CUT_REASON")
    manifest_path = (
        REPO
        / "papers/tpc-133-executable-native-entrance/"
        "samples/tpc133_packet_manifest.json"
    )
    certificate_path = (
        REPO
        / "papers/tpc-133-executable-native-entrance/"
        "experiments/tpc133_native_entrance_certificate.json"
    )
    frontier_path = (
        REPO
        / "papers/tpc-135-tpc17-tpc18-block-frontier/"
        "samples/tpc135_frontier_manifest.json"
    )
    manifest = load_json(manifest_path)
    certificate = load_json(certificate_path)
    frontier = load_json(frontier_path)
    strict_equal(
        manifest["delta"], {"numerator": 1, "denominator": 4}, "MANIFEST_DELTA"
    )
    require(
        sha256_bytes(canonical_text_bytes(manifest_path))
        == TPC133_MANIFEST_SHA256,
        "MANIFEST_HASH",
    )
    strict_equal(
        certificate["packet"],
        {
            "Q": 4,
            "U": 2,
            "V": 2,
            "X": 512,
            "delta": "1/4",
            "h0": 2,
            "physical_normalization": "nu_X",
            "support_proof_id": "sample-manifest-declaration-only",
            "weight_source_id": "sample-symbolic-bump-v1",
        },
        "TPC133_CERTIFICATE_PACKET",
    )
    require(certificate["archive"]["record_count"] == 866, "TPC133_RECORD_COUNT")
    require(
        certificate["archive"]["jsonl_sha256"]
        == sha256_bytes(row_path.read_bytes()),
        "TPC133_CERTIFICATE_ARCHIVE_HASH",
    )
    strict_equal(
        {
            key: frontier["scope"][key]
            for key in ["R", "V", "X", "h0", "physical_normalization"]
        },
        {
            "R": 4,
            "V": 2,
            "X": 512,
            "h0": 2,
            "physical_normalization": "nu_X",
        },
        "TPC135_TYPED_SCOPE",
    )
    for path, cut in [(path_a, cut_a), (path_g, cut_g)]:
        require(path["metadata"]["Q"] == frontier["scope"]["R"], "Q_TO_R_BRIDGE")
        require(cut["metadata"]["Q"] == frontier["scope"]["R"], "CUT_Q_TO_R_BRIDGE")
    require(4 ** 4 <= 512 < 5 ** 4, "TRUNCATION_INTEGER_CHECK")
    require(math.isqrt(4) == 2, "V_INTEGER_CHECK")
    require(2 ** 6 == 64 and 2 ** 3 == 8, "DYADIC_VALUES")
    require(103 * 1 * 5 + 2 == 517, "N_ALPHA")
    require(107 * 1 * 5 + 2 == 537, "N_GAMMA")
    return {
        "candidate_id": "TPC206_SELECTED_DUAL_ROW_13_FIELD_PROJECTION",
        "orientation": "ORDERED_ALPHA_103_GAMMA_107_NO_SWAP_QUOTIENT",
        "evidence_level": "ROW_AND_CUT_SCOPE_WITH_EXACT_TYPED_DERIVATIONS",
        "production_occurrence": False,
        "selected_records": [
            {
                "role": "alpha_row",
                "path": str(row_path.relative_to(REPO)).replace("\\", "/"),
                "semantic_id": alpha_id,
                "diagnostic_line": row_a_line,
                "integrity_sha256": row_a["integrity_sha256"],
            },
            {
                "role": "gamma_row",
                "path": str(row_path.relative_to(REPO)).replace("\\", "/"),
                "semantic_id": gamma_id,
                "diagnostic_line": row_g_line,
                "integrity_sha256": row_g["integrity_sha256"],
            },
            {
                "role": "alpha_path",
                "path": str(path_path.relative_to(REPO)).replace("\\", "/"),
                "semantic_id": alpha_path_id,
                "diagnostic_line": path_a_line,
                "integrity_sha256": path_a["integrity_sha256"],
                "parent_integrity_sha256": path_a["metadata"][
                    "parent_integrity_sha256"
                ],
            },
            {
                "role": "gamma_path",
                "path": str(path_path.relative_to(REPO)).replace("\\", "/"),
                "semantic_id": gamma_path_id,
                "diagnostic_line": path_g_line,
                "integrity_sha256": path_g["integrity_sha256"],
                "parent_integrity_sha256": path_g["metadata"][
                    "parent_integrity_sha256"
                ],
            },
            {
                "role": "alpha_cut",
                "path": str(cut_path.relative_to(REPO)).replace("\\", "/"),
                "semantic_id": alpha_cut_id,
                "diagnostic_line": cut_a_line,
                "integrity_sha256": cut_a["integrity_sha256"],
                "upstream_integrity_sha256": cut_a["metadata"][
                    "upstream_integrity_sha256"
                ],
            },
            {
                "role": "gamma_cut",
                "path": str(cut_path.relative_to(REPO)).replace("\\", "/"),
                "semantic_id": gamma_cut_id,
                "diagnostic_line": cut_g_line,
                "integrity_sha256": cut_g["integrity_sha256"],
                "upstream_integrity_sha256": cut_g["metadata"][
                    "upstream_integrity_sha256"
                ],
            },
        ],
        "exact_derivations": [
            {
                "field_id": "delta",
                "rule_id": "TPC133_CHOSEN_MANIFEST_CERTIFICATE_ARCHIVE_PROVENANCE",
                "result": {"numerator": 1, "denominator": 4},
                "scope": "FINITE_X_512_MANIFEST_ONLY_NOT_CROSS_SCALE_SCHEDULE",
                "manifest_path": str(manifest_path.relative_to(REPO)).replace(
                    "\\", "/"
                ),
                "manifest_canonical_sha256": TPC133_MANIFEST_SHA256,
                "archive_sha256": certificate["archive"]["jsonl_sha256"],
            },
            {
                "field_id": "R",
                "rule_id": "TPC133_TRUNCATION_Q_TO_TPC18_R_TYPED_ALIAS",
                "result": 4,
                "firewall": "DO_NOT_FILL_TPC18_ROW_SCALE_Q",
            },
            {
                "field_id": "L",
                "rule_id": "TPC134_L_EQUALS_TWO_TO_JL",
                "inputs": {"j_L": 6},
                "result": 64,
            },
            {
                "field_id": "K",
                "rule_id": "TPC134_K_EQUALS_TWO_TO_JK",
                "inputs": {"j_K": 3},
                "result": 8,
            },
            {
                "field_id": "j_and_targets",
                "rule_id": "TPC18_NATIVE_k_EQUALS_d_TIMES_j_AND_N_EQUALS_ell_d_j_PLUS_h0",
                "inputs": {
                    "alpha_native_tuple": [103, 5, 1],
                    "gamma_native_tuple": [107, 5, 1],
                    "h0": 2,
                },
                "result": {"j": 5, "N_alpha": 517, "N_gamma": 537},
                "firewall": "LOWERCASE_NATIVE_k_5_IS_NOT_DYADIC_K_8",
            },
        ],
        "id_envelope": {
            "projection_id": (
                "projection|X=512|h0=2|delta=1/4|"
                f"manifest={TPC133_MANIFEST_SHA256}|"
                "alpha=103,1|gamma=107,1|j=5"
            ),
            "projection_id_semantics": (
                "SELECTED_PROVENANCE_PROJECTION_ID_NOT_PRODUCTION_ID"
            ),
            "pair_record_id": None,
            "edge_instance_id": None,
            "target_occurrence_id": None,
            "id_fields_counted_inside_42": False,
            "projection_provenance_locator_is_not_joint_production_source_locator": True,
        },
    }


def build_selected_lineage_graph(lineage: dict[str, Any]) -> dict[str, Any]:
    records = {row["role"]: row for row in lineage["selected_records"]}
    nodes = [
        {
            "node_id": "record:alpha_row",
            "kind": "SOURCE_RECORD",
            "source_roles": ["alpha_row"],
            "integrity_sha256": records["alpha_row"]["integrity_sha256"],
            "provides": {
                "X": 512,
                "h0": 2,
                "V": 2,
                "alpha=(ell_alpha,d_alpha)": [103, 1],
            },
        },
        {
            "node_id": "record:gamma_row",
            "kind": "SOURCE_RECORD",
            "source_roles": ["gamma_row"],
            "integrity_sha256": records["gamma_row"]["integrity_sha256"],
            "provides": {
                "X": 512,
                "h0": 2,
                "V": 2,
                "gamma=(ell_gamma,d_gamma)": [107, 1],
            },
        },
        {
            "node_id": "record:alpha_path",
            "kind": "SOURCE_RECORD",
            "source_roles": ["alpha_path"],
            "integrity_sha256": records["alpha_path"]["integrity_sha256"],
            "provides": {"D0": 0},
        },
        {
            "node_id": "record:gamma_path",
            "kind": "SOURCE_RECORD",
            "source_roles": ["gamma_path"],
            "integrity_sha256": records["gamma_path"]["integrity_sha256"],
            "provides": {"D0": 0},
        },
        {
            "node_id": "record:alpha_cut",
            "kind": "SOURCE_RECORD",
            "source_roles": ["alpha_cut"],
            "integrity_sha256": records["alpha_cut"]["integrity_sha256"],
            "provides": {},
        },
        {
            "node_id": "record:gamma_cut",
            "kind": "SOURCE_RECORD",
            "source_roles": ["gamma_cut"],
            "integrity_sha256": records["gamma_cut"]["integrity_sha256"],
            "provides": {},
        },
        {
            "node_id": "derive:chosen_manifest_delta",
            "kind": "LOCKED_TYPED_DERIVATION",
            "source_roles": ["alpha_row", "gamma_row"],
            "rule_id": "TPC133_CHOSEN_MANIFEST_CERTIFICATE_ARCHIVE_PROVENANCE",
            "provides": {"delta": {"numerator": 1, "denominator": 4}},
        },
        {
            "node_id": "derive:truncation_R",
            "kind": "LOCKED_TYPED_DERIVATION",
            "source_roles": ["alpha_path", "gamma_path"],
            "rule_id": "TPC133_TRUNCATION_Q_TO_TPC18_R_TYPED_ALIAS",
            "provides": {"R": 4},
            "firewall": "TPC18_ROW_SCALE_Q_REMAINS_MISSING",
        },
        {
            "node_id": "derive:dyadic_L_K",
            "kind": "LOCKED_TYPED_DERIVATION",
            "source_roles": ["alpha_path", "gamma_path"],
            "rule_id": "TPC134_L_K_EQUAL_POW2_OF_jL_jK",
            "provides": {"L": 64, "K": 8},
        },
        {
            "node_id": "derive:native_j_targets",
            "kind": "LOCKED_TYPED_DERIVATION",
            "source_roles": ["alpha_row", "gamma_row"],
            "rule_id": (
                "TPC18_NATIVE_k_EQUALS_d_TIMES_j_AND_"
                "N_EQUALS_ell_d_j_PLUS_h0"
            ),
            "provides": {"j": 5, "N_alpha(j)": 517, "N_gamma(j)": 537},
            "firewall": "LOWERCASE_NATIVE_k_5_IS_NOT_DYADIC_K_8",
        },
    ]
    edges = [
        ["record:alpha_row", "record:alpha_path", "PARENT_INTEGRITY"],
        ["record:gamma_row", "record:gamma_path", "PARENT_INTEGRITY"],
        ["record:alpha_path", "record:alpha_cut", "UPSTREAM_INTEGRITY"],
        ["record:gamma_path", "record:gamma_cut", "UPSTREAM_INTEGRITY"],
        [
            "derive:chosen_manifest_delta",
            "record:alpha_row",
            "CERTIFICATE_ARCHIVE_HASH",
        ],
        [
            "derive:chosen_manifest_delta",
            "record:gamma_row",
            "CERTIFICATE_ARCHIVE_HASH",
        ],
        ["record:alpha_path", "derive:truncation_R", "TYPED_Q_TO_R"],
        ["record:gamma_path", "derive:truncation_R", "TYPED_Q_TO_R"],
        ["record:alpha_path", "derive:dyadic_L_K", "BLOCK_EXPONENTS"],
        ["record:gamma_path", "derive:dyadic_L_K", "BLOCK_EXPONENTS"],
        ["record:alpha_row", "derive:native_j_targets", "NATIVE_TUPLE"],
        ["record:gamma_row", "derive:native_j_targets", "NATIVE_TUPLE"],
    ]
    closure: dict[str, dict[str, Any]] = {}
    for node in nodes:
        for field_id, value in node["provides"].items():
            if field_id in closure:
                strict_equal(closure[field_id]["value"], value, f"GRAPH_VALUE:{field_id}")
                closure[field_id]["providers"].append(node["node_id"])
            else:
                closure[field_id] = {
                    "field_id": field_id,
                    "value": copy.deepcopy(value),
                    "providers": [node["node_id"]],
                }
    contract_order = [field for fields in FIELD_BLOCKS.values() for field in fields]
    closure_rows = [closure[field] for field in contract_order if field in closure]
    strict_equal(
        {row["field_id"]: row["value"] for row in closure_rows},
        MATERIALIZED_VALUES,
        "GRAPH_FIELD_CLOSURE",
    )
    require(len(nodes) == 10 and len(edges) == 12, "GRAPH_SIZE")
    require(len(closure_rows) == 13, "GRAPH_CLOSURE_COUNT")
    return {
        "graph_id": DECLARED_CORPUS,
        "scope": "EXPLICIT_SIX_RECORD_PLUS_FOUR_TYPED_DERIVATION_NODES",
        "nodes": nodes,
        "dependency_edges": edges,
        "field_closure": closure_rows,
        "field_closure_count": len(closure_rows),
        "closed_under_declared_nodes": True,
        "external_nodes_are_not_implicitly_joinable": True,
        "corpus_wide_candidate_graph_enumerated": False,
        "corpus_wide_maximality_inferred": False,
    }


def build_field_ledger(graph: dict[str, Any]) -> list[dict[str, Any]]:
    closure = {row["field_id"]: row for row in graph["field_closure"]}
    rows = []
    ordinal = 0
    for block, fields in FIELD_BLOCKS.items():
        for field_id in fields:
            ordinal += 1
            materialized = field_id in closure
            rows.append(
                {
                    "one_based_index": ordinal,
                    "block": block,
                    "field_id": field_id,
                    "value_state": (
                        "DERIVED_EXACT"
                        if materialized
                        and DERIVATION_RULES[field_id]
                        not in {
                            "TPC133_SELECTED_ROWS_LITERAL_PACKET_SCOPE",
                            "TPC134_TPC136_SELECTED_PATH_LITERAL",
                        }
                        else "LITERAL"
                        if materialized
                        else "MISSING"
                    ),
                    "evidence_mode": (
                        "THEOREM_CROSSWALK"
                        if materialized
                        and DERIVATION_RULES[field_id]
                        not in {
                            "TPC133_SELECTED_ROWS_LITERAL_PACKET_SCOPE",
                            "TPC134_TPC136_SELECTED_PATH_LITERAL",
                        }
                        else "ROW_ONLY"
                        if materialized
                        else "NONE"
                    ),
                    "counts_as_legal_partial_projection": materialized,
                    "counts_as_production_record": False,
                    "value": (
                        copy.deepcopy(closure[field_id]["value"])
                        if materialized
                        else None
                    ),
                    "provider_node_ids": (
                        list(closure[field_id]["providers"]) if materialized else []
                    ),
                    "derivation_rule_id": (
                        DERIVATION_RULES[field_id] if materialized else None
                    ),
                    "blocker": None if materialized else FIELD_BLOCKERS[field_id],
                }
            )
    require(len(rows) == 42, "FIELD_LEDGER_COUNT")
    require(sum(row["counts_as_legal_partial_projection"] for row in rows) == 13,
            "FIELD_LEDGER_PASS_COUNT")
    require(sum(not row["counts_as_legal_partial_projection"] for row in rows) == 29,
            "FIELD_LEDGER_MISSING_COUNT")
    first = next(row for row in rows if not row["counts_as_legal_partial_projection"])
    require(
        first["field_id"] == FIRST_MISSING_FIELD
        and first["one_based_index"] == FIRST_MISSING_INDEX,
        "FIRST_MISSING_FIELD",
    )
    return rows


def build_selected_non_splicing_ledger(
    field_ledger: list[dict[str, Any]],
) -> list[dict[str, Any]]:
    rows = []
    for row in field_ledger:
        if row["counts_as_legal_partial_projection"]:
            continue
        rows.append(
            {
                "field_id": row["field_id"],
                "selected_graph_status": "MISSING",
                "selected_graph_provider_count": 0,
                "blocker": row["blocker"],
                "external_donor_policy": "DISALLOWED_CROSS_LINEAGE_SPLICE",
                "absence_claim_scope": "EXPLICIT_SELECTED_GRAPH_ONLY",
                "global_absence_claim": False,
            }
        )
    require(len(rows) == 29, "SELECTED_NON_SPLICING_LEDGER_COUNT")
    return rows


def build_payload(include_scan: bool = True) -> dict[str, Any]:
    source_locks = build_source_locks()
    lineage = build_lineage()
    graph = build_selected_lineage_graph(lineage)
    fields = build_field_ledger(graph)
    non_splicing = build_selected_non_splicing_ledger(fields)
    scan = scan_declared_git_corpus() if include_scan else None
    return {
        "schema": "tpc-206-selected-lineage-pair-registry-v1",
        "paper": PAPER_NUMBER,
        "parent_paper": PARENT_PAPER,
        "authorization": {
            "scope": AUTHORIZATION_SCOPE,
            "user_authorized": True,
            "continuing_numbering_authorization": True,
            "authorization_is_theorem_evidence": False,
        },
        "classification": CLASSIFICATION,
        "theorem_status": THEOREM_STATUS,
        "verdict": VERDICT,
        "source_snapshot_commit": SOURCE_SNAPSHOT_COMMIT,
        "declared_corpus": {
            "id": DECLARED_CORPUS,
            "scope": (
                "EXPLICIT_SELECTED_SIX_RECORD_PLUS_FOUR_TYPED_DERIVATION_GRAPH"
            ),
            "future_sources_excluded": True,
            "unknown_encodings_excluded": True,
            "nonexistence_scope": "SELECTED_LINEAGE_GRAPH_ONLY",
            "archive_census_role": (
                "CONTEXT_AND_REOPEN_TRIGGER_AUDIT_NOT_MAXIMALITY_EVIDENCE"
            ),
            "jsonl_semantic_census_complete": False,
            "corpus_wide_candidate_graph_enumerated": False,
        },
        "archive_census": scan,
        "source_locks": source_locks,
        "contract_import": {
            "parent_required_fields": copy.deepcopy(FIELD_BLOCKS),
            "required_field_count": 42,
            "three_id_envelope_is_outside_42": True,
            "ordered_pair_quotient": "FORBIDDEN",
        },
        "legal_join_rules": {
            "same_connected_lineage_required": True,
            "semantic_id_and_integrity_chain_required": True,
            "shared_numeric_values_are_not_join_keys": True,
            "cross_candidate_patchwork": "FORBIDDEN",
            "selected_row_only_fields_may_form_selected_projection": True,
            "row_only_fields_may_form_production_record": False,
            "derived_L0_fields_may_form_production_record": False,
            "external_L0_fixture_may_extend_selected_projection": False,
            "label_only_normalization_counts": False,
            "formula_type_without_record_attachment_counts": False,
            "undecided_nonzero_counts": False,
        },
        "selected_projection": lineage,
        "selected_lineage_graph": graph,
        "field_ledger": fields,
        "selected_non_splicing_ledger": non_splicing,
        "comparison_fixture": {
            "id": "TPC32_TPC93_DERIVED_L0_ONLY",
            "direct_fields": {
                "L": 100,
                "R": 12,
                "T": 50,
                "U0": 200,
                "h0": 2,
                "j": 1,
                "alpha": [59, 1],
                "gamma": [71, 1],
            },
            "derived_child_fields": {
                "polarization": "L",
                "u": 61,
                "sigma": 1,
                "v": 1,
                "t": 1,
                "projector_weight": 1,
            },
            "evidence_mode": "DERIVED_L0_ONLY",
            "partial_field_count_in_its_own_fixture": 14,
            "production_occurrence": False,
            "same_packet_or_source_key_as_selected_projection": False,
            "legal_join_with_selected_projection": False,
            "reason": "DISALLOWED_CROSS_LINEAGE_SPLICE_INTO_SELECTED_GRAPH",
            "corpus_wide_maximality_consequence": "NOT_EVALUATED",
        },
        "selected_lineage_theorem": {
            "required_fields": 42,
            "selected_graph_materialized_fields": 13,
            "missing_fields": 29,
            "full_completions_inside_explicit_selected_graph": 0,
            "production_occurrences_inside_explicit_selected_graph": 0,
            "selected_graph_closed_under_declared_nodes": True,
            "theorem_scope": "EXPLICIT_SELECTED_LINEAGE_GRAPH_ONLY",
            "corpus_wide_maximum_materialized_fields": None,
            "corpus_wide_full_join_count": None,
            "corpus_wide_maximality_status": "NOT_TESTABLE",
            "first_missing_field_id": FIRST_MISSING_FIELD,
            "first_missing_field_index": FIRST_MISSING_INDEX,
            "first_missing": FIRST_MISSING,
            "parent_first_missing": PARENT_FIRST_MISSING,
            "first_failed_subgate": (
                "PAIR_NATIVE_POST_TTSTAR_ACTUAL_REGISTRY_WITH_FULL_"
                "LITERAL_SCOPE_AND_COEFFICIENT"
            ),
        },
        "downstream_gates": [
            {
                "id": "SOURCE_LOCKED_SELECTED_LINEAGE_13_OF_42_PARTIAL_PROJECTION",
                "status": "PASS_L1_SELECTED_GRAPH",
            },
            {
                "id": "SELECTED_LINEAGE_CLOSURE_UNDER_DECLARED_DERIVATIONS",
                "status": "PASS_L1_SELECTED_GRAPH",
            },
            {
                "id": "SELECTED_LINEAGE_FULL_COMPLETION",
                "status": "FAIL",
            },
            {
                "id": "CORPUS_WIDE_MAXIMALITY",
                "status": "NOT_TESTABLE",
            },
            {
                "id": "ACTIVE_PRODUCTION_PAIR_OCCURRENCE",
                "status": "NOT_TESTABLE",
            },
            {
                "id": "SOURCE_LOCKED_PAIR_TO_OMEGA_CROSSWALK",
                "status": "FAIL",
            },
            {
                "id": "GLOBAL_NORMALIZATION_RETURN",
                "status": "FAIL",
            },
            {
                "id": "H1_E_REPAIR",
                "status": "FAIL",
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
                "id": "PAIR_NATIVE_ARCHITECTURE_REROUTE_CANDIDATE",
                "status": "OPEN",
            },
        ],
        "claim_firewall": {
            "production_pair_occurrence_proved": False,
            "pair_to_omega_crosswalk_proved": False,
            "H1_E_repair_proved": False,
            "mathematical_reopen": False,
            "structural_reopen": False,
            "fixed_atom_decay_obtained": False,
            "positive_sigma_obtained": False,
            "strict_one_over_400_paid": False,
            "fixed_atom_credit": 0,
            "program_positive_L2": False,
            "L2_result": "NONE",
            "twin_prime_theorem": False,
        },
        "route_state": {
            "pair_native_architecture_reroute": "OPEN",
            "bad_endpoint_O161_parent": "OPEN",
            "direct_twist_O161_parent": "OPEN",
            "H1_architecture": "OPEN",
            "global_architecture": "OPEN",
        },
        "stop_scoped": copy.deepcopy(STOP_SCOPED),
        "decision": {
            "workflow_authorization_mode": "CONTINUING_NO_SEPARATE_NUMBERING_GATE",
            "next_paper": None,
            "mathematical_gate_required_for_any_next_paper": True,
        },
        "summary_counts": {
            "source_locks": len(source_locks),
            "required_fields": 42,
            "materialized_fields": 13,
            "missing_fields": 29,
            "selected_non_splicing_rows": len(non_splicing),
            "selected_graph_nodes": len(graph["nodes"]),
            "selected_graph_edges": len(graph["dependency_edges"]),
            "selected_row_records": 2,
            "selected_path_records": 2,
            "selected_cut_records": 2,
            "selected_ordered_projections": 1,
            "selected_lineage_full_completions": 0,
            "selected_lineage_production_occurrences": 0,
            "comparison_fixture_partial_fields": 14,
            "corpus_wide_maximum": None,
            "semantic_mutations": len(SEMANTIC_MUTATIONS),
            "base_mutations": len(BASE_MUTATIONS),
            "strict_type_mutations": len(STRICT_TYPE_MUTATIONS),
        },
    }


def build_audit(payload: dict[str, Any], payload_schema: dict[str, Any]) -> dict[str, Any]:
    base_rows = build_mutation_rows(
        payload, payload_schema, BASE_MUTATIONS, "base"
    )
    semantic_rows = build_mutation_rows(
        payload, payload_schema, SEMANTIC_MUTATIONS, "semantic"
    )
    strict_rows = build_mutation_rows(
        payload, payload_schema, STRICT_TYPE_MUTATIONS, "strict"
    )
    return {
        "schema": "tpc-206-selected-lineage-pair-registry-audit-v1",
        "paper": PAPER_NUMBER,
        "payload_sha256": sha256_bytes(canonical(payload).encode("utf-8")),
        "payload_schema_sha256": sha256_bytes(
            canonical(payload_schema).encode("utf-8")
        ),
        "checks": [
            "SOURCE_LOCKS_29_REVERIFIED",
            "EXPLICIT_28_TIP_GIT_CLOSURE_REBUILT",
            "STRUCTURED_JSON_KEY_AUDIT_REBUILT",
            "SEMANTIC_SELECTORS_UNIQUE",
            "SIX_RECORD_INTEGRITY_CHAIN_REBUILT",
            "TPC133_MANIFEST_CERTIFICATE_ARCHIVE_CHAIN_REBUILT",
            "TPC133_Q_TO_TPC18_R_TYPED_ALIAS_REBUILT",
            "TPC134_DYADIC_VALUES_REBUILT",
            "SELECTED_GRAPH_10_NODES_12_EDGES_REBUILT",
            "FIELD_LEDGER_42_ROWS",
            "MATERIALIZED_13_MISSING_29",
            "FIRST_MISSING_D_INDEX_9",
            "SELECTED_NON_SPLICING_29_ROWS",
            "TPC32_TPC93_L0_SPLICE_REJECTED",
            "SELECTED_LINEAGE_FULL_COMPLETION_ZERO",
            "CORPUS_WIDE_MAXIMALITY_NOT_TESTABLE",
            "CLAIM_FIREWALL_LOCKED",
            "STOP_SCOPED_PRESERVED",
        ],
        "mutation_contract": {
            "base_exact_schema_mutations": base_rows,
            "coordinated_semantic_mutations": semantic_rows,
            "strict_bool_int_mutations": strict_rows,
            "active_schema_rejections": len(base_rows)
            + len(semantic_rows)
            + len(strict_rows),
            "regenerated_exact_schema_acceptances": len(base_rows)
            + len(semantic_rows)
            + len(strict_rows),
            "expected_reconstruction_semantic_rejections": len(semantic_rows),
            "all_rejected": True,
        },
        "parser_firewall": {
            "duplicate_json_keys_rejected": True,
            "NaN_and_Infinity_rejected": True,
            "canonical_payload_bytes_required": True,
            "python_optimized_mode_fails_closed": True,
        },
        "manifest_trust": {
            "mode": "REPOSITORY_PIN_REQUIRES_GIT_REVIEW_NOT_EXTERNAL_SIGNATURE",
            "external_signature": False,
            "theorem_evidence": False,
        },
        "summary": {
            "source_locks_verified": 29,
            "archive_objects_verified": payload["archive_census"]["counts"][
                "reachable_object_count"
            ],
            "fields_verified": 42,
            "materialized_fields_verified": 13,
            "missing_fields_verified": 29,
            "selected_graph_nodes_verified": 10,
            "selected_graph_edges_verified": 12,
            "selected_non_splicing_rows_verified": 29,
            "selected_lineage_full_completions": 0,
            "corpus_wide_maximality": "NOT_TESTABLE",
            "mathematical_reopen": False,
            "verdict": VERDICT,
        },
    }


def validate_payload(payload: dict[str, Any]) -> dict[str, Any]:
    expected = build_payload(include_scan=True)
    strict_equal(payload, expected, "PAYLOAD")
    return {
        "source_locks_verified": 29,
        "archive_objects_verified": payload["archive_census"]["counts"][
            "reachable_object_count"
        ],
        "fields_verified": 42,
        "materialized_fields_verified": 13,
        "missing_fields_verified": 29,
        "selected_graph_nodes_verified": 10,
        "selected_graph_edges_verified": 12,
        "selected_non_splicing_rows_verified": 29,
        "selected_lineage_full_completions": 0,
        "corpus_wide_maximality": "NOT_TESTABLE",
        "mathematical_reopen": False,
        "verdict": VERDICT,
    }


def materialize() -> None:
    payload = build_payload(include_scan=True)
    payload_schema = exact_schema(
        payload, "TPC-206 selected-lineage pair-registry projection"
    )
    audit = build_audit(payload, payload_schema)
    audit_schema = exact_schema(
        audit, "TPC-206 selected-lineage pair-registry projection audit"
    )
    PAYLOAD_PATH.parent.mkdir(parents=True, exist_ok=True)
    PAYLOAD_SCHEMA_PATH.parent.mkdir(parents=True, exist_ok=True)
    PAYLOAD_PATH.write_text(canonical(payload), encoding="utf-8", newline="\n")
    PAYLOAD_SCHEMA_PATH.write_text(
        canonical(payload_schema), encoding="utf-8", newline="\n"
    )
    AUDIT_PATH.write_text(canonical(audit), encoding="utf-8", newline="\n")
    AUDIT_SCHEMA_PATH.write_text(
        canonical(audit_schema), encoding="utf-8", newline="\n"
    )


def refresh_manifest() -> dict[str, Any]:
    artifacts = []
    for relative in ACTIVE_ARTIFACTS:
        path = REPO / relative
        require(path.is_file(), f"MANIFEST_ARTIFACT_MISSING:{relative}")
        artifacts.append(
            {
                "path": relative,
                "raw_sha256": sha256_bytes(path.read_bytes()),
                "bytes": path.stat().st_size,
            }
        )
    manifest = {
        "schema": "tpc-206-certificate-manifest-v1",
        "paper": PAPER_NUMBER,
        "trust_mode": "REPOSITORY_PIN_REQUIRES_GIT_REVIEW_NOT_EXTERNAL_SIGNATURE",
        "artifacts": artifacts,
        "summary": {
            "artifacts_pinned": len(artifacts),
            "required_fields": 42,
            "materialized_fields": 13,
            "missing_fields": 29,
            "selected_lineage_full_completions": 0,
            "corpus_wide_maximality": "NOT_TESTABLE",
            "verdict": VERDICT,
        },
    }
    MANIFEST_PATH.write_text(canonical(manifest), encoding="utf-8", newline="\n")
    return manifest


def verify_manifest() -> dict[str, Any]:
    require(MANIFEST_PATH.is_file(), "MANIFEST_REQUIRED")
    manifest = load_json(MANIFEST_PATH, canonical_bytes=True)
    strict_equal(
        set(manifest),
        {"schema", "paper", "trust_mode", "artifacts", "summary"},
        "MANIFEST_TOP_KEYS",
    )
    require(manifest["schema"] == "tpc-206-certificate-manifest-v1", "MANIFEST_SCHEMA")
    require(type(manifest["paper"]) is int and manifest["paper"] == PAPER_NUMBER,
            "MANIFEST_PAPER")
    require(
        manifest["trust_mode"]
        == "REPOSITORY_PIN_REQUIRES_GIT_REVIEW_NOT_EXTERNAL_SIGNATURE",
        "MANIFEST_TRUST_MODE",
    )
    require(type(manifest["artifacts"]) is list, "MANIFEST_ARTIFACT_TYPE")
    strict_equal(
        [item["path"] for item in manifest["artifacts"]],
        ACTIVE_ARTIFACTS,
        "MANIFEST_PATHS",
    )
    for item in manifest["artifacts"]:
        strict_equal(
            set(item), {"path", "raw_sha256", "bytes"}, "MANIFEST_ROW_KEYS"
        )
        require(type(item["path"]) is str, "MANIFEST_PATH_TYPE")
        require(
            type(item["raw_sha256"]) is str
            and len(item["raw_sha256"]) == 64
            and all(ch in "0123456789abcdef" for ch in item["raw_sha256"]),
            f"MANIFEST_HASH_TYPE:{item['path']}",
        )
        require(
            type(item["bytes"]) is int and item["bytes"] >= 0,
            f"MANIFEST_BYTES_TYPE:{item['path']}",
        )
        path = REPO / item["path"]
        require(path.is_file(), f"MANIFEST_MISSING:{item['path']}")
        require(path.stat().st_size == item["bytes"], f"MANIFEST_SIZE:{item['path']}")
        require(
            sha256_bytes(path.read_bytes()) == item["raw_sha256"],
            f"MANIFEST_HASH:{item['path']}",
        )
    strict_equal(
        manifest["summary"],
        {
            "artifacts_pinned": len(ACTIVE_ARTIFACTS),
            "required_fields": 42,
            "materialized_fields": 13,
            "missing_fields": 29,
            "selected_lineage_full_completions": 0,
            "corpus_wide_maximality": "NOT_TESTABLE",
            "verdict": VERDICT,
        },
        "MANIFEST_SUMMARY",
    )
    return {
        "artifacts_pinned": len(ACTIVE_ARTIFACTS),
        "trust_mode": manifest["trust_mode"],
    }


def verify_active_artifacts() -> dict[str, Any]:
    payload = load_json(PAYLOAD_PATH, canonical_bytes=True)
    payload_schema = load_json(PAYLOAD_SCHEMA_PATH, canonical_bytes=True)
    audit = load_json(AUDIT_PATH, canonical_bytes=True)
    audit_schema = load_json(AUDIT_SCHEMA_PATH, canonical_bytes=True)
    verify_exact_schema(
        payload, payload_schema, "PAYLOAD_SCHEMA"
    )
    verify_exact_schema(
        audit, audit_schema, "AUDIT_SCHEMA"
    )
    result = validate_payload(payload)
    strict_equal(
        audit, build_audit(payload, payload_schema), "AUDIT"
    )
    return result


def main() -> None:
    if not __debug__:
        raise RuntimeError("TPC-206 certificate fails closed under optimized Python")
    parser = argparse.ArgumentParser()
    parser.add_argument("--check", action="store_true")
    parser.add_argument("--refresh-manifest", action="store_true")
    args = parser.parse_args()
    if not args.check:
        materialize()
    result = verify_active_artifacts()
    manifest = None
    if args.refresh_manifest:
        manifest = refresh_manifest()
    elif args.check:
        manifest = verify_manifest()
    print(
        json.dumps(
            {
                "paper": PAPER_NUMBER,
                "materialized": not args.check,
                "check": True,
                "verdict": VERDICT,
                "certificate": result,
                "manifest": manifest,
            },
            sort_keys=True,
        )
    )


if __name__ == "__main__":
    main()
