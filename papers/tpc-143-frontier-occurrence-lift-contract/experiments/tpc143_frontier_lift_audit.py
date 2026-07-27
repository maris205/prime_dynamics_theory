#!/usr/bin/env python3
"""Build and verify the TPC-143 frontier occurrence-lift obligations.

The program uses only the Python standard library.  Default mode writes
deterministic artifacts; ``--check`` compares them byte for byte and
does not write.  The current archive is never completed with fabricated
downstream labels.
"""

from __future__ import annotations

import argparse
import copy
import hashlib
import importlib.util
import json
import tempfile
from pathlib import Path
from typing import Any, Iterable


HERE = Path(__file__).resolve().parent
PAPER = HERE.parent
PAPERS = PAPER.parent
TPC133 = PAPERS / "tpc-133-executable-native-entrance"
TPC134 = PAPERS / "tpc-134-boundary-complete-dyadic-prefix-tail-archive"
TPC135 = PAPERS / "tpc-135-tpc17-tpc18-block-frontier"
TPC136 = PAPERS / "tpc-136-complete-native-cut-archive"
ATOM_FILE = TPC133 / "samples" / "tpc133_native_atoms.jsonl"
TPC133_MANIFEST = TPC133 / "samples" / "tpc133_packet_manifest.json"
TPC133_CERT = TPC133 / "experiments" / "tpc133_native_entrance_certificate.json"
TPC134_PATHS = TPC134 / "samples" / "tpc134_paths.jsonl"
TPC134_CERT = TPC134 / "experiments" / "tpc134_branch_archive_certificate.json"
TPC135_MANIFEST = TPC135 / "samples" / "tpc135_frontier_manifest.json"
TPC135_CERT = TPC135 / "experiments" / "tpc135_domain_cover_certificate.json"
CUT_FILE = TPC136 / "samples" / "tpc136_cut_paths.jsonl"
TPC136_MAPS = TPC136 / "samples" / "tpc136_downstream_maps.json"
TPC136_CERT = TPC136 / "experiments" / "tpc136_cut_archive_certificate.json"
OUT_JSONL = PAPER / "samples" / "tpc143_frontier_lift_obligations.jsonl"
OUT_CERT = HERE / "tpc143_frontier_lift_certificate.json"

NONSOFT = {"ELIGIBLE_TAIL_OPEN", "FRONTIER_UNMAPPED"}
MISSING = "REQUIRED_MISSING"


def canonical_bytes(value: Any) -> bytes:
    return (
        json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False)
        .encode("utf-8")
    )


def digest(value: Any) -> str:
    return hashlib.sha256(canonical_bytes(value)).hexdigest()


def digest_text(value: str) -> str:
    return hashlib.sha256(value.encode("utf-8")).hexdigest()


