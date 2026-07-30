#!/usr/bin/env python3
"""Independent read-only verifier for the finite TPC-206 theorem.

This checker imports neither the builder nor the authoritative materializer.
It independently rebuilds the frozen Git-object census, source locks, selected
lineage chains, exact schemas, finite field count, selected-graph no-splicing
closure, claim firewall, mutation registry, and strict release manifest.
"""

from __future__ import annotations

import argparse
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
PAYLOAD_SCHEMA_PATH = (
    PAPER / "schemas" / "tpc206-selected-lineage-pair-registry-v1.schema.json"
)
AUDIT_SCHEMA_PATH = (
    PAPER
    / "schemas"
    / "tpc206-selected-lineage-pair-registry-audit-v1.schema.json"
)
MANIFEST_PATH = HERE / "tpc206_certificate_manifest.json"

SOURCE_SNAPSHOT = "42507087b774d9057ba3794468a4790bf93162d5"
TPC205_COMMIT = "98b3e6c462008b07538b496ed130b1004a84747f"
CLASSIFICATION = "PAIR_NATIVE_SELECTED_LINEAGE_PROJECTION_L1"
THEOREM_STATUS = (
    "PROVED_SELECTED_SOURCE_LOCKED_13_OF_42_PROJECTION_AND_FIRST_MISSING_D_L1"
)
VERDICT = (
    "SELECTED_SOURCE_LOCKED_13_OF_42_PAIR_REGISTRY_PROJECTION_"
    "CERTIFIED_NOT_REOPENED"
)
EXPECTED_RELEASE_HASHES = {
    "payload": "b0e8ca954ed25679ae19178fd4c31c0e8c891d0de78e87ac5f74632232e9370c",
    "payload_schema": "e8b7624e293fb96a99c9d0da3d5c71e41ed5cd4cd85b1deb10288eb47fbefd19",
    "audit": "a82cea21b4bfde405f85e5c71dd7729862b08c8b539c911258915582bf191b3c",
    "audit_schema": "9ba595f09384e9b3bc6a756ee90ed2935fb39e82d4dba22198fa6ed30ac2b5a0",
}

REF_PAIRS = [
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
    ["refs/heads/tpc-27-calibrated-base-closure", SOURCE_SNAPSHOT],
    ["refs/heads/tpc-5-prime-weighted-transfer", "be8cd9dd528d4f58599772146516a2c27e6e2317"],
    ["refs/heads/tpc-6-prime-target-defect", "12fce45af98061ac95d7dcb6a8b3a9a540e33394"],
    ["refs/heads/tpc-7-almost-all-shift-defect", "0c2346b0a799d17bc062f2c2e553f182d386b448"],
    ["refs/heads/tpc-8-low-conductor-second-coefficient", "18655dd8ed978d2247e85858d33e71dcb9863b9a"],
    ["refs/heads/tpc-9-prime-residual-covariance", "ad77517ad8b06bf89f45cc682739b052c5560411"],
    ["refs/heads/twin-prime-correlations", "3317f65f60fa430dc1bab22af3e857eadc312046"],
    ["refs/remotes/origin/HEAD", SOURCE_SNAPSHOT],
    ["refs/remotes/origin/main", SOURCE_SNAPSHOT],
    ["refs/remotes/origin/rough-pair-parity", "a5b348d9084833a51e33defae44d04c7cf7dc6d8"],
    ["refs/remotes/origin/short-box-sieve-kernels", "a4c8a4a018bf26802033990e13b6f06a8d0190ce"],
    ["refs/remotes/origin/structured-sieve-low-conductor", "cc8b3fac16294cff4e26d77f903f77aa73a40400"],
    ["refs/remotes/origin/twin-prime-correlations", "3317f65f60fa430dc1bab22af3e857eadc312046"],
]
TIPS = sorted({oid for _, oid in REF_PAIRS})

TEXT_SUFFIXES = {
    ".bib", ".cfg", ".csv", ".ini", ".json", ".jsonl", ".md", ".py",
    ".rst", ".tex", ".toml", ".tsv", ".txt", ".yaml", ".yml",
}
RECORD_TOKENS = {
    "archive", "audit", "certificate", "fixture", "ledger", "manifest",
    "record", "registry", "result", "sample", "schema",
}
STRUCTURED_KEYS = [
    "pair_record", "pair_records", "pair_record_id", "row_pair",
    "row_pair_id", "joint_mask", "literal_coefficient", "pair_nonzero",
    "coefficient_nonzero", "nonzero_status", "global_normalization",
    "source_atom", "pair_to_omega", "ordered_pair", "coefficient_ast",
    "packet_schedule", "global_normalization_return", "pair_to_omega_bridge",
    "pair_to_omega_crosswalk_proved", "omega",
]
EXPECTED_STRUCTURED_COUNTS = {
    "pair_record": [0, 0], "pair_records": [0, 0],
    "pair_record_id": [0, 0], "row_pair": [0, 0],
    "row_pair_id": [0, 0], "joint_mask": [0, 0],
    "literal_coefficient": [0, 0], "pair_nonzero": [0, 0],
    "coefficient_nonzero": [0, 0], "nonzero_status": [0, 0],
    "global_normalization": [0, 0], "source_atom": [0, 0],
    "pair_to_omega": [0, 0], "ordered_pair": [4, 4],
    "coefficient_ast": [1, 1], "packet_schedule": [6, 6],
    "global_normalization_return": [2, 2],
    "pair_to_omega_bridge": [2, 2],
    "pair_to_omega_crosswalk_proved": [2, 2], "omega": [1, 1],
}
EXPECTED_ARCHIVE_COUNTS = {
    "ref_count": 34, "unique_tip_count": 28, "commit_count": 328,
    "reachable_object_count": 12203, "commit_object_count": 328,
    "tree_object_count": 3316, "blob_object_count": 8559,
    "blob_bytes": 549022045, "text_blob_count": 7479,
    "text_blob_bytes": 165158579, "record_like_blob_count": 3551,
    "record_like_blob_bytes": 146302386, "parseable_json_blob_count": 1707,
    "json_parse_failures": 17,
}
EXPECTED_ARCHIVE_DIGESTS = {
    "refs_tsv": "6ab93d0eea746d3f1395ededcc982d221894de47939841964776e3bf0b7ef823",
    "tips_lf": "2e72549ba295cbc6c0fc2efb39bee4b0c11ac1a3a0734afa64da547e43726607",
    "commits_lf": "bbfef7198e46ce6165c00832b53a9b09b94642701f4e4fa76ab5db5ea875bcee",
    "objects_tsv": "3d88cccca291330ad99393f62d9dd4d024f29affbb53ff4201c28d769528ffaf",
    "text_tsv": "51dc91013d8230ac7decce1a63dcfe25cc8e6fa2d65aa4700f74a746fd3e461f",
    "record_like_tsv": "3d11a15ab0524213ce9a99bf7246f0b8f206b3352e4db8b22c40c3fffef89eee",
    "json_tsv": "c8f46549dcaa69288d5635b9bc416603131ab174f5b824d3045d6eca5cbb8b65",
    "structured_keys": "40a5b076fe134099caf98267fff372de0306b770289750f4557f577bde5c2f90",
}

SUBTREE_DIGESTS = {
    "authorization": "bdcdf88b22e06a3b135f70092929a94318786116cfa8a4e58f687904b523436f",
    "contract_import": "5ec92bc46b4d04af691ee29d8efe674fc49e8228d5a8d15c6914661a642efc71",
    "declared_corpus": "873634fffc611ffe9fa7ef89891f229a41aa44d0a13a79784f48f86466a5a98b",
    "decision": "600403e8ca3c2384fb79b845d7fa4cf749dbbabd813489ab42cc1c3df8e407e0",
    "summary_counts": "292c6108a6981d2d35d0c80eba7a723a6c4a773a149609cb515e2743aceffcb9",
    "source_locks": "5d55802c498bd45f5e105f5620e377aec1526e20b86d661e39a7195e2fd7e9aa",
    "selected_projection": "ef8f58977268bf95ccd1776d1bf3201a1a1ff2a06bec904ae516f84f6f1de519",
    "selected_lineage_graph": "199f30f6612874391303aeeec70a5c87f0baf33efc8031bd8012725739e04483",
    "field_ledger": "31d786fed76f685a8ccd2c6feabcbfe097588720634754a4772f73cfa6792ac0",
    "selected_non_splicing_ledger": "1b24631fa010072d4806d412830333875d769cd638bad49b1ea5261d2b461b5f",
    "legal_join_rules": "a9ac0f8d2a5c461b7e817c28e060eb951994f9bfe543bba9228dc0ba5e78dbd9",
    "selected_lineage_theorem": "0807fb4d698aa414c930f0fdd96885f1ae61c62515ab7f5937e26e72e1ffad9f",
    "claim_firewall": "4e95015e3feb383ef89c328203387eed7672dad8b6f2fac48a854764b7a899f4",
    "route_state": "07ba9f7de22d48e2123d62084ed6348cfdb8dc321aa1c48c9e7242efa7125b72",
    "stop_scoped": "ced2c684a8132d12ffd0df690b0572a61e1b8e3105c05b90b3fd7de851056ebc",
    "downstream_gates": "cf92db84065e54f2262b11792069dbac3ec74140f82fc197fc62aeb1d0404d70",
    "comparison_fixture": "1de0fff2be7f867024961160a592cef8fbf4f33adc64517151a9a301c7e56d97",
}

FIELDS = [
    "X", "h0", "delta", "R", "V", "D0", "L", "K", "D", "J", "Q",
    "T", "U0", "G_X_row", "packet_id", "source_locator",
    "alpha=(ell_alpha,d_alpha)", "gamma=(ell_gamma,d_gamma)", "j",
    "N_alpha(j)", "N_gamma(j)", "joint_mask_value",
    "literal_pair_coefficient_ast", "relation_type=TTSTAR_BILINEAR_PAIR_TERM",
    "formal_support_status", "numeric_nonzero_status", "polarization", "u",
    "sigma", "v", "iota", "theta", "t", "projector_weight",
    "child_to_source_inverse", "content_child", "frequency_child",
    "resolved_xi", "source_normalization", "linear_normalization",
    "quadratic_normalization", "target_normalization",
]
MATERIALIZED = {
    "X": 512, "h0": 2, "delta": {"denominator": 4, "numerator": 1},
    "R": 4, "V": 2, "D0": 0, "L": 64, "K": 8,
    "alpha=(ell_alpha,d_alpha)": [103, 1],
    "gamma=(ell_gamma,d_gamma)": [107, 1],
    "j": 5, "N_alpha(j)": 517, "N_gamma(j)": 537,
}

BASE_MUTATIONS = {
    "wrong_schema", "wrong_paper_number", "wrong_parent_paper",
    "wrong_classification", "wrong_theorem_status", "wrong_verdict",
    "wrong_source_snapshot", "wrong_required_field_count",
    "wrong_materialized_count", "wrong_missing_count",
    "wrong_first_missing_index", "extra_top_level_key",
}
STRICT_MUTATIONS = {
    "paper_true", "parent_paper_false", "X_true", "h0_false", "D0_false",
    "field_index_true", "materialized_count_true", "missing_count_false",
    "delta_numerator_true", "delta_denominator_true", "authorization_zero",
    "mathematical_reopen_zero",
}
SEMANTIC_MUTATIONS = {
    "promote_13_to_14", "omit_blocked_field",
    "replace_first_missing_D_with_d", "reuse_tpc133_Q_as_tpc205_Q",
    "detach_delta_from_manifest_lineage",
    "replace_R_typed_alias_with_name_equality", "use_jL_as_L_without_pow2",
    "use_jK_as_K_without_pow2",
    "promote_finite_delta_to_cross_scale_schedule",
    "promote_projection_id_to_production_id",
    "collapse_pair_edge_target_ids", "swap_alpha_gamma_quotient",
    "splice_tpc32_child_fields", "splice_tpc32_T_U0", "manual_u_selection",
    "manual_polarization_selection", "promote_row_only_to_production",
    "promote_l0_to_production", "promote_shadow_to_actual",
    "promote_formal_to_actual", "promote_synthetic_to_actual",
    "support_to_nonzero", "null_joint_mask_to_one",
    "B_alias_to_full_literal", "implicit_conjugation",
    "nu_X_label_to_scalar", "copy_one_normalization_to_four_stages",
    "drop_quadratic_scalar_square", "pair_to_omega_pass",
    "remove_supplied_omega_premise", "single_child_restores_source",
    "drop_projector_support", "pay_hard_remainder",
    "pay_square_root_return", "pay_endpoint_return",
    "production_count_zero_to_one", "full_join_zero_to_one",
    "mathematical_reopen_true", "H1_E_repair_true",
    "fixed_atom_credit_positive", "positive_sigma_true",
    "strict_one_over_400_paid", "L2_promoted", "stop_scoped_removed",
    "stop_scoped_globalized", "O161_parent_closed",
    "H1_architecture_closed", "authorization_becomes_evidence",
    "source_lock_rebound_with_content", "archive_census_omission",
    "structured_key_count_rewrite", "selected_scope_globalized",
}