def load_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def load_upstream_module(name: str, script: Path) -> Any:
    spec = importlib.util.spec_from_file_location(name, script)
    if spec is None or spec.loader is None:
        raise ValueError(f"cannot load upstream generator: {script}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def set_nested(value: dict[str, Any], path: tuple[str, ...], replacement: Any) -> None:
    cursor = value
    for key in path[:-1]:
        cursor = cursor[key]
    cursor[path[-1]] = replacement


def compare_except_raw_hashes(
    stored: dict[str, Any],
    generated: dict[str, Any],
    ignored_paths: tuple[tuple[str, ...], ...],
    label: str,
) -> None:
    normalized = copy.deepcopy(stored)
    for path in ignored_paths:
        cursor = generated
        for key in path:
            cursor = cursor[key]
        set_nested(normalized, path, cursor)
    if normalized != generated:
        raise ValueError(f"semantic generator mismatch: {label}")


def classify_legacy_raw_hash(
    recorded: str, path: Path, label: str
) -> dict[str, str]:
    text_value = path.read_text(encoding="utf-8")
    canonical = hashlib.sha256(text_value.encode("utf-8")).hexdigest()
    crlf = hashlib.sha256(text_value.replace("\n", "\r\n").encode("utf-8")).hexdigest()
    if recorded == canonical:
        status = "CANONICAL_UTF8_LF_MATCH"
    elif recorded == crlf:
        status = "LEGACY_RAW_HASH_STALE"
    else:
        raise ValueError(f"non-EOL source hash mismatch: {label}")
    return {
        "status": status,
        "recorded_sha256": recorded,
        "canonical_utf8_lf_sha256": canonical,
    }


def validate_source_chain() -> dict[str, Any]:
    """Regenerate the TPC-133--136 chain and canonicalize legacy EOL locks."""
    c133 = load_json(TPC133_CERT)
    c134 = load_json(TPC134_CERT)
    c135 = load_json(TPC135_CERT)
    c136 = load_json(TPC136_CERT)
    for name, certificate in (
        ("TPC-133", c133),
        ("TPC-134", c134),
        ("TPC-135", c135),
        ("TPC-136", c136),
    ):
        if certificate.get("status") != "PASS":
            raise ValueError(f"{name} certificate is not PASS")

    m133 = load_upstream_module(
        "tpc143_source_tpc133",
        TPC133 / "experiments" / "tpc133_native_entrance.py",
    )
    m134 = load_upstream_module(
        "tpc143_source_tpc134",
        TPC134 / "experiments" / "tpc134_branch_archive.py",
    )
    m135 = load_upstream_module(
        "tpc143_source_tpc135",
        TPC135 / "experiments" / "tpc135_domain_cover_audit.py",
    )
    m136 = load_upstream_module(
        "tpc143_source_tpc136",
        TPC136 / "experiments" / "tpc136_cut_archive.py",
    )

    atoms_text, c133_text, generated_c133 = m133.build_artifacts(TPC133_MANIFEST)
    if ATOM_FILE.read_text(encoding="utf-8") != atoms_text or c133 != generated_c133:
        raise ValueError("semantic generator mismatch: TPC-133")

    paths_text, c134_text, generated_c134 = m134.build_artifacts(ATOM_FILE)
    if TPC134_PATHS.read_text(encoding="utf-8") != paths_text:
        raise ValueError("semantic generator mismatch: TPC-134 paths")
    compare_except_raw_hashes(
        c134,
        generated_c134,
        (("upstream", "tpc133_atoms_sha256"),),
        "TPC-134 certificate",
    )

    manifest_text, c135_text, generated_c135 = m135.build_artifacts(TPC134_PATHS)
    if TPC135_MANIFEST.read_text(encoding="utf-8") != manifest_text:
        raise ValueError("semantic generator mismatch: TPC-135 manifest")
    compare_except_raw_hashes(
        c135,
        generated_c135,
        (("upstream", "tpc134_paths_sha256"),),
        "TPC-135 certificate",
    )

    with tempfile.TemporaryDirectory(prefix="tpc143-source-chain-") as tmp_name:
        tmp = Path(tmp_name)
        tmp_paths = tmp / "tpc134_paths.jsonl"
        tmp_manifest = tmp / "tpc135_frontier_manifest.json"
        tmp_certificate = tmp / "tpc135_domain_cover_certificate.json"
        tmp_paths.write_bytes(paths_text.encode("utf-8"))
        tmp_manifest.write_bytes(manifest_text.encode("utf-8"))
        tmp_certificate.write_bytes(c135_text.encode("utf-8"))
        cut_text, maps_text, c136_text, generated_c136 = m136.build_artifacts(
            tmp_paths, tmp_manifest, tmp_certificate
        )
    if CUT_FILE.read_text(encoding="utf-8") != cut_text:
        raise ValueError("semantic generator mismatch: TPC-136 cut paths")
    if TPC136_MAPS.read_text(encoding="utf-8") != maps_text:
        raise ValueError("semantic generator mismatch: TPC-136 downstream maps")
    compare_except_raw_hashes(
        c136,
        generated_c136,
        (
            ("upstream", "tpc134_paths_sha256"),
            ("upstream", "tpc135_frontier_manifest_sha256"),
            ("upstream", "tpc135_certificate_sha256"),
        ),
        "TPC-136 certificate",
    )

    legacy_bindings = {
        "tpc134_to_tpc133_atoms": classify_legacy_raw_hash(
            c134["upstream"]["tpc133_atoms_sha256"],
            ATOM_FILE,
            "TPC-134/TPC-133 atoms",
        ),
        "tpc135_to_tpc134_paths": classify_legacy_raw_hash(
            c135["upstream"]["tpc134_paths_sha256"],
            TPC134_PATHS,
            "TPC-135/TPC-134 paths",
        ),
        "tpc136_to_tpc134_paths": classify_legacy_raw_hash(
            c136["upstream"]["tpc134_paths_sha256"],
            TPC134_PATHS,
            "TPC-136/TPC-134 paths",
        ),
        "tpc136_to_tpc135_manifest": classify_legacy_raw_hash(
            c136["upstream"]["tpc135_frontier_manifest_sha256"],
            TPC135_MANIFEST,
            "TPC-136/TPC-135 manifest",
        ),
        "tpc136_to_tpc135_certificate": classify_legacy_raw_hash(
            c136["upstream"]["tpc135_certificate_sha256"],
            TPC135_CERT,
            "TPC-136/TPC-135 certificate",
        ),
    }
    legacy_status = (
        "LEGACY_RAW_HASH_STALE"
        if any(
            item["status"] == "LEGACY_RAW_HASH_STALE"
            for item in legacy_bindings.values()
        )
        else "CANONICAL_UTF8_LF_MATCH"
    )
    return {
        "lock_mode": "CANONICAL_UTF8_LF_V2",
        "semantic_generation_chain": "PASS",
        "legacy_raw_hash_status": legacy_status,
        "legacy_raw_hash_bindings": legacy_bindings,
        "canonical_locks": {
            "tpc133_atoms_sha256": digest_text(atoms_text),
            "tpc133_certificate_sha256": digest_text(c133_text),
            "tpc134_paths_sha256": digest_text(paths_text),
            "tpc134_certificate_sha256": digest_text(c134_text),
            "tpc135_manifest_sha256": digest_text(manifest_text),
            "tpc135_certificate_sha256": digest_text(c135_text),
            "tpc136_cut_paths_sha256": digest_text(cut_text),
            "tpc136_downstream_maps_sha256": digest_text(maps_text),
            "tpc136_certificate_sha256": digest_text(c136_text),
        },
    }


def load_jsonl(path: Path) -> list[dict[str, Any]]:
    records = []
    for line_number, line in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
        if line.strip():
            try:
                records.append(json.loads(line))
            except json.JSONDecodeError as exc:
                raise ValueError(f"{path}:{line_number}: {exc}") from exc
    return records


def scope_key_from_atom(atom: dict[str, Any]) -> tuple[Any, ...]:
    scope = atom["packet_scope"]
    return (
        scope["X"],
        scope["h0"],
        scope["Q"],
        scope["U"],
        scope["V"],
        scope["weight_source_id"],
        scope["physical_normalization"],
        tuple(atom["native_tuple"]),
    )


def scope_key_from_cut(record: dict[str, Any]) -> tuple[Any, ...]:
    meta = record["metadata"]
    return (
        meta["X"],
        meta["h0"],
        meta["Q"],
        meta["U"],
        meta["V"],
        meta["weight_source_id"],
        meta["physical_normalization"],
        tuple(meta["native_tuple"]),
    )


def downstream_groups() -> dict[str, Any]:
    return {
        "canonical_parent_and_QD": {
            "status": MISSING,
            "required_fields": [
                "canonical_parent_key_alpha_gamma_j",
                "row_ids_and_integer_slopes",
                "ordered_targets_x_y",
                "content_gcd",
                "signed_determinant_numerator",
                "exact_determinant_label",
                "inverse_aggregation_relation",
                "physical_and_computational_multiplicity",
                "literal_parent_coefficient",
                "determinant_bin_map_edge"
            ]
        },
        "outer_zero_mode_and_QZ": {
            "status": MISSING,
            "required_fields": [
                "outer_affine_key",
                "ordered_coordinate_and_rank",
                "arithmetic_sign",
                "outer_weight",
                "factor_allocation_id",
                "content_remainder_destination",
                "zero_mode_map_edge"
            ]
        },
        "physical_grouping_G": {
            "status": MISSING,
            "required_fields": [
                "physical_occurrence_id",
                "physical_group_id",
                "exact_reconstruction_multiplier",
                "multiplicity_and_inverse_aggregation",
                "physical_cover_class",
                "reconnection_destination",
                "physical_map_edge"
            ]
        },
        "downstream_shift_selector": {
            "status": MISSING,
            "required_fields": [
                "stage_id",
                "source_shift_tag",
                "target_shift_tag",
                "source_and_target_selector_domains",
                "stage_matrix_edge",
                "shift_preservation_source"
            ]
        },
        "affine_corridor_consumer": {
            "status": MISSING,
            "required_fields": [
                "affine_D_intercept_d_and_slope_s",
                "affine_V_intercept_u_and_slope_a",
                "determinant_su_minus_ad",
                "coefficient_height",
                "residue_modulus_and_class",
                "ordered_interval_with_endpoint_convention",
                "periodic_weight_period_and_source",
                "coprimality_squarefree_content_prefix_masks",
                "coefficient_l1_mass",
                "prefix_or_window_id",
                "endpoint_ledger_token"
            ]
        }
    }


def build_obligation(
    cut: dict[str, Any], atom: dict[str, Any]
) -> dict[str, Any]:
    meta = cut["metadata"]
    identity = {
        "packet_scope": {
            "X": meta["X"],
            "h0": meta["h0"],
            "Q": meta["Q"],
            "U": meta["U"],
            "V": meta["V"],
            "weight_source_id": meta["weight_source_id"],
            "physical_normalization": meta["physical_normalization"]
        },
        "native_tuple": list(meta["native_tuple"]),
        "upstream_path_id": cut["upstream_path_id"]
    }
    result = {
        "schema": "tpc143-frontier-lift-obligation-v1",
        "cut_path_id": cut["cut_path_id"],
        "required_domain": "ALL_NONSOFT_CUT_PATHS",
        "cut_terminal_type": cut["cut_terminal_type"],
        "exact_identity": identity,
        "cut_fields": {
            "status": "PRESENT_PROVED_L1",
            "native_coefficient_ast": atom["coefficient_ast"],
            "native_constraint_witnesses": atom["constraint_witnesses"],
            "dyadic_edge_multiplier_ast": cut["edge_multiplier_ast"],
            "block": meta["block"],
            "D0": meta["D0"],
            "boundary_rule": meta["boundary_rule"],
            "frontier_reason": meta.get("frontier_reason"),
            "support_role": "FORMAL_SUPPORT_ENVELOPE",
            "numeric_coefficient_nonzero_status": "UNDECIDED"
        },
        "cut_shift_selector": {
            "map_id": "P_h0_cut",
            "h0": meta["h0"],
            "action_on_this_row": "IDENTITY",
            "status": "PROVED_L1",
            "not_downstream_selector": True
        },
        "occurrence_lift": {
            "map_id": "frontier_occurrence_lift_LX",
            "matrix_type": "ROW_SEPARATED_SPARSE_ONE_TO_MANY",
            "required_conservation": "ONE_TRANSPOSE_LX_EQUALS_ONE_TRANSPOSE",
            "required_metadata": [
                "native_tuple",
                "h0",
                "physical_normalization"
            ],
            "status": "NOT_TESTABLE",
            "actual_map_edges": []
        },
        "downstream_field_groups": downstream_groups(),
        "claim_boundary": {
            "formal_path_retained_without_nonzero_claim": True,
            "hashes_integrity_only": True,
            "new_positive_fixed_h0_L2": False,
            "prime_pair_or_twin_prime_theorem": False
        }
    }
    result["integrity_sha256"] = digest(result)
    return result


def validate_obligations(
    obligations: list[dict[str, Any]],
    nonsoft_paths: list[dict[str, Any]],
    atom_index: dict[tuple[Any, ...], dict[str, Any]],
) -> None:
    if len(obligations) != len(nonsoft_paths):
        raise ValueError("one obligation per nonsoft cut path is required")
    ids = [row["cut_path_id"] for row in obligations]
    expected_ids = [row["cut_path_id"] for row in nonsoft_paths]
    if len(ids) != len(set(ids)) or set(ids) != set(expected_ids):
        raise ValueError("obligation path identity is incomplete or duplicated")
    cut_index = {row["cut_path_id"]: row for row in nonsoft_paths}
    for row in obligations:
        saved = row["integrity_sha256"]
        clone = dict(row)
        del clone["integrity_sha256"]
        if digest(clone) != saved:
            raise ValueError(f"integrity mismatch: {row['cut_path_id']}")
        if row["required_domain"] != "ALL_NONSOFT_CUT_PATHS":
            raise ValueError("frontier-only domain promotion rejected")
        if row["cut_terminal_type"] not in NONSOFT:
            raise ValueError("soft path entered nonsoft lift obligations")
        if row["cut_shift_selector"]["map_id"] != "P_h0_cut":
            raise ValueError("cut and downstream selectors were conflated")
        if not row["cut_shift_selector"]["not_downstream_selector"]:
            raise ValueError("cut selector was promoted downstream")
        if row["occurrence_lift"]["status"] != "NOT_TESTABLE":
            raise ValueError("missing occurrence lift was fabricated")
        if row["occurrence_lift"]["actual_map_edges"]:
            raise ValueError("current audit must not fabricate occurrence edges")
        if row["cut_fields"]["numeric_coefficient_nonzero_status"] != "UNDECIDED":
            raise ValueError("formal support was promoted to nonzero arithmetic support")
        cut = cut_index[row["cut_path_id"]]
        atom_key = scope_key_from_cut(cut)
        if atom_key not in atom_index:
            raise ValueError(f"missing exact TPC-133 join for {row['cut_path_id']}")
        if row != build_obligation(cut, atom_index[atom_key]):
            raise ValueError(
                f"obligation does not exactly descend from sources: {row['cut_path_id']}"
            )


def mutation_regressions(
    obligations: list[dict[str, Any]],
    paths: list[dict[str, Any]],
    atom_index: dict[tuple[Any, ...], dict[str, Any]],
) -> dict[str, bool]:
    if not obligations:
        raise ValueError("mutation regressions require at least one obligation")

    def rejected(mutator) -> bool:
        trial = copy.deepcopy(obligations)
        mutator(trial)
        for row in trial:
            if "integrity_sha256" in row:
                unsigned = dict(row)
                del unsigned["integrity_sha256"]
                row["integrity_sha256"] = digest(unsigned)
        try:
            validate_obligations(trial, paths, atom_index)
        except ValueError:
            return True
        return False

    def rehash(row: dict[str, Any]) -> None:
        unsigned = dict(row)
        del unsigned["integrity_sha256"]
        row["integrity_sha256"] = digest(unsigned)

    def relabel_terminal(rows: list[dict[str, Any]]) -> None:
        rows[0]["cut_terminal_type"] = (
            "ELIGIBLE_TAIL_OPEN"
            if rows[0]["cut_terminal_type"] == "FRONTIER_UNMAPPED"
            else "FRONTIER_UNMAPPED"
        )
        rehash(rows[0])

    def promote_downstream_group(rows: list[dict[str, Any]]) -> None:
        rows[0]["downstream_field_groups"]["canonical_parent_and_QD"][
            "status"
        ] = "PROVED_L1"
        rehash(rows[0])

    tests = {
        "deleted_path_rejected": rejected(lambda rows: rows.pop()),
        "duplicate_path_rejected": rejected(lambda rows: rows.append(copy.deepcopy(rows[0]))),
        "frontier_only_domain_rejected": rejected(
            lambda rows: rows[0].__setitem__("required_domain", "FRONTIER_ONLY")
        ),
        "cut_selector_promotion_rejected": rejected(
            lambda rows: rows[0]["cut_shift_selector"].__setitem__(
                "not_downstream_selector", False
            )
        ),
        "fabricated_occurrence_edge_rejected": rejected(
            lambda rows: rows[0]["occurrence_lift"]["actual_map_edges"].append(
                {"target": "fabricated"}
            )
        ),
        "false_nonzero_support_rejected": rejected(
            lambda rows: rows[0]["cut_fields"].__setitem__(
                "numeric_coefficient_nonzero_status", "PROVED_NONZERO"
            )
        ),
        "source_terminal_relabel_rejected": rejected(relabel_terminal),
        "downstream_group_promotion_rejected": rejected(promote_downstream_group),
        "false_L2_claim_rejected": rejected(
            lambda rows: rows[0]["claim_boundary"].__setitem__(
                "new_positive_fixed_h0_L2", True
            )
        ),
    }
    if not all(tests.values()):
        raise ValueError("a TPC-143 mutation was not rejected")
    return tests


def render_jsonl(records: Iterable[dict[str, Any]]) -> bytes:
    return b"".join(canonical_bytes(record) + b"\n" for record in records)


def render_json(value: Any) -> bytes:
    return (
        json.dumps(value, sort_keys=True, indent=2, ensure_ascii=False) + "\n"
    ).encode("utf-8")


def build() -> tuple[bytes, bytes]:
    source_hashes = validate_source_chain()
    atoms = load_jsonl(ATOM_FILE)
    cuts = load_jsonl(CUT_FILE)
    atom_index: dict[tuple[Any, ...], dict[str, Any]] = {}
    for atom in atoms:
        key = scope_key_from_atom(atom)
        if key in atom_index:
            raise ValueError("duplicate exact TPC-133 scope/native tuple")
        atom_index[key] = atom

    nonsoft = [row for row in cuts if row["cut_terminal_type"] in NONSOFT]
    obligations = []
    for cut in nonsoft:
        key = scope_key_from_cut(cut)
        if key not in atom_index:
            raise ValueError(f"missing exact TPC-133 join for {cut['cut_path_id']}")
        obligations.append(build_obligation(cut, atom_index[key]))
    obligations.sort(key=lambda row: row["cut_path_id"])
    nonsoft_sorted = sorted(nonsoft, key=lambda row: row["cut_path_id"])
    validate_obligations(obligations, nonsoft_sorted, atom_index)
    mutations = mutation_regressions(obligations, nonsoft_sorted, atom_index)

    type_counts = {
        name: sum(row["cut_terminal_type"] == name for row in nonsoft)
        for name in sorted(NONSOFT)
    }
    obligations_bytes = render_jsonl(obligations)
    certificate = {
        "schema": "tpc143-frontier-lift-certificate-v1",
        "status": "PASS",
        "scope": "all nonsoft cut paths; formal support envelope, not minimal nonzero support",
        "source": {
            **source_hashes,
            "source_chain_validation": "PASS",
            "hashes_are_integrity_only": True
        },
        "census": {
            "cut_path_count": len(cuts),
            "nonsoft_path_count": len(nonsoft),
            "terminal_type_counts": type_counts,
            "obligation_count": len(obligations),
            "obligations_sha256": hashlib.sha256(obligations_bytes).hexdigest(),
            "finite_sample_empty_ETO": type_counts["ELIGIBLE_TAIL_OPEN"] == 0,
            "empty_ETO_is_asymptotic_totality": False
        },
        "proved": {
            "exact_scope_native_tuple_join": True,
            "one_obligation_per_nonsoft_path": True,
            "required_domain_all_nonsoft_ETO_plus_FUM": True,
            "P_h0_cut_identity": "PROVED_L1",
            "P_h0_cut_is_not_downstream_selector": True,
            "field_descent_criterion": "PROVED_L0"
        },
        "current_actual_status": {
            "H1.frontier_occurrence_lift": "NOT_TESTABLE",
            "H1.frontier_QD_totality": "NOT_TESTABLE",
            "H1.frontier_QZ_totality": "NOT_TESTABLE",
            "H1.frontier_G_totality": "NOT_TESTABLE",
            "H1.frontier_Ph0_downstream_totality": "NOT_TESTABLE"
        },
        "first_missing": {
            "node_id": "H1.frontier_occurrence_lift",
            "artifact": "conservative row-separated one-to-many cut-to-occurrence matrix with complete lineage"
        },
        "scoped_stop": {
            "route": "current_schema_only_downstream_label_derivation",
            "status": "STOP_DECLARED_ROUTE",
            "selected_augmented_route_stopped": False
        },
        "mutation_regression": mutations,
        "claim_boundary": {
            "actual_arithmetic_coefficient_nonzero": False,
            "new_positive_fixed_h0_L2": False,
            "frontier_scalar_oX": False,
            "endpoint_1_over_400": False,
            "prime_pair_or_twin_prime_theorem": False
        }
    }
    return obligations_bytes, render_json(certificate)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()
    obligations_bytes, certificate_bytes = build()
    outputs = {
        OUT_JSONL: obligations_bytes,
        OUT_CERT: certificate_bytes
    }
    if args.check:
        for path, expected in outputs.items():
            if not path.exists() or path.read_bytes() != expected:
                raise SystemExit(f"DRIFT: {path}")
        print("TPC-143 CHECK PASS")
    else:
        for path, content in outputs.items():
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_bytes(content)
        print("TPC-143 WRITE PASS")
    certificate = json.loads(certificate_bytes)
    print(
        json.dumps(
            {
                "nonsoft": certificate["census"]["nonsoft_path_count"],
                "ETO": certificate["census"]["terminal_type_counts"]["ELIGIBLE_TAIL_OPEN"],
                "FUM": certificate["census"]["terminal_type_counts"]["FRONTIER_UNMAPPED"],
                "first_missing": certificate["first_missing"]["node_id"]
            },
            sort_keys=True
        )
    )


if __name__ == "__main__":
    main()