ACTIVE_ARTIFACTS = [
    "papers/tpc-206-selected-lineage-pair-registry-projection/experiments/build_tpc206.py",
    "papers/tpc-206-selected-lineage-pair-registry-projection/experiments/tpc206_selected_lineage_pair_registry.py",
    "papers/tpc-206-selected-lineage-pair-registry-projection/experiments/tpc206_independent_checker.py",
    "papers/tpc-206-selected-lineage-pair-registry-projection/experiments/tpc206_selected_lineage_pair_registry.json",
    "papers/tpc-206-selected-lineage-pair-registry-projection/experiments/tpc206_selected_lineage_pair_registry_audit.json",
    "papers/tpc-206-selected-lineage-pair-registry-projection/schemas/tpc206-selected-lineage-pair-registry-v1.schema.json",
    "papers/tpc-206-selected-lineage-pair-registry-projection/schemas/tpc206-selected-lineage-pair-registry-audit-v1.schema.json",
    "papers/tpc-206-selected-lineage-pair-registry-projection/README.md",
    "papers/tpc-206-selected-lineage-pair-registry-projection/main.tex",
    "papers/tpc-206-selected-lineage-pair-registry-projection/references.bib",
    "papers/tpc-206-selected-lineage-pair-registry-projection/tpc-206-selected-lineage-pair-registry-projection.pdf",
]


def require(condition: bool, code: str) -> None:
    if not condition:
        raise RuntimeError(code)


def reject_constant(token: str) -> None:
    raise ValueError(f"non-finite JSON constant: {token}")


def unique_object(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
    result: dict[str, Any] = {}
    for key, value in pairs:
        if key in result:
            raise ValueError(f"duplicate JSON key: {key}")
        result[key] = value
    return result


def canonical(value: Any) -> str:
    return json.dumps(value, ensure_ascii=False, indent=2, sort_keys=True) + "\n"


def compact(value: Any) -> bytes:
    return json.dumps(
        value, ensure_ascii=False, separators=(",", ":"), sort_keys=True
    ).encode("utf-8")


def sha(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


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


def load_json(path: Path, require_canonical: bool = False) -> Any:
    raw = path.read_bytes()
    value = json.loads(
        raw.decode("utf-8"),
        object_pairs_hook=unique_object,
        parse_constant=reject_constant,
    )
    if require_canonical:
        require(raw == canonical(value).encode("utf-8"), f"NONCANONICAL:{path}")
    return value


def exact_schema(value: Any, title: str | None = None) -> dict[str, Any]:
    if type(value) is dict:
        result: dict[str, Any] = {
            "type": "object",
            "properties": {
                key: exact_schema(value[key]) for key in sorted(value)
            },
            "required": sorted(value),
            "additionalProperties": False,
        }
    elif type(value) is list:
        result = {
            "type": "array",
            "prefixItems": [exact_schema(item) for item in value],
            "items": False,
            "minItems": len(value),
            "maxItems": len(value),
        }
    elif type(value) is bool:
        result = {"type": "boolean", "const": value}
    elif type(value) is int:
        result = {"type": "integer", "const": value}
    elif type(value) is float:
        require(math.isfinite(value), "NONFINITE_FLOAT")
        result = {"type": "number", "const": value}
    elif type(value) is str:
        result = {"type": "string", "const": value}
    elif value is None:
        result = {"type": "null", "const": None}
    else:
        raise TypeError(type(value))
    if title is not None:
        result = {
            "$schema": "https://json-schema.org/draft/2020-12/schema",
            "title": title,
            **result,
        }
    return result


def schema_accepts(schema: dict[str, Any], value: Any) -> bool:
    types = {
        "object": dict, "array": list, "null": type(None), "boolean": bool,
        "integer": int, "number": float, "string": str,
    }
    kind = schema.get("type")
    if kind not in types or type(value) is not types[kind]:
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
            len(value) == schema.get("minItems") == schema.get("maxItems")
            and len(prefix) == len(value)
        ):
            return False
        return all(
            schema_accepts(child_schema, child)
            for child_schema, child in zip(prefix, value)
        )
    return True


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
    require(result.returncode == 0, f"GIT:{args}:{result.stderr.strip()}")
    return result.stdout


def batch_metadata(oids: list[str]) -> dict[str, tuple[str, int]]:
    output = git_output(
        ["cat-file", "--batch-check=%(objectname)\t%(objecttype)\t%(objectsize)"],
        "".join(f"{oid}\n" for oid in oids),
    )
    result = {}
    for line in output.splitlines():
        oid, kind, size = line.split("\t")
        result[oid] = (kind, int(size))
    require(set(result) == set(oids), "OBJECT_METADATA_COVER")
    return result


def batch_blobs(oids: list[str]) -> dict[str, bytes]:
    proc = subprocess.run(
        ["git", "cat-file", "--batch"],
        cwd=REPO,
        input="".join(f"{oid}\n" for oid in oids).encode("ascii"),
        capture_output=True,
        check=False,
    )
    require(proc.returncode == 0, "BLOB_BATCH")
    output = proc.stdout
    cursor = 0
    result = {}
    for expected in oids:
        end = output.find(b"\n", cursor)
        require(end >= 0, f"BLOB_HEADER:{expected}")
        header = output[cursor:end].decode("ascii").split()
        require(
            len(header) == 3 and header[0] == expected and header[1] == "blob",
            f"BLOB_TYPE:{expected}",
        )
        size = int(header[2])
        cursor = end + 1
        result[expected] = output[cursor:cursor + size]
        require(len(result[expected]) == size, f"BLOB_SIZE:{expected}")
        cursor += size
        require(output[cursor:cursor + 1] == b"\n", f"BLOB_END:{expected}")
        cursor += 1
    require(cursor == len(output), "BLOB_TRAILING")
    return result


def tsv(rows: Iterable[str]) -> tuple[str, int]:
    raw = "".join(f"{row}\n" for row in rows).encode("utf-8")
    return sha(raw), len(raw)


def collect_keys(
    value: Any,
    pointer: str,
    hits: dict[str, list[list[str]]],
    oid: str,
    path: str,
) -> None:
    if type(value) is dict:
        for key, child in value.items():
            escaped = key.replace("~", "~0").replace("/", "~1")
            child_pointer = f"{pointer}/{escaped}"
            if key in hits:
                hits[key].append([oid, path, child_pointer, sha(compact(child))])
            collect_keys(child, child_pointer, hits, oid, path)
    elif type(value) is list:
        for index, child in enumerate(value):
            collect_keys(child, f"{pointer}/{index}", hits, oid, path)


def rebuild_archive() -> dict[str, Any]:
    for oid in TIPS:
        require(git_output(["cat-file", "-t", oid]).strip() == "commit", "TIP")
    require(
        git_output(["merge-base", "--is-ancestor", TPC205_COMMIT, SOURCE_SNAPSHOT])
        == "",
        "TPC205_ANCESTRY",
    )
    changed = git_output(
        [
            "diff", "--name-only", f"{TPC205_COMMIT}..{SOURCE_SNAPSHOT}",
            "--", "papers/tpc-*",
        ]
    ).strip()
    require(changed == "", "TPC_CHANGED_AFTER_205")

    object_paths: dict[str, str] = {}
    for line in git_output(["rev-list", "--objects", *TIPS]).splitlines():
        if " " in line:
            oid, path = line.split(" ", 1)
            if oid not in object_paths or path < object_paths[oid]:
                object_paths[oid] = path
        else:
            object_paths.setdefault(line, "")
    oids = sorted(object_paths)
    metadata = batch_metadata(oids)
    commits = sorted(oid for oid in oids if metadata[oid][0] == "commit")
    trees = sorted(oid for oid in oids if metadata[oid][0] == "tree")
    blobs = sorted(oid for oid in oids if metadata[oid][0] == "blob")
    object_rows = [
        f"{oid}\t{metadata[oid][0]}\t{metadata[oid][1]}" for oid in oids
    ]
    text_rows: list[str] = []
    record_rows: list[str] = []
    candidates: list[str] = []
    text_bytes = 0
    record_bytes = 0
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
            candidates.append(oid)
    raw_blobs = batch_blobs(candidates)
    json_rows: list[str] = []
    failures = 0
    hits = {key: [] for key in STRUCTURED_KEYS}
    for oid in candidates:
        path = object_paths[oid]
        size = metadata[oid][1]
        try:
            value = json.loads(
                raw_blobs[oid].decode("utf-8-sig"),
                object_pairs_hook=unique_object,
                parse_constant=reject_constant,
            )
        except (UnicodeDecodeError, json.JSONDecodeError, ValueError):
            failures += 1
            continue
        json_rows.append(f"{oid}\t{size}\t{path}")
        collect_keys(value, "", hits, oid, path)
    structured = {
        "schema": "tpc-reachable-structured-key-audit-v1",
        "parseable_json_blobs": len(json_rows),
        "keys": {key: sorted(hits[key]) for key in STRUCTURED_KEYS},
    }
    digest_rows = {
        "refs_tsv": tsv(
            f"{name}\t{oid}" for name, oid in sorted(REF_PAIRS)
        ),
        "tips_lf": tsv(sorted(TIPS)),
        "commits_lf": tsv(commits),
        "objects_tsv": tsv(object_rows),
        "text_tsv": tsv(sorted(text_rows)),
        "record_like_tsv": tsv(sorted(record_rows)),
        "json_tsv": tsv(sorted(json_rows)),
    }
    structured_raw = compact(structured) + b"\n"
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
            "head": SOURCE_SNAPSHOT,
            "origin_main": SOURCE_SNAPSHOT,
            "local_main": "a5f6c645504261d36081898a6e7b11e4992fac8d",
            "ref_pairs": sorted(REF_PAIRS),
            "unique_tips": list(TIPS),
        },
        "counts": {
            "ref_count": len(REF_PAIRS),
            "unique_tip_count": len(TIPS),
            "commit_count": len(commits),
            "reachable_object_count": len(oids),
            "commit_object_count": len(commits),
            "tree_object_count": len(trees),
            "blob_object_count": len(blobs),
            "blob_bytes": sum(metadata[oid][1] for oid in blobs),
            "text_blob_count": len(text_rows),
            "text_blob_bytes": text_bytes,
            "record_like_blob_count": len(record_rows),
            "record_like_blob_bytes": record_bytes,
            "parseable_json_blob_count": len(json_rows),
            "json_parse_failures": failures,
        },
        "inventory_bytes": {
            key: digest_rows[key][1] for key in digest_rows
        } | {"structured_keys": len(structured_raw)},
        "digests": {
            key: digest_rows[key][0] for key in digest_rows
        } | {"structured_keys": sha(structured_raw)},
        "structured_key_counts": {
            key: [len({row[0] for row in hits[key]}), len(hits[key])]
            for key in STRUCTURED_KEYS
        },
    }
    require(strict_same(result["counts"], EXPECTED_ARCHIVE_COUNTS), "ARCHIVE_COUNTS")
    require(
        strict_same(result["digests"], EXPECTED_ARCHIVE_DIGESTS),
        "ARCHIVE_DIGESTS",
    )
    require(
        strict_same(result["structured_key_counts"], EXPECTED_STRUCTURED_COUNTS),
        "STRUCTURED_COUNTS",
    )
    return result


def read_jsonl_unique(path: Path, key: str, expected: str) -> tuple[dict[str, Any], int]:
    found = []
    for number, line in enumerate(
        path.read_text(encoding="utf-8").splitlines(), start=1
    ):
        row = json.loads(
            line,
            object_pairs_hook=unique_object,
            parse_constant=reject_constant,
        )
        if type(row) is dict and row.get(key) == expected:
            found.append((row, number))
    require(len(found) == 1, f"SELECTOR:{expected}")
    return found[0]


def verify_integrity(row: dict[str, Any]) -> None:
    expected = row["integrity_sha256"]
    body = {key: value for key, value in row.items() if key != "integrity_sha256"}
    require(sha(compact(body)) == expected, f"INTEGRITY:{expected}")


def verify_lineage(payload: dict[str, Any]) -> None:
    require(
        sha(compact(payload["selected_projection"]))
        == SUBTREE_DIGESTS["selected_projection"],
        "SELECTED_PROJECTION_PIN",
    )
    row_path = (
        REPO
        / "papers/tpc-133-executable-native-entrance/samples/"
        "tpc133_native_atoms.jsonl"
    )
    path_path = (
        REPO
        / "papers/tpc-134-boundary-complete-dyadic-prefix-tail-archive/"
        "samples/tpc134_paths.jsonl"
    )
    cut_path = (
        REPO
        / "papers/tpc-136-complete-native-cut-archive/samples/"
        "tpc136_cut_paths.jsonl"
    )
    alpha = "X=512|h0=2|ell=103|k=5|d=1"
    gamma = "X=512|h0=2|ell=107|k=5|d=1"
    alpha_path = f"{alpha}|jL=6|jK=3|D0=0|type=TAIL"
    gamma_path = f"{gamma}|jL=6|jK=3|D0=0|type=TAIL"
    rows = [
        read_jsonl_unique(row_path, "native_id", alpha),
        read_jsonl_unique(row_path, "native_id", gamma),
        read_jsonl_unique(path_path, "path_id", alpha_path),
        read_jsonl_unique(path_path, "path_id", gamma_path),
        read_jsonl_unique(cut_path, "cut_path_id", f"cut|{alpha_path}"),
        read_jsonl_unique(cut_path, "cut_path_id", f"cut|{gamma_path}"),
    ]
    require([line for _, line in rows] == [724, 736, 2554, 2602, 2554, 2602],
            "LINE_NUMBERS")
    for row, _ in rows:
        verify_integrity(row)
    payload_records = {
        row["role"]: row for row in payload["selected_projection"]["selected_records"]
    }
    require(
        set(payload_records)
        == {
            "alpha_row", "gamma_row", "alpha_path", "gamma_path",
            "alpha_cut", "gamma_cut",
        },
        "PAYLOAD_RECORD_ROLES",
    )
    row_a, row_g, path_a, path_g, cut_a, cut_g = [row for row, _ in rows]
    live_rows = [
        ("alpha_row", row_a, 724, "native_id", alpha, row_path),
        ("gamma_row", row_g, 736, "native_id", gamma, row_path),
        ("alpha_path", path_a, 2554, "path_id", alpha_path, path_path),
        ("gamma_path", path_g, 2602, "path_id", gamma_path, path_path),
        ("alpha_cut", cut_a, 2554, "cut_path_id", f"cut|{alpha_path}", cut_path),
        ("gamma_cut", cut_g, 2602, "cut_path_id", f"cut|{gamma_path}", cut_path),
    ]
    for role, live, line, id_key, semantic_id, path in live_rows:
        locked = payload_records[role]
        require(locked["semantic_id"] == semantic_id, f"PAYLOAD_ID:{role}")
        require(locked["diagnostic_line"] == line, f"PAYLOAD_LINE:{role}")
        require(
            locked["path"] == str(path.relative_to(REPO)).replace("\\", "/"),
            f"PAYLOAD_PATH:{role}",
        )
        require(
            locked["integrity_sha256"] == live["integrity_sha256"],
            f"PAYLOAD_INTEGRITY:{role}",
        )
        require(live[id_key] == semantic_id, f"LIVE_ID:{role}")
    require(row_a["native_tuple"] == [103, 5, 1], "ALPHA_TUPLE")
    require(row_g["native_tuple"] == [107, 5, 1], "GAMMA_TUPLE")
    require(
        path_a["metadata"]["parent_integrity_sha256"]
        == row_a["integrity_sha256"],
        "ALPHA_PARENT",
    )
    require(
        payload_records["alpha_path"]["parent_integrity_sha256"]
        == row_a["integrity_sha256"],
        "PAYLOAD_ALPHA_PARENT",
    )
    require(
        path_g["metadata"]["parent_integrity_sha256"]
        == row_g["integrity_sha256"],
        "GAMMA_PARENT",
    )
    require(
        payload_records["gamma_path"]["parent_integrity_sha256"]
        == row_g["integrity_sha256"],
        "PAYLOAD_GAMMA_PARENT",
    )
    require(
        cut_a["metadata"]["upstream_integrity_sha256"]
        == path_a["integrity_sha256"],
        "ALPHA_UPSTREAM",
    )
    require(
        payload_records["alpha_cut"]["upstream_integrity_sha256"]
        == path_a["integrity_sha256"],
        "PAYLOAD_ALPHA_UPSTREAM",
    )
    require(
        cut_g["metadata"]["upstream_integrity_sha256"]
        == path_g["integrity_sha256"],
        "GAMMA_UPSTREAM",
    )
    require(
        payload_records["gamma_cut"]["upstream_integrity_sha256"]
        == path_g["integrity_sha256"],
        "PAYLOAD_GAMMA_UPSTREAM",
    )
    for row in (row_a, row_g):
        require(
            row["packet_scope"]["X"] == 512
            and row["packet_scope"]["h0"] == 2
            and row["packet_scope"]["Q"] == 4
            and row["packet_scope"]["V"] == 2,
            "PACKET_SCOPE",
        )
    for path, cut in ((path_a, cut_a), (path_g, cut_g)):
        require(path["block"] == {"j_K": 3, "j_L": 6}, "PATH_BLOCK")
        require(path["D0"] == 0, "PATH_D0")
        require(cut["cut_terminal_type"] == "FRONTIER_UNMAPPED", "CUT_TYPE")
        require(cut["metadata"]["frontier_reason"] == "NO_TAIL_ROOM", "CUT_REASON")
    manifest_path = (
        REPO
        / "papers/tpc-133-executable-native-entrance/samples/"
        "tpc133_packet_manifest.json"
    )
    certificate_path = (
        REPO
        / "papers/tpc-133-executable-native-entrance/experiments/"
        "tpc133_native_entrance_certificate.json"
    )
    frontier_path = (
        REPO
        / "papers/tpc-135-tpc17-tpc18-block-frontier/samples/"
        "tpc135_frontier_manifest.json"
    )
    manifest = load_json(manifest_path)
    certificate = load_json(certificate_path)
    frontier = load_json(frontier_path)
    require(
        manifest["delta"] == {"numerator": 1, "denominator": 4},
        "MANIFEST_DELTA",
    )
    require(
        sha(
            manifest_path.read_text(encoding="utf-8")
            .replace("\r\n", "\n")
            .replace("\r", "\n")
            .encode("utf-8")
        )
        == "bda1a64348bc0d97fca4239b1c2a099a58aea5fbc4908580fc740f114a57fd39",
        "MANIFEST_HASH",
    )
    require(certificate["archive"]["record_count"] == 866, "CERTIFICATE_COUNT")
    require(
        certificate["archive"]["jsonl_sha256"] == sha(row_path.read_bytes()),
        "CERTIFICATE_ARCHIVE_HASH",
    )
    require(
        {
            key: certificate["packet"][key]
            for key in ["X", "h0", "delta", "Q", "V"]
        }
        == {"X": 512, "h0": 2, "delta": "1/4", "Q": 4, "V": 2},
        "CERTIFICATE_PACKET",
    )
    require(
        {
            key: frontier["scope"][key] for key in ["X", "h0", "R", "V"]
        }
        == {"X": 512, "h0": 2, "R": 4, "V": 2},
        "FRONTIER_SCOPE",
    )
    for path, cut in ((path_a, cut_a), (path_g, cut_g)):
        require(path["metadata"]["Q"] == frontier["scope"]["R"], "Q_R_BRIDGE")
        require(cut["metadata"]["Q"] == frontier["scope"]["R"], "CUT_Q_R_BRIDGE")
    require(4 ** 4 <= 512 < 5 ** 4, "R_ARITHMETIC")
    require(2 ** 6 == 64 and 2 ** 3 == 8, "DYADIC_ARITHMETIC")
    require(103 * 5 + 2 == 517 and 107 * 5 + 2 == 537, "TARGET_ARITHMETIC")


def verify_sources(payload: dict[str, Any]) -> None:
    locks = payload["source_locks"]
    require(len(locks) == 29, "SOURCE_COUNT")
    require(sha(compact(locks)) == SUBTREE_DIGESTS["source_locks"], "SOURCE_PIN")
    require(len({row["id"] for row in locks}) == 29, "SOURCE_IDS")
    require(len({row["path"] for row in locks}) == 29, "SOURCE_PATHS")
    repo_root = REPO.resolve()
    for lock in locks:
        path = (REPO / lock["path"]).resolve()
        require(path.is_relative_to(repo_root), f"SOURCE_ESCAPE:{lock['id']}")
        require(path.is_file(), f"SOURCE_MISSING:{lock['id']}")
        text = path.read_text(encoding="utf-8").replace("\r\n", "\n").replace(
            "\r", "\n"
        )
        digest = sha(text.encode("utf-8"))
        require(
            digest == lock["canonical_sha256"],
            f"SOURCE_HASH:{lock['id']}",
        )
        require(
            lock["frozen_expected_sha256"] == digest,
            f"SOURCE_FROZEN_HASH:{lock['id']}",
        )
        require(
            lock["snapshot_commit"] == SOURCE_SNAPSHOT,
            f"SOURCE_SNAPSHOT_ID:{lock['id']}",
        )
        snapshot = subprocess.run(
            ["git", "show", f"{SOURCE_SNAPSHOT}:{lock['path']}"],
            cwd=REPO,
            capture_output=True,
            check=False,
        )
        require(snapshot.returncode == 0, f"SOURCE_SNAPSHOT_MISSING:{lock['id']}")
        snapshot_text = snapshot.stdout.decode("utf-8").replace(
            "\r\n", "\n"
        ).replace("\r", "\n")
        require(
            sha(snapshot_text.encode("utf-8")) == digest,
            f"SOURCE_SNAPSHOT_HASH:{lock['id']}",
        )
        for anchor in lock["required_anchors"]:
            require(anchor in text, f"SOURCE_ANCHOR:{lock['id']}:{anchor}")


def verify_field_theorem(payload: dict[str, Any]) -> None:
    for key in SUBTREE_DIGESTS:
        require(
            sha(compact(payload[key])) == SUBTREE_DIGESTS[key],
            f"SUBTREE_PIN:{key}",
        )
    graph = payload["selected_lineage_graph"]
    require(
        graph["scope"] == "EXPLICIT_SIX_RECORD_PLUS_FOUR_TYPED_DERIVATION_NODES",
        "GRAPH_SCOPE",
    )
    require(
        graph["corpus_wide_candidate_graph_enumerated"] is False
        and graph["corpus_wide_maximality_inferred"] is False,
        "GRAPH_GLOBAL_FIREWALL",
    )
    require(len(graph["nodes"]) == 10 and len(graph["dependency_edges"]) == 12,
            "GRAPH_SIZE")
    expected_node_ids = {
        "record:alpha_row", "record:gamma_row", "record:alpha_path",
        "record:gamma_path", "record:alpha_cut", "record:gamma_cut",
        "derive:chosen_manifest_delta", "derive:truncation_R",
        "derive:dyadic_L_K", "derive:native_j_targets",
    }
    require(
        {node["node_id"] for node in graph["nodes"]} == expected_node_ids,
        "GRAPH_NODE_IDS",
    )
    closure: dict[str, dict[str, Any]] = {}
    for node in graph["nodes"]:
        require(
            node["kind"] in {"SOURCE_RECORD", "LOCKED_TYPED_DERIVATION"},
            f"GRAPH_NODE_KIND:{node['node_id']}",
        )
        for field_id, value in node["provides"].items():
            if field_id in closure:
                require(
                    strict_same(closure[field_id]["value"], value),
                    f"GRAPH_VALUE_CONFLICT:{field_id}",
                )
                closure[field_id]["providers"].append(node["node_id"])
            else:
                closure[field_id] = {
                    "field_id": field_id,
                    "value": value,
                    "providers": [node["node_id"]],
                }
    expected_closure = [
        closure[field_id] for field_id in FIELDS if field_id in closure
    ]
    require(
        strict_same(graph["field_closure"], expected_closure),
        "GRAPH_CLOSURE_REBUILD",
    )
    require(
        graph["field_closure_count"] == len(expected_closure) == 13,
        "GRAPH_CLOSURE_COUNT",
    )
    require(
        strict_same(
            {row["field_id"]: row["value"] for row in expected_closure},
            MATERIALIZED,
        ),
        "GRAPH_MATERIALIZED_VALUES",
    )

    ledger = payload["field_ledger"]
    require(len(ledger) == 42, "FIELD_COUNT")
    require([row["field_id"] for row in ledger] == FIELDS, "FIELD_ORDER")
    require(
        [row["one_based_index"] for row in ledger] == list(range(1, 43)),
        "FIELD_ORDINALS",
    )
    passed = [row for row in ledger if row["counts_as_legal_partial_projection"]]
    missing = [row for row in ledger if not row["counts_as_legal_partial_projection"]]
    require(len(passed) == 13 and len(missing) == 29, "FIELD_PARTITION")
    require(missing[0]["field_id"] == "D" and missing[0]["one_based_index"] == 9,
            "FIRST_MISSING_D")
    for row in ledger:
        field = row["field_id"]
        if field in MATERIALIZED:
            require(strict_same(row["value"], MATERIALIZED[field]), f"VALUE:{field}")
            require(row["blocker"] is None, f"PASS_BLOCKER:{field}")
            require(
                row["provider_node_ids"] == closure[field]["providers"],
                f"PROVIDERS:{field}",
            )
        else:
            require(row["value"] is None, f"MISSING_VALUE:{field}")
            require(type(row["blocker"]) is str and row["blocker"], f"BLOCKER:{field}")
            require(row["provider_node_ids"] == [], f"MISSING_PROVIDERS:{field}")
        require(row["counts_as_production_record"] is False, f"PRODUCTION:{field}")
    no_splice = payload["selected_non_splicing_ledger"]
    require(
        [row["field_id"] for row in no_splice]
        == [row["field_id"] for row in missing],
        "NO_SPLICE_COVER",
    )
    require(
        all(
            row["external_donor_policy"] == "DISALLOWED_CROSS_LINEAGE_SPLICE"
            and row["absence_claim_scope"] == "EXPLICIT_SELECTED_GRAPH_ONLY"
            and row["global_absence_claim"] is False
            and row["selected_graph_provider_count"] == 0
            for row in no_splice
        ),
        "NO_SPLICE_RULE",
    )
    theorem = payload["selected_lineage_theorem"]
    require(
        theorem["required_fields"] == 42
        and theorem["selected_graph_materialized_fields"] == len(passed)
        and theorem["missing_fields"] == len(missing)
        and theorem["full_completions_inside_explicit_selected_graph"] == 0
        and theorem["production_occurrences_inside_explicit_selected_graph"] == 0
        and theorem["theorem_scope"] == "EXPLICIT_SELECTED_LINEAGE_GRAPH_ONLY"
        and theorem["corpus_wide_maximum_materialized_fields"] is None
        and theorem["corpus_wide_full_join_count"] is None
        and theorem["corpus_wide_maximality_status"] == "NOT_TESTABLE",
        "SELECTED_LINEAGE_THEOREM",
    )
    fixture = payload["comparison_fixture"]
    require(
        fixture["partial_field_count_in_its_own_fixture"] == 14
        and fixture["legal_join_with_selected_projection"] is False
        and fixture["corpus_wide_maximality_consequence"] == "NOT_EVALUATED",
        "COMPARISON_FIXTURE_FIREWALL",
    )
    gate_map = {row["id"]: row["status"] for row in payload["downstream_gates"]}
    require(gate_map["CORPUS_WIDE_MAXIMALITY"] == "NOT_TESTABLE", "GLOBAL_GATE")
    require(payload["claim_firewall"]["fixed_atom_credit"] == 0, "CREDIT")
    require(payload["claim_firewall"]["L2_result"] == "NONE", "L2")
    require(payload["claim_firewall"]["mathematical_reopen"] is False, "REOPEN")


def set_path(value: Any, path: list[Any], replacement: Any) -> Any:
    result = json.loads(canonical(value))
    cursor = result
    for key in path[:-1]:
        cursor = cursor[key]
    cursor[path[-1]] = replacement
    return result


def verify_mutations(
    payload: dict[str, Any],
    schema: dict[str, Any],
    audit: dict[str, Any],
) -> int:
    contract = audit["mutation_contract"]
    groups = [
        ("base_exact_schema_mutations", BASE_MUTATIONS),
        ("coordinated_semantic_mutations", SEMANTIC_MUTATIONS),
        ("strict_bool_int_mutations", STRICT_MUTATIONS),
    ]
    total = 0
    for key, expected_names in groups:
        rows = contract[key]
        require({row["name"] for row in rows} == expected_names, f"MUTATION_NAMES:{key}")
        require(len(rows) == len(expected_names), f"MUTATION_DUPLICATE:{key}")
        for row in rows:
            require(row["payload_changed"] is True, f"MUTATION_CHANGED:{row['name']}")
            require(
                row["active_exact_schema_rejected"] is True,
                f"MUTATION_SCHEMA:{row['name']}",
            )
            require(
                row["regenerated_exact_schema_accepts"] is True,
                f"MUTATION_REGEN:{row['name']}",
            )
            require(
                row["expected_payload_reconstruction_rejected"] is True,
                f"MUTATION_REBUILD:{row['name']}",
            )
        total += len(rows)
    require(contract["active_schema_rejections"] == total, "MUTATION_TOTAL")
    require(
        contract["regenerated_exact_schema_acceptances"]
        == total,
        "REGENERATED_SCHEMA_TOTAL",
    )
    require(
        contract["expected_reconstruction_semantic_rejections"]
        == len(SEMANTIC_MUTATIONS),
        "SEMANTIC_TOTAL",
    )
    require(contract["all_rejected"] is True, "MUTATION_ALL")

    probes = [
        {**payload, "unexpected": 1},
        set_path(payload, ["paper"], True),
        set_path(payload, ["summary_counts", "materialized_fields"], 14),
        set_path(payload, ["selected_lineage_theorem", "first_missing_field_id"], "d"),
        set_path(payload, ["field_ledger", 10, "value"], 4),
        set_path(payload, ["claim_firewall", "mathematical_reopen"], True),
        set_path(payload, ["source_locks", 0, "canonical_sha256"], "0" * 64),
        set_path(payload, ["archive_census", "counts", "reachable_object_count"], 1),
        set_path(
            payload,
            ["selected_lineage_graph", "corpus_wide_maximality_inferred"],
            True,
        ),
    ]
    require(all(not schema_accepts(schema, probe) for probe in probes), "PROBE_SCHEMA")
    require(
        all(schema_accepts(exact_schema(probe, "probe"), probe) for probe in probes),
        "PROBE_REGENERATED_SCHEMA",
    )
    require(all(not strict_same(probe, payload) for probe in probes), "PROBE_REBUILD")
    return total


def verify_manifest() -> dict[str, Any]:
    require(MANIFEST_PATH.is_file(), "MANIFEST_REQUIRED")
    manifest = load_json(MANIFEST_PATH, require_canonical=True)
    require(
        set(manifest) == {"schema", "paper", "trust_mode", "artifacts", "summary"},
        "MANIFEST_TOP_KEYS",
    )
    require(manifest["schema"] == "tpc-206-certificate-manifest-v1", "MANIFEST_SCHEMA")
    require(type(manifest["paper"]) is int and manifest["paper"] == 206,
            "MANIFEST_PAPER")
    require(
        manifest["trust_mode"]
        == "REPOSITORY_PIN_REQUIRES_GIT_REVIEW_NOT_EXTERNAL_SIGNATURE",
        "MANIFEST_TRUST",
    )
    require(type(manifest["artifacts"]) is list, "MANIFEST_ARTIFACTS_TYPE")
    require(
        [row["path"] for row in manifest["artifacts"]] == ACTIVE_ARTIFACTS,
        "MANIFEST_PATHS",
    )
    for row in manifest["artifacts"]:
        require(set(row) == {"path", "raw_sha256", "bytes"}, "MANIFEST_ROW_KEYS")
        require(type(row["path"]) is str, "MANIFEST_PATH_TYPE")
        require(
            type(row["raw_sha256"]) is str
            and len(row["raw_sha256"]) == 64
            and all(ch in "0123456789abcdef" for ch in row["raw_sha256"]),
            "MANIFEST_HASH_TYPE",
        )
        require(type(row["bytes"]) is int and row["bytes"] >= 0,
                "MANIFEST_BYTES_TYPE")
        path = REPO / row["path"]
        require(path.is_file(), f"MANIFEST_MISSING:{row['path']}")
        require(path.stat().st_size == row["bytes"], f"MANIFEST_SIZE:{row['path']}")
        require(sha(path.read_bytes()) == row["raw_sha256"], f"MANIFEST_HASH:{row['path']}")
    require(
        strict_same(
            manifest["summary"],
            {
                "artifacts_pinned": 11,
                "required_fields": 42,
                "materialized_fields": 13,
                "missing_fields": 29,
                "selected_lineage_full_completions": 0,
                "corpus_wide_maximality": "NOT_TESTABLE",
                "verdict": VERDICT,
            },
        ),
        "MANIFEST_SUMMARY",
    )
    return {
        "artifacts_pinned": 11,
        "trust_mode": manifest["trust_mode"],
    }


def main() -> None:
    if not __debug__:
        raise RuntimeError("TPC-206 independent checker fails closed under -O")
    parser = argparse.ArgumentParser()
    parser.add_argument("--check", action="store_true")
    parser.parse_args()
    require(
        sha(PAYLOAD_PATH.read_bytes()) == EXPECTED_RELEASE_HASHES["payload"],
        "PAYLOAD_RELEASE_PIN",
    )
    require(
        sha(PAYLOAD_SCHEMA_PATH.read_bytes())
        == EXPECTED_RELEASE_HASHES["payload_schema"],
        "PAYLOAD_SCHEMA_RELEASE_PIN",
    )
    require(
        sha(AUDIT_PATH.read_bytes()) == EXPECTED_RELEASE_HASHES["audit"],
        "AUDIT_RELEASE_PIN",
    )
    require(
        sha(AUDIT_SCHEMA_PATH.read_bytes())
        == EXPECTED_RELEASE_HASHES["audit_schema"],
        "AUDIT_SCHEMA_RELEASE_PIN",
    )
    payload = load_json(PAYLOAD_PATH, require_canonical=True)
    schema = load_json(PAYLOAD_SCHEMA_PATH, require_canonical=True)
    audit = load_json(AUDIT_PATH, require_canonical=True)
    audit_schema = load_json(AUDIT_SCHEMA_PATH, require_canonical=True)
    require(
        payload["schema"] == "tpc-206-selected-lineage-pair-registry-v1",
        "PAYLOAD_SCHEMA_ID",
    )
    require(
        type(payload["paper"]) is int
        and payload["paper"] == 206
        and type(payload["parent_paper"]) is int
        and payload["parent_paper"] == 205,
        "PAPER",
    )
    require(payload["classification"] == CLASSIFICATION, "CLASSIFICATION")
    require(payload["theorem_status"] == THEOREM_STATUS, "THEOREM_STATUS")
    require(payload["verdict"] == VERDICT, "VERDICT")
    require(payload["source_snapshot_commit"] == SOURCE_SNAPSHOT, "SNAPSHOT")
    require(strict_same(schema, exact_schema(payload, schema["title"])), "PAYLOAD_SCHEMA")
    require(schema_accepts(schema, payload), "PAYLOAD_SCHEMA_ACCEPTANCE")
    require(strict_same(audit_schema, exact_schema(audit, audit_schema["title"])),
            "AUDIT_SCHEMA")
    require(schema_accepts(audit_schema, audit), "AUDIT_SCHEMA_ACCEPTANCE")
    require(
        audit["payload_sha256"] == sha(canonical(payload).encode("utf-8")),
        "AUDIT_PAYLOAD_HASH",
    )
    require(
        audit["payload_schema_sha256"] == sha(canonical(schema).encode("utf-8")),
        "AUDIT_SCHEMA_HASH",
    )
    rebuilt_archive = rebuild_archive()
    require(strict_same(payload["archive_census"], rebuilt_archive), "ARCHIVE_REBUILD")
    verify_sources(payload)
    verify_lineage(payload)
    verify_field_theorem(payload)
    mutation_total = verify_mutations(payload, schema, audit)
    manifest = verify_manifest()
    print(
        json.dumps(
            {
                "paper": 206,
                "independent_check": True,
                "archive_objects_verified": 12203,
                "source_locks_verified": 29,
                "lineage_records_verified": 6,
                "fields_verified": 42,
                "materialized_fields": 13,
                "missing_fields": 29,
                "selected_graph_nodes_verified": 10,
                "selected_graph_edges_verified": 12,
                "selected_lineage_full_completions": 0,
                "corpus_wide_maximality": "NOT_TESTABLE",
                "mutation_rows_verified": mutation_total,
                "mathematical_reopen": False,
                "manifest": manifest,
                "verdict": VERDICT,
            },
            sort_keys=True,
        )
    )


if __name__ == "__main__":
    main()
